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


def call_gemini(prompt):
    api_key = load_api_key()
    if not api_key:
        print("No API key found. Please enter it now.")
        ok = prompt_and_save_key()
        if not ok:
            print("API key not set. Aborting.")
            return None
        api_key = load_api_key()
        if not api_key:
            print("Failed to save API key. Aborting.")
            return None

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        resp = requests.post(f"{API_URL}?key={api_key}", headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        print(f"Network error while calling API: {e}")
        return None

    if resp.status_code != 200:
        print(f"Error: {resp.status_code} from API.")
        try:
            print(resp.json())
        except Exception:
            print(resp.text)
        return None

    try:
        resp_json = resp.json()
        return resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (ValueError, KeyError, IndexError, TypeError):
        print("Error: unexpected API response format.")
        print(json.dumps(resp.json(), indent=2))
        return None


def explain_command(command):
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
    text_output = call_gemini(prompt)
    if not text_output:
        return

    try:
        data_json = json.loads(text_output)
    except json.JSONDecodeError:
        start = text_output.find("{")
        end = text_output.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                data_json = json.loads(text_output[start:end + 1])
            except json.JSONDecodeError:
                print("⚠️ API returned non-JSON output. Showing raw response:")
                print(text_output)
                return
        else:
            print("⚠️ API returned non-JSON output. Showing raw response:")
            print(text_output)
            return

    print_response(data_json)


def find_command_for_purpose(purpose):
    prompt = f"""
You are a Linux command expert.
Given the task: "{purpose}", return the **best matching Linux command(s)** in this JSON format only:

{{
  "command": "the exact command to run",
  "description": "what it does",
  "options": [
    {{"flag": "-x", "desc": "option description"}}
  ],
  "example": "example usage if needed"
}}

If there are multiple valid commands, choose the most common one.
Do not output anything outside of JSON.
"""
    text_output = call_gemini(prompt)
    if not text_output:
        return

    try:
        data_json = json.loads(text_output)
    except json.JSONDecodeError:
        start = text_output.find("{")
        end = text_output.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                data_json = json.loads(text_output[start:end + 1])
            except json.JSONDecodeError:
                print("⚠️ API returned non-JSON output. Showing raw response:")
                print(text_output)
                return
        else:
            print("⚠️ API returned non-JSON output. Showing raw response:")
            print(text_output)
            return

    print_response(data_json)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  woman <command>          - Explain a command")
        print("  woman -p \"task to do\"   - Find command for a purpose")
        print("  woman set-key            - Set API key")
        return

    first = sys.argv[1].lower()

    if first in ("set-key", "--set-key", "--set_key", "set_key"):
        if prompt_and_save_key():
            return
        else:
            sys.exit(1)

    if first == "-p":
        purpose = " ".join(sys.argv[2:]).strip()
        if not purpose:
            print("Error: No purpose given.")
            return
        find_command_for_purpose(purpose)
        return

    # Normal mode: explain command
    command = " ".join(sys.argv[1:])
    explain_command(command)


if __name__ == "__main__":
    main()
