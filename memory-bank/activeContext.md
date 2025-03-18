# Active Context

## Current Focus

The project is currently focused on:
- Running unified experiments through `experiment_runner.py`
- Managing results in a structured directory system for all LLMs
- Evaluating emotional analysis capabilities across different models, personas, and texts
- Integrating and comparing results from Gemini, Claude, and Grok models

## Recent Changes

- Refactored codebase to use a unified experiment runner:
  - Created `BaseExperimentRunner` with common functionality
  - Implemented `GeminiExperimentRunner`, `ClaudeExperimentRunner`, and `GrokExperimentRunner`
  - Updated model definitions in `parameters.py` to include all LLMs
- Reorganized result directory structure:
  - Unified format: `results/{llm}/p{persona}_{model}_n{trial}_temp{temp}_t{text}.txt`
  - Separate directories for Gemini and Claude results
- Integrated model checking functionality in `check_models.py`
- Updated documentation to reflect new architecture and file organization

## Next Steps

- Run complete experiments with all models (Gemini, Claude, and Grok)
- Compare emotional analysis results across different LLMs
- Analyze performance patterns between model versions and providers
- Document insights from cross-model comparisons
- Implement additional analysis tools for three-way model comparison
