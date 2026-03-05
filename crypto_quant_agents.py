#!/usr/bin/env python3
"""
加密货币量化交易 Agent 团队演示
===============================
使用 AutoGen 实现多 Agent 协作进行量化交易

角色分工:
- MarketResearcher: 市场研究与数据分析
- DataAnalyst: 技术指标计算
- StrategyDesigner: 策略设计与回测
- RiskManager: 风险管理
- Trader: 交易执行
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any

# 模拟 Agent 类（实际使用需安装 autogen）
class TradingAgent:
    """交易 Agent 基类"""
    
    def __init__(self, name: str, role: str, description: str, system_prompt: str):
        self.name = name
        self.role = role
        self.description = description
        self.system_prompt = system_prompt
        self.messages = []
    
    def __repr__(self):
        return f"<{self.name} ({self.role})>"


# ==================== 角色定义 ====================

def create_trading_team():
    """创建量化交易 Agent 团队"""
    
    agents = []
    
    # 1. MarketResearcher - 市场研究员
    researcher = TradingAgent(
        name="MarketResearcher",
        role="市场研究员",
        description="负责收集加密货币市场数据、行业动态、项目信息",
        system_prompt="""你是一个专业的加密货币市场研究员。
职责：
- 收集 BTC、ETH 等主流币种的市场数据
- 分析行业趋势和热点赛道
- 评估项目基本面
- 搜索相关新闻和事件

输出格式：
- 当前市场情绪（恐慌/贪婪/中性）
- 热门赛道和趋势
- 重点关注币种及理由
- 潜在风险提示"""
    )
    agents.append(researcher)
    
    # 2. DataAnalyst - 数据分析师
    analyst = TradingAgent(
        name="DataAnalyst",
        role="数据分析师",
        description="负责技术指标计算、数据处理、趋势判断",
        system_prompt="""你是一个专业的金融数据分析师。
职责：
- 计算技术指标（MA, EMA, RSI, MACD, Bollinger Bands）
- 分析价格趋势和波动性
- 识别支撑位和阻力位
- 生成交易信号

技术指标参数：
- MA/EMA: 7, 25, 99 日
- RSI: 14 周期
- MACD: 12, 26, 9
- Bollinger Bands: 20 周期, 2 倍标准差

输出格式：
- 各项指标数值
- 综合信号（买入/卖出/观望）
- 风险等级（低/中/高）"""
    )
    agents.append(analyst)
    
    # 3. StrategyDesigner - 策略设计师
    strategist = TradingAgent(
        name="StrategyDesigner",
        role="策略设计师",
        description="设计交易策略、参数优化、回测验证",
        system_prompt="""你是一个专业的量化策略设计师。
职责：
- 根据市场环境和数据设计交易策略
- 进行回测验证策略有效性
- 优化策略参数
- 比较不同策略的优劣

可用策略：
- MACD 金叉/死叉
- RSI 超买超卖
- 布林带突破
- 趋势跟踪
- 多指标综合

输出格式：
- 推荐策略及理由
- 策略参数建议
- 历史回测表现
- 风险收益比"""
    )
    agents.append(strategist)
    
    # 4. RiskManager - 风险管理师
    risk_manager = TradingAgent(
        name="RiskManager",
        role="风险管理师",
        description="评估交易风险、计算仓位、设置止损止盈",
        system_prompt="""你是一个专业的风险管理师。
职责：
- 评估每笔交易的风险收益比
- 计算推荐仓位大小
- 设置止损止盈点位
- 监控总体风险敞口

风险管理规则：
- 单笔交易风险 ≤ 2% 本金
- 总仓位 ≤ 60% 
- 止损设置：-5% 买入价
- 止盈设置：+15% 或移动止盈

输出格式：
- 风险等级评估
- 推荐仓位
- 止损/止盈价格
- 风险收益比"""
    )
    agents.append(risk_manager)
    
    # 5. Trader - 交易员
    trader = TradingAgent(
        name="Trader",
        role="交易员",
        description="执行交易操作、订单管理、持仓监控",
        system_prompt="""你是一个专业的加密货币交易员。
职责：
- 执行买入/卖出指令
- 管理订单和持仓
- 记录交易日志
- 追踪盈亏情况

交易规则：
- 只执行经过 RiskManager 批准的交易
- 记录每笔交易的详细信息
- 实时监控持仓状态

