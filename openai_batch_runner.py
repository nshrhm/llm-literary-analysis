"""OpenAI batch processing implementation."""

import os
import json
from datetime import datetime
from openai import OpenAI
from parameters import OPENAI_MODELS

class OpenAIBatchRunner:
    """Handles OpenAI batch processing experiments."""
    
    def __init__(self):
        """Initialize the batch runner."""
        self.client = OpenAI()
        
        # Create required directories
        os.makedirs("results/openai/batch_inputs", exist_ok=True)
        os.makedirs("results/openai/batch_results", exist_ok=True)
        os.makedirs("results/openai/batch_errors", exist_ok=True)
        
    def _create_jsonl_input(self):
        """Create JSONL input file for batch processing."""
        from parameters import TEXT_CONTENT, PERSONAS, TEMPERATURE
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_file = f"results/openai/batch_inputs/batch_requests_{timestamp}.jsonl"
        
        # Get first model for initial test
        model_config = next(iter(OPENAI_MODELS.values()))
        text = TEXT_CONTENT["t1"]  # 懐中時計のテキスト
        persona = PERSONAS["p1"]  # 大学1年生
        
        # Create request with proper prompt
        request = {
            "custom_id": f"p1_t1_n01",  # Format: persona_text_trial
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model_config["model_name"],
                "temperature": TEMPERATURE,
                "messages": [
                    {
                        "role": "system",
                        "content": f"あなたは{persona}です。日本の文学テキストに対する感情分析を行います。"
                    },
                    {
                        "role": "user",
                        "content": f"""以下のテキストを読んで、4つの感情（面白さ、驚き、悲しみ、怒り）について0-100の数値で評価し、
その理由も説明してください。

テキスト：
{text}

回答は以下の形式で記述してください：
Q1. 面白さ(数値): [0-100]
Q1. 面白さ(理由): [説明]

Q2. 驚き(数値): [0-100]
Q2. 驚き(理由): [説明]

Q3. 悲しみ(数値): [0-100]
Q3. 悲しみ(理由): [説明]

Q4. 怒り(数値): [0-100]
Q4. 怒り(理由): [説明]"""
                    }
                ]
            }
        }
        
        # Write request to JSONL file
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(request, f, ensure_ascii=False)
            f.write("\n")
        
        return input_file
    
    def _wait_for_completion(self, batch_id, max_retries=24, sleep_time=10):
        """Wait for batch job completion."""
        import time
        
        retries = 0
        while retries < max_retries:
            status = self.client.batches.retrieve(batch_id)
            print(f"Batch status: {status.status}")
            
            # Print detailed status information
            print(f"\nBatch status details:")
            print(f"- Status: {status.status}")
            print(f"- Total requests: {status.request_counts.total}")
            print(f"- Completed: {status.request_counts.completed}")
            print(f"- Failed: {status.request_counts.failed}")
            
            if status.status == "completed":
                return status
            elif status.status in ["failed", "cancelled", "expired"]:
                if status.errors:
                    print("\nBatch errors:")
                    for error in status.errors.data:
                        print(f"- {error.message}")
                return status
            
            retries += 1
            if retries < max_retries:
                # Adjust sleep time based on status
                if status.status == "validating":
                    current_sleep = 5  # Shorter wait during validation
                else:
                    current_sleep = sleep_time
                    
                print(f"\nWaiting {current_sleep} seconds before next check...")
                time.sleep(current_sleep)
            else:
                print(f"\nNote: The batch job {batch_id} is still processing.")
                print("You can check its status later using:")
                print(f"python openai_example.py --status {batch_id}")
                return status
        
        return None

    def _save_results(self, status, timestamp):
        """Save batch processing results."""
        if status.output_file_id:
            output_file = self.client.files.retrieve_content(status.output_file_id)
            results_file = f"results/openai/batch_results/results_{timestamp}.jsonl"
            
            # 結果データをJSONとして解析し、整形して保存
            result_data = json.loads(output_file)
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            print(f"Results saved to: {results_file}")
            
        if status.error_file_id:
            error_file = self.client.files.retrieve_content(status.error_file_id)
            error_log = f"results/openai/batch_errors/errors_{timestamp}.jsonl"
            
            # エラーデータも同様に整形
            error_data = json.loads(error_file)
            with open(error_log, "w", encoding="utf-8") as f:
                json.dump(error_data, f, ensure_ascii=False, indent=2)
            print(f"Errors saved to: {error_log}")

    def run_batch_experiment(self):
        """Run the batch experiment."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create input file
            input_file = self._create_jsonl_input()
            print(f"Created input file: {input_file}")
            
            # Upload file to OpenAI
            with open(input_file, "rb") as f:
                uploaded_file = self.client.files.create(
                    file=f,
                    purpose="batch"
                )
            print(f"Uploaded file with ID: {uploaded_file.id}")
            
            # Create batch
            batch = self.client.batches.create(
                input_file_id=uploaded_file.id,
                endpoint="/v1/chat/completions",
                completion_window="24h"
            )
            print(f"Created batch with ID: {batch.id}")
            
            # Wait for completion
            status = self._wait_for_completion(batch.id)
            if status:
                self._save_results(status, timestamp)
            
        except Exception as e:
            print(f"Error in batch processing: {str(e)}")
            raise
