---
title: RustでパーサージェネレーターParolを使い始める
tags:
  - Rust
  - Parol
private: false
updated_at: '2025-09-02T01:04:43+09:00'
id: 00ed3b8d2affd9a618ae
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
# Parolって？
READMEを読んでください
### GitHubリポジトリ
https://github.com/jsinger67/parol

### ドキュメント
https://jsinger67.github.io/

# インストール
これに従う
https://jsinger67.github.io/GettingStarted.html

```
cargo install parol
```
```
$ parol -V
parol 4.0.1
```

# プロジェクトを作る
```
parol new --bin --path ./my_grammar
cd ./my_grammar
cargo build
```

失敗します。

# 修正する
この記事を書いた理由です。

`cargo.toml` が下のようになっています。

```
[dependencies]
anyhow = "1.0"
env_logger = "0.11"
parol_runtime = "3.0"
thiserror = "2.0"

[build-dependencies]
parol = "4.0.1"
```

依存関係が間違っているのでしょうか？
下を実行すると解決します。

```
cargo add parol_runtime@4.0
cargo add scnr2
```

## 追記（2025-09-02）
`cargo 1.87.0` だと駄目でした。[これ](https://github.com/rust-lang/rust/issues/53667)が関わっていそうなので `1.88.0` 以降にしましょう

# 文法を設定しよう

サンプルがあるので参考にするといいです

https://github.com/jsinger67/parol/tree/main/examples

# Rustでレッツ自作言語ライフ！
