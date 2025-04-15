## バッチ処理ガイドライン

## コア原則

1. 単一モデルのバッチ処理
   - 各バッチは単一のモデルのみを含む
   - 異なるモデルは別バッチで処理
   - システム全体で一貫したモデル識別子を使用

2. モデル識別
   - 標準化されたモデル識別子を使用
   - 識別子と表示名のマッピングを維持
   - 一貫した命名規則に従う

3. ファイル命名と構成
   - 標準化されたファイル命名パターン
   - モデル識別子をファイル名に含める
   - メタデータの一貫性を維持

## 実装ノート

### モデル識別子の処理（2025-04-15更新）

1. モデル識別子フォーマット
```python
def _get_model_identifier(model: str) -> str:
    # GPT-4.1シリーズ
    if model_id == "gpt-4.1":
        return "gpt-4.1"
    elif model_id == "gpt-4.1-mini":
        return "gpt-4.1-mini"
    elif model_id == "gpt-4.1-nano":
        return "gpt-4.1-nano"
    
    # DeepSeekモデル
    elif model_id == "deepseekr1":
        return "deepseekr1"
    elif model_id == "deepseekv3":
        return "deepseekv3"
    elif model_id == "deepseekv3-0324":
        return "deepseekv3-0324"

    # Llamaモデル
    elif model_id == "llama33-70Bit":
        return "llama33-70Bit"
    elif model_id == "llama31-405Bit":
        return "llama31-405Bit"
    elif model_id == "llama31-8Bit":
        return "llama31-8Bit"
```

2. 表示名生成
```python
def _get_model_display_name(model: str) -> str:
    # GPT-4.1シリーズ
    if model_id == "gpt-4.1":
        return "GPT-4.1"
    elif model_id == "gpt-4.1-mini":
        return "GPT-4.1 Mini"
    elif model_id == "gpt-4.1-nano":
        return "GPT-4.1 Nano"
    
    # DeepSeek表示名
    elif model_id == "deepseekr1":
        return "DeepSeek-R1"
    elif model_id == "deepseekv3":
        return "DeepSeek-V3"
    elif model_id == "deepseekv3-0324":
        return "DeepSeek-V3-0324"

    # Llama表示名
    elif model_id == "llama33-70Bit":
        return "Llama-3.3-70B"
    elif model_id == "llama31-405Bit":
        return "Llama-3.1-405B"
    elif model_id == "llama31-8Bit":
        return "Llama-3.1-8B"
```

3. 価格情報管理（2025-04-15追加）
```python
def get_model_pricing(model: str) -> Dict:
    if model_id == "gpt-4.1":
        return {
            "input": 2.00,
            "cached_input": 0.50,
            "output": 8.00
        }
    elif model_id == "gpt-4.1-mini":
        return {
            "input": 0.40,
            "cached_input": 0.10,
            "output": 1.60
        }
    elif model_id == "gpt-4.1-nano":
        return {
            "input": 0.10,
            "cached_input": 0.025,
            "output": 0.40
        }
    return None
```

### リクエストフォーマット

1. モデル固有の適応（2025-03-27更新）
```python
def create_batch_requests(model: str, ...) -> List[Dict]:
    # モデル識別子と表示名を取得
    model_identifier = _get_model_identifier(model)
    model_display_name = _get_model_display_name(model)

    # モデル固有のカスタムID生成
    custom_id = f"{persona_id}_{model_identifier}_{text_id}_{trial_num}"
    if not is_reasoning_model(model_identifier):
        custom_id += f"_temp{temperature}"

    # モデル表示名を含むリクエスト作成
    request = {
        "custom_id": custom_id,
        "model_display_name": model_display_name,
        ...
    }
```

### エラーハンドリング

1. バリデーションルール
   - モデル識別子フォーマットの検証
   - 表示名の一貫性チェック
   - ファイル命名パターンの検証

2. 処理チェック
   - モデルタイプの一貫性確認
   - メタデータフォーマットの検証
   - 識別子マッピングの確認

3. 結果管理
   - 結果内のモデル名の検証
   - 表示名の一貫性確保
   - ファイル命名規則の遵守

## ベストプラクティス

1. モデル識別
   - 一貫した識別子フォーマットを使用
   - 明確な識別子-表示名マッピングを維持
   - モデル命名規則を文書化

2. ファイル構成
   - 標準化された命名パターンに従う
   - パスにモデル識別子を含める
   - メタデータの一貫性を維持

3. ドキュメント
   - モデル識別子を文書化
   - 命名規則を最新に保つ
   - 識別子マッピングを維持

## 結果管理

1. ファイル命名
   - ファイル名にモデル識別子を使用
   - 標準化されたパターンに従う
   - 必要なコンポーネントをすべて含める

2. メタデータ
   - モデル表示名を含める
   - 一貫したフォーマットを維持
   - バージョン情報を文書化

3. 集計
   - レポートで表示名を使用
   - モデルグループ化を維持
   - バージョン追跡を確保
