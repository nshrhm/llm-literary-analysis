"""Example script for running Qwen experiments."""

import os
import argparse
from experiment_runner import QwenExperimentRunner
from parameters import QWEN_MODELS

def main():
    """Run example analysis using Qwen."""
    parser = argparse.ArgumentParser(description="Run Qwen experiments")
    parser.add_argument("--model", nargs="+", 
                       choices=list(QWEN_MODELS.keys()),
                       help="Specify one or more models to run")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("KLUSTERAI_API_KEY"):
            print("Error: KLUSTERAI_API_KEY environment variable is not set")
            return

        # Create and run Qwen experiment
        if args.model:
            # 複数モデルの実行
            models = {model: QWEN_MODELS[model] for model in args.model}
            print(f"Starting Qwen experiment with models: {', '.join(args.model)}")
        else:
            # 全モデルの実行
            models = QWEN_MODELS
            print(f"Starting Qwen experiment with {len(QWEN_MODELS)} models...")

        runner = QwenExperimentRunner()
        runner.run_experiment()
        print("Qwen experiment completed successfully!")
    except Exception as e:
        print(f"Error running Qwen experiment: {str(e)}")

if __name__ == "__main__":
    main()
