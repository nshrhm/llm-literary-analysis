# Active Context

## Current Focus

The project is currently focused on:
- Integrating Claude models into the experiment framework
- Running unified experiments through `experiment_runner.py`
- Managing results in a structured directory system for both LLMs
- Evaluating emotional analysis capabilities across different models, personas, and texts

## Recent Changes

- Refactored codebase to use a unified experiment runner:
  - Created `BaseExperimentRunner` with common functionality
  - Implemented `GeminiExperimentRunner` and `ClaudeExperimentRunner`
  - Updated model definitions in `parameters.py`
- Reorganized result directory structure:
  - Unified format: `results/{llm}/p{persona}_{model}_n{trial}_temp{temp}_t{text}.txt`
  - Separate directories for Gemini and Claude results
- Integrated model checking functionality in `check_models.py`
- Updated documentation to reflect new architecture and file organization

## Next Steps

- Run complete experiments with both Gemini and Claude models
- Compare emotional analysis results across different LLMs
- Analyze performance patterns between model versions
- Document insights from cross-model comparisons
- Consider implementing additional analysis tools for result comparison
