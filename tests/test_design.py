import unittest
import unittest.mock
from promptrunner.models import Prompt, ModelDefinition, Result, ResultType, OutputType, Role
from promptrunner.loaders.yaml_prompt_loader import YAMLPromptLoader
from promptrunner.loaders.yaml_model_configuration import YAMLModelConfiguration
from promptrunner.runner import PromptRunner
from promptrunner.interfaces import PromptLoader, ModelConfiguration

class TestPromptRunnerDesign(unittest.TestCase):
    
    def test_models_instantiation(self):
        """Test that Pydantic models can be instantiated with correct data."""
        # Test Prompt model
        prompt_data = {
            "name": "test_prompt",
            "version": "1.0",
            "model": "gpt-4-model",
            "parameters": {
                "max-tokens": 100,
                "temperature": 0.7,
                "output-type": "text"
            },
            "messages": [
                {"role": "system", "content": "You are a helper."},
                {"role": "user", "content": "Hello {{name}}"}
            ]
        }
        prompt = Prompt(**prompt_data)
        self.assertEqual(prompt.name, "test_prompt")
        self.assertEqual(prompt.messages[0].role, Role.SYSTEM)
        
        # Test ModelDefinition model
        model_data = {
            "id": "gpt-4-model",
            "model-type": "OpenAI",
            "model-name": "gpt-4",
            "model-version": "2023-05-15"
        }
        model_def = ModelDefinition(**model_data)
        self.assertEqual(model_def.id, "gpt-4-model")
        self.assertEqual(model_def.model_type, "OpenAI")

    def test_loaders_inheritance(self):
        """Test that loaders implement the correct interfaces."""
        self.assertTrue(issubclass(YAMLPromptLoader, PromptLoader))
        self.assertTrue(issubclass(YAMLModelConfiguration, ModelConfiguration))

    def test_yaml_prompt_loader(self):
        """Test loading prompts from YAML file."""
        loader = YAMLPromptLoader("tests/test_prompts.yaml")
        prompt = loader.get_prompt("test_prompt")
        self.assertEqual(prompt.name, "test_prompt")
        self.assertEqual(prompt.model, "gpt-4-model")
        self.assertEqual(len(prompt.messages), 2)
        
        with self.assertRaises(ValueError):
            loader.get_prompt("non_existent_prompt")

    def test_yaml_model_configuration(self):
        """Test loading model configuration from YAML file."""
        config = YAMLModelConfiguration("tests/test_models.yaml")
        model = config.get_model("gpt-4-model")
        self.assertEqual(model.id, "gpt-4-model")
        self.assertEqual(model.model_name, "gpt-4")
        
        with self.assertRaises(ValueError):
            config.get_model("non_existent_model")

    @unittest.mock.patch('promptrunner.drivers.openai_driver.OpenAI')
    def test_runner_structure(self, mock_openai):
        """Test PromptRunner initialization and method signatures."""
        # We need valid files for initialization now because loaders load in __init__
        loader = YAMLPromptLoader("tests/test_prompts.yaml")
        config = YAMLModelConfiguration("tests/test_models.yaml")
        runner = PromptRunner(loader, config)
        
        self.assertIsInstance(runner, PromptRunner)

    @unittest.mock.patch('promptrunner.drivers.openai_driver.OpenAI')
    def test_runner_execution(self, mock_openai):
        """Test PromptRunner execution with mocked OpenAI."""
        # Setup mock
        mock_client = mock_openai.return_value
        mock_response = unittest.mock.MagicMock()
        mock_response.choices[0].message.content = "Hello Developer"
        mock_client.chat.completions.create.return_value = mock_response

        loader = YAMLPromptLoader("tests/test_prompts.yaml")
        config = YAMLModelConfiguration("tests/test_models.yaml")
        runner = PromptRunner(loader, config)
        
        result = runner.run("test_prompt", {"name": "Developer"})
        
        self.assertEqual(result.type, ResultType.TEXT)
        self.assertEqual(result.content, "Hello Developer")
        
        # Verify OpenAI was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_args["model"], "gpt-4")
        self.assertEqual(call_args["messages"][1]["content"], "Hello Developer")

if __name__ == '__main__':
    unittest.main()
