"""Example script for running DeepSeek experiments."""

from experiment_runner import DeepSeekExperimentRunner

def main():
    """Run example analysis using DeepSeek."""
    try:
        # Create and run DeepSeek experiment
        runner = DeepSeekExperimentRunner()
        runner.run_experiment()
        print("DeepSeek example completed successfully!")
    except Exception as e:
        print(f"Error running DeepSeek example: {str(e)}")

if __name__ == "__main__":
    main()
