"""Example script for running OpenAI experiments with batch processing support."""

import os
import argparse
from experiment_runner import OpenAIExperimentRunner
from openai_batch_runner import OpenAIBatchRunner
from parameters import OPENAI_MODELS

def main():
    """Run example analysis using OpenAI."""
    parser = argparse.ArgumentParser(description="Run OpenAI experiments")
    parser.add_argument("--batch", action="store_true", help="Use batch processing (50% cost reduction)")
    parser.add_argument("--cancel", help="Cancel a batch job with the specified batch ID")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set")
            return

        # バッチジョブのキャンセル
        if args.cancel:
            try:
                from openai import OpenAI
                client = OpenAI()
                client.batches.cancel(args.cancel)
                print(f"Successfully cancelled batch job: {args.cancel}")
                return
            except Exception as e:
                print(f"Error cancelling batch job: {str(e)}")
                return

        # Create and run OpenAI experiment
        print(f"Starting OpenAI experiment with {len(OPENAI_MODELS)} models...")
        
        if args.batch:
            print("Using batch processing (50% cost reduction enabled)...")
            runner = OpenAIBatchRunner()
            runner.run_batch_experiment()
        else:
            print("Using standard processing (consider using --batch for 50% cost reduction)...")
            runner = OpenAIExperimentRunner()
            runner.run_experiment()
            
        print("OpenAI experiment completed successfully!")
    except Exception as e:
        print(f"Error running OpenAI experiment: {str(e)}")

if __name__ == "__main__":
    main()
