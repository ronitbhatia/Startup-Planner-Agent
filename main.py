from agents.idea_parser import parse_startup_idea
from agents.market_research import run_market_research
from agents.swot_analysis import generate_swot
from agents.mvp_planner import create_mvp_plan

if __name__ == "__main__":
    idea = input("Enter your startup idea:\n> ")

    parsed = parse_startup_idea(idea)
    print("\n [Step 1] Parsed Idea:")
    for key, value in parsed.items():
        print(f"{key.capitalize()}: {value}")

    market = run_market_research(parsed)
    print("\n [Step 2] Market Research:")
    for key, value in market.items():
        print(f"{key.capitalize()}: {value}")

    swot = generate_swot(parsed, market)
    print("\n [Step 3] SWOT Analysis:")
    for key, value in swot.items():
        print(f"{key.capitalize()}: {value}")

    mvp = create_mvp_plan(parsed, swot)
    print("\n [Step 4] MVP Plan:")
    for key, value in mvp.items():
        print(f"{key.capitalize()}: {value}")
