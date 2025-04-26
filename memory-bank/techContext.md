# 技術コンテキスト

## 開発環境

### 言語とバージョン
- Python 3.12
- UTF-8エンコーディング
- 日本語テキスト処理対応

### 依存関係
- google-generativeai>=0.3.0
- anthropic>=0.43.0
- openai>=1.0.0
- python-dotenv>=1.0.0

## 温度制御システム（2025-04-11更新）

### 概要
文学解析の精度を高めるため、ペルソナベースの温度制御システムを実装。各ペルソナの特性とテキストの性質を組み合わせて最終的な温度を決定します。

### 実装の変更点（2025-04-11）
1. プロンプト形式の強化
   - システムメッセージとユーザーメッセージの分離
   - 数値回答形式の明確化
   - エラー検出機能の改善

2. パターンマッチングの拡張
   - 8種類の日本語パターンに対応
   - より柔軟な形式認識
   - エラー耐性の向上

3. 基本実装の改善
   - デフォルト値0.5の削除
   - PERSONAS/TEXTSからの直接的な温度計算の実装
   - OpenAIの特殊ケース（reasoningモデル）の維持
   - ストリーミング応答への対応（Gemini）

### プロンプト形式
```python
enhanced_prompt = f"""
{system}

重要：必ず以下の形式で回答してください。各項目の数値を必ず記入してください。

{user}

注意：
- 必ず数値を[0-100]の範囲で明示的に記入してください
- 各項目の(数値)と(理由)を明確に分けて記述してください
- 形式は厳密に守ってください
"""
```

### パターンマッチング
```python
patterns = [
    rf"Q\d+\.\s*{question}\(数値\):\s*(\d+)",  # Q1. 面白さ(数値): 80
    rf"Q\d+\.\s*{question}:\s*\(数値\):\s*(\d+)",  # Q1. 面白さ: (数値): 80
    rf"Q\d+\.\s*{question}\s*数値:\s*(\d+)",  # Q1. 面白さ 数値: 80
    rf"Q\d+\.\s*{question}:\s*(\d+)",  # Q1. 面白さ: 80
    rf"{question}(?:の評価)?(?:\s*[:：]\s*|\s+)(\d+)",  # 面白さ: 80 or 面白さの評価: 80
    rf"{question}(?:度|レベル)(?:\s*[:：]\s*|\s+)(\d+)",  # 面白さ度: 80 or 面白さレベル: 80
    rf"「{question}」\s*[:：]?\s*(\d+)",  # 「面白さ」: 80
    rf"\[{question}\]\s*[:：]?\s*(\d+)"  # [面白さ]: 80
]
```

### 主要コンポーネント

#### ペルソナベースの基本温度
```python
PERSONAS = {
    "p1": {  # 大学１年生
        "base_temperature": 0.7,  # 柔軟な思考を促進
        "description": "若く柔軟な発想を持つ大学1年生"
    },
    "p2": {  # 文学研究者
        "base_temperature": 0.4,  # 論理的分析を重視
        "description": "論理的で分析的な文学研究者"
    },
    "p3": {  # 感情豊かな詩人
        "base_temperature": 0.9,  # 創造性を最大限に
        "description": "繊細で感情豊かな詩人"
    },
    "p4": {  # 無感情なロボット
        "base_temperature": 0.1,  # 決定論的な応答を促進
        "description": "機械的で論理的なロボット"
    }
}
```

#### テキスト特性による調整
```python
TEXTS = {
    "t1": {
        "name": "懐中時計",
        "temperature_modifier": 0.0  # 寓話的なテキスト
    },
    "t2": {
        "name": "お金とピストル",
        "temperature_modifier": 0.0  # 物語的なテキスト
    },
    "t3": {
        "name": "ぼろぼろな駝鳥",
        "temperature_modifier": 0.0  # 詩的なテキスト
    }
}
```

### 実装の詳細

#### 温度計算
```python
base_temp = PERSONAS[persona_key]["base_temperature"]
temp_modifier = TEXTS[text_key]["temperature_modifier"]
temperature = base_temp + temp_modifier
```

#### モデル固有の処理
1. 標準モデル：
   - 計算された温度を使用
   - 結果ファイルに温度値を記録

2. OpenAI推論モデル：
   - 温度パラメータを使用しない
   - 結果ファイルにNoneとして記録

#### 結果の保存形式
```
timestamp: [YYYY-MM-DD HH:MM:SS]
persona: [ペルソナ名]
model: [モデル名]
trial: [試行番号]
temperature: [温度値 or None]
...
```

### 次のステップ

#### 実装の改善
- 温度値の範囲チェック追加
- エラーハンドリングの強化
- ログ出力の詳細化

#### モニタリング強化
- 温度設定と結果の相関分析
- モデル別のパフォーマンス追跡
- エラー率の監視

#### 将来の拡張
- 動的な温度調整
- モデル固有の温度補正
- バッチ処理の最適化

## APIインテグレーション

