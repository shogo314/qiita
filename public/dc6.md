---
title: 競技プログラミングでdcを使う(6/8)
tags:
  - AtCoder
  - コードゴルフ
  - 競技プログラミング
  - DC
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
ignorePublish: true
---
[1](https://qiita.com/shogo314/items/abdf5e8e9e213bafe837) [2](https://qiita.com/shogo314/items/059094162959029cce3e) [3](https://qiita.com/shogo314/items/6838b0beb84f911f0515) [4](https://qiita.com/shogo314/items/a7b6668602bb976ef940) [5](https://qiita.com/shogo314/items/2c48e1db9574ef0c61a6) \*\*6\*\* 7(執筆中)

# はじめに
前回はマクロを使ってif文のような処理を書きました。今回は、条件が「かつ」「または」で組み合わさっていたり、答えが3通り以上に分かれたりする、少し複雑な問題を扱います。新しいコマンドはほとんど出てきません。これまでのコマンドの組み合わせ方を見ていきます。

この記事ではAtCoderで使われている`GNU dc 1.5.2`で動作を確認しています。メモリの名前は前回と同じく、マクロを入れるメモリには小文字（使う順にa, b, c, …）、数値を入れるメモリには大文字（問題文の変数名）を使います。

# 3通り以上に分ける
前回の「もっと短い書き方」で、「R」を使って3つの文字列から1つを選ぶ方法を紹介しました。答えが「正・負・0」で3通りに分かれる問題では、この方法がよく使えます。

[ABC078](https://atcoder.jp/contests/abc078/tasks/abc078_a)

```
[>][<][=]?-3*Rp
```

|入力|E C|
|:-:|:-|

|出力|>|
|:-:|:-|

![a078_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc6/a078_01.png)

入力はAからFのアルファベットですが、dcでは大文字のAからFは10から15を表す数字なので、「?」でそのまま数値として読み込めます。
「-」で$X-Y$を計算し、「3\*」で3倍してから「R」に渡します。正なら「3R」と同じふるまいをして一番下の>が、負なら「-3R」と同じふるまいをして真ん中の<が、0なら何もしないので一番上の=が出力されます。$X-Y$の絶対値は1や2のこともあるので、3倍して3以上にしています。

<details><summary>もっと短い書き方</summary><div>

```
?-dd*v/61+P
```

3ページ目で紹介したように、「P」は一番上が数値ならその文字コードの文字を出力します。<、=、>の文字コードは60、61、62なので、61に$X-Y$の符号（正なら1、負なら-1、0なら0）を足して出力します。
符号は「dd\*v/」で$X-Y$を$\sqrt{(X-Y)^2}=|X-Y|$で割って求めます。$X=Y$のときは0で割ることになり「/」はエラーになりますが、スタックはそのまま残るので、一番上の0に61が足されて=が出力されます。
「P」は改行を出力しませんが、AtCoderでは末尾の改行がなくても正解になります。

</div></details>

***

[ABC030](https://atcoder.jp/contests/abc030/tasks/abc030_a)

```
[TAKAHASHI][AOKI][DRAW]?sD*rlD*-3*Rp
```

|入力|5 2 6 3|
|:-:|:-|

|出力|AOKI|
|:-:|:-|

勝率$\frac{B}{A}$と$\frac{D}{C}$を比べる代わりに、分母を払った$BC$と$AD$を比べます。「?sD\*rlD\*-」で$BC-AD$を計算すれば、あとはABC078と同じです。

***

[ABC054](https://atcoder.jp/contests/abc054/tasks/abc054_a)

```
[Bob][Alice][Draw]?B+D%rB+D%-3*Rp
```

|入力|8 6|
|:-:|:-|

|出力|Alice|
|:-:|:-|

1が一番強いので、そのままでは大小を比べられません。そこで「B+D%」で11を足して13で割った余りにすると、2から13は0から11に、1は12になり、強さの順に並びます。
「?B+D%rB+D%-」でBobの強さからAliceの強さを引き、正ならBob、負ならAlice、0ならDrawを出力します。

# 掛け算で「または」
「$x=0$または$y=0$」は「$xy=0$」と同じです。この性質を使うと、「または」の条件を1回の比較で判定できます。

[ABC073](https://atcoder.jp/contests/abc073/tasks/abc073_a)

```
[No][Yes]?A~9-r9-*0=0rp
```

|入力|29|
|:-:|:-|

|出力|Yes|
|:-:|:-|

![a073_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc6/a073_01.png)

「A~」で十の位と一の位に分け、それぞれから9を引いて掛けます。どちらかが9なら積は0です。
最後の「0=0rp」は4ページ目のABC016と同じ書き方で、積が0なら0を積んでから「r」で入れ替えるので、Yesが出力されます。

***

[ABC067](https://atcoder.jp/contests/abc067/tasks/abc067_a)

```
[Impossible][Possible]?d3Rd3R+**3%0=0rp
```

|入力|4 5|
|:-:|:-|

|出力|Possible|
|:-:|:-|

$A$、$B$、$A+B$のどれかが3で割り切れればよいので、$AB(A+B)$が3で割り切れるかを調べます。3は素数なので、積が3で割り切れることと、どれかが3で割り切れることは同じです。
「d3Rd3R」で前回と同じく$B,A$を$B,A,A,B$にし、「+\*\*」で$AB(A+B)$を計算しています。

***

[ABC047](https://atcoder.jp/contests/abc047/tasks/abc047_a)

```
[No][Yes]?sCsBsAlAlB+lC-lBlC+lA-*lAlC+lB-*0=0rp
```

|入力|10 30 20|
|:-:|:-|

|出力|Yes|
|:-:|:-|

$a+b=c$、$b+c=a$、$a+c=b$のどれかが成り立てばよいので、$(a+b-c)(b+c-a)(a+c-b)$が0かを調べます。

# マクロで「かつ」と「または」
掛け算が使えない条件では、マクロを組み合わせます。

- 「または」：条件ごとに同じマクロを実行します。前回のABC100で使った方法です。
- 「かつ」：1つ目の条件で実行するマクロの中に、2つ目の条件を書きます。

[ABC097](https://atcoder.jp/contests/abc097/tasks/abc097_a)

```
[s.[Yes]]sa[lBlC-d*lD!<a]sb[No]?d*sDsCsBsAlAlC-d*lD!<alAlB-d*lD!<bp
```

|入力|4 7 9 3|
|:-:|:-|

|出力|Yes|
|:-:|:-|

「$|a-c| \leqq d$」または「$|a-b| \leqq d$かつ$|b-c| \leqq d$」なら会話できます。絶対値を使う代わりに、2乗して$(a-c)^2 \leqq d^2$のように比べています。$d^2$はメモリDに入れています。
aは前回のABC033と同じく、一番上の答えをYesに置き換えるマクロです。何回実行しても結果は同じなので、「または」のそれぞれの条件で実行できます。
bは$(b-c)^2 \leqq d^2$ならaを実行するマクロです。$(a-b)^2 \leqq d^2$のときにbを実行するので、両方が成り立ったときだけaが実行されます。

***

[ABC046](https://atcoder.jp/contests/abc046/tasks/abc046_a)

```
[1+]sa[lClB!=a]sb1?sCsBsAlAlB!=alAlC!=bp
```

|入力|3 1 4|
|:-:|:-|

|出力|3|
|:-:|:-|

色の種類は、$a$の1種類に、「$b$が$a$と違えば1種類」と「$c$が$a$とも$b$とも違えば1種類」を足した数です。
最初に1を積み、$a \neq b$ならaで1を足します。$c$の方は「かつ」なので、$a \neq c$のときにbを実行し、その中で$b \neq c$ならaを実行します。

***

[ABC027](https://atcoder.jp/contests/abc027/tasks/abc027_a)

```
[s.lC]sa?sCsBsAlAlB+lC-lAlB=ap
```

|入力|1 1 2|
|:-:|:-|

|出力|2|
|:-:|:-|

$l_1=l_2$なら答えは$l_3$です。そうでなければ$l_3$は$l_1$か$l_2$と同じなので、答えは$l_1+l_2-l_3$です。
先に$l_1+l_2-l_3$を計算しておき、$l_1=l_2$ならaでそれを$l_3$に置き換えています。正方形のときも$l_1=l_2$なので正しく動きます。

# 並べ替え
前回の最大値と最小値の書き方を使うと、2つの数を並べ替えられます。

```
[r]sa3 5d3Rd3R<a
```

これで下に大きい方の5、上に小さい方の3が残ります。

[ABC031](https://atcoder.jp/contests/abc031/tasks/abc031_a)

```
[r]sa?d3Rd3R<a1+*p
```

|入力|31 87|
|:-:|:-|

|出力|2784|
|:-:|:-|

小さい方に1を足した方が積は大きくなります。並べ替えると上が小さい方になるので、「1+\*」で（大きい方）×（小さい方+1）を計算します。

***

[ABC019](https://atcoder.jp/contests/abc019/tasks/abc019_1)

```
[r]sa?d3Rd3R<a3Rd3Rd3R<as.d3Rd3R<ap
```

|入力|5 100 5|
|:-:|:-|

|出力|5|
|:-:|:-|

![a019_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc6/a019_01.png)

並べ替えを3回して中央値を求めます。

1. $b,c$を並べ替えて、大きい方$M$を下、小さい方$m$を上にします。
1. 「3R」で$a$を一番上に持ってきて、$m$と$a$を並べ替えます。下の方の$\max(m,a)$が残り、上の方の$\min(m,a)$は「s.」で捨てます。$\min(m,a)$は3つの中で一番小さい数なので、中央値ではありません。
1. 残った$M$と$\max(m,a)$を並べ替えると、小さい方が中央値なので、一番上を出力します。

***

[ABC066](https://atcoder.jp/contests/abc066/tasks/abc066_a)

```
[r]sa?d3Rd3R<ar3Rd3Rd3R<ars.+p
```

|入力|700 600 780|
|:-:|:-|

|出力|1300|
|:-:|:-|

安い方から2つの和を求めます。ABC019と同じように並べ替えますが、今度は$b,c$の小さい方$m$を残し、大きい方$M$と$a$を比べます。$m$と$\min(M,a)$が安い方から2つなので、その和を出力します。

# その他の問題
[ABC065](https://atcoder.jp/contests/abc065/tasks/abc065_a)

```
[[delicious]pq]sa[[dangerous]pq]sb?r-d0!<a>b[safe]p
```

|入力|4 3 6|
|:-:|:-|

|出力|safe|
|:-:|:-|

賞味期限を過ぎた日数は$B-A$です。前回のelseの書き方で、0以下ならdelicious、$X$より大きければdangerous、どちらでもなければsafeを出力します。

***

[ABC071](https://atcoder.jp/contests/abc071/tasks/abc071_a)

```
[B][A]?3RdsX-d*rlX-d*<0rp
```

|入力|5 2 7|
|:-:|:-|

|出力|B|
|:-:|:-|

距離を比べる代わりに、距離の2乗$(b-x)^2$と$(a-x)^2$を比べています。$(a-x)^2$の方が小さければ0を積み、「r」で入れ替えてAを出力します。

***

[ABC024](https://atcoder.jp/contests/abc024/tasks/abc024_a)

```
[lSlT+lC*-]sa?sKsC?sTsSlT*rlS*+lSlT+lK!>ap
```

|入力|100 200 50 20<br>40 10|
|:-:|:-|

|出力|3500|
|:-:|:-|

割引なしの料金$AS+BT$を計算し、合計人数$S+T$が$K$以上ならaで$C(S+T)$を引きます。「!>a」は「$K$が$S+T$より大きくない」ときにaを実行します。

***

[ABC018](https://atcoder.jp/contests/abc018/tasks/abc018_1)

```
[1+]sa[sX1lXlA>alXlB>alXlC>ap]sb?sA?sB?sClAlbxlBlbxlClbx
```

|入力|12<br>18<br>11|
|:-:|:-|

|出力|2<br>1<br>3|
|:-:|:-|

順位は、自分より得点の高い人数に1を足したものです。bは一番上の得点をメモリXに入れ、3人の得点と比べて順位を出力するマクロです。自分自身と比べたときは大きくないので数えられません。
同じ処理を3回するので、マクロにまとめて「lbx」で呼び出しています。

***

[ABC039](https://atcoder.jp/contests/abc039/tasks/abc039_a)

```
?sCd3Rd3R*_3R+lC*+2*p
```

|入力|2 3 4|
|:-:|:-|

|出力|52|
|:-:|:-|

表面積は$2(AB+BC+CA) = 2(AB+(A+B)C)$です。「d3Rd3R\*」で$B,A,AB$とし、「_3R」で$AB$を一番下に移してから$A+B$を計算しています。

# おわりに
ここまでの知識で解ける問題があるので[こちら](https://qiita.com/shogo314/items/fff4be1573d2f86dba2a#%E6%9D%A1%E4%BB%B6%E3%81%8C%E8%A4%87%E9%9B%91)の「条件が複雑」の箇所にある問題を解いてみましょう。
次回は、マクロで繰り返しを書く方法を勉強します。

#
[1](https://qiita.com/shogo314/items/abdf5e8e9e213bafe837) [2](https://qiita.com/shogo314/items/059094162959029cce3e) [3](https://qiita.com/shogo314/items/6838b0beb84f911f0515) [4](https://qiita.com/shogo314/items/a7b6668602bb976ef940) [5](https://qiita.com/shogo314/items/2c48e1db9574ef0c61a6) \*\*6\*\* 7(執筆中)
