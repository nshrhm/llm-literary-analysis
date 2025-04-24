# プロジェクト構造ガイド

## ディレクトリ構造（2025-04-24更新）

```
llm-literary-analysis/
├── experiment_runner.py           # 統合実験ランナー
├── check_models.py               # モデル可用性チェッカー
├── parameters.py                 # 実験パラメータ
├── prompt_manager.py            # プロンプト管理システム（2025-04-11追加）
├── aggregate_experiment_results.py # 結果分析ツール
├── tools/                        # ユーティリティツール
│   ├── openai/                   # OpenAI専用ツール
│   │   ├── batch_cleanup.py     # バッチ管理ツール
│   │   ├── batch_result_converter.py  # バッチ結果変換ツール（2025-03-27更新）
│   │   └── tests/              # OpenAIツールのテスト
│   └── shared/                   # 共有ツール
├── docs/                         # ドキュメント
│   ├── api/                      # APIドキュメント
│   │   ├── openai/              # OpenAI API実装詳細
│   │   ├── claude/              # Claude API実装詳細
│   │   ├── kluster.ai/          # kluster.ai API実装詳細
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
│       ├── batch-temperature.md # バッチ処理時の温度制御
│       └── patterns/            # 実装パターン
└── results/                      # 実験結果
    ├── gemini/                   # Gemini結果
    │   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
    ├── claude/                   # Claude結果
    │   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
    ├── grok/                     # Grok結果
    │   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
    ├── openai/                   # OpenAI結果
    │   ├── batch_results/       # バッチ処理結果
    │   │   └── batch_{id}_output.jsonl
    │   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
    ├── deepseek/                 # DeepSeek結果
    │   └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
    └── llama/                    # Llama結果
        └── {text}_{model}_{persona}_temp{temp}_{trial}.txt
```

## 主要コンポーネント（2025-04-24更新）

### 実験実行
1. experiment_runner.py
   - 全モデルでの実験実行
   - インテリジェント温度設定システム
   - パターンマッチングによる品質保証
   - コスト最適化（GPT-4.1シリーズ）

2. prompt_manager.py（2025-04-11追加）
   - プロンプトの一元管理
   - モデル固有の形式対応
   - 8種類のパターンマッチング
   - 応答品質の検証

3. check_models.py
   - モデルの可用性確認
   - APIキーの検証
   - バッチ処理の検証
   - 温度設定のテスト

4. parameters.py
   - モデル定義と価格情報
   - ペルソナベースの温度設定
   - プロンプト設定
   - 実験パラメータ

### ツール類（2025-04-17更新）

#### OpenAIツール
1. batch_cleanup.py
   - バッチリソースの管理
   - 古いバッチの削除
   - コスト最適化の監視
   - キャッシュ利用の追跡

2. batch_result_converter.py（2025-03-27更新）
   - JSONLからテキストへの変換
   - メタデータの抽出
   - 価格情報の処理（GPT-4.1シリーズ）
   - 温度パラメータの正規化

#### 共有ツール
- 統一的なバッチ処理
- エラーハンドリング
- コスト分析
- パターンマッチング

### 結果管理（2025-04-24更新）
1. aggregate_experiment_results.py
   - 結果の集計とフォーマット統一
   - 統計分析とコスト分析
   - パターンマッチング統計
   - レポート生成

2. results/ディレクトリ
   - 新ファイル命名規則：
     ```
     {text}_{model}_{persona}_temp{temp}_{trial}.txt
     例）t1_gpt-4.1_p1_temp70_01.txt
     ```
   - 温度パラメータの扱い：
     - 標準モデル：実数値（0-100）
     - 推論モデル：temp--
   - バッチ処理結果の保存
   - メタデータと価格情報の管理

## 依存関係（2025-04-19更新）

### 必須パッケージ
```
python>=3.12
google-generativeai>=0.3.0  # Gemini 2.5対応
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

# バッチ処理のテスト
python *_batch_runner.py
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
3. バッチ処理対応の実装
4. 温度設定の構成
5. パターンマッチングの検証
6. テストの実装

### 機能拡張
1. 既存インターフェースの確認
2. 互換性の維持
3. ドキュメントの更新
4. テストケースの追加
5. コスト効率の検証

## メンテナンス

### 定期タスク
- 古いバッチ結果の削除
- リソース使用量の確認
- APIキーの更新
- 依存パッケージの更新
- コスト分析の実行
- パターンマッチング統計の確認

### トラブルシューティング
1. ログの確認
2. エラーパターンの特定
3. 設定の検証
4. 環境変数の確認
5. コスト異常の検出
6. パターンマッチング失敗の分析
