#!/usr/bin/env python3
"""dcのスタックの変化を図にする。

定義ファイル（TOML）に書いた図をまとめてPNGにする。

    python3 tools/dcstack.py images/dc2.toml          # すべての図を作る
    python3 tools/dcstack.py images/dc2.toml b02_04   # 指定した図だけ作る

定義ファイルの書き方:

    [defaults]            # 省略可。すべての図に適用される
    font = "/path/to/font.ttc"
    scale = 1.0
    # base_url = "https://..."  # 画像の URL の前半（省略すると GitHub の main ブランチ）

    [b02_04]              # 図の名前。<定義ファイル名>/b02_04.png に出力される
    setup = "6 8"         # 最初の状態を作るコード（矢印にはならない）
    code = "+"            # 1コマンドごとに矢印にするコード
    # steps = ["6 8", "+"]  # code の代わりに、矢印ごとのコードを並べてもよい
    # labels = ["8を足す"]  # 矢印のラベル（省略するとコードがそのまま入る）
    # input = "5 3\\n9"     # ? で読み込む入力
    # wrap = 5              # 1行に並べる状態の数（長い図を折り返す）
"""

import argparse
import re
import subprocess
import sys
import tomllib
from fractions import Fraction
from math import cos, hypot, isqrt, radians, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# dc の再現
# ---------------------------------------------------------------------------

DIGITS = "0123456789ABCDEF"


class Num:
    """dc の数値。v / 10**s を表す。"""

    __slots__ = ("v", "s")

    def __init__(self, v, s=0):
        self.v = v
        self.s = s

    @staticmethod
    def of(x):
        return Num(int(x), 0)

    def scaled(self, s):
        """小数点以下を s 桁にする（減らすときは0方向に切り捨て）。"""
        if s >= self.s:
            return Num(self.v * 10 ** (s - self.s), s)
        return Num(tdiv(self.v, 10 ** (self.s - s)), s)

    def to_int(self):
        return tdiv(self.v, 10**self.s)

    def __str__(self):
        if self.v == 0:
            return "0"
        sign = "-" if self.v < 0 else ""
        a = abs(self.v)
        if self.s == 0:
            return sign + str(a)
        ip, fp = divmod(a, 10**self.s)
        return sign + (str(ip) if ip else "") + "." + str(fp).zfill(self.s)


def tdiv(a, b):
    """0方向に切り捨てる整数除算。"""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def to_str_base(n, base):
    """出力の基数が base のときの表記。"""
    if base == 10:
        return str(n)
    if n.v == 0:
        return "0"
    a = abs(n.v)
    ip, fp = divmod(a, 10**n.s)
    if base <= 16:
        fmt, sep = (lambda d: DIGITS[d]), ""
    else:
        # 16 より大きい基数では、各桁を空白区切りの10進数で書く
        w = len(str(base - 1))
        fmt, sep = (lambda d: str(d).zfill(w)), " "
    ds = []
    while ip:
        ip, d = divmod(ip, base)
        ds.append(d)
    out = "".join(sep + fmt(d) for d in reversed(ds))
    if n.s:
        # base**m >= 10**s となる最小の m 桁まで出す（切り捨て）
        m = 0
        while base**m < 10**n.s:
            m += 1
        f = Fraction(fp, 10**n.s)
        fd = []
        for _ in range(m):
            f *= base
            fd.append(int(f))
            f -= int(f)
        out += "." + sep.join(fmt(d) for d in fd)
    return ("-" if n.v < 0 else "") + out


def show(x):
    """スタックの値を図に描くときの表記。"""
    return f"[{x}]" if isinstance(x, str) else str(x)


class DCError(Exception):
    """dc のエラー。keep が真なら、取り出した値は戻さない。"""

    def __init__(self, msg, keep=False):
        super().__init__(msg)
        self.keep = keep


class Halt(Exception):
    """q でプログラムが終了した。"""


