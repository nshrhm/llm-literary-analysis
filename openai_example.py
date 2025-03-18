"""Example script for running OpenAI experiments."""

import os
from experiment_runner import OpenAIExperimentRunner
from parameters import OPENAI_MODELS

def main():
    """Run example analysis using OpenAI."""
    try:
        # Check if API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set")
            return

        # Create and run OpenAI experiment
        print(f"Starting OpenAI experiment with {len(OPENAI_MODELS)} models...")
        runner = OpenAIExperimentRunner()
        runner.run_experiment()
        print("OpenAI experiment completed successfully!")
    except Exception as e:
        print(f"Error running OpenAI experiment: {str(e)}")

if __name__ == "__main__":
    main()
