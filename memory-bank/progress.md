# Progress Memory Bank

## 2025-03-26
### モデル識別子とファイル名の改善
- Llamaモデルの識別子と表示名を修正
  - ファイル名: llama33-70Bit, llama31-405Bit, llama31-8Bit
  - 表示名: Llama-3.3-70B, Llama-3.1-405B, Llama-3.1-8B
- DeepSeekモデルの識別子と表示名を修正
  - ファイル名: deepseekr1, deepseekv3, deepseekv3-0324
  - 表示名: DeepSeek-R1, DeepSeek-V3, DeepSeek-V3-0324

### 実装の改善
- _get_model_identifier メソッドの追加
  - モデルのフルパスから適切な識別子を抽出
  - DeepSeekとLlamaモデルの両方に対応

- create_batch_requests メソッドの修正
  - カスタムIDにモデル固有の識別子を使用
  - 結果ファイルにモデル表示名を正しく保存

### 結果の整理
- 既存の結果ファイルを消去し、新しい命名規則で再生成
- ファイル名とメタデータの一貫性を確保
- 集計CSVファイルでのモデル区別を実現

### バッチ実験の実施
- DeepSeekモデルのバッチ実験完了（360結果）
- Llamaモデルのバッチ実験完了（360結果）
- すべてのモデルとペルソナの組み合わせで実行
- 集計CSVファイルの生成と確認

## 2025-03-27
### バッチ処理の改善
- TRIALSパラメータの適切な使用（10トライアル）
- DeepSeekとLlamaのバッチ実行スクリプトを修正
- README.mdの更新
  - 新しいDeepSeek-V3-0324モデルの追加
  - バッチ処理コマンドの説明を追加
  - 結果数の更新（各360結果）

### 次のステップ
- 他のモデル（Gemini, Claude, Grok）のバッチ処理実装
- 集計結果の比較分析
- ドキュメントの継続的な更新
