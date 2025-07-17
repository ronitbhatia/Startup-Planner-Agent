import json
import re
from tools.ollama_runner import run_ollama

def run_market_research(parsed_idea: dict) -> dict:
    industry = parsed_idea.get("industry", "a general business domain")
    solution = parsed_idea.get("solution", "")
    target = parsed_idea.get("target_user", "")

    prompt = f"""
You are a startup business researcher.

Given the following startup idea in the {industry} industry:

Target Users: {target}  
Solution: {solution}

Please provide the following in **valid JSON format only**:
{{
  "competitors": ["List of 3–5 direct or indirect competitors"],
  "market_size": "Estimated market size with year and source if known",
  "trends": ["3–5 industry trends relevant to this business"]
}}

Do not include any commentary. Only return valid JSON.
"""

    output = run_ollama(prompt)

    try:
        json_block = re.search(r"\{[\s\S]*\}", output).group(0)
        parsed = json.loads(json_block)
    except Exception:
        parsed = {"raw_output": output}

    return parsed
