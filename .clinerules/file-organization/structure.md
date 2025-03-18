# プロジェクト構造の概要

## 基本構造

プロジェクトは統一されたアーキテクチャを採用し、以下のような構造を持ちます：

```
results/
├── gemini/          # Gemini実験結果
└── claude/          # Claude実験結果

src/
├── experiment_runner.py     # 統合実験ランナー
├── check_models.py         # モデル可用性チェック
├── parameters.py           # 設定と定義
└── aggregate_experiment_results.py  # 結果集計
```

## 主要コンポーネント

- `experiment_runner.py`: ベース実験ランナーと各LLM固有の実装を含む
- `check_models.py`: 両LLMのモデル可用性確認機能を提供
- `parameters.py`: プロジェクト全体の設定と定義を管理
- `aggregate_experiment_results.py`: 実験結果の集計と分析を担当

## 言語と文字セット

- すべてのプロンプトとテキストコンテンツは日本語
- 結果ファイルはUTF-8エンコーディングを使用
- コメントとドキュメントは日本語を基本とする
