#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_batch_cleanup.py: Test cases for batch cleanup tools.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..batch_cleanup import BatchCleanup

class TestBatchCleanup(unittest.TestCase):
    """BatchCleanupクラスのテストケース"""

    def setUp(self):
        """各テストの前処理"""
        # OpenAI クライアントのモック
        self.mock_client = MagicMock()
        patcher = patch('openai.OpenAI', return_value=self.mock_client)
        patcher.start()
        self.cleanup = BatchCleanup(api_key="test_key")
        self.cleanup.client = self.mock_client

    def test_delete_file_success(self):
        """ファイル削除成功のテスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.deleted = True
        self.mock_client.files.delete.return_value = mock_response

        # テスト実行
        result = self.cleanup._delete_file("file-123")
        self.assertTrue(result)

    def test_delete_file_failure(self):
        """ファイル削除失敗のテスト"""
        # モックの設定
        self.mock_client.files.delete.side_effect = Exception("API error")

        # テスト実行
        result = self.cleanup._delete_file("file-123")
        self.assertFalse(result)

    def test_cancel_batch_success(self):
        """バッチキャンセル成功のテスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status = "cancelling"
        self.mock_client.batches.cancel.return_value = mock_response

        # テスト実行
        result = self.cleanup._cancel_batch("batch-123")
        self.assertTrue(result)

    def test_delete_batch_success(self):
        """バッチ削除成功のテスト"""
        # モックの設定
        mock_batch = MagicMock()
        mock_batch.status = "completed"
        mock_batch.input_file_id = "file-1"
        mock_batch.output_file_id = "file-2"
        mock_batch.error_file_id = "file-3"
        self.mock_client.batches.retrieve.return_value = mock_batch

        mock_delete = MagicMock()
        mock_delete.deleted = True
        self.mock_client.files.delete.return_value = mock_delete

        # テスト実行
        result = self.cleanup.delete_batch("batch-123")
        self.assertTrue(result)

    def test_delete_all_batches(self):
        """全バッチ削除のテスト"""
        # モックの設定
        mock_batch1 = MagicMock()
        mock_batch1.id = "batch-1"
        mock_batch2 = MagicMock()
        mock_batch2.id = "batch-2"

        mock_list = MagicMock()
        mock_list.data = [mock_batch1, mock_batch2]
        self.mock_client.batches.list.return_value = mock_list

        # delete_batchメソッドをモック化
        with patch.object(BatchCleanup, 'delete_batch', return_value=True) as mock_delete:
            results = self.cleanup.delete_all_batches()

        # 検証
        self.assertEqual(len(results["success"]), 2)
        self.assertEqual(len(results["failed"]), 0)
        self.assertEqual(mock_delete.call_count, 2)

if __name__ == '__main__':
    unittest.main()
