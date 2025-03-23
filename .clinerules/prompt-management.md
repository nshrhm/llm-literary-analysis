# Prompt Management Guide

## Design Patterns

### 1. Centralized Prompt Definition

```python
# parameters.py
BASE_PROMPT = """..."""
SYSTEM_PROMPTS = {...}
MODEL_CONFIGS = {...}
```

Benefits:
- Single source of truth for prompts
- Easy maintenance and updates
- Consistent formatting across models

### 2. Model-Specific Adaptations

```python
# prompt_manager.py
class PromptManager:
    @staticmethod
    def get_prompt(model_type, persona_id, text_content, model_id=None):
        base = _get_base_prompt(text_content)
        system = _get_system_prompt(persona_id)
        return _adapt_for_model(model_type, base, system, model_id)
```

Use Cases:
- Standard message format (OpenAI, Gemini, Grok)
- Content format (Claude)
- System role limitations (o1-mini)
- Temperature handling (o3-mini)

### 3. Error Prevention

```python
MODEL_CONFIGS = {
    "openai": {
        "standard": {
            "max_tokens": 1024,
            "format": "messages"
        },
        "o1-mini": {
            "max_tokens": 1024,
            "format": "combined"
        }
    }
}
```

Validation Points:
- Model configuration existence
- Format type validation
- Parameter compatibility
- Token limits

## Implementation Guidelines

### 1. Adding New Models

1. Update MODEL_CONFIGS:
```python
MODEL_CONFIGS["new_model"] = {
    "standard": {
        "max_tokens": 1024,
        "format": "messages"
    }
}
```

2. Implement format adapter if needed:
```python
def _adapt_for_model(model_type, base, system, model_id):
    if model_type == "new_model":
        return create_new_model_format(base, system)
```

### 2. Error Handling

1. Configuration validation:
```python
if model_type not in MODEL_CONFIGS:
    raise ValueError(f"Unsupported model type: {model_type}")
```

2. Format validation:
```python
if "format" not in model_config:
    raise ValueError(f"Missing format configuration for {model_type}")
```

### 3. Testing

1. Format verification:
```python
def test_prompt_format():
    prompt = PromptManager.get_prompt("openai", "p1", "test")
    assert "messages" in prompt
    assert len(prompt["messages"]) == 2  # system + user
```

2. Content validation:
```python
def test_content_format():
    prompt = PromptManager.get_prompt("claude", "p1", "test")
    assert "system" in prompt
    assert isinstance(prompt["messages"][0]["content"], list)
```

## Best Practices

1. Prompt Design
   - Keep base prompts simple and clear
   - Use template strings for dynamic content
   - Document format requirements

2. Configuration Management
   - Use constants for common values
   - Document model limitations
   - Version control configurations

3. Error Handling
   - Validate inputs early
   - Provide clear error messages
   - Log validation failures

4. Testing
   - Test all supported formats
   - Verify error cases
   - Document test scenarios

## Known Issues

1. System Role Support
   - o1-mini: No native system role support
   - Solution: Combine with user message

2. Temperature Parameter
   - o3-mini: No temperature support
   - Solution: Omit parameter

3. Message Format
   - Claude: Requires content array
   - Solution: Use format adapter

## Future Improvements

1. Dynamic Registration
   - Plugin system for new models
   - Auto-configuration detection
   - Format validation rules

2. Performance
   - Cache common prompts
   - Lazy loading of configurations
   - Format pre-validation

3. Monitoring
   - Usage tracking
   - Error rate monitoring
   - Format validation metrics
