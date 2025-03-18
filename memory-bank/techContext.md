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
- **Libraries:** 
  - `google-generativeai>=0.3.0` (Google Gemini API client)
  - `anthropic>=0.43.0` (Anthropic Claude API client)
  - `openai>=1.0.0` (X.AI Grok API client)
  - `python-dotenv>=1.0.0` (Environment variable management)

## Development Setup

- The project is set up as a Python project.
- Dependencies are installed using `pip install -r requirements.txt`.
- Required environment variables:
  - `GEMINI_API_KEY`: API key for accessing Gemini models
  - `ANTHROPIC_API_KEY`: API key for accessing Claude models
  - `XAI_API_KEY`: API key for accessing Grok models (from console.x.ai)

## Technical Constraints

- The project may be limited by the capabilities and limitations of the chosen LLMs (Claude and Gemini).
- API rate limits and costs may be a constraint.
