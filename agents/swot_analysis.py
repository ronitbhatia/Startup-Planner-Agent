import json
import re
from tools.ollama_runner import run_ollama

def generate_swot(parsed_idea: dict, market: dict) -> dict:
    industry = parsed_idea.get("industry", "technology")
    solution = parsed_idea.get("solution", "A digital platform addressing a common user pain point.")
    competitors = market.get("competitors", []) or ["Generic competitor A", "Generic competitor B"]
    trends = market.get("trends", []) or ["Trend A", "Trend B"]

    prompt = f"""
You are a startup strategy assistant.

Please perform a SWOT analysis for a startup with the following details:

Industry: {industry}
Solution: {solution}
Competitors: {', '.join(competitors)}
Trends: {', '.join(trends)}

Respond ONLY with valid JSON using this format:

{{
  "strengths": ["..."],
  "weaknesses": ["..."],
  "opportunities": ["..."],
  "threats": ["..."]
}}
"""

    output = run_ollama(prompt)

    try:
        json_block = re.search(r"\{[\s\S]*\}", output).group(0)
        parsed = json.loads(json_block)

        # Ensure all 4 keys exist
        required_keys = ["strengths", "weaknesses", "opportunities", "threats"]
        if not all(k in parsed for k in required_keys):
            raise ValueError("Missing SWOT keys")

    except Exception:
        parsed = {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": [],
            "raw_output": output
        }

    return parsed
