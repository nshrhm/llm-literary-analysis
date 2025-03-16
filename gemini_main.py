"""Main program for running the literature analysis experiment with Gemini."""

import os
import re
import datetime
import google.generativeai as genai
from parameters import *

# Directory for storing experiment results
RESULTS_DIR = "results_gemini"

class ExperimentRunner:
    def __init__(self):
        """Initialize the experiment runner."""
        self._setup_api()
        os.makedirs(RESULTS_DIR, exist_ok=True)

    def _setup_api(self):
        """Set up the Gemini API."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable")
        genai.configure(api_key=api_key)

    def generate_prompt(self, persona: str, text_content: str) -> str:
        """Generate the prompt for the experiment.
        
        Args:
            persona: The persona to use for the analysis
            text_content: The text content to analyze
        
        Returns:
            str: The generated prompt
        """
        return f"""あなたは {persona} です。以下の文章を読んで得られた感情の強さを0から100の間の整数で答えてください。0はその感情が全くない状態、100はその感情が最も強い状態を表します。各感情について、値と理由を答えてください。

{text_content}

面白さ: (値) (理由)
驚き: (値) (理由)
悲しみ: (値) (理由)
怒り: (値) (理由)"""

    def extract_value(self, text: str, question: str) -> str:
        """Extract the value from the response text.
        
        Args:
            text: The response text
            question: The question to extract the value for (面白さ, 驚き, etc.)
        
        Returns:
            str: The extracted value
        """
        patterns = [
            rf"{question}:\s*\(値\)\s*(\d+)",  # (値) パターン
            rf"{question}:\s*(\d+)\s*\(",      # 数字が先のパターン
            rf"{question}:\s*\((\d+)\)",       # 括弧付き数字のパターン
            rf"{question}:\s*(\d+)",           # 単純な数字のパターン
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
            rf"{question}:.*?\(理由[:：]?\)\s*(.+?)(?=(?:\n[^\n]|$))",  # (理由) パターン
            rf"{question}:.*?\(.*?\)\s*(.+?)(?=(?:\n[^\n]|$))",         # 一般的な括弧パターン
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
        filename = f"{params['persona_key']}_{params['text_key']}_{params['model_key']}_n{params['trial']:02d}_temp{int(TEMPERATURE*100):02d}.txt"
        filepath = os.path.join(RESULTS_DIR, filename)
        
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
        """Run the complete experiment across all combinations."""
        for model_key, model_name in MODELS.items():
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
                            print(f"Completed: {params['persona_key']}_{params['text_key']}_{params['model_key']}_n{trial:02d}")
                            
                        except Exception as e:
                            print(f"Error in trial {trial} with {model_name}: {str(e)}")
                            continue

def main():
    """Main entry point for the experiment."""
    try:
        runner = ExperimentRunner()
        runner.run_experiment()
        print("Experiment completed successfully!")
    except Exception as e:
        print(f"Error running experiment: {str(e)}")

if __name__ == "__main__":
    main()
