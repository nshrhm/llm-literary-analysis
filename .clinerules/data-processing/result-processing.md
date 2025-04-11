# 結果処理ルール（2025-04-11作成）

## パターンマッチング処理

### 数値抽出プロセス
1. 優先順位付きパターン適用
```python
def extract_value(text, question):
    """段階的なパターンマッチングの適用"""
    patterns = [
        rf"Q\d+\.\s*{question}\(数値\):\s*(\d+)",  # 標準形式
        rf"Q\d+\.\s*{question}:\s*\(数値\):\s*(\d+)",  # 代替形式1
        rf"Q\d+\.\s*{question}\s*数値:\s*(\d+)",  # 代替形式2
        rf"Q\d+\.\s*{question}:\s*(\d+)",  # シンプル形式
        rf"{question}(?:の評価)?(?:\s*[:：]\s*|\s+)(\d+)",  # 日本語形式1
        rf"{question}(?:度|レベル)(?:\s*[:：]\s*|\s+)(\d+)",  # 日本語形式2
        rf"「{question}」\s*[:：]?\s*(\d+)",  # 括弧形式
        rf"\[{question}\]\s*[:：]?\s*(\d+)"  # 角括弧形式
    ]
    
    for pattern in patterns:
        if match := re.search(pattern, text, re.MULTILINE):
            return match.group(1)
    return ""
```

2. パターン使用統計の記録
```python
def track_pattern_usage(text, question, patterns):
    """パターンの使用状況を追跡"""
    for pattern_name, pattern in patterns.items():
        if re.search(pattern, text, re.MULTILINE):
            return pattern_name
    return "unknown"
```

### 検証プロセス
1. 必須フィールドの確認
```python
def validate_required_fields(response):
    """必須フィールドの存在確認"""
    required = ["面白さ", "驚き", "悲しみ", "怒り"]
    for field in required:
        if not extract_value(response, field):
            return False
    return True
```

2. 数値範囲の検証
```python
def validate_value_range(value):
    """数値範囲の検証（0-100）"""
    try:
        num_value = int(value)
        return 0 <= num_value <= 100
    except ValueError:
        return False
```

## エラー処理

### リトライメカニズム
```python
def handle_validation_error(model, prompt, max_retries=3):
    """検証エラー時の再試行処理"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if validate_response(response):
                return response, attempt + 1
        except Exception as e:
            log_error(f"Attempt {attempt + 1} failed: {str(e)}")
    raise ValidationError("Maximum retries exceeded")
```

### エラーログ記録
```python
def log_validation_error(response, error_type):
    """検証エラーの詳細記録"""
    return {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "response_text": response.text,
        "matched_patterns": track_all_patterns(response),
        "validation_details": get_validation_details(response)
    }
```

## 結果の集計

### パターン使用統計
```python
def aggregate_pattern_stats(results):
    """パターン使用状況の集計"""
    stats = {
        "total_responses": len(results),
        "pattern_usage": defaultdict(int),
        "success_rate": defaultdict(float),
        "retry_rates": defaultdict(list)
    }
    
    for result in results:
        for field, pattern in result["matched_patterns"].items():
            stats["pattern_usage"][pattern] += 1
            stats["success_rate"][pattern] += (1 if result["validation_status"] == "success" else 0)
            stats["retry_rates"][pattern].append(result["retry_count"])
    
    return stats
```

### 品質メトリクス
1. 応答品質指標
- パターンマッチング成功率
- 初回検証成功率
- 再試行成功率
- 平均再試行回数

2. モデル別統計
- パターン使用傾向
- エラー発生率
- 応答時間分布

## 結果ファイルの構造

### メタデータセクション
```yaml
# 基本情報
timestamp: YYYY-MM-DD HH:MM:SS
model: モデル名
temperature: 温度値

# 検証情報
validation_status: success/retry_success/failed
retry_count: 試行回数
matched_patterns:
  field1: パターン名
  field2: パターン名
  ...

# エラー情報（該当する場合）
error_details:
  type: エラータイプ
  message: エラーメッセージ
  timestamp: エラー発生時刻
```

### データセクション
```yaml
results:
  - question: 面白さ
    value: 80
    pattern: 標準形式
    validation: success
  - question: 驚き
    value: 65
    pattern: 代替形式1
    validation: success
  ...
