"""Main program for running the literature analysis experiment with Gemini."""

import os
import datetime
import google.generativeai as genai
from parameters import *

class ExperimentRunner:
    def __init__(self):
        """Initialize the experiment runner."""
        self._setup_api()
        os.makedirs("results_gemini", exist_ok=True)

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
        return f"""あなたは {persona} です。以下の文章を読んで得られた感情の強さを0から100の間の整数で答えてください。0はその感情が全くない状態、100はその感情が最も強い状態を表します。

{text_content}

Q1. 面白さ:
Q2. 驚き:
Q3. 悲しみ:
Q4. 怒り:"""

    def save_result(self, result: str, params: dict):
        """Save the experiment result to a file.
        
        Args:
            result: The response from the model
            params: Dictionary containing experiment parameters
        """
        filename = f"{params['persona_key']}_{params['text_key']}_{params['model_key']}_n{params['trial']:02d}_temp{int(TEMPERATURE*100):02d}.txt"
        filepath = os.path.join("results_gemini", filename)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""timestamp: {timestamp}
persona: {params['persona']}
text: {params['text_name']}
model: {params['model']}
trial: {params['trial']}
temperature: {TEMPERATURE}
response:
{result}
"""
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
