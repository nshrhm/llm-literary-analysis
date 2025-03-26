# LLM文学解析

このプロジェクトは、大規模言語モデル（LLM）の文学理解能力を評価する研究プロジェクトです。AIモデルが文学作品をどの程度理解し解釈できるかを分析します。

## プロジェクト概要

本プロジェクトは以下のLLMモデルをサポートしています：

### Google Gemini
- Gemini 2.0: Pro Exp, Flash Thinking Exp, Flash
- Gemini 1.5: Pro, Flash
- Gemma 3.0: 27B IT

### Anthropic Claude
- Claude 3.7: Sonnet
- Claude 3.5: Sonnet, Haiku
- Claude 3.0: Sonnet, Haiku

注：Claude-3-Opusモデル（claude-3-opus-20240229）は、API費用が高額なため一時的に無効化されています（2025/03/18現在）。

### X.AI Grok
- Grok 2.0: Latest

### OpenAI
- テキスト生成モデル：
  - GPT-4: o, o-mini
- 推論モデル：
  - O3: mini
  - O1: mini

### kluster.ai DeepSeek
- DeepSeek-R1
- DeepSeek-V3

### kluster.ai Meta Llama
- Llama 3.3: 70B Instruct Turbo
- Llama 3.1: 405B Instruct Turbo, 8B Instruct Turbo

## 機能

### コア機能
- LLMの文学解析能力の体系的評価
- 複数のLLMモデルのサポート
- 統一されたプロンプト管理
- 標準化された結果形式と集計

### 統一プロンプト管理
- 一元化されたプロンプト定義と設定
- モデル固有のフォーマット適応
- 様々なモデル要件のサポート：
  - 標準メッセージフォーマット（OpenAI, Gemini, Grok）
  - コンテンツフォーマット（Claude）
  - システムロールの制限（o1-mini）
  - 温度パラメータの扱い（o3-mini）
- 新規モデルの容易な追加

### 分析機能
- 4つの感情次元での分析：
  - 面白さ
  - 驚き
  - 悲しみ
  - 怒り
- 定量的スコアリング（0-100）と詳細な理由付け
- 自動結果集計と分析
- モデルとペルソナ間の比較分析

### バッチ処理
- コスト削減のためのバッチAPI統合：
  - OpenAI（Ver.1 - 実装済み）：
    - JSONLによる50%のコスト削減
    - モデル固有のリクエストフォーマット
    - 自動エラー回復
    - すべてのOpenAIモデルのサポート：
      - 標準モデル（gpt-4o, gpt-4o-mini）
      - 制限付きモデル（o3-mini：温度パラメータなし、o1-mini：システムロールなし）
  - Claude：Message Batches API（実装済み）
    - バッチリクエストの生成と管理
    - 最大100,000リクエスト対応
    - 29日間の結果保持
    - エラーハンドリングとリカバリ
    - 標準的なAPI機能のサポート：
      - temperature
      - max_tokens
      - system messages
      - prompt caching対応
  - kluster.ai（実装済み）：
    - DeepSeek：R1およびV3モデル
    - Llama：70B、405B、8Bモデル
    - OpenAI互換APIインターフェース
    - バッチリクエスト用JSONLフォーマット
    - 24時間処理ウィンドウ
    - ステータス監視とエラーハンドリング
    - 集計用TXTファイルの自動生成

機能詳細：
- リクエスト処理：
  - モデル固有のリクエストフォーマット
  - バッチリクエスト用JSONLフォーマット
  - 自動パラメータ検証
  - エラー防止と回復

- 実行制御：
  - 24時間処理ウィンドウ
  - プロバイダー最適化されたバッチサイズ
  - バックオフ付きステータス監視
  - 部分的成功のハンドリング

- 結果管理：
  - バッチ結果用JSONLフォーマット
  - 個別結果用標準TXTフォーマット
  - 一貫したメタデータフォーマット
  - エラーログと追跡

- エラーハンドリング：
  - モデル固有の適応
  - バックオフ付き自動リトライ
  - 部分的結果の回復
  - 詳細なエラーログ

## 必要条件

- Python 3.12
- google-generativeai>=0.3.0（Geminiモデル用）
- anthropic>=0.43.0（Claudeモデル用）
- openai>=1.0.0（GrokとOpenAIモデル用）
- python-dotenv>=1.0.0（環境変数用）

## セットアップ

1. リポジトリのクローン：
```bash
git clone https://github.com/nshrhm/llm-literary-analysis.git
cd llm-literary-analysis
```

2. 依存関係のインストール：
```bash
pip install -r requirements.txt
```

