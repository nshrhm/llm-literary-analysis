# 技術コンテキスト

## 使用技術

### LLM API
- Gemini API
  - 環境変数: GEMINI_API_KEY
  - モデル定義: GEMINI_MODELS in parameters.py

- Claude API
  - 環境変数: ANTHROPIC_API_KEY
  - モデル定義: CLAUDE_MODELS in parameters.py
  - 注意: claude-3-opus-20240229は高コストのため一時的に無効化（2025/03/18）

- Grok API
  - 環境変数: XAI_API_KEY
  - エンドポイント: https://api.x.ai/v1
  - モデル定義: GROK_MODELS in parameters.py

- OpenAI API
  - 環境変数: OPENAI_API_KEY
  - エンドポイント: https://api.openai.com/v1
  - モデル定義: OPENAI_MODELS in parameters.py

## 開発環境
- Python 3.12
- 主要ライブラリ:
  - google.generativeai
  - anthropic
  - requests
  - openai
