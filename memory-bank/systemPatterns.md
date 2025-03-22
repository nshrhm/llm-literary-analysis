# System Patterns

## Batch Processing Patterns

### 1. Model-Specific Request Adaptation (2025/03/22)

#### Pattern: Dynamic Request Format
```python
def create_request(model_id, params):
    if model_id in MODEL_LIMITATIONS:
        return adapt_request(params, MODEL_LIMITATIONS[model_id])
    return create_standard_request(params)
```

#### Use Cases
- OpenAI o3-mini: Remove temperature parameter
- OpenAI o1-mini: Adapt system role messages
- Future model adaptations

#### Benefits
- Flexible request handling
- Error prevention
- Maintainable code

### 2. Batch Progress Monitoring

#### Pattern: Status Polling with Backoff
```python
def monitor_batch(batch_id):
    while not is_complete(batch_id):
        status = check_status(batch_id)
        if status.needs_retry:
            apply_backoff()
        yield status
```

#### Use Cases
- Long-running batch jobs
- Rate limit handling
- Status tracking

#### Benefits
- Efficient resource usage
- Reliable monitoring
- Error recovery

### 3. Result Processing Pipeline

#### Pattern: Multi-format Result Handler
```python
def process_results(batch_results):
    # Save raw results
    save_jsonl_results(batch_results)
    
    # Process individual results
    for result in batch_results:
        # Convert to standard format
        processed = convert_to_standard_format(result)
        # Save in required format
        save_txt_result(processed)
```

#### Use Cases
- Format conversion
- Result validation
- Data aggregation

#### Benefits
- Format consistency
- Easy aggregation
- Error tracking

### 4. Error Recovery Strategy

#### Pattern: Tiered Error Handling
```python
def handle_error(error, context):
    if is_model_limitation(error):
        return adapt_request_format(context)
    if is_temporary_error(error):
        return retry_with_backoff(context)
    if is_partial_failure(error):
        return handle_partial_results(context)
    raise UnrecoverableError(error)
```

#### Use Cases
- Model limitations
- API errors
- Partial failures

#### Benefits
- Graceful degradation
- Maximum data recovery
- Clear error patterns

### 5. Resource Management

#### Pattern: Automatic Cleanup
```python
def manage_resources(batch_job):
    try:
        process_batch(batch_job)
    finally:
        cleanup_temp_files()
        release_resources()
```

#### Use Cases
- Temporary file management
- Resource allocation
- Memory management

#### Benefits
- Resource efficiency
- Reliable cleanup
- Error resilience

## Application Guidelines

1. Model Support
   - Check model limitations
   - Implement appropriate adaptations
   - Document restrictions

2. Error Management
   - Define error categories
   - Implement recovery strategies
   - Log error patterns

3. Resource Optimization
   - Monitor resource usage
   - Implement cleanup
   - Track performance

4. Documentation
   - Update pattern documentation
   - Record known issues
   - Share best practices
