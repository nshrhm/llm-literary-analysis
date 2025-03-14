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
- Detailed performance metrics and analysis
- Comparative analysis across different models

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
├── gemini_*.py        # Gemini model implementations
├── claude_*.py        # Claude model implementations
├── results_gemini/    # Test results for Gemini models
└── [Additional directories will be added for other models]
```

## Usage

Documentation for usage and example commands will be added soon.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
