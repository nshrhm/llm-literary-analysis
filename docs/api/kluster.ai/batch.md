# Perform batch inference jobs

# Overview
This guide provides examples and instructions on how to create, submit, retrieve, and manage batch inference jobs using the kluster.ai API. You will find guidance about preparing your data, selecting a model, submitting your batch job, and retrieving your results. Please make sure you check the API request limits.

# Prerequisites

This guide assumes familiarity with Large Language Model (LLM) development and OpenAI libraries. Before getting started, make sure you have:

- A kluster.ai account - sign up on the kluster.ai platform if you don't have one
- A kluster.ai API key - after signing in, go to the API Keys section and create a new key. For detailed instructions, check out the Get an API key guide
- A virtual Python environment - (optional) recommended for developers using Python. It helps isolate Python installations in a virtual environment to reduce the risk of environment or package conflicts between your projects
- Required Python libraries - install the following Python libraries:
  - OpenAI Python API library - to access the openai module
  - getpass - to handle API keys safely
-  A basic understanding of JSON Lines (JSONL) - JSONL is the required text input format for performing batch inferences with the kluster.ai API

If you plan to use cURL via the CLI, you can export your kluster.ai API key as a variable:

export API_KEY=INSERT_API_KEY

# Supported models

Batch inference using kluster.ai supports the following models:

- deepseek-ai/DeepSeek-R1
- deepseek-ai/DeepSeek-V3
- klusterai/Meta-Llama-3.1-8B-Instruct-Turbo
- klusterai/Meta-Llama-3.1-405B-Instruct-Turbo
- klusterai/Meta-Llama-3.3-70B-Instruct-Turbo
- Qwen/Qwen2.5-VL-7B-Instruct

In addition, you can see the complete list of available models programmatically using the list supported models endpoint.

# Batch job workflow overview

Working with batch jobs in the kluster.ai API involves the following steps:

1. Create batch job file - prepare a JSON Lines file containing one or more chat completion requests to execute in the batch
2. Upload batch job file - upload the file to kluster.ai to receive a unique file ID
3. Start the batch job - initiate a new batch job using the file ID
4. Monitor job progress - track the status of your batch job to ensure successful completion
5. Retrieve results - once the job finishes, access and process the results as needed

In addition to these core steps, this guide will give you hands-on experience to:

- Cancel a batch job - cancel an ongoing batch job before it completes
- List all batch jobs - review all of your batch jobs

### Warning

For the free tier, the maximum number of batch requests (lines in the JSONL file) must be less than 1000, and each file must not exceed 100 MB. For the standard tier, there is no limit to the number of batch requests, but the maximum batch file size is 100 MB per file.

# Quickstart snippets

The following code snippets provide a full end-to-end batch inference example for different models supported by kluster.ai. You can simply copy and paste the snippet into your local environment.

Python
To use these snippets, run the Python script and enter your kluster.ai API key when prompted.

DeepSeek R1
```python
from openai import OpenAI
from getpass import getpass
import json
import time

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-4",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                },
                {
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                },
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
)

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print("Batch status: {}".format(batch_status.status))
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
```

DeepSeek V3
```python
from openai import OpenAI
from getpass import getpass
import json
import time

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-4",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                },
                {
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                },
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
)

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print("Batch status: {}".format(batch_status.status))
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
```

LLama 3.1 8B
```python
from openai import OpenAI
from getpass import getpass
import json
import time

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-4",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                },
                {
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                },
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
)

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print("Batch status: {}".format(batch_status.status))
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
```

LLama 3.1 405B
```python
from openai import OpenAI
from getpass import getpass
import json
import time

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-4",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                },
                {
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                },
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
)

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print("Batch status: {}".format(batch_status.status))
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
```

LLama 3.3 70B
```python
from openai import OpenAI
from getpass import getpass
import json
import time

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-4",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                },
                {
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                },
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
)

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print("Batch status: {}".format(batch_status.status))
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
```

