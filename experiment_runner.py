"""Base class and implementations for running the literature analysis experiment."""

import os
import re
import datetime
import google.generativeai as genai
import anthropic
from openai import OpenAI
from parameters import *

# Directory for storing experiment results
RESULTS_DIR = "results"

class BaseExperimentRunner:
    """Base class for experiment runners."""
    
    def __init__(self):
        """Initialize the base experiment runner."""
        self.results_dir = os.path.join(RESULTS_DIR, self.get_model_type())
        os.makedirs(self.results_dir, exist_ok=True)

    def get_model_type(self) -> str:
        """Get the model type (e.g., 'gemini' or 'claude')."""
        raise NotImplementedError("Subclasses must implement get_model_type")

    def generate_prompt(self, persona: str, text_content: str) -> str:
        """Generate the prompt for the experiment.
        
        Args:
            persona: The persona to use for the analysis
            text_content: The text content to analyze
        
        Returns:
            str: The generated prompt
        """
        return f"""あなたは {persona} です。以下の文章を読み、それぞれの感情について、以下の定義と基準に従って0から100の間の整数で評価してください。0はその感情が全くない状態、100はその感情が最も強い状態を表します。そして、その感情の強さの理由を記述してください。

* 感情の定義: 

面白さ: 読んでいて楽しい、愉快だと感じる度合い（基準：物語のユーモラスな表現、意外性のある展開など）
驚き: 予想外の展開や情報に触れ、心が動揺する度合い（基準：物語の展開の斬新さ、予想を裏切る展開など）
悲しみ: 登場人物の心情に共感し、心が痛む度合い（基準：登場人物の心情への共感度合い、物語の結末など）
怒り: 不当な行為や状況に対して、憤りを感じる度合い（基準：登場人物の行動への共感度合い、社会的なテーマへの共感度合い）

{text_content}

Q1. 面白さ(数値): 
Q1. 面白さ(理由): 
Q2. 驚き(数値): 
Q2. 驚き(理由): 
Q3. 悲しみ(数値): 
Q3. 悲しみ(理由): 
Q4. 怒り(数値): 
Q4. 怒り(理由): 
"""

    def extract_value(self, text: str, question: str) -> str:
        """Extract the value from the response text.
        
        Args:
            text: The response text
            question: The question to extract the value for (面白さ, 驚き, etc.)
        
        Returns:
            str: The extracted value
        """
        patterns = [
            rf"Q\d+\.\s*{question}\(数値\):\s*(\d+)",  # Q1. 面白さ(数値): 80
            rf"Q\d+\.\s*{question}:\s*\(数値\):\s*(\d+)",  # Q1. 面白さ: (数値): 80
            rf"Q\d+\.\s*{question}\s*数値:\s*(\d+)",  # Q1. 面白さ 数値: 80
            rf"Q\d+\.\s*{question}:\s*(\d+)",  # Q1. 面白さ: 80 - フォールバックパターン
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1)
        return ""

    def extract_reason(self, text: str, question: str) -> str:
        """Extract the reason from the response text.
        
        Args:
            text: The response text
            question: The question to extract the reason for (面白さ, 驚き, etc.)
        
        Returns:
            str: The extracted reason
        """
        patterns = [
            rf"Q\d+\.\s*{question}\(理由\):\s*(.+?)(?=(?:\n[QA]|$))",  # Q1. 面白さ(理由): [理由]
            rf"Q\d+\.\s*{question}:\s*\(理由\):\s*(.+?)(?=(?:\n[QA]|$))",  # Q1. 面白さ: (理由): [理由]
            rf"Q\d+\.\s*{question}\s*理由:\s*(.+?)(?=(?:\n[QA]|$))",  # Q1. 面白さ 理由: [理由]
            rf"Q\d+\.\s*{question}理由:\s*(.+?)(?=(?:\n[QA]|$))",  # フォールバックパターン
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return ""

    def save_result(self, result: str, params: dict):
        """Save the experiment result to a file.
        
        Args:
            result: The response from the model
            params: Dictionary containing experiment parameters
        """
        filename = f"{params['persona_key']}_{params['model_key']}_n{params['trial']:02d}_temp{int(TEMPERATURE*100):02d}_t{params['text_key']}.txt"
        filepath = os.path.join(self.results_dir, filename)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract values and reasons
        q1_value = self.extract_value(result, "面白さ")
        q1_reason = self.extract_reason(result, "面白さ")
        q2_value = self.extract_value(result, "驚き")
        q2_reason = self.extract_reason(result, "驚き")
        q3_value = self.extract_value(result, "悲しみ")
        q3_reason = self.extract_reason(result, "悲しみ")
        q4_value = self.extract_value(result, "怒り")
        q4_reason = self.extract_reason(result, "怒り")
        
        content = f"""timestamp: {timestamp}
persona: {params['persona']}
model: {params['model']}
trial: {params['trial']}
temperature: {TEMPERATURE}
text: {params['text_name']}
Q1value: {q1_value}
Q1reason: {q1_reason}
Q2value: {q2_value}
Q2reason: {q2_reason}
Q3value: {q3_value}
Q3reason: {q3_reason}
Q4value: {q4_value}
Q4reason: {q4_reason}"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def run_experiment(self):
        """Run the experiment."""
        raise NotImplementedError("Subclasses must implement run_experiment")

class GeminiExperimentRunner(BaseExperimentRunner):
    """Experiment runner for Gemini models."""
    
    def get_model_type(self) -> str:
        return "gemini"

    def __init__(self):
        """Initialize the Gemini experiment runner."""
        super().__init__()
        self._setup_api()

    def _setup_api(self):
        """Set up the Gemini API."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable")
        genai.configure(api_key=api_key)

    def run_experiment(self):
        """Run the experiment with Gemini models."""
        for model_key, model_name in GEMINI_MODELS.items():
            model = genai.GenerativeModel(model_name)
            generation_config = genai.GenerationConfig(temperature=TEMPERATURE)
            
            for persona_key, persona in PERSONAS.items():
                for text_key, text_name in TEXTS.items():
                    text_content = TEXT_CONTENT[text_key]
                    prompt = self.generate_prompt(persona, text_content)
                    
                    for trial in range(1, TRIALS + 1):
                        try:
                            response = model.generate_content(prompt, generation_config=generation_config)
                            
                            params = {
                                "persona_key": persona_key,
                                "text_key": text_key,
                                "model_key": model_key,
                                "trial": trial,
                                "persona": persona,
                                "text_name": text_name,
                                "model": model_name
                            }
                            
                            self.save_result(response.text, params)
                            print(f"Completed: {params['persona_key']}_{params['model_key']}_n{trial:02d}_temp{int(TEMPERATURE*100):02d}_t{params['text_key']}")
                            
                        except Exception as e:
                            print(f"Error in trial {trial} with {model_name}: {str(e)}")
                            continue

