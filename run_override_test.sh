#!/bin/bash

# Run the prompt
poetry run promptrunner basic-test \
    '{"assistant_name": "Rufus", "user_question": "Explain me in detail how text embeddings work and how a transformer model can be used to calculate them"}' \
    --prompts-file prompts/prompts.yaml \
    --models-file prompts/models.yaml \
    --overrides '{"model": "gpt-5", "parameters": {"temperature": 1, "max-tokens": null, "max-completion-tokens": 700}}' \
    --md
