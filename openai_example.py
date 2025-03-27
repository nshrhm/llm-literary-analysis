"""Example script for running OpenAI experiments with batch processing support."""

import os
import argparse
from datetime import datetime
from experiment_runner import OpenAIExperimentRunner
from openai_batch_runner import OpenAIBatchRunner
from parameters import OPENAI_MODELS

def main():
    """Run example analysis using OpenAI."""
    parser = argparse.ArgumentParser(description="Run OpenAI experiments")
    parser.add_argument("--batch", action="store_true", help="Use batch processing (50% cost reduction)")
    parser.add_argument("--cancel", help="Cancel a batch job with the specified batch ID")
    parser.add_argument("--status", help="Check status of a batch job with the specified batch ID")
    parser.add_argument("--model", choices=list(OPENAI_MODELS.keys()), help="Specify a single model to run")
    args = parser.parse_args()

    try:
        # Check if API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set")
            return

        # Check batch status
        if args.status:
            try:
                runner = OpenAIBatchRunner()
                status = runner.client.batches.retrieve(args.status)
                print(f"\nBatch {args.status} status:")
                print(f"- Status: {status.status}")
                print(f"- Total requests: {status.request_counts.total}")
                print(f"- Completed: {status.request_counts.completed}")
                print(f"- Failed: {status.request_counts.failed}")
                
                # If completed, save results
                if status.status == "completed":
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    runner._save_results(status, timestamp)
                elif status.errors:
                    print("\nBatch errors:")
                    for error in status.errors.data:
                        print(f"- {error.message}")
                return
            except Exception as e:
                print(f"Error checking batch status: {str(e)}")
                return

        # Cancel batch job
        if args.cancel:
            try:
                runner = OpenAIBatchRunner()
                runner.client.batches.cancel(args.cancel)
                print(f"Successfully cancelled batch job: {args.cancel}")
                return
            except Exception as e:
                print(f"Error cancelling batch job: {str(e)}")
                return

        # Create and run OpenAI experiment
        if args.model:
            # 単一モデルの実行
            models = {args.model: OPENAI_MODELS[args.model]}
            print(f"Starting OpenAI experiment with model: {args.model}")
        else:
            # 全モデルの実行
            models = OPENAI_MODELS
            print(f"Starting OpenAI experiment with {len(OPENAI_MODELS)} models...")
        
        if args.batch:
            print("Using batch processing (50% cost reduction enabled)...")
            runner = OpenAIBatchRunner()
            runner.run_batch_experiment(models)
        else:
            print("Using standard processing (consider using --batch for 50% cost reduction)...")
            runner = OpenAIExperimentRunner()
            runner.run_experiment()
            
        print("OpenAI experiment completed successfully!")
    except Exception as e:
        print(f"Error running OpenAI experiment: {str(e)}")

if __name__ == "__main__":
    main()
