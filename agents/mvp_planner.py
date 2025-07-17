import json
import re
from tools.ollama_runner import run_ollama

def create_mvp_plan(parsed_idea: dict, swot: dict) -> dict:
    industry = parsed_idea.get("industry", "tech")
    solution = parsed_idea.get("solution", "A tech-enabled solution to a user pain point.")
    strengths = swot.get("strengths", []) or ["Strong product-market fit"]
    weaknesses = swot.get("weaknesses", []) or ["Limited budget"]

    prompt = f"""
You are an expert product manager.

You are helping build an MVP for a startup in the "{industry}" industry.

Product Concept:
{solution}

Key Strengths: {', '.join(strengths)}
Key Weaknesses: {', '.join(weaknesses)}

Based on this, return ONLY a valid JSON with the following structure:

{{
  "features": ["List 3–5 MVP features"],
  "tech_stack": {{
    "frontend": "...",
    "backend": "...",
    "database": "...",
    "other": ["Optional tools, APIs, or services"]
  }},
  "timeline": "Time to develop MVP (e.g. 6-8 weeks)",
  "risks": ["List 2–4 key risks"]
}}

Respond with only JSON. No explanation.
"""

    output = run_ollama(prompt)

    try:
        # Extract JSON block from model output
        json_block = re.search(r"\{[\s\S]*\}", output).group(0)
        parsed = json.loads(json_block)

        # Optional: Validate that key fields exist
        if not all(k in parsed for k in ["features", "tech_stack", "timeline", "risks"]):
            raise ValueError("Missing keys in parsed response")

    except Exception:
        parsed = {
            "features": [],
            "tech_stack": {
                "frontend": "",
                "backend": "",
                "database": "",
                "other": []
            },
            "timeline": "",
            "risks": [],
            "raw_output": output
        }

    return parsed