class GrokExperimentRunner(BaseExperimentRunner):
    """Experiment runner for Grok models."""
    
    def get_model_type(self) -> str:
        return "grok"

    def __init__(self):
        """Initialize the Grok experiment runner."""
        super().__init__()
        self._setup_api()

    def _setup_api(self):
        """Set up the Grok API."""
        api_key = os.environ.get("XAI_API_KEY")
        if not api_key:
            raise ValueError("Missing XAI_API_KEY environment variable")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

    def run_experiment(self):
        """Run the experiment with Grok models."""
        for model_key, model_name in GROK_MODELS.items():
            for persona_key, persona in PERSONAS.items():
                for text_key, text_name in TEXTS.items():
                    text_content = TEXT_CONTENT[text_key]
                    prompt = self.generate_prompt(persona, text_content)
                    
                    for trial in range(1, TRIALS + 1):
                        try:
                            response = self.client.chat.completions.create(
                                model=model_name,
                                temperature=TEMPERATURE,
                                messages=[
                                    {"role": "user", "content": prompt}
                                ]
                            )
                            
                            params = {
                                "persona_key": persona_key,
                                "text_key": text_key,
                                "model_key": model_key,
                                "trial": trial,
                                "persona": persona,
                                "text_name": text_name,
                                "model": model_name
                            }
                            
                            self.save_result(response.choices[0].message.content, params)
                            print(f"Completed: {params['persona_key']}_{params['model_key']}_n{trial:02d}_temp{int(TEMPERATURE*100):02d}_t{params['text_key']}")
                            
                        except Exception as e:
                            print(f"Error in trial {trial} with {model_name}: {str(e)}")
                            continue

class ClaudeExperimentRunner(BaseExperimentRunner):
    """Experiment runner for Claude models."""
    
    def get_model_type(self) -> str:
        return "claude"

    def __init__(self):
        """Initialize the Claude experiment runner."""
        super().__init__()
        self._setup_api()

    def _setup_api(self):
        """Set up the Claude API."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Missing ANTHROPIC_API_KEY environment variable")
        self.client = anthropic.Client(api_key=api_key)

    def run_experiment(self):
        """Run the experiment with Claude models."""
        for model_key, model_name in CLAUDE_MODELS.items():
            for persona_key, persona in PERSONAS.items():
                for text_key, text_name in TEXTS.items():
                    text_content = TEXT_CONTENT[text_key]
                    prompt = self.generate_prompt(persona, text_content)
                    
                    for trial in range(1, TRIALS + 1):
                        try:
                            response = self.client.messages.create(
                                model=model_name,
                                max_tokens=1000,
                                temperature=TEMPERATURE,
                                messages=[
                                    {"role": "user", "content": prompt}
                                ]
                            )
                            
                            params = {
                                "persona_key": persona_key,
                                "text_key": text_key,
                                "model_key": model_key,
                                "trial": trial,
                                "persona": persona,
                                "text_name": text_name,
                                "model": model_name
                            }
                            
                            self.save_result(response.content[0].text, params)
                            print(f"Completed: {params['persona_key']}_{params['model_key']}_n{trial:02d}_temp{int(TEMPERATURE*100):02d}_t{params['text_key']}")
                            
                        except Exception as e:
                            print(f"Error in trial {trial} with {model_name}: {str(e)}")
                            continue

def main():
    """Main entry point for the experiment."""
    try:
        # Run Grok experiment
        grok_runner = GrokExperimentRunner()
        grok_runner.run_experiment()

        # Run Gemini experiment
        gemini_runner = GeminiExperimentRunner()
        gemini_runner.run_experiment()
        
        # Run Claude experiment
        claude_runner = ClaudeExperimentRunner()
        claude_runner.run_experiment()
        
        print("Experiment completed successfully!")
    except Exception as e:
        print(f"Error running experiment: {str(e)}")

if __name__ == "__main__":
    main()