Qwen 2.5 7B
```python
import json
import time
from getpass import getpass

from openai import OpenAI

image1_url="https://github.com/kluster-ai/docs/blob/main/images/get-started/start-building/cat-image.jpg?raw=true"
image2_url="https://github.com/kluster-ai/docs/blob/main/images/get-started/start-building/emoji-image.jpg?raw=true"
image3_url="https://github.com/kluster-ai/docs/blob/main/images/get-started/start-building/parking-image.jpg?raw=true"


# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is this?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image1_url
                            },
                        },
                    ],
                }
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is this?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image2_url
                            },
                        },
                    ],
                }
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-3",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Who can park in the area?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image3_url
                            },
                        },
                    ],
                }
            ],
            "max_completion_tokens": 1000,
        },
    },
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(file=open(file_name, "rb"), purpose="batch")

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print(f"Batch status: {batch_status.status}")
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

print(f"\nImage1 URL: {image1_url}")
print(f"\nImage2 URL: {image2_url}")
print(f"\nImage3 URL: {image3_url}")

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
    print(batch_status)
```

# Batch inference flow＃
This section details the batch inference process using the kluster.ai API and DeepSeek R1 model, but you can adapt it to any of the supported models.

## Create batch jobs as JSON files＃
To begin the batch job workflow, you'll need to assemble your batch requests and add them to a JSON Lines file (.jsonl).

Each request must include the following arguments:

- custom_id string - a unique request ID to match outputs to inputs
- method string - the HTTP method to use for the request. Currently, only POST is supported
- url string -  the /v1/chat/completions endpoint
- body object - a request body containing:
  - model string required - name of one of the supported models
  -  messages array required - a list of chat messages (system, user, or assistant roles, and also image_url for images)
  - Any optional chat completion parameters, such as temperature, max_completion_tokens, etc.

Tip
You can use a different model for each request you submit.

The following examples generate requests and save them in a JSONL file, which is ready to be uploaded for processing.


```python
import time
from getpass import getpass

from openai import OpenAI

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-3",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Who can park in the area?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://github.com/kluster-ai/docs/blob/main/images/get-started/start-building/parking-image.jpg?raw=true"
                            },
                        },
                    ],
                }
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")
```
Warning

For the free tier, the maximum number of batch requests (lines in the JSONL file) must be less than 1000, and each file must not exceed 100 MB. For the standard tier, there is no limit to the number of batch requests, but the maximum batch file size is 100 MB per file.

# Upload batch job files
After you've created the JSON Lines file, you need to upload it using the files endpoint along with the intended purpose. Consequently, you need to set the purpose value to "batch" for batch jobs.

The response will contain an id field; save this value as you'll need it in the next step, where it's referred to as input_file_id. You can view your uploaded files in the Files tab of the kluster.ai platform.

Use the following command examples to upload your batch job files:


```python
# Upload batch job file
batch_input_file = client.files.create(file=open(file_name, "rb"), purpose="batch")

```
Response

```json
{
    "id": "myfile-123",
    "bytes": 2797,
    "created_at": "1733832768",
    "filename": "my_batch_request.jsonl",
    "object": "file",
    "purpose": "batch"
}
```

Warning

Remember that the maximum file size permitted is 100 MB.

# Submit a batch job

Next, submit a batch job by calling the batches endpoint and providing the id of the uploaded batch job file (from the previous section) as the input_file_id, and additional parameters to specify the job's configuration.

The response includes an id that can be used to monitor the job's progress, as demonstrated in the next section.

You can use the following snippets to submit your batch job:

```python
# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

Response

{
    "id": "mybatch-123",
    "completion_window": "24h",
    "created_at": 1733832777,
    "endpoint": "/v1/chat/completions",
    "input_file_id": "myfile-123",
    "object": "batch",
    "status": "validating",
    "cancelled_at": null,
    "cancelling_at": null,
    "completed_at": null,
    "error_file_id": null,
    "errors": null,
    "expired_at": null,
    "expires_at": 1733919177,
    "failed_at": null,
    "finalizing_at": null,
    "in_progress_at": null,
    "metadata": {},
    "output_file_id": null,
    "request_counts": {
        "completed": 0,
        "failed": 0,
        "total": 0
 }
}
```

# Monitor job progress
You can make periodic requests to the batches endpoint to monitor your batch job's progress. Use the id of the batch request from the preceding section as the batch_id to check its status. The job is complete when the status field returns "completed". You can also monitor jobs in the Batch tab of the kluster.ai platform UI.

To see a complete list of the supported statuses, refer to the Retrieve a batch API reference page.

You can use the following snippets to monitor your batch job:


```python
# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print(f"Batch status: {batch_status.status}")
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again
```

