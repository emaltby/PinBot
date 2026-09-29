# PinBot 📌🤖

PinBot is an automated pinball machine listing scraper and notifier. It monitors platforms like Facebook Marketplace for target pinball machines, performs robust fuzzy name matching (handling typos, spelling variations, and formatting differences), logs new listings, and sends email alerts when matches are found. It also includes a Flask-based Web UI for managing configuration and viewing seen listings.

---

## Features

- **Automated Scrapers**: Scrapes Facebook Marketplace for pinball listings.
- **Robust Machine Name Matching**: Advanced normalization, token similarity, and fuzzy string matching (`difflib`) to accurately match target machines even with typos, abbreviations, or formatting differences (e.g., "Medievall Madness" matching "Medieval Madness").
- **Email Notifications**: Alerts you instantly via SMTP when a new matching listing appears within price and time constraints.
- **Web UI**: Flask application to view scraped listings and dynamically update target keywords and target machines.
- **Docker Support**: Containerized setup for running the scraper and Web UI reliably.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Playwright (for browser automation)

### Installation

1. Clone the repository and navigate to the project directory.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Copy `.env.example` to `.env` and configure your SMTP settings and environment variables:
   ```bash
   cp .env.example .env
   ```

---

## Useful Commands

### 1. Running Unit Tests
To run the complete test suite (matcher tests, database deduplication tests, and main loop tests):
```bash
python3 -m unittest discover tests
```

### 2. Running the Scraper Bot Locally
```bash
python3 main.py
```

### 3. Running the Web UI Locally
```bash
python3 web_ui.py
```
*(Access the Web UI at `http://localhost:5000`)*

### 4. Running with Docker (Recommended)
To build and run both the scraper service and the Web UI in Docker containers:
```bash
docker compose up --build
```

To run in detached mode (background):
```bash
docker compose up -d --build
```

To stop the Docker containers:
```bash
docker compose down
```

---

## Configuration

- **Target Machines & Keywords**: Configured via `data/config.json` or dynamically through the Web UI.
- **Environment Variables (`.env`)**:
  - `DB_PATH`: Path to SQLite database (default: `listings.db`)
  - `EMAIL_SENDER`: Sender email address for alerts
  - `EMAIL_PASSWORD`: Email app password / SMTP password
  - `EMAIL_RECEIVER`: Recipient email address
  - `SMTP_SERVER`: SMTP server hostname (default: `smtp.gmail.com`)
  - `SMTP_PORT`: SMTP server port (default: `587`)
