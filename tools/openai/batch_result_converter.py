"""OpenAI batch results converter with enhanced pattern matching and GPT-4.1 series support."""

import json
import os
import re
from datetime import datetime
from typing import Dict, Optional, List, Tuple

def create_patterns(question: str) -> List[str]:
    """Create list of patterns for matching response values.
    
    Args:
        question (str): Question type (面白さ、驚き、etc.)
    
    Returns:
        List[str]: List of regex patterns
    """
    return [
        rf"Q\d+\.\s*{question}\(数値\):\s*(\d+)",  # 標準形式
        rf"Q\d+\.\s*{question}:\s*\(数値\):\s*(\d+)",  # 代替形式1
        rf"Q\d+\.\s*{question}\s*数値:\s*(\d+)",  # 代替形式2
        rf"Q\d+\.\s*{question}:\s*(\d+)",  # シンプル形式
        rf"{question}(?:の評価)?(?:\s*[:：]\s*|\s+)(\d+)",  # 日本語形式1
        rf"{question}(?:度|レベル)(?:\s*[:：]\s*|\s+)(\d+)",  # 日本語形式2
        rf"「{question}」\s*[:：]?\s*(\d+)",  # 括弧形式
        rf"\[{question}\]\s*[:：]?\s*(\d+)"  # 角括弧形式
    ]

