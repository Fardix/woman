#!/usr/bin/env python3
import sys
import requests

from woman.config import save_api_key, load_api_key

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"

def set_key():
    key = input("Enter your Gemini API key: ").strip()
    if not key:
        print("API key cannot be empty.")
        sys.exit(1)
    save_api_key(key)
    print("API key saved.")

def query_gemini(api_key, command):
    headers = {"Content-Type": "application/json"}
    prompt = (
        f"You are a helpful Linux man page assistant.\n"
        f"Explain concisely what the '{command}' command does in Unix/Linux.\n\n"
        f"Format the answer in Markdown with:\n"
        f"**Description:** one short paragraph.\n"
        f"**Important Options:** bullet list with only the most useful options (if any).\n"
        f"**Example:** one simple, realistic usage example in a fenced code block.\n"
        f"Be concise and avoid unnecessary text."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    resp = requests.post(f"{API_URL}?key={api_key}", json=payload, headers=headers)

    if resp.status_code != 200:
        print(f"Error: {resp.status_code} {resp.text}")
        sys.exit(1)

    data = resp.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "No response from Gemini."


def main():
    if len(sys.argv) < 2:
        print("Usage: woman <command> | woman set-key")
        sys.exit(1)

    if sys.argv[1] == "set-key":
        set_key()
        return

    api_key = load_api_key()
    if not api_key:
        print("No API key found.")
        set_key()
        api_key = load_api_key()
        if not api_key:
            print("Failed to set API key.")
            sys.exit(1)

    command = " ".join(sys.argv[1:])
    print(query_gemini(api_key, command))

if __name__ == "__main__":
    main()
