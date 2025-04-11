# モデル構成の定義（2025-04-11更新）

## モデル定義と制御

### モデル分類
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

LLAMA_MODELS = {
    "llama33-70Bit": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
    "llama31-405Bit": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
    "llama31-8Bit": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo"
}
```

## 組織化の原則

- モデルIDは短縮形を使用（例：gemini20pe）
- フルネームは実際のAPIモデル名を反映
- バージョンと機能を識別子に含める
- 各モデルタイプ（Gemini/Claude/Llama）で一貫した命名規則を使用

## モデル制御パターン（2025-04-11追加）

### Geminiモデル設定
```python
GEMINI_CONFIG = {
    "gemini20pe": {
        "model_name": "gemini-2.0-pro-exp",
        "supports_temperature": True,
        "supports_pattern_matching": True,
        "retry_limit": 3,
        "format_validation": True
    },
    "gemini15f": {
        "model_name": "gemini-1.5-flash-8b-latest",
        "supports_temperature": True,
        "supports_pattern_matching": True,
        "retry_limit": 3,
        "format_validation": True
    }
}
```

### 温度制御設定
```python
TEMPERATURE_CONTROL = {
    "gemini": {
        "base_range": (0.0, 1.0),
        "supports_persona": True,
        "supports_text_modifier": True,
        "pattern_matching": True,
        "validation": {
            "enabled": True,
            "patterns": [
                "標準形式",
                "代替形式1",
                "代替形式2",
                "シンプル形式",
                "日本語形式1",
                "日本語形式2",
                "括弧形式",
                "角括弧形式"
            ],
            "retry_limit": 3
        }
    }
}
```

### 品質管理設定
```python
QUALITY_CONTROL = {
    "gemini": {
        "response_validation": {
            "required_fields": ["面白さ", "驚き", "悲しみ", "怒り"],
            "value_range": (0, 100),
            "format_check": True,
            "reason_required": True
        },
        "error_handling": {
            "max_retries": 3,
            "backoff_factor": 1.5,
            "retry_on_pattern_mismatch": True
        },
        "monitoring": {
            "track_pattern_usage": True,
            "track_retry_rate": True,
            "track_validation_success": True
        }
    }
}
```

## モデル特性（2025-04-11追加）

### Geminiモデルの特徴
1. プロンプト制御
   - システム/ユーザーメッセージの分離
   - 強化された形式指定
   - 明示的な数値範囲指定

2. パターンマッチング
   - 8種類の応答パターン対応
   - 段階的マッチング処理
   - エラー耐性の向上

3. 品質管理
   - 応答形式の検証
   - 自動再試行メカニズム
   - 結果の一貫性確保

4. モニタリング
   - パターン使用率の追跡
   - 検証成功率の監視
   - エラー発生率の分析
