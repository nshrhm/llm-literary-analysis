# 技術コンテキスト

## 開発環境

### 言語とバージョン
- Python 3.12
- UTF-8エンコーディング
- 日本語テキスト処理対応

### 依存関係
- google-generativeai>=0.3.0
- anthropic>=0.43.0
- openai>=1.0.0
- python-dotenv>=1.0.0

## APIインテグレーション

### OpenAI API
1. バッチ処理（Ver.1）
   - エンドポイント: `/v1/chat/completions`
   - フォーマット: JSONL
   - コスト削減: 50%
   - 処理時間: 24時間以内
   - 制限:
     - 最大50,000リクエスト/バッチ
     - ファイルサイズ上限: 200MB

2. モデル固有の制約
   - o3-mini: 温度パラメータなし
   - o1-mini: システムロールなし

3. バッチ結果変換（2025-03-27実装）
   - tools/openai/batch_result_converter.py
   - 機能:
     - JSONLからテキストファイルへの変換
     - Unicodeエスケープの解決
     - temperature: None対応
   - 入力: batch_results/<batch_id>_output.jsonl
   - 出力: results/openai/*.txt

### Claude API
1. Message Batches API
   - 最大100,000リクエスト
   - 29日間の結果保持
   - スロットリング: 100リクエスト/分

2. 標準機能
   - temperature
   - max_tokens
   - system messages
   - prompt caching

### kluster.ai API
1. DeepSeekモデル
   - R1, V3, V3-0324
   - OpenAI互換インターフェース
   - バッチ処理対応

2. Llamaモデル
   - 70B, 405B, 8B
   - バッチ処理サポート
   - 24時間処理ウィンドウ

## ファイル構造

### プロジェクト構成
```
llm-literary-analysis/
├── tools/
│   ├── openai/
│   │   ├── batch_cleanup.py
│   │   ├── batch_result_converter.py  # 2025-03-27追加
│   │   └── tests/
│   └── shared/
└── results/
    ├── openai/
    │   ├── batch_results/
    │   └── *.txt
    ├── claude/
    ├── deepseek/
    └── llama/
```

### 結果ファイル形式
1. バッチ結果（JSONL）
```json
{
  "custom_id": "p{persona}_{model}_n{trial}_{text}",
  "response": {
    "status_code": 200,
    "body": {
      "choices": [{
        "message": {
          "content": "..."
        }
      }]
    }
  }
}
```

2. 変換後のテキストファイル
```
timestamp: YYYY-MM-DD HH:MM:SS
persona: p1-p4
model: model_name
trial: n01-n10
temperature: value or None
text: t1-t3

Q1value: [0-100]
Q1reason: [explanation]
...
Q4value: [0-100]
Q4reason: [explanation]
```

## 実装詳細

### バッチ処理
1. リクエスト生成
```python
def create_batch_request(requests):
    return {
        "custom_id": generate_custom_id(),
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model_name,
            "messages": messages,
            "temperature": temp  # 推論モデルでは省略
        }
    }
```

2. 結果変換（2025-03-27実装）
```python
def convert_batch_results(input_file):
    """Convert batch results to text files."""
    for line in read_jsonl(input_file):
        metadata = extract_metadata(line)
        content = extract_content(line)
        if is_reasoning_model(metadata['model']):
            metadata['temperature'] = None
        save_result_file(metadata, content)
```

### エラーハンドリング
1. バッチエラー
```python
def handle_batch_error(error):
    if error.is_rate_limit:
        retry_with_backoff()
    elif error.is_partial_failure:
        handle_partial_results()
    else:
        raise BatchProcessingError(error)
```

2. 変換エラー
```python
def handle_conversion_error(error):
    log_error(error)
    if error.is_unicode:
        retry_with_encoding()
    elif error.is_format:
        skip_and_log()
    else:
        raise ConversionError(error)
```

## 監視と制御

### バッチ監視
1. ステータスチェック
   - 5分間隔での確認
   - エラー時の自動ログ
   - 完了通知

2. エラー監視
   - エラー率の追跡
   - リトライ回数の制限
   - クリティカルエラーの通知

### リソース管理
1. ファイル管理
   - 自動バックアップ
   - 古いバッチの削除
   - ディスク使用量の監視

2. API制限
   - レート制限の遵守
   - コスト最適化
   - 並列実行の制御
