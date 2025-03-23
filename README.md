# LLM Literary Analysis

This research project evaluates the literary comprehension capabilities of various Large Language Models (LLMs). The project analyzes how well AI models can appreciate and interpret literary works.

## Project Overview

The project currently supports the following LLM models:

### Google Gemini
- Gemini 2.0: Pro Exp, Flash Thinking Exp, Flash
- Gemini 1.5: Pro, Flash
- Gemma 3.0: 27B IT

### Anthropic Claude
- Claude 3.7: Sonnet
- Claude 3.5: Sonnet, Haiku
- Claude 3.0: Sonnet, Haiku

Note: Claude-3-Opus model (claude-3-opus-20240229) is temporarily disabled due to high API costs (as of 2025/03/18).

### X.AI Grok
- Grok 2.0: Latest

### OpenAI
- Text Generation Models:
  - GPT-4: o, o-mini
- Reasoning Models:
  - O3: mini
  - O1: mini

### kluster.ai DeepSeek
- DeepSeek-R1
- DeepSeek-V3

### kluster.ai Meta Llama
- Llama 3.3: 70B Instruct Turbo
- Llama 3.1: 405B Instruct Turbo, 8B Instruct Turbo

## Features

### Core Features
- Systematic evaluation of LLM's literary analysis capabilities
- Support for multiple LLM models
- Unified prompt management across all models
- Standardized result format and aggregation

### Unified Prompt Management
- Centralized prompt definition and configuration
- Model-specific format adaptations
- Support for various model requirements:
  - Standard message format (OpenAI, Gemini, Grok)
  - Content format (Claude)
  - System role limitations (o1-mini)
  - Temperature handling (o3-mini)
- Easy extension for new models

### Analysis Features
- Emotional analysis across four dimensions:
  - Interest/Fun (面白さ)
  - Surprise (驚き)
  - Sadness (悲しみ)
  - Anger (怒り)
- Quantitative scoring (0-100) with detailed reasoning
- Automated result aggregation and analysis
- Comparative analysis across different models and personas

### Batch Processing
- Batch API Integration for cost reduction:
  - OpenAI (Ver.1 - Implemented):
    - JSONL processing with 50% cost reduction
    - Model-specific request formatting
    - Automatic error recovery
    - Support for all OpenAI models:
      - Standard models (gpt-4o, gpt-4o-mini)
      - Limited models (o3-mini: no temperature, o1-mini: no system role)
  - Claude: Message Batches API (Implemented)
    - バッチリクエストの生成と管理
    - 最大100,000リクエスト対応
    - 29日間の結果保持
    - エラーハンドリングとリカバリ
  - Gemini: Vertex AI Batch Prediction (Planned)
  - Groq: Batch API (Planned)
  - kluster.ai: Adaptive Batch Processing (Planned)

Features:
- Request Processing:
  - Model-specific request formatting
  - JSONL format for batch requests
  - Automatic parameter validation
  - Error prevention and recovery

- Execution Control:
  - 24-hour processing windows
  - Provider-optimized batch sizes
  - Status monitoring with backoff
  - Partial success handling

- Result Management:
  - JSONL format for batch results
  - Standard TXT format for individual results
  - Consistent metadata format
  - Error logging and tracking

- Error Handling:
  - Model-specific adaptations
  - Automatic retries with backoff
  - Partial result recovery
  - Detailed error logging

## Requirements

- Python 3.12
- google-generativeai>=0.3.0 (for Gemini models)
- anthropic>=0.43.0 (for Claude models)
- openai>=1.0.0 (for Grok and OpenAI models)
- python-dotenv>=1.0.0 (for environment variables)

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
export XAI_API_KEY="your_xai_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export KLUSTERAI_API_KEY="your_klusterai_api_key"  # Required for DeepSeek and Llama models
```

## Project Structure

```
llm-literary-analysis/
├── experiment_runner.py           # Unified experiment runner
├── check_models.py               # Model availability checker
├── parameters.py                 # Experiment parameters
├── aggregate_experiment_results.py # Result analysis tool
└── results/                      # Experiment results
    ├── gemini/                   # Gemini results
    ├── claude/                   # Claude results
    ├── grok/                     # Grok results
    ├── openai/                   # OpenAI results
    ├── deepseek/                 # DeepSeek results
    └── llama/                    # Llama results
