# モデル構成の定義

## モデルの分類

モデルはLLMタイプごとに`parameters.py`で定義されています：

```python
GEMINI_MODELS = {
    "gemini20pe": "gemini-2.0-pro-exp",
    "gemini15f": "gemini-1.5-flash-8b-latest",
    ...
}

CLAUDE_MODELS = {
    "claude37s": "claude-3-7-sonnet-20250219",
    "claude30h": "claude-3-haiku-20240307",
    ...
}
```

## 組織化の原則

- モデルIDは短縮形を使用（例：gemini20pe）
- フルネームは実際のAPIモデル名を反映
- バージョンと機能を識別子に含める
- 各モデルタイプ（Gemini/Claude）で一貫した命名規則を使用
