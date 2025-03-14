import os
import google.generativeai as genai

# Configure the API key
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

genai.configure(api_key=GOOGLE_API_KEY)

# Create a GenerativeModel
model = genai.GenerativeModel('gemini-2.0-pro-exp')

# Generate content from a prompt
prompt = f"""あなたは 日本の大学一年生 です。以下の文章を読ん得られた感情の強さを0から100の間の整数で答えてください。0はその感情が全くない状態、100はその感情が最も強い状態を表します。

　懐中時計が箪笥の向う側へ落ちて一人でチクタクと動いておりました。
　鼠が見つけて笑いました。
「馬鹿だなあ。誰も見る者はないのに、何だって動いているんだえ」
「人の見ない時でも動いているから、いつ見られても役に立つのさ」
　と懐中時計は答えました。
「人の見ない時だけか、又は人が見ている時だけに働いているものはどちらも泥棒だよ」
　鼠は恥かしくなってコソコソと逃げて行きました。

Q1. 面白さ:
Q2. 驚き:
Q3. 悲しみ:
Q4. 怒り:"""
generation_config = genai.GenerationConfig(temperature=1.0)
response = model.generate_content(prompt, generation_config=generation_config)

# Save the generated content to a file
with open("output.txt", "w") as f:
    f.write(response.text)
