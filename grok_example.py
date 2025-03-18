"""Example script for running Grok experiments."""

from experiment_runner import GrokExperimentRunner

def main():
    """Run example analysis using Grok."""
    try:
        # Create and run Grok experiment
        runner = GrokExperimentRunner()
        runner.run_experiment()
        print("Grok example completed successfully!")
    except Exception as e:
        print(f"Error running Grok example: {str(e)}")

if __name__ == "__main__":
    main()