### OpenAI API（2025-04-15更新）
1. バッチ処理
   a. 基本仕様（Ver.1）
      - エンドポイント: `/v1/chat/completions`
      - フォーマット: JSONL
      - コスト削減: 50%
      - 処理時間: 24時間以内
      - 制限:
        - 最大50,000リクエスト/バッチ
        - ファイルサイズ上限: 200MB

   b. GPT-4.1シリーズの価格設定（2025-04-15）
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

2. モデル固有の制約
   - o3-mini: 温度パラメータなし
   - o1-mini: システムロールなし

3. バッチ結果変換（2025-03-27実装）
   - tools/openai/batch_result_converter.py
   - 機能:
     - JSONLからテキストファイルへの変換
     - Unicodeエスケープの解決
     - temperature: None対応
   - 入力: batch_results/<batch_id>_output.jsonl
   - 出力: results/openai/*.txt

### Claude API（2025-04-25更新）
1. Message Batches API
   - 最大100,000リクエスト
   - 29日間の結果保持
   - スロットリング: 100リクエスト/分

2. PromptManager統合
   ```python
   # コンテンツ形式の生成
   prompt = PromptManager.get_prompt(
       model_type="claude",
       persona_id=persona_id,
       text_content=text_content,
       text_id=text_id,
       model_id=model_id
   )

   # Claudeバッチリクエスト形式
   request = Request(
       custom_id=custom_id,
       params=MessageCreateParamsNonStreaming(
           model=model_config,
           system=prompt["system"],
           messages=prompt["messages"],
           temperature=temp_value
       )
   )
   ```

3. バッチ処理の最適化
   - システム/ユーザーメッセージの分離
   - 温度制御の統一管理
   - カスタムIDの標準化
   - メタデータの一貫性確保

2. 標準機能
   - temperature
   - max_tokens
   - system messages
   - prompt caching

### kluster.ai API
1. DeepSeekモデル
   - R1, V3, V3-0324
   - OpenAI互換インターフェース
   - バッチ処理対応

2. Llamaモデル（2025-04-25追加）
   - 70B, 405B, 8B
   - バッチ処理サポート
   - 24時間処理ウィンドウ
   - チェック機能の実装完了
   - OpenAI互換インターフェースを使用
   - シンプルなテストリクエストによる可用性確認

## ファイル構造

### プロジェクト構成
```
llm-literary-analysis/
├── tools/
│   ├── openai/
│   │   ├── batch_cleanup.py
│   │   ├── batch_result_converter.py  # 2025-03-27追加
│   │   └── tests/
│   └── shared/
└── results/
    ├── openai/
    │   ├── batch_results/
    │   └── *.txt
    ├── claude/
    ├── deepseek/
    └── llama/
```

### 結果ファイル形式
1. バッチ結果（JSONL）
```json
{
  "custom_id": "p{persona}_{model}_n{trial}_{text}",
  "response": {
    "status_code": 200,
    "body": {
      "choices": [{
        "message": {
          "content": "..."
        }
      }]
    }
  }
}
```

2. 変換後のテキストファイル
```
timestamp: YYYY-MM-DD HH:MM:SS
persona: p1-p4
model: model_name
trial: n01-n10
temperature: value or None
text: t1-t3

Q1value: [0-100]
Q1reason: [explanation]
...
Q4value: [0-100]
Q4reason: [explanation]
```

## 実装詳細

### バッチ処理
1. リクエスト生成
```python
def create_batch_request(requests):
    return {
        "custom_id": generate_custom_id(),
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model_name,
            "messages": messages,
            "temperature": temp  # 推論モデルでは省略
        }
    }
```

2. 結果変換（2025-03-27実装）
```python
def convert_batch_results(input_file):
    """Convert batch results to text files."""
    for line in read_jsonl(input_file):
        metadata = extract_metadata(line)
        content = extract_content(line)
        if is_reasoning_model(metadata['model']):
            metadata['temperature'] = None
        save_result_file(metadata, content)
```

### エラーハンドリング
1. バッチエラー
```python
def handle_batch_error(error):
    if error.is_rate_limit:
        retry_with_backoff()
    elif error.is_partial_failure:
        handle_partial_results()
    else:
        raise BatchProcessingError(error)
```

2. 変換エラー
```python
def handle_conversion_error(error):
    log_error(error)
    if error.is_unicode:
        retry_with_encoding()
    elif error.is_format:
        skip_and_log()
    else:
        raise ConversionError(error)
```

## 監視と制御

### バッチ監視
1. ステータスチェック
   - 5分間隔での確認
   - エラー時の自動ログ
   - 完了通知

2. エラー監視
   - エラー率の追跡
   - リトライ回数の制限
   - クリティカルエラーの通知

### リソース管理
1. ファイル管理
   - 自動バックアップ
   - 古いバッチの削除
   - ディスク使用量の監視

2. API制限
   - レート制限の遵守
   - コスト最適化
   - 並列実行の制御
