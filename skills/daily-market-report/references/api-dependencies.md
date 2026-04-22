# API 依赖说明

本 skill 依赖以下服务和 API。

## 数据源 API

### 股票数据

**来源：** crypto-market-data skill  
**底层服务：** Yahoo Finance API

**获取方式：**
- 股票代码（雅虎财经格式）
- 实时价格
- 涨跌幅
- 50/200日均线
- 成交量
- 年内高/低点

**API 限制：**
- Yahoo Finance 免费层有请求频率限制
- 建议监控的股票数量 < 20

**数据更新频率：**
- 实时数据（市场开放时）
- 延迟 15-20 分钟（某些市场）

---

### 加密货币数据

**来源：** crypto-market-data skill  
**底层服务：** CoinGecko API

**获取方式：**
- 加密货币 ID（CoinGecko 格式）
- USD 价格
- 24h 涨跌幅

**API 限制：**
- 免费层：10-50 次/分钟
- 建议监控的加密货币数量 < 10

**数据更新频率：**
- 实时价格

---

## 邮件发送 API

### Maton API

**用途：** 发送邮件报告  
**文档：** https://maton.ai/

**必需配置：**
- `maton_api_key` - Maton API Key

**API 限制：**
- 取决于你的 Maton 账户计划

**降级方案：**
- 如果 API Key 未配置或发送失败
- 报告会保存到本地文件：`~/.hermes/reports/market_report.md`

---

## Cron Job 管理 API

### Hermes Agent

**用途：** 管理 Cron job 调度

**主要命令：**
```bash
hermes cronjob list           # 列出所有 jobs
hermes cronjob create         # 创建 job
hermes cronjob run <id>      # 手动运行
hermes cronjob pause <id>     # 暂停
hermes cronjob resume <id>    # 恢复
hermes cronjob remove <id>    # 删除
hermes cronjob log <id>       # 查看日志
```

---

## 网络依赖

### 所需网络访问

- ✅ Yahoo Finance API（股票数据）
- ✅ CoinGecko API（加密货币数据）
- ✅ Maton Gateway（邮件发送，可选）

### 防火墙配置

确保以下域名可访问：

- `finance.yahoo.com`
- `api.coingecko.com`
- `gateway.maton.ai`（如果使用邮件发送）

### 代理配置

如果需要使用代理，设置环境变量：

```bash
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080
```

---

## API 故障恢复

### 股票数据 API 故障

**症状：** 股票数据获取失败  
**影响：** 报告中缺少股票数据  
**恢复：** 继续生成报告，标注数据缺失

### 加密货币数据 API 故障

**症状：** 加密货币数据获取失败  
**影响：** 报告中缺少加密货币数据  
**恢复：** 继续生成报告，标注数据缺失

### 邮件 API 故障

**症状：** 邮件发送失败  
**影响：** 报告保存到本地文件  
**恢复：** 自动降级到本地文件保存

---

## 更新和维护

### API 变更通知

建议定期检查：
- crypto-market-data skill 更新
- API 文档变更
- Hermes Agent 版本更新

### 手动更新依赖

```bash
# 更新 crypto-market-data skill
skillhub install crypto-market-data --update

# 更新 Hermes Agent
hermes update
```
