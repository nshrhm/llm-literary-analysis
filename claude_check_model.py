import os
import anthropic
from typing import Dict, List, Tuple

def check_model_availability(client: anthropic.Client, model: str) -> Tuple[bool, str]:
    """
    Check if a model is available by attempting to create a simple message.
    
    Args:
        client: Anthropic API client
        model: Model name to check
    
    Returns:
        Tuple[bool, str]: (is_available, status_message)
    """
    try:
        # Simple test message
        client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        return True, "Available"
    except anthropic.APIError as e:
        if "model not found" in str(e).lower():
            return False, "Model not found"
        else:
            return False, f"Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def list_claude_models():
    """Lists and checks availability of Claude models."""
    # Configure the API key
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        return

    # Create an Anthropic client
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

    # List of models to check (from newest to oldest)
    models = [
        "claude-3-7-sonnet-20250219",  # New model
        "claude-3-5-sonnet-20241022",  # New model
        "claude-3-5-haiku-20241022",   # New model
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "claude-3-opus-20240229",
    ]

    print("\nChecking Claude models availability...")
    print("-" * 50)
    print(f"{'Model':<40} {'Status':<20}")
    print("-" * 50)

    for model in models:
        is_available, status = check_model_availability(client, model)
        status_display = "✓ " + status if is_available else "✗ " + status
        print(f"{model:<40} {status_display:<20}")

if __name__ == "__main__":
    list_claude_models()
