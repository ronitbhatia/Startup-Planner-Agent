import json
import re
from tools.ollama_runner import run_ollama

def generate_swot(parsed_idea: dict, market: dict) -> dict:
    industry = parsed_idea.get("industry", "")
    solution = parsed_idea.get("solution", "")
    competitors = market.get("competitors", [])
    trends = market.get("trends", [])

    prompt = f"""
You are a business strategy assistant.

Here is a startup idea in the {industry} industry:
Solution: {solution}
Competitors: {', '.join(competitors)}
Trends: {', '.join(trends)}

Perform a SWOT analysis and return only this valid JSON:
{{
  "strengths": ["..."],
  "weaknesses": ["..."],
  "opportunities": ["..."],
  "threats": ["..."]
}}

Strictly return only JSON. No explanation or questions.
"""


    output = run_ollama(prompt)

    try:
        json_block = re.search(r"\{[\s\S]*\}", output).group(0)
        parsed = json.loads(json_block)
    except Exception:
        parsed = {"raw_output": output}

    return parsed
