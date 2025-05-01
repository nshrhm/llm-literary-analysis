# モデルガイド

## モデル選択ガイド（2025-04-24追加）

各モデルの実行時には、短縮名（モデルID）を使用してモデルを指定します。以下に各モデルのIDと正式名称の対応を示します。

### Google Geminiモデル
| モデルID | 正式名称 | 説明 |
|----------|----------|------|
| gemini25p | gemini-2.5-pro-preview-03-25 | Pro Preview 2.5 |
| gemini25f | gemini-2.5-flash-preview-04-17 | Flash Preview 2.5 |
| gemini20f | gemini-2.0-flash | Flash 2.0 |
| gemini20fl | gemini-2.0-flash-lite | Flash Lite 2.0 |
| gemini20p | gemini-2.0-pro-exp | Pro Exp 2.0 |
| gemini20t | gemini-2.0-flash-thinking-exp | Flash Thinking 2.0 |

### Anthropic Claudeモデル
| モデルID | 正式名称 | 説明 |
|----------|----------|------|
| claude37s | claude-3-7-sonnet-20250219 | Sonnet 3.7 |
| claude35s | claude-3-5-sonnet-20241022 | Sonnet 3.5 |
| claude35h | claude-3-5-haiku-20241022 | Haiku 3.5 |
| claude30h | claude-3-haiku-20240307 | Haiku 3.0 |

### X.AI Grokモデル
| モデルID | 正式名称 | 説明 |
|----------|----------|------|
| grok20l | grok-2-latest | Grok 2シリーズ最新版 |
| grok3mf | grok-3-mini-fast-latest | Grok 3 Mini Fast |
| grok3m | grok-3-mini-latest | Grok 3 Mini |
| grok3f | grok-3-fast-latest | Grok 3 Fast |
| grok3 | grok-3-latest | Grok 3標準 |

### DeepSeekモデル
| モデルID | 正式名称 | 説明 |
|----------|----------|------|
| deepseekr1 | deepseek-ai/DeepSeek-R1 | R1シリーズ |
| deepseekv3 | deepseek-ai/DeepSeek-V3 | V3シリーズ |
| deepseekv3-0324 | deepseek-ai/DeepSeek-V3-0324 | V3シリーズ（0324更新版） |

### Meta Llamaモデル（2025-04-25更新）
| モデルID | 正式名称 | 説明 |
|----------|----------|------|
| llama4-maveric | meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8 | Maverick 17B |
| llama4-scout | meta-llama/Llama-4-Scout-17B-16E-Instruct | Scout 17B |
| llama33-70Bit | klusterai/Meta-Llama-3.3-70B-Instruct-Turbo | 70B Instruct Turbo |

### OpenAIモデル
| モデルID | 正式名称 | 説明 |
|----------|----------|------|
| gpt-4.1 | gpt-4.1 | 高精度解析向け（高コスト） |
| gpt-4.1-mini | gpt-4.1-mini | 一般的な解析タスク向け（中コスト） |
| gpt-4.1-nano | gpt-4.1-nano | 軽量な解析に最適（低コスト） |
| gpt-4o | gpt-4o | テキスト生成モデル |
| gpt-4o-mini | gpt-4o-mini | テキスト生成モデル（軽量版） |
| o4-mini | o4-mini | 推論モデル |
| o3 | o3 | 推論モデル |
| o3-mini | o3-mini | 推論モデル（軽量版） |
| o1-mini | o1-mini | 推論モデル（軽量版） |

#### モデルチェック機能
- KLUSTERAI_API_KEYによる認証
- OpenAI互換インターフェースを使用
- シンプルなテストリクエストによる可用性確認
- バッチ処理との統合テスト機能

#### チェック方法
```bash
# すべてのモデルをチェック
python check_models.py

# Llamaモデルのみをチェック
python llama_example.py --check
```

## 使用例
複数のモデルを選択して実行する場合：
```bash
# Geminiモデルの場合
python gemini_example.py --model gemini25p gemini25f

# Claudeモデルの場合
python claude_example.py --model claude37s claude35s

# Grokモデルの場合
python grok_example.py --model grok20l grok3mf

# DeepSeekモデルの場合
python deepseek_example.py --model deepseekr1 deepseekv3

# Llamaモデルの場合
python llama_example.py --model llama4-maveric llama4-scout

# OpenAIモデルの場合
python openai_example.py --model gpt-4.1 gpt-4.1-mini
```

