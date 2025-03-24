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
        from parameters import TEXT_CONTENT, TEMPERATURE
        from prompt_manager import PromptManager

        # Determine model type
        model_type = "deepseek" if "deepseek" in model.lower() else "llama"

        requests = []
        for persona_id, text_id in persona_texts:
            # Generate custom ID
            custom_id = f"{persona_id}_{model_type}_{text_id}_{trial_num}_temp{int(TEMPERATURE*100)}"

            # Get text content
            text_content = TEXT_CONTENT[text_id]

            # Get prompt using PromptManager
            prompt = PromptManager.get_prompt(
                model_type=model_type,
                persona_id=persona_id,
                text_content=text_content
            )

            # Create request
            request = {
                "custom_id": custom_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": model,
                    "temperature": TEMPERATURE,
                    "max_completion_tokens": max_tokens,
                    **prompt
                }
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
    ) -> Optional[str]:
        """
        Save batch processing results.

        Args:
            batch_status (Dict): Batch status information
            model_type (str): Type of model ("deepseek" or "llama")
            timestamp (str, optional): Timestamp for filename. Defaults to current time.

        Returns:
            Optional[str]: Path to the saved results file, or None if processing failed
        """
        if batch_status.status.lower() != "completed":
            print(f"Batch failed with status: {batch_status.status}")
            return None

        if not timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directories if they don't exist
        results_dir = f"results/{model_type}/batch_results"
        os.makedirs(results_dir, exist_ok=True)

        # Get results and parse JSON
        result_file_id = batch_status.output_file_id
        results = self.client.files.content(result_file_id).content
        
        # Parse each line and re-encode with proper Japanese handling
        processed_results = []
        for line in results.decode().split('\n'):
            if line:
                # Parse JSON and re-encode with Japanese support
                result = json.loads(line)
                processed_results.append(json.dumps(result, ensure_ascii=False))
        
        # Save to file with proper encoding
        results_path = f"{results_dir}/batch_results_{timestamp}.jsonl"
        with open(results_path, "w", encoding="utf-8") as f:
            for result in processed_results:
                f.write(result + "\n")

        return results_path

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
