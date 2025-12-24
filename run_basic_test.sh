#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the prompt
python run.py basic-test \
    '{"assistant_name": "Rufus", "user_question": "Explain me in detail how text embeddings work and how a transformer model can be used to calculate them"}' \
    --prompts-file prompts/prompts.yaml \
    --models-file prompts/models.yaml
