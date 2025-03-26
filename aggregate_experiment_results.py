import os
import csv
import re
import argparse
from datetime import datetime
from pathlib import Path

def extract_q_data(line):
    """Extract Q value and reason from Q lines"""
    # 数値を抽出するパターン
    patterns = [
        r'Q\d+\.\s*[^(]+\(数値\):\s*(\d+)',          # Q1. 面白さ(数値): 80
        r'Q\d+\.\s*[^:]+:\s*\(数値\):\s*(\d+)',      # Q1. 面白さ: (数値): 80
        r'Q\d+\.\s*[^:]+数値:\s*(\d+)',              # Q1. 面白さ 数値: 80
        r'Q\d+\.\s*[^:]+:\s*(\d+)',                  # Q1. 面白さ: 80
        r'Q\d+value:\s*(\d+)'                        # 従来形式も残す
    ]
    
    # 理由を抽出するパターン
    reason_patterns = [
        r'Q\d+\.\s*[^(]+\(理由\):\s*(.+)',          # Q1. 面白さ(理由): [理由]
        r'Q\d+\.\s*[^:]+:\s*\(理由\):\s*(.+)',      # Q1. 面白さ: (理由): [理由]
        r'Q\d+\.\s*[^:]+理由:\s*(.+)',              # Q1. 面白さ 理由: [理由]
        r'Q\d+reason:\s*(.+)'                       # 従来形式も残す
    ]
    
    # 数値の抽出を試みる
    for pattern in patterns:
        value_match = re.search(pattern, line)
        if value_match:
            return int(value_match.group(1))
    
    # 理由の抽出を試みる
    for pattern in reason_patterns:
        reason_match = re.search(pattern, line)
        if reason_match:
            return reason_match.group(1).strip()
    
    return None

def process_file(filepath):
    """Process a single result file and extract relevant data"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        data = {
            'timestamp': None,
            'persona': None,
            'model': None,
            'trial': None,
            'temperature': None,
            'text': None,
            'Q1value': None,
            'Q2value': None,
            'Q3value': None,
            'Q4value': None,
            'Q1reason': None,
            'Q2reason': None,
            'Q3reason': None,
            'Q4reason': None
        }
        
        current_q = None
        
        for line in lines:
            line = line.strip()
            
            # メタデータの抽出
            if line.startswith('timestamp:'):
                data['timestamp'] = line.replace('timestamp:', '').strip()
            elif line.startswith('persona:'):
                data['persona'] = line.replace('persona:', '').strip()
            elif line.startswith('text:'):
                data['text'] = line.replace('text:', '').strip()
            elif line.startswith('model:'):
                # モデル名を正規化
                model = line.replace('model:', '').strip()
                # DeepSeekモデルの場合、完全な名前を使用
                if model.startswith('DeepSeek'):
                    data['model'] = model
                else:
                    data['model'] = model.split('/')[-1] if '/' in model else model
            elif line.startswith('trial:'):
                data['trial'] = line.replace('trial:', '').strip()
            elif line.startswith('temperature:'):
                data['temperature'] = line.replace('temperature:', '').strip()
            elif line.startswith('Q'):
                # Q1-Q4の数値の抽出
                for i in range(1, 5):
                    if line.startswith(f'Q{i}'):
                        if '数値' in line or 'value' in line.lower():
                            data[f'Q{i}value'] = extract_q_data(line)
                        elif '理由' in line or 'reason' in line.lower():
                            data[f'Q{i}reason'] = extract_q_data(line)
        
        return data
    except Exception as e:
        raise Exception(f"Error processing {filepath}: {str(e)}")

def generate_output_filename(input_dir, prefix="aggregated"):
    """Generate output filename with timestamp and input directory name"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = os.path.basename(os.path.abspath(input_dir))
    return f"{prefix}_{dir_name}_{timestamp}.csv"

def main():
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser(description='Aggregate experiment results from text files into CSV')
    parser.add_argument('input_dir', help='Directory containing result text files')
    parser.add_argument('--output-dir', default='.',
                      help='Directory for output CSV file (default: current directory)')
    parser.add_argument('--pattern', default='*.txt',
                      help='File pattern to match (default: *.txt)')
    args = parser.parse_args()

    # 入出力パスの設定
    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 出力ファイル名の生成
    output_file = output_path / generate_output_filename(args.input_dir)
    
    # CSVヘッダーの設定
    headers = ['timestamp', 'persona', 'model', 'trial', 'temperature', 'text',
              'Q1value', 'Q2value', 'Q3value', 'Q4value',
              'Q1reason', 'Q2reason', 'Q3reason', 'Q4reason']
    
    # 処理状況のカウンター初期化
    file_count = 0
    success_count = 0
    error_count = 0
    errors = []
    
    print(f"\n結果ファイルの集計を開始します...")
    print(f"入力ディレクトリ: {input_path}")
    print(f"出力ファイル: {output_file}\n")
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        # 再帰的にファイルを処理
        for filepath in input_path.rglob(args.pattern):
            file_count += 1
            try:
                print(f"処理中: {filepath.name}")
                data = process_file(filepath)
                writer.writerow(data)
                success_count += 1
            except Exception as e:
                print(f"エラー: {str(e)}")
                errors.append(f"{filepath.name}: {str(e)}")
                error_count += 1
    
    # 結果サマリーの表示
    print(f"\n処理完了!")
    print(f"合計処理ファイル数: {file_count}")
    print(f"正常処理: {success_count}")
    print(f"エラー: {error_count}")
    
    if errors:
        print("\nエラー詳細:")
        for error in errors:
            print(f"- {error}")
    
    print(f"\n集計結果: {output_file}")

if __name__ == '__main__':
    main()
