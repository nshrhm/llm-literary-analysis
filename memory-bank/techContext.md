# Technical Context

## Batch Processing Implementation

### OpenAI Batch API (Ver.1) - 2025/03/22

1. Architecture Overview
   - Request Generation (per model)
   - Batch Job Management
   - Result Processing
   - Error Handling

2. Key Components
   ```python
   class OpenAIBatchRunner:
       def _create_model_batch()  # Model-specific request creation
       def _wait_for_completion() # Batch status monitoring
       def _save_results()        # Result processing and storage
   ```

3. Model-Specific Adaptations
   - o3-mini: No temperature parameter support
   ```python
   # Remove temperature parameter
   request = {
       "model": "o3-mini",
       "messages": [...] # Standard messages
   }
   ```
   
   - o1-mini: No system role message support
   ```python
   # Combine system and user messages
   request = {
       "model": "o1-mini",
       "messages": [{
           "role": "user",
           "content": f"{system_content}\n\n{user_content}"
       }]
   }
   ```

   - Standard models: Full parameter support
   ```python
   request = {
       "model": model_name,
       "temperature": 0.5,
       "messages": [
           {"role": "system", "content": system_content},
           {"role": "user", "content": user_content}
       ]
   }
   ```

4. Error Handling Strategies
   - Model-specific request validation
   - Status monitoring with exponential backoff
   - Result format validation
   - Partial success handling

5. Performance Optimization
   - Batch size: 12 requests per batch
   - Processing window: 24 hours
   - Status check interval: 5-10 seconds
   - Error retry limit: 24 attempts

6. Result Management
   - JSONL format for batch results
   - TXT format for individual results
   - Standard metadata format
   - Error logging and tracking

7. Cost Optimization
   - 50% cost reduction through batch processing
   - Efficient retry strategies
   - Resource cleanup

8. Lessons Learned
   - Model-specific limitations require flexible request formatting
   - Batch size affects processing time and reliability
   - Error handling is critical for long-running jobs
   - Result format consistency is important for aggregation

9. Future Improvements
   - Dynamic batch size adjustment
   - Enhanced error recovery
   - Better progress monitoring
   - Result validation enhancement

10. Application to Other APIs
    - Claude: Message batches
    - Gemini: Vertex AI batch prediction
    - Groq: Native batch API
    - kluster.ai: Adaptive processing
