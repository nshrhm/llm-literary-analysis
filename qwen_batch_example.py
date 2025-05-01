#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
qwen_batch_example.py: Example usage of batch processing for Qwen models
"""

import os
from datetime import datetime
from typing import List, Dict

from kluster_batch_runner import KlusterBatchRunner

import argparse
from datetime import datetime
from kluster_batch_runner import KlusterBatchRunner
from parameters import QWEN_MODELS, TRIALS

def main():
    parser = argparse.ArgumentParser(description="Run Qwen batch experiments")
    parser.add_argument("--model", nargs="+", choices=list(QWEN_MODELS.keys()), help="Specify one or more models to run")
    args = parser.parse_args()

    runner = KlusterBatchRunner()

    personas = ["p1", "p2", "p3", "p4"]
    texts = ["t1", "t2", "t3"]
    persona_texts = [(p, t) for p in personas for t in texts]

    if args.model:
        selected_models = {model: QWEN_MODELS[model]["model_name"] for model in args.model}
    else:
        selected_models = {model: info["model_name"] for model, info in QWEN_MODELS.items()}

    for model_id, model_name in selected_models.items():
        print(f"\nRunning batch job for {model_id}...")

        for trial in range(1, TRIALS + 1):
            trial_num = f"n{trial:02d}"

            requests = runner.create_batch_requests(
                model=model_name,
                persona_texts=persona_texts,
                trial_num=trial_num
            )

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_file = runner.save_batch_requests(
                requests=requests,
                model_type="qwen",
                timestamp=timestamp
            )

            batch_request = runner.submit_batch_job(input_file)
            batch_status = runner.monitor_status(batch_request.id)

            jsonl_path, txt_paths = runner.save_results(
                batch_status=batch_status,
                model_type="qwen",
                timestamp=timestamp
            )

            print(f"Trial {trial} complete:")
            print(f"Input file: {input_file}")
            print(f"JSONL file: {jsonl_path}")
            print(f"Generated {len(txt_paths)} TXT files")

if __name__ == "__main__":
    main()
