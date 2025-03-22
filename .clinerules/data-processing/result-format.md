# 結果フォーマットの仕様

## 標準実験結果フォーマット

### 評価項目
実験結果は以下の4つの感情に対する数値評価（0-100）と理由を含みます：

- 面白さ (Interesting/Fun)
- 驚き (Surprise)
- 悲しみ (Sadness)
- 怒り (Anger)

### フォーマット構造
結果は質問番号とラベルを明確に示す形式で記録されます：

```
Q1. 面白さ(数値): [0-100]
Q1. 面白さ(理由): [explanation]

Q2. 驚き(数値): [0-100]
Q2. 驚き(理由): [explanation]

Q3. 悲しみ(数値): [0-100]
Q3. 悲しみ(理由): [explanation]

Q4. 怒り(数値): [0-100]
Q4. 怒り(理由): [explanation]
```

### 評価基準
- 数値評価（0-100）
  - 0: 全く感じない
  - 50: 中程度
  - 100: 非常に強く感じる
- 理由の説明は日本語で記述
- 各評価に対して具体的な根拠を提供

## バッチ処理結果フォーマット

### JSONLリクエストファイル
ファイル名パターン: `batch_requests_{timestamp}.jsonl`

```json
{
  "custom_id": "p{persona}_{text}_n{trial}",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "モデル名",
    "temperature": 温度値,
    "messages": [
      {
        "role": "system",
        "content": "システムメッセージ"
      },
      {
        "role": "user",
        "content": "ユーザーメッセージ"
      }
    ]
  }
}
```

### バッチ結果ファイル
ファイル名パターン: `results_{timestamp}.jsonl`

```json
{
  "id": "バッチリクエストID",
  "custom_id": "p{persona}_{text}_n{trial}",
  "response": {
    "status_code": HTTPステータスコード,
    "request_id": "リクエストID",
    "body": {
      "choices": [
        {
          "message": {
            "role": "assistant",
            "content": "Q1. 面白さ(数値): [0-100]\nQ1. 面白さ(理由): [説明]\n\nQ2..."
          }
        }
      ]
    }
  }
}
```

### エラーログファイル
ファイル名パターン: `errors_{timestamp}.jsonl`

```json
{
  "timestamp": "ISO8601形式",
  "batch_id": "バッチID",
  "error_type": "エラー種別",
  "message": "エラーメッセージ",
  "details": "詳細情報"
}
```

## 命名規則

### ファイル名コンポーネント
- `{persona}`: p1-p4
- `{text}`: t1-t3
- `{trial}`: n01, n02, n03...
- `{timestamp}`: YYYYMMDD_HHMMSS
- `{temp}`: temp50（0.5）など

### パターン例
- 標準結果: `p1_gpt4o_n01_temp50_t1.txt`
- バッチリクエスト: `batch_requests_20250322_123456.jsonl`
- バッチ結果: `results_20250322_123456.jsonl`
- エラーログ: `errors_20250322_123456.jsonl`
