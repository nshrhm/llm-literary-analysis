# バッチ処理ガイド

## 概要

バッチ処理システムは、大規模な実験を効率的に実行し、APIコストを削減するために設計されています。JSONLフォーマットを使用することで、最大50%のコスト削減を実現しています。

## プロバイダー別の実装

### OpenAI

#### 基本仕様
- エンドポイント: `/v1/chat/completions`
- フォーマット: JSONL
- 処理時間: 24時間以内
- 制限:
  - 最大50,000リクエスト/バッチ
  - ファイルサイズ上限: 200MB

#### コスト構造（2025-04-15更新）
1. GPT-4.1シリーズ
   - gpt-4.1:
     - Input: $2.00
     - Cached input: $0.50
     - Output: $8.00
   - gpt-4.1-mini:
     - Input: $0.40
     - Cached input: $0.10
     - Output: $1.60
   - gpt-4.1-nano:
     - Input: $0.10
     - Cached input: $0.025
     - Output: $0.40

#### 使用方法
```bash
# バッチ処理の実行
python openai_example.py --batch [--model gpt-4.1 gpt-4.1-mini]

# ステータス確認
python openai_example.py --status <batch_id>

# バッチのキャンセル
python openai_example.py --cancel <batch_id>

# 結果の変換
python tools/openai/batch_result_converter.py results/openai/batch_results/<batch_id>_output.jsonl
```

### Claude

#### 基本仕様
- Message Batches API
- 最大100,000リクエスト
- 29日間の結果保持
- レート制限: 100リクエスト/分

#### 使用方法
```bash
python claude_example.py --batch [--model claude37s claude35s]
```

### kluster.ai

#### DeepSeek & Llama
- OpenAI互換APIインターフェース
- バッチ処理サポート
- 24時間処理ウィンドウ

#### 使用方法
```bash
# DeepSeekバッチ処理
python deepseek_batch_example.py [--model deepseekr1 deepseekv3]

# Llamaバッチ処理
python llama_batch_example.py [--model llama4-maveric llama4-scout]
```

## 実装詳細

### リクエスト構造
```python
{
    "custom_id": "p{persona}_{model}_n{trial}_{text}",
    "method": "POST",
    "url": "/v1/chat/completions",
    "body": {
        "model": model_name,
        "messages": messages,
        "temperature": temp  # 推論モデルでは省略
    }
}
```

### バッチ処理フロー
1. リクエスト生成
   - モデル固有のフォーマット適用
   - パラメータ検証
   - カスタムID生成

2. バッチ実行
   - JSONLファイルの作成
   - バッチジョブの実行
   - ステータス監視

3. 結果処理
   - JSONLからテキストへの変換
   - メタデータの抽出
   - 結果の検証

### エラーハンドリング

#### リトライ戦略
```python
def handle_batch_error(batch_id, error):
    """バッチエラーの処理"""
    if is_partial_success(error):
        save_partial_results(batch_id)
        retry_failed_requests(batch_id)
    else:
        handle_complete_failure(batch_id)
```

#### エラー種別
1. 一時的なエラー
   - レート制限
   - ネットワークエラー
   - サーバー負荷

2. 永続的なエラー
   - 無効なパラメータ
   - モデルの非対応
   - 認証エラー

## 最適化とモニタリング

### バッチサイズの最適化
- プロバイダーごとの制限考慮
- メモリ使用量の管理
- 処理時間の制御

### リソース管理
1. ファイル管理
   - 自動クリーンアップ
   - バックアップ戦略
   - ディスク使用量の監視

2. APIリソース
   - レート制限の遵守
   - コスト最適化
   - 並列実行の制御

### パフォーマンス指標
- 処理時間
- 成功率
- エラー発生率
- コスト効率

## メンテナンスツール

### バッチクリーンアップ
```bash
# 特定のバッチを削除
python tools/openai/batch_cleanup.py --batch-id <batch_id>

# すべてのバッチを削除
python tools/openai/batch_cleanup.py --all

# 最大50件のバッチを削除
python tools/openai/batch_cleanup.py --all --limit 50
```

### モニタリングツール
- ステータス監視
- リソース使用量の追跡
- エラー通知の設定
- コスト分析レポート
