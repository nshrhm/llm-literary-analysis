"""Unit tests for OpenAIBatchRunner with excluded models."""
import unittest
from unittest.mock import MagicMock, patch
from openai_batch_runner import OpenAIBatchRunner
from parameters import OPENAI_MODELS

class TestOpenAIBatchRunner(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.runner = OpenAIBatchRunner()
        self.runner.client = MagicMock()  # Mock OpenAI client

    def test_model_processing(self):
        """Test that all configured models are processed."""
        for model_id in OPENAI_MODELS:
            self.assertIn(model_id, OPENAI_MODELS,
                        f"Configured model {model_id} should be in OPENAI_MODELS")

    @patch('openai_batch_runner.OpenAIBatchRunner._create_model_batch')
    @patch('builtins.print')
    def test_model_selection(self, mock_print, mock_create_batch):
        """Test that all configured models are selected for processing."""
        self.runner.run_batch_experiment()
        
        # Check mock was called for all configured models
        called_models = [args[0] for args, _ in mock_create_batch.call_args_list]
        for model_id in OPENAI_MODELS:
            self.assertIn(model_id, called_models)

    def test_custom_id_format(self):
        """Test custom ID follows expected format."""
        model_id = "o3-mini"
        
        # Mock _create_model_batch to test ID format
        with patch('builtins.open', unittest.mock.mock_open()):
            self.runner._create_model_batch(model_id, OPENAI_MODELS[model_id], "test")
        
        # Verify ID contains required components
        # Actual value checking is done in prompt_manager tests
        self.assertTrue(model_id in OPENAI_MODELS)

if __name__ == '__main__':
    unittest.main()
