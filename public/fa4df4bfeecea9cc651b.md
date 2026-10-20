---
title: AtCoder Beginner ContestのA問題のdcでの解答と解説1
tags:
  - AtCoder
  - コードゴルフ
  - 競技プログラミング
  - DC
private: false
updated_at: '2021-07-21T04:50:54+09:00'
id: fa4df4bfeecea9cc651b
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
**1~25** [26~50](https://qiita.com/shogo314/items/bb29ad8f6b89337d052b) [51~75](https://qiita.com/shogo314/items/ce2c73256c8e74cd8589) [76~100](https://qiita.com/shogo314/items/1fa04e8e253e745bf463)

# はじめに
ここでは[こちら](https://qiita.com/shogo314/items/fff4be1573d2f86dba2a)で簡単に書けると分類されているものに限り掲載しております。<br>入力は入力例のものを使用しています。最後の「p」は図では基本的に省略しています。
# [ABC001](https://atcoder.jp/contests/abc001/tasks/abc001_1)
<details>
<summary>??-p</summary><div>

```
??-p
```

|入力|15<br>10|
|:-:|:-:|

|出力|5|
|:-:|:-:|

![a001_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/0e14c23e-a00c-1e89-b6d4-4f8d4b42bc08.png)
</div></details>

# [ABC002](https://atcoder.jp/contests/abc002/tasks/abc002_1)
<details>
<summary>?sadla>ap</summary><div>

```
?sadla>ap
```

|入力|10 11|
|:-:|:-:|

|出力|11|
|:-:|:-:|

![a002_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/f4016567-e7fd-bf27-2588-fad5b79f0007.png)

***

|入力|100000000 10000000|
|:-:|:-:|

|出力|10000000|
|:-:|:-:|

![a002_02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/4d987eb8-b354-0ac5-ab3e-8768420d45d4.png)
</div></details>

# [ABC003](https://atcoder.jp/contests/abc003/tasks/abc003_1)
<details>
<summary>?1+5000*p</summary><div>

```
?1+5000*p
```

|入力|6|
|:-:|:-:|

|出力|35000|
|:-:|:-:|

![a003_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/c36be167-308f-4ea3-3991-b6645efe690b.png)
</div></details>

# [ABC004](https://atcoder.jp/contests/abc004/tasks/abc004_1)
<details>
<summary>?2*p</summary><div>

```
?2*p
```

|入力|1000|
|:-:|:-:|

|出力|2000|
|:-:|:-:|

![a004_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/1913e329-0429-378e-e565-2a29e0dc4be0.png)
</div></details>

# [ABC005](https://atcoder.jp/contests/abc005/tasks/abc005_1)
<details>
<summary>?r/p</summary><div>

```
?r/p
```

|入力|4 7|
|:-:|:-:|

|出力|1|
|:-:|:-:|

![a005_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/97341172-d639-318d-1d80-2d16ca732d6a.png)
</div></details>

# [ABC006](https://atcoder.jp/contests/abc006/tasks/abc006_1)
<details>
<summary>[NO][YES]0?3%=0rp</summary><div>

```
[NO][YES]0?3%=0rp
```

|入力|2|
|:-:|:-:|

|出力|NO|
|:-:|:-:|

![a006_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/991ddc7b-9e33-b17f-8d65-3c47f3523f0b.png)

***

|入力|9|
|:-:|:-:|

|出力|YES|
|:-:|:-:|

![a006_02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/6d298f41-7ff9-139b-ff69-68aa037ee3be.png)

Nが一桁なのでNに3が含まれる場合はNが3で割り切れる場合に含まれています。
</div></details>

# [ABC007](https://atcoder.jp/contests/abc007/tasks/abc007_1)
<details>
<summary>?1-p</summary><div>

```
?1-p
```

|入力|4|
|:-:|:-:|

|出力|3|
|:-:|:-:|

![a007_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/6f1a9355-1936-5cbb-323e-9930dd6b20fd.png)
</div></details>

# [ABC008](https://atcoder.jp/contests/abc008/tasks/abc008_1)
<details>
<summary>1?--p</summary><div>

```
1?--p
```

|入力|4 7|
|:-:|:-:|

|出力|4|
|:-:|:-:|

![a008_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/8fb99e43-c4ba-f780-68e4-be4921f799e1.png)

</div></details>
上のコードは私では思いつかなかったので私が書いたコードも載せます。
<details>
<summary>?r-1+p</summary><div>

```
?r-1+p
```

|入力|4 7|
|:-:|:-:|

|出力|4|
|:-:|:-:|

![a008_02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/d824f7d7-6472-721a-e5ea-5cfac6375175.png)
</div></details>

# [ABC009](https://atcoder.jp/contests/abc009/tasks/abc009_1)
<details>
<summary>?1+2/p</summary><div>

```
?1+2/p
```

|入力|2|
|:-:|:-:|

|出力|1|
|:-:|:-:|

![a009_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/e28ec43b-0168-6848-76c1-4f42181e99d0.png)
</div></details>

# [ABC011](https://atcoder.jp/contests/abc011/tasks/abc011_1)
<details>
<summary>?C%1+p</summary><div>

```
?C%1+p
```

|入力|12|
|:-:|:-:|

|出力|1|
|:-:|:-:|

![a011_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/c077de53-55db-8d99-7860-611e4254411f.png)
「C」は12と解釈されます。
</div></details>

# [ABC012](https://atcoder.jp/contests/abc012/tasks/abc012_1)
<details>
<summary>?n[ ]Pp</summary><div>

```
?n[ ]Pp
```

|入力|1 2|
|:-:|:-:|

|出力|2 1|
|:-:|:-:|

![a012_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/0a8a5c58-6f75-7a95-15a6-cf4360b04a8f.png)
空白の文字コードは32であるため、[ ]の部分は32としてもよい
</div></details>

# [ABC013](https://atcoder.jp/contests/abc013/tasks/abc013_1)
<details>
<summary>?9-p</summary><div>

```
?9-p
```

|入力|A|
|:-:|:-:|

|出力|1|
|:-:|:-:|

![a013_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/90d96458-981e-d10a-c820-70ae18d0db92.png)
</div></details>

# [ABC014](https://atcoder.jp/contests/abc014/tasks/abc014_1)
<details>
<summary>??dd4Rr%-r%p</summary><div>

```
??dd4Rr%-r%p
```

|入力|7<br>3|
|:-:|:-:|

|出力|2|
|:-:|:-:|

![a014_02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/664356f0-9ea2-8e0a-8c82-5c414d9acaad.png)

入力をa,bとします。「dd4Rr」でまずデータを意図した順に並べます。次に$b-a\%b$でいくつ買い足すかを求めますが、これだと買い足す必要がないときの答えが$b$になってしまうのでこれをbで割った余りにしています。
</div></details>
下はRのコマンドを知る前に私の書いたコードです。
<details>
<summary>?d1-?dsa/1+la*r-p</summary><div>

```
?d1-?dsa/1+la*r-p
```

|入力|7<br>3|
|:-:|:-:|

|出力|2|
|:-:|:-:|

![a014_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/1c894551-120e-62e3-15f8-c95bb35db801.png)

入力をa,bとします。$a \leqq bn$を満たす最小のnを求めて$bn-a$を答えとしています。$bn=a$となる場合のために「1-」をしています。
</div></details>

# [ABC016](https://atcoder.jp/contests/abc016/tasks/abc016_1)
<details>
<summary>[NO][YES]0?%=0rp</summary><div>

```
[NO][YES]0?%=0rp
```

|入力|1 1|
|:-:|:-:|

|出力|YES|
|:-:|:-:|

![a016_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/9e1005aa-c61a-c0bb-a321-0ed7b0cdbbb2.png)

***

|入力|2 29|
|:-:|:-:|

|出力|NO|
|:-:|:-:|

![a016_02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/758c6014-dc38-f6ab-d4cc-11d349303aac.png)
</div></details>

# [ABC017](https://atcoder.jp/contests/abc017/tasks/abc017_1)
<details>
<summary>?\*?\*?\*++A/p</summary><div>

```
?*?*?*++A/p
```

|入力|50 7<br>40 8<br>30 9|
|:-:|:-:|

|出力|94|
|:-:|:-:|

![a017_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/5501724b-f9c5-c06a-645d-ec5fda9d2f75.png)
</div></details>

# [ABC020](https://atcoder.jp/contests/abc020/tasks/abc020_a)
<details>
<summary>[chokudai][ABC]?Rp</summary><div>

```
[chokudai][ABC]?Rp
```

|入力|1|
|:-:|:-:|

|出力|ABC|
|:-:|:-:|

![a020_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/e859a451-114e-86e4-495c-c9e837b806dd.png)

***

|入力|2|
|:-:|:-:|

|出力|chokudai|
|:-:|:-:|

![a020_02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/ceb8e7ff-de43-edf8-7c68-194710ec8eee.png)
</div></details>

# [ABC023](https://atcoder.jp/contests/abc023/tasks/abc023_a)
<details>
<summary>?A~+p</summary><div>

```
?A~+p
```

|入力|23|
|:-:|:-:|

|出力|5|
|:-:|:-:|

![a023_01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1327735/30c2baa7-3eed-32e9-8dff-13d8a7548d27.png)
</div></details>

#
**1~25** [26~50](https://qiita.com/shogo314/items/bb29ad8f6b89337d052b) [51~75](https://qiita.com/shogo314/items/ce2c73256c8e74cd8589) [76~100](https://qiita.com/shogo314/items/1fa04e8e253e745bf463)
