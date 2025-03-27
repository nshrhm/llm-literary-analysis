#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
batch_cleanup.py: Tools for managing OpenAI batch jobs and cleaning up resources.
"""

import os
import time
from typing import List, Optional, Dict
import logging
from openai import OpenAI

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BatchCleanup:
    """OpenAIバッチジョブのクリーンアップツール"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー（未指定の場合は環境変数から取得）
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        if not api_key and not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY must be provided")

    def _delete_file(self, file_id: str) -> bool:
        """
        ファイルを削除
        
        Args:
            file_id: 削除するファイルのID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            response = self.client.files.delete(file_id)
            return response.deleted
        except Exception as e:
            logger.error(f"Error deleting file {file_id}: {e}")
            return False

    def _cancel_batch(self, batch_id: str) -> bool:
        """
        バッチをキャンセル
        
        Args:
            batch_id: キャンセルするバッチのID
            
        Returns:
            bool: キャンセルが成功したかどうか
        """
        try:
            batch = self.client.batches.cancel(batch_id)
            return batch.status in ["cancelling", "cancelled"]
        except Exception as e:
            logger.error(f"Error cancelling batch {batch_id}: {e}")
            return False

    def delete_batch(self, batch_id: str) -> bool:
        """
        指定されたバッチと関連リソースを削除
        
        Args:
            batch_id: 削除するバッチのID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        logger.info(f"Starting cleanup for batch {batch_id}")
        
        try:
            # バッチ情報を取得
            batch = self.client.batches.retrieve(batch_id)
            
            # 進行中のバッチをキャンセル
            if batch.status in ["validating", "in_progress"]:
                if not self._cancel_batch(batch_id):
                    logger.error(f"Failed to cancel batch {batch_id}")
                    return False
                # キャンセル完了を待機（最大60秒）
                for _ in range(12):  # 5秒 × 12 = 60秒
                    time.sleep(5)
                    batch = self.client.batches.retrieve(batch_id)
                    if batch.status in ["cancelled", "completed", "failed"]:
                        break
            
            # 関連ファイルを削除
            files_to_delete = [
                (batch.input_file_id, "input file"),
                (batch.output_file_id, "output file"),
                (batch.error_file_id, "error file")
            ]
            
            success = True
            for file_id, file_type in files_to_delete:
                if file_id:
                    if self._delete_file(file_id):
                        logger.info(f"Successfully deleted {file_type} {file_id}")
                    else:
                        logger.error(f"Failed to delete {file_type} {file_id}")
                        success = False
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing batch {batch_id}: {e}")
            return False

    def delete_all_batches(self, limit: int = 100) -> Dict[str, List[str]]:
        """
        すべてのバッチと関連リソースを削除
        
        Args:
            limit: 一度に処理するバッチの最大数
            
        Returns:
            Dict[str, List[str]]: 成功・失敗したバッチIDのリスト
        """
        logger.info("Starting cleanup of all batches")
        
        results = {
            "success": [],
            "failed": []
        }
        
        try:
            # バッチ一覧を取得
            batches = self.client.batches.list(limit=limit)
            total_batches = len(batches.data)
            logger.info(f"Found {total_batches} batches to process")
            
            # 各バッチを処理
            for i, batch in enumerate(batches.data, 1):
                batch_id = batch.id
                logger.info(f"Processing batch {i}/{total_batches}: {batch_id}")
                
                if self.delete_batch(batch_id):
                    results["success"].append(batch_id)
                    logger.info(f"Successfully cleaned up batch {batch_id}")
                else:
                    results["failed"].append(batch_id)
                    logger.error(f"Failed to clean up batch {batch_id}")
                
                # レート制限を考慮して待機
                if i < total_batches:
                    time.sleep(1)
            
            return results
            
        except Exception as e:
            logger.error(f"Error listing batches: {e}")
            return results

def main():
    """メイン実行関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenAI Batch Cleanup Tool")
    parser.add_argument("--batch-id", help="Specific batch ID to clean up")
    parser.add_argument("--all", action="store_true", help="Clean up all batches")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of batches to process")
    args = parser.parse_args()
    
    try:
        cleanup = BatchCleanup()
        
        if args.batch_id:
            # 特定のバッチを削除
            if cleanup.delete_batch(args.batch_id):
                logger.info(f"Successfully cleaned up batch {args.batch_id}")
            else:
                logger.error(f"Failed to clean up batch {args.batch_id}")
        
        elif args.all:
            # すべてのバッチを削除
            results = cleanup.delete_all_batches(limit=args.limit)
            logger.info(f"Cleanup completed. Success: {len(results['success'])}, Failed: {len(results['failed'])}")
            if results["failed"]:
                logger.error(f"Failed batches: {', '.join(results['failed'])}")
        
        else:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
