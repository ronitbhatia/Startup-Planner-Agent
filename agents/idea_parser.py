import json
import re
from tools.ollama_runner import run_ollama

def parse_startup_idea(idea: str) -> dict:
    prompt = f"""
You are a startup analyst.

Given the following idea:
\"\"\"{idea}\"\"\"

Analyze and return only this structured JSON:
{{
  "industry": "...",
  "target_user": "...",
  "pain_point": "...",
  "solution": "...",
  "monetization": "..."
}}

Only return valid JSON — no extra text or explanation.
"""

    output = run_ollama(prompt)

    # Extract JSON using regex (most robust)
    try:
        output_clean = output.split("Raw_output:")[-1].strip()
        json_block = re.search(r"\{[\s\S]*\}", output_clean).group(0)
        parsed = json.loads(json_block)
    except Exception:
        parsed = {"raw_output": output}

    return parsed
