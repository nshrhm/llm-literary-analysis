"""Configuration parameters for the experiment."""

# Prompt definitions
BASE_PROMPT = """以下のテキストを読んで、4つの感情（面白さ、驚き、悲しみ、怒り）について0-100の数値で評価し、
その理由も説明してください。

テキスト：
{text_content}

回答は以下の形式で記述してください：
Q1. 面白さ(数値): [0-100]
Q1. 面白さ(理由): [説明]

Q2. 驚き(数値): [0-100]
Q2. 驚き(理由): [説明]

Q3. 悲しみ(数値): [0-100]
Q3. 悲しみ(理由): [説明]

Q4. 怒り(数値): [0-100]
Q4. 怒り(理由): [説明]"""

SYSTEM_PROMPTS = {
    "p1": "あなたは大学１年生です。日本の文学テキストに対する感情分析を行います。",
    "p2": "あなたは文学研究者です。日本の文学テキストに対する感情分析を行います。",
    "p3": "あなたは感情豊かな詩人です。日本の文学テキストに対する感情分析を行います。",
    "p4": "あなたは無感情なロボットです。日本の文学テキストに対する感情分析を行います。"
}

# Model-specific prompt configurations
MODEL_CONFIGS = {
    "openai": {
        "standard": {
            "max_tokens": 1024,
            "format": "messages"
        },
        "o1-mini": {
            "max_tokens": 1024,
            "format": "combined"  # system+userを結合
        }
    },
    "claude": {
        "standard": {
            "max_tokens": 1024,
            "format": "content"
        }
    },
    "gemini": {
        "standard": {
            "max_tokens": 1024,
            "format": "messages"
        }
    },
    "grok": {
        "standard": {
            "max_tokens": 1024,
            "format": "messages"
        }
    },
    "deepseek": {
        "standard": {
            "max_tokens": 1024,
            "format": "messages"
        }
    },
    "llama": {
        "standard": {
            "max_tokens": 1024,
            "format": "messages"
        }
    }
}


# Persona definitions
PERSONAS = {
    "p1": "大学１年生",
    "p2": "文学研究者",
    "p3": "感情豊かな詩人",
    "p4": "無感情なロボット"
}

# Text definitions
TEXTS = {
    "t1": "懐中時計",
    "t2": "お金とピストル",
    "t3": "ぼろぼろな駝鳥"
}

# Model definitions
GROK_MODELS = {
    "grok20l": "grok-2-latest",
}

GEMINI_MODELS = {
    "gemma30": "gemma-3-27b-it",
    "gemini20fte": "gemini-2.0-flash-thinking-exp",
    "gemini20pe": "gemini-2.0-pro-exp",
    "gemini20fl": "gemini-2.0-flash-lite-001",
    "gemini20f": "gemini-2.0-flash-001",
    "gemini15f": "gemini-1.5-flash-8b-latest",
    "gemini15p": "gemini-1.5-pro-latest"
}

# Claude model definitions
CLAUDE_MODELS = {
    "claude37s": "claude-3-7-sonnet-20250219",
    "claude35s": "claude-3-5-sonnet-20241022",
    "claude35h": "claude-3-5-haiku-20241022",
    "claude30s": "claude-3-sonnet-20240229",
    "claude30h": "claude-3-haiku-20240307",
    # 2025/03/18: API利用コストが高額なため一時的に無効化
    # 将来的に費用対効果が改善した場合は再度有効化を検討
    # "claude30o": "claude-3-opus-20240229"
}

# DeepSeek model definitions
DEEPSEEK_MODELS = {
    "deepseekr1": "deepseek-ai/DeepSeek-R1",
    "deepseekv3": "deepseek-ai/DeepSeek-V3"
}

# Llama model definitions
LLAMA_MODELS = {
    "llama33-70Bit": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
    "llama31-405Bit": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
    "llama31-8Bit": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo"
}

# Model type definitions
MODEL_TYPES = {
    "grok": GROK_MODELS,
    "gemini": GEMINI_MODELS,
    "claude": CLAUDE_MODELS,
    "deepseek": DEEPSEEK_MODELS,
    "llama": LLAMA_MODELS
}

# OpenAI model definitions
OPENAI_MODELS = {
    "gpt-4o": {
         "model_name": "gpt-4o",
         "type": "text_generation",
         "endpoint": "https://api.openai.com/v1/engines/gpt-4o/completions"
    },
    "gpt-4o-mini": {
         "model_name": "gpt-4o-mini",
         "type": "text_generation",
         "endpoint": "https://api.openai.com/v1/engines/gpt-4o-mini/completions"
    },
    "o3-mini": {
         "model_name": "o3-mini",
         "type": "reasoning",
         "temperature_support": False,
         "endpoint": "https://api.openai.com/v1/engines/o3-mini/completions"
    },
    "o1-mini": {
         "model_name": "o1-mini",
         "type": "reasoning",
         "temperature_support": False,
         "endpoint": "https://api.openai.com/v1/engines/o1-mini/completions"
    }
}

# Experiment parameters
TRIALS = 1
TEMPERATURE = 0.5

# Text content definitions
TEXT_CONTENT = {
    "t1": """懐中時計が箪笥の向う側へ落ちて一人でチクタクと動いておりました。
鼠が見つけて笑いました。
「馬鹿だなあ。誰も見る者はないのに、何だって動いているんだえ」
「人の見ない時でも動いているから、いつ見られても役に立つのさ」
と懐中時計は答えました。
「人の見ない時だけか、又は人が見ている時だけに働いているものはどちらも泥棒だよ」
鼠は恥かしくなってコソコソと逃げて行きました。""",

    "t2": """泥棒がケチンボの家へ入ってピストルを見せて、お金を出せと言いました。ケチンボは、
「ただお金を出すのはいやだ。その短銃(ピストル)を売ってくれるなら千円で買おう。お前は私からお金さえ貰えばそんなピストルは要らないだろう」
泥棒は考えておりましたが、とうとうそのピストルを千円でケチンボに売りました。ケチンボは泥棒からピストルを受け取ると、すぐにも泥棒を撃ちそうにしながら、
「さあ、そのお金ばかりでない、ほかで盗んだお金もみんな出せ。出さないと殺してしまうぞ」
と怒鳴りました。
泥棒は腹を抱えて笑いました。
「アハハ。そのピストルはオモチャのピストルで、撃っても弾丸が出ないのだよ」
と言ううちに表へ逃げ出しました。ケチンボはピストルを投げ出して泥棒を追っかけて、往来で取っ組み合いを始めましたが、やがて通りかかったおまわりさんが二人を押えて警察へ連れて行きました。
警察でいろいろ調べてみますと、泥棒が貰った千円のお金はみんな贋物のお金で、ピストルはやっぱり本物のピストルでした。
二人共牢屋へ入れられました。""",

    "t3": """何が面白くて駝鳥を飼かうのだ。
動物園の四坪半のぬかるみの中では、
脚が大股過ぎるぢじゃないか。
頚があんまり長過ぎるぢゃないか。
雪の降る国にこれでは羽がぼろぼろ過ぎるぢゃないか。
腹がへるから堅パンも喰ふくだらうが、
駝鳥の眼は遠くばかり見てゐるぢじゃないか。
身も世もない様に燃えてゐるぢじゃないか。
瑠璃色の風が今にも吹いて来るのを待ちかまへえてゐるぢじゃないか。
あの小さな素朴な頭が無辺大の夢で逆まいてゐるぢゃないか。
これはもう駝鳥ぢゃないぢゃないか。
人間よ、
もう止せ、こんな事は。"""
}
