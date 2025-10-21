# DeclanRiceBot

A lightweight Discord bot that shares the love for Declan Rice **and** fetches live Arsenal stats using publicly available data from [TheSportsDB](https://www.thesportsdb.com/).

## Features

- Friendly small-talk responses for Rice fans.
- `!arsenal`, `!arsenal stats`, `!arsenal latest`, or `!arsenal next` – get Arsenal's current Premier League position plus the latest and upcoming fixtures.
- Supports private replies by prefixing commands with `?` (for example, `?!arsenal stats`).

## Getting started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file next to `main.py` containing your Discord bot token:
   ```env
   DISCORD_TOKEN=your-token-here
   ```
3. Run the bot:
   ```bash
   python main.py
   ```

If the live data provider is temporarily unavailable, the bot will gracefully inform the user instead of failing.
