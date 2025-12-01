#!/usr/bin/env python3
"""
OpenAI Helper

Basic usage of the OpenAI API.
Set your API key in .env file or: export OPENAI_API_KEY="sk-..."
"""
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")

client = OpenAI()


def prompt(
    input: str,
    model: str = "gpt-4o-mini",
    instructions: str = None,
    reasoning: dict = None,
) -> str:
    """
    Send a prompt to OpenAI and return the response.

    Args:
        input: The user input/prompt
        model: Model to use (default: gpt-4o-mini)
        instructions: System instructions for the model
        reasoning: Reasoning config, e.g. {"effort": "low"}

    Returns:
        The model's response text
    """
    kwargs = {"model": model, "input": input}
    if instructions:
        kwargs["instructions"] = instructions
    if reasoning:
        kwargs["reasoning"] = reasoning

    response = client.responses.create(**kwargs)
    return response.output_text


if __name__ == "__main__":
    # Quick test
    result = prompt(
        input="What trade would install copper pipes in a building?",
        instructions="You are a construction expert. Be concise.",
    )
    print(result)
