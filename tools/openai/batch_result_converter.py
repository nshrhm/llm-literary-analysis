"""OpenAI batch results converter."""

import json
import os
import re
from datetime import datetime

def clean_content(content):
    """Clean and normalize content from API response.
    
    Args:
        content (str): Raw content from API response
    
    Returns:
        str: Cleaned and normalized content
    """
    # 空白文字の正規化
    content = content.strip()
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Qセクションの整形
    for i in range(1, 5):
        pattern = f"Q{i}"
        if pattern in content:
            # Qセクションの前に適切な改行を確保
            content = re.sub(f'(?<!\\n)({pattern})', r'\n\1', content)
    
    return content

def convert_batch_results(input_file):
    """Convert batch results from JSONL to individual text files.
    
    Args:
        input_file (str): Path to the input JSONL file
    """
    print(f"Converting batch results from: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Create output directory if not exists
        os.makedirs("results/openai", exist_ok=True)
        
        processed = 0
        for line in lines:
            try:
                # Parse JSONL
                data = json.loads(line)
                
                # Extract data
                custom_id = data['custom_id']
                response = data['response']
                
                if response['status_code'] == 200:
                    # Parse custom_id
                    parts = custom_id.split('_')
                    persona_id = parts[0]
                    model_id = parts[1]
                    text_id = parts[2]
                    trial = parts[3]
                    
                    # Extract and clean content
                    content = response['body']['choices'][0]['message']['content']
                    content = clean_content(content)
                    
                    # Save as text file
                    output_file = f"results/openai/{custom_id}.txt"
                    with open(output_file, "w", encoding='utf-8') as f:
                        # Write metadata
                        f.write(f"timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"persona: {persona_id}\n")
                        f.write(f"model: {model_id}\n")
                        f.write(f"trial: {trial}\n")
                        f.write(f"text: {text_id}\n")
                        f.write(f"temperature: None\n")  # reasoningタイプのモデルの場合
                        f.write(f"\n{content}\n")
                    
                    processed += 1
                    print(f"Processed: {custom_id}")
                        
            except Exception as e:
                print(f"Error processing response for {custom_id}: {str(e)}")
                continue
                
        print(f"\nConversion completed. {processed} files generated.")
                
    except Exception as e:
        raise Exception(f"Error reading batch results file: {str(e)}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python batch_result_converter.py <input_jsonl_file>")
        sys.exit(1)
        
    convert_batch_results(sys.argv[1])
