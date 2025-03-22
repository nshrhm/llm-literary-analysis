# Error Handling Guidelines

## Model-Specific Errors

### OpenAI Models

1. o3-mini
   ```python
   # Error: Unsupported parameter 'temperature'
   # Solution: Remove temperature parameter
   request = {
       "messages": [...],
       # temperature parameter removed
   }
   ```

2. o1-mini
   ```python
   # Error: Unsupported system role
   # Solution: Combine with user message
   request = {
       "messages": [
           {
               "role": "user",
               "content": f"{system_content}\n\n{user_content}"
           }
       ]
   }
   ```

## Common Error Patterns

1. API Rate Limits
   ```python
   def handle_rate_limit(retry_after):
       if retry_after:
           time.sleep(retry_after)
       else:
           time.sleep(exponential_backoff())
   ```

2. Model Availability
   ```python
   def handle_model_unavailable(model_id):
       # Log unavailability
       log_model_status(model_id, "unavailable")
       # Try fallback model if available
       if fallback := get_fallback_model(model_id):
           return retry_with_model(fallback)
       raise ModelUnavailableError(model_id)
   ```

3. Batch Processing Errors
   ```python
   def handle_batch_error(batch_id, error):
       if is_partial_success(error):
           # Save successful results
           save_partial_results(batch_id)
           # Retry failed requests
           retry_failed_requests(batch_id)
       else:
           # Complete failure
           handle_complete_failure(batch_id)
   ```

## Error Recovery Strategies

1. Exponential Backoff
   ```python
   def exponential_backoff(attempt, base_delay=1, max_delay=300):
       delay = min(base_delay * (2 ** attempt), max_delay)
       jitter = random.uniform(0, 0.1 * delay)
       return delay + jitter
   ```

2. Batch Splitting
   ```python
   def split_batch(batch_id):
       """Split a failed batch into smaller chunks"""
       requests = get_batch_requests(batch_id)
       chunks = split_into_chunks(requests)
       return [create_new_batch(chunk) for chunk in chunks]
   ```

3. Result Validation
   ```python
   def validate_results(results):
       """Validate batch processing results"""
       for result in results:
           if not is_valid_format(result):
               log_format_error(result)
               continue
           if not is_valid_content(result):
               log_content_error(result)
               continue
           save_valid_result(result)
   ```

## Logging and Monitoring

1. Error Logging
   ```python
   def log_batch_error(batch_id, error):
       log.error(f"Batch {batch_id} failed: {error}")
       metrics.increment("batch_errors", tags={"type": error.type})
   ```

2. Performance Monitoring
   ```python
   def monitor_batch_performance(batch_id):
       start_time = time.time()
       try:
           process_batch(batch_id)
       finally:
           duration = time.time() - start_time
           metrics.timing("batch_duration", duration)
   ```

## Best Practices

1. Error Documentation
   - Document all error types
   - Maintain error handling patterns
   - Update based on new failures

2. Recovery Procedures
   - Define clear recovery steps
   - Document manual intervention cases
   - Maintain fallback procedures

3. Monitoring
   - Track error rates
   - Monitor recovery success
   - Alert on pattern changes

4. Testing
   - Test error scenarios
   - Verify recovery procedures
   - Validate logging
