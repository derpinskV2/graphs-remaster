#!/bin/bash

unset POETRY_ENV_PATH

if [ ! -f pyproject.toml ]; then
    echo "No pyproject.toml found in the current directory!"
    exit 1
fi

POETRY_ENV_PATH=$(poetry env info --path)

if [ -z "$POETRY_ENV_PATH" ]; then
    echo "No Poetry environment found. Creating one..."
    poetry install
    POETRY_ENV_PATH=$(poetry env info --path)
fi

echo "Virtual environment path: $POETRY_ENV_PATH/bin/python3"
