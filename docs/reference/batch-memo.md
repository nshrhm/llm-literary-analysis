



# Claude
https://docs.anthropic.com/en/docs/build-with-claude/batch-processing

# kluster.ai
from openai import OpenAI
# OpenAI compatible API
client = OpenAI(
  base_url="https://api.kluster.ai/v1",
  api_key=YOUR_KLUSTERAI_API_KEY
)
# Upload LLM requests
batch_input_file = client.files.create(
  file=open("batch_1lm_requests.jsonl", "rb"), purpose="batch"
)
# Start adaptive inference
batch_request = client.batches.create(
  input_file_id=batch_input_file.id,
  endpoint="/v1/chat/completions",
  completion_window="24h"
)
# Wait for completion
while client.batches.retrieve(batch_request.id) != "completed":
  time.sleep(60)

# Download results
result_file_id = client.batches.retrieve(batch_request.id).output_file_id
llm_inference_results = client.files.content(result_file_id).content