Response
```json
{
    "id": "mybatch-123",
    "object": "batch",
    "endpoint": "/v1/chat/completions",
    "errors": null,
    "input_file_id": "myfile-123",
    "completion_window": "24h",
    "status": "completed",
    "output_file_id": "myfile-123-output",
    "error_file_id": null,
    "created_at": "1733832777",
    "in_progress_at": "1733832777",
    "expires_at": "1733919177",
    "finalizing_at": "1733832781",
    "completed_at": "1733832781",
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": null,
    "cancelled_at": null,
    "request_counts": {
        "total": 4,
        "completed": 4,
        "failed": 0
 },
    "metadata": {}
}
```

# Retrieve results
To retrieve the content of your batch jobs output file, send a request to the files endpoint specifying the output_file_id, which is returned from querying the batch's status (from the previous section).

The output file will be a JSONL file, where each line contains the custom_id from your input file request and the corresponding response.

You can use the following snippets to retrieve the results from your batch job:


```python
import json
import time
from getpass import getpass

from openai import OpenAI

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-3",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Who can park in the area?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://github.com/kluster-ai/docs/blob/main/images/get-started/start-building/parking-image.jpg?raw=true"
                            },
                        },
                    ],
                }
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(file=open(file_name, "rb"), purpose="batch")

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print(f"Batch status: {batch_status.status}")
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Save results to a file
    result_file_name = "batch_results.jsonl"
    with open(result_file_name, "wb") as file:
        file.write(results)
    print(f"💾 Response saved to {result_file_name}")
else:
    print(f"Batch failed with status: {batch_status.status}")
```

# List all batch jobs

To list all of your batch jobs, send a request to the batches endpoint without specifying a batch_id. To constrain the query response, you can also use a limit parameter.

You can use the following snippets to list all of your batch jobs:

```python
from openai import OpenAI
from getpass import getpass

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Log all batch jobs (limit to 3)
print(client.batches.list(limit=3).to_dict())
```

Response
```json
{
"object": "list",
"data": [
    {
    "id": "mybatch-123",
    "object": "batch",
    "endpoint": "/v1/chat/completions",
    "errors": null,
    "input_file_id": "myfile-123",
    "completion_window": "24h",
    "status": "completed",
    "output_file_id": "myfile-123-output",
    "error_file_id": null,
    "created_at": "1733832777",
    "in_progress_at": "1733832777",
    "expires_at": "1733919177",
    "finalizing_at": "1733832781",
    "completed_at": "1733832781",
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": null,
    "cancelled_at": null,
    "request_counts": {
        "total": 4,
        "completed": 4,
        "failed": 0
    },
    "metadata": {}
    },
{ ... },
],
"first_id": "mybatch-123",
"last_id": "mybatch-789",
"has_more": false,
"count": 1,
"page": 1,
"page_count": -1,
"items_per_page": 9223372036854775807
}
```

# Cancel a batch job

To cancel a batch job currently in progress, send a request to the cancel endpoint with your batch_id. Note that cancellation may take up to 10 minutes to complete, and the status will show as canceling. Once complete, the status will show as cancelled.

You can use the following snippets to cancel a batch job:

Example

```python
from openai import OpenAI
from getpass import getpass

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Cancel batch job with specified ID
client.batches.cancel("mybatch-123")
```

Response

```json
{
    "id": "mybatch-123",
    "object": "batch",
    "endpoint": "/v1/chat/completions",
    "errors": null,
    "input_file_id": "myfile-123",
    "completion_window": "24h",
    "status": "cancelling",
    "output_file_id": "myfile-123-output",
    "error_file_id": null,
    "created_at": "1730821906",
    "in_progress_at": "1730821911",
    "expires_at": "1730821906",
    "finalizing_at": null,
    "completed_at": null,
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": "1730821906",
    "cancelled_at": null,
    "request_counts": {
        "total": 3,
        "completed": 3,
        "failed": 0
    },
    "metadata": {}
}
```

# Summary
You have now experienced the complete batch inference job lifecycle using kluster.ai's batch API. In this guide, you've learned how to:

- Prepare and submit batch jobs with structured request inputs
- Track your job's progress in real-time
- Retrieve and handle job results
- View and manage your batch jobs
- Cancel jobs when needed
- View supported models

The kluster.ai batch API is designed to efficiently and reliably handle your large-scale LLM workloads. If you have questions or suggestions, the support team would love to hear from you.