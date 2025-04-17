# 結果フォーマットガイド

## 結果の構造

### ディレクトリ構成
```
results/
├── gemini/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── claude/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── grok/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── openai/
│   ├── batch_results/
│   │   └── batch_{id}_output.jsonl  # バッチ処理の生結果
│   └── p{persona}_{model}_n{trial}[_temp{temp}]_{text}.txt
├── deepseek/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
└── llama/
    └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
```

### ファイル命名規則（2025-04-17更新）
- GPT-4.1シリーズ：`p{persona}_gpt-4.1[-(mini|nano)]_n{trial}_temp{temp}_{text}.txt`
  例：`p1_gpt-4.1_n01_temp70_t1.txt`
- 標準形式：`p{persona}_{model}_n{trial}_temp{temp}_{text}.txt`
  例：`p1_gemini20pe_n01_temp70_t1.txt`
- 推論モデル：`p{persona}_{model}_n{trial}_{text}.txt`
  例：`p1_o3-mini_n01_t1.txt`
- バッチ結果：`batch_{id}_output.jsonl`

## 結果ファイルフォーマット

### メタデータセクション（2025-04-17更新）
```yaml
# 基本情報
timestamp: [YYYY-MM-DD HH:MM:SS]
persona: [ペルソナ名]
model: [モデル名]
trial: [試行番号]
temperature: [温度値 or None]
text: [テキスト名]

# GPT-4.1シリーズの価格情報（2025-04-17追加）
pricing: {
  "input": [rate],      # 入力コスト（$）
  "cached_input": [rate], # キャッシュ利用時の入力コスト（$）
  "output": [rate]      # 出力コスト（$）
}

# 検証情報
validation_status: [success/retry_success/failed]
matched_patterns:
  面白さ: [使用されたパターン]
  驚き: [使用されたパターン]
  悲しみ: [使用されたパターン]
  怒り: [使用されたパターン]
retry_count: [0-3]
error_details: [エラー情報]
```

### 応答データセクション
```yaml
Q1value: [0-100]
Q1reason: [面白さの理由]
Q2value: [0-100]
Q2reason: [驚きの理由]
Q3value: [0-100]
Q3reason: [悲しみの理由]
Q4value: [0-100]
Q4reason: [怒りの理由]
```

## パターンマッチング

### サポートされる応答パターン
1. 標準形式: `Q1. 面白さ(数値): 80`
2. 代替形式1: `Q1. 面白さ: (数値): 80`
3. 代替形式2: `Q1. 面白さ 数値: 80`
4. シンプル形式: `Q1. 面白さ: 80`
5. 日本語形式1: `面白さの評価: 80`
6. 日本語形式2: `面白さレベル: 80`
7. 括弧形式: `「面白さ」: 80`
8. 角括弧形式: `[面白さ]: 80`

### 正規表現パターン
```python
patterns = [
    rf"Q\d+\.\s*{question}\(数値\):\s*(\d+)",
    rf"Q\d+\.\s*{question}:\s*\(数値\):\s*(\d+)",
    rf"Q\d+\.\s*{question}\s*数値:\s*(\d+)",
    rf"Q\d+\.\s*{question}:\s*(\d+)",
    rf"{question}(?:の評価)?(?:\s*[:：]\s*|\s+)(\d+)",
    rf"{question}(?:度|レベル)(?:\s*[:：]\s*|\s+)(\d+)",
    rf"「{question}」\s*[:：]?\s*(\d+)",
    rf"\[{question}\]\s*[:：]?\s*(\d+)"
]
```

## 集計結果

### CSV出力形式
```
aggregated_results/
├── aggregated_openai_[timestamp].csv
├── aggregated_claude_[timestamp].csv
├── aggregated_gemini_[timestamp].csv
├── aggregated_grok_[timestamp].csv
├── aggregated_deepseek_[timestamp].csv
└── aggregated_llama_[timestamp].csv
```

### 集計内容（2025-04-17更新）
1. 基本情報
   - メタデータ完全セット
   - 感情次元のスコア
   - 理由付けテキスト
   - 価格情報（GPT-4.1シリーズ）

2. パターンマッチング情報
   - 使用パターンの種類
   - パターン使用頻度
   - パターン成功率

3. 品質メトリクス
   - 初回検証成功率
   - 再試行率
   - 平均再試行回数
   - エラーパターン

4. コスト分析（2025-04-17追加）
   - 入力コスト集計
   - キャッシュ利用率
   - コスト削減効果
   - モデル別効率

5. エラー統計
   - エラータイプの頻度
   - 回復成功率
   - モデル別傾向

## 結果検証

### 数値検証
- 範囲チェック（0-100）
- 整数値の確認
- 欠損値の検出
- 異常値の識別

### テキスト検証
- 日本語文字列の確認
- エンコーディング検証
- 最小文字数チェック
- フォーマット整合性

### メタデータ検証
1. 基本フィールド
   - タイムスタンプ形式
   - ペルソナID（p1-p4）
   - 試行番号（n01-n10）
   - テキストID（t1-t3）

2. 価格情報（2025-04-17追加）
   - フィールドの存在確認
   - レート値の検証
   - キャッシュ率の確認

## エラー処理

### メタデータエラー
1. データ形式
   - 不正なタイムスタンプ
   - 未知のモデル識別子
   - 温度値の不整合
   - ID形式の誤り

2. 価格情報（2025-04-17追加）
   - 不正なレート値
   - キャッシュ率の不整合
   - 必須フィールドの欠落

### 評価データエラー
1. 数値評価
   - 範囲外の値
   - 非整数値の検出
   - 必須値の欠落

2. テキストデータ
   - 空の説明
   - 文字化け
   - 言語不一致

### リカバリー手順
1. エラーの分類
2. 自動修正の試行
3. 手動確認の要求
4. エラーログの記録
