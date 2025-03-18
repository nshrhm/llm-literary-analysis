# Tech Context

## Technologies

- **Programming Language:** Python 3.12
- **LLMs:** 
  - Claude:
    - Claude 3.7: claude-3-7-sonnet-20250219
    - Claude 3.5: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022
    - Claude 3.0: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
  - Gemini:
    - Gemini 2.0: gemini-2.0-pro-exp, gemini-2.0-flash-thinking-exp, etc.
    - Gemini 1.5: gemini-1.5-pro-latest, gemini-1.5-flash-8b-latest
    - Gemma: gemma-3-27b-it
  - Grok:
    - Grok 2.0: grok-2-latest
  - OpenAI:
    - Text Generation: gpt-4o, gpt-4o-mini
    - Reasoning: o3-mini, o1-mini
- **Libraries:** 
  - `google-generativeai>=0.3.0` (Google Gemini API client)
  - `anthropic>=0.43.0` (Anthropic Claude API client)
  - `openai>=1.0.0` (OpenAI & X.AI Grok API client)
  - `python-dotenv>=1.0.0` (Environment variable management)

## Model Characteristics

### Temperature Support
- Standard Models (Gemini, Claude, standard OpenAI):
  - Uses temperature parameter (0.0-1.0)
  - Default: 0.5
- OpenAI Reasoning Models:
  - No temperature parameter
  - Optimized for consistent logical analysis

### API Endpoints
- Gemini: api.gemini.google.com
- Claude: api.anthropic.com
- Grok: api.x.ai
- OpenAI: api.openai.com

## Development Setup

- The project is set up as a Python project.
- Dependencies are installed using `pip install -r requirements.txt`.
- Required environment variables:
  - `GEMINI_API_KEY`: API key for accessing Gemini models
  - `ANTHROPIC_API_KEY`: API key for accessing Claude models
  - `XAI_API_KEY`: API key for accessing Grok models (from console.x.ai)
  - `OPENAI_API_KEY`: API key for accessing OpenAI models

## Technical Constraints

- Model Specific Limitations:
  - Temperature handling varies by model type
  - Response format consistency varies between providers
  - API rate limits differ by provider
- Cost Considerations:
  - Each provider has different pricing models
  - Usage tracking needed for each API separately
- Implementation Challenges:
  - Handling different API response formats
  - Managing model-specific error cases
  - Supporting provider-specific features
