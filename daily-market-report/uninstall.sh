#!/bin/bash
# Daily Market Report 卸载脚本

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}══════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}║      Daily Market Report - 卸载                     ║${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════${NC}"

# 1. 删除 Cron job
echo -e "\n${BLUE}[1/3] 删除 Cron job...${NC}"

# 尝试获取 job ID
JOB_ID=$(hermes cronjob list 2>/dev/null | grep -B 2 "Daily Market Report" | grep "job_id:" | grep -oP '\w[0-9a-z]{11}' || echo "")

if [ -z "$JOB_ID" ]; then
    echo -e "${YELLOW}⚠️  未找到 Daily Market Report Cron job${NC}"
    JOB_ID=$(hermes cronjob list 2>/dev/null | grep "Daily Market Report" -A 10 | grep "job_id:" | head -1 | grep -oP '"[^"]+' | sed 's/"//g' || echo "")
fi

if [ -n "$JOB_ID" ]; then
    echo -e "${YELLOW}找到 Cron job (ID: $JOB_ID)${NC}"
    read -p "确认删除？[Y/n] " confirm
    if [ "$confirm" != "n" ] && [ "$confirm" != "N" ]; then
        hermes cronjob remove "$JOB_ID"
        echo -e "${GREEN}✅ Cron job 已删除${NC}"
    else
        echo -e "${YELLOW}跳过删除 Cron job${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  未找到 Cron job${NC}"
fi

# 2. 询问删除配置文件
echo -e "\n${BLUE}[2/3] 删除配置文件?${NC}"
CONFIG_FILE="$HOME/.hermes/scripts/market_report_config.yaml"

if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}配置文件: $CONFIG_FILE${NC}"
    read -p "删除配置文件？[y/N] " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        rm "$CONFIG_FILE"
        echo -e "${GREEN}✅ 配置文件已删除${NC}"
    else
        echo -e "${YELLOW}保留配置文件${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  配置文件不存在${NC}"
fi

# 3. 询问删除脚本文件
echo -e "\n${BLUE}[3/3] 删除脚本文件?${NC}"
SCRIPT_FILE="$HOME/.hermes/scripts/daily_market_report.py"

if [ -f "$SCRIPT_FILE" ]; then
    echo -e "${YELLOW}脚本文件: $SCRIPT_FILE${NC}"
    read -p "删除脚本文件？[y/N] " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        rm "$SCRIPT_FILE"
        echo -e "${GREEN}✅ 脚本文件已删除${NC}"
    else
        echo -e "${YELLOW}保留脚本文件${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  脚本文件不存在${NC}"
fi

# 完成
echo -e "\n${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}║            卸载完成！                              ║${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"
