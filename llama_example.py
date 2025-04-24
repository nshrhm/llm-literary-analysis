"""Example script for running Llama experiments."""

import os
import argparse
from experiment_runner import LlamaExperimentRunner
from parameters import LLAMA_MODELS

def main():
    """Run example analysis using Llama."""
    parser = argparse.ArgumentParser(description="Run Llama experiments")
    parser.add_argument("--model", nargs="+", 
                       choices=list(LLAMA_MODELS.keys()),
                       help="Specify one or more models to run")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("KLUSTERAI_API_KEY"):
            print("Error: KLUSTERAI_API_KEY environment variable is not set")
            return

        # Create and run Llama experiment
        if args.model:
            # 複数モデルの実行
            models = {model: LLAMA_MODELS[model] for model in args.model}
            print(f"Starting Llama experiment with models: {', '.join(args.model)}")
        else:
            # 全モデルの実行
            models = LLAMA_MODELS
            print(f"Starting Llama experiment with {len(LLAMA_MODELS)} models...")

        runner = LlamaExperimentRunner()
        runner.run_experiment()
        print("Llama experiment completed successfully!")
    except Exception as e:
        print(f"Error running Llama experiment: {str(e)}")

if __name__ == "__main__":
    main()
