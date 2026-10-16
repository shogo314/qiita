---
title: AtCoderのABCのA問題でdcで書きやすいものまとめ
tags:
  - AtCoder
  - コードゴルフ
  - 競技プログラミング
  - DC
private: false
updated_at: '2026-10-16T03:23:14+09:00'
id: fff4be1573d2f86dba2a
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
この記事は作成途中です。

コマンドについての解説は[こちら](https://qiita.com/shogo314/items/abdf5e8e9e213bafe837)をご覧ください。

載せているすべての簡単に書ける問題は[こちらの記事](https://qiita.com/shogo314/items/fa4df4bfeecea9cc651b "現在執筆中")で解説しています。

ABC100までの全ての問題をダブりのないように書いています。

AtCoderのdcは`GNU dc 1.5.2`です。以前の`GNU dc 1.4.1`との違いは[こちらの記事](https://qiita.com/shogo314/items/1b4833f4b66ea8f599d3)にまとめています。
# dcで簡単に書ける問題
### 単純な計算
ひとつの整数を読み込み2スタックだけの単純な計算で求まるもの
[003](https://atcoder.jp/contests/abc003/tasks/abc003_1) [004](https://atcoder.jp/contests/abc004/tasks/abc004_1) [007](https://atcoder.jp/contests/abc007/tasks/abc007_1) [009](https://atcoder.jp/contests/abc009/tasks/abc009_1) [011](https://atcoder.jp/contests/abc011/tasks/abc011_1) [013](https://atcoder.jp/contests/abc013/tasks/abc013_1) [081](https://atcoder.jp/contests/abc081/tasks/abc081_a) [089](https://atcoder.jp/contests/abc089/tasks/abc089_a)
### 複数のスタックを用いる
複数の整数を読み込み2スタック以上用いて計算を行うもの
[001](https://atcoder.jp/contests/abc001/tasks/abc001_1) [008](https://atcoder.jp/contests/abc008/tasks/abc008_1) [017](https://atcoder.jp/contests/abc017/tasks/abc017_1) [023](https://atcoder.jp/contests/abc023/tasks/abc023_a) [045](https://atcoder.jp/contests/abc045/tasks/abc045_a) [057](https://atcoder.jp/contests/abc057/tasks/abc057_a) [082](https://atcoder.jp/contests/abc082/tasks/abc082_a) [084](https://atcoder.jp/contests/abc084/tasks/abc084_a) [087](https://atcoder.jp/contests/abc087/tasks/abc087_a)
### 基本的なコマンドを用いる
d,r,s等のコマンドを用いるもの
[005](https://atcoder.jp/contests/abc005/tasks/abc005_1)


未分類
[012](https://atcoder.jp/contests/abc012/tasks/abc012_1) [014](https://atcoder.jp/contests/abc014/tasks/abc014_1) [026](https://atcoder.jp/contests/abc026/tasks/abc026_a) [036](https://atcoder.jp/contests/abc036/tasks/abc036_a) [043](https://atcoder.jp/contests/abc043/tasks/abc043_a) [044](https://atcoder.jp/contests/abc044/tasks/abc044_a) [055](https://atcoder.jp/contests/abc055/tasks/abc055_a) [068](https://atcoder.jp/contests/abc068/tasks/abc068_a) [069](https://atcoder.jp/contests/abc069/tasks/abc069_a) [070](https://atcoder.jp/contests/abc070/tasks/abc070_a) [074](https://atcoder.jp/contests/abc074/tasks/abc074_a) [076](https://atcoder.jp/contests/abc076/tasks/abc076_a)
### 単純なif
あらかじめ文字列を用意しておくようなものはこちらにした。
[002](https://atcoder.jp/contests/abc002/tasks/abc002_1) [006](https://atcoder.jp/contests/abc006/tasks/abc006_1) [016](https://atcoder.jp/contests/abc016/tasks/abc016_1) [020](https://atcoder.jp/contests/abc020/tasks/abc020_a) [034](https://atcoder.jp/contests/abc034/tasks/abc034_a) [035](https://atcoder.jp/contests/abc035/tasks/abc035_a) [042](https://atcoder.jp/contests/abc042/tasks/abc042_a) [053](https://atcoder.jp/contests/abc053/tasks/abc053_a) [058](https://atcoder.jp/contests/abc058/tasks/abc058_a) [064](https://atcoder.jp/contests/abc064/tasks/abc064_a) [086](https://atcoder.jp/contests/abc086/tasks/abc086_a) [088](https://atcoder.jp/contests/abc088/tasks/abc088_a) [091](https://atcoder.jp/contests/abc091/tasks/abc091_a) [099](https://atcoder.jp/contests/abc099/tasks/abc099_a)
# 簡単に書けないもの
自分の主観で分類した。
### 複雑なif
[028](https://atcoder.jp/contests/abc028/tasks/abc028_a) [033](https://atcoder.jp/contests/abc033/tasks/abc033_a) [037](https://atcoder.jp/contests/abc037/tasks/abc037_a) [040](https://atcoder.jp/contests/abc040/tasks/abc040_a) [052](https://atcoder.jp/contests/abc052/tasks/abc052_a) [063](https://atcoder.jp/contests/abc063/tasks/abc063_a) [072](https://atcoder.jp/contests/abc072/tasks/abc072_a) [080](https://atcoder.jp/contests/abc080/tasks/abc080_a) [083](https://atcoder.jp/contests/abc083/tasks/abc083_a) [092](https://atcoder.jp/contests/abc092/tasks/abc092_a) [094](https://atcoder.jp/contests/abc094/tasks/abc094_a) [096](https://atcoder.jp/contests/abc096/tasks/abc096_a) [097](https://atcoder.jp/contests/abc097/tasks/abc097_a) [098](https://atcoder.jp/contests/abc098/tasks/abc098_a) [100](https://atcoder.jp/contests/abc100/tasks/abc100_a)
### 条件が複雑
#### dcが最短
[024](https://atcoder.jp/contests/abc024/tasks/abc024_a) [030](https://atcoder.jp/contests/abc030/tasks/abc030_a) [031](https://atcoder.jp/contests/abc031/tasks/abc031_a) [032](https://atcoder.jp/contests/abc032/tasks/abc032_a) [039](https://atcoder.jp/contests/abc039/tasks/abc039_a) [065](https://atcoder.jp/contests/abc065/tasks/abc065_a) [067](https://atcoder.jp/contests/abc067/tasks/abc067_a) [078](https://atcoder.jp/contests/abc078/tasks/abc078_a)
#### dcでの解答がある
[018](https://atcoder.jp/contests/abc018/tasks/abc018_1) [019](https://atcoder.jp/contests/abc019/tasks/abc019_1) [027](https://atcoder.jp/contests/abc027/tasks/abc027_a) [046](https://atcoder.jp/contests/abc046/tasks/abc046_a) [047](https://atcoder.jp/contests/abc047/tasks/abc047_a) [054](https://atcoder.jp/contests/abc054/tasks/abc054_a) [062](https://atcoder.jp/contests/abc062/tasks/abc062_a) [066](https://atcoder.jp/contests/abc066/tasks/abc066_a) [071](https://atcoder.jp/contests/abc071/tasks/abc071_a) [073](https://atcoder.jp/contests/abc073/tasks/abc073_a) [079](https://atcoder.jp/contests/abc079/tasks/abc079_a) [085](https://atcoder.jp/contests/abc085/tasks/abc085_a)
#### dcでは解けない
入力の負の数が引き算として実行され、答えが違う入力を区別できないもの
[061](https://atcoder.jp/contests/abc061/tasks/abc061_a) [075](https://atcoder.jp/contests/abc075/tasks/abc075_a)
### 繰り返し
書けないことはないがfor文をdcでわざわざ書く必要は無い
[021](https://atcoder.jp/contests/abc021/tasks/abc021_a) [022](https://atcoder.jp/contests/abc022/tasks/abc022_a)
### 文字列を読み込む必要がある
#### dcで解ける
入力がコマンドとして実行されることを利用するもの
[050](https://atcoder.jp/contests/abc050/tasks/abc050_a) [056](https://atcoder.jp/contests/abc056/tasks/abc056_a) [095](https://atcoder.jp/contests/abc095/tasks/abc095_a)
#### dcでは解けない
[010](https://atcoder.jp/contests/abc010/tasks/abc010_1) [015](https://atcoder.jp/contests/abc015/tasks/abc015_1) [025](https://atcoder.jp/contests/abc025/tasks/abc025_a) [029](https://atcoder.jp/contests/abc029/tasks/abc029_a) [038](https://atcoder.jp/contests/abc038/tasks/abc038_a) [041](https://atcoder.jp/contests/abc041/tasks/abc041_a) [048](https://atcoder.jp/contests/abc048/tasks/abc048_a) [049](https://atcoder.jp/contests/abc049/tasks/abc049_a) [051](https://atcoder.jp/contests/abc051/tasks/abc051_a) [059](https://atcoder.jp/contests/abc059/tasks/abc059_a) [060](https://atcoder.jp/contests/abc060/tasks/abc060_a) [077](https://atcoder.jp/contests/abc077/tasks/abc077_a) [090](https://atcoder.jp/contests/abc090/tasks/abc090_a) [093](https://atcoder.jp/contests/abc093/tasks/abc093_a)