```

## Usage

### Running Experiments

1. Run experiments with individual models:
```bash
python grok_example.py      # Run Grok experiments
python gemini_example.py    # Run Gemini experiments
python claude_example.py    # Run Claude experiments
python openai_example.py    # Run OpenAI experiments
python deepseek_example.py  # Run DeepSeek experiments
python llama_example.py     # Run Llama experiments
```

2. Run OpenAI experiments with batch processing (50% cost reduction):
```bash
python openai_example.py --batch                    # Run with batch processing
python openai_example.py --status <batch_id>        # Check batch job status
python openai_example.py --cancel <batch_id>        # Cancel ongoing batch job
```

3. Run experiments with all models:
```bash
python experiment_runner.py
```

4. Check model availability:
```bash
python check_models.py
```

### Processing Results

1. Aggregate results into CSV format:
```bash
python aggregate_experiment_results.py results/  # すべての結果を集計
python aggregate_experiment_results.py results/deepseek  # DeepSeekの結果のみを集計
```

The script will process all result files and generate a CSV file with:
- Metadata (timestamp, model, persona, etc.)
- Numerical evaluations (0-100 scores)
- Reasoning for each evaluation

### Results

#### Result Organization
The experiment results are organized by LLM type:
```
results/
├── gemini/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── claude/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── grok/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
├── openai/
│   └── p{persona}_{model}_n{trial}[_temp{temp}]_{text}.txt
├── deepseek/
│   └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
└── llama/
    └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt

Note: For OpenAI reasoning models (o3-mini, o1-mini), the temperature parameter is omitted from the filename as these models do not use temperature settings.
```

#### Result Files
Each result file includes:
```
timestamp: [YYYY-MM-DD HH:MM:SS]
persona: [Persona name]
model: [Model name]
trial: [Trial number]
temperature: [Temperature value]
text: [Text name]
Q1value: [0-100]
Q1reason: [Explanation for Interest/Fun]
Q2value: [0-100]
Q2reason: [Explanation for Surprise]
Q3value: [0-100]
Q3reason: [Explanation for Sadness]
Q4value: [0-100]
Q4reason: [Explanation for Anger]
```

#### Aggregated Results
The `aggregate_experiment_results.py` script processes all result files and generates model-specific CSV files:

```
aggregated_results/
├── aggregated_openai_[timestamp].csv     (48 results)
├── aggregated_claude_[timestamp].csv     (60 results)
├── aggregated_gemini_[timestamp].csv     (83 results)
├── aggregated_grok_[timestamp].csv       (12 results)
├── aggregated_deepseek_[timestamp].csv   (24 results)
└── aggregated_llama_[timestamp].csv      (36 results)
```

Each CSV file contains:
- Complete metadata (timestamp, model, persona, etc.)
- Numerical scores for all emotional dimensions
- Detailed reasoning for each score
- Error tracking and validation results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas of particular interest:
- Support for new LLM models
- Enhanced prompt management features
- Result analysis improvements
- Documentation translations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## For Developers

Development documentation is maintained locally in the `docs/` directory and is not included in the public repository for security and maintenance reasons. After cloning the repository, you can find API references and developer notes in:

- API Documentation: `docs/api/`
  - OpenAI API implementation details (batch processing, files, uploads)
  - Claude API integration guides (batch processing)
- Developer Notes: `docs/reference/`
  - Batch processing implementation guides
  - Best practices and known issues

Note: These documents are automatically excluded from Git to maintain separate development and production environments.
