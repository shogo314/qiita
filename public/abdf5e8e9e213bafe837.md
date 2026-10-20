---
title: 競技プログラミングでdcを使う(1/8)
tags:
  - AtCoder
  - コードゴルフ
  - 競技プログラミング
  - DC
private: false
updated_at: '2026-10-16T04:39:09+09:00'
id: abdf5e8e9e213bafe837
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
**1** [2](https://qiita.com/shogo314/items/059094162959029cce3e) [3](https://qiita.com/shogo314/items/6838b0beb84f911f0515) [4](https://qiita.com/shogo314/items/a7b6668602bb976ef940) [5](https://qiita.com/shogo314/items/2c48e1db9574ef0c61a6) [6](https://qiita.com/shogo314/items/b3995de81116b7ca5465) [7](https://qiita.com/shogo314/items/23ac5a98e316802bed87) [8](https://qiita.com/shogo314/items/50c4fe35128b1027ccc1)

# はじめに
この記事はAtCoderのABCのA問題をdcで解くためのものです。
私は全くの初心者であり、ネットで適当に拾ってきた情報から自分なりに解釈したものなので間違っている部分があればお教えください。C言語やPythonなどの一般的な言語を扱える（A問題やB問題がその言語で解ける）ことを前提としているので、説明をとばしている部分があります。

dcを勉強するにあたって[こちら](https://kazmax.zpp.jp/cmd/d/dc.1.html)のページ（以下、参考ページ）を参考にしました。

この連載では、AtCoderで使われている`GNU dc 1.5.2`で動作を確認しています。以前のAtCoderで使われていた`GNU dc 1.4.1`との違いは[こちらの記事](https://qiita.com/shogo314/items/1b4833f4b66ea8f599d3)にまとめています。
# dcについて
まずdcが何かについては[Wikipedia](https://ja.wikipedia.org/wiki/Dc_(UNIX) "dc (UNIX)")でも見てください。私はそもそもUNIXが何かすらわかっていません。私が認識しているのはAtCoderで使える言語の中で単純な計算問題ならばdcが最も短く書けるということだけです。ただ速く解きたいだけの私にはそれで十分なのです。
# 本題
この記事と対応するように問題を分類した記事を作成しました。
[AtCoderのABCのA問題でdcで書きやすいものまとめ](https://qiita.com/shogo314/items/fff4be1573d2f86dba2a#%E5%8D%98%E7%B4%94%E3%81%AA%E8%A8%88%E7%AE%97)
# 単純な計算
実際に問題を見ていきましょう。<br>[ABC004](https://atcoder.jp/contests/abc004/tasks/abc004_1)<br>数字をひとつ読み込んでそれを二倍したものを出力すればよいです。コードは

```
?2*p
```

こうなります。短いですね。これを読み解くと、<br>「?」で数字を読み込む→「2\*」で読み込んだ数字に2を掛ける→「p」でその数字を出力する<br>
という流れになります。「2」と「\*」の順番が気になると思いますが、2を掛けるという言葉の通りの順番だと解釈しましょう。
「\*」以外にも「+」「-」「/」「%」などが同様に扱えます。また「^」で累乗の計算もできます。
***
少し練習しましょう。<br>[ABC007](https://atcoder.jp/contests/abc007/tasks/abc007_1)<br>数字をひとつ読み込んでそれから1引いたものを出力すればよいです。

```
?1-p
```
***
2回以上の演算も行えます。<br>[ABC009](https://atcoder.jp/contests/abc009/tasks/abc009_1)<br>読み込んだ数字を2で割って切り上げたものを出力すればよいです。<br>つまり読み込んだ数字に1を足して2で割ります。
<details><summary>1を足す理由</summary>ほとんどの言語において整数の割り算は計算結果を切り下げたものになります。dcはちょっと複雑なのですが、A問題を解くときは数字は常に整数型であると思っておいて問題ないでしょう。このような切り捨てになる割り算において、切り上げの計算にしたいときは、割られる数に割る数を足して1引いておきます。つまり
⌈a÷b⌉=⌊(a+b-1)÷b⌋ (⌈⌉:天井関数 ⌊⌋:床関数 [参考](https://ja.wikipedia.org/wiki/%E5%BA%8A%E9%96%A2%E6%95%B0%E3%81%A8%E5%A4%A9%E4%BA%95%E9%96%A2%E6%95%B0))
となります。if文を使う必要がなくなるので是非覚えておきましょう。</details>

```
?1+2/p
```

普通なら「*」や「/」を「+」よりも先に計算しますがdcでは言葉で説明したときと同じ順になります。
***
dcでは「A」「B」「C」「D」「E」「F」はそれぞれ「10」「11」「12」「13」「14」「15」と解釈されます。なぜか微妙に16進数を採用しているのです。また、おもしろいことに「BD」と書くと「123」と認識されます。これは10の位に11が入って、1の位に13が入るためです。

[ABC013](https://atcoder.jp/contests/abc013/tasks/abc013_1)

```
?9-p
```

「?」は本来文字は読めないのですが、この問題で使う文字はA~Eなので読めてしまいます。
# おわりに
これらの知識だけで解ける問題があるので[こちら](https://qiita.com/shogo314/items/fff4be1573d2f86dba2a#%E5%8D%98%E7%B4%94%E3%81%AA%E8%A8%88%E7%AE%97)の「単純な計算」の箇所にある問題を解いてみましょう。

ここまででも十分速くなりますが、残念ながらA問題といえども、これだけで解ける問題は少ないです。次の記事ではスタックについて勉強します。

#
**1** [2](https://qiita.com/shogo314/items/059094162959029cce3e) [3](https://qiita.com/shogo314/items/6838b0beb84f911f0515) [4](https://qiita.com/shogo314/items/a7b6668602bb976ef940) [5](https://qiita.com/shogo314/items/2c48e1db9574ef0c61a6) [6](https://qiita.com/shogo314/items/b3995de81116b7ca5465) [7](https://qiita.com/shogo314/items/23ac5a98e316802bed87) [8](https://qiita.com/shogo314/items/50c4fe35128b1027ccc1)
