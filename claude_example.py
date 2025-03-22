"""Example script for running Claude experiments."""

import os
import argparse
from experiment_runner import ClaudeExperimentRunner
from claude_batch_runner import ClaudeBatchRunner
from parameters import CLAUDE_MODELS
from anthropic import Anthropic

def check_batch_status(batch_id):
    """Check status of a batch job."""
    try:
        client = Anthropic()
        status = client.messages.batches.retrieve(batch_id)
        print(f"Batch {batch_id} status:")
        print(f"- Status: {status.processing_status}")
        print(f"- Total requests: {status.request_counts.processing + status.request_counts.succeeded + status.request_counts.errored}")
        print(f"- Completed: {status.request_counts.succeeded}")
        print(f"- Failed: {status.request_counts.errored}")
        
        if status.processing_status == "ended" and status.results_url:
            # Process and save results if completed
            timestamp = status.created_at.strftime("%Y%m%d_%H%M%S")
            runner = ClaudeBatchRunner()
            runner._save_results(status, timestamp, "unknown")  # Model ID unknown in status check
            print("Results saved to: results/claude/")
            
    except Exception as e:
        print(f"Error checking batch status: {str(e)}")

def cancel_batch(batch_id):
    """Cancel a running batch job."""
    try:
        client = Anthropic()
        client.messages.batches.cancel(batch_id)
        print(f"Cancelled batch job: {batch_id}")
    except Exception as e:
        print(f"Error cancelling batch: {str(e)}")

def main():
    """Run example analysis using Claude."""
    parser = argparse.ArgumentParser(description="Run Claude experiments")
    parser.add_argument("--batch", action="store_true", help="Use batch processing")
    parser.add_argument("--status", help="Check status of batch job")
    parser.add_argument("--cancel", help="Cancel batch job")
    args = parser.parse_args()
    
    try:
        # Check if API key is set
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("Error: ANTHROPIC_API_KEY environment variable is not set")
            return
        
        if args.status:
            check_batch_status(args.status)
        elif args.cancel:
            cancel_batch(args.cancel)
        else:
            # Create and run Claude experiment
            print(f"Starting Claude experiment with {len(CLAUDE_MODELS)} models...")
            
            if args.batch:
                print("Using batch processing (50% cost reduction enabled)...")
                runner = ClaudeBatchRunner()
                runner.run_batch_experiment()
            else:
                runner = ClaudeExperimentRunner()
                runner.run_experiment()
                
            print("Claude experiment completed successfully!")
            
    except Exception as e:
        print(f"Error running Claude experiment: {str(e)}")

if __name__ == "__main__":
    main()
