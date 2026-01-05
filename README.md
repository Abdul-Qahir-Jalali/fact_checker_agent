# 🔍 Fact Checker Agent

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)

A powerful, AI-driven fact-checking system that uses a hybrid **Local Client + Cloud Server** architecture to verify statements with real-time web search.


## 🚀 Features

- **🧠 Intelligent Analysis:** Uses **Groq LLM (Llama 3)** to break down complex statements into verifiable claims.
- **☁️ Hybrid Architecture:**
  - **Local Client:** Runs the AI logic and orchestration using the custom **DO Framework** (Directives-Orchestration-Execution).
  - **Cloud Server:** Custom **FastMCP + FastAPI** server deployed on Hugging Face to perform web searches via Tavily.
- **⚡ Real-time Verification:** Fetches live data from the web to verify or refute claims.
- **🎨 Modern Web UI:** Beautiful, high-contrast interface built with HTML/CSS and served via FastAPI.
- **🔄 State Management:** Powered by **LangGraph** for robust workflow orchestration.

## 🏗️ Architecture: The DO Framework

This project implements a custom **Directives-Orchestration-Execution (DO)** pattern:

1.  **Directives (`src/directives/`):** logic defining *HOW* to analyze and verify (AI Prompts).
2.  **Orchestration (`src/orchestration/`):** logic defining *WHEN* steps happen (LangGraph workflow).
3.  **Execution (`src/execution/`):** logic defining *actions* (HTTP calls to the search server).

## 🛠️ Tech Stack

- **AI/LLM:** LangChain, ChatGroq (Llama 3.1)
- **Orchestration:** LangGraph
- **Backend:** FastAPI, Uvicorn
- **Search:** Tavily API (via custom MCP Server)
- **Frontend:** Vanilla HTML/CSS/JS

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/fact_checker_agent.git
    cd fact_checker_agent
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_key
    TAVILY_API_KEY=your_tavily_key
    MCP_SERVER_URL=https://your-deployed-server-url.hf.space
    ```

## 🚀 Usage

1.  **Start the UI Server:**
    ```bash
    python ui_server.py
    ```

2.  **Open in Browser:**
    Navigate to `http://localhost:8000`

3.  **Verify Facts:**
    Enter any statement (e.g., *"Islamabad is the capital of India"*) and hit Enter!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
