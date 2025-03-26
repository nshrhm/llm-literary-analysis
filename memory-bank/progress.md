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

### 次のステップ
- 全モデルでの新規テスト実行と結果の確認
- 集計結果の分析と比較
- 必要に応じた追加の改善
