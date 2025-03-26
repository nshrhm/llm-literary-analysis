# Technical Context Memory Bank

## モデル識別子とファイル名の設計
### ファイル命名規則
```
{persona_id}_{model_identifier}_{text_id}_{trial_num}_temp{temperature}.txt
```
例：
- p1_llama33-70Bit_t1_n01_temp50.txt
- p1_deepseekr1_t1_n01_temp50.txt

### モデル識別子
1. Llamaモデル
- llama33-70Bit → Llama-3.3-70B
- llama31-405Bit → Llama-3.1-405B
- llama31-8Bit → Llama-3.1-8B

2. DeepSeekモデル
- deepseekr1 → DeepSeek-R1
- deepseekv3 → DeepSeek-V3
- deepseekv3-0324 → DeepSeek-V3-0324

## 実装の詳細
### モデル識別子の抽出
```python
def _get_model_identifier(self, model: str) -> str:
    # Check DeepSeek models
    if model_id == "deepseekr1":
        return "deepseekr1"
    elif model_id == "deepseekv3":
        return "deepseekv3"
    elif model_id == "deepseekv3-0324":
        return "deepseekv3-0324"

    # Check Llama models
    # Return model_id directly as it's already in correct format
```

### モデル表示名の生成
```python
def _get_model_display_name(self, model: str) -> str:
    # DeepSeek display names
    if model_id == "deepseekr1":
        return "DeepSeek-R1"
    elif model_id == "deepseekv3":
        return "DeepSeek-V3"
    elif model_id == "deepseekv3-0324":
        return "DeepSeek-V3-0324"

    # Llama display names
    if model_id == "llama33-70Bit":
        return "Llama-3.3-70B"
    elif model_id == "llama31-405Bit":
        return "Llama-3.1-405B"
    elif model_id == "llama31-8Bit":
        return "Llama-3.1-8B"
```

## メタデータの構造
```
timestamp: YYYY-MM-DD HH:MM:SS
persona: p1-p4
model: [Display Name]
trial: n01-n03
temperature: 0.5
text: t1-t3
```

## 集計ファイル形式
```
timestamp,persona,model,trial,temperature,text,Q1value,Q2value,Q3value,Q4value,Q1reason,Q2reason,Q3reason,Q4reason
```
- modelカラムには表示名（例：Llama-3.3-70B）が使用される
