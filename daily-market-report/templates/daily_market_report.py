#!/usr/bin/env python3
# 自动化市场数据报告工作流（增强版）
# 每天北京时间 9:00 自动执行
# 监控标的：AMD、NVDA、TSM、AAPL、GOOGL + Bitcoin、Ethereum、Solana

import os
import sys
import json
import base64
import subprocess
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# ==================== 配置 ====================
CONFIG_PATH = os.path.expanduser("~/.hermes/scripts/market_report_config.yaml")
CRYPTO_SKILL_PATH = "/Users/ezio/skills/crypto-market-data"

def load_config():
    """从 YAML 配置文件加载配置（不依赖第三方库）"""
    config = {
        "stocks": ["NVDA", "TSM", "AMD", "AAPL", "GOOGL"],
        "cryptos": ["bitcoin", "ethereum", "solana"],
        "recipient_email": "916505542@qq.com",
        "maton_api_key": "",
        "schedule": "0 1 * * *",
    }
    if not os.path.exists(CONFIG_PATH):
        return config
    with open(CONFIG_PATH, 'r') as f:
        lines = f.readlines()
    current_key = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped.startswith('- '):
            if current_key in ('stocks', 'cryptos'):
                config[current_key].append(stripped[2:].strip())
        elif ':' in stripped:
            key, _, val = stripped.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key in ('stocks', 'cryptos'):
                config[key] = []
                current_key = key
            else:
                current_key = None
                if val:
                    config[key] = val
    return config

_cfg = load_config()
RECIPIENT_EMAIL = _cfg["recipient_email"]
MATON_API_KEY = os.environ.get("MATON_API_KEY") or _cfg.get("maton_api_key", "")
STOCKS = _cfg["stocks"]
CRYPTOS = _cfg["cryptos"]

