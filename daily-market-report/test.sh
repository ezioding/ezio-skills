#!/bin/bash
# Daily Market Report 测试脚本

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}║      Daily Market Report - 测试                     ║${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"

PASS_COUNT=0
FAIL_COUNT=0

# 测试函数
run_test() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "  $name... "
    
    if eval "$command" &> /dev/null; then
        if [ "$expected" = "pass" ]; then
            echo -e "${GREEN}✅ PASS${NC}"
            ((PASS_COUNT++))
            return 0
        fi
    else
        if [ "$expected" = "fail" ]; then
            echo -e "${GREEN}✅ PASS${NC}"
            ((PASS_COUNT++))
            return 0
        fi
    fi
    
    echo -e "${RED}❌ FAIL${NC}"
    ((FAIL_COUNT++))
    return 1
}

# 测试 1: Node.js
echo -e "\n${BLUE}[1] 依赖检查${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "  Node.js... ${GREEN}✅ 已安装 ($NODE_VERSION)${NC}"
    ((PASS_COUNT++))
else
    echo -e "  Node.js... ${RED}❌ 未安装${NC}"
    ((FAIL_COUNT++))
fi

# 测试 2: crypto-market-data skill
echo -n "  crypto-market-data skill... "
if [ -d "$HOME/.hermes/hermes-agent/skills/crypto-market-data" ]; then
    echo -e "${GREEN}✅ 已安装${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  未安装${NC}"
    ((FAIL_COUNT++))
fi

# 测试 3: 配置文件
echo -e "\n${BLUE}[2] 配置检查${NC}"
CONFIG_FILE="$HOME/.hermes/scripts/market_report_config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    echo -n "  配置文件存在... "
    if python3 -c "import yaml; yaml.safe_load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo -e "${GREEN}✅ 格式正确${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ 格式错误${NC}"
        ((FAIL_COUNT++))
    fi
    
    # 验证必需字段
    echo -n "  必需字段验证... "
    STOCKS=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print('ok' if 'stocks' in c and c.get('stocks') else 'missing')" 2>/dev/null)
    CRYPTOS=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print('ok' if 'cryptos' in c and c.get('cryptos') else 'missing')" 2>/dev/null)
    EMAIL=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print('ok' if 'recipient_email' in c and c.get('recipient_email') else 'missing')" 2>/dev/null)
    
    if [ "$STOCKS" = "ok" ] && [ "$CRYPTOS" = "ok" ] && [ "$EMAIL" = "ok" ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((FAIL_COUNT++))
    fi
else
    echo -e "  配置文件... ${YELLOW}⚠️  不存在${NC}"
    echo -e "  💡 运行 ${BLUE}./install.sh${NC} 生成配置文件"
    ((FAIL_COUNT++))
fi

# 测试 4: 脚本文件
echo -e "\n${BLUE}[3] 脚本检查${NC}"
SCRIPT_FILE="$HOME/.hermes/scripts/daily_market_report.py"
if [ -f "$SCRIPT_FILE" ]; then
    echo -n "  脚本存在... "
    if python3 -m py_compile "$SCRIPT_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ 语法正确${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ 语法错误${NC}"
        ((FAIL_COUNT++))
    fi
else
    echo -e "  脚本... ${YELLOW}⚠️  不存在${NC}"
    ((FAIL_COUNT++))
fi

# 测试 5: 数据采集（可选）
echo -e "\n${BLUE}[4] 数据采集测试（可选）${NC}"
if [ -d "$HOME/.hermes/hermes-agent/skills/crypto-market-data" ]; then
    echo -n "  NVDA 数据获取... "
    cd "$HOME/.hermes/hermes-agent/skills/crypto-market-data"
    RESULT=$(node scripts/get_stock_quote.js NVDA 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print('OK' if d and len(d)>0 else 'FAIL')" 2>/dev/null)
    cd - > /dev/null
    
    if [ "$RESULT" = "OK" ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${YELLOW}⚠️  数据获取失败${NC}"
        ((FAIL_COUNT++))
    fi
    
    echo -n "  Bitcoin 数据获取... "
    cd "$HOME/.hermes/hermes-agent/skills/crypto-market-data"
    RESULT=$(node scripts/get_crypto_price.js bitcoin 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print('OK' if d else 'FAIL')" 2>/dev/null)
    cd - > /dev/null
    
    if [ "$RESULT" = "OK" ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${YELLOW}⚠️  数据获取失败${NC}"
        ((FAIL_COUNT++))
    fi
else
    echo -e "  ⚠️  跳过（缺少 crypto-market-data skill）${NC}"
fi

# 测试 6: Cron job
echo -e "\n${BLUE}[5] Cron job 检查${NC}"
if command -v hermes &> /dev/null; then
    CRON_EXISTS=$(hermes cronjob list 2>/dev/null | grep -c "Daily Market Report" || echo "0")
    if [ "$CRON_EXISTS" -gt 0 ]; then
        echo -e "Cron job... ${GREEN}✅ 已配置${NC}"
        ((PASS_COUNT++))
    else
        echo -e "Cron job... ${YELLOW}⚠️  未配置${NC}"
        ((FAIL_COUNT++))
    fi
else
    echo -e "Cron job... ${YELLOW}⚠️  hermes CLI 不可用${NC}"
    ((FAIL_COUNT++))
fi

# 总结
echo -e "\n${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}║              测试结果汇总                            ║${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════${NC}"
echo -e "  ${GREEN}✅ 通过: $PASS_COUNT${NC}"
echo -e "  ${RED}❌ 失败: $FAIL_COUNT${NC}"
echo -e "  ${BLUE}总计: $((PASS_COUNT + FAIL_COUNT))${NC}"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "\n${GREEN}🎉 所有测试通过！${NC}"
    exit 0
else
    echo -e "\n${YELLOW}💡 有测试失败，请检查配置${NC}"
    exit 1
fi
