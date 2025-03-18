"""Example script for running Claude experiments."""

import os
from experiment_runner import ClaudeExperimentRunner
from parameters import CLAUDE_MODELS

def main():
    """Run example analysis using Claude."""
    try:
        # Check if API key is set
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("Error: ANTHROPIC_API_KEY environment variable is not set")
            return
            
        # Create and run Claude experiment
        print(f"Starting Claude experiment with {len(CLAUDE_MODELS)} models...")
        runner = ClaudeExperimentRunner()
        runner.run_experiment()
        print("Claude experiment completed successfully!")
    except Exception as e:
        print(f"Error running Claude experiment: {str(e)}")

if __name__ == "__main__":
    main()
