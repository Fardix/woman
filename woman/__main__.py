#!/usr/bin/env python3
import sys
import requests
import json
from woman.config import load_api_key, save_api_key
from woman.output import print_response

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"


def prompt_and_save_key():
    key = input("Enter your Gemini API key: ").strip()
    if not key:
        print("API key cannot be empty.")
        return False
    save_api_key(key)
    print("API key saved.")
    return True


def explain_command(command):
    api_key = load_api_key()
    if not api_key:
        # Prompt and save key, then reload
        print("No API key found. Please enter it now.")
        ok = prompt_and_save_key()
        if not ok:
            print("API key not set. Aborting.")
            return
        api_key = load_api_key()
        if not api_key:
            print("Failed to save API key. Aborting.")
            return

    # Gemini prompt requesting strict JSON (note: braces doubled to escape f-string)
    prompt = f"""
You are a Linux CLI documentation expert.
Explain concisely the command '{command}' in the following JSON format only:

{{
  "command": "{command}",
  "description": "description here",
  "options": [
    {{"flag": "-x", "desc": "option description"}}
  ],
  "example": "example usage here"
}}

Include only the most important 2-5 options.
Include one useful example if possible.
Do not include extra commentary or text outside of JSON.
"""

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        resp = requests.post(f"{API_URL}?key={api_key}", headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        print(f"Network error while calling API: {e}")
        return

    if resp.status_code != 200:
        # Print helpful error details
        print(f"Error: {resp.status_code} from API.")
        try:
            print(resp.json())
        except Exception:
            print(resp.text)
        return

    # Try to extract text safely from API response
    try:
        resp_json = resp.json()
    except ValueError:
        print("Error: API returned non-JSON response.")
        print(resp.text)
        return

    try:
        text_output = resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, TypeError):
        print("Error: unexpected API response format.")
        print(json.dumps(resp_json, indent=2))
        return

    # Try parsing the returned text as JSON. If that fails, try to find a JSON substring.
    try:
        data_json = json.loads(text_output)
        print_response(data_json)
    except json.JSONDecodeError:
        # Attempt to find a JSON object inside the text (best-effort)
        start = text_output.find("{")
        end = text_output.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                data_json = json.loads(text_output[start : end + 1])
                print_response(data_json)
                return
            except json.JSONDecodeError:
                pass

        # Final fallback: show raw output with warning
        print("⚠️ Warning: API returned non-JSON output. Showing raw response:")
        print(text_output)


def main():
    if len(sys.argv) < 2:
        print("Usage: woman <command> | woman set-key")
        return

    first = sys.argv[1].lower()
    if first in ("set-key", "--set-key", "--set_key", "set_key"):
        # Interactive set-key and exit
        if prompt_and_save_key():
            return
        else:
            sys.exit(1)

    # Otherwise treat everything after the first arg as the command to explain
    command = " ".join(sys.argv[1:])
    explain_command(command)


if __name__ == "__main__":
    main()
