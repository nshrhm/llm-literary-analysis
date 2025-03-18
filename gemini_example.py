"""Example script for running Gemini experiments."""

import os
from experiment_runner import GeminiExperimentRunner
from parameters import GEMINI_MODELS

def main():
    """Run example analysis using Gemini."""
    try:
        # Check if API key is set
        if not os.environ.get("GEMINI_API_KEY"):
            print("Error: GEMINI_API_KEY environment variable is not set")
            return
            
        # Create and run Gemini experiment
        print(f"Starting Gemini experiment with {len(GEMINI_MODELS)} models...")
        runner = GeminiExperimentRunner()
        runner.run_experiment()
        print("Gemini experiment completed successfully!")
    except Exception as e:
        print(f"Error running Gemini experiment: {str(e)}")

if __name__ == "__main__":
    main()
