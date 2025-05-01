#!/bin/bash
# Claudeモデル名を短縮形から正式名称に置換するスクリプト

# モデル名のマッピング
declare -A model_map=(
    ["claude30h"]="claude-3-haiku-20240307"
    ["claude37s"]="claude-3-7-sonnet-20250219"
    ["claude35s"]="claude-3-5-sonnet-20241022"
    ["claude35h"]="claude-3-5-haiku-20241022"
)

# 結果ファイルのディレクトリ
DIR="results/claude/"

# 各ファイルに対して置換を実行
for file in "$DIR"*.txt; do
    if [ -f "$file" ]; then
        echo "処理中: $file"
        for short_name in "${!model_map[@]}"; do
            sed -i "s/model: $short_name/model: ${model_map[$short_name]}/g" "$file"
        done
    fi
done

echo "すべてのファイルの処理が完了しました。"
