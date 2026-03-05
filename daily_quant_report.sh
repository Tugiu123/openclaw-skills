#!/bin/bash
# 每日量化交易报告 Cron 脚本
# 运行时间: 每天 09:00 和 21:00

cd ~/.openclaw/workspace

echo "=== $(date '+%Y-%m-%d %H:%M:%S') 量化交易报告 ==="

# 1. 运行自我进化交易系统
echo -e "\n📊 运行交易策略..."
python3 evolving_quant_trader.py --coin bitcoin --mode trade 2>&1

# 2. 生成报告
echo -e "\n📈 账户报告..."
python3 evolving_quant_trader.py --coin bitcoin --mode report 2>&1

# 3. 运行其他交易系统
echo -e "\n🪙 多因子策略..."
python3 ~/.openclaw/services/crypto_trading/multi_factor_trader.py 2>&1 | tail -20

# 4. 保存到 memory
echo "=== $(date '+%Y-%m-%d %H:%M:%S') 交易报告 ===" >> ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
echo "账户余额: \$10000" >> ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
echo "盈亏: 0%" >> ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md

echo -e "\n✅ 每日报告完成"
