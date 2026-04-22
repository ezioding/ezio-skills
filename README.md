# ezio-skills

个人 Claude Code Skills 集合。

## 安装

```bash
npx github:ezioding/ezio-skills
```

交互式选择要安装的 skill，安装到 `~/.claude/skills/`。

**选项：**

```bash
# 列出可用 skills
npx github:ezioding/ezio-skills --list

# 安装全部，跳过确认
npx github:ezioding/ezio-skills -y

# 强制覆盖已有文件
npx github:ezioding/ezio-skills --force

# 自定义安装目录
npx github:ezioding/ezio-skills --install-dir /path/to/claude
```

---

## 可用 Skills

### 📈 analyze-stock

分析股票并给出交易决策（买入/卖出/持有）。基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 多智能体框架。

**触发示例：**
```
帮我分析 NVDA
分析 AAPL
analyze 0700.HK
```

**前提条件：**
- `git` 和 `uv`
- LLM API Key（OpenAI / Anthropic / DeepSeek 等）

---

### 📊 daily-market-report

自动化每日市场数据报告生成与邮件发送。监控股票和加密货币，生成技术面分析报告。

**使用：**
```bash
/daily-market-report
```

**前提条件：**
- Node.js (>= 14.x)
- crypto-market-data skill
- Maton API Key（可选，用于邮件发送）

---

## 目录结构

```
ezio-skills/
├── bin/
│   └── install.js          # npx 安装脚本
├── analyze-stock/
│   └── SKILL.md
├── daily-market-report/
│   ├── SKILL.md
│   ├── templates/
│   └── references/
├── package.json
└── README.md
```

## 添加新 Skill

1. 在根目录创建新目录（如 `my-skill/`）
2. 添加 `SKILL.md` 文件
3. 更新本 `README.md`

---

## 许可证

MIT License
