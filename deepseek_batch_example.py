#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deepseek_batch_example.py: Example usage of batch processing for DeepSeek models
"""

import os
from datetime import datetime
from typing import List, Dict

from kluster_batch_runner import KlusterBatchRunner

def main():
    # Initialize the batch runner
    runner = KlusterBatchRunner()

    # Get model definitions
    from parameters import DEEPSEEK_MODELS

    # Create persona-text combinations
    personas = ["p1", "p2", "p3", "p4"]  # Personas 1-4
    texts = ["t1", "t2", "t3"]          # Texts 1-3

    # Create all combinations
    persona_texts = [(p, t) for p in personas for t in texts]

    # Process each DeepSeek model
    for model_id, model_name in DEEPSEEK_MODELS.items():
        print(f"\nRunning batch job for {model_id}...")
        
        # Create batch requests for each trial
        for trial in range(1, 4):  # 3 trials
            trial_num = f"n{trial:02d}"
            
            # Create and process batch requests
            requests = runner.create_batch_requests(
                model=model_name,
                persona_texts=persona_texts,
                trial_num=trial_num
            )
            
            # Save requests and submit batch job
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_file = runner.save_batch_requests(
                requests=requests,
                model_type="deepseek",
                timestamp=timestamp
            )
            
            # Submit and monitor job
            batch_request = runner.submit_batch_job(input_file)
            batch_status = runner.monitor_status(batch_request.id)
            
            # Save results
            jsonl_path, txt_paths = runner.save_results(
                batch_status=batch_status,
                model_type="deepseek",
                timestamp=timestamp
            )
            
            print(f"Trial {trial} complete:")
            print(f"Input file: {input_file}")
            print(f"JSONL file: {jsonl_path}")
            print(f"Generated {len(txt_paths)} TXT files")

if __name__ == "__main__":
    main()
