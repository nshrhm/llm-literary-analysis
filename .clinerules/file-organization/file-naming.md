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

  3. その他のモデル
  - gemini15f
  - claude30h
  など

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

## メタデータ形式

ファイル内のメタデータは以下の形式で記録：

```
timestamp: YYYY-MM-DD HH:MM:SS
persona: p1-p4
model: [Display Name]  # 例：Llama-3.3-70B, DeepSeek-R1
trial: n01-n03
temperature: 0.5
text: t1-t3
```

## 集計ファイル

集計CSVファイルのモデルカラムには表示名を使用：
- Llama-3.3-70B
- Llama-3.1-405B
- Llama-3.1-8B
- DeepSeek-R1
- DeepSeek-V3
- DeepSeek-V3-0324
