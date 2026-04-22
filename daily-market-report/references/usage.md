# 使用指南

## 自动执行

安装完成后，Cron job 会自动每天定时执行。

## 手动执行

### 运行一次报告

```bash
python3 ~/.hermes/scripts/daily_market_report.py
```

### 使用不同的配置文件

```bash
python3 ~/.hermes/scripts/daily_market_report.py --config /path/to/config.yaml
```

## Cron Job 管理

### 查看 Cron job 状态

```bash
hermes cronjob list
```

### 手动触发执行

```bash
hermes cronjob run <job_id>
```

### 暂停 Cron job

```bash
hermes cronjob pause <job_id>
```

### 恢复 Cron job

```bash
hermes cronjob resume <job_id>
```

### 删除 Cron job

```bash
hermes cronjob remove <job_id>
```

## 报告输出

### 邮件发送

如果配置了 Maton API Key，报告会自动发送到指定邮箱。

### 本地文件保存

如果未配置 Maton API Key 或邮件发送失败，报告会保存到：

```
~/.hermes/reports/market_report.md
```

## 日志查看

脚本会输出详细日志到控制台，包括：

- ✅ 数据获取状态
- 📊 分析进度
- 📧 发送状态
- ⚠️  警告信息
- ❌ 错误信息

查看 Cron job 执行日志：

```bash
hermes cronjob log <job_id>
```
