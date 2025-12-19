#!/usr/bin/env python3
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import yaml


load_dotenv(Path(__file__).parent.parent / ".env")
client = OpenAI()


def _load_prompt() -> dict:
    prompt_path = Path(__file__).parent / "prompt.yml"
    with open(prompt_path, "r") as f:
        return yaml.safe_load(f)

PROMPT_CONFIG = _load_prompt()

def classify_trade(
    description: str,
    allowed_trades: List[str],
    model: str = "gpt-4o-mini"
) -> str:
    """
    Classify a BOQ item description into a single trade.
    """

    system_prompt = PROMPT_CONFIG.get("system", "")
    user_template = PROMPT_CONFIG.get("user_template", "")

    user_prompt = user_template \
        .replace("{{description}}", description.strip()) \
        .replace("{{allowed_trades}}", ", ".join(allowed_trades))

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_prompt
    )

    return response.output_text.strip()