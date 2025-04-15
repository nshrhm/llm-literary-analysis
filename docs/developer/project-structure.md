# プロジェクト構造ガイド

## ディレクトリ構造

```
llm-literary-analysis/
├── experiment_runner.py           # 統合実験ランナー
├── check_models.py               # モデル可用性チェッカー
├── parameters.py                 # 実験パラメータ
├── aggregate_experiment_results.py # 結果分析ツール
├── tools/                        # ユーティリティツール
│   ├── openai/                   # OpenAI専用ツール
│   │   ├── batch_cleanup.py     # バッチ管理ツール
│   │   ├── batch_result_converter.py  # バッチ結果変換ツール
│   │   └── tests/              # OpenAIツールのテスト
│   └── shared/                   # 共有ツール
├── docs/                         # ドキュメント
│   ├── api/                      # APIドキュメント
│   │   ├── openai/              # OpenAI API実装詳細
│   │   ├── claude/              # Claude API実装詳細
│   │   └── shared/              # 共有APIコンポーネント
│   ├── guides/                   # 使用ガイド
│   │   ├── models.md            # モデル詳細
│   │   ├── features.md          # 機能詳細
│   │   ├── batch-processing.md  # バッチ処理
│   │   └── results.md           # 結果形式
│   ├── developer/               # 開発者向け
│   │   ├── project-structure.md # プロジェクト構造
│   │   └── contribution.md      # コントリビューション
│   └── reference/               # 技術リファレンス
│       ├── temperature.md       # 温度設定
│       └── patterns/            # 実装パターン
└── results/                      # 実験結果
    ├── gemini/                   # Gemini結果
    ├── claude/                   # Claude結果
    ├── grok/                     # Grok結果
    ├── openai/                   # OpenAI結果
    │   ├── batch_results/       # バッチ処理結果
    │   └── *.txt                # 変換済み結果
    ├── deepseek/                 # DeepSeek結果
    └── llama/                    # Llama結果
```

## 主要コンポーネント

### 実験実行
1. experiment_runner.py
   - 全モデルでの実験実行
   - 設定の一括管理
   - 結果の集約

2. check_models.py
   - モデルの可用性確認
   - APIキーの検証
   - 接続テスト

3. parameters.py
   - モデル定義
   - プロンプト設定
   - 実験パラメータ

### ツール類

#### OpenAIツール
1. batch_cleanup.py
   - バッチリソースの管理
   - 古いバッチの削除
   - ディスク容量の管理

2. batch_result_converter.py
   - JSONLからテキストへの変換
   - メタデータの抽出
   - 結果の標準化

#### 共有ツール
- API接続ユーティリティ
- エラーハンドリング
- ロギング機能

### 結果管理
1. aggregate_experiment_results.py
   - 結果の集計
   - 統計分析
   - レポート生成

2. results/ディレクトリ
   - モデル別の結果保存
   - バッチ処理結果
   - 変換済みテキストファイル

## 依存関係

### 必須パッケージ
```
python>=3.12
google-generativeai>=0.3.0
anthropic>=0.43.0
openai>=1.0.0
python-dotenv>=1.0.0
```

### 環境変数
```bash
GEMINI_API_KEY="your_gemini_api_key"
ANTHROPIC_API_KEY="your_anthropic_api_key"
XAI_API_KEY="your_xai_api_key"
OPENAI_API_KEY="your_openai_api_key"
KLUSTERAI_API_KEY="your_klusterai_api_key"
```

## デプロイメント

### 開発環境
1. リポジトリのクローン
```bash
git clone https://github.com/nshrhm/llm-literary-analysis.git
cd llm-literary-analysis
```

2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

### テスト実行
```bash
# モデル可用性の確認
python check_models.py

# 個別モデルのテスト
python grok_example.py
python gemini_example.py
python claude_example.py
python openai_example.py
python deepseek_example.py
python llama_example.py
```

## コーディング規約

### スタイルガイド
- PEP 8準拠
- タイプヒントの使用
- ドキュメント文字列の必須化
- 日本語コメントの推奨

### コードフォーマット
```python
def example_function(param1: str, param2: int = 0) -> Dict[str, Any]:
    """機能の説明を記載

    Args:
        param1: パラメータ1の説明
        param2: パラメータ2の説明（デフォルト: 0）

    Returns:
        処理結果の説明

    Raises:
        ValueError: エラーの条件を説明
    """
    pass
```

### エラーハンドリング
- 具体的な例外の使用
- エラーメッセージの日本語化
- ログの構造化
- リカバリー手順の明確化

## 拡張ガイド

### 新規モデルの追加
1. parameters.pyにモデル定義を追加
2. モデル固有の実行スクリプトを作成
3. バッチ処理対応（オプション）
4. テストの実装

### 機能拡張
1. 既存インターフェースの確認
2. 互換性の維持
3. ドキュメントの更新
4. テストケースの追加

## メンテナンス

### 定期タスク
- 古いバッチ結果の削除
- リソース使用量の確認
- APIキーの更新
- 依存パッケージの更新

### トラブルシューティング
1. ログの確認
2. エラーパターンの特定
3. 設定の検証
4. 環境変数の確認
