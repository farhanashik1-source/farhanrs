# Real Estate Data Cleaning and AI Marketing Pipeline

A lightweight, production-ready Python pipeline designed to ingest raw property listings, validate financial and attribute data using strict Pydantic guardrails, and enrich verified properties with AI-generated marketing hooks via the Claude API.

## Why This Project Exists

In real estate tech and automation, incoming listing data from MLS feeds, broker exports, and manual submissions is notoriously messy. Common issues like negative prices, missing square footage, or broken strings can cause downstream errors or waste expensive LLM token credits.

This pipeline solves that problem by acting as a strict quality gatekeeper. It automatically catches and isolates corrupted records before sending clean listings to Claude, ensuring high data hygiene, zero wasted API calls, and reliable outputs.

---

## Architecture and Workflow

Raw CSV (raw_properties.csv)
       |
       v
Pandas Ingestion and Pydantic Validation Gatekeeper
       |-- [BAD DATA] --> Isolated and Logged in Quarantine Stream
       `-- [VALID]    --> Sent to Anthropic Claude API (claude-haiku-4-5)
                               |
                               v
                    Clean Output CSV (clean_properties.csv)

1. Ingestion (Pandas): Ingests raw batch property feeds from local files or database exports.
2. Schema Guardrails (Pydantic): Enforces strict types and constraints (price > 0, square footage > 0). Any record violating constraints triggers a [RISK ALERT] log and gets quarantined without crashing the execution loop.
3. AI Marketing Generation (Anthropic SDK): Sends verified property parameters to Claude to generate high-converting, single-sentence property descriptions.
4. Structured Export: Saves validated listing records alongside their AI marketing hooks directly to clean_properties.csv.

---

## Tech Stack

* Language: Python 3.9+
* Data Processing: Pandas
* Data Quality and Validation: Pydantic
* AI and LLM Orchestration: Anthropic Python SDK (Claude API)
* Environment Management: python-dotenv

---

## Live Terminal Output and Quarantine Logs

When running pipeline.py, the validation guardrails actively inspect rows and quarantine anomalies before firing API requests:

--- Starting Real Estate Automation Pipeline ---

[RISK ALERT] Quarantined row 1 due to invalid data: {'property_id': '102', 'address': '456 Oak Rd', 'price': -150000.0, 'square_feet': 1200, 'status': 'active'}

--- Verification Complete ---
Valid records processed: 3
Bad records caught and quarantined: 1

--- Generating AI Marketing Hooks for Valid Listings ---
Listing ID 101: Charming 900 sq ft gem at 321 Elm Street-$300,000 and ready to be your story.
Listing ID 103: Spacious 1,800 sq ft home at 789 Pine Ave offering prime location and luxury living for $520,000.
Listing ID 104: Cozy 1,100 sq ft residence at 101 Maple Drive priced at $275,000-ideal for first-time buyers.

---

## Final Enriched Output (clean_properties.csv)

Valid entries are automatically structured and saved into a ready-to-use CSV file:

| property_id | address | price | square_feet | status | ai_marketing_hook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | 321 Elm Street | $300,000 | 900 | active | Charming 900 sq ft gem at 321 Elm Street-$300,000 and ready to be your story. |
| 103 | 789 Pine Ave | $520,000 | 1,800 | active | Spacious 1,800 sq ft home at 789 Pine Ave offering prime location... |
| 104 | 101 Maple Drive | $275,000 | 1,100 | active | Cozy 1,100 sq ft residence at 101 Maple Drive priced at $275,000... |

---

## Quick Start Guide

### 1. Clone the Repository
git clone https://github.com/farhanashik1-source/farhanrs.git
cd farhanrs

### 2. Set Up Virtual Environment and Dependencies
python3 -m venv venv
source venv/bin/activate
pip install pandas pydantic anthropic python-dotenv

### 3. Configure API Key
Create a .env file in the project root:
ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here

### 4. Run the Pipeline
python pipeline.py
