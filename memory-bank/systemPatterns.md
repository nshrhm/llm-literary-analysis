# System Patterns

## Architecture

The project follows a modular architecture, with separate scripts for interacting with each LLM (Claude and Gemini). The `parameters.py` file manages shared configurations.

## Design Patterns

- **Strategy Pattern:** Used to switch between different LLM models (Claude and Gemini).
- **Factory Pattern:** Used to create different LLM clients based on the model name.

## Component Relationships

```mermaid
flowchart LR
    subgraph LLM Interaction
        parameters.py --> claude_*.py
        parameters.py --> gemini_*.py
        claude_*.py --> Claude API
        gemini_*.py --> Gemini API
    end
