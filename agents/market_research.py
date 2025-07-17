import json
import re
from tools.ollama_runner import run_ollama

def run_market_research(parsed_idea: dict) -> dict:
    industry = parsed_idea.get("industry", "technology and services")
    solution = parsed_idea.get("solution", "A tech platform that solves a customer need.")
    target = parsed_idea.get("target_user", "end users or businesses")

    prompt = f"""
You are a startup market researcher.

Given this business idea:

Industry: {industry}  
Target Users: {target}  
Solution: {solution}

Please return only the following JSON structure:

{{
  "competitors": ["List of 3–5 relevant companies or platforms"],
  "market_size": "Estimated market size (include year + source if possible)",
  "trends": ["List 3–5 relevant trends in this industry"]
}}

Only return valid JSON. No commentary or extra output.
"""

    output = run_ollama(prompt)

    try:
        json_block = re.search(r"\{[\s\S]*\}", output).group(0)
        parsed = json.loads(json_block)

        # Ensure all expected keys exist
        required_keys = ["competitors", "market_size", "trends"]
        if not all(k in parsed for k in required_keys):
            raise ValueError("Missing keys in market research")

    except Exception:
        parsed = {
            "competitors": [],
            "market_size": "",
            "trends": [],
            "raw_output": output
        }

    return parsed
