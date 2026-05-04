#!/usr/bin/env -S uv run --script
import base64
import json
import mimetypes
import os
import sys
import urllib.request


PROMPT = """The following feynman diagrams all include a particle labeled `a`, which is a long lived particle. Could you organize them into analyses by final state that search for these `a`'s? Write the answer in markdown."""


def image_data_url(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


model = sys.argv[1]
image_paths = [path for arg in sys.argv[2:] for path in arg.split(",") if path]

content = [{"type": "input_text", "text": PROMPT}]
content += [
    {"type": "input_image", "image_url": image_data_url(path), "detail": "auto"}
    for path in image_paths
]

payload = {
    "model": model,
    "input": [
        {
            "role": "user",
            "content": content,
        }
    ],
}

request = urllib.request.Request(
    "https://api.openai.com/v1/responses",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    },
    method="POST",
)

response = json.loads(urllib.request.urlopen(request).read().decode("utf-8"))

print(
    "\n".join(
        part["text"]
        for item in response["output"]
        if item["type"] == "message"
        for part in item["content"]
        if part["type"] == "output_text"
    )
)
