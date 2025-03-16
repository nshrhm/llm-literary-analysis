# Tech Context

## Technologies

- **Programming Language:** Python 3.12
- **LLMs:** 
  - Claude (claude-3-opus-20240229, claude-3-sonnet-20240229)
  - Gemini (gemini-2.0-pro-exp, gemini-1.5-pro-latest, etc.)
- **Libraries:** 
  - `google-generativeai>=0.3.0` (Google Gemini API client)
  - `anthropic>=0.43.0` (Anthropic Claude API client)
  - `python-dotenv>=1.0.0` (Environment variable management)

## Development Setup

- The project is set up as a Python project.
- Dependencies are installed using `pip install -r requirements.txt`.
- Required environment variables:
  - `GEMINI_API_KEY`: API key for accessing Gemini models
  - `ANTHROPIC_API_KEY`: API key for accessing Claude models

## Technical Constraints

- The project may be limited by the capabilities and limitations of the chosen LLMs (Claude and Gemini).
- API rate limits and costs may be a constraint.
