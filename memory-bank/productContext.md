# Product Context

## Purpose

The purpose of this project is to evaluate how well different LLMs (Claude and Gemini) can understand and analyze Japanese literary texts. The project focuses specifically on emotional analysis, where models are asked to rate the strength of different emotions (面白さ、驚き、悲しみ、怒り) on a scale of 0-100.

## Key Features

- Multiple personas (大学１年生、文学研究者、感情豊かな詩人、無感情なロボット)
- Various literary texts (懐中時計、お金とピストル、ぼろぼろな駝鳥)
- Support for multiple LLM models and versions
- Systematic evaluation methodology

## User Experience

The project provides Python scripts for:
- Checking model availability (`*_check_model.py`)
- Running example analysis (`*_example.py`)
- Conducting full experiments (`gemini_main.py`)

Results are saved in model-specific directories (e.g., `results_gemini/`) with detailed metadata including:
- Timestamp
- Persona used
- Text analyzed
- Model version
- Trial number
- Temperature setting
