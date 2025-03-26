## Batch Processing Guidelines

## Core Principles

1. Single Model Per Batch
   - Each batch must contain requests for a single model only
   - Separate batches for different model versions
   - Use consistent model identifiers across the system

2. Model Identification
   - Use standardized model identifiers
   - Maintain mapping between identifiers and display names
   - Follow consistent naming conventions

3. File Naming and Organization
   - Use standardized file naming patterns
   - Include model identifiers in filenames
   - Maintain metadata consistency

## Implementation Notes

### Model Identifier Handling

1. Model Identifier Format
```python
def _get_model_identifier(model: str) -> str:
    # DeepSeek models
    if model_id == "deepseekr1":
        return "deepseekr1"
    elif model_id == "deepseekv3":
        return "deepseekv3"
    elif model_id == "deepseekv3-0324":
        return "deepseekv3-0324"

    # Llama models
    if model_id == "llama33-70Bit":
        return "llama33-70Bit"
    elif model_id == "llama31-405Bit":
        return "llama31-405Bit"
    elif model_id == "llama31-8Bit":
        return "llama31-8Bit"
```

2. Display Name Generation
```python
def _get_model_display_name(model: str) -> str:
    # DeepSeek display names
    if model_id == "deepseekr1":
        return "DeepSeek-R1"
    elif model_id == "deepseekv3":
        return "DeepSeek-V3"
    elif model_id == "deepseekv3-0324":
        return "DeepSeek-V3-0324"

    # Llama display names
    if model_id == "llama33-70Bit":
        return "Llama-3.3-70B"
    elif model_id == "llama31-405Bit":
        return "Llama-3.1-405B"
    elif model_id == "llama31-8Bit":
        return "Llama-3.1-8B"
```

### Request Formatting

1. Model-Specific Adaptations
```python
def create_batch_requests(model: str, ...) -> List[Dict]:
    # Get model identifier and display name
    model_identifier = _get_model_identifier(model)
    model_display_name = _get_model_display_name(model)

    # Generate custom ID with model identifier
    custom_id = f"{persona_id}_{model_identifier}_{text_id}_{trial_num}_temp{temperature}"

    # Create request with model display name
    request = {
        "custom_id": custom_id,
        "model_display_name": model_display_name,
        ...
    }
```

### Error Handling

1. Validation Rules
   - Verify model identifier format
   - Check display name consistency
   - Validate file naming patterns

2. Processing Checks
   - Ensure model type consistency
   - Verify metadata format
   - Check identifier mapping

3. Result Management
   - Validate model names in results
   - Ensure consistent display names
   - Check file naming compliance

## Best Practices

1. Model Identification
   - Use consistent identifier formats
   - Maintain clear identifier-display name mapping
   - Document model naming conventions

2. File Organization
   - Follow standardized naming patterns
   - Include model identifiers in paths
   - Maintain metadata consistency

3. Documentation
   - Document model identifiers
   - Keep naming conventions updated
   - Maintain identifier mappings

## Result Management

1. File Naming
   - Use model identifiers in filenames
   - Follow standardized patterns
   - Include all required components

2. Metadata
   - Include model display names
   - Maintain consistent format
   - Document version information

3. Aggregation
   - Use display names in reports
   - Maintain model grouping
   - Ensure version tracking