def extract_value(content: str, question: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract value and used pattern from content.
    
    Args:
        content (str): Response content
        question (str): Question type
    
    Returns:
        Tuple[Optional[str], Optional[str]]: (value, pattern_used)
    """
    patterns = create_patterns(question)
    for i, pattern in enumerate(patterns):
        if match := re.search(pattern, content, re.MULTILINE):
            return match.group(1), f"pattern_{i+1}"
    return None, None

def extract_reason(content: str, question: str) -> Optional[str]:
    """Extract reason from content.
    
    Args:
        content (str): Response content
        question (str): Question type
    
    Returns:
        Optional[str]: Extracted reason
    """
    reason_patterns = [
        rf"Q\d+\.\s*{question}\(理由\):\s*(.+?)(?=(?:\n[QA]|$))",
        rf"Q\d+\.\s*{question}:\s*\(理由\):\s*(.+?)(?=(?:\n[QA]|$))",
        rf"Q\d+\.\s*{question}\s*理由:\s*(.+?)(?=(?:\n[QA]|$))",
        rf"{question}(?:の)?理由:\s*(.+?)(?=(?:\n|$))"
    ]
    
    for pattern in reason_patterns:
        if match := re.search(pattern, content, re.MULTILINE):
            return match.group(1).strip()
    return None

def clean_content(content: str) -> str:
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
            content = re.sub(f'(?<!\\n)({pattern})', r'\n\1', content)
    
    return content

def get_model_pricing(model: str) -> Optional[Dict]:
    """Get pricing information for GPT-4.1 series models.
    
    Args:
        model (str): Model identifier
    
    Returns:
        Optional[Dict]: Pricing information if available
    """
    pricing = {
        "gpt-4.1": {
            "input": 2.00,
            "cached_input": 0.50,
            "output": 8.00
        },
        "gpt-4.1-mini": {
            "input": 0.40,
            "cached_input": 0.10,
            "output": 1.60
        },
        "gpt-4.1-nano": {
            "input": 0.10,
            "cached_input": 0.025,
            "output": 0.40
        }
    }
    return pricing.get(model)

def validate_response(content: str) -> Tuple[bool, Dict]:
    """Validate response content and extract values.
    
    Args:
        content (str): Response content
    
    Returns:
        Tuple[bool, Dict]: (is_valid, validation_info)
    """
    questions = ["面白さ", "驚き", "悲しみ", "怒り"]
    validation_info = {
        "values": {},
        "reasons": {},
        "patterns": {},
        "is_complete": True
    }
    
    for q in questions:
        value, pattern = extract_value(content, q)
        reason = extract_reason(content, q)
        
        if not value or not (0 <= int(value) <= 100):
            validation_info["is_complete"] = False
        if not reason:
            validation_info["is_complete"] = False
            
        validation_info["values"][q] = value
        validation_info["reasons"][q] = reason
        validation_info["patterns"][q] = pattern
    
    return validation_info["is_complete"], validation_info

def write_result_file(output_file: str, metadata: Dict, content: str, validation_info: Dict):
    """Write result to file with metadata and validation info.
    
    Args:
        output_file (str): Output file path
        metadata (Dict): Metadata information
        content (str): Original content
        validation_info (Dict): Validation information
    """
    with open(output_file, "w", encoding='utf-8') as f:
        # Write metadata in specified order (text, model, persona, temperature, trial)
        f.write(f"timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"text: {metadata['text']}\n")
        f.write(f"model: {metadata['model']}\n")
        f.write(f"persona: {metadata['persona']}\n")
        f.write(f"trial: {metadata['trial']}\n")  # Add trial information
        
        # Write temperature and pricing info for GPT-4.1 series
        if pricing := get_model_pricing(metadata['model']):
            f.write(f"temperature: {metadata.get('temperature', '0.7')}\n")  # Default to 0.7
            f.write(f"pricing: {json.dumps(pricing, indent=2)}\n")
        else:
            f.write(f"temperature: None\n")  # reasoningタイプのモデル
        
        # Write content
        f.write(f"\n{content}\n")

def convert_batch_results(input_file: str):
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
        validation_stats = {"success": 0, "partial": 0, "failed": 0}
        
        for line in lines:
            try:
                # Parse JSONL
                data = json.loads(line)
                custom_id = data['custom_id']
                response = data['response']
                
                if response['status_code'] == 200:
                    # Parse custom_id (format: text_model_persona_temp{temp}_trial)
                    parts = custom_id.split('_')
                    metadata = {
                        "text": parts[0],
                        "model": parts[1],
                        "persona": parts[2]
                    }
                    
                    # Parse temperature and trial
                    if len(parts) >= 5:
                        temp_part = parts[3]
                        # Handle temperature (format: temp50 or temp--)
                        if temp_part.startswith("temp"):
                            if temp_part == "temp--":
                                metadata["temperature"] = None
                            else:
                                metadata["temperature"] = float(temp_part[4:]) / 100
                        # Handle trial number (both "01" and "n01" formats)
                        trial_num = parts[4]
                        if trial_num.startswith('n'):
                            trial_num = trial_num[1:]  # Remove 'n' prefix
                        metadata["trial"] = str(int(trial_num))  # Convert to integer string (e.g., "01" → "1")
                    
                    # Extract and clean content
                    content = response['body']['choices'][0]['message']['content']
                    content = clean_content(content)
                    
                    # Validate response
                    is_valid, validation_info = validate_response(content)
                    
                    # Save as text file
                    output_file = f"results/openai/{custom_id}.txt"
                    write_result_file(output_file, metadata, content, validation_info)
                    
                    # Update stats
                    if is_valid:
                        validation_stats["success"] += 1
                    else:
                        validation_stats["partial"] += 1
                    
                    processed += 1
                    print(f"Processed: {custom_id} (Valid: {is_valid})")
                        
            except Exception as e:
                validation_stats["failed"] += 1
                print(f"Error processing response for {custom_id}: {str(e)}")
                continue
        
        # Print summary
        print(f"\nConversion completed:")
        print(f"- Files generated: {processed}")
        print(f"- Fully valid: {validation_stats['success']}")
        print(f"- Partially valid: {validation_stats['partial']}")
        print(f"- Failed: {validation_stats['failed']}")
                
    except Exception as e:
        raise Exception(f"Error reading batch results file: {str(e)}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python batch_result_converter.py <input_jsonl_file>")
        sys.exit(1)
        
    convert_batch_results(sys.argv[1])
