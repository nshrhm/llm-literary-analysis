"""Example script for running Llama experiments."""

from experiment_runner import LlamaExperimentRunner

def main():
    """Run example analysis using Llama."""
    try:
        # Create and run Llama experiment
        runner = LlamaExperimentRunner()
        runner.run_experiment()
        print("Llama example completed successfully!")
    except Exception as e:
        print(f"Error running Llama example: {str(e)}")

if __name__ == "__main__":
    main()
