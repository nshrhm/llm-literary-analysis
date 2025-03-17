"""Script to check available models for both Gemini and Claude."""

import os
import google.generativeai as genai
import anthropic
from parameters import GEMINI_MODELS, CLAUDE_MODELS

def check_gemini_models():
    """Check available Gemini models."""
    print("\n=== Gemini Models ===")
    
    # Configure the API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return
    
    genai.configure(api_key=api_key)
    
    # List all models that can generate content
    print("\nConfigured models:")
    for short_name, model_name in GEMINI_MODELS.items():
        print(f"- {short_name}: {model_name}")
    
    print("\nAvailable models and capabilities:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}: {m.description}")

def check_claude_models():
    """Check available Claude models."""
    print("\n=== Claude Models ===")
    
    # Configure the API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        return
    
    client = anthropic.Client(api_key=api_key)
    
    # List configured models
    for short_name, model_name in CLAUDE_MODELS.items():
        try:
            # Try to create a simple message to test model availability
            client.messages.create(
                model=model_name,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "test"}
                ]
            )
            status = "✓ Available"
        except Exception as e:
            status = f"✗ Not Available ({str(e)})"
        
        print(f"{short_name} ({model_name}): {status}")

def main():
    """Main function to check models."""
    try:
        check_gemini_models()
        check_claude_models()
    except Exception as e:
        print(f"Error checking models: {str(e)}")

if __name__ == "__main__":
    main()
