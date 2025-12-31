import unittest
from unittest.mock import MagicMock, patch
from promptrunner.runner import PromptRunner
from promptrunner.models import Prompt, ModelDefinition, Result, ResultType, ModelType
from promptrunner.interfaces import PromptLoader, ModelConfiguration

class TestOverrides(unittest.TestCase):
    @patch('promptrunner.runner.OpenAIDriver')
    def setUp(self, mock_openai_driver_cls):
        self.mock_loader = MagicMock(spec=PromptLoader)
        self.mock_config = MagicMock(spec=ModelConfiguration)
        self.runner = PromptRunner(self.mock_loader, self.mock_config)
        
        # Setup default prompt
        self.prompt = Prompt(
            name="test_prompt",
            version="1.0",
            model="default-model",
            parameters={"temperature": 0.5, "max_tokens": 100},
            messages=[]
        )
        self.mock_loader.get_prompt.return_value = self.prompt
        
        # Setup default model definition
        self.model_def = ModelDefinition(
            id="default-model",
            **{"model-type": ModelType.OPENAI, "model-name": "gpt-3.5-turbo"}
        )
        self.mock_config.get_model.return_value = self.model_def

    def test_override_model(self):
        # Mock the driver
        mock_driver = MagicMock()
        mock_driver.execute.return_value = Result(type=ResultType.TEXT, content="ok")
        self.runner._drivers[ModelType.OPENAI] = mock_driver
        
        # Run with overrides
        overrides = {"model": "new-model"}
        
        new_model_def = ModelDefinition(
            id="new-model",
            **{"model-type": ModelType.OPENAI, "model-name": "gpt-4"}
        )
        
        def get_model_side_effect(model_id):
            if model_id == "new-model":
                return new_model_def
            return self.model_def
            
        self.mock_config.get_model.side_effect = get_model_side_effect
        
        self.runner.run("test_prompt", {}, overrides=overrides)
        
        # Check if get_model was called with new model
        self.mock_config.get_model.assert_called_with("new-model")
        
        # Check if driver.execute was called with modified prompt
        args, _ = mock_driver.execute.call_args
        executed_prompt = args[0]
        self.assertEqual(executed_prompt.model, "new-model")

    def test_override_parameters(self):
        # Mock the driver
        mock_driver = MagicMock()
        mock_driver.execute.return_value = Result(type=ResultType.TEXT, content="ok")
        self.runner._drivers[ModelType.OPENAI] = mock_driver
        
        overrides = {"parameters": {"temperature": 0.9, "top_p": 1.0}}
        
        self.runner.run("test_prompt", {}, overrides=overrides)
        
        args, _ = mock_driver.execute.call_args
        executed_prompt = args[0]
        
        self.assertEqual(executed_prompt.parameters["temperature"], 0.9)
        self.assertEqual(executed_prompt.parameters["max_tokens"], 100) # Should be preserved
        self.assertEqual(executed_prompt.parameters["top_p"], 1.0) # Should be added
