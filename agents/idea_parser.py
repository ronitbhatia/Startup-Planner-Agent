import json
import re
from tools.ollama_runner import run_ollama

def parse_startup_idea(idea: str) -> dict:
    if not idea or len(idea.strip()) < 10:
        return {
            "industry": "",
            "target_user": "",
            "pain_point": "",
            "solution": "",
            "monetization": "",
            "raw_output": "Startup idea input was too short or invalid."
        }

    prompt = f"""
You are a startup analyst.

Given this idea:
\"\"\"{idea.strip()}\"\"\"

Return ONLY valid JSON in this format:

{{
  "industry": "...",
  "target_user": "...",
  "pain_point": "...",
  "solution": "...",
  "monetization": "..."
}}

Only JSON. No extra output.
"""

    output = run_ollama(prompt)

    try:
        output_clean = output.split("Raw_output:")[-1].strip()
        json_block = re.search(r"\{[\s\S]*\}", output_clean).group(0)
        parsed = json.loads(json_block)

        keys = ["industry", "target_user", "pain_point", "solution", "monetization"]
        if not all(k in parsed for k in keys):
            raise ValueError("Missing keys")

    except Exception:
        parsed = {
            "industry": "",
            "target_user": "",
            "pain_point": "",
            "solution": "",
            "monetization": "",
            "raw_output": output
        }

    return parsed

