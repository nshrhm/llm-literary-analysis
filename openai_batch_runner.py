"""OpenAI batch processing implementation."""

import os
import json
from datetime import datetime
from openai import OpenAI
from parameters import OPENAI_MODELS, TRIALS
from prompt_manager import PromptManager

class OpenAIBatchRunner:
    """Handles OpenAI batch processing experiments."""
    
    def __init__(self):
        """Initialize the batch runner."""
        self.client = OpenAI()
        
        # Create required directories
        os.makedirs("results/openai/batch_inputs", exist_ok=True)
        os.makedirs("results/openai/batch_results", exist_ok=True)
        os.makedirs("results/openai/batch_errors", exist_ok=True)
        os.makedirs("results/openai", exist_ok=True)
        

    
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
            # Get output content
            output_file = self.client.files.retrieve_content(status.output_file_id)
            
            # Parse JSONL format (one JSON object per line)
            results_data = []
            for line in output_file.strip().split('\n'):
                if line:
                    results_data.append(json.loads(line))
            
            # Save results in JSONL format for reference
            results_file = f"results/openai/batch_results/results_{timestamp}.jsonl"
            with open(results_file, "w", encoding="utf-8") as f:
                for result in results_data:
                    json.dump(result, f, ensure_ascii=False)
                    f.write('\n')
            
            # Process each result and save as txt
            for result in results_data:
                try:
                    custom_id = result["custom_id"]
                    response = result["response"]
                    
                    if response["status_code"] == 200:
                        # Parse custom_id
                        parts = custom_id.split("_")
                        persona_id = parts[0]
                        model_id = parts[1]
                        text_id = parts[2]
                        trial = parts[3]
                        
                        # Extract content
                        content = response["body"]["choices"][0]["message"]["content"]
                        
                        # Save in txt format
                        output_file = f"results/openai/{custom_id}.txt"
                        with open(output_file, "w", encoding="utf-8") as f:
                            # Write metadata
                            f.write(f"timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"persona: {persona_id}\n")
                            f.write(f"model: {model_id}\n")
                            f.write(f"trial: {trial}\n")
                            f.write(f"text: {text_id}\n")
                            
                            # temperatureはモデルがサポートする場合のみ追加
                            if len(parts) > 4 and "temp" in parts[4]:
                                temp = int(parts[4].replace("temp", "")) / 100
                                f.write(f"temperature: {temp}\n")
                            # Write content
                            f.write(f"\n{content}\n")
                
                except Exception as e:
                    print(f"Error processing result for {custom_id}: {str(e)}")
            
            print(f"Results saved to: {results_file}")
            print("Individual result files saved in results/openai/")
            
        if status.error_file_id:
            error_file = self.client.files.retrieve_content(status.error_file_id)
            error_log = f"results/openai/batch_errors/errors_{timestamp}.jsonl"
            
            # Parse and save errors in JSONL format
            error_data = []
            for line in error_file.strip().split('\n'):
                if line:
                    error_data.append(json.loads(line))
            
            with open(error_log, "w", encoding="utf-8") as f:
                for error in error_data:
                    json.dump(error, f, ensure_ascii=False)
                    f.write('\n')
            print(f"Errors saved to: {error_log}")

    def _create_model_batch(self, model_id, model_config, timestamp):
        """Create batch for a specific model."""
        from parameters import TEXT_CONTENT, PERSONAS, TEXTS
        
        # Debug print to check model config
        print(f"\nCreating batch for model: {model_id}")
        print(f"Model config: {model_config}")
        print(f"Temperature support: {model_config.get('temperature_support', True)}")
        
        # Create input file for this model
        input_file = f"results/openai/batch_inputs/batch_requests_{model_id}_{timestamp}.jsonl"
        
        with open(input_file, "w", encoding="utf-8") as f:
                    for persona_id, persona_info in PERSONAS.items():
                        for text_id, text_info in TEXTS.items():
                            for trial in range(1, TRIALS + 1):
                                text_content = TEXT_CONTENT[text_id]
                                
                                # PromptManagerでプロンプトを生成（温度制御も含む）
                                prompt = PromptManager.get_prompt("openai", persona_id, text_content, text_id, model_id)
                                
                                # カスタムIDを生成 (試行番号を2桁でフォーマット)
                                trial_num = f"n{trial:02d}"
                                custom_id = f"{persona_id}_{model_id}_{text_id}_{trial_num}"
                                
                                # temperature_supportがTrueの場合のみtemp値を追加
                                if model_config.get("temperature_support", False):
                                    temp_value = prompt.get("temperature", 0.5)  # デフォルト値0.5
                                    custom_id += f"_temp{int(temp_value*100)}"
                                
                                # リクエストの作成
                                request = {
                                    "custom_id": custom_id,
                                    "method": "POST",
                                    "url": "/v1/chat/completions",
                                    "body": {
                                        "model": model_config["model_name"],
                                        **prompt
                                    }
                                }
                                
                                json.dump(request, f, ensure_ascii=False)
                                f.write("\n")
        
        return input_file

    def run_batch_experiment(self, models=None):
        """Run the batch experiment.
        
        Args:
            models: Dictionary of models to process. If None, uses all OPENAI_MODELS.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # If no models specified, use all OPENAI_MODELS
            models = models or OPENAI_MODELS
            
            print(f"Starting batch processing for {len(models)} models...")
            for model_id, model_config in models.items():
                print(f"\nProcessing model: {model_id}")
                
                # Create input file for this model
                input_file = self._create_model_batch(model_id, model_config, timestamp)
                print(f"Created input file: {input_file}")
                
                try:
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
                    
                    # Wait for completion and save results
                    print(f"Waiting for batch completion...")
                    status = self._wait_for_completion(batch.id)
                    if status and status.status == "completed":
                        self._save_results(status, f"{timestamp}_{model_id}")
                    
                except Exception as e:
                    print(f"Error processing model {model_id}: {str(e)}")
                    continue
                
            print("\nBatch processing completed for all models!")
            
        except Exception as e:
            print(f"Error in batch processing: {str(e)}")
            raise
