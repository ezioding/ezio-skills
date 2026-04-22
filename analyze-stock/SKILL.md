---
name: analyze-stock
description: Use when the user asks to analyze a stock, get a trading decision, or run TradingAgents on a ticker. Triggers on phrases like "analyze NVDA", "分析股票", "帮我分析", "/analyze NVDA 2026-04-22". Includes automatic first-time setup of TradingAgents.
---

# analyze-stock

## Overview

Analyze a stock ticker using TradingAgents multi-agent framework and return a trading decision (buy/sell/hold) with full report.

First-time use automatically installs TradingAgents and configures your LLM provider. Subsequent uses run instantly from saved config.

## Step 1: Check Setup

Run this first to determine which path to take:

```bash
test -f ~/.tradingagents-claude.env && echo "CONFIGURED" || echo "NEEDS_SETUP"
```

- If output is `CONFIGURED` → skip to **Step 3: Run Analysis**
- If output is `NEEDS_SETUP` → continue to **Step 2: Setup**

## Step 2: First-Time Setup

### 2a. Check prerequisites

```bash
which git && which uv && echo "OK" || echo "MISSING"
```

If `MISSING`: tell user to install missing tools:
- git: https://git-scm.com
- uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2b. Clone and install TradingAgents

```bash
git clone https://github.com/TauricResearch/TradingAgents.git ~/TradingAgents
cd ~/TradingAgents
uv venv .venv --python 3.13
uv pip install .
```

### 2c. Ask the user (only 2 questions)

**Question 1:** Which LLM provider do you use?

Present these options:
1. OpenAI (gpt-4o)
2. Anthropic (claude-sonnet-4-6)
3. DeepSeek (deepseek-chat)
4. 火山引擎 / Volcano Engine (glm-4.7, OpenAI-compatible)
5. Other OpenAI-compatible endpoint

**Question 2:** Please provide your API key (and base_url if you chose option 4 or 5).

### 2d. Map provider to config values

Use this mapping to determine config values:

| Choice | LLM_PROVIDER | DEEP_MODEL | QUICK_MODEL | needs BASE_URL |
|--------|-------------|-----------|------------|----------------|
| 1 OpenAI | openai | gpt-4o | gpt-4o-mini | No |
| 2 Anthropic | anthropic | claude-sonnet-4-6 | claude-haiku-4-5-20251001 | No |
| 3 DeepSeek | deepseek | deepseek-chat | deepseek-chat | No |
| 4 火山引擎 | openrouter | glm-4.7 | glm-4.7 | Yes |
| 5 Other | openrouter | (ask user) | (same) | Yes |

### 2e. Write config file

Write the following to `~/.tradingagents-claude.env` using actual values from user input and the mapping above:

```
TRADINGAGENTS_DIR=~/TradingAgents
LLM_PROVIDER=<value from mapping>
DEEP_MODEL=<value from mapping>
QUICK_MODEL=<value from mapping>
API_KEY=<user provided>
BASE_URL=<user provided, or leave empty if not needed>
OUTPUT_LANGUAGE=Chinese
```

Tell user: "Setup complete! Config saved to ~/.tradingagents-claude.env"

## Step 3: Run Analysis

### 3a. Parse ticker and date from user message

- Ticker: the stock symbol mentioned (e.g. NVDA, AAPL, 0700.HK)
- Date: mentioned date in YYYY-MM-DD format, or today's date if not specified
- HK stocks format: 4-digit code + .HK (e.g. 0700.HK, 2513.HK)

### 3b. Load config and run

```bash
set -a && source ~/.tradingagents-claude.env && set +a
cd ${TRADINGAGENTS_DIR:-~/TradingAgents}
source .venv/bin/activate
python -c "
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import os

config = DEFAULT_CONFIG.copy()
config['llm_provider'] = os.environ['LLM_PROVIDER']
config['deep_think_llm'] = os.environ['DEEP_MODEL']
config['quick_think_llm'] = os.environ['QUICK_MODEL']
config['max_debate_rounds'] = 1
config['output_language'] = os.environ.get('OUTPUT_LANGUAGE', 'Chinese')

base_url = os.environ.get('BASE_URL', '').strip()
if base_url:
    config['backend_url'] = base_url

os.environ['OPENAI_API_KEY'] = os.environ.get('API_KEY', '')
os.environ['OPENROUTER_API_KEY'] = os.environ.get('API_KEY', '')
os.environ['ANTHROPIC_API_KEY'] = os.environ.get('API_KEY', '')
os.environ['DEEPSEEK_API_KEY'] = os.environ.get('API_KEY', '')

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate('__TICKER__', '__DATE__')
print(decision)
" 2>&1
```

Replace `__TICKER__` and `__DATE__` with actual values before running.

## Step 4: Present Results

After the analysis completes (5-10 minutes), parse the output and present a structured report:

- **Final Decision** (BUY / SELL / HOLD) — prominently displayed
- **Technical Analysis** — key indicators and price levels
- **Fundamentals** — valuation, earnings
- **Sentiment** — social/news sentiment
- **Macro** — relevant macro factors
- **Risk factors** — key risks to watch

End with disclaimer: ⚠️ 仅供参考，不构成投资建议。

## Notes

- Config file: `~/.tradingagents-claude.env`
- TradingAgents default install: `~/TradingAgents`
- Analysis time: 5-10 minutes per stock
- HK stocks: use format `0700.HK` (4 digits + .HK)
- To reconfigure: delete `~/.tradingagents-claude.env` and run again
