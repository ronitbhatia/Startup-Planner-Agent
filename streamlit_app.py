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
        if not parsed.get("industry"):
            st.error("❌ Step 1 failed to parse the startup idea. Please try rephrasing it.")
            st.stop()

        market = run_market_research(parsed)
        if not market.get("competitors"):
            st.error("❌ Step 2 (Market Research) failed. Try a different idea.")
            st.stop()

        swot = generate_swot(parsed, market)
        if not swot.get("strengths"):
            st.warning("⚠️ Step 3 (SWOT Analysis) might be incomplete.")

        mvp = create_mvp_plan(parsed, swot)
        if not mvp.get("features"):
            st.warning("⚠️ Step 4 (MVP Planner) might be incomplete.")

    st.success("✅ Done! Here's your startup plan:")

    # STEP 1 — IDEA PARSER
    with st.expander("Step 1: Idea Parser", expanded=True):
        st.markdown(f"""
**Industry**: {parsed.get('industry', '')}  
**Target Users**: {parsed.get('target_user', '')}  
**Pain Point**: {parsed.get('pain_point', '')}  
**Solution**: {parsed.get('solution', '')}  
**Monetization**: {parsed.get('monetization', '')}
""")

    # STEP 2 — MARKET RESEARCH
    with st.expander("Step 2: Market Research", expanded=True):
        st.markdown("**Competitors:**")
        st.markdown("- " + "\n- ".join(market.get("competitors", [])))
        st.markdown(f"\n**Market Size:** {market.get('market_size', '')}")
        st.markdown("\n**Trends:**")
        st.markdown("- " + "\n- ".join(market.get("trends", [])))

    # STEP 3 — SWOT ANALYSIS
    with st.expander("Step 3: SWOT Analysis", expanded=True):
        for key in ["strengths", "weaknesses", "opportunities", "threats"]:
            st.markdown(f"**{key.capitalize()}:**")
            st.markdown("- " + "\n- ".join(swot.get(key, [])))

    # STEP 4 — MVP PLANNER
    with st.expander("Step 4: MVP Planner", expanded=True):
        st.markdown("**Key Features:**")
        st.markdown("- " + "\n- ".join(mvp.get("features", [])))

        tech = mvp.get("tech_stack", {})
        st.markdown("**Tech Stack:**")
        st.markdown(f"""
- **Frontend**: {tech.get('frontend', '')}  
- **Backend**: {tech.get('backend', '')}  
- **Database**: {tech.get('database', '')}  
- **Other**: {', '.join(tech.get('other', [])) if tech.get('other') else 'None'}
""")

        st.markdown(f"\n**Timeline**: {mvp.get('timeline', '')}")
        st.markdown("**Risks:**")
        st.markdown("- " + "\n- ".join(mvp.get("risks", [])))

    # COMBINE OUTPUT FOR DOWNLOAD
    full_result = {
        "idea": idea,
        "parsed": parsed,
        "market": market,
        "swot": swot,
        "mvp": mvp,
    }

    st.download_button(
        label="📁 Download JSON",
        data=json.dumps(full_result, indent=2),
        file_name="startup_plan.json",
        mime="application/json"
    )

    # Generate text version
    text_output = f"""Startup Idea: {idea}

Step 1: Idea Parser
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
        label="📄 Download Text",
        data=text_output,
        file_name="startup_plan.txt",
        mime="text/plain"
    )
