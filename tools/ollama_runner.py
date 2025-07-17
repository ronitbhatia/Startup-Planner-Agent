import subprocess
import json
import re

def run_ollama(prompt: str, model: str = "llama3", timeout: int = 60, json_only: bool = False) -> str:
    def _invoke_ollama(raw_prompt: str) -> str:
        cmd = ["ollama", "run", model]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate(raw_prompt, timeout=timeout)

        if process.returncode != 0:
            raise RuntimeError(f"Ollama failed with error:\n{error.strip()}")

        return output.strip()

    def _looks_like_json(text: str) -> bool:
        return bool(re.search(r"\{[\s\S]*\}", text))

    # First attempt
    output = _invoke_ollama(prompt)

    if json_only and not _looks_like_json(output):
        # Retry once with simplified prompt
        retry_prompt = f"{prompt.strip()}\n\nONLY return valid JSON. No intro or explanation."
        output = _invoke_ollama(retry_prompt)

    return output.strip()
