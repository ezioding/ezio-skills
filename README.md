# ezio-skills

Claude Code 个人 skill 集合。

## 安装

将需要的 skill 目录复制到 `~/.claude/skills/`：

```bash
cp -r skills/analyze-stock ~/.claude/skills/
```

## 可用 Skills

### analyze-stock

分析股票并给出交易决策（买入/卖出/持有）。基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 多智能体框架。

**首次使用**会自动完成 TradingAgents 安装和配置，只需提供：
- LLM provider（OpenAI / Anthropic / DeepSeek / 火山引擎 / 其他中转）
- API Key

**触发方式：**
- `帮我分析 NVDA`
- `analyze AAPL 2026-04-22`
- `分析一下 0700.HK`

**支持股票：** 美股（NVDA、AAPL 等）、港股（0700.HK 格式）、A 股（需 yfinance 支持）

**前提条件：** 已安装 `git` 和 `uv`
