#!/bin/bash
# Daily Market Report 交互式安装脚本

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}║      Daily Market Report - 交互式安装             ║${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"

# 1. 检查 Node.js
echo -e "\n${BLUE}[1/6] 检查依赖...${NC}"
echo -n "  Node.js... "
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未安装${NC}"
    echo -e "${YELLOW}请先安装 Node.js: https://nodejs.org/${NC}"
    exit 1
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ 已安装 ($NODE_VERSION)${NC}"
fi

# 2. 检查 crypto-market-data skill
echo -n "  crypto-market-data skill... "
SKILL_DIR="$HOME/.hermes/hermes-agent/skills/crypto-market-data"
if [ ! -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}⚠️  未安装${NC}"
    echo -e "${YELLOW}正在尝试通过 skillhub 安装...${NC}"
    
    if command -v skillhub &> /dev/null; then
        skillhub install crypto-market-data || {
            echo -e "${RED}❌ 安装失败${NC}"
            echo -e "${YELLOW}请手动安装: skillhub install crypto-market-data${NC}"
            exit 1
        }
        echo -e "${GREEN}✅ 安装成功${NC}"
    else
        echo -e "${RED}❌ skillhub 未安装${NC}"
        echo -e "${YELLOW}请先安装 skillhub CLI${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ 已安装${NC}"
fi

# 3. 交互式配置
echo -e "\n${BLUE}[2/6] 交互式配置...${NC}"
echo -e "${YELLOW}请配置以下参数（直接回车使用默认值）:${NC}\n"

read -p "股票列表（逗号分隔，默认: AMD,NVDA,TSM,AAPL,GOOGL）: " input_stocks
STOCKS=${input_stocks:-"AMD,NVDA,TSM,AAPL,GOOGL"}

read -p "加密货币列表（逗号分隔，默认: bitcoin,ethereum,solana）: " input_cryptos
CRYPTOS=${input_cryptos:-"bitcoin,ethereum,solana"}

read -p "接收邮箱: " input_email
while [ -z "$input_email" ]; do
    echo -e "${RED}❌ 邮箱不能为空${NC}"
    read -p "接收邮箱: " input_email
done
EMAIL="$input_email"

read -p "执行时间（Cron 格式，默认: 0 1 * * *，即每天 UTC 1:00 / 北京 9:00）: " input_schedule
SCHEDULE=${input_schedule:-"0 1 * * *"}

read -p "Maton API Key（可选，不输入则跳过）: " input_maton_key
MATON_KEY="$input_maton_key"

echo -e "\n${GREEN}配置汇总:${NC}"
echo -e "  股票列表: ${STOCKS}"
echo -e "  加密货币列表: ${CRYPTOS}"
echo -e "  接收邮箱: ${EMAIL}"
echo -e "  执行时间: ${SCHEDULE}"
echo -e "  Maton API Key: ${MATON_KEY:+已设置}${MATON_KEY:-未设置}"

read -p "\n确认配置？[Y/n] " confirm
if [ "$confirm" = "n" ] || [ "$confirm" = "N" ]; then
    echo -e "${YELLOW}安装已取消${NC}"
    exit 0
fi

# 4. 生成配置文件
echo -e "\n${BLUE}[3/6] 生成配置文件...${NC}"
CONFIG_DIR="$HOME/.hermes/scripts"
mkdir -p "$CONFIG_DIR"

CONFIG_FILE="$CONFIG_DIR/market_report_config.yaml"

# 将逗号分隔的列表转换为 YAML 数组格式
echo -n "stocks:" > "$CONFIG_FILE"
echo "$STOCKS" | tr ',' '\n' | while read -r stock; do
    echo "  - ${stock}" >> "$CONFIG_FILE"
done

echo -n "cryptos:" >> "$CONFIG_FILE"
echo "$CRYPTOS" | tr ',' '\n' | while read -r crypto; do
    echo "  - ${crypto}" >> "$CONFIG_FILE"
done

cat >> "$CONFIG_FILE" << ENDCONFIG
recipient_email: "${EMAIL}"
maton_api_key: "${MATON_KEY}"
schedule: "${SCHEDULE}"
ENDCONFIG

echo -e "${GREEN}✅ 配置文件已生成: $CONFIG_FILE${NC}"

# 5. 复制脚本模板
echo -e "\n${BLUE}[4/6] 复制脚本模板...${NC}"

SCRIPT_DIR="$(pwd)/templates"
DEST_SCRIPT="$CONFIG_DIR/daily_market_report.py"

if [ -f "$SCRIPT_DIR/daily_market_report.py" ]; then
    cp "$SCRIPT_DIR/daily_market_report.py" "$DEST_SCRIPT"
    chmod +x "$DEST_SCRIPT"
    echo -e "${GREEN}✅ 脚本已复制到: $DEST_SCRIPT${NC}"
else
    echo -e "${RED}❌ 脚本模板不存在: $SCRIPT_DIR/daily_market_report.py${NC}"
    exit 1
fi

# 6. 创建/更新 Cron job
echo -e "\n${BLUE}[5/6] 创建 Cron job...${NC}"

# 检查是否已存在同名 job
EXISTING_JOB=$(hermes cronjob list 2>/dev/null | grep -A 2 "Daily Market Report" | grep "job_id:" | grep -oP '\w{12}' || echo "")

if [ -n "$EXISTING_JOB" ]; then
    echo -e "${YELLOW}检测到已存在的 Cron job (ID: $EXISTING_JOB)${NC}"
    read -p "是否删除旧 job 并重新创建？[Y/n] " replace_confirm
    if [ "$replace_confirm" != "n" ] && [ "$replace_confirm" != "N" ]; then
        hermes cronjob remove "$EXISTING_JOB"
        echo -e "${GREEN}✅ 旧 job 已删除${NC}"
    else
        echo -e "${YELLOW}跳过 Cron job 创建${NC}"
        echo -e "${YELLOW}如需手动创建，请使用以下命令:${NC}"
        echo -e "${BLUE}hermes cronjob create --name 'Daily Market Report' --prompt '执行每日市场报告脚本：python3 ~/.hermes/scripts/daily_market_report.py' --schedule '$SCHEDULE' --deliver origin${NC}"
        SKIP_CRON=1
    fi
fi

if [ -z "$SKIP_CRON" ]; then
    echo -e "${YELLOW}正在创建 Cron job...${NC}"
    
    # 使用 hermes cronjob CLI
    hermes cronjob create \
        --name "Daily Market Report" \
        --prompt "执行每日市场报告脚本：python3 ~/.hermes/scripts/daily_market_report.py" \
        --schedule "$SCHEDULE" \
        --deliver origin
    
    echo -e "${GREEN}✅ Cron job 创建成功！${NC}"
fi

# 7. 完成
echo -e "\n${BLUE}[6/6] 安装完成！${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}║            安装成功！                              ║${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "\n${GREEN}配置文件:${NC} $CONFIG_FILE"
echo -e "${GREEN}脚本位置:${NC} $DEST_SCRIPT"
echo -e "${GREEN}Cron 调度:${NC} $SCHEDULE"
echo -e "\n${YELLOW}下一步:${NC}"
echo -e "  1. 运行测试: ${BLUE}./test.sh${NC}"
echo -e "  2. 手动运行: ${BLUE}python3 $DEST_SCRIPT${NC}"
echo -e "  3. 查看 Cron job: ${BLUE}hermes cronjob list${NC}"
