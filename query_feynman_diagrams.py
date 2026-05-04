#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["openai>=1.40.0", "typer>=0.12.0"]
# ///
import base64
import mimetypes
from typing import List

import typer
from openai import OpenAI

PROMPT = """The following feynman diagrams all include a particle labeled `a`, which is a long lived particle. Could you organize them into analyses by final state that search for these `a`'s? Write the answer in markdown."""


def image_data_url(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def main(model: str, images: List[str] = typer.Argument(..., help="Image file paths")):
    content = [{"type": "input_text", "text": PROMPT}]
    content += [
        {"type": "input_image", "image_url": image_data_url(path), "detail": "auto"}
        for path in images
    ]

    payload = {
        "model": model,
        "input": [{"role": "user", "content": content}],
    }

    client = OpenAI()
    response = client.responses.create(**payload)
    print(response.output_text)


if __name__ == "__main__":
    typer.run(main)
