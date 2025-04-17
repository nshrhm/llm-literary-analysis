# Error Handling Guidelines

## Model-Specific Errors

### OpenAI Models（2025-04-17更新）

1. GPT-4.1シリーズ
   ```python
   # 価格情報の検証
   def validate_pricing_info(model_id, pricing):
       if not pricing or not all(k in pricing for k in ["input", "cached_input", "output"]):
           raise ValidationError("Invalid pricing format")
       
       expected = get_model_pricing(model_id)
       if not all(abs(pricing[k] - expected[k]) < 0.001 for k in expected):
           raise ValidationError("Pricing rates mismatch")
   
   # バッチ処理のコスト最適化
   def optimize_batch_cost(batch_requests):
       """コストを50%削減するためのバッチ最適化"""
       return {
           "model": model_id,
           "messages": batch_requests["messages"],
           "temperature": batch_requests["temperature"],
           "use_cache": True  # キャッシュ利用による入力コスト削減
       }
   ```

2. o3-mini
   ```python
   # Error: Unsupported parameter 'temperature'
   # Solution: Remove temperature parameter
   request = {
       "messages": [...],
       # temperature parameter removed
   }
   ```

3. o1-mini
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

3. Batch Processing Errors（2025-04-17更新）
   ```python
   def handle_batch_error(batch_id, error):
       if is_partial_success(error):
           # Save successful results
           save_partial_results(batch_id)
           # Save cost information for completed requests
           save_cost_info(batch_id)
           # Retry failed requests with cost optimization
           retry_with_cost_optimization(batch_id)
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

2. Batch Splitting（2025-04-17更新）
   ```python
   def split_batch(batch_id):
       """Split a failed batch into smaller chunks"""
       requests = get_batch_requests(batch_id)
       if is_gpt41_series(requests["model"]):
           # コスト最適化を考慮したチャンク分割
           return split_with_cost_optimization(requests)
       return default_split(requests)
   ```

3. Result Validation（2025-04-17更新）
   ```python
   def validate_results(results):
       """Validate batch processing results"""
       for result in results:
           # Format validation
           if not is_valid_format(result):
               log_format_error(result)
               continue
           
           # Content validation
           if not is_valid_content(result):
               log_content_error(result)
               continue
           
           # Cost validation for GPT-4.1 series
           if is_gpt41_series(result.model):
               if not validate_pricing_info(result.model, result.pricing):
                   log_pricing_error(result)
                   continue
           
           save_valid_result(result)
   ```

## Logging and Monitoring（2025-04-17更新）

1. Error Logging
   ```python
   def log_batch_error(batch_id, error):
       log.error(f"Batch {batch_id} failed: {error}")
       metrics.increment("batch_errors", tags={"type": error.type})
       
       # コストに関連するエラーの追跡
       if is_pricing_error(error):
           metrics.increment("pricing_errors", tags={
               "model": error.model,
               "error_type": error.pricing_error_type
           })
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
           
           # コスト効率の計測
           if is_gpt41_series(get_batch_model(batch_id)):
               cost_efficiency = calculate_cost_efficiency(batch_id)
               metrics.gauge("cost_efficiency", cost_efficiency)
   ```

3. Cost Tracking（2025-04-17追加）
   ```python
   def track_batch_costs(batch_id):
       """バッチ処理のコスト追跡"""
       costs = {
           "total_input": 0,
           "total_cached_input": 0,
           "total_output": 0,
           "savings": 0
       }
       
       for result in get_batch_results(batch_id):
           if is_gpt41_series(result.model):
               update_cost_metrics(costs, result.pricing)
       
       return costs
   ```

## Best Practices

1. Error Documentation
   - Document all error types
   - Maintain error handling patterns
   - Update based on new failures
   - Track cost-related errors（2025-04-17追加）

2. Recovery Procedures
   - Define clear recovery steps
   - Document manual intervention cases
   - Maintain fallback procedures
   - Consider cost implications（2025-04-17追加）

3. Monitoring
   - Track error rates
   - Monitor recovery success
   - Alert on pattern changes
   - Track cost efficiency（2025-04-17追加）

4. Testing
   - Test error scenarios
   - Verify recovery procedures
   - Validate logging
   - Verify cost calculations（2025-04-17追加）
