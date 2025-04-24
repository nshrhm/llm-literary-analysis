#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
kluster_batch_runner.py: Batch processing implementation for kluster.ai models (DeepSeek and Llama)
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

from openai import OpenAI

class KlusterBatchRunner:
    """Batch processing runner for kluster.ai models."""

    def __init__(self, api_key: str = None):
        """
        Initialize the batch runner.

        Args:
            api_key (str, optional): kluster.ai API key. Defaults to environment variable.
        """
        self.api_key = api_key or os.getenv("KLUSTERAI_API_KEY")
        if not self.api_key:
            raise ValueError("KLUSTERAI_API_KEY must be provided")

        self.client = OpenAI(
            base_url="https://api.kluster.ai/v1",
            api_key=self.api_key
        )
        self.current_model = None  # Store current model for reference

    def _get_model_identifier(self, model: str) -> str:
        """
        Get model identifier from full model path.

        Args:
            model (str): Full model path

        Returns:
            str: Model identifier
        """
        from parameters import DEEPSEEK_MODELS, LLAMA_MODELS

        # Check DeepSeek models
        for model_id, model_path in DEEPSEEK_MODELS.items():
            if model_path == model:
                if model_id == "deepseekr1":
                    return "deepseekr1"
                elif model_id == "deepseekv3":
                    return "deepseekv3"
                elif model_id == "deepseekv3-0324":
                    return "deepseekv3-0324"
                return model_id

        # Check Llama models
        for model_id, model_path in LLAMA_MODELS.items():
            if model_path == model:
                return model_id

        # Default to base name if not found
        return model.split('/')[-1]

    def _get_model_display_name(self, model: str) -> str:
        """
        Get display name for the model.

        Args:
            model (str): Full model identifier

        Returns:
            str: Display name for the model
        """
        from parameters import DEEPSEEK_MODELS, LLAMA_MODELS

        # Check DeepSeek models
        for model_id, model_path in DEEPSEEK_MODELS.items():
            if model_path == model:
                if model_id == "deepseekr1":
                    return "DeepSeek-R1"
                elif model_id == "deepseekv3":
                    return "DeepSeek-V3"
                elif model_id == "deepseekv3-0324":
                    return "DeepSeek-V3-0324"

        # Check Llama models
        for model_id, model_path in LLAMA_MODELS.items():
            if model_path == model:
                if model_id == "llama4-maveric":
                    return "Llama-4-Maverick-17B"
                elif model_id == "llama4-scout":
                    return "Llama-4-Scout-17B"
                # elif model_id == "llama33-70Bit":
                #     return "Llama-3.3-70B"
                # elif model_id == "llama31-405Bit":
                #     return "Llama-3.1-405B"
                # elif model_id == "llama31-8Bit":
                #     return "Llama-3.1-8B"

        # Default to full path if not found
        return model

    def create_batch_requests(
        self,
        model: str,
        persona_texts: List[tuple[str, str]],
        trial_num: str,
        max_tokens: int = 1000
    ) -> List[Dict]:
        """
        Create batch requests using PromptManager.

        Args:
            model (str): Model identifier (DeepSeek or Llama model)
            persona_texts: List of (persona_id, text_id) tuples
            trial_num (str): Trial number (e.g., "n01")
            max_tokens (int, optional): Maximum tokens for completion. Defaults to 1000.

        Returns:
            List[Dict]: List of formatted batch requests
        """
        from parameters import TEXT_CONTENT, PERSONAS, TEXTS
        from prompt_manager import PromptManager

        # Store current model
        self.current_model = model

        # Get model identifier and display name
        model_identifier = self._get_model_identifier(model)
        model_display_name = self._get_model_display_name(model)

        requests = []
        for persona_id, text_id in persona_texts:
            # Calculate temperature from persona and text settings
            base_temp = PERSONAS[persona_id]["base_temperature"]
            temp_modifier = TEXTS[text_id]["temperature_modifier"]
            temperature = base_temp + temp_modifier

            # Generate custom ID with model identifier
            custom_id = f"{text_id}_{model_identifier}_{persona_id}_temp{int(temperature*100)}_{trial_num.replace('n', '')}"

            # Get text content
            text_content = TEXT_CONTENT[text_id]

            # Get prompt using PromptManager
            prompt = PromptManager.get_prompt(
                model_type="deepseek" if "deepseek" in model.lower() else "llama",
                persona_id=persona_id,
                text_content=text_content,
                text_id=text_id
            )

            # Create request
            request = {
                "custom_id": custom_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": model,
                    "temperature": temperature,
                    "max_completion_tokens": max_tokens,
                    **prompt
                },
                "model_display_name": model_display_name  # Add display name for reference
            }
            requests.append(request)

        return requests

    def save_batch_requests(
        self,
        requests: List[Dict],
        model_type: str,
        timestamp: str = None
    ) -> str:
        """
        Save batch requests to a JSONL file.

        Args:
            requests (List[Dict]): List of batch requests
            model_type (str): Type of model ("deepseek" or "llama")
            timestamp (str, optional): Timestamp for filename. Defaults to current time.

        Returns:
            str: Path to the saved JSONL file
        """
        if not timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directories if they don't exist
        base_dir = f"results/{model_type}/batch_inputs"
        os.makedirs(base_dir, exist_ok=True)

        file_path = f"{base_dir}/batch_requests_{timestamp}.jsonl"
        with open(file_path, "w") as f:
            for request in requests:
                f.write(json.dumps(request) + "\n")

        return file_path

    def submit_batch_job(
        self,
        file_path: str,
        completion_window: str = "24h"
    ) -> Dict:
        """
        Submit a batch job for processing.

        Args:
            file_path (str): Path to the JSONL file containing requests
            completion_window (str, optional): Processing window. Defaults to "24h".

        Returns:
            Dict: Batch job information
        """
        # Upload the file
        batch_input_file = self.client.files.create(
            file=open(file_path, "rb"),
            purpose="batch"
        )

        # Create the batch job
        batch_request = self.client.batches.create(
            input_file_id=batch_input_file.id,
            endpoint="/v1/chat/completions",
            completion_window=completion_window
        )

        return batch_request

    def monitor_status(
        self,
        batch_id: str,
        interval: int = 10
    ) -> Dict:
        """
        Monitor the status of a batch job.

        Args:
            batch_id (str): Batch job ID
            interval (int, optional): Polling interval in seconds. Defaults to 10.

        Returns:
            Dict: Final batch status
        """
        while True:
            batch_status = self.client.batches.retrieve(batch_id)
            status = batch_status.status.lower()
            completed = batch_status.request_counts.completed
            total = batch_status.request_counts.total

            print(f"Batch status: {status}")
            print(f"Completed tasks: {completed} / {total}")

            if status in ["completed", "failed", "cancelled"]:
                return batch_status

            time.sleep(interval)

    def save_results(
        self,
        batch_status: Dict,
        model_type: str,
        timestamp: str = None
    ) -> tuple[Optional[str], List[str]]:
        """
        Save batch results in both JSONL and TXT formats.

        Args:
            batch_status (Dict): Batch status information
            model_type (str): Type of model ("deepseek" or "llama")
            timestamp (str, optional): Timestamp for filename. Defaults to current time.

        Returns:
            tuple[Optional[str], List[str]]: Tuple of (jsonl_path, list of txt_paths), or (None, []) if failed
        """
        if batch_status.status.lower() != "completed":
            print(f"Batch failed with status: {batch_status.status}")
            return None, []

        if not timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directories if they don't exist
        results_dir = f"results/{model_type}/batch_results"
        os.makedirs(results_dir, exist_ok=True)
        os.makedirs(f"results/{model_type}", exist_ok=True)

        # Get results and parse JSON
        result_file_id = batch_status.output_file_id
        results = self.client.files.content(result_file_id).content
        
        # Parse each line and process results
        processed_results = []
        txt_paths = []
        
        # Get model display name using stored current model
        model_display_name = self._get_model_display_name(self.current_model)
        
        for line in results.decode().split('\n'):
            if line:
                # Parse JSON with Japanese support
                result = json.loads(line)
                processed_results.append(json.dumps(result, ensure_ascii=False))
                
                # Extract data for TXT file
                custom_id = result["custom_id"]
                response = result["response"]["body"]["choices"][0]["message"]["content"]
                
                # Save TXT file with model identifier in the filename
                model_identifier = custom_id.split('_')[1]
                txt_path = f"results/{model_type}/{custom_id}.txt"
                
                with open(txt_path, "w", encoding="utf-8") as f:
                    # Write metadata
                    f.write(f"timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"persona: {custom_id.split('_')[2]}\n")
                    f.write(f"model: {model_display_name}\n")  # Use display name
                    f.write(f"trial: {custom_id.split('_')[4]}\n")
                    f.write(f"temperature: {float(custom_id.split('_')[3].replace('temp',''))/100}\n")
                    f.write(f"text: {custom_id.split('_')[0]}\n\n")
                    # Write evaluation results
                    f.write(response)
                
                txt_paths.append(txt_path)
        
        # Save JSONL file
        jsonl_path = f"{results_dir}/batch_results_{timestamp}.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for result in processed_results:
                f.write(result + "\n")

        return jsonl_path, txt_paths

    def run_batch_job(
        self,
        model: str,
        persona_texts: List[tuple[str, str]],
        trial_num: str,
        max_tokens: int = 1000,
        completion_window: str = "24h"
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Run a complete batch job workflow.

        Args:
            model (str): Model identifier
            persona_texts: List of (persona_id, text_id) tuples
            trial_num (str): Trial number (e.g., "n01")
            max_tokens (int, optional): Maximum tokens for completion. Defaults to 1000.
            completion_window (str, optional): Processing window. Defaults to "24h".

        Returns:
            tuple[Optional[str], Optional[str]]: Paths to the input and results files
        """
        # Determine model type
        if "deepseek" in model.lower():
            model_type = "deepseek"
        elif "llama" in model.lower():
            model_type = "llama"
        else:
            raise ValueError("Unsupported model type")

        # Generate timestamp for file naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create and save requests
        requests = self.create_batch_requests(
            model=model,
            persona_texts=persona_texts,
            trial_num=trial_num,
            max_tokens=max_tokens
        )
        input_file = self.save_batch_requests(
            requests=requests,
            model_type=model_type,
            timestamp=timestamp
        )

        # Submit job
        batch_request = self.submit_batch_job(
            file_path=input_file,
            completion_window=completion_window
        )

        # Monitor progress
        batch_status = self.monitor_status(batch_request.id)

        # Save results
        results_file = self.save_results(
            batch_status=batch_status,
            model_type=model_type,
            timestamp=timestamp
        )

        return input_file, results_file
