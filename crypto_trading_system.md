# 加密货币交易系统 - 已就绪 ✅

## 系统概述

基于从 Skills.sh、SkillsMP 和 Awesome OpenClaw Skills 学到的最佳实践，成功构建了一个完整的加密货币交易系统。

## 系统功能

### 📊 市场分析
- 全球市场数据（总市值、交易量、ETH/BTC 占比）
- 趋势币种发现
- 24h 涨跌幅榜

### 📈 技术指标
- SMA/EMA 移动平均线
- RSI 相对强弱指标
- MACD 指数
- 布林带
- 支撑/阻力位

### 🎯 交易策略
| 策略 | 逻辑 | 适用场景 |
|------|------|----------|
| MACD | 金叉买入，死叉卖出 | 趋势行情 |
| RSI | 超卖买入，超买卖出 | 震荡行情 |
| 布林带 | 触下轨买入，触上轨卖出 | 波动交易 |
| 综合 | 多指标共振 | 高可靠性 |
| 趋势跟踪 | 顺势而为 | 长线投资 |

### 🔬 回测功能
- 多策略对比
- 收益率/胜率/回撤分析
- 盈亏比计算

### 💰 模拟交易
- 零风险实盘模拟
- 订单/持仓管理
- 盈亏实时计算
- 状态持久化

## 文件结构

```
~/.openclaw/services/crypto_trading/
├── main.py              # 主控制器
├── market_data.py       # 市场数据获取
├── technical_analysis.py # 技术指标
├── strategies.py        # 交易策略
├── backtest.py          # 回测系统
├── paper_trading.py    # 模拟交易
└── README.md           # 使用说明

~/.openclaw/knowledge/trading/
├── demo_backtest.json   # 回测结果
└── paper_trading.json   # 模拟交易状态
```

## 使用方法

```bash
# 1. 查看市场概览
python3 ~/.openclaw/services/crypto_trading/main.py --overview

# 2. 分析币种（如 Bitcoin）
python3 ~/.openclaw/services/crypto_trading/main.py --coin bitcoin --days 30

# 3. 运行回测
python3 ~/.openclaw/services/crypto_trading/main.py --backtest bitcoin --days 90

# 4. 模拟交易
python3 ~/.openclaw/services/crypto_trading/main.py --paper bitcoin --strategy Combined

# 5. 查看 Top 20 币种
python3 ~/.openclaw/services/crypto_trading/main.py --list 20

# 6. 搜索币种
python3 ~/.openclaw/services/crypto_trading/main.py --search ethereum
```

## 演示结果

使用模拟数据进行回测：

| 策略 | 收益率 | 胜率 | 最大回撤 | 交易次数 |
|------|--------|------|----------|----------|
| MACD Crossover | +1.90% | 40% | 55.16% | 10 |
| RSI | 0.00% | 0% | 0.00% | 0 |
| **Bollinger Bands** | **+155.32%** | **100%** | **48.24%** | 7 |
| Combined | 0.00% | 0% | 0.00% | 0 |
| Trend Following | -4.71% | 66.7% | 56.10% | 6 |

🏆 **最优策略**: Bollinger Bands (模拟数据)

## 数据来源

- **CoinGecko API** - 免费加密货币数据（无需 API Key）
- 全球 10,000+ 币种数据
- 24h 价格/交易量/市值

## 注意事项

⚠️ **重要提示**:
1. 本系统仅供学习和研究使用
2. 模拟交易结果不代表真实收益
3. 加密货币投资风险极高
4. 实盘前请充分测试
5. 永远不要投资超过承受能力的资金

## 后续改进方向

1. **数据源扩展**
   - 集成 Binance/OKX API
   - 添加期货/杠杆数据

2. **策略优化**
   - 机器学习策略 (LSTM)
   - 多时间框架分析

3. **风险管理**
   - 仓位管理
   - 止损止盈
   - 风险敞口限制

4. **自动化**
   - Webhook 触发
   - 实时监控
   - 自动下单

---

**系统状态**: ✅ 已就绪，可进行市场分析、回测和模拟交易