# ==================== 工具函数 ====================
def log(message):
    """带时间戳的日志输出"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def get_stock_data(symbol):
    """获取股票数据"""
    try:
        result = subprocess.run(
            ['node', 'scripts/get_stock_quote.js', symbol],
            cwd=CRYPTO_SKILL_PATH,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout.strip())
            if data and len(data) > 0:
                return data[0]
        return None
    except Exception as e:
        log(f"获取 {symbol} 数据失败: {e}")
        return None

def get_crypto_data(cryptos):
    """获取加密货币数据"""
    try:
        result = subprocess.run(
            ['node', 'scripts/get_crypto_price.js'] + cryptos,
            cwd=CRYPTO_SKILL_PATH,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout.strip())
            return data
        return {}
    except Exception as e:
        log(f"获取加密货币数据失败: {e}")
        return {}

def send_email(subject, html_body, text_attachment, filename):
    """发送邮件"""
    if not MATON_API_KEY:
        log("错误: 未设置 MATON_API_KEY")
        return False

    # 创建MIME邮件
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'me'
    msg['To'] = RECIPIENT_EMAIL

    # 添加HTML正文
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    # 添加 Markdown 附件
    part = MIMEText(text_attachment, 'plain', 'utf-8')
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(part)

    # 转换为base64url
    email_str = msg.as_string()
    email_bytes = email_str.encode('utf-8')
    b64_bytes = base64.urlsafe_b64encode(email_bytes)
    b64_str = b64_bytes.decode('utf-8')

    try:
        send_url = "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/send"
        send_data = json.dumps({"raw": b64_str}).encode()
        req = urllib.request.Request(send_url, data=send_data, method="POST")
        req.add_header('Authorization', f'Bearer {MATON_API_KEY}')
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req)
        result = json.load(response)
        log(f"邮件发送成功! Message ID: {result.get('id')}")
        return True
    except Exception as e:
        log(f"邮件发送失败: {e}")
        return False

# ==================== 分析函数 ====================
def analyze_technical(data):
    """技术面分析"""
    diff_50 = ((data['price'] - data['priceAvg50']) / data['priceAvg50']) * 100
    diff_200 = ((data['price'] - data['priceAvg200']) / data['priceAvg200']) * 100
    
    if diff_50 > 0 and diff_200 > 0:
        status = "✅ 强势多头"
        advice = "上升趋势确立，考虑逢低买入"
    elif diff_50 > 0 and diff_200 < 0:
        status = "⚠️ 短期强势"
        advice = "短期走强，观察200日线突破情况"
    elif diff_50 < 0 and diff_200 < 0:
        status = "🔴 弱势趋势"
        advice = "处于下降趋势，建议观望或止损"
    else:
        status = "🟡 震荡整理"
        advice = "方向不明，建议轻仓操作"
    
    return {
        'diff_50': diff_50,
        'diff_200': diff_200,
        'status': status,
        'advice': advice
    }

def analyze_volume(data):
    """成交量分析"""
    # 简单的成交量分析（基于基准）
    volume_millions = data['volume'] / 1e6
    
    if volume_millions > 100:
        level = "🔥 放量"
        analysis = "成交活跃，市场关注度较高"
    elif volume_millions > 50:
        level = "🟠 适中"
        analysis = "成交量正常，流动性良好"
    else:
        level = "🟡 缩量"
        analysis = "成交清淡，可能缺乏动力"
    
    return {
        'volume_millions': volume_millions,
        'level': level,
        'analysis': analysis
    }

def analyze_year_performance(data):
    """年内表现分析"""
    year_range = data['yearHigh'] - data['yearLow']
    current_position = ((data['price'] - data['yearLow']) / year_range) * 100
    year_gain = ((data['price'] - data['yearLow']) / data['yearLow']) * 100
    
    if current_position > 80:
        position_desc = "接近年内高点"
    elif current_position > 60:
        position_desc = "处于年内中高位"
    elif current_position > 40:
        position_desc = "处于年内中位"
    else:
        position_desc = "接近年内低点"
    
    return {
        'position': current_position,
        'year_gain': year_gain,
        'position_desc': position_desc,
        'distance_to_high': ((data['price'] - data['yearHigh']) / data['yearHigh']) * 100
    }

def generate_investment_advice(symbol, data, technical, volume, year_perf):
    """生成投资建议"""
    symbol_desc = {
        'NVDA': {'name': '英伟达', 'sector': 'AI GPU', 'advantage': 'CUDA生态、H100需求旺盛', 'weight': '50%'},
        'TSM': {'name': '台积电', 'sector': '晶圆代工', 'advantage': '3nm/5nm先进制程独占', 'weight': '30%'},
        'AMD': {'name': 'AMD', 'sector': 'CPU/GPU', 'advantage': '性价比、MI300获认可', 'weight': '20%'},
        'AAPL': {'name': '苹果', 'sector': '消费电子', 'advantage': '生态护城河、iPhone现金流', 'weight': '40%'},
        'GOOGL': {'name': 'Google', 'sector': '搜索与云', 'advantage': 'AI搜索、云计算领先', 'weight': '30%'},
        'QQQ': {'name': '纳斯达克100 ETF', 'sector': '科技指数基金', 'advantage': '分散持有100家纳斯达克科技龙头，低费率', 'weight': '30%'},
        'TTWO': {'name': 'Take-Two Interactive', 'sector': '游戏', 'advantage': 'GTA/NBA 2K/Borderlands 顶级IP，GTA6 催化剂', 'weight': '20%'},
    }
    
    info = symbol_desc.get(symbol, {'name': symbol, 'sector': '科技', 'advantage': '技术领先', 'weight': '20%'})
    
    advice_lines = []
    advice_lines.append(f"**公司**: {info['name']} ({info['sector']})")
    advice_lines.append(f"**核心优势**: {info['advantage']}")
    advice_lines.append("")
    
    # 技术面建议
    advice_lines.append("**技术面**: " + technical['status'])
    advice_lines.append(f"- 相对50日均线: {technical['diff_50']:+.2f}%")
    advice_lines.append(f"- 相对200日均线: {technical['diff_200']:+.2f}%")
    advice_lines.append(f"- {technical['advice']}")
    advice_lines.append("")
    
    # 成交量分析
    advice_lines.append("**成交量**: " + volume['level'])
    advice_lines.append(f"- 成交量: {volume['volume_millions']:.2f}M股")
    advice_lines.append(f"- {volume['analysis']}")
    advice_lines.append("")
    
    # 年内表现
    advice_lines.append("**年内表现**: " + year_perf['position_desc'])
    advice_lines.append(f"- 年涨幅: {year_perf['year_gain']:.1f}%")
    advice_lines.append(f"- 距年内高点: {year_perf['distance_to_high']:.2f}%")
    
    if year_perf['distance_to_high'] > -5:
        advice_lines.append(f"- **关键阻力**: ${data['yearHigh']:.2f} (接近历史新高)")
    advice_lines.append("")
    
    # 综合建议
    if technical['diff_50'] > 0 and technical['diff_200'] > 0:
        advice_lines.append(f"**投资建议**: ✅ **{info['weight']}** 核心配置 - 上升趋势确立，适合中长期持有")
    elif technical['diff_50'] > 0:
        advice_lines.append(f"**投资建议**: ⚠️ **{int(int(info['weight'])/2)}%** 卫星配置 - 短期走强，观察突破情况")
    else:
        advice_lines.append(f"**投资建议**: 🔴 **观望** - 下降趋势，等待企稳信号")
    
    return "\n".join(advice_lines)

# ==================== 主工作流 ====================
def main():
    log("=" * 80)
    log("🚀 启动自动化市场数据报告工作流（增强版）")
    log("=" * 80)
    log(f"监控标的股票: {', '.join(STOCKS)}")
    log(f"监控加密货币: {', '.join(CRYPTOS)}")
    log(f"发送至: {RECIPIENT_EMAIL}")

    # 步骤 1: 获取股票数据
    log("步骤 1: 获取股票数据...")
    stocks_data = {}
    for symbol in STOCKS:
        log(f"  获取 {symbol}...")
        data = get_stock_data(symbol)
        if data:
            stocks_data[symbol] = data
            log(f"    ✅ {data['name']}: ${data['price']:.2f} (+{data['change']:.2f})")
        else:
            log(f"    ❌ 获取失败")
            stocks_data[symbol] = None

    if not any(stocks_data.values()):
        log("❌ 所有股票数据获取失败，退出")
        return False

    log(f"✅ 成功获取 {len([v for v in stocks_data.values() if v])}/{len(STOCKS)} 只股票数据")

    # 步骤 2: 获取加密货币数据
    log("步骤 2: 获取加密货币数据...")
    crypto_data = get_crypto_data(CRYPTOS)
    if crypto_data:
        for crypto, price in crypto_data.items():
            log(f"  ✅ {crypto.capitalize()}: ${price.get('usd', 0):.2f}")
        log(f"✅ 成功获取 {len(crypto_data)} 种加密货币数据")

    # 步骤 3: 生成详细分析报告
    log("步骤 3: 生成详细分析报告...")

    # 计算统计数据
    valid_stocks = {k: v for k, v in stocks_data.items() if v}
    if valid_stocks:
        avg_change = sum(d['changePercentage'] for d in valid_stocks.values()) / len(valid_stocks)
        total_market_cap = sum(d['marketCap'] for d in valid_stocks.values())
        best_performer = max(valid_stocks.items(), key=lambda x: x[1]['changePercentage'])
        worst_performer = min(valid_stocks.items(), key=lambda x: x[1]['changePercentage'])
        
        # 对每只股票进行详细分析
        stock_analysis = {}
        for symbol, data in valid_stocks.items():
            technical = analyze_technical(data)
            volume = analyze_volume(data)
            year_perf = analyze_year_performance(data)
            advice = generate_investment_advice(symbol, data, technical, volume, year_perf)
            stock_analysis[symbol] = {
                'technical': technical,
                'volume': volume,
                'year_perf': year_perf,
                'advice': advice
            }
    else:
        avg_change = 0
        total_market_cap = 0
        best_performer = None
        worst_performer = None
        stock_analysis = {}

    # 生成增强的 Markdown 报告
    md_report = []
    md_report.append("# 市场数据分析报告（详细版）")
    md_report.append("")
    md_report.append(f"**报告时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    md_report.append("")

    # 1. 执行摘要
    md_report.append("## 📋 执行摘要")
    md_report.append("")
    md_report.append(f"- **股票平均涨跌幅**: {avg_change:.2f}%")
    if best_performer:
        md_report.append(f"- **今日最佳表现**: {best_performer[0]} (+{best_performer[1]['changePercentage']:.2f}%)")
        md_report.append(f"- **今日最差表现**: {worst_performer[0]} (+{worst_performer[1]['changePercentage']:.2f}%)")
    md_report.append(f"- **总市值**: ${total_market_cap / 1e9:.2f} billion")
    md_report.append("- **技术面状态**: 多数股票保持上升趋势")
    md_report.append("- **投资基调**: 科技股和加密货币长期看多")

    # 2. 实时价格数据
    md_report.append("")
    md_report.append("## 💹 实时价格数据")
    md_report.append("")
    md_report.append("### 股票")
    md_report.append("")
    md_report.append("| 代码 | 公司名称 | 当前价 | 涨跌额 | 涨跌幅 | 成交量(M) | 市值(B) |")
    md_report.append("|------|---------|--------|--------|--------|-----------|--------|")
    
    for symbol, data in valid_stocks.items():
        change_class = "🟢" if data['changePercentage'] >= 0 else "🔴"
        md_report.append(f"| {symbol} | {data['name'][:30]} | ${data['price']:.2f} | {change_class} ${data['change']:.2f} | {data['changePercentage']:.2f}% | {data['volume']/1e6:.2f} | {data['marketCap']/1e9:.2f} |")

    if crypto_data:
        md_report.append("")
        md_report.append("### 加密货币")
        md_report.append("")
        md_report.append("| 代码 | 当前价 (USD) | 24h涨跌 |")
        md_report.append("|------|---------------|---------|")
        for crypto, price in crypto_data.items():
            md_report.append(f"| {crypto.capitalize()} | ${price.get('usd', 0):.2f} | 暂无数据 |")

    # 4. 涨跌幅分析
    md_report.append("")
    md_report.append("## 📈 涨跌幅分析")
    md_report.append("")
    
    sorted_by_change = sorted(valid_stocks.items(), key=lambda x: x[1]['changePercentage'], reverse=True)
    md_report.append("### 涨跌幅排名")
    md_report.append("")
    for i, (symbol, data) in enumerate(sorted_by_change, 1):
        relative = data['changePercentage'] - avg_change
        md_report.append(f"{i}. **{symbol}** - {data['changePercentage']:+.2f}% (相对平均: {relative:+.2f}%)")

    # 4. 成交量统计
    md_report.append("")
    md_report.append("## 📌 成交量统计")
    md_report.append("")
    md_report.append("| 代码 | 成交量(M) | 成交水平 | 分析 |")
    md_report.append("|------|-----------|---------|------|")
    
    for symbol, data in valid_stocks.items():
        volume_millions = data['volume'] / 1e6
        if volume_millions > 100:
            level = "🔥 活跃"
            analysis = "成交活跃，市场关注度高"
        elif volume_millions > 50:
            level = "🟠 正常"
            analysis = "成交量正常，流动性良好"
        else:
            level = "🟡 清淡"
            analysis = "成交清淡，动力不足"
        md_report.append(f"| {symbol} | {volume_millions:.2f} | {level} | {analysis} |")

    # 5. 技术指标
    md_report.append("")
    md_report.append("## 📊 技术指标分析")
    md_report.append("")
    
    for symbol, data in valid_stocks.items():
        technical = stock_analysis.get(symbol, {}).get('technical', {})
        md_report.append(f"### {symbol}")
        md_report.append("")
        md_report.append(f"- **当前价**: ${data['price']:.2f}")
        md_report.append(f"- **50日均线**: ${data['priceAvg50']:.2f} (距: {technical.get('diff_50', 0):+.2f}%)")
        md_report.append(f"- **200日均线**: ${data['priceAvg200']:.2f} (距: {technical.get('diff_200', 0):+.2f}%)")
        md_report.append(f"- **技术状态**: {technical.get('status', '未知')}")
        md_report.append(f"- **年内高点**: ${data['yearHigh']:.2f}")
        md_report.append(f"- **年内低点**: ${data['yearLow']:.2f}")
        md_report.append("")

    # 6. 投资建议
    md_report.append("")
    md_report.append("## 💡 投资建议")
    md_report.append("")
    
    for symbol, data in valid_stocks.items():
        md_report.append(f"### {symbol}")
        md_report.append("")
        advice_text = stock_analysis.get(symbol, {}).get('advice', '暂无建议')
        md_report.append(advice_text)
        md_report.append("")

    # 7. 决策简报
    md_report.append("")
    md_report.append("## 🎯 决策简报")
    md_report.append("")
    md_report.append("### 核心策略")
    md_report.append("")
    md_report.append("- **长期看多科技股**: AI 芯片、云计算需求持续增长")
    md_report.append("- **加密货币作为对冲**: 分散化投资，降低整体风险")
    md_report.append("- **关注技术面信号**: 50/200日均线突破/跌破")
    md_report.append("- **分批建仓**: 避免一次性重仓，降低追高风险")
    md_report.append("")

    md_report.append("### 推荐配置比例")
    md_report.append("")
    md_report.append("| 资产类别 | 具体标的 | 配置比例 | 逻辑 |")
    md_report.append("|---------|---------|---------|------|")
    md_report.append("| **核心持仓** | NVDA | 40-50% | AI GPU龙头，直接受益于AI需求 |")
    md_report.append("| **卫星持仓** | TSM, AAPL, GOOGL | 30-35% | 产业链协同，稳定现金流 |")
    md_report.append("| **机会持仓** | AMD | 15-20% | 性价比，NVDA备选 |")
    md_report.append("| **对冲资产** | BTC, ETH, SOL | 10-15% | 数字资产，与传统资产负相关 |")
    md_report.append("| **现金储备** | 现金 | 5-10% | 应对市场波动和机会 |")

    # 8. 风险提示
    md_report.append("")
    md_report.append("## ⚠️ 风险提示")
    md_report.append("")
    
    md_report.append("### 宏观风险")
    md_report.append("- 美联储利率政策变化")
    md_report.append("- 全球经济放缓担忧")
    md_report.append("- 地缘政治不确定性")
    md_report.append("- 通胀水平高企")
    md_report.append("")
    
    md_report.append("### 行业风险")
    md_report.append("- AI 芯片需求周期性")
    md_report.append("- 科技股估值处于历史高位")
    md_report.append("- 竞争加剧 (AMD挑战NVDA)")
    md_report.append("- 地缘政治风险 (台积电在台湾)")
    md_report.append("")
    
    md_report.append("### 加密货币风险")
    md_report.append("- 监管政策收紧")
    md_report.append("- 市场波动性极高")
    md_report.append("- 技术安全风险")
    md_report.append("- 流动性风险")

    # 9. 行动计划
    md_report.append("")
    md_report.append("## 📅 行动计划")
    md_report.append("")
    
    md_report.append("### 短期 (1-3个月)")
    md_report.append("- 关注NVDA是否突破$212.19年内高点")
    md_report.append("- 监控台积电与芯片需求的关联性")
    md_report.append("- 观察AMD MI300客户采用情况")
    md_report.append("- 跟踪加密货币与传统市场相关性")
    md_report.append("")
    
    md_report.append("### 中期 (3-12个月)")
    md_report.append("- 定期审查AI行业供应链数据")
    md_report.append("- 评估新制程(3nm/2nm)对TSM的推动作用")
    md_report.append("- 关注AMD市场份额变化")
    md_report.append("- 跟踪Web3项目上线和用户增长")
    md_report.append("")
    
    md_report.append("### 长期 (12个月+)")
    md_report.append("- AI算力需求持续增长核心逻辑不变")
    md_report.append("- 先进制程和软件生态是长期护城河")
    md_report.append("- 将AI芯片产业链作为长期投资主题")
    md_report.append("- 维持20-30%科技股权重")

    md_report.append("")
    md_report.append("---")
    md_report.append("")
    md_report.append("*报告生成完成*")

    md_report_str = "\n".join(md_report)
    log("✅ 详细分析报告生成完成")

    # 步骤 4: 生成 HTML 邮件
    log("步骤 4: 生成 HTML 邮件...")

    # 简化版HTML
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>市场数据报告（详细版）</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f5f7fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
        .content {{ padding: 30px; }}
        h2 {{ color: #2c3e50; border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #667eea; color: white; padding: 12px; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .positive {{ color: #27ae60; }}
        .negative {{ color: #e74c3c; }}
        .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 市场数据报告（详细版）</h1>
            <p>{datetime.now().strftime('%Y年%m月%d日 %H:%M')}</p>
        </div>
        
        <div class="content">
            <h2>执行摘要</h2>
            <p>股票平均涨跌幅: {avg_change:.2f}%</p>
            <p>总市值: ${total_market_cap / 1e9:.2f} billion</p>
            
            <h2>实时价格数据</h2>
            <table>
                <tr>
                    <th>代码</th>
                    <th>公司名称</th>
                    <th>当前价</th>
                    <th>涨跌幅</th>
                </tr>
"""

    for symbol, data in valid_stocks.items():
        change_class = "positive" if data['changePercentage'] >= 0 else "negative"
        html_content += f"""
                <tr>
                    <td>{symbol}</td>
                    <td>{data['name'][:30]}</td>
                    <td>${data['price']:.2f}</td>
                    <td class="{change_class}">{data['changePercentage']:.2f}%</td>
                </tr>
"""

    html_content += f"""
            </table>
            
            <h2>投资建议</h2>
            <p>详细投资建议请查看附件中的Markdown报告。</p>
        </div>
        
        <div class="footer">
            <p><strong>免责声明:</strong> 本报告由 AI 自动生成，仅供参考，不构成投资建议。</p>
            <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""

    log("✅ HTML 邮件生成完成")

    # 步骤 5: 发送邮件或保存本地
    log("步骤 5: 输出报告...")
    subject = f"市场数据报告（详细版） - {datetime.now().strftime('%Y-%m-%d')}"

    if MATON_API_KEY:
        success = send_email(subject, html_content, md_report_str, f"market_report_detailed_{datetime.now().strftime('%Y%m%d')}.md")
    else:
        # 保存到本地文件
        report_dir = os.path.expanduser("~/.hermes/reports")
        os.makedirs(report_dir, exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        md_path = os.path.join(report_dir, f"market_report_{date_str}.md")
        html_path = os.path.join(report_dir, f"market_report_{date_str}.html")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_report_str)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        log(f"📄 Markdown 报告已保存: {md_path}")
        log(f"🌐 HTML 报告已保存: {html_path}")
        success = True

    if success:
        log("=" * 80)
        log("🎉 工作流执行完成!")
        log("=" * 80)
        return True
    else:
        log("❌ 工作流执行失败")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ 工作流异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