输出格式：
- 订单执行结果
- 当前持仓状态
- 累计盈亏"""
    )
    agents.append(trader)
    
    return agents


# ==================== 任务协作流程 ====================

def run_trading_workflow(coin: str = "bitcoin", mode: str = "demo"):
    """
    运行量化交易工作流
    
    Args:
        coin: 交易的币种
        mode: demo/simulate/live
    """
    print(f"\n{'='*60}")
    print(f"🚀 启动量化交易 Agent 团队")
    print(f"   交易品种: {coin.upper()}")
    print(f"   模式: {mode}")
    print(f"{'='*60}\n")
    
    # 创建团队
    team = create_trading_team()
    
    # 打印团队成员
    print("📋 Agent 团队成员:")
    for i, agent in enumerate(team, 1):
        print(f"   {i}. {agent.name} - {agent.role}")
        print(f"      {agent.description}")
    print()
    
    # 工作流步骤
    workflow = [
        ("MarketResearcher", f"研究 {coin} 的市场环境，获取最新数据"),
        ("DataAnalyst", f"分析 {coin} 的技术指标，生成交易信号"),
        ("StrategyDesigner", f"根据分析结果设计最佳交易策略"),
        ("RiskManager", f"评估交易风险，计算仓位和止损"),
        ("Trader", f"执行交易操作"),
    ]
    
    results = {}
    
    # 依次执行任务
    for agent_name, task_desc in workflow:
        print(f"\n{'─'*50}")
        print(f"▶ {agent_name}: {task_desc}")
        print(f"{'─'*50}")
        
        # 模拟 Agent 工作
        result = simulate_agent_work(agent_name, coin, task_desc)
        results[agent_name] = result
        
        # 打印结果
        print(f"\n📊 {agent_name} 输出:")
        print(f"   {result['output']}")
        
        # 如果是风险管理，检查是否阻止交易
        if agent_name == "RiskManager":
            if result.get("risk_level") == "HIGH":
                print(f"\n⚠️ 风险过高，交易被阻止！")
                return None
    
    # 生成最终报告
    print(f"\n{'='*60}")
    print(f"📈 交易决策报告")
    print(f"{'='*60}")
    
    final_decision = results.get("Trader", {}).get("output", "无交易")
    print(f"\n{final_decision}")
    
    return results


def simulate_agent_work(agent_name: str, coin: str, task: str) -> Dict:
    """模拟 Agent 工作（实际使用时替换为真实 LLM 调用）"""
    
    import random
    
    # 模拟输出
    outputs = {
        "MarketResearcher": {
            "output": f"📊 {coin.upper()} 市场分析：\n• 当前价格: ${random.randint(40000, 120000):,}\n• 24h波动: ±{random.randint(2, 8)}%\n• 市场情绪: {'贪婪' if random.random() > 0.5 else '中性'}\n• 建议: 关注支撑位水平",
            "risk_level": "MEDIUM"
        },
        "DataAnalyst": {
            "output": f"📈 技术指标分析 ({coin}):\n• RSI(14): {random.randint(30, 70)} (中性)\n• MACD: {'金叉形成' if random.random() > 0.5 else '死叉形成'}\n• MA25: 价格{'高于' if random.random() > 0.5 else '低于'}均线\n• 综合信号: {'买入' if random.random() > 0.4 else '观望'}",
            "signal": "BUY" if random.random() > 0.4 else "HOLD"
        },
        "StrategyDesigner": {
            "output": f"🎯 策略建议:\n• 推荐策略: 布林带突破\n• 买入条件: 价格触及下轨\n• 止盈: +15%\n• 止损: -5%\n• 预期胜率: 65%",
            "strategy": "Bollinger Bands"
        },
        "RiskManager": {
            "output": f"⚖️ 风险评估:\n• 风险等级: {'LOW' if random.random() > 0.3 else 'MEDIUM'}\n• 推荐仓位: 10% (约 ${random.randint(500, 2000)})\n• 止损价格: -5%\n• 止盈价格: +15%\n• 风险收益比: 1:3",
            "risk_level": "LOW" if random.random() > 0.3 else "MEDIUM",
            "position": "10%"
        },
        "Trader": {
            "output": f"✅ 交易执行:\n• 买入价: ${random.randint(95000, 105000):,}\n• 数量: {random.uniform(0.01, 0.1):.4f} BTC\n• 止损: -5%\n• 状态: {'已提交' if random.random() > 0.2 else '待确认'}",
            "executed": True
        }
    }
    
    return outputs.get(agent_name, {"output": "无输出"})


# ==================== 实际使用示例 ====================

def example_real_usage():
    """
    实际使用 AutoGen 的示例代码
    实际运行时需要安装 autogen 并配置 LLM
    """
    
    code = '''
# 实际使用 AutoGen 的代码示例

from autogen import AssistantAgent, UserProxyAgent, GroupChat

# 1. 创建各个 Agent
researcher = AssistantAgent(
    name="MarketResearcher",
    system_prompt="""你是一个专业的加密货币市场研究员。
    职责：收集市场数据、分析趋势、评估风险
    """
)

analyst = AssistantAgent(
    name="DataAnalyst", 
    system_prompt="""你是一个金融数据分析师。
    职责：计算技术指标、分析价格走势、生成信号
    """
)

# 2. 创建群聊
team = GroupChat(
    agents=[researcher, analyst],
    messages=[],
    max_round=5
)

# 3. 发起任务
researcher.initiate_chat(
    team,
    message="分析 BTC 当前是否适合买入"
)
'''
    return code


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    coin = sys.argv[1] if len(sys.argv) > 1 else "bitcoin"
    
    print("""
🪙 加密货币量化交易 Agent 系统
==============================
选择模式:
1. 演示模式 (demo) - 模拟运行
2. 模拟交易 (simulate) - 使用真实数据
3. 查看代码 (code) - 查看实际使用代码
""")
    
    mode = sys.argv[2] if len(sys.argv) > 2 else "demo"
    
    if mode == "demo":
        run_trading_workflow(coin, "demo")
    elif mode == "code":
        print(example_real_usage())
    else:
        print("⚠️ 模拟交易需要配置 API")
