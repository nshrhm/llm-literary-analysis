# システムパターン

## ファイル命名規則

### バッチ処理結果ファイル
1. 命名パターン
```
{type}_{identifier}_output.jsonl
例：batch_gpt-4.1_output.jsonl
```

2. 個別結果ファイル
```
{text}_{model}_{persona}_temp{temperature}_{trial}.txt
例：t1_gpt-4o_p1_temp50_01.txt
    t1_gpt-4o_p1_temp--_01.txt  # temperatureなしの場合
```

## メタデータ標準化

### ヘッダー情報
1. 必須フィールド（順序固定）
```
timestamp: YYYY-MM-DD HH:MM:SS
text: <テキストID>
model: <モデル名>
persona: <ペルソナID>
trial: <試行番号>  # 整数値として表示
temperature: <温度値 or None>
```

2. オプションフィールド
```
pricing: {  # GPT-4.1シリーズの場合
  "input": <入力単価>,
  "cached_input": <キャッシュ入力単価>,
  "output": <出力単価>
}
```

## データ処理パターン

### 試行番号の正規化
1. 入力処理
- 01-10形式の処理
- nプレフィックスの除去（n01 → 1）
- 整数値への変換と文字列化

2. エラー処理
- 無効な形式の検出
- 数値範囲の検証（1-10）
- エラーメッセージの標準化

### レスポンスの処理
1. 応答形式のチェック
- 複数のパターンによる値の抽出
- 理由文の検証
- 形式エラーの検出

2. バリデーション
- 数値範囲（0-100）の確認
- 必須要素の存在確認
- 形式の一貫性チェック

## テストパターン

### 単体テスト
1. 入力検証
- 標準ケース
- 境界値ケース
- エラーケース

2. 出力検証
- メタデータの順序
- 値の正規化
- フォーマットの一貫性

### 統合テスト
1. ワークフロー検証
- バッチ処理の完全性
- ファイル生成の正確性
- エラー処理の一貫性

2. パフォーマンス検証
- 処理速度の測定
- リソース使用量の確認
- エラー回復の効率

## エラー処理パターン

### エラーの分類
1. 入力エラー
- ファイル名形式の不一致
- メタデータの欠落
- 値の範囲外

2. 処理エラー
- API通信エラー
- パース失敗
- バリデーション失敗

### エラー対応
1. 自動リカバリー
- リトライ処理
- 部分的成功の保存
- ログ記録

2. エラー通知
- エラー種別の識別
- 詳細情報の記録
- 統計情報の更新

## ログ記録パターン

### 処理ログ
1. 基本情報
- タイムスタンプ
- 処理ID
- 操作種別

2. 詳細情報
- 入力パラメータ
- 処理結果
- エラー詳細

### 統計ログ
1. 処理統計
- 成功件数
- 失敗件数
- 処理時間

2. エラー統計
- エラー種別ごとの件数
- リトライ回数
- 復旧率

## バックアップパターン

### データ保護
1. ファイルバックアップ
- 処理前の状態保存
- 増分バックアップ
- 世代管理

2. メタデータバックアップ
- 設定情報の保存
- 処理履歴の保持
- 復元ポイントの管理

### リカバリー
1. 障害復旧
- チェックポイントからの再開
- 部分的復元
- データ整合性の確保

2. データ検証
- バックアップの完全性確認
- 復元データの検証
- エラーログの分析