def warn(msg):
    print(f"dcstack: {msg}", file=sys.stderr)


class DC:
    """GNU dc 1.5.2（AtCoder のバージョン）の動作を再現するインタプリタ。"""

    MAX_COMMANDS = 10**6

    def __init__(self, input_text=""):
        self.stack = []
        self.regs = {}  # レジスタ名 -> [(値, 配列)] のスタック
        self.k = 0
        self.ibase = 10
        self.obase = 10
        self.lines = input_text.splitlines()
        self.out = []
        self.halted = False
        self.count = 0

    # -- 補助 ---------------------------------------------------------------

    def pop(self):
        if not self.stack:
            raise DCError("stack empty")
        return self.stack.pop()

    def need(self, n):
        if len(self.stack) < n:
            raise DCError("stack empty")

    def num(self, x):
        if not isinstance(x, Num):
            raise DCError("non-numeric value")
        return x

    def pop_nums(self, n):
        """数値を n 個取り出す（深い方から順に返す）。失敗したらスタックは変えない。"""
        self.need(n)
        xs = self.stack[-n:]
        for x in xs:
            self.num(x)
        del self.stack[-n:]
        return xs

    def pop_arg(self):
        """整数の引数を取り出す。数値でなければ None。"""
        x = self.pop()
        return x.to_int() if isinstance(x, Num) else None

    def reg(self, r):
        return self.regs.setdefault(r, [])

    def write(self, s):
        self.out.append(s)

    def format_num(self, n):
        s = to_str_base(n, self.obase)
        # GNU dc は70文字ごとに \ を付けて改行する
        lines = []
        while len(s) > 69:
            lines.append(s[:69] + "\\")
            s = s[69:]
        lines.append(s)
        return "\n".join(lines)

    # -- 実行 ---------------------------------------------------------------

    def run(self, code):
        """code をトップレベルのプログラムとして実行する。"""
        if self.halted:
            return
        frames = [[code, 0]]
        try:
            while frames:
                frame = frames[-1]
                code, i = frame
                if i >= len(code):
                    frames.pop()
                    continue
                self.count += 1
                if self.count > self.MAX_COMMANDS:
                    raise Halt("実行したコマンド数が多すぎます（無限ループ？）")
                frame[1] = self.step(code, i, frames)
        except Halt as e:
            if e.args:
                warn(e.args[0])
            self.halted = True

    def call(self, frames, code):
        """マクロを実行する。末尾呼び出しならフレームを積まない。"""
        top = frames[-1]
        if len(frames) > 1 and top[1] >= len(top[0]):
            frames.pop()
        frames.append([code, 0])

    def quit_levels(self, frames, n, from_q):
        # frames[0] はトップレベル。マクロは frames[1:]
        macros = len(frames) - 1
        if from_q and n >= macros + 1:
            raise Halt()
        n = min(n, macros)
        del frames[len(frames) - n :]
        if not frames:
            frames.append(["", 0])

    def step(self, code, i, frames):
        """code[i] から始まるコマンドを1つ実行し、次の位置を返す。"""
        c = code[i]
        j = i + 1
        snapshot = list(self.stack)
        try:
            if c in " \t\r\n":
                pass
            elif c == "#":
                while j < len(code) and code[j] != "\n":
                    j += 1
            elif c in DIGITS or c in "._":
                n, j = self.read_number(code, i)
                self.stack.append(n)
            elif c == "[":
                depth = 1
                while j < len(code) and depth:
                    depth += {"[": 1, "]": -1}.get(code[j], 0)
                    j += 1
                if depth:
                    raise DCError("unterminated string")
                self.stack.append(code[i + 1 : j - 1])
            elif c in "slSL:;<>=":
                if j >= len(code):
                    raise DCError(f"'{c}' にレジスタ名がありません")
                j += 1
                self.register_command(c, code[j - 1], frames)
            elif c == "!":
                if j < len(code) and code[j] in "<>=":
                    if j + 1 >= len(code):
                        raise DCError(f"'!{code[j]}' にレジスタ名がありません")
                    j += 2
                    self.register_command("!" + code[j - 2], code[j - 1], frames)
                else:
                    raise DCError("! によるシェルコマンドは未対応です")
            else:
                self.simple_command(c, frames)
        except DCError as e:
            if not e.keep:
                self.stack[:] = snapshot
            warn(f"{e}（{code[i:j]!r}）")
        return j

    def read_number(self, code, i):
        j = i
        neg = False
        if code[j] == "_":
            neg = True
            j += 1
        ip = Fraction(0)
        while j < len(code) and code[j] in DIGITS:
            ip = ip * self.ibase + DIGITS.index(code[j])
            j += 1
        fp = Fraction(0)
        nfrac = 0
        if j < len(code) and code[j] == ".":
            j += 1
            while j < len(code) and code[j] in DIGITS:
                nfrac += 1
                fp += Fraction(DIGITS.index(code[j]), self.ibase**nfrac)
                j += 1
        v = ip + fp
        n = Num(int(v * 10**nfrac), nfrac)  # 小数部分は nfrac 桁で切り捨て
        if neg:
            n.v = -n.v
        return n, j

    def register_command(self, c, r, frames):
        rs = self.reg(r)
        if c == "s":
            x = self.pop()
            if rs:
                rs[-1] = (x, rs[-1][1])
            else:
                rs.append((x, {}))
        elif c == "S":
            rs.append((self.pop(), {}))
        elif c == "l":
            self.stack.append(rs[-1][0] if rs else Num(0))
        elif c == "L":
            if not rs:
                raise DCError(f"stack register '{r}' is empty")
            self.stack.append(rs.pop()[0])
        elif c == ":":
            idx = self.pop_arg()
            x = self.pop()
            if idx is None or idx < 0:
                raise DCError("array index must be a nonnegative integer")
            if not rs:
                rs.append((Num(0), {}))
            rs[-1][1][idx] = x
        elif c == ";":
            idx = self.pop_arg()
            if idx is None or idx < 0:
                raise DCError("array index must be a nonnegative integer")
            self.stack.append(rs[-1][1].get(idx, Num(0)) if rs else Num(0))
        else:
            a, b = self.pop_nums(2)  # b が一番上
            s = max(a.s, b.s)
            diff = b.scaled(s).v - a.scaled(s).v
            ok = {">": diff > 0, "<": diff < 0, "=": diff == 0}[c[-1]]
            if c.startswith("!"):
                ok = not ok
            if ok:
                self.execute_value(rs[-1][0] if rs else Num(0), frames)

    def execute_value(self, x, frames):
        if isinstance(x, str):
            self.call(frames, x)
        else:
            self.stack.append(x)

    def simple_command(self, c, frames):
        k = self.k
        if c == "p":
            self.need(1)
            x = self.stack[-1]
            self.write((x if isinstance(x, str) else self.format_num(x)) + "\n")
        elif c == "n":
            x = self.pop()
            self.write(x if isinstance(x, str) else self.format_num(x))
        elif c == "P":
            x = self.pop()
            if isinstance(x, str):
                self.write(x)
            else:
                i = abs(x.to_int())
                bs = [i % 256]
                i //= 256
                while i:
                    i, b = divmod(i, 256)
                    bs.append(b)
                self.write(bytes(reversed(bs)).decode("latin-1"))
        elif c == "f":
            for x in reversed(self.stack):
                self.write((x if isinstance(x, str) else self.format_num(x)) + "\n")
        elif c == "+" or c == "-":
            a, b = self.pop_nums(2)
            s = max(a.s, b.s)
            v = a.scaled(s).v + (b.scaled(s).v if c == "+" else -b.scaled(s).v)
            self.stack.append(Num(v, s))
        elif c == "*":
            a, b = self.pop_nums(2)
            self.stack.append(Num(a.v * b.v, a.s + b.s).scaled(min(a.s + b.s, max(k, a.s, b.s))))
        elif c == "/":
            a, b = self.pop_nums(2)
            self.stack.append(self.div(a, b))
        elif c == "%":
            a, b = self.pop_nums(2)
            self.stack.append(self.mod(a, b))
        elif c == "~":
            a, b = self.pop_nums(2)
            q, r = self.div(a, b), self.mod(a, b)
            self.stack += [q, r]
        elif c == "^":
            a, b = self.pop_nums(2)
            e = b.to_int()
            if b.s and b.v % 10**b.s:
                if e == 0:
                    # GNU dc 1.5.2 は整数部分が 0 の小数の指数をエラーにする
                    raise DCError("exponent too large in raise")
                warn("Runtime warning: non-zero scale in exponent（小数部分は無視されます）")
            if e >= 0:
                p = Num(a.v**e, a.s * e)
                self.stack.append(p.scaled(min(a.s * e, max(k, a.s))))
            else:
                if a.v == 0:
                    self.stack.append(Num(0))
                    return
                self.stack.append(self.div(Num(1), Num(a.v ** (-e), a.s * (-e))))
        elif c == "|":
            a, b, m = self.pop_nums(3)
            if any(x.s and x.v % 10**x.s for x in (a, b, m)):
                warn("| の小数は未対応なので整数部分だけで計算します（GNU dc とは結果が違うことがあります）")
            a, b, m = a.to_int(), b.to_int(), m.to_int()
            if m == 0:
                raise DCError("remainder by zero")
            if b < 0:
                raise DCError("negative exponent")
            r = pow(abs(a), b, abs(m))
            if a < 0 and b % 2:
                r = -r
            self.stack.append(Num.of(r))
        elif c == "v":
            a = self.num(self.pop())
            if a.v < 0:
                raise DCError("square root of negative number")
            if a.v == 0 or a.v == 10**a.s:
                # GNU dc は 0 と 1 の平方根を小数点以下0桁で返す
                self.stack.append(Num(a.v // 10**a.s))
                return
            t = max(k, a.s)
            self.stack.append(Num(isqrt(a.v * 10 ** (2 * t - a.s)), t))
        elif c == "c":
            self.stack.clear()
        elif c == "d":
            self.need(1)
            self.stack.append(self.stack[-1])
        elif c == "r":
            self.need(2)
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif c == "R":
            x = self.pop()
            if not isinstance(x, Num):
                raise DCError("rotation count must be numeric")
            n = x.to_int()
            if n > 0:
                n = min(n, len(self.stack))
                if n:
                    self.stack.append(self.stack.pop(-n))
            elif n < 0:
                n = min(-n, len(self.stack))
                if n:
                    x = self.stack.pop()
                    self.stack.insert(len(self.stack) - n + 1, x)
        elif c == "k":
            n = self.pop_arg()
            if n is None or n < 0:
                raise DCError("scale must be a nonnegative number")
            self.k = n
        elif c == "K":
            self.stack.append(Num.of(self.k))
        elif c == "i":
            n = self.pop_arg()
            if n is None or not 2 <= n <= 16:
                raise DCError("input base must be a number between 2 and 16 (inclusive)")
            self.ibase = n
        elif c == "I":
            self.stack.append(Num.of(self.ibase))
        elif c == "o":
            n = self.pop_arg()
            if n is None or n < 2:
                raise DCError("output base must be a number greater than 1")
            self.obase = n
        elif c == "O":
            self.stack.append(Num.of(self.obase))
        elif c == "z":
            self.stack.append(Num.of(len(self.stack)))
        elif c == "Z":
            x = self.pop()
            if isinstance(x, str):
                self.stack.append(Num.of(len(x)))
            else:
                a = abs(x.v)
                self.stack.append(Num.of(len(str(a)) if a else 1))
        elif c == "X":
            x = self.pop()
            self.stack.append(Num.of(0 if isinstance(x, str) else x.s))
        elif c == "a":
            warn("'a' command is deprecated（GNU dc 1.5.2 は警告を出します）")
            x = self.pop()
            if isinstance(x, str):
                self.stack.append(x[:1])
            else:
                self.stack.append(chr(x.to_int() % 256))
        elif c == "x":
            self.execute_value(self.pop(), frames)
        elif c == "?":
            if not self.lines:
                raise Halt()  # 入力の終わりでは dc を終了する
            self.call(frames, self.lines.pop(0) + "\n")
        elif c == "q":
            self.quit_levels(frames, 2, True)
        elif c == "Q":
            n = self.pop_arg()
            if n is None or n < 0:
                raise DCError("Q command requires a number >= 0")
            if n > len(frames) - 1:
                # 抜けられるだけ抜けてからエラーにする（取り出した値は戻さない）
                self.quit_levels(frames, n, False)
                raise DCError("Q command argument exceeded string execution depth", keep=True)
            self.quit_levels(frames, n, False)
        else:
            raise DCError(f"'{c}' (0{ord(c):o}) unimplemented")

    def div(self, a, b):
        if b.v == 0:
            raise DCError("divide by zero")
        k = self.k
        return Num(tdiv(a.v * 10 ** (k + b.s), b.v * 10**a.s), k)

    def mod(self, a, b):
        if b.v == 0:
            raise DCError("remainder by zero")
        q = self.div(a, b)
        s = max(a.s, b.s + self.k)
        qb = Num(q.v * b.v, q.s + b.s)
        return Num(a.scaled(s).v - qb.scaled(s).v, s)


def split_commands(code):
    """dc のコードを1コマンドずつに分ける（空白とコメントは捨てる）。"""
    out = []
    i = 0
    while i < len(code):
        c = code[i]
        j = i + 1
        if c in " \t\r\n":
            i = j
            continue
        if c == "#":
            while j < len(code) and code[j] != "\n":
                j += 1
            i = j
            continue
        if c in DIGITS or c in "._":
            seen_dot = c == "."
            while j < len(code) and (code[j] in DIGITS or (code[j] == "." and not seen_dot)):
                seen_dot |= code[j] == "."
                j += 1
        elif c == "[":
            depth = 1
            while j < len(code) and depth:
                depth += {"[": 1, "]": -1}.get(code[j], 0)
                j += 1
        elif c in "slSL:;<>=":
            j += 1
        elif c == "!" and j < len(code) and code[j] in "<>=":
            j += 2
        out.append(code[i:j])
        i = j
    return out


# ---------------------------------------------------------------------------
# 描画
# ---------------------------------------------------------------------------

FONT_CANDIDATES = [
    "/mnt/c/Windows/Fonts/YuGothR.ttc",
    "C:/Windows/Fonts/YuGothR.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf",
]

# 寸法（scale = 1 のときのピクセル数）
CELL_W = 520  # スタックの箱の最小の幅
CELL_H = 130  # スタックの箱1段の高さ
FLOOR_PAD = 65  # 床が箱からはみ出す長さ
FLOOR_GAP = 260  # 床と床の間隔
FLOOR_T = 12  # 床の太さ
LINE_W = 4  # 箱と矢印の線の太さ
FONT_SIZE = 76
TEXT_PAD = 60  # 箱の中の文字の左右の余白
ARROW_GAP = 65  # 矢印の始点・終点とスタックの間隔
ARROW_H = 130  # 矢印の弧の高さ
ARROW_IN = 130  # 矢印の端が床の端から内側に入る長さ
ARROW_END = 350  # 弧の終わりの角度（360 で真下を向く）
HEAD_LEN = 60  # 矢じりの長さ
HEAD_W = 80  # 矢じりの幅
LABEL_GAP = 30  # ラベルと矢印の間隔
MARGIN = 20
ROW_GAP = 40  # 折り返したときの行の間隔
SUPERSAMPLE = 3


def find_font(path):
    if path:
        return path
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return p
    sys.exit("dcstack: 日本語フォントが見つかりません。定義ファイルの [defaults] に font を指定してください")


def render(states, labels, font_path, scale=1.0, wrap=0):
    """states: 各段階のスタック（下から順の表記のリスト）。labels: 矢印のラベル。

    wrap を指定すると、1行に wrap 個の状態を並べて折り返す。
    """
    u = scale * SUPERSAMPLE

    def px(x):
        return round(x * u)

    font = ImageFont.truetype(font_path, px(FONT_SIZE))
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))

    def text_w(t):
        return probe.textbbox((0, 0), t, font=font, anchor="ls")[2]

    cell_w = max([px(CELL_W)] + [text_w(t) + 2 * px(TEXT_PAD) for s in states for t in s])
    floor_w = cell_w + 2 * px(FLOOR_PAD)
    pitch = floor_w + px(FLOOR_GAP)
    cell_h = px(CELL_H)

    def row(states, labels):
        """1行分の図を描く。"""
        # まず床を y = 0 として座標を計算し、あとで全体をずらす
        def top(s):
            return -cell_h * len(s)

        arrows = []
        for n, label in enumerate(labels):
            x0 = n * pitch + floor_w - px(ARROW_IN)
            x1 = (n + 1) * pitch + px(ARROW_IN)
            y = min(top(states[n]), top(states[n + 1])) - px(ARROW_GAP)
            arrows.append((x0, x1, y, label))

        asc, desc = font.getmetrics()
        min_y = min([top(s) for s in states] + [y - px(ARROW_H) - px(LABEL_GAP) - asc - desc for *_, y, _ in arrows])
        oy = -min_y + px(MARGIN)
        width = pitch * (len(states) - 1) + floor_w
        height = oy + px(FLOOR_T) + px(MARGIN)

        img = Image.new("L", (width, height), 255)
        d = ImageDraw.Draw(img)
        lw = max(1, px(LINE_W))

        for n, s in enumerate(states):
            fx = n * pitch
            d.rectangle([fx, oy, fx + floor_w, oy + px(FLOOR_T)], fill=0)
            bx = fx + px(FLOOR_PAD)
            if not s:
                continue
            # 外枠を描いてから、段の境目に1本ずつ線を引く（線が二重にならないように）
            d.rectangle([bx, oy - cell_h * len(s), bx + cell_w, oy], outline=0, width=lw)
            for h, t in enumerate(s):
                y1 = oy - cell_h * h
                if h:
                    d.rectangle([bx, y1 - lw // 2, bx + cell_w, y1 - lw // 2 + lw - 1], fill=0)
                d.text((bx + cell_w / 2, y1 - cell_h / 2), t, font=font, fill=0, anchor="mm")

        for x0, x1, y, label in arrows:
            y += oy
            h = px(ARROW_H)
            # 上半分の楕円で弧を描き、終点に弧の向きに沿った矢じりを付ける
            d.arc([x0, y - h, x1, y + h], 180, ARROW_END, fill=0, width=lw)
            cx, cy, a = (x0 + x1) / 2, y, (x1 - x0) / 2
            t = radians(ARROW_END)
            ex, ey = cx + a * cos(t), cy + h * sin(t)
            tx, ty = -a * sin(t), h * cos(t)
            norm = hypot(tx, ty)
            tx, ty = tx / norm, ty / norm
            hl, hw = px(HEAD_LEN), px(HEAD_W) / 2
            d.polygon(
                [(ex + tx * hl, ey + ty * hl), (ex - ty * hw, ey + tx * hw), (ex + ty * hw, ey - tx * hw)],
                fill=0,
            )
            if label:
                d.text(((x0 + x1) / 2, y - h - px(LABEL_GAP)), label, font=font, fill=0, anchor="md")

        return img

    # wrap 個ずつの状態で行を折り返す。次の行は前の行の最後の状態から始める
    per = wrap - 1 if wrap and wrap >= 2 else max(1, len(labels))
    rows = [row(states[i : i + per + 1], labels[i : i + per]) for i in range(0, max(1, len(labels)), per)]
    width = max(r.width for r in rows)
    gap = px(ROW_GAP)
    img = Image.new("L", (width, sum(r.height for r in rows) + gap * (len(rows) - 1)), 255)
    y = 0
    for r in rows:
        img.paste(r, (0, y))
        y += r.height + gap
    width, height = img.size
    return img.resize((round(width / SUPERSAMPLE), round(height / SUPERSAMPLE)), Image.LANCZOS)


# ---------------------------------------------------------------------------
# 定義ファイルの処理
# ---------------------------------------------------------------------------


def image_url(path, base_url):
    """記事に貼る画像の URL。base_url がなければ GitHub の origin と main ブランチから作る。"""
    path = path.resolve()
    try:
        root = Path(git("rev-parse", "--show-toplevel", cwd=path.parent))
        rel = path.relative_to(root).as_posix()
        if base_url:
            return base_url.rstrip("/") + "/" + rel
        m = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", git("remote", "get-url", "origin", cwd=root))
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return None
    if not m:
        return None
    return f"https://raw.githubusercontent.com/{m[1]}/{m[2]}/main/{rel}"


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def build(name, spec, defaults, out_dir):
    opts = {**defaults, **spec}
    unknown = set(opts) - {"setup", "code", "steps", "labels", "input", "font", "scale", "base_url", "wrap"}
    if unknown:
        sys.exit(f"dcstack: [{name}] に不明なキーがあります: {', '.join(sorted(unknown))}")
    if ("code" in opts) == ("steps" in opts):
        sys.exit(f"dcstack: [{name}] には code か steps のどちらか一方を書いてください")
    steps = split_commands(opts["code"]) if "code" in opts else list(opts["steps"])
    labels = list(opts.get("labels", steps))
    if len(labels) != len(steps):
        sys.exit(f"dcstack: [{name}] の labels の数（{len(labels)}）が矢印の数（{len(steps)}）と合いません")

    dc = DC(opts.get("input", ""))
    dc.run(opts.get("setup", ""))
    states = [[show(x) for x in dc.stack]]
    for st in steps:
        dc.run(st)
        states.append([show(x) for x in dc.stack])

    img = render(states, labels, find_font(opts.get("font")), opts.get("scale", 1.0), opts.get("wrap", 0))
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.png"
    img.save(path, optimize=True)

    output = "".join(dc.out)
    print(f"{path}")
    if output:
        print("  出力: " + output.rstrip("\n").replace("\n", "\n        "))
    url = image_url(path, opts.get("base_url"))
    if url:
        print(f"  ![{name}.png]({url})")


def main():
    ap = argparse.ArgumentParser(description="dcのスタックの変化を図にする")
    ap.add_argument("toml", type=Path, help="図の定義ファイル")
    ap.add_argument("names", nargs="*", help="作る図の名前（省略するとすべて）")
    ap.add_argument("-o", "--out-dir", type=Path, help="出力先（省略すると定義ファイルと同名のディレクトリ）")
    args = ap.parse_args()

    with open(args.toml, "rb") as f:
        conf = tomllib.load(f)
    defaults = conf.pop("defaults", {})
    out_dir = args.out_dir or args.toml.with_suffix("")
    names = args.names or list(conf)
    for name in names:
        if name not in conf:
            sys.exit(f"dcstack: [{name}] は定義ファイルにありません")
        build(name, conf[name], defaults, out_dir)


if __name__ == "__main__":
    main()
