import os
import csv
import re
import argparse
from datetime import datetime
from pathlib import Path

def extract_q_data(text, line_index=None):
    """Extract Q value and reason from text content.
    
    Args:
        text (str): Full text content or single line
        line_index (int, optional): Current line index for context
    
    Returns:
        Union[int, str, None]: Extracted value or reason
    """
    # 数値を抽出するパターン
    patterns = [
        r'Q\d+\.\s*[^(]+\(数値\):\s*(\d+)',          # Q1. 面白さ(数値): 80
        r'Q\d+\.\s*[^:]+:\s*\(数値\):\s*(\d+)',      # Q1. 面白さ: (数値): 80
        r'Q\d+\.\s*[^:]+数値:\s*(\d+)',              # Q1. 面白さ 数値: 80
        r'Q\d+\.\s*[^:]+:\s*(\d+)',                  # Q1. 面白さ: 80
        r'Q\d+value:\s*(\d+)'                        # 従来形式も残す
    ]
    
    # 理由を抽出するパターン（改行を含む可能性を考慮）
    reason_patterns = [
        r'Q\d+\.\s*[^(]+\(理由\):\s*(.+?)(?=(?:\n\s*Q\d|$))',  # 次のQまたは終端までマッチ
        r'Q\d+\.\s*[^:]+:\s*\(理由\):\s*(.+?)(?=(?:\n\s*Q\d|$))',
        r'Q\d+\.\s*[^:]+理由:\s*(.+?)(?=(?:\n\s*Q\d|$))',
        r'Q\d+reason:\s*(.+?)(?=(?:\n\s*Q\d|$))'
    ]
    
    # 数値の抽出を試みる
    for pattern in patterns:
        value_match = re.search(pattern, text, re.MULTILINE)
        if value_match:
            return int(value_match.group(1))
    
    # 理由の抽出を試みる（改行を含む可能性を考慮）
    for pattern in reason_patterns:
        reason_match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if reason_match:
            # 余分な改行と空白を削除して正規化
            reason = reason_match.group(1).strip()
            reason = re.sub(r'\s+', ' ', reason)
            return reason
    
    return None

def process_file(filepath):
    """Process a single result file and extract relevant data"""
    try:
        # ファイル全体を一度に読み込む
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 行ごとの処理用に分割
        lines = content.splitlines()
        
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
        
        # メタデータの処理
        for line in lines:
            line = line.strip()
            
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
        
        # Q1-Q4の数値と理由の抽出（ファイル全体から）
        for i in range(1, 5):
            # 数値の抽出（行単位）
            for line in lines:
                if line.startswith(f'Q{i}') and ('数値' in line or 'value' in line.lower()):
                    data[f'Q{i}value'] = extract_q_data(line)
                    break
            
            # 理由の抽出（複数行対応）
            for pattern in [
                f'Q{i}\\.[^(]+\\(理由\\):[^\\n]*(?:\\n(?!Q\\d)[^\\n]*)*',  # 標準形式
                f'Q{i}\\.[^:]+:\\s*\\(理由\\):[^\\n]*(?:\\n(?!Q\\d)[^\\n]*)*',  # 代替形式1
                f'Q{i}\\.[^:]+理由:[^\\n]*(?:\\n(?!Q\\d)[^\\n]*)*',  # 代替形式2
                f'Q{i}reason:[^\\n]*(?:\\n(?!Q\\d)[^\\n]*)*'  # 従来形式
            ]:
                match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
                if match:
                    reason_text = match.group(0)
                    data[f'Q{i}reason'] = extract_q_data(reason_text)
                    break
        
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
