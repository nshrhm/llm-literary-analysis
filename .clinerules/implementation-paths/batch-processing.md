# バッチ処理の実装指針

## ディレクトリ構造
results/{provider}/の下に以下のディレクトリを配置:

- batch_inputs/: バッチリクエストのJSONLファイル
- batch_results/: 処理結果ファイル
- batch_errors/: エラーログ
- backup/: 自動バックアップ

各ディレクトリはタイムスタンプ付きのサブディレクトリを持つ（YYYYMMDD_HHMMSS形式）

## バッチ処理ルール

### リクエスト
- 1バッチあたり最大50,000リクエスト
- ファイルサイズ上限: 200MB
- 24時間以内の処理完了を保証

### 監視と再試行
- 5分間隔でのステータス確認
- エラー発生時は自動的にログを記録
- バッチ全体の失敗時は個別リクエストに分割して再試行

### エラー処理
1. エラーの種類
   - バッチ作成エラー
   - 処理タイムアウト
   - 部分的な失敗
   - データ形式エラー

2. エラーログ形式
```json
{
    "timestamp": "ISO8601形式",
    "batch_id": "バッチID",
    "error_type": "エラー種別",
    "message": "エラーメッセージ",
    "details": "詳細情報"
}
```

### バックアップ
- バッチ処理開始時に既存結果を自動バックアップ
- タイムスタンプ付きディレクトリに保存
- 入力、結果、エラーログを含む完全バックアップ
