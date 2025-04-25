"""Script to check available models for Gemini, Claude, Grok, DeepSeek, and OpenAI."""

import os
import google.generativeai as genai
import anthropic
import requests
from openai import OpenAI
from parameters import (
    GEMINI_MODELS, CLAUDE_MODELS, GROK_MODELS,
    OPENAI_MODELS, DEEPSEEK_MODELS, LLAMA_MODELS
)

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

def check_grok_models():
    """Check available Grok models."""
    print("\n=== Grok Models ===")
    
    # Configure the API key
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("Error: XAI_API_KEY environment variable not set.")
        return
    
    # List configured models
    print("\nConfigured models:")
    for short_name, model_name in GROK_MODELS.items():
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        try:
            # Simple test request to check model availability
            response = requests.get(
                "https://api.x.ai/v1/models",
                headers=headers
            )
            if response.status_code == 200:
                status = "✓ Available"
            else:
                status = f"✗ Not Available (HTTP {response.status_code})"
        except Exception as e:
            status = f"✗ Not Available ({str(e)})"
            
        print(f"- {short_name}: {model_name} - {status}")

def check_openai_models():
    """Check available OpenAI models."""
    print("\n=== OpenAI Models ===")
    
    # Configure the API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("\nConfigured models:")
    for short_name, model_info in OPENAI_MODELS.items():
        try:
            # Test model availability using the endpoint
            response = requests.get(
                model_info["endpoint"].replace("/completions", ""),
                headers=headers
            )
            if response.status_code == 200:
                status = "✓ Available"
            else:
                status = f"✗ Not Available (HTTP {response.status_code})"
        except Exception as e:
            status = f"✗ Not Available ({str(e)})"
            
        print(f"- {short_name} ({model_info['model_name']}) - Type: {model_info['type']} - {status}")

def check_deepseek_models():
    """Check available DeepSeek models."""
    print("\n=== DeepSeek Models ===")
    
    # Configure the API key
    api_key = os.environ.get("KLUSTERAI_API_KEY")
    if not api_key:
        print("Error: KLUSTERAI_API_KEY environment variable not set.")
        return
    
    # Prepare OpenAI client for kluster.ai
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.kluster.ai/v1"
    )
    
    # List configured models
    print("\nConfigured models:")
    for short_name, model_name in DEEPSEEK_MODELS.items():
        try:
            # Test model availability
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            status = "✓ Available"
        except Exception as e:
            status = f"✗ Not Available ({str(e)})"
        
        print(f"- {short_name}: {model_name} - {status}")

def check_llama_models():
    """Check available Llama models."""
    print("\n=== Llama Models ===")
    
    # Configure the API key
    api_key = os.environ.get("KLUSTERAI_API_KEY")
    if not api_key:
        print("Error: KLUSTERAI_API_KEY environment variable not set.")
        return
    
    # Prepare OpenAI client for kluster.ai
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.kluster.ai/v1"
    )
    
    # List configured models
    print("\nConfigured models:")
    for short_name, model_name in LLAMA_MODELS.items():
        try:
            # Test model availability
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            status = "✓ Available"
        except Exception as e:
            status = f"✗ Not Available ({str(e)})"
        
        print(f"- {short_name}: {model_name} - {status}")

def main():
    """Main function to check models."""
    try:
        check_gemini_models()
        check_claude_models()
        check_grok_models()
        check_openai_models()
        check_deepseek_models()
        check_llama_models()
    except Exception as e:
        print(f"Error checking models: {str(e)}")

if __name__ == "__main__":
    main()
