"""Example script for running Gemini experiments."""

import os
import argparse
from experiment_runner import GeminiExperimentRunner
from parameters import GEMINI_MODELS

def main():
    """Run example analysis using Gemini."""
    parser = argparse.ArgumentParser(description="Run Gemini experiments")
    parser.add_argument("--model", nargs="+", 
                       choices=list(GEMINI_MODELS.keys()),
                       help="Specify one or more models to run")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("GEMINI_API_KEY"):
            print("Error: GEMINI_API_KEY environment variable is not set")
            return
            
        # Create and run Gemini experiment
        if args.model:
            # 複数モデルの実行
            models = {model: GEMINI_MODELS[model] for model in args.model}
            print(f"Starting Gemini experiment with models: {', '.join(args.model)}")
        else:
            # 全モデルの実行
            models = GEMINI_MODELS
            print(f"Starting Gemini experiment with {len(GEMINI_MODELS)} models...")

        runner = GeminiExperimentRunner()
        runner.run_experiment()
        print("Gemini experiment completed successfully!")
    except Exception as e:
        print(f"Error running Gemini experiment: {str(e)}")

if __name__ == "__main__":
    main()
