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

## 安装

运行安装脚本：

```bash
cd /path/to/daily-market-report
./install.sh
```

安装脚本会：
1. 检查依赖（Node.js, crypto-market-data skill）
2. 交互式配置参数
3. 生成配置文件
4. 创建 Cron job

## 配置

安装后配置文件位于：`~/.hermes/scripts/market_report_config.yaml`

可配置项：
- 股票列表
- 加密货币列表
- 接收邮箱
- 执行时间
- Maton API Key

## 使用

安装完成后，系统会自动创建 Cron job，每天定时执行。

手动运行：
```bash
python3 ~/.hermes/scripts/daily_market_report.py
```

## 卸载

```bash
cd /path/to/daily-market-report
./uninstall.sh
```

## 依赖

- **Node.js**: 用于运行 crypto-market-data skill 的数据采集脚本
- **crypto-market-data skill**: 用于获取股票和加密货币数据
- **Maton API Key**: 用于发送邮件（可选）

## 详细文档

查看 `references/` 目录获取更详细的文档：
- `installation.md` - 安装指南
- `configuration.md` - 配置说明
- `usage.md` - 使用指南
- `troubleshooting.md` - 故障排除
- `api-dependencies.md` - API 依赖说明
