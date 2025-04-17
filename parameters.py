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
            "format": "messages",
            "temperature_support": True  # 明示的に設定
        },
        "o1-mini": {
            "max_tokens": 1024,
            "format": "combined",  # system+userを結合
            "temperature_support": False  # 明示的に設定
        },
        "reasoning": {
            "max_tokens": 1024,
            "format": "combined",  # system+userを結合
            "temperature_support": False  # reasoningモデル用の共通設定
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


# Persona definitions with temperature settings
PERSONAS = {
    "p1": {
        "name": "大学１年生",
        "base_temperature": 0.7,
        "description": "若く柔軟な発想を持つ大学1年生"
    },
    "p2": {
        "name": "文学研究者",
        "base_temperature": 0.4,
        "description": "論理的で分析的な文学研究者"
    },
    "p3": {
        "name": "感情豊かな詩人",
        "base_temperature": 0.9,
        "description": "繊細で感情豊かな詩人"
    },
    "p4": {
        "name": "無感情なロボット",
        "base_temperature": 0.1,
        "description": "機械的で論理的なロボット"
    }
}

# Text definitions with temperature modifiers
TEXTS = {
    "t1": {
        "name": "懐中時計",
        "temperature_modifier": 0.0  # 寓話的なテキストを踏まえてえ変更も可能
    },
    "t2": {
        "name": "お金とピストル",
        "temperature_modifier": 0.0  # 物語的なテキストを踏まえてえ変更も可能
    },
    "t3": {
        "name": "ぼろぼろな駝鳥",
        "temperature_modifier": 0.0  # 詩的なテキストを踏まえてえ変更も可能
    }
}

# Model definitions

# OpenAI model definitions
OPENAI_MODELS = {
    "gpt-4.1": {
        "model_name": "gpt-4.1",
        "type": "text_generation",
        "pricing": {
            "input": 2.00,
            "cached_input": 0.50,
            "output": 8.00
            },
        "endpoint": "https://api.openai.com/v1/engines/gpt-4.1/completions"
    },
    "gpt-4.1-mini": {
        "model_name": "gpt-4.1-mini",
        "type": "text_generation",
        "pricing": {
            "input": 0.40,
            "cached_input": 0.10,
            "output": 1.60
        },
        "endpoint": "https://api.openai.com/v1/engines/gpt-4.1-mini/completions"
    },
    "gpt-4.1-nano": {
        "model_name": "gpt-4.1-nano",
        "type": "text_generation",
        "pricing": {
            "input": 0.10,
            "cached_input": 0.025,
            "output": 0.40
        },
        "endpoint": "https://api.openai.com/v1/engines/gpt-4.1-nano/completions"
    },
    "gpt-4o": {
        "model_name": "gpt-4o",
        "type": "text_generation",
        "pricing": {
            "input": 2.50,
            "cached_input": 1.25,
            "output": 10.00
        },
        "endpoint": "https://api.openai.com/v1/engines/gpt-4o/completions"
    },
    "gpt-4o-mini": {
        "model_name": "gpt-4o-mini",
        "type": "text_generation",
        "pricing": {
            "input": 0.15,
            "cached_input": 0.075,
            "output": 0.60
        },
        "endpoint": "https://api.openai.com/v1/engines/gpt-4o-mini/completions"
    },
    "o4-mini": {
        "model_name": "o4-mini",
        "type": "reasoning",
        "temperature_support": False,  # このモデルはtemperatureパラメータをサポートしない
        "pricing": {
            "input": 1.10,
            "cached_input": 0.275,
            "output": 4.40
        },
        "endpoint": "https://api.openai.com/v1/engines/o4-mini/completions"
    },
    "o3": {
        "model_name": "o3",
        "type": "reasoning",
        "temperature_support": False,  # このモデルはtemperatureパラメータをサポートしない
        "pricing": {
            "input": 10,
            "cached_input": 2.5,
            "output": 40
        },
        "endpoint": "https://api.openai.com/v1/engines/o3/completions"
    },
    "o3-mini": {
        "model_name": "o3-mini",
        "type": "reasoning",
        "temperature_support": False,  # このモデルはtemperatureパラメータをサポートしない
        "pricing": {
            "input": 1.10,
            "cached_input": 0.55,
            "output": 4.40
        },
        "endpoint": "https://api.openai.com/v1/engines/o3-mini/completions"
    },
    "o1-mini": {
        "model_name": "o1-mini",
        "type": "reasoning",
        "temperature_support": False,  # このモデルはtemperatureパラメータをサポートしない
        "pricing": {
            "input": 1.10,
            "cached_input": 0.55,
            "output": 4.40
        },
        "endpoint": "https://api.openai.com/v1/engines/o1-mini/completions"
    }
}

# Claude model definitions
CLAUDE_MODELS = {
    # Note: claude-3-sonnet-20240229 does not support batching
    # Using other supported models
    "claude37s": "claude-3-7-sonnet-20250219",
    "claude35s": "claude-3-5-sonnet-20241022",
    "claude35h": "claude-3-5-haiku-20241022",
    "claude30h": "claude-3-haiku-20240307"
    
    # Temporarily disabled models
    # "claude30s": "claude-3-sonnet-20240229" # Does not support batching
    # "claude30o": "claude-3-opus-20240229"   # Cost optimization
}

GEMINI_MODELS = {
    # Gemini 2.5/2.0シリーズ
    "gemini25p": "gemini-2.5-pro-preview-03-25",
    "gemini20f": "gemini-2.0-flash",
    "gemini20fl": "gemini-2.0-flash-lite",
    "gemini20p": "gemini-2.0-pro-exp",
    "gemini20t": "gemini-2.0-flash-thinking-exp",
    
    # Gemma シリーズ
    "gemma1b": "gemma-3-1b-it",
    "gemma4b": "gemma-3-4b-it",
    "gemma12b": "gemma-3-12b-it",
    "gemma27b": "gemma-3-27b-it"
}

GROK_MODELS = {
    # Grok 2シリーズ（8 requests/second）
    "grok20l": "grok-2-latest",
    
    # Grok 3シリーズ（5 requests/second）
    "grok3mf": "grok-3-mini-fast-latest",
    "grok3m": "grok-3-mini-latest",
    "grok3f": "grok-3-fast-latest",
    "grok3": "grok-3-latest"
}

# DeepSeek model definitions
DEEPSEEK_MODELS = {
    "deepseekr1": "deepseek-ai/DeepSeek-R1",
    "deepseekv3": "deepseek-ai/DeepSeek-V3",
    "deepseekv3-0324": "deepseek-ai/DeepSeek-V3-0324"
}

# Llama model definitions
LLAMA_MODELS = {
    "llama4-maveric": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    "llama4-scout": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    "llama33-70Bit": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
    # "llama31-405Bit": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
    # "llama31-8Bit": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo"
}

# Experiment parameters
TRIALS = 10  # 試行回数を10回に設定

# Model type definitions (Reserved for future unified model selection)
# Currently not used in the codebase as of 2025-03
# Planned usage: Provider-agnostic model configuration
MODEL_TYPES = {
  "openai": OPENAI_MODELS,
  "claude": CLAUDE_MODELS,
  "gemini": GEMINI_MODELS,
  "grok": GROK_MODELS,
  "deepseek": DEEPSEEK_MODELS,
  "llama": LLAMA_MODELS
}

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
