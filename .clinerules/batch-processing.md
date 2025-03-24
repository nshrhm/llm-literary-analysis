# Batch Processing Guidelines

## Core Principles

1. Single Model Per Batch
   - Each batch must contain requests for a single model only
   - Separate batches for different model versions

2. Request Format Adaptation
   - Consider model-specific limitations
   - Adapt system prompts based on model capabilities
   - Remove unsupported parameters

3. Performance Optimization
   - Use provider-recommended batch sizes
   - Implement appropriate retry strategies
   - Monitor batch processing status

## Implementation Notes

### Request Formatting

1. Model Capability Check
```python
def _create_model_batch(self model_id model_config):
    # Adapt request format based on model capabilities
    if model_id in ['o3-mini']:
        # Remove temperature parameter
        request = create_request_without_temperature()
    elif model_id in ['o1-mini']:
        # Combine system and user messages
        request = create_request_without_system_role()
    elif model_id.startswith('claude'):
        # Claude models support standard parameters
        request = create_claude_request(
            model_config=model_config,
            temperature=TEMPERATURE,  # Standard temperature support
            max_tokens=1024,
            system=system_message,
            messages=user_messages
        )
    else:
        # Use standard format
        request = create_standard_request()
```

2. Claude-Specific Features
- Temperature Support: 全モデルでtemperature対応 (0.0-1.0)
- System Messages: ペルソナ設定用のシステムメッセージ対応
- Batch Size: 最大100,000リクエスト
- Result Retention: 29日間のデータ保持
- Prompt Caching: コスト最適化のためのキャッシュ対応

2. Batch Size Optimization
```python
# Provider-specific batch sizes
BATCH_SIZES = {
    'openai': 50,    # OpenAI recommended
    'claude': 100,   # Anthropic recommended
    'gemini': 250    # Google recommended
}
```

### Error Handling

1. Batch Creation
   - Validate model compatibility
   - Check request format
   - Verify input parameters

2. Processing
   - Monitor completion status
   - Handle partial failures
   - Implement retry logic

3. Result Management
   - Validate response format
   - Process partial successes
   - Log and report errors

## Best Practices

1. Testing
   - Test with small batches first
   - Verify format compatibility
   - Check error handling

2. Monitoring
   - Track batch progress
   - Monitor completion rates
   - Log error patterns

3. Documentation
   - Document model limitations
   - Keep error handling guides
   - Update implementation notes

## Cost Optimization

1. Batch Size
   - Balance between throughput and reliability
   - Consider API rate limits
   - Monitor cost per request

2. Retry Strategy
   - Implement exponential backoff
   - Set maximum retry attempts
   - Track failure patterns

3. Resource Management
   - Clean up temporary files
   - Monitor disk usage
   - Manage API quotas
