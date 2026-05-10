"""Thin OpenAI client wrapper used everywhere we need GPT reasoning."""

from openai import OpenAI

from src.config.settings import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)


def message_to_gpt(message: str) -> str:
    """Send a single prompt to OpenAI and return the plain-text response.

    Args:
        message: The fully formatted prompt to send.

    Returns:
        The model's text output.
    """
    response = client.responses.create(model="gpt-5-nano", input=message)
    return response.output_text
