# 結果フォーマットガイド

## 結果の構造

### ディレクトリ構成
```
results/
├── gemini/
│   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
├── claude/
│   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
├── grok/
│   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
├── openai/
│   ├── batch_results/
│   │   └── batch_{id}_output.jsonl  # バッチ処理の生結果
│   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
├── deepseek/
│   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
└── llama/
    └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
```

### ファイル命名規則（2025-04-30更新）
- GPT-4.1シリーズ：`{text}_gpt-4.1[-(mini|nano)]_{persona}_temp{temp}_{trial}.txt`
  例：`t1_gpt-4.1_p1_temp70_01.txt`
- 標準形式：`{text}_{model}_{persona}_temp{temp}_{trial}.txt`
  例：`t1_gemini20pe_p1_temp70_01.txt`
- 推論モデル：`{text}_{model}_{persona}_temp--_{trial}.txt`
  例：`t1_o3-mini_p1_temp--_01.txt`
- バッチ結果：`batch_{id}_output.jsonl`

## 結果ファイルフォーマット

### メタデータセクション（2025-04-30更新）
```yaml
# 基本情報（順序固定）
timestamp: [YYYY-MM-DD HH:MM:SS]
text: [テキスト名]
model: [モデル名]
persona: [ペルソナ名]
trial: [試行番号]  # 整数値として表示（例：1, 2, 3）
temperature: [温度値 or None]

# GPT-4.1シリーズの価格情報（2025-04-17追加）
pricing: {
  "input": [rate],      # 入力コスト（$）
  "cached_input": [rate], # キャッシュ利用時の入力コスト（$）
  "output": [rate]      # 出力コスト（$）
}
```

### 応答データセクション
```yaml
Q1. 面白さ(数値): [0-100]
Q1. 面白さ(理由): [面白さの理由]
Q2. 驚き(数値): [0-100]
Q2. 驚き(理由): [驚きの理由]
Q3. 悲しみ(数値): [0-100]
Q3. 悲しみ(理由): [悲しみの理由]
Q4. 怒り(数値): [0-100]
Q4. 怒り(理由): [怒りの理由]
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

### 集計内容（2025-04-30更新）
1. 基本情報
   - メタデータ（標準順序）
   - 感情次元のスコア
   - 理由付けテキスト
   - 価格情報（GPT-4.1シリーズ）

2. 品質メトリクス
   - 初回検証成功率
   - 再試行率
   - 平均再試行回数
   - エラーパターン

3. コスト分析
   - 入力コスト集計
   - キャッシュ利用率
   - コスト削減効果
   - モデル別効率

4. エラー統計
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
   - テキストID（t1-t3）
   - モデル名の形式
   - ペルソナID（p1-p4）
   - 試行番号（1-10、整数値）
   - 温度値（数値またはNone）

2. 価格情報（GPT-4.1シリーズ）
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

2. 価格情報
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