3. 環境変数の設定：
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export XAI_API_KEY="your_xai_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export KLUSTERAI_API_KEY="your_klusterai_api_key"  # DeepSeekとLlamaモデルに必要
```

## プロジェクト構造

```
llm-literary-analysis/
├── experiment_runner.py           # 統合実験ランナー
├── check_models.py               # モデル可用性チェッカー
├── parameters.py                 # 実験パラメータ
├── aggregate_experiment_results.py # 結果分析ツール
└── results/                      # 実験結果
    ├── gemini/                   # Gemini結果
    ├── claude/                   # Claude結果
    ├── grok/                     # Grok結果
    ├── openai/                   # OpenAI結果
    ├── deepseek/                 # DeepSeek結果
    └── llama/                    # Llama結果
```

## 使用方法

### 実験の実行

1. 個別モデルでの実験実行：
```bash
python grok_example.py      # Grok実験の実行
python gemini_example.py    # Gemini実験の実行
python claude_example.py    # Claude実験の実行
python openai_example.py    # OpenAI実験の実行
python deepseek_example.py  # DeepSeek実験の実行
python llama_example.py     # Llama実験の実行
```

2. バッチ処理によるOpenAI実験の実行（50%コスト削減）：
```bash
python openai_example.py --batch                    # バッチ処理で実行
python openai_example.py --status <batch_id>        # バッチジョブのステータス確認
python openai_example.py --cancel <batch_id>        # 進行中のバッチジョブのキャンセル
```

3. すべてのモデルでの実験実行：
```bash
python experiment_runner.py
```

4. モデル可用性の確認：
```bash
python check_models.py
```

### 結果の処理

1. 結果のCSV形式への集計：
```bash
python aggregate_experiment_results.py results/  # すべての結果を集計
python aggregate_experiment_results.py results/deepseek  # DeepSeekの結果のみを集計
```

このスクリプトは、すべての結果ファイルを処理し、以下を含むCSVファイルを生成します：
- メタデータ（タイムスタンプ、モデル、ペルソナなど）
- 数値評価（0-100のスコア）
- 各評価の理由付け

### 結果

#### 結果の構成
実験結果はLLMタイプごとに整理されています：
```
results/
├── gemini/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── claude/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── grok/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── openai/
│   └── p{persona}_{model}_n{trial}[_temp{temp}]_{text}.txt
├── deepseek/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
└── llama/
    └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt

注：OpenAI推論モデル（o3-mini、o1-mini）では、これらのモデルが温度設定を使用しないため、ファイル名から温度パラメータが省略されます。
```

#### 結果ファイル
各結果ファイルには以下が含まれます：
```
timestamp: [YYYY-MM-DD HH:MM:SS]
persona: [ペルソナ名]
model: [モデル名]
trial: [試行番号]
temperature: [温度値]
text: [テキスト名]
Q1value: [0-100]
Q1reason: [面白さの理由]
Q2value: [0-100]
Q2reason: [驚きの理由]
Q3value: [0-100]
Q3reason: [悲しみの理由]
Q4value: [0-100]
Q4reason: [怒りの理由]
```

#### 集計結果
`aggregate_experiment_results.py`スクリプトは、すべての結果ファイルを処理し、モデル固有のCSVファイルを生成します：

```
aggregated_results/
├── aggregated_openai_[timestamp].csv     （48結果）
├── aggregated_claude_[timestamp].csv     （60結果）
├── aggregated_gemini_[timestamp].csv     （83結果）
├── aggregated_grok_[timestamp].csv       （12結果）
├── aggregated_deepseek_[timestamp].csv   （24結果）
└── aggregated_llama_[timestamp].csv      （36結果）
```

各CSVファイルには以下が含まれます：
- 完全なメタデータ（タイムスタンプ、モデル、ペルソナなど）
- すべての感情次元の数値スコア
- 各スコアの詳細な理由付け
- エラー追跡と検証結果

## コントリビューション

コントリビューションを歓迎します！Pull Requestをお気軽に提出してください。特に以下の分野に興味があります：
- 新しいLLMモデルのサポート
- プロンプト管理機能の強化
- 結果分析の改善
- ドキュメントの翻訳

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 開発者向け

開発ドキュメントはセキュリティと保守性の理由から、`docs/`ディレクトリにローカルに保管され、公開リポジトリには含まれていません。リポジトリをクローンした後、以下でAPIリファレンスと開発者ノートを見つけることができます：

- APIドキュメント：`docs/api/`
  - OpenAI APIの実装詳細（バッチ処理、ファイル、アップロード）
  - Claude API統合ガイド（バッチ処理）
- 開発者ノート：`docs/reference/`
  - バッチ処理の実装ガイド
  - ベストプラクティスと既知の問題

注：これらのドキュメントは、開発環境と本番環境を分離して維持するため、Gitから自動的に除外されます。
