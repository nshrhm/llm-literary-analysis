# 実験ランナーの実装詳細

## 概要

`experiment_runner.py`は、GeminiとClaudeモデル両方の実験を実行するための統合実験ランナーを提供します：

- `BaseExperimentRunner`: すべてのLLM実験に共通する機能
- `GeminiExperimentRunner`: Gemini固有の実装
- `ClaudeExperimentRunner`: Claude固有の実装

## 関連ファイル

- `check_models.py`: 両LLMのモデル可用性チェック
- `parameters.py`: ペルソナ、テキスト、モデル設定の定義
- `aggregate_experiment_results.py`: 実験結果の集計と分析

## 主要機能

### BaseExperimentRunner

共通機能を提供：
- `generate_prompt`: 標準化されたプロンプトの作成
- `extract_value/reason`: モデルレスポンスの処理
- `save_result`: 結果ファイルの生成

### モデル固有の実装

#### GeminiExperimentRunner
- google.generativeai を使用したAPI連携
- Gemini固有の応答処理

#### ClaudeExperimentRunner
- anthropic を使用したAPI連携
- Claude固有の応答処理
