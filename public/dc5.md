---
title: 競技プログラミングでdcを使う(5/8)
tags:
  - AtCoder
  - コードゴルフ
  - 競技プログラミング
  - DC
private: false
updated_at: '2026-10-15T15:30:52+09:00'
id: 2c48e1db9574ef0c61a6
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
[1](https://qiita.com/shogo314/items/abdf5e8e9e213bafe837) [2](https://qiita.com/shogo314/items/059094162959029cce3e) [3](https://qiita.com/shogo314/items/6838b0beb84f911f0515) [4](https://qiita.com/shogo314/items/a7b6668602bb976ef940) **5** 6(執筆中)

# はじめに
前回は比較のコマンドを使って、何も入れていないメモリの0を積むだけの問題を扱いました。今回はメモリに「マクロ」を入れることで、普通のプログラミング言語のif文のような処理を書いていきます。

この記事ではAtCoderで使われている`GNU dc 1.5.2`で動作を確認しています。

# マクロ
3ページ目で、文字列は[*characters*]と書いてスタックに積めることを紹介しました。「x」はスタックの一番上の文字列を取り出し、それをコードとして実行します。このようにコードとして実行する文字列をマクロと呼びます。

```
3[2*]xp
```

|出力|6|
|:-:|:-|

![b05_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/b05_01.png)

「[2\*]」を積んだあと、「x」でそれを取り出して実行しています。「3 2\*p」と書いたのと同じ結果になります。なお、一番上が数値のときに「x」を使うと、取り出した数値をそのまま積み直すので何も起きません。

***

マクロはメモリに入れておくと何度でも使えます。

```
[2*]sa3laxlaxp
```

|出力|12|
|:-:|:-|

![b05_02.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/b05_02.png)

「la」でマクロを積んで「x」で実行するのを2回繰り返しているので、3に2を2回掛けています。

# 比較とマクロ
前回紹介した「>*x*」などは、条件が成り立つと*x*を実行するコマンドでした。*x*にマクロを入れておけば、条件が成り立ったときだけそのマクロが実行されます。これでif文が書けます。

[ABC072](https://atcoder.jp/contests/abc072/tasks/abc072_a)
$X-t$を出力すればよいですが、負になるときは0を出力します。

```
[s.0]sa?-d0>ap
```

|入力|48 58|
|:-:|:-|

|出力|0|
|:-:|:-|

![a072_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a072_01.png)

「s.」は「.」という名前のメモリに値を入れるコマンドですが、ここでは一番上の値を捨てるために使っています。
「d0>a」で計算結果を複製してから0と比べます。0の方が大きい、つまり計算結果が負のときにaが実行され、計算結果を捨てて0を積みます。
このように「条件が成り立ったら値を置き換える」マクロはよく使います。

<details><summary>もっと短い書き方</summary><div>

この問題はマクロを使わずに次のようにも書けます。

```
?-kKp
```

「k」は一番上の数値を取り出して小数点以下の桁数に設定し、「K」は今の桁数をスタックに積むコマンドです。桁数は最初は0です。

|入力|100 17|
|:-:|:-|

|出力|83|
|:-:|:-|

![a072_02.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a072_02.png)

計算結果が0以上のときは、「k」で桁数に設定した値を「K」で積み直すだけなので、そのまま出力されます。

|入力|48 58|
|:-:|:-|

|出力|0|
|:-:|:-|

![a072_03.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a072_03.png)

計算結果が負のときは、桁数に負の値は設定できないので「k」はエラーになり、桁数は0のままです。そのため「K」で0が積まれ、それが出力されます。エラーメッセージは標準エラー出力に出ますが、AtCoderでは標準出力だけで判定されるので問題ありません。

</div></details>

***

[ABC033](https://atcoder.jp/contests/abc033/tasks/abc033_a)
4桁とも同じ数字ならSAME、そうでなければDIFFERENTを出力します。4桁とも同じ数字であることは、1111で割り切れることと同じです。

```
[s.[SAME]]sa[DIFFERENT]?1111%0=ap
```

|入力|2222|
|:-:|:-|

|出力|SAME|
|:-:|:-|

![a033_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a033_01.png)

先に答えの候補として「DIFFERENT」を積んでおき、条件が成り立ったら「SAME」に置き換えています。入力が0000のときも、「?」で読み込むと0になるので正しく動きます。

<details><summary>もっと短い書き方</summary><div>

3ページ目で紹介した「R」を使うと、マクロを使わずに次のようにも書けます。

```
[DIFFERENT][SAME]?AB1%1+Rp
```

「AB1」は$10 \times 100 + 11 \times 10 + 1$で1111です。1111で割り切れるときは余りが0なので、「1+」で1になります。「1R」は何もしないので、一番上のSAMEが出力されます。
割り切れないときは「1+」で2以上になります。「R」はnがデータの数より大きいとき、nがデータの数と同じときのふるまいをするので、一番下のDIFFERENTが一番上に来て出力されます。

</div></details>

***

置き換えるだけでなく、値に何かを足すこともできます。

[ABC096](https://atcoder.jp/contests/abc096/tasks/abc096_a)
1月1日からa月b日までに、月と日が同じ日が何日あるかを求めます。1月からa-1月までに1日ずつあり、さらに$a \leqq b$ならa月a日も含まれます。

```
[1+]sx?sbd1-rlb!<xp
```

|入力|5 5|
|:-:|:-|

|出力|5|
|:-:|:-|

![a096_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a096_01.png)

「!<x」は一番上の数値が二番目の数値より小さくないときにxを実行するので、$b \geqq a$のときに1を足しています。

<details><summary>もっと短い書き方</summary><div>

```
?sbdlbr/0r^-p
```

「?sbdlbr/」で$a$と$b \div a$（切り捨て）を積みます。$a \leqq b$なら$b \div a$は1以上、そうでなければ0です。
次に「0r^」で$0^{b \div a}$を計算します。$b \div a$が1以上なら0、0なら$0^0=1$になります。最後に「-」で$a$から引くので、$a \leqq b$なら$a$、そうでなければ$a-1$が出力されます。

</div></details>

# elseの書き方
「q」はマクロの実行をやめて、そのマクロを呼び出したマクロからも抜けるコマンドです。比較のコマンドから直接呼び出したマクロの中で「q」を使うと、プログラム自体が終了します。
これを使うと、条件が成り立ったときは答えを出力して終了し、成り立たなかったときだけその後ろのコードを実行する、というelseのような書き方ができます。

[ABC063](https://atcoder.jp/contests/abc063/tasks/abc063_a)
$A+B$が10以上ならerror、そうでなければ$A+B$を出力します。

```
[[error]pq]sa?+d9<ap
```

|入力|6 3|
|:-:|:-|

|出力|9|
|:-:|:-|

![a063_01.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a063_01.png)

|入力|6 4|
|:-:|:-|

|出力|error|
|:-:|:-|

![a063_02.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/a063_02.png)

2つめの例では「<a」でaが実行され、「error」を出力したあと「q」で終了するので、最後の「p」は実行されません。

<details><summary>もっと短い書き方</summary><div>

```
[error]?+dZRp
```

「Z」は一番上の数値を取り出して、その桁数を積むコマンドです。$A+B$が10未満なら1、10以上なら2が積まれます。
1のときは「1R」は何もしないので、$A+B$が出力されます。2のときは「2R」で下にある「error」が一番上に来るので、errorが出力されます。

</div></details>

***

同じ書き方で、3つ以上に分けることもできます。

[ABC083](https://atcoder.jp/contests/abc083/tasks/abc083_a)

```
[[Left]pq]sa[[Right]pq]sb?+-+d0<a0>b[Balanced]p
```

|入力|3 8 7 1|
|:-:|:-|

|出力|Left|
|:-:|:-|

「?+-+」で$(A+B)-(C+D)$を計算しています。「+」で$C+D$、「-」で$B-(C+D)$、もう一度「+」で$A+B-(C+D)$となるので、演算子の順番に注意してください。
計算結果が正ならLeft、負ならRightを出力して終了し、どちらでもなければBalancedを出力します。

<details><summary>もっと短い書き方</summary><div>

```
[Left][Right][Balanced]?+-+3*Rp
```

「?+-+」で$A+B-(C+D)$を計算し、「3*」で3倍してから「R」に渡します。
0のときは「0R」は何もしないので、一番上のBalancedが出力されます。
正のときは3以上になるので、「R」は「3R」と同じふるまいをして、一番下のLeftが一番上に来ます。
「R」に負の数$-n$を渡すと、逆向きに回して一番上を上から$n$番目に移します。負のときは-3以下になるので「-3R」と同じふるまいをして、Balancedが一番下に移り、Rightが一番上に来ます。

</div></details>

***

[ABC028](https://atcoder.jp/contests/abc028/tasks/abc028_a)

```
[[Perfect]pq]sa[[Great]pq]sb[[Good]pq]sc?d99<ad89<b59<c[Bad]p
```

|入力|80|
|:-:|:-|

|出力|Good|
|:-:|:-|

点数の大きい方から順に比べていきます。最初に成り立った条件で出力して終了するので、「60点以上89点以下」のような範囲を書かなくて済みます。最後の比較では点数を複製しないので、「59<c」で点数がスタックから消えます。

<details><summary>もっと短い書き方</summary><div>

```
[Bad][Good]dd[Great][Perfect]B?A/-Rp
```

「d」でGoodを3つにして、下からBad、Good、Good、Good、Great、Perfectの6つを積みます。
「B?A/-」で$11 - N \div 10$（切り捨て）を計算します。100点なら1、90点台なら2、80点台から60点台なら3から5、59点以下なら6以上になります。
「R」は一番上から数えてその番目にある文字列を一番上に持ってくるので、それぞれPerfect、Great、Good、Badが出力されます。6より大きい数は6と同じふるまいをするので、59点以下はすべてBadになります。

</div></details>

***

同じマクロを2回使えば「または」が書けます。

[ABC100](https://atcoder.jp/contests/abc100/tasks/abc100_a)
AとBのどちらかが8より大きければ「:(」、そうでなければ「Yay!」を出力します。

```
[[:(]pq]sa?8<a8<a[Yay!]p
```

|入力|11 4|
|:-:|:-|

|出力|:(|
|:-:|:-|

比較のコマンドは2つの値を取り出すので、1回目の「8<a」ではBと、2回目の「8<a」ではAと比べることになります。

<details><summary>もっと短い書き方</summary><div>

```
[Yay!][:(]?8<08<0rp
```

前回と同じく、何も入れていないメモリ0を実行して0を積む方法です。「8<0」は、比べた値が8より大きければ0を1つ積みます。
Bが8より大きいときは、1回目の「8<0」で0が積まれます。2回目の「8<0」ではAの代わりにこの0と比べるので何も積まれず、スタックは下からYay!、:(、Aになります。
Bが8以下でAが8より大きいときは、2回目の「8<0」で0が積まれ、スタックは下からYay!、:(、0になります。
どちらも最後の「r」で一番上と2番目が入れ替わり、:(が一番上に来ます。AもBも8以下のときは何も積まれないので、「r」でYay!が一番上に来ます。

</div></details>

***

[ABC094](https://atcoder.jp/contests/abc094/tasks/abc094_a)
$A \leqq X \leqq A+B$ならYES、そうでなければNOを出力します。

```
[[NO]pq]sn?sxsbsalalx<nlalb+lx>n[YES]p
```

|入力|3 5 4|
|:-:|:-|

|出力|YES|
|:-:|:-|

値を何度も使うので、いったん全てメモリに入れています。$X<A$と$X>A+B$のどちらかが成り立てばNOを出力して終了します。どちらも成り立たなければ$A \leqq X \leqq A+B$なのでYESを出力します。

<details><summary>もっと短い書き方</summary><div>

```
[YES][NO]?rk-dK+*0<0rp
```

「r」でBとXを入れ替え、「k」でBを小数点以下の桁数として取っておきます。「K」で取り出せるので、メモリの代わりに使えます。値は整数なので、計算結果は変わりません。
「-dK+*」で$(A-X)(A-X+B)$を計算します。$A \leqq X \leqq A+B$のとき、またそのときに限り$A-X \leqq 0 \leqq A-X+B$となるので、この値は0以下になります。
「0<0」は値が0より大きいとき、つまり答えがNOのときだけ0を積みます。あとはABC100の短い書き方と同じく、「r」でNOかYESが一番上に来ます。

</div></details>

# 最大値と最小値
2つの数の大きい方を残したいときは、次のように書きます。

```
[r]sr3 5d3Rd3R<rs.p
```

|出力|5|
|:-:|:-|

![b05_03.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/b05_03.png)

「d3Rd3R」で、上から$b,a$と積まれているスタックを、上から$b,a,a,b$にしています。上の2つを「<r」で比べて、$b<a$なら残った2つを「r」で入れ替えます。こうすると残った2つは大きい方が下になるので、「s.」で上を捨てれば大きい方が残ります。

```
[r]sr5 3d3Rd3R<rs.p
```

|出力|5|
|:-:|:-|

![b05_04.png](https://raw.githubusercontent.com/shogo314/qiita/main/images/dc5/b05_04.png)

小さい方を残したいときは「<r」を「>r」にします。

***

[ABC052](https://atcoder.jp/contests/abc052/tasks/abc052_a)

```
[r]sr?*sb*lbd3Rd3R<rs.p
```

|入力|3 5 2 7|
|:-:|:-|

|出力|15|
|:-:|:-|

2つの長方形の面積を計算して、大きい方を出力しています。

<details><summary>もっと短い書き方</summary><div>

```
?*sY*dlY>Yp
```

メモリに数値を入れておくと、比較のコマンドでそのメモリを実行したときにその数値が積まれます。これを使うと「r」を入れたマクロがいりません。
「?\*sY」で$C \times D$をYに入れ、「\*」で$A \times B$を計算します。「dlY>Y」で$C \times D$の方が大きければYを実行して$C \times D$を積むので、一番上は大きい方になります。
小さい方の値がスタックに残ることがありますが、「p」は一番上だけを出力するので問題ありません。

</div></details>

***

[ABC080](https://atcoder.jp/contests/abc080/tasks/abc080_a)

```
[r]sr?sb*lbd3Rd3R>rs.p
```

|入力|7 17 120|
|:-:|:-|

|出力|119|
|:-:|:-|

$A \times N$と$B$の小さい方を出力しています。

<details><summary>もっと短い書き方</summary><div>

```
?sB*dlB<Bp
```

ABC052の短い書き方と同じ方法です。$B$をメモリBに入れ、$B$の方が小さければBを実行して$B$を積みます。

</div></details>

***

[ABC092](https://atcoder.jp/contests/abc092/tasks/abc092_a)

```
[r]sr??d3Rd3R>rs.??d3Rd3R>rs.+p
```

|入力|600<br>300<br>220<br>420|
|:-:|:-|

|出力|520|
|:-:|:-|

電車とバスそれぞれで安い方を選んで、足しています。

<details><summary>もっと短い書き方</summary><div>

```
[x?d?-dd*v+2/-]dx+p
```

$A$と$B$の小さい方は$A - \max(A-B, 0)$で、$\max(x, 0)$は$x$と$|x|$の平均です。$|x|$は「d\*v」で$\sqrt{x^2}$として計算できるので、「?d?-dd\*v+2/-」で小さい方が求まります。
同じ処理を2回するために、マクロを「d」で2つにしてから「x」で実行しています。実行したマクロは最初の「x」でもう1つのマクロを実行するので、処理が2回行われます。2つ目のマクロの「x」はスタックが空なのでエラーになりますが、エラーメッセージが出るだけで何も起こりません。

</div></details>

***

[ABC037](https://atcoder.jp/contests/abc037/tasks/abc037_a)

```
[r]sr?scd3Rd3R>rs.lcr/p
```

|入力|3 5 6|
|:-:|:-|

|出力|2|
|:-:|:-|

$C$を$A,B$の小さい方で割っています。

<details><summary>もっと短い書き方</summary><div>

```
?sCsBdlB<BlCr/p
```

ABC052の短い書き方と同じ方法で$A,B$の小さい方を一番上にしてから、「lCr/」で$C$を割っています。

</div></details>

***

[ABC040](https://atcoder.jp/contests/abc040/tasks/abc040_a)

```
[r]sr?dsx-lx1-d3Rd3R>rs.p
```

|入力|5 2|
|:-:|:-|

|出力|1|
|:-:|:-|

$n-x$と$x-1$の小さい方を出力しています。

<details><summary>もっと短い書き方</summary><div>

```
?d1-sa-dla<ap
```

$x-1$をメモリaに入れ、「-」で$n-x$を計算します。ABC052の短い書き方と同じ方法で、$x-1$の方が小さければaを実行して積みます。

</div></details>

# おわりに
ここまでの知識で解ける問題があるので[こちら](https://qiita.com/shogo314/items/fff4be1573d2f86dba2a#%E8%A4%87%E9%9B%91%E3%81%AAif)の「複雑なif」の箇所にある問題を解いてみましょう。
次回は条件が複雑な問題を扱います。

#
[1](https://qiita.com/shogo314/items/abdf5e8e9e213bafe837) [2](https://qiita.com/shogo314/items/059094162959029cce3e) [3](https://qiita.com/shogo314/items/6838b0beb84f911f0515) [4](https://qiita.com/shogo314/items/a7b6668602bb976ef940) **5** 6(執筆中)
