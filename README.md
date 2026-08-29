# Task-Bot

Lightweight Telegram multi-session worker scaffold with MongoDB and isolated Firefox support.

## Setup

1. Install Python 3.x, Firefox, and GeckoDriver.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Edit `config.py` with local configuration. Do not commit real tokens, session strings, passwords, or other secrets.
4. Run:

```bash
python main.py
```

## Structure

- `main.py` — application entrypoint
- `config.py` — configuration
- `telegram_worker.py` — Telegram/session layer
- `task_worker.py` — task state/lifecycle
- `browser.py` — isolated Firefox profiles
- `database.py` — MongoDB
- `logger.py` — lightweight logging
