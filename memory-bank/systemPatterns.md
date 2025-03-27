# システムパターン

## アーキテクチャパターン

### バッチ処理システム
```mermaid
graph TD
    A[バッチリクエスト生成] --> B[JSONLファイル作成]
    B --> C[バッチジョブ作成]
    C --> D[ステータス監視]
    D --> E{完了判定}
    E -->|完了| F[結果取得]
    E -->|未完了| D
    F --> G[結果変換]
    G --> H[個別ファイル保存]
```

1. リクエスト生成
   - モデル固有のフォーマット適用
   - パラメータ検証
   - カスタムID生成

2. バッチ処理
   - JSONLフォーマット使用
   - 非同期処理
   - ステータス管理

3. 結果処理（2025-03-27更新）
   - JSONLからテキストへの変換
   - Unicodeエスケープ解決
   - temperature: None対応
   - メタデータの標準化

### 結果管理システム
```mermaid
graph TD
    A[結果ファイル] --> B{フォーマット判定}
    B -->|JSONL| C[バッチ結果変換]
    B -->|TXT| D[直接処理]
    C --> E[メタデータ抽出]
    D --> E
    E --> F[結果検証]
    F --> G[集計処理]
```

1. ファイル構造
   - モデル別ディレクトリ
   - 標準化されたファイル名
   - メタデータ形式

2. データフロー
   - バッチ結果の変換
   - メタデータの抽出
   - 結果の検証
   - 集計処理

## 実装パターン

### バッチ処理
1. リクエスト生成
```python
def create_batch_request(model_type, requests):
    if model_type == "openai":
        return create_openai_batch(requests)
    elif model_type == "claude":
        return create_claude_batch(requests)
    elif model_type == "klusterai":
        return create_klusterai_batch(requests)
```

2. 結果変換（2025-03-27更新）
```python
def convert_batch_results(input_file):
    """Convert batch results from JSONL to individual text files."""
    with open(input_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            # Extract metadata
            metadata = extract_metadata(data)
            # Handle temperature
            if is_reasoning_model(metadata['model']):
                metadata['temperature'] = None
            # Convert and save
            save_result_file(metadata, data['content'])
```

### エラーハンドリング
1. バッチ処理エラー
```python
def handle_batch_error(batch_id, error):
    if is_partial_success(error):
        save_partial_results(batch_id)
        retry_failed_requests(batch_id)
    else:
        handle_complete_failure(batch_id)
```

2. 変換エラー
```python
def handle_conversion_error(file_id, error):
    log_error(file_id, error)
    if is_recoverable(error):
        retry_conversion(file_id)
    else:
        mark_as_failed(file_id)
```

## データパターン

### メタデータ形式
```python
metadata = {
    'timestamp': 'YYYY-MM-DD HH:MM:SS',
    'persona': 'p1-p4',
    'model': 'model_name',
    'trial': 'n01-n10',
    'temperature': float or None,  # 2025-03-27: None for reasoning models
    'text': 't1-t3'
}
```

### 結果フォーマット
```
timestamp: [timestamp]
persona: [persona_id]
model: [model_id]
trial: [trial_number]
temperature: [value or None]
text: [text_id]

Q1value: [0-100]
Q1reason: [explanation]
...
Q4value: [0-100]
Q4reason: [explanation]
```

## モニタリングパターン

### バッチ処理監視
1. ステータスチェック
```python
def check_batch_status(batch_id):
    status = get_batch_status(batch_id)
    if status.is_complete:
        process_results(batch_id)
    elif status.has_error:
        handle_batch_error(batch_id)
    else:
        schedule_next_check(batch_id)
```

2. エラー追跡
```python
def track_errors(batch_id):
    errors = collect_errors(batch_id)
    log_errors(errors)
    notify_if_critical(errors)
    update_error_stats(errors)
```

## 拡張パターン

### 新規モデル追加
1. バッチ処理サポート
```python
def add_model_support(model_config):
    register_batch_handler(model_config)
    register_result_converter(model_config)
    update_monitoring(model_config)
```

2. 結果変換サポート
```python
def add_converter_support(model_config):
    register_metadata_handler(model_config)
    register_content_converter(model_config)
    register_validation_rules(model_config)
