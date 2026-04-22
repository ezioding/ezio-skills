---
name: daily-market-report
description: >
  自动化每日市场数据报告生成和发送工作流。监控股票和加密货币，生成详细的技术面分析报告。
  自动创建 Cron job，每天定时执行。
tags: [automation, market-data, cron-job, investment]
---

# Daily Market Report

## 用途

每天自动生成并发送市场数据报告，包括：
- 股票实时价格和技术指标（50/200日均线、成交量、年内表现）
- 加密货币价格
- 技术面分析和投资建议
- 邮件发送到指定邮箱

## 安装流程

**必须在安装前通过 AskUserQuestion 完成以下所有配置收集，不得跳过任何项目。**

### 第一步：收集监控标的（必问）

使用 AskUserQuestion 询问：

**问题1 - 股票列表：**
- 问题：`您想监控哪些股票？（雅虎财经代码，逗号分隔）`
- 选项1：`保留默认：NVDA, TSM, AMD, AAPL, GOOGL`
- 选项2：`我来自定义`（提示用户通过 Other 输入框填写，示例：`NVDA,TSM,AMD,AAPL,GOOGL,QQQ,TTWO`）

**问题2 - 加密货币列表：**
- 问题：`您想监控哪些加密货币？（CoinGecko ID，逗号分隔）`
- 选项1：`保留默认：bitcoin, ethereum, solana`
- 选项2：`我来自定义`（提示用户通过 Other 输入框填写，示例：`bitcoin,ethereum,solana`）

**问题3 - 接收邮箱：**
- 问题：`报告接收邮箱？`
- 选项1：`916505542@qq.com（默认）`
- 选项2：`其他邮箱`

**问题4 - Maton API Key：**
- 问题：`是否有 Maton API Key？（用于发送邮件）`
- 选项1：`有，稍后我自己填入配置文件`
- 选项2：`没有，保存报告到本地文件`

### 第二步：检查依赖

1. 检查 Node.js：`node --version`
2. 检查 crypto-market-data skill：`ls ~/skills/crypto-market-data/scripts/ 2>/dev/null`
   - 未安装则运行：`skillhub install crypto-market-data`
   - skillhub 路径可能在 `~/.local/bin/skillhub`

### 第三步：生成配置文件

根据用户输入写入 `~/.hermes/scripts/market_report_config.yaml`：

```yaml
stocks:
  - STOCK1
  - STOCK2
cryptos:
  - crypto1
  - crypto2
recipient_email: "user@example.com"
maton_api_key: ""
schedule: "0 1 * * *"
```

### 第四步：安装脚本

从模板复制并修改 Python 脚本到 `~/.hermes/scripts/daily_market_report.py`：

- 将 `CRYPTO_SKILL_PATH` 改为实际安装路径（通常为 `/Users/<username>/skills/crypto-market-data`）
- 确保脚本从配置文件读取 STOCKS 和 CRYPTOS（不硬编码）
- 无 Maton API Key 时保存报告到 `~/.hermes/reports/`

### 第五步：定时任务

根据用户在第一步选择的方式创建定时任务（参见下方「定时任务方式」）。

### 第六步：验证

运行一次确认数据正常获取：
```bash
python3 ~/.hermes/scripts/daily_market_report.py
```

---

## 定时任务方式

### 方式1：Claude Code 远程触发器（推荐，无需 hermes）

```bash
# 通过 RemoteTrigger API 创建定时任务
# Claude Code 内置支持，无需额外安装
```

### 方式2：系统 crontab

```bash
crontab -e
# 添加：0 9 * * 1-5 python3 ~/.hermes/scripts/daily_market_report.py
```

### 方式3：hermes cronjob（需要 hermes CLI）

```bash
hermes cronjob create \
  --name "Daily Market Report" \
  --prompt "执行每日市场报告脚本：python3 ~/.hermes/scripts/daily_market_report.py" \
  --schedule "0 1 * * *" \
  --deliver origin
```

---

## 手动运行

```bash
python3 ~/.hermes/scripts/daily_market_report.py
```

## 配置文件

位于：`~/.hermes/scripts/market_report_config.yaml`

可直接编辑修改股票/加密货币列表，修改后立即生效（无需重启）。

## 卸载

```bash
cd /path/to/daily-market-report
./uninstall.sh
```

## 依赖

- **Node.js**: 用于运行 crypto-market-data skill 的数据采集脚本
- **crypto-market-data skill**: 用于获取股票和加密货币数据（`skillhub install crypto-market-data`）
- **Maton API Key**: 用于发送邮件（可选）

## 详细文档

查看 `references/` 目录获取更详细的文档：
- `installation.md` - 安装指南
- `configuration.md` - 配置说明
- `usage.md` - 使用指南
- `troubleshooting.md` - 故障排除
- `api-dependencies.md` - API 依赖说明
