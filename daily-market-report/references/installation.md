# 安装指南

本指南详细说明如何安装 Daily Market Report skill。

## 前置要求

### 必需依赖

1. **Hermes Agent**
   - 已安装并配置好的 Hermes Agent
   - 用于 Cron job 管理

2. **Node.js** (>= 14.x)
   - 用于运行 crypto-market-data skill 的数据采集脚本
   - 安装：访问 https://nodejs.org/

3. **Python 3** (>= 3.7)
   - 用于运行主报告脚本
   - 大多数 Linux 系统已预装

### 可选依赖

1. **Maton API Key**
   - 用于发送邮件
   - 如不设置，报告将保存到本地文件
   - 获取方式：访问 https://maton.ai/

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/ezioding/ezio-skills.git
cd ezio-skills/daily-market-report
```

### 2. 确保脚本可

执行

```bash
chmod +x install.sh uninstall.sh test.sh
```

### 3. 运行安装脚本

```bash
./install.sh
```

安装脚本会执行与其他操作：

#### 3.1 检查依赖

- 检查 Node.js 是否安装
- 检查 crypto-market-data skill 是否存在
- 如果 crypto-market-data skill 不存在，自动尝试安装

#### 3.2 交互式配置

安装脚本会提示你配置以下参数：

| 参数 | 说明 | 默认值 | 必需 |
|-----|------|--------|------|
| 股票列表 | 监控的股票代码（逗号分隔） | AMD,NVDA,TSM,AAPL,GOOGL | 否 |
| 加密货币列表 | 监控的加密货币（逗号分隔） | bitcoin,ethereum,solana | 否 |
| 接收邮箱 | 接收报告的邮箱地址 | 无 | 是 |
| 执行时间 | Cron 调度表达式 | 0 1 * * * | 否 |
| Maton API Key | 邮件发送 API Key | 无 | 否 |

**示例输入：**

```
股票列表（逗号分隔，默认: AMD,NVDA,TSM,AAPL,GOOGL）: 
加密货币列表（逗号分隔，默认: bitcoin,ethereum,solana）: 
接收邮箱: your_email@example.com
执行时间（Cron 格式，默认: 0 1 * * *）: 
Maton API Key（可选，不输入则跳过）: your_maton_api_key
```

#### 3.3 生成配置文件

配置文件会保存到：`~/.hermes/scripts/market_report_config.yaml`

#### 3.4 复制脚本模板

主脚本会复制到：`~/.hermes/scripts/daily_market_report.py`

#### 3.5 创建 Cron job

自动创建名为 "Daily Market Report" 的 Cron job

## 验证安装

### 运行测试脚本

```bash
./test.sh
```

测试脚本会检查：
- ✅ Node.js 是否安装
- ✅ crypto-market-data skill 是否存在
- ✅ 配置文件格式是否正确
- ✅ 脚本语法是否正确
- ✅ 数据采集是否正常
- ✅ Cron job 是否配置

### 查看 Cron job 状态

```bash
hermes cronjob list
```

你应该看到类似输出：

```
Name: Daily Market Report
Schedule: 0 1 * * *
Status: scheduled
Next run: 2026-04-23T01:00:00+08:00
```

### 手动运行一次

```bash
python3 ~/.hermes/scripts/daily_market_report.py
```

检查输出是否正常，并确认收到邮件（如果配置了 Maton API Key）。

## 常见问题

### Q: crypto-market-data skill 安装失败？

**A:** 手动安装：

```bash
skillhub install crypto-market-data
```

如果 skillhub 不可用，请先安装 skillhub CLI。

### Q: Cron job 创建失败？

**A:** 检查 hermes CLI 是否可用：

```bash
hermes --version
```

如果 hermes CLI 不可用，请手动创建 Cron job：

```bash
hermes cronjob create \
  --name "Daily Market Report" \
  --prompt "执行每日市场报告脚本：python3 ~/.hermes/scripts/daily_market_report.py" \
  --schedule "0 1 * * *" \
  --deliver origin
```

### Q: 如何修改配置？

**A:** 编辑配置文件：

```bash
nano ~/.hermes/scripts/market_report_config.yaml
```

修改后，需要重启 Cron job 或重新创建。

### Q: 卸载后重新安装？

**A:** 运行卸载脚本后再安装：

```bash
./uninstall.sh
./install.sh
```

## 下一步

安装完成后，请查看：
- [配置说明](configuration.md) - 了解配置选项
- [使用指南](usage.md) - 学习如何使用
- [故障排除](troubleshooting.md) - 解决常见问题
