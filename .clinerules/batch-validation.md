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

#### OpenAI (48 results)
- Standard models: All fields present
- o3-mini: No temperature field
- o1-mini: Combined system-user content

#### Claude (60 results)
- Content array format
- System role presence
- Message structure

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
        return data
```

### 2. CSV Generation
```python
def generate_csv(results, output_file):
    """Generate CSV with validated results"""
    headers = [
        'timestamp', 'persona', 'model', 'trial',
        'temperature', 'text',
        'Q1value', 'Q2value', 'Q3value', 'Q4value',
        'Q1reason', 'Q2reason', 'Q3reason', 'Q4reason'
    ]
    # Write CSV with validation checks
```

## Validation Results (2025-03-23)

### 1. File Processing
- OpenAI: 48/48 (100% success)
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

2. Processing
   - Validate all fields
   - Check value ranges
   - Verify formats
   - Handle errors gracefully

3. Post-processing
   - Verify CSV output
   - Check result counts
   - Validate aggregations
   - Document issues

## Monitoring

1. Process Metrics
   - Files processed
   - Success rate
   - Error rate
   - Processing time

2. Data Quality
   - Field completeness
   - Value distributions
   - Format consistency
   - Error patterns

3. System Performance
   - Memory usage
   - Processing speed
   - File I/O
   - Error handling
