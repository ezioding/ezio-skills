# ezio-skills

个人 Hermes Agent Skills 集合。

---

## 📚 可用 Skills

### 📊 daily-market-report

自动化每日市场数据报告生成和发送工作流。

**功能特性：**
- 📊 自动获取股票和加密货币实时数据
- 📈 技术面分析（50/200日均线、成交量、年内表现）
- 💡 生成投资建议和决策简报
- 📧 自动发送邮件到指定邮箱
- ⏰ Cron job 定时执行

**快速开始：**
```bash
cd skills/daily-market-report
./install.sh
```

**监控标的：**
- 股票：AMD, NVDA, TSM, AAPL, GOOGL（可自定义）
- 加密货币：Bitcoin, Ethereum, Solana（可自定义）

**依赖：**
- Node.js (>= 14.x)
- crypto-market-data skill
- Maton API Key（可选，用于邮件发送）

**详细文档：**
- [安装指南](skills/daily-market-report/references/installation.md)
- [配置说明](skills/daily-market-report/references/configuration.md)
- [使用指南](skills/daily-market-report/references/usage.md)
- [故障排除](skills/daily-market-report/references/troubleshooting.md)

---

### 📈 analyze-stock

分析股票并给出交易决策（买入/卖出/持有）。基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 多智能体框架。

**触发方式：**
```bash
帮我分析 NVDA
analyze AAPL 2026-04-22
分析一下 0700.HK
```

**支持股票：**
- 美股（NVDA、AAPL 等）
- 港股（0700.HK 格式）
- A 股（需 yfinance 支持）

**首次使用**会自动完成 TradingAgents 安装和配置，只需提供：
- LLM provider（OpenAI / Anthropic / DeepSeek / 其他中转）
- API Key

**前提条件：** 已安装 `git` 和 `uv`

---

## 🚀 安装

### 安装单个 Skill

将需要的 skill 目录复制到 `~/.hermes/skills/`：

```bash
# 安装 daily-market-report
cp -r skills/daily-market-report ~/.hermes/skills/

# 安装 analyze-stock
cp -r skills/analyze-stock ~/.hermes/skills/
```

### 使用 SkillHub 安装（推荐）

如果 skill 已发布到 SkillHub：

```bash
skillhub install daily-market-report
skillhub install analyze-stock
```

---

## 📖 使用方法

### daily-market-report

```bash
cd ~/.hermes/skills/daily-market-report

# 交互式安装
./install.sh

# 运行测试
./test.sh

# 手动执行
python3 ~/.hermes/scripts/daily_market_report.py

# 卸载
./uninstall.sh
```

### analyze-stock

安装后在 Hermes 中直接使用：

```
帮我分析 NVDA 股票
```

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
