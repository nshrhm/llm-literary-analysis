# 現在の作業コンテキスト

## 最新の更新（2025-03-20）

### OpenAIバッチ処理の実装
- Batch APIを使用した処理の実装
  - JSONLファイルの生成と管理
  - バッチジョブの作成と監視
  - 結果の処理とエラーハンドリング
- 開発状況：
  - リクエスト形式のJSON形式化に問題があり、修正中
  - レスポンス処理の改善が必要
  - デバッグログの強化を実施

### バッチ処理のディレクトリ構造
```
results/openai/
├── batch_inputs/      # JSONLファイル
├── batch_results/     # 結果ファイル
├── batch_errors/      # エラーログ
└── backup/           # バックアップ
```

### 既知の問題
- JSONLファイルの形式が不正確
- レスポンスの解析でpersonaエラーが発生
- バッチ処理の完了確認に時間がかかる（5分間隔）

### 次のステップ
- JSONLファイルの形式の修正
- レスポンス処理の改善
- エラーハンドリングの強化

## 保留中の課題（2025-03-19）

### MetaのLlamaモデルの実装
- LLAMA_MODELSをparameters.pyに追加
  - llama33-70Bit: Meta-Llama-3.3-70B-Instruct-Turbo
  - llama31-405Bit: Meta-Llama-3.1-405B-Instruct-Turbo
  - llama31-8Bit: Meta-Llama-3.1-8B-Instruct-Turbo
- Kluster.aiを介したAPI連携を実装
- LlamaExperimentRunnerクラスを追加
- DeepSeekと同じKLUSTERAI_API_KEYを使用

### DeepSeek-V3モデルの追加
- DeepSeek-V3モデルをDEEPSEEK_MODELSに追加
- 既存のDeepSeek-R1と同じインターフェースで実装
- バックアップと動作検証を実施

### DeepSeekモデルの特徴
- 内部思考プロセスを中国語で出力する傾向
- aggregate_experiment_results.pyで正常に処理可能
- 最終的な回答は日本語で適切に出力

### Claude-3-Opusモデルの一時的無効化（2025-03-18）
- コスト削減のためclaude-3-opus-20240229を一時的に無効化
- parameters.pyのCLAUDE_MODELSでコメントアウト処理
- 将来的な費用対効果改善時に再検討予定
