# モデルガイド

## サポート対象モデル

### Google Gemini
- Gemini 2.0: Pro Exp, Flash Thinking Exp, Flash
- Gemini 1.5: Pro, Flash
- Gemma 3.0: 27B IT

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

### Claude
- claude-3-sonnet-20240229はバッチ処理非対応
- Message Batches APIで最大100,000リクエストまで対応
- スロットリング：100リクエスト/分

### DeepSeek & Llama
- OpenAI互換APIインターフェース
- 24時間処理ウィンドウ
- バッチサイズの最適化が必要

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
