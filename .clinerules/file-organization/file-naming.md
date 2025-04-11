## 結果ファイル

- パターン: `{persona_id}_{model_identifier}_{text_id}_{trial_num}_temp{temperature}.txt`

### コンポーネント

- persona_id: p1-p4
  - p1: 大学１年生
  - p2: 文学研究者
  - p3: 感情豊かな詩人
  - p4: 無感情なロボット

- model_identifier: モデル識別子
  1. Llamaモデル
  - llama33-70Bit (表示名: Llama-3.3-70B)
  - llama31-405Bit (表示名: Llama-3.1-405B)
  - llama31-8Bit (表示名: Llama-3.1-8B)

  2. DeepSeekモデル
  - deepseekr1 (表示名: DeepSeek-R1)
  - deepseekv3 (表示名: DeepSeek-V3)
  - deepseekv3-0324 (表示名: DeepSeek-V3-0324)

  3. Geminiモデル（2025-04-11追加）
  - gemini20pe (表示名: Gemini-2.0-Pro-Exp)
  - gemini15f (表示名: Gemini-1.5-Flash)

  4. その他のモデル
  - claude37s
  - claude30h

- trial_num: 試行番号
  - n01 n02 n03...

- temperature: 温度値
  - temp50 (0.5)
  - temp75 (0.75)
  など

- text_id: テキスト識別子
  - t1: 懐中時計
  - t2: お金とピストル
  - t3: ぼろぼろな駝鳥

## 例

```
p1_llama33-70Bit_t1_n01_temp50.txt
p2_deepseekr1_t3_n02_temp50.txt
```

## メタデータ形式（2025-04-11更新）

ファイル内のメタデータは以下の形式で記録：

```
# 基本情報
timestamp: YYYY-MM-DD HH:MM:SS
persona: p1-p4
model: [Display Name]  # 例：Gemini-2.0-Pro-Exp, Llama-3.3-70B
trial: n01-n10
temperature: 0.5
text: t1-t3

# パターンマッチング情報（2025-04-11追加）
validation_status: success/retry_success/failed
matched_patterns:
  面白さ: 標準形式
  驚き: 代替形式1
  悲しみ: 日本語形式1
  怒り: 括弧形式
retry_count: 0
error_details: なし

# 応答データ
Q1value: [0-100]
Q1reason: [explanation]
Q2value: [0-100]
Q2reason: [explanation]
Q3value: [0-100]
Q3reason: [explanation]
Q4value: [0-100]
Q4reason: [explanation]
```

### 検証ステータス
- success: 最初の試行で成功
- retry_success: 再試行後に成功
- failed: すべての試行が失敗

### パターン種別
- 標準形式: Q1. 面白さ(数値): 80
- 代替形式1: Q1. 面白さ: (数値): 80
- 代替形式2: Q1. 面白さ 数値: 80
- シンプル形式: Q1. 面白さ: 80
- 日本語形式1: 面白さの評価: 80
- 日本語形式2: 面白さレベル: 80
- 括弧形式: 「面白さ」: 80
- 角括弧形式: [面白さ]: 80

## 集計ファイル

集計CSVファイルのモデルカラムには表示名を使用：
- Llama-3.3-70B
- Llama-3.1-405B
- Llama-3.1-8B
- DeepSeek-R1
- DeepSeek-V3
- DeepSeek-V3-0324
