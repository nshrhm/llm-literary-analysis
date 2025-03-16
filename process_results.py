import os
import csv
import re

def extract_q_value(line):
    # Extract numeric value from Q1-Q4 lines, handling different formats
    match = re.search(r'Q\d.*?(\d+)', line)
    if match:
        return int(match.group(1))
    return None

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    data = {
        'persona': None,
        'text': None,
        'model': None,
        'trial': None,
        'temperature': None,
        'timestamp': None,
        'Q1': None,
        'Q2': None,
        'Q3': None,
        'Q4': None,
        'comment': ''
    }
    
    response_started = False
    comment_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Get timestamp from first line
        if i == 0 and line.startswith('timestamp:'):
            data['timestamp'] = line.replace('timestamp:', '').strip()
        elif i == 1 and line.startswith('persona:'):
            data['persona'] = line.replace('persona:', '').strip()
        elif i == 2 and line.startswith('text:'):
            data['text'] = line.replace('text:', '').strip()
        elif i == 3 and line.startswith('model:'):
            data['model'] = line.replace('model:', '').strip()
        elif line.startswith('trial:'):
            data['trial'] = line.replace('trial:', '').strip()
        elif line.startswith('temperature:'):
            data['temperature'] = line.replace('temperature:', '').strip()
        
        if line.lower() == 'response:':
            response_started = True
            continue
            
        if response_started:
            if line.startswith('Q1'):
                data['Q1'] = extract_q_value(line)
            elif line.startswith('Q2'):
                data['Q2'] = extract_q_value(line)
            elif line.startswith('Q3'):
                data['Q3'] = extract_q_value(line)
            elif line.startswith('Q4'):
                data['Q4'] = extract_q_value(line)
            elif line and not any(line.startswith(f'Q{i}') for i in range(1, 5)):
                if line.strip():  # Only add non-empty lines
                    comment_lines.append(line.strip())
    
    data['comment'] = ' '.join(comment_lines)
    return data

def main():
    # Create/overwrite the CSV file with headers
    headers = ['persona', 'text', 'model', 'trial', 'temperature', 
              'Q1', 'Q2', 'Q3', 'Q4', 'timestamp', 'comment']
    
    file_count = 0
    success_count = 0
    error_count = 0
    
    with open('result_gemini.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        # Process all .txt files
        for filename in sorted(os.listdir('.')):
            if filename.endswith('.txt'):
                file_count += 1
                try:
                    data = process_file(filename)
                    writer.writerow(data)
                    success_count += 1
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    error_count += 1
    
    print(f"\nProcessing complete!")
    print(f"Total files processed: {file_count}")
    print(f"Successfully processed: {success_count}")
    print(f"Errors encountered: {error_count}")

if __name__ == '__main__':
    main()
