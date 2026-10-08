"""Shared setup and helpers for the Claude API notebooks.

Usage in a notebook:
    from claude_utils import check_settings, add_user_message, add_assistant_message, chat
    check_settings()
"""
import os
import sys
from pathlib import Path

import anthropic
import httpx
from dotenv import load_dotenv

# Load the .env that sits next to this file, regardless of the notebook's working directory
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 1000

_client = None


def get_client():
    """Return a shared Anthropic client, created on first use."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def check_settings():
    print("anthropic:", anthropic.__version__)
    print("httpx:", httpx.__version__)
    print(".env file:", ENV_PATH, "(found)" if ENV_PATH.exists() else "(missing)")
    print("API key present:", bool(os.getenv("ANTHROPIC_API_KEY")))
    print("Python:", sys.executable)


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})
    return messages


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
    return messages


def chat(messages, system=None, model=MODEL, max_tokens=MAX_TOKENS):
    params = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        params["system"] = system
    message = get_client().messages.create(**params)
    return message.content[0].text
