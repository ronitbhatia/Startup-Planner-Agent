import json
import re
from tools.ollama_runner import run_ollama

def create_mvp_plan(parsed_idea: dict, swot: dict) -> dict:
    solution = parsed_idea.get("solution", "")
    industry = parsed_idea.get("industry", "")
    strengths = swot.get("strengths", [])
    weaknesses = swot.get("weaknesses", [])

    prompt = f"""
You are a product manager.

You're building an MVP for a startup in the industry: "{industry}".

Product concept: {solution}

Strengths: {', '.join(strengths)}
Weaknesses: {', '.join(weaknesses)}

Return a valid JSON object with:
{{
  "features": ["List 3–5 key MVP features"],
  "tech_stack": {{
    "frontend": "...",
    "backend": "...",
    "database": "...",
    "other": "Optional libraries/services"
  }},
  "timeline": "Estimate dev time (e.g., 4–6 weeks)",
  "risks": ["Technical or business risks (2–4)"]
}}

No extra text. Only return valid JSON.
"""

    output = run_ollama(prompt)

    try:
        json_block = re.search(r"\{[\s\S]*\}", output).group(0)
        parsed = json.loads(json_block)
    except Exception:
        parsed = {"raw_output": output}

    return parsed
