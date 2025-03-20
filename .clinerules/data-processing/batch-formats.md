# バッチ処理のファイルフォーマット

## JSONLリクエストファイル
ファイル名パターン: `batch_requests_{model}.jsonl`

### リクエスト形式
```jsonl
{
  "custom_id": "p{persona}_{model}_n{trial}[_temp{temp}]_{text}",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "{model_name}",
    "messages": [
      {
        "role": "user",
        "content": "{prompt}"
      }
    ],
    "temperature": {temp}  // text_generation型のみ
  }
}
```

## 結果ファイル
ファイル名パターン: `p{persona}_{model}_n{trial}[_temp{temp}]_{text}.txt`

### 結果ファイル形式
```
timestamp: [YYYY-MM-DD HH:MM:SS]
persona: [p1-p4]
model: [モデル名]
trial: [試行番号]
temperature: [温度設定] // text_generation型のみ
text: [テキスト識別子]
Q1value: [0-100]
Q1reason: [面白さの理由]
Q2value: [0-100]
Q2reason: [驚きの理由]
Q3value: [0-100]
Q3reason: [悲しみの理由]
Q4value: [0-100]
Q4reason: [怒りの理由]
```

## エラーログファイル
ファイル名: `error_log.txt`

### エラーログエントリ形式
```json
{
  "timestamp": "ISO8601形式タイムスタンプ",
  "batch_id": "バッチ処理ID",
  "error_type": [
    "batch_processing_error",    // バッチ処理全般のエラー
    "metadata_extraction_error", // メタデータ解析エラー
    "response_processing_error", // レスポンス処理エラー
    "invalid_response_format",   // 不正なレスポンス形式
    "batch_partial_failure"      // 一部リクエストの失敗
  ],
  "message": "エラーの説明",
  "details": "エラーの詳細情報"
}
```

## パラメータ表記規則

### 識別子フォーマット
- `{persona}`: p1, p2, p3, p4
- `{model}`: gpt-4o, gpt-4o-mini, o3-mini, o1-mini など
- `{trial}`: n01, n02, n03 など
- `{temp}`: temp50（temperature=0.5）など
- `{text}`: t1, t2, t3, t4 など

### 共通規則
- すべてのファイル名は小文字を使用
- 数値は常に2桁で0埋め
- タイムスタンプは YYYYMMDD_HHMMSS 形式
- temperature値は100倍して整数表記
