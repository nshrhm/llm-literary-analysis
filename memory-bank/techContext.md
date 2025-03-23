# Technical Context

## Unified Prompt Management Implementation (2025-03-23)

1. Architecture Overview
   ```python
   class PromptManager:
       def get_prompt(model_type, persona_id, text_content, model_id=None):
           base = _get_base_prompt(text_content)
           system = _get_system_prompt(persona_id)
           return _adapt_for_model(model_type, base, system, model_id)
   ```

2. Key Components
   - Centralized prompt definition in parameters.py
   - Model-specific configurations
   - Standard format adapters
   - Error prevention mechanisms

3. Model-Specific Adaptations
   ```python
   # OpenAI standard format
   {
       "messages": [
           {"role": "system", "content": system},
           {"role": "user", "content": base}
       ]
   }
   
   # OpenAI o1-mini format (no system role)
   {
       "messages": [
           {"role": "user", "content": f"{system}\n\n{base}"}
       ]
   }
   
   # Claude format
   {
       "system": [{"type": "text", "text": system}],
       "messages": [{
           "role": "user",
           "content": [{"type": "text", "text": base}]
       }]
   }
   ```

4. Result Aggregation Verification
   - Files Processed:
     - OpenAI: 48 files (100% success)
     - Claude: 60 files (100% success)
     - Gemini: 83 files (100% success)
     - Grok: 12 files (100% success)
     - DeepSeek: 24 files (100% success)
     - Llama: 36 files (100% success)
   
   - Data Format:
     - Metadata extraction validated
     - Score ranges confirmed (0-100)
     - Reason text properly extracted
     - Unicode handling verified

5. Performance Metrics
   - Average processing time per file: <1s
   - Memory usage: stable
   - Error rate: 0%
   - Format consistency: 100%

6. Future Improvements
   - Dynamic model registration
   - Enhanced error recovery
   - Performance optimization
   - Format validation enhancements

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
