# Startup Planner Agent

An AI-powered app that helps you brainstorm, research, and design startup MVPs using **local LLMs** — no API keys required.

Built with [Streamlit](https://streamlit.io) for the frontend and [Ollama](https://ollama.com) to run models like **LLaMA 3** locally on your machine.

---

## What It Does

Input a startup idea, and this tool will generate:

**Step 1: Idea Breakdown** — Industry, target user, pain point, solution, monetization  
**Step 2: Market Research** — Competitors, market size, industry trends  
**Step 3: SWOT Analysis** — Strengths, weaknesses, opportunities, threats  
**Step 4: MVP Plan** — Features, tech stack, dev timeline, risks

---

## Example Output

**Input Idea:**

> An app that connects dog walkers with pet owners using real-time GPS and reviews.

**Output Includes:**

- Target users: Pet owners and dog walkers  
- Pain point: Difficulty finding reliable dog walkers  
- Solution: GPS tracking + review-based matching  
- MVP Features: Walk tracking, reviews, payments  
- Tech Stack: React Native + Node.js + Firebase  
- Risks: Trust, GPS accuracy, market competition

---

## How to Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/startup-planner-agent.git
cd startup-planner-agent
````

### 2. Install Python Dependencies

```bash
pip install streamlit
```

### 3. Install and Run Ollama

Install Ollama from [https://ollama.com/download](https://ollama.com/download) and then:

```bash
ollama run llama3
```

This will download and run the LLaMA 3 model locally.

### 4. Launch the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📂 Project Structure

```
startup-planner-agent/
├── streamlit_app.py           # Streamlit UI
├── requirements.txt           # Streamlit dependency
├── agents/                    # Agents for each step
│   ├── idea_parser.py
│   ├── market_research.py
│   ├── swot_analysis.py
│   └── mvp_planner.py
├── tools/
│   └── ollama_runner.py       # Calls local LLM via subprocess
├── README.md
```

---


## 🔒 Privacy & Offline Use

This app runs **entirely locally** — your ideas are not sent to the cloud.
It uses Ollama and LLaMA 3, no API keys or internet connection required after model download.

---

##Credits

* [Ollama](https://ollama.com) for local model serving
* [Meta's LLaMA 3](https://ai.meta.com/llama/) for model architecture
* [Streamlit](https://streamlit.io) for the UI framework

