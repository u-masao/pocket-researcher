# Pocket Researcher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LLMを活用した自律調査エージェント。手軽に情報収集、概要把握。

## 概要

Pocket Researcher は、大規模言語モデル（LLM）を活用した自律調査エージェントです。
まるでポケットに小さな研究者がいるかのように、あなたが知りたいテーマについて、エージェントが自律的に情報を収集・分析し、概要をレポートします。

複雑な設定や操作は不要で、調査したいテーマを与えるだけで、手軽にリサーチを開始できることを目指しています。

このプロジェクトは、Qiitaの記事「[LLMに自律的に調査を行わせるためのフレームワーク](https://qiita.com/zazen_inu/items/5dc2ea32aa4de18c02c7)」に記載された、階層構造、自問自答、計画・実行分離といった考え方を参考に実装されています。

## 主な機能

* **自律的な情報収集:** 指定されたテーマに基づき、Web検索やAPIを利用して関連情報を収集します。
* **情報の分析と要約:** 収集した情報を整理し、重要なポイントを抽出して要約します。AIモデルを活用して精度の高い分析を行います。
* **階層的なタスク実行:** 複雑な調査テーマを小さなサブタスクに分解し、段階的に実行します。これにより、効率的な情報収集と分析が可能です。
* **シンプルなインターフェース:** ブラウザでリサーチを開始でき、直感的に操作できます。

## 動作原理

1.  ユーザーから調査テーマを受け取ります。
2.  LLMがテーマを分析し、調査計画（サブタスクのリスト）を立案します。
3.  LLMが計画に従い、必要な情報を検索したり、内容を分析したりといったサブタスクを自律的に実行します（この過程で自問自答を繰り返します）。
4.  全てのサブタスクが完了したら、最終的な調査結果をレポートとしてまとめ、出力します。

## インストール方法

1.  **リポジトリをクローン:**
    ```bash
    git clone https://github.com/u-masao/pocket-researcher.git
    cd pocket-researcher
    ```

2.  **必要なライブラリをインストール:**
    ```bash
    uv sync
    ```

3.  **設定ファイル:**

    以下のように設定ファイルをコピーしてから設定を変更します。OpenAI API の API KEY は別途取得してください。

    ```bash
    cp .env.example .env
    # nano .env や vim .env などで編集
    OPENAI_API_KEY=<your_api_key>
    ```

    利用モデルは、gpt-4o-mini のままで動かすことをおすすめします。
    動作に問題が無いことを確認したらモデルの指定を変更して見てください。
    o1-pro とか使うとかなりの金額になる気がします。

## 使用方法

以下のコマンドを使用してアプリケーションを実行します。

```bash
make run
```

## 実行例

model: o3-mini-2025-01-31

[全文はこちら](EXAMPLE.md)


$ make run
PYTHONPATH=src uv run python -m pocket_researcher.main

> 考えたいことや調べたいことを入力してください。
> 論文の形式でリサーチ結果を表示します。

> 考えたいことや調べたいことの背景と目的を書いてください:
>    (入力終了は Ctrl+D または Ctrl+Z を入力)
OpenAI Agents SDK で構築可能な AI Agent アプリケーションのなかで特に有用なものを開発しようと考えています。開発すべきサービスを特定するため調査を行います。
openai agents sdk の使い方や応用例について記載したブログ記事、技術ブログ、公式ドキュメントや公式サンプルをインターネット検索等で徹底的かつ網羅的に調査してください。既存の利用方法について体系的に分類整理してください。それらについて有用性を比較して。
> 背景と目的:

```
OpenAI Agents SDK で構築可能な AI Agent アプリケーションのなかで特に有用なものを開発しようと考えています。開発すべきサービスを特定するため調査を行います。
openai agents sdk の使い方や応用例について記載したブログ記事、技術ブログ、公式ドキュメントや公式サンプルをインターネット検索等で徹底的かつ網羅的に調査してください。既存の利用方法について体系的に分類整理してください。それらについて有用性を比較して。

```
> 回答作成中
> 背景と目的と指摘事項:

```
【要約】
・OpenAI Agents SDK を活用して、特に有用な AI Agent アプリケーションの開発を目指す。
・開発すべきサービスを明確にするため、公式ドキュメント、技術ブログ、公式サンプルなどあらゆる情報源から徹底的・網羅的に調査を実施する。
・調査結果を既存の利用方法の体系的な分類と有用性比較によって整理・評価することが目的です。

【指摘点】
・有用性の比較基準や評価軸、具体的な評価方法が明記されていないため、実験計画における評価方法の明確化が必要です。
・調査範囲の詳細（例えば、検索対象の期間や言語、技術的な制限）が不足しており、調査手法の具体性を補う必要があります。
```
> この後の処理はノンストップです。
> 背景と目的を確定して論文を作成しますか？(yes/no):
