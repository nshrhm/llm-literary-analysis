"""Tests for batch result converter."""

import os
import json
import pytest
from datetime import datetime
from ..batch_result_converter import (
    clean_content, 
    extract_value,
    extract_reason,
    validate_response,
    get_model_pricing,
    write_result_file,
    convert_batch_results
)

def test_clean_content():
    """Test content cleaning functionality."""
    input_content = "Q1\n\n\ntest\nQ2\ntest"
    expected = "Q1\n\ntest\nQ2\ntest"
    assert clean_content(input_content) == expected

def test_extract_value():
    """Test value extraction with different patterns."""
    test_cases = [
        ("Q1. 面白さ(数値): 80", "面白さ", "80", "pattern_1"),  # 標準形式
        ("Q1. 面白さ: (数値): 80", "面白さ", "80", "pattern_2"),  # 代替形式1
        ("Q1. 面白さ 数値: 80", "面白さ", "80", "pattern_3"),  # 代替形式2
        ("Q1. 面白さ: 80", "面白さ", "80", "pattern_4"),  # シンプル形式
        ("面白さの評価: 80", "面白さ", "80", "pattern_5"),  # 日本語形式1
        ("面白さレベル: 80", "面白さ", "80", "pattern_6"),  # 日本語形式2
        ("「面白さ」: 80", "面白さ", "80", "pattern_7"),  # 括弧形式
        ("[面白さ]: 80", "面白さ", "80", "pattern_8")  # 角括弧形式
    ]
    
    for content, question, expected_value, expected_pattern in test_cases:
        value, pattern = extract_value(content, question)
        assert value == expected_value
        assert pattern == expected_pattern

def test_write_result_file(tmp_path):
    """Test result file writing with the new metadata order."""
    output_file = tmp_path / "test_output.txt"
    metadata = {
        "text": "t1",
        "model": "gpt-4.1",
        "persona": "p1",
        "trial": "1",
        "temperature": None
    }
    content = "Test content"
    validation_info = {
        "values": {"面白さ": "80"},
        "reasons": {"面白さ": "理由"},
        "patterns": {"面白さ": "pattern_1"}
    }

    # Write test file
    write_result_file(str(output_file), metadata, content, validation_info)

    # Read and verify content
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Verify metadata order and format
    assert "text: t1" in lines[1]
    assert "model: gpt-4.1" in lines[2]
    assert "persona: p1" in lines[3]
    assert "trial: 1" in lines[4]  # 試行番号の確認
    assert "temperature: None" in lines[5]

    # Verify pattern_matching section is not present
    content = '\n'.join(lines)
    assert "pattern_matching:" not in content

def test_convert_batch_results_new_format(tmp_path):
    """Test batch conversion with new file name format."""
    # Create test input files with different trial numbers
    input_file = tmp_path / "test_batch.jsonl"
    test_data = [
        {
            "custom_id": "t1_gpt-4o_p1_temp50_n01",  # temperatureあり、nプレフィックス付き
            "response": {
                "status_code": 200,
                "body": {
                    "choices": [{
                        "message": {
                            "content": "Q1. 面白さ(数値): 80\nQ1. 面白さ(理由): テスト"
                        }
                    }]
                }
            }
        },
        {
            "custom_id": "t2_gpt-4o_p2_temp--_n10",  # temperatureなし、nプレフィックス付き
            "response": {
                "status_code": 200,
                "body": {
                    "choices": [{
                        "message": {
                            "content": "Q1. 面白さ(数値): 70\nQ1. 面白さ(理由): テスト2"
                        }
                    }]
                }
            }
        }
    ]
    
    with open(input_file, 'w', encoding='utf-8') as f:
        for data in test_data:
            json.dump(data, f)
            f.write('\n')

    # Create results directory
    results_dir = tmp_path / "results" / "openai"
    os.makedirs(results_dir)

    # Run conversion
    convert_batch_results(str(input_file))

    # Verify output files exist and check their content
    for data in test_data:
        output_file = results_dir / f"{data['custom_id']}.txt"
        assert output_file.exists()

        # Read content
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Check trial number format
            trial_num = data['custom_id'].split('_')[-1]
            if trial_num.startswith('n'):
                trial_num = trial_num[1:]
            assert f"trial: {int(trial_num)}" in content

            # Check temperature handling
            temp_part = data['custom_id'].split('_')[3]
            if temp_part == "temp--":
                assert "temperature: None" in content
            elif temp_part.startswith("temp"):
                temp_value = float(temp_part[4:]) / 100
                assert f"temperature: {temp_value}" in content

            # Verify pattern_matching section is not present
            assert "pattern_matching:" not in content

def test_get_model_pricing():
    """Test GPT-4.1 series pricing retrieval."""
    # Test GPT-4.1
    pricing = get_model_pricing("gpt-4.1")
    assert pricing["input"] == 2.00
    assert pricing["cached_input"] == 0.50
    assert pricing["output"] == 8.00
    
    # Test GPT-4.1-mini
    pricing = get_model_pricing("gpt-4.1-mini")
    assert pricing["input"] == 0.40
    assert pricing["cached_input"] == 0.10
    assert pricing["output"] == 1.60
    
    # Test GPT-4.1-nano
    pricing = get_model_pricing("gpt-4.1-nano")
    assert pricing["input"] == 0.10
    assert pricing["cached_input"] == 0.025
    assert pricing["output"] == 0.40
    
    # Test non-GPT-4.1 model
    assert get_model_pricing("other-model") is None
