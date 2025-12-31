import argparse
import json
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.json import JSON
from promptrunner.loaders.yaml_prompt_loader import YAMLPromptLoader
from promptrunner.loaders.yaml_model_configuration import YAMLModelConfiguration
from promptrunner.runner import PromptRunner
from promptrunner.models.result_type import ResultType

def main():
    load_dotenv()
    console = Console()
    
    parser = argparse.ArgumentParser(description="Run a prompt using PromptRunner.")
    parser.add_argument("prompt_name", help="The name of the prompt to run")
    parser.add_argument("params", help="JSON string of parameters")
    parser.add_argument("--overrides", help="JSON string of overrides (e.g. '{\"model\": \"gpt-4\", \"parameters\": {\"temperature\": 0.5}}')")
    parser.add_argument("--prompts-file", default="prompts.yaml", help="Path to prompts YAML file")
    parser.add_argument("--models-file", default="models.yaml", help="Path to models YAML file")
    parser.add_argument("--md", action="store_true", help="Format output as Markdown")
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        print("Error: params must be a valid JSON string")
        return

    overrides = None
    if args.overrides:
        try:
            overrides = json.loads(args.overrides)
        except json.JSONDecodeError:
            print("Error: overrides must be a valid JSON string")
            return

    loader = YAMLPromptLoader(args.prompts_file)
    config = YAMLModelConfiguration(args.models_file)
    runner = PromptRunner(loader, config)
    
    try:
        result = runner.run(args.prompt_name, params, overrides=overrides)
        console.print(f"[bold blue]Result Type:[/bold blue] {result.type.value}")
        
        if result.type == ResultType.TEXT:
            if args.md:
                console.print(Markdown(str(result.content)))
            else:
                print(result.content)
        elif result.type == ResultType.OBJECT:
            console.print(JSON(json.dumps(result.content)))
        else:
            console.print(f"Content: {result.content}")
            
    except NotImplementedError:
        console.print("[bold red]Error:[/bold red] Implementation pending.")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
