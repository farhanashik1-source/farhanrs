# Real Estate Data Cleaning & AI Enrichment Pipeline

An automated Python script designed to ingest raw property transaction data, apply strict Pydantic verification schemas to eliminate financial risks (like negative pricing errors), and enrich verified listings using the Claude API.

## Features
- **Data Guardrails:** Uses Pydantic data modeling to catch anomalies before database commits.
- **AI Integration:** Dynamically generates marketing content via Claude.
- **Risk Mitigation:** Isolates dirty or corrupted rows into a quarantine log.

## Quick Start
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your Anthropic API key in your terminal: `export ANTHROPIC_API_KEY="your_key"`
4. Run the script: `python pipeline.py`