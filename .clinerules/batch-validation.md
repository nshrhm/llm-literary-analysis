# Batch Result Validation Guide

## Validation Standards

### 1. File Format Validation

#### Result Files
```
results/
├── openai/
├── claude/
├── gemini/
├── grok/
├── deepseek/
└── llama/
    └── p{persona}_{model}_n{trial}_temp{temp}_{text}.txt
```

Validation Points:
- Filename format
- Directory structure
- File permissions
- Character encoding (UTF-8)

### 2. Content Validation

#### Required Fields
```
timestamp: [YYYY-MM-DD HH:MM:SS]
persona: [Persona name]
model: [Model name]
trial: [Trial number]
temperature: [Temperature value]
text: [Text name]
pricing: {  # 2025-04-17追加：GPT-4.1シリーズ用
  "input": [rate],
  "cached_input": [rate],
  "output": [rate]
}
Q1value: [0-100]
Q1reason: [Explanation]
Q2value: [0-100]
Q2reason: [Explanation]
Q3value: [0-100]
Q3reason: [Explanation]
Q4value: [0-100]
Q4reason: [Explanation]
```

Validation Points:
- Field presence
- Value ranges
- Format consistency
- Text encoding

### 3. Model-Specific Validation

#### OpenAI (408 results)（2025-04-17更新）
1. GPT-4.1シリーズ（360結果）：
   - 3モデル × 4ペルソナ × 3テキスト × 10トライアル
   - 価格情報の検証（input/cached_input/output rates）
   - バッチ処理のコスト削減効果（50%）
   - パターンマッチング成功率
   - エラー回復効率

2. 従来モデル（48結果）：
   - Standard models: All fields present
   - o3-mini: No temperature field
   - o1-mini: Combined system-user content

#### Claude (60 results)
- Content array format
- System role presence
- Message structure
- Temperature support (0.0-1.0)
- Batch processing検証:
  - リクエスト数: 最大100,000
  - バッチサイズ: 最大256MB
  - 処理時間: 24時間以内
  - 結果保持: 29日間
- Prompt caching検証:
  - キャッシュヒット率
  - コスト削減効果

#### Gemini (83 results)
- GenerationConfig usage
- Temperature parameter
- Response format

#### Grok (12 results)
- X.AI API format
- Message structure
- Response parsing

#### DeepSeek (24 results)
- Kluster.ai format
- Response structure
- Unicode handling

#### Llama (36 results)
- Kluster.ai format
- Message compatibility
- Response parsing

## Aggregation Process

### 1. Data Collection
```python
def process_file(filepath):
    """Process and validate individual result file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = {}
        # Field extraction and validation
        # Format verification
        # Value range checking
        # 2025-04-17追加：価格情報の検証
        if "pricing" in data:
            validate_pricing_info(data["pricing"])
        return data
```

### 2. CSV Generation
```python
def generate_csv(results, output_file):
    """Generate CSV with validated results"""
    headers = [
        'timestamp', 'persona', 'model', 'trial',
        'temperature', 'text',
        'pricing_input', 'pricing_cached_input', 'pricing_output',  # 2025-04-17追加
        'Q1value', 'Q2value', 'Q3value', 'Q4value',
        'Q1reason', 'Q2reason', 'Q3reason', 'Q4reason'
    ]
    # Write CSV with validation checks
```

## Validation Results (2025-04-17更新)

### 1. File Processing
- OpenAI: 408/408 (100% success)
  - GPT-4.1シリーズ: 360/360 (100% success)
  - 従来モデル: 48/48 (100% success)
- Claude: 60/60 (100% success)
- Gemini: 83/83 (100% success)
- Grok: 12/12 (100% success)
- DeepSeek: 24/24 (100% success)
- Llama: 36/36 (100% success)

### 2. Data Validation
- Metadata: 100% valid
- Q-values: All within 0-100 range
- Reasons: All properly formatted
- Unicode: No encoding issues
- Pricing: 100% valid（GPT-4.1シリーズ）

### 3. Output Files
```
aggregated_results/
├── aggregated_openai_[timestamp].csv
├── aggregated_claude_[timestamp].csv
├── aggregated_gemini_[timestamp].csv
├── aggregated_grok_[timestamp].csv
├── aggregated_deepseek_[timestamp].csv
└── aggregated_llama_[timestamp].csv
```

## Error Handling

### 1. File Errors
- Missing files
- Invalid permissions
- Encoding issues
- Directory structure

### 2. Content Errors
- Missing fields
- Invalid values
- Format inconsistencies
- Unicode problems
- Pricing validation errors（2025-04-17追加）

### 3. Processing Errors
- CSV writing failures
- Memory constraints
- Performance issues
- System errors

## Best Practices

1. Pre-processing
   - Check file existence
   - Validate permissions
   - Verify encoding
   - Check structure
   - Verify pricing format（2025-04-17追加）

2. Processing
   - Validate all fields
   - Check value ranges
   - Verify formats
   - Handle errors gracefully
   - Process pricing data（2025-04-17追加）

3. Post-processing
   - Verify CSV output
   - Check result counts
   - Validate aggregations
   - Document issues
   - Confirm cost calculations（2025-04-17追加）

## Monitoring

1. Process Metrics
   - Files processed
   - Success rate
   - Error rate
   - Processing time
   - Cost efficiency（2025-04-17追加）

2. Data Quality
   - Field completeness
   - Value distributions
   - Format consistency
   - Error patterns
   - Pricing accuracy（2025-04-17追加）

3. System Performance
   - Memory usage
   - Processing speed
   - File I/O
   - Error handling
   - Batch optimization（2025-04-17追加）
