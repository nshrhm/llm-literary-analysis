# LLM Literary Analysis

This research project evaluates the literary comprehension capabilities of various Large Language Models (LLMs). The project analyzes how well AI models can appreciate and interpret literary works.

## Project Overview

The project currently supports the following LLM models:
- Google Gemini
- Anthropic Claude
- (Future planned support for OpenAI, GitHub Copilot, Deepseek, Grok)

## Features

- Systematic evaluation of LLM's literary analysis capabilities
- Support for multiple LLM models
- Emotional analysis across four dimensions:
  - Interest/Fun (面白さ)
  - Surprise (驚き)
  - Sadness (悲しみ)
  - Anger (怒り)
- Quantitative scoring (0-100) with detailed reasoning
- Automated result aggregation and analysis
- Comparative analysis across different models and personas

## Requirements

- Python 3.12
- google-generativeai (for Gemini models)
- anthropic (for Claude models)
- (Additional requirements will be added as more models are supported)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/nshrhm/llm-literary-analysis.git
cd llm-literary-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
```

## Project Structure

```
llm-literary-analysis/
├── gemini_*.py                    # Gemini model implementations
├── claude_*.py                    # Claude model implementations
├── parameters.py                  # Experiment parameters
├── aggregate_experiment_results.py # Result analysis tool
├── output/                        # Current experiment results
└── results/                       # Versioned experiment results
```

## Usage

### Running Experiments

1. Run experiments with Gemini models:
```bash
python gemini_main.py
```

2. Check model availability:
```bash
python gemini_check_model.py
python claude_check_model.py
```

### Processing Results

1. Aggregate results into CSV format:
```bash
python aggregate_experiment_results.py output/
```

The script will process all result files and generate a CSV file with:
- Metadata (timestamp, model, persona, etc.)
- Numerical evaluations (0-100 scores)
- Reasoning for each evaluation

### Result Format

Each evaluation includes:
```
Q1. 面白さ(数値): [0-100]
Q1. 面白さ(理由): [explanation]
Q2. 驚き(数値): [0-100]
Q2. 驚き(理由): [explanation]
...
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
