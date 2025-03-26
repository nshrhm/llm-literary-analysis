# プロジェクト構造の概要

## 基本構造

プロジェクトは統一されたアーキテクチャを採用し、以下のような構造を持ちます：

```
results/
├── llama/             # Llama実験結果
│   ├── batch_inputs/  # バッチリクエストファイル
│   ├── batch_results/ # バッチ実行結果
│   └── p1_llama33-70Bit_t1_n01_temp50.txt  # 個別結果ファイル
├── deepseek/          # DeepSeek実験結果
│   ├── batch_inputs/
│   ├── batch_results/
│   └── p1_deepseekr1_t1_n01_temp50.txt
├── gemini/           # Gemini実験結果
└── claude/           # Claude実験結果

aggregated_results/   # 集計結果
├── aggregated_llama_YYYYMMDD_HHMMSS.csv
└── aggregated_deepseek_YYYYMMDD_HHMMSS.csv

# プログラムファイル
├── experiment_runner.py     # 統合実験ランナー
├── kluster_batch_runner.py  # Kluster.ai用バッチランナー
├── check_models.py         # モデル可用性チェック
├── parameters.py           # 設定と定義
└── aggregate_experiment_results.py  # 結果集計
```

## モデル識別子と表示名の対応

### Llamaモデル
- ファイル名用識別子
  - llama33-70Bit
  - llama31-405Bit
  - llama31-8Bit
- 表示名（メタデータ・集計用）
  - Llama-3.3-70B
  - Llama-3.1-405B
  - Llama-3.1-8B

### DeepSeekモデル
- ファイル名用識別子
  - deepseekr1
  - deepseekv3
  - deepseekv3-0324
- 表示名（メタデータ・集計用）
  - DeepSeek-R1
  - DeepSeek-V3
  - DeepSeek-V3-0324

## ファイル命名規則

### 結果ファイル
- パターン: `{persona_id}_{model_identifier}_{text_id}_{trial_num}_temp{temperature}.txt`
- 例: `p1_llama33-70Bit_t1_n01_temp50.txt`

### バッチ関連ファイル
- リクエスト: `batch_requests_YYYYMMDD_HHMMSS.jsonl`
- 結果: `batch_results_YYYYMMDD_HHMMSS.jsonl`

### 集計ファイル
- パターン: `aggregated_{model_type}_YYYYMMDD_HHMMSS.csv`
- 例: `aggregated_llama_20250326_134306.csv`

## 言語と文字セット

- すべてのプロンプトとテキストコンテンツは日本語
- 結果ファイルはUTF-8エンコーディングを使用
- コメントとドキュメントは日本語を基本とする
