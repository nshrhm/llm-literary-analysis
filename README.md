# LLM文学解析

## 概要

このプロジェクトは、大規模言語モデル（LLM）の文学理解能力を評価する研究プロジェクトです。AIモデルが文学作品をどの程度理解し解釈できるかを分析します。

## 機能

- 複数のLLMモデルによる文学テキストの分析
- 感情分析（面白さ、驚き、悲しみ、怒り）
- バッチ処理による効率的な実験実行（50%のコスト削減を実現）
- 高度なパターンマッチングによる結果検証
- モデル選択機能による柔軟な実験実行（2025-04-24追加）
- 詳細な結果分析と可視化

## サポート対象モデル（2025-04-19更新）

### Google Gemini（2.5/2.0シリーズ）
- Gemini 2.5 Flash Preview
  - 40実験結果の生成完了（4ペルソナ × 1テキスト × 10トライアル）
  - バッチ処理の安定性確認済み
  - パターンマッチングによる応答形式の一貫性確保
- その他：Pro、Flash、Flash Thinking

### OpenAI（GPT-4.1/GPT-4シリーズ）
- GPT-4.1シリーズ（価格情報）：
  - gpt-4.1: 高精度解析用（入力$2.00、キャッシュ入力$0.50、出力$8.00）
  - gpt-4.1-mini: 一般解析用（入力$0.40、キャッシュ入力$0.10、出力$1.60）
  - gpt-4.1-nano: 軽量解析用（入力$0.10、キャッシュ入力$0.025、出力$0.40）
- バッチ処理による50%のコスト削減を実現
- 全360実験結果の生成完了（3モデル × 4ペルソナ × 3テキスト × 10トライアル）

### その他のサポートモデル（2025-04-25更新）
- Anthropic Claude（3.7/3.5/3.0シリーズ）
- X.AI Grok（2.0シリーズ）
- kluster.ai DeepSeek（R1/V3シリーズ）
- kluster.ai Meta Llama（4.0/3.3シリーズ）
  - チェック機能実装完了
  - OpenAI互換APIを使用
  - モデル可用性の簡易確認機能

詳細は[モデルガイド](docs/guides/models.md)を参照してください。

## 必要条件

- Python 3.12
- google-generativeai>=0.3.0（Geminiモデル用）
- anthropic>=0.43.0（Claudeモデル用）
- openai>=1.0.0（GrokとOpenAIモデル用）
- python-dotenv>=1.0.0（環境変数用）

## クイックスタート

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
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

4. モデルの可用性確認（2025-04-25更新）：
```bash
# すべてのモデルの可用性を確認
python check_models.py

# 特定のモデルの可用性を確認
# OpenAI
python openai_example.py --check
# Claude
python claude_example.py --check
# Gemini
python gemini_example.py --check
# Grok
python grok_example.py --check
# DeepSeek
python deepseek_example.py --check
# Llama（2025-04-25追加）
python llama_example.py --check
```

## 使用方法

### バッチ処理実行
各バッチ処理の実装と実行例:
```bash
# OpenAIバッチ処理
python openai_example.py --batch [--model gpt-4.1 gpt-4.1-mini]

# Claudeバッチ処理
python claude_example.py --batch [--model claude37s claude35s]

# DeepSeekバッチ処理
python deepseek_batch_example.py [--model deepseekr1 deepseekv3]

# Llamaバッチ処理
python llama_batch_example.py [--model llama4-maveric llama4-scout]
```

### モデル選択実行（2025-04-24追加）
各モデルのexampleスクリプトで特定のモデルを選択実行できます：
```bash
# OpenAIモデルの選択実行
python openai_example.py --model gpt-4.1 gpt-4.1-mini

# Claudeモデルの選択実行
python claude_example.py --model claude-3 claude-3-haiku

# Geminiモデルの選択実行
python gemini_example.py --model gemini20p gemini20pe

# Grokモデルの選択実行
python grok_example.py --model grok20 grok20e

# DeepSeekモデルの選択実行
python deepseek_example.py --model deepseek-r1 deepseek-v3

# Llamaモデルの選択実行
python llama_example.py --model llama70b llama405b
```

### モデルIDと正式名称の対応
モデル選択実行に使用する短縮モデルIDと対応する正式モデル名については、詳細は[モデルガイド](docs/guides/models.md#モデル選択ガイド)を参照してください。

### 基本的な使用方法
- [機能ガイド](docs/guides/features.md)
- [バッチ処理ガイド](docs/guides/batch-processing.md)
- [結果フォーマットガイド](docs/guides/results.md)

### 高度な機能

#### インテリジェント温度設定
- ペルソナ特性に基づく基本温度調整：
  - 大学1年生（0.7）：柔軟な解釈を促進
  - 文学研究者（0.4）：分析的なアプローチを重視
  - 感情豊かな詩人（0.9）：創造的な表現を最大化
  - 無感情なロボット（0.1）：一貫性のある判断を維持

#### 品質保証機能
- 8種類のパターンマッチングによる応答検証
- 自動エラー検出と再試行メカニズム
- 結果フォーマットの厳密な検証
- 日本語テキスト処理の最適化

#### バッチ処理最適化
- JSONLフォーマットによる効率的な処理
- モデル別の最適化戦略
- キャッシュ機能による入力コストの削減
- 処理状況のリアルタイムモニタリング

## 開発者向け情報

- [プロジェクト構造](docs/developer/project-structure.md)
- [コントリビューションガイド](docs/developer/contribution.md)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
