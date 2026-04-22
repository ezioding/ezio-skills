# ezio-skills

个人 Hermes Agent Skills 集合。

---

## 📚 可用 Skills

### 📊 daily-market-report

自动化每日市场数据报告生成和发送工作流。自动获取股票和加密货币实时数据，生成技术面分析报告并通过邮件发送。

**安装：**
```bash
# Claude Code
cp -r skills/daily-market-report ~/.claude/skills/

# Hermes
cp -r skills/daily-market-report ~/.hermes/skills/
```

**使用：**
```bash
cd ~/.hermes/skills/daily-market-report
./install.sh
```

**前提条件：**
- Node.js (>= 14.x)
- crypto-market-data skill
- Maton API Key（可选，用于邮件发送）

---

### 📈 analyze-stock

分析股票并给出交易决策（买入/卖出/持有）。基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 多智能体框架。

**安装：**
```bash
# Claude Code
cp -r skills/analyze-stock ~/.claude/skills/

# Hermes
cp -r skills/analyze-stock ~/.hermes/skills/
```

**触发示例：**
```
帮我分析 NVDA
分析 AAPL
analyze 0700.HK
```

**前提条件：**
- 已安装 `git` 和 `uv`
- LLM provider（OpenAI / Anthropic / DeepSeek / 其他中转）
- API Key

---

## 🛠️ 开发和贡献

### 目录结构

```
ezio-skills/
├── skills/                    # 所有 skills
│   ├── daily-market-report/   # 市场报告 skill
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── install.sh
│   │   ├── uninstall.sh
│   │   ├── test.sh
│   │   ├── templates/
│   │   └── references/
│   └── analyze-stock/        # 股票分析 skill
│       └── SKILL.md
└── README.md                 # 本文件
```

### 添加新 Skill

1. 在 `skills/` 目录下创建新目录
2. 添加 `SKILL.md` 文件（Hermes 技能格式）
3. 更新根目录的 `README.md`
4. 提交并推送到 GitHub

---

## 📄 许可证

MIT License

---

## 📧 联系

如有问题或建议，请提交 Issue 或 Pull Request。
