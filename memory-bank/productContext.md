# Product Context

## Purpose

The purpose of this project is to evaluate how well different LLMs (Claude, Gemini, Grok, and OpenAI) can understand and analyze Japanese literary texts. The project focuses specifically on emotional analysis, where models are asked to rate the strength of different emotions (面白さ、驚き、悲しみ、怒り) on a scale of 0-100. By comparing various LLMs, including specialized reasoning models, we can better understand their literary comprehension capabilities.

## Key Features

- Multiple personas (大学１年生、文学研究者、感情豊かな詩人、無感情なロボット)
- Various literary texts (懐中時計、お金とピストル、ぼろぼろな駝鳥)
- Support for multiple LLM models and versions:
  - Gemini (2.0/1.5シリーズ、Gemma)
  - Claude (3.7/3.5/3.0シリーズ)
  - Grok (2.0シリーズ)
  - OpenAI (text-generation/reasoningモデル)
- Systematic evaluation methodology
- Unified experiment runner architecture
- Model-specific temperature handling

## User Experience

The project provides Python scripts for:
- Checking model availability (`check_models.py`)
- Running example analysis (`*_example.py`)
- Conducting full experiments (`experiment_runner.py`)
- Aggregating and analyzing results (`aggregate_experiment_results.py`)

Results are saved in model-specific directories (e.g., `results/gemini/`) with detailed metadata including:
- Timestamp
- Persona used
- Text analyzed
- Model version
- Trial number
- Temperature setting
