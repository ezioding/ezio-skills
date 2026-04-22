# Daily Market Report

> 自动化每日市场数据报告生成和发送工作流

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 功能特性

- 自动获取股票和加密货币实时数据
- 技术面分析（50/200日均线、成交量、年内表现）
- 生成投资建议和决策简报
- 自动发送邮件到指定邮箱
- Cron job: 定时执行
- 交互式安装和配置
- 完善的错误处理和降级方案

## 示例报告

报告包含以下内容：

### 执行摘要
- 股票平均涨跌幅
- 今日最佳/最差表现
- 总市值统计

### 实时价格数据
- 股票价格表（代码、公司、当前价、涨跌幅、成交量、市值）
- 加密货币价格表

### 技术分析
- 50/200日均线分析
- 成交量分析
- 年内表现分析

### 投资建议
- 技术面状态
- 投资建议和配置比例
- 风险提示

## 快速开始

### 前置要求

- [x] Hermes Agent 已安装
- [x] Node.js (>= 14.x)
- [x] Python 3.7+
- [x] crypto-market-data skill

### 安装

1. 克隆仓库
```bash
git clone https://github.com/ezioding/ezio-skills.git
cd ezio-skills/daily-market-report
```

2. 运行安装脚本
```bash
chmod +x install.sh
./install.sh
```

3. 按照提示配置
- `股票列表`: AMD,NVDA,TSM,AAPL,GOOGL（默认）
- `加密货币列表`: bitcoin,ethereum,solana（默认）
- `接收邮箱`: 必需输入
- `执行时间`: 0 1 * * *（默认，每天 UTC 1:00 / 北京 9:00）
- `Maton API Key`: 可选

4. 验证安装
```bash
./test.sh
```

## 使用

### 自动执行

安装完成后，系统会自动创建 Cron job，每天定时执行。

### 手动执行

```bash
python3 ~/.hermes/scripts/daily_market_report.py
```

### 查看 Cron job 状态

```bash
hermes cronjob list:1
```

### 手动触发执行

```bash
hermes cronjob run <job_id>
```

## 配置

配置文件位置：`~/.hermes/scripts/market_report_config.yaml`

```yaml
# 监控的股票列表（雅虎财经代码）
stocks:
  - AMD
  - NVDA
  - TSM
  - AAPL
  - GOOGL

# 监控的加密货币列表（CoinGecko ID）
cryptos:
  - bitcoin
  - ethereum
  - solana

# 接收邮件的邮箱地址
recipient_email: "your_email@example.com"

# Maton API Key（用于发送邮件）
maton_api_key: ""

# Cron 调度表达式
schedule: "0 1 * * *"
```

## 测试

运行测试脚本：

```bash
./test.sh
```

测试内容：
- Node.js 是否安装
- crypto-market-data skill 是否存在
- 配置文件格式是否正确
- 脚本语法是否正确
- 数据采集是否正常

## 卸载

```bash
./uninstall.sh
```

卸载脚本会：
- 删除 Cron job
- 询问是否删除配置文件
- 询问是否删除脚本文件

## 详细文档

查看 `references/` 目录获取更详细的文档：

- [`installation.md`](references/installation.md) - 安装指南
- [`configuration.md`](references/configuration.md) - 配置说明
- [`usage.md`](references/usage.md) - 使用指南
- [`troubleshooting.md`](references/troubleshooting.md) - 故障排除
- [`api-dependencies.md`](references/api-dependencies.md) - API 依赖说明

## 依赖

- [crypto-market-data](https://github.com/) - 股票和加密货币数据获取
- [Hermes Agent](https://github.com/) - Cron job 管理
- [Maton](https://maton.ai/) - 邮件发送

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系

如有问题，请创建 Issue 或联系维护者。
