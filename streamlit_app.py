import streamlit as st
import json

from agents.idea_parser import parse_startup_idea
from agents.market_research import run_market_research
from agents.swot_analysis import generate_swot
from agents.mvp_planner import create_mvp_plan

st.set_page_config(page_title="Startup Planner Agent", layout="centered")
st.title("Startup Planner Agent")

st.markdown("Enter a startup idea below to generate a full strategic breakdown using local AI agents.")

idea = st.text_area("Enter your startup idea:", height=150)

if st.button("Run All Agents") and idea.strip():
    with st.spinner("Thinking..."):
        parsed = parse_startup_idea(idea)
        market = run_market_research(parsed)
        swot = generate_swot(parsed, market)
        mvp = create_mvp_plan(parsed, swot)

    # Combined result for download
    full_result = {
        "idea": idea,
        "parsed": parsed,
        "market": market,
        "swot": swot,
        "mvp": mvp,
    }

    st.success("Done! Here's your startup plan:")

    # Step 1: Parsed Idea
    with st.expander("Step 1: Idea Parser"):
        st.markdown(f"""
**Industry**: {parsed.get('industry', '')}  
**Target Users**: {parsed.get('target_user', '')}  
**Pain Point**: {parsed.get('pain_point', '')}  
**Solution**: {parsed.get('solution', '')}  
**Monetization**: {parsed.get('monetization', '')}
""")

    # Step 2: Market Research
    with st.expander("Step 2: Market Research"):
        st.markdown("**Competitors:**")
        st.markdown("- " + "\n- ".join(market.get("competitors", [])))
        st.markdown(f"\n**Market Size:** {market.get('market_size', '')}")
        st.markdown("\n**Trends:**")
        st.markdown("- " + "\n- ".join(market.get("trends", [])))

    # Step 3: SWOT Analysis
    with st.expander("Step 3: SWOT Analysis"):
        for category in ["strengths", "weaknesses", "opportunities", "threats"]:
            st.markdown(f"**{category.capitalize()}:**")
            st.markdown("- " + "\n- ".join(swot.get(category, [])))

    # Step 4: MVP Plan
    with st.expander("Step 4: MVP Planner"):
        st.markdown("**Key Features:**")
        st.markdown("- " + "\n- ".join(mvp.get("features", [])))

        tech = mvp.get("tech_stack", {})
        st.markdown("\n**Tech Stack:**")
        st.markdown(f"""
- **Frontend**: {tech.get('frontend', '')}  
- **Backend**: {tech.get('backend', '')}  
- **Database**: {tech.get('database', '')}  
- **Other**: {', '.join(tech.get('other', [])) if tech.get('other') else 'None'}
""")

        st.markdown(f"\n**Timeline**: {mvp.get('timeline', '')}")
        st.markdown("\n**Risks:**")
        st.markdown("- " + "\n- ".join(mvp.get("risks", [])))

    # Download as JSON
    st.download_button(
        label="Download as JSON",
        data=json.dumps(full_result, indent=2),
        file_name="startup_plan.json",
        mime="application/json"
    )

    # Download as TXT
    text_output = f"""Startup Idea: {idea}

Step 1: Parsed Idea
-------------------
Industry: {parsed.get('industry', '')}
Target Users: {parsed.get('target_user', '')}
Pain Point: {parsed.get('pain_point', '')}
Solution: {parsed.get('solution', '')}
Monetization: {parsed.get('monetization', '')}

Step 2: Market Research
-----------------------
Competitors: {', '.join(market.get("competitors", []))}
Market Size: {market.get("market_size", '')}
Trends:
- {chr(10).join(market.get("trends", []))}

Step 3: SWOT Analysis
---------------------
Strengths:
- {chr(10).join(swot.get("strengths", []))}
Weaknesses:
- {chr(10).join(swot.get("weaknesses", []))}
Opportunities:
- {chr(10).join(swot.get("opportunities", []))}
Threats:
- {chr(10).join(swot.get("threats", []))}

Step 4: MVP Plan
----------------
Features:
- {chr(10).join(mvp.get("features", []))}

Tech Stack:
Frontend: {tech.get("frontend", "")}
Backend: {tech.get("backend", "")}
Database: {tech.get("database", "")}
Other: {', '.join(tech.get("other", [])) if tech.get("other") else 'None'}

Timeline: {mvp.get("timeline", '')}
Risks:
- {chr(10).join(mvp.get("risks", []))}
"""

    st.download_button(
        label="Download as TXT",
        data=text_output,
        file_name="startup_plan.txt",
        mime="text/plain"
    )
