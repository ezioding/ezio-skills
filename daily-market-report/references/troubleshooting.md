# 故障排除

## 常见问题

### 问题：配置文件不存在

**错误信息：**
```
❌ 配置文件不存在: ~/.hermes/scripts/market_report_config.yaml
```

**解决方法：**
1. 运行 `./install.sh` 重新安装
2. 或手动创建配置文件，参考 `templates/config.example.yaml`

---

### 问题：Node.js 未安装

**错误信息：**
```
❌ 未安装 Node.js
```

**解决方法：**
1. 安装 Node.js: https://nodejs.org/
2. 验证安装：`node --version`

---

### 问题：crypto-market-data skill 不存在

**错误信息：**
```
⚠️  crypto-market-data skill 未安装
```

**解决方法：**
```bash
skillhub install crypto-market-data
```

---

### 问题：数据获取失败

**错误信息：**
```
⚠️ NVDA: 获取失败
```

**可能原因：**
1. 网络连接问题
2. API 服务不可用
3. 股票代码错误

**解决方法：**
1. 检查网络连接
2. 验证股票代码是否正确
3. 单独测试数据获取：
   ```bash
   cd ~/.hermes/hermes-agent/skills/crypto-market-data
   node scripts/get_stock_quote.js NVDA
   ```

---

### 问题：邮件发送失败

**错误信息：**
```
🟠 邮件发送失败: [错误详情]
```

**解决方法：**
1. 检查 Maton API Key 是否正确
2. 检查邮箱地址是否有效
3. 查看报告是否保存到本地文件：
   ```bash
   cat ~/.hermes/reports/market_report.md
   ```

---

### 问题：Cron job 不执行

**检查步骤：**

1. 验证 Cron job 是否存在：
   ```bash
   hermes cronjob list
   ```

2. 检查 Cron job 是否启用：
   ```bash
   hermes cronjob list | grep "enabled"
   ```

3. 查看最后一次执行：状态：
   ```bash
   hermes cronjob list | grep -A 5 "Daily Market Report"
   ```

4. 查看执行日志：
   ```bash
   hermes cronjob log <job_id>
   ```

5. 手动触发测试：
   ```bash
   hermes cronjob run <job_id>
   ```

---

## 获取帮助

如果以上方法无法解决问题，请：

1. 查看完整日志：`hermes cronjob log <job_id>`
2. 运行测试脚本：`./test.sh`
3. 查看错误详情：检查 `last_error` 字段
4. 提交 Issue：https://github.com/ezioding/ezio-skills/issues

## 调试模式

手动运行时启用调试输出：

```bash
DEBUG=1 python3 ~/. ~/.hermes/scripts/daily_market_report.py
```

这将输出更详细的调试信息。
