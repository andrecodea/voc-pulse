# 🌡️ VoC Pulse
*A Voice of Customer Performance Thermometer with Embeddings*

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VoC Pulse** is an AI-powered analytics platform designed to interpret unstructured customer feedback. Currently operating as a Proof-of-Concept (POC) developed in a 48-hour sprint, it transforms qualitative data (reviews, comments) into quantitative insights using Embeddings and Large Language Models (LLMs).

It automatically processes text to extract three key data points: **Sentiment** (Positive, Negative, Mixed), **Topic** (e.g., "Buffet", "DJ"), and **Vector Embeddings** for semantic search.

---

## 🚀 Live Demo

**[>> LIVE APP DEMO ON STREAMLIT CLOUD <<](https://voc-pulse.streamlit.app/)**

---

## 📸 Screenshots

![Dashboard Screenshot](kpi_screenshot.png)

---

## 🌟 Core Features (V1 - Current)

* **KPI Dashboard:** An interactive dashboard visualizing supplier performance based on real customer sentiment using **Plotly** (Trend Charts) and **Matplotlib** (Distribution).
* **Semantic Pie Charts:** Interactive breakdown of sentiment for specific, user-selected suppliers.
* **Targeted Word Clouds:** A dynamic generator showing frequent *keywords* filtered by a "whitelist" of value-words (e.g., "great", "cold", "late") for specific suppliers.
* **Manual RAG Chatbot:** A custom-built Retrieval-Augmented Generation (RAG) pipeline. It bypasses standard framework limitations by manually orchestrating `OpenAI` and `ChromaDB` to allow managers to chat with data in plain English.

---

## 🗺️ VoC Agent: Roadmap for RAG System with Agents

**Transforming event reviews into actionable insights through an intelligent agent.**

---

### 📅 Week 1: Data Foundation & Basic RAG

**Goal:** Prepare data and establish the semantic retrieval pipeline.

* [ ] **Pre-processing:**

  * Run `scripts/preprocess.py` to generate `reviews_processed.csv`
  * Add `Event_Date` (last 6 months) and `sentiment` classification (TextBlob)
  * Validate distribution: ~33% Positive/Negative/Mixed

* [ ] **ChromaDB Setup:**

  * Implement `backend/app/db/chroma_client.py` (client + collection)
  * Populate vector store with processed reviews + metadata (date, sentiment, vendors)
  * Test basic queries: "problems with catering", "praise for the DJ"

* [ ] **Retrieval Tool (first tool):**

  * Create `backend/app/tools/retrieval_tool.py`
  * Implement filters: `{"sentiment": "Negative", "date": {"$gte": "2024-12-01"}}`
  * Manual test: retrieve negative reviews from the past 30 days

**Deliverable:** Functional ChromaDB with 1000 reviews + tested basic retrieval.

---

### 📅 Week 2: ReAct Agent + Visualization Tools

**Goal:** Build an autonomous agent capable of analyzing VoC and generating plots.

* [ ] **ReAct Agent (Strands or LangChain):**

  * Implement `backend/app/agent.py` with local Ollama
  * Prompt engineering: "You are an event VoC analyst. Use tools to answer."
  * Test CoT: agent explains reasoning before using tools

* [ ] **Plot Tools (3 types):**

  * `plot_sentiment_tool.py`: Bar chart (Positive/Negative/Mixed)
  * `plot_trends_tool.py`: Sentiment timeline by month
  * `plot_themes_tool.py`: Wordcloud or topic count (DJ vs Catering)

* [ ] **Observability (LangFuse):**

  * Integrate callbacks to track: tool calls, latency, tokens
  * LangFuse dashboard: monitor agent response quality

**Deliverable:** Agent responds to "Show sentiment about DJs" → retrieval + automatic plot.

---

### 📅 Week 3: FastAPI + Agent Endpoints

**Goal:** Expose the agent through a REST API for frontend consumption.

* [ ] **FastAPI Backend:**

  * `backend/app/main.py`: `POST /api/chat` endpoint (receives question, returns response + plots)
  * `backend/app/config.py`: Centralize settings (ChromaDB path, Ollama URL)
  * Health check: `GET /health` validates ChromaDB + Ollama

* [ ] **Plot Serialization:**

  * Tools return Plotly JSON (`fig.to_dict()`)
  * API response: `{"text": "...", "plot": {...}, "sources": [...]}`

* [ ] **CORS + Docs:**

  * Enable CORS for Gradio to consume API
  * Auto-generated Swagger available at `/docs`

**Deliverable:** API running on `localhost:8000`, testable via Postman/cURL.

---

### 📅 Week 4: Gradio Frontend + Full Loop

**Goal:** Conversational interface for PM/CS teams to query VoC insights.

* [ ] **Gradio UI:**

  * `frontend/app.py`: Chat consuming `POST /api/chat`
  * Render Plotly charts in side panel
  * Conversation history persisted per session

* [ ] **UX Refinements:**

  * Loading indicator while agent "thinks"
  * Show intermediate steps (tool calls) for transparency
  * "New conversation" button (reset context)

* [ ] **Local Deployment:**

  * Docker Compose: ChromaDB + Ollama + Backend + Frontend
  * README with setup instructions

**Deliverable:** End-to-end system functional.
PM asks *"What were the main issues in December?"* → agent returns analysis + charts.

---

### 🎯 Validation Milestones

**MVP 1 (Week 2):** Standalone agent (CLI) responds using retrieval + plots.
**MVP 2 (Week 3):** API exposed and testable via Swagger.
**MVP 3 (Week 4):** Full Gradio interface, demo-ready for stakeholders.

---

### 📈 Future Improvements (Post-MVP)

* **Week 5+:** Prediction tool (scikit-learn) to detect high-risk events
* **Week 6+:** Automated ingestion via webhook (`POST /api/ingest`)
* **Week 7+:** Multi-agent system: one for analysis, one for recommendations
---

## 🏛️ Architecture Diagram (V1)

This project currently uses a 2-phase "Smart Hack" architecture to ensure sub-3-second load times on Streamlit Cloud.

![Architecture Diagram](voc-pulse-architecture.png)

### How It Works: The 2-Phase Architecture

1.  **Phase 1: Offline AI Processing (The "Hack")**
    * The `scripts/run_pipeline.py` script is executed **locally**.
    * It processes raw CSV data via OpenAI API (Chat + Embeddings).
    * It saves the result to `data/processed/data_enriched.json`, which is **committed to the repository**.

2.  **Phase 2: Instant-Load Streamlit App (The "App")**
    * The `app.py` acts as the Maestro.
    * It **instantly** reads the pre-processed JSON.
    * It loads embeddings into an **in-memory** `ChromaDB`.
    * The `pages/` (Dashboard, Chatbot) read directly from the session cache.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM & Embeddings:** OpenAI API
* **Orchestration:** Manual RAG (Python) -> *Moving to LangChain (V2)*
* **Vector Database:** ChromaDB (in-memory)
* **Data Viz:** Plotly (Interactive), Matplotlib, Seaborn, WordCloud
* **Data Science:** Pandas, Scikit-learn
* **Config:** PyYAML, python-dotenv

---

## 🏃 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/username/VoC-Pulse.git](https://github.com/username/VoC-Pulse.git)
    cd VoC-Pulse
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (Windows: .\venv\Scripts\activate)
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Secrets:**
    * Create `.streamlit/secrets.toml`:
        ```toml
        OPENAI_API_KEY = "sk-..."
        ```

5.  **Run the Pipeline (One-Time Setup):**
    ```bash
    python scripts/run_pipeline.py
    ```

6.  **Launch the App:**
    ```bash
    streamlit run app.py
    ```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
