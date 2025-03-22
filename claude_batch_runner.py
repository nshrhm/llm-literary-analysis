"""Claude batch processing implementation."""

import os
import json
from datetime import datetime
from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

class ClaudeBatchRunner:
    """Handles Claude batch processing experiments."""
    
    def __init__(self):
        """Initialize the batch runner."""
        self.client = Anthropic()
        
        # Create required directories
        os.makedirs("results/claude/batch_inputs", exist_ok=True)
        os.makedirs("results/claude/batch_results", exist_ok=True)
        os.makedirs("results/claude/batch_errors", exist_ok=True)
        os.makedirs("results/claude", exist_ok=True)
        
    def _create_batch_requests(self, model_id, model_config, timestamp):
        """Create batch requests for Claude API."""
        from parameters import TEXT_CONTENT, PERSONAS
        
        requests = []
        for persona_id, persona in PERSONAS.items():
            for text_id, text_content in TEXT_CONTENT.items():
                custom_id = f"{persona_id}_{model_id}_{text_id}_n01"
                
                # Prepare content
                content = [{
                    "type": "text",
                    "text": f"""以下のテキストを読んで、4つの感情（面白さ、驚き、悲しみ、怒り）について0-100の数値で評価し、
その理由も説明してください。

テキスト：
{text_content}

回答は以下の形式で記述してください：
Q1. 面白さ(数値): [0-100]
Q1. 面白さ(理由): [説明]

Q2. 驚き(数値): [0-100]
Q2. 驚き(理由): [説明]

Q3. 悲しみ(数値): [0-100]
Q3. 悲しみ(理由): [説明]

Q4. 怒り(数値): [0-100]
Q4. 怒り(理由): [説明]"""
                }]

                # Create request
                request = Request(
                    custom_id=custom_id,
                    params=MessageCreateParamsNonStreaming(
                        model=model_config,  # CLAUDEモデルは直接モデル名を使用
                        max_tokens=1024,
                        system=[{
                            "type": "text",
                            "text": f"あなたは{persona}です。日本の文学テキストに対する感情分析を行います。"
                        }],
                        messages=[{
                            "role": "user",
                            "content": content
                        }]
                    )
                )
                requests.append(request)
        
        return requests
    
    def _wait_for_completion(self, batch_id, max_retries=24, sleep_time=300):
        """Wait for batch job completion."""
        import time
        
        retries = 0
        while retries < max_retries:
            status = self.client.messages.batches.retrieve(batch_id)
            print(f"\nBatch status details:")
            print(f"- Status: {status.processing_status}")
            print(f"- Total requests: {status.request_counts.processing + status.request_counts.succeeded + status.request_counts.errored}")
            print(f"- Completed: {status.request_counts.succeeded}")
            print(f"- Failed: {status.request_counts.errored}")
            
            if status.processing_status == "ended":
                return status
            
            retries += 1
            if retries < max_retries:
                print(f"\nWaiting {sleep_time} seconds before next check...")
                time.sleep(sleep_time)
            else:
                print(f"\nNote: The batch job {batch_id} is still processing.")
                print("You can check its status later using:")
                print(f"python claude_example.py --status {batch_id}")
                return status
        
        return None
    
    def _save_results(self, status, timestamp, model_id):
        """Save batch processing results."""
        if status.results_url:
            # Process results by streaming
            for result in self.client.messages.batches.results(status.id):
                try:
                    custom_id = result.custom_id
                    
                    match result.result.type:
                        case "succeeded":
                            # Parse custom_id: persona_model_text_trial
                            parts = custom_id.split("_")
                            persona_id = parts[0]
                            model_id = parts[1]
                            text_id = parts[2]
                            trial = parts[3]
                            
                            # Extract content
                            message = result.result.message
                            content = message.content[0].text
                            
                            # Save in txt format
                            output_file = f"results/claude/{custom_id}.txt"
                            with open(output_file, "w", encoding="utf-8") as f:
                                # Write metadata
                                f.write(f"timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                f.write(f"persona: {persona_id}\n")
                                f.write(f"model: {model_id}\n")
                                f.write(f"trial: {trial}\n")
                                f.write(f"text: {text_id}\n")
                                # Write content
                                f.write(f"\n{content}\n")
                            
                            print(f"Saved result for {custom_id}")
                            
                        case "errored":
                            error_log = f"results/claude/batch_errors/error_{custom_id}_{timestamp}.jsonl"
                            with open(error_log, "w", encoding="utf-8") as f:
                                error_data = {
                                    "type": result.result.error.type,
                                    "message": result.result.error.message
                                }
                                json.dump(error_data, f, ensure_ascii=False)
                            print(f"Error processing {custom_id}: {result.result.error.message}")
                            
                        case _:
                            print(f"Unexpected result type for {custom_id}: {result.result.type}")
                
                except Exception as e:
                    print(f"Error processing result for {custom_id}: {str(e)}")
            
            print(f"Results processing completed for model {model_id}")
    
    def run_batch_experiment(self):
        """Run the batch experiment."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Get supported Claude models from parameters
            from parameters import CLAUDE_MODELS
            
            print(f"Starting batch processing for {len(CLAUDE_MODELS)} models...")
            for model_id, model_config in CLAUDE_MODELS.items():
                print(f"\nProcessing model: {model_id}")
                
                try:
                    # Create batch requests
                    requests = self._create_batch_requests(model_id, model_config, timestamp)
                    print(f"Created {len(requests)} requests")
                    
                    # Create batch
                    batch = self.client.messages.batches.create(requests=requests)
                    print(f"Created batch with ID: {batch.id}")
                    
                    # Wait for completion and save results
                    print(f"Waiting for batch completion...")
                    status = self._wait_for_completion(batch.id)
                    if status and status.processing_status == "ended":
                        self._save_results(status, timestamp, model_id)
                    
                except Exception as e:
                    print(f"Error processing model {model_id}: {str(e)}")
                    continue
                
            print("\nBatch processing completed for all models!")
            
        except Exception as e:
            print(f"Error in batch processing: {str(e)}")
            raise
