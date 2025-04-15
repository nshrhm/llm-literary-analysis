# LLM文学解析

## 概要

このプロジェクトは、大規模言語モデル（LLM）の文学理解能力を評価する研究プロジェクトです。AIモデルが文学作品をどの程度理解し解釈できるかを分析します。

## 機能

- 複数のLLMモデルによる文学テキストの分析
- 感情分析（面白さ、驚き、悲しみ、怒り）
- バッチ処理による効率的な実験実行
- 詳細な結果分析と可視化

## サポート対象モデル

- Google Gemini（2.0/1.5シリーズ）
- Anthropic Claude（3.7/3.5/3.0シリーズ）
- X.AI Grok（2.0シリーズ）
- OpenAI（GPT-4.1/GPT-4シリーズ）
- kluster.ai DeepSeek（R1/V3シリーズ）
- kluster.ai Meta Llama（3.3/3.1シリーズ）

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

4. モデルの可用性確認：
```bash
python check_models.py
```

## 使用方法

基本的な使用方法については以下のガイドを参照してください：
- [機能ガイド](docs/guides/features.md)
- [バッチ処理ガイド](docs/guides/batch-processing.md)
- [結果フォーマットガイド](docs/guides/results.md)

## 開発者向け情報

- [プロジェクト構造](docs/developer/project-structure.md)
- [コントリビューションガイド](docs/developer/contribution.md)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