バッチ処理と組み合わせる場合：
```bash
python claude_example.py --batch --model claude37s claude35s

python openai_example.py --batch --model gpt-4.1 gpt-4.1-mini
```

## サポート対象モデル

### Google Gemini（2025-04-19更新）
1. Gemini 2.5シリーズ：
   - Pro Preview（2.5）
   - Flash Preview（2.5）：新規追加（2025-04-19）
     - 高速処理に最適化
     - バッチ処理の安定性向上
     - 標準フォーマットへの完全準拠

2. Gemini 2.0シリーズ：
   - Pro Exp
   - Flash Thinking Exp
   - Flash
   - Flash Lite

3. Gemmaシリーズ：
   - 27B IT
   - 12B IT
   - 4B IT
   - 1B IT

### Anthropic Claude
- Claude 3.7: Sonnet
- Claude 3.5: Sonnet, Haiku
- Claude 3.0: Sonnet, Haiku

注：Claude-3-Opusモデル（claude-3-opus-20240229）は、API費用が高額なため一時的に無効化されています（2025/03/18現在）。

### X.AI Grok
- Grok 2.0: Latest

### OpenAI
- テキスト生成モデル：
  - GPT-4.1（2025/04/15追加）：
    - gpt-4.1：高精度解析向け（高コスト）
      - Input: $2.00
      - Cached input: $0.50
      - Output: $8.00
    - gpt-4.1-mini：一般的な解析タスク向け（中コスト）
      - Input: $0.40
      - Cached input: $0.10
      - Output: $1.60
    - gpt-4.1-nano：軽量な解析に最適（低コスト）
      - Input: $0.10
      - Cached input: $0.025
      - Output: $0.40
  - GPT-4: o, o-mini
- 推論モデル：
  - O3: mini
  - O1: mini

### kluster.ai DeepSeek
- DeepSeek-R1
- DeepSeek-V3
- DeepSeek-V3-0324

### kluster.ai Meta Llama
- Llama 3.3: 70B Instruct Turbo
- Llama 3.1: 405B Instruct Turbo, 8B Instruct Turbo

## モデル固有の制約事項

### OpenAI推論モデル
1. o3-mini
   - 温度パラメータ（temperature）非対応
   - 標準の結果フォーマットに準拠

2. o1-mini
   - システムロール非対応
   - 温度パラメータ（temperature）非対応

3. o4-mini
   - 温度パラメータ（temperature）非対応

4. o3
   - 温度パラメータ（temperature）非対応

### Claude
- claude-3-sonnet-20240229はバッチ処理非対応
- Message Batches APIで最大100,000リクエストまで対応
- スロットリング：100リクエスト/分

### Gemini（2025-04-19更新）
1. Gemini 2.5 Flash Preview
   - バッチ処理の最適化
   - 高速な応答生成
   - 効率的なリソース使用

2. 共通の制約
   - レート制限の考慮
   - メモリ使用量の最適化
   - 並列処理の制御

### DeepSeek & Llama（2025-04-25更新）
1. DeepSeekモデル
   - OpenAI互換APIインターフェース
   - 24時間処理ウィンドウ
   - バッチサイズの最適化が必要

2. Llamaモデル
   - OpenAI互換APIインターフェース（kluster.ai API）
   - モデルチェック機能による可用性確認
   - 24時間処理ウィンドウ
   - バッチサイズの最適化が必要
   - KLUSTERAI_API_KEYが必要

## 将来の拡張計画
- プロバイダー非依存のモデル選択機能実装予定
- 統一モデルインターフェース(MODEL_TYPES)の活用
- OpenAIモデルの統合対応

## 価格最適化戦略
1. バッチ処理の活用
   - JSONLフォーマットによる50%のコスト削減
   - キャッシュ入力の活用
   - 大規模バッチの効率的な処理

2. モデル選択の最適化
   - タスクの要件に応じた適切なモデルの選択
   - コストと品質のバランス考慮
   - バッチサイズの最適化

## モニタリングとメンテナンス
- モデルの可用性チェック
- APIレート制限の監視
- コスト効率の追跡
- パフォーマンス指標の監視
