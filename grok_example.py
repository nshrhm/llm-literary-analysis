"""Example script for running Grok experiments."""

import os
import argparse
from experiment_runner import GrokExperimentRunner
from parameters import GROK_MODELS

def main():
    """Run example analysis using Grok."""
    parser = argparse.ArgumentParser(description="Run Grok experiments")
    parser.add_argument("--model", nargs="+", 
                       choices=list(GROK_MODELS.keys()),
                       help="Specify one or more models to run")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("XAI_API_KEY"):
            print("Error: XAI_API_KEY environment variable is not set")
            return

        # Create and run Grok experiment
        if args.model:
            # 複数モデルの実行
            models = {model: GROK_MODELS[model] for model in args.model}
            print(f"Starting Grok experiment with models: {', '.join(args.model)}")
        else:
            # 全モデルの実行
            models = GROK_MODELS
            print(f"Starting Grok experiment with {len(GROK_MODELS)} models...")

        runner = GrokExperimentRunner()
        runner.run_experiment()
        print("Grok experiment completed successfully!")
    except Exception as e:
        print(f"Error running Grok experiment: {str(e)}")

if __name__ == "__main__":
    main()
