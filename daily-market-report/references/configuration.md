# 配置说明

配置文件位置：`~/.hermes/scripts/market_report_config.yaml`

## 配置项

### stocks

监控的股票列表（雅虎财经代码）

```yaml
stocks:
  - AMD
  - NVDA
  - TSM
  - AAPL
  - GOOGL
```

### cryptos

监控的加密货币列表（CoinGecko ID）

```yaml
cryptos:
  - bitcoin
  - ethereum
  - solana
```

### recipient_email

接收报告的邮箱地址（必需）

```yaml
recipient_email: "your_email@example.com"
```

### maton_api_key

Maton API Key（可选）

```yaml
maton_api_key: "your_api_key"
```

### schedule

Cron 调度表达式

```yaml
schedule: "0 1 * * *"  # 每天 UTC 1:00
```

常用示例：
- `0 1 * * *` - 每天 UTC 1:00（北京时间 9:00）
- `0 9 * * 1` - 每周一 UTC 9:00
- `30 8 * * 1-5` - 工作日 8:30 UTC
- `0 */6 * * *` - 每 6 小时

## 修改配置

编辑配置文件：

```bash
nano ~/.hermes/scripts/market_report_config.yaml
```

修改后需要重启或重新创建 Cron job。
