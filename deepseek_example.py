"""Example script for running DeepSeek experiments."""

import os
import argparse
from experiment_runner import DeepSeekExperimentRunner
from parameters import DEEPSEEK_MODELS

def main():
    """Run example analysis using DeepSeek."""
    parser = argparse.ArgumentParser(description="Run DeepSeek experiments")
    parser.add_argument("--model", nargs="+", 
                       choices=list(DEEPSEEK_MODELS.keys()),
                       help="Specify one or more models to run")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("KLUSTERAI_API_KEY"):
            print("Error: KLUSTERAI_API_KEY environment variable is not set")
            return

        # Create and run DeepSeek experiment
        if args.model:
            # 複数モデルの実行
            models = {model: DEEPSEEK_MODELS[model] for model in args.model}
            print(f"Starting DeepSeek experiment with models: {', '.join(args.model)}")
        else:
            # 全モデルの実行
            models = DEEPSEEK_MODELS
            print(f"Starting DeepSeek experiment with {len(DEEPSEEK_MODELS)} models...")

        runner = DeepSeekExperimentRunner()
        runner.run_experiment()
        print("DeepSeek experiment completed successfully!")
    except Exception as e:
        print(f"Error running DeepSeek experiment: {str(e)}")

if __name__ == "__main__":
    main()
