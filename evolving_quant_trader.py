#!/usr/bin/env python3
"""
自我进化量化交易系统 v2.0
=========================
功能：
1. 真实市场数据模拟交易
2. LLM 驱动的策略优化
3. 每日自动报告
4. 策略自我进化

依赖：
- ollama (本地模型服务)
- requests (API 调用)
"""

import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import random

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== 配置 ====================

@dataclass
class Config:
    """系统配置"""
    # 模型配置
    ollama_base_url: str = "http://localhost:11434"
    model: str = "kimi-k2.5:cloud"  # 或 glm-4.7:cloud
    
    # 交易配置
    initial_balance: float = 10000.0  # 初始资金
    max_position: float = 0.6  # 最大仓位 60%
    risk_per_trade: float = 0.02  # 单笔风险 2%
    
    # 进化配置
    min_trades_for_evolution: int = 5  # 最少交易次数才进化
    evolution_threshold: float = -0.05  # 亏损 5% 触发强制进化
    
    # 数据目录
    data_dir: Path = Path("~/.openclaw/workspace/crypto_data")
    reports_dir: Path = Path("~/.openclaw/workspace/crypto_reports")


config = Config()

# ==================== LLM 调用 ====================

class LLMClient:
    """Ollama LLM 客户端"""
    
    def __init__(self, model: str = None):
        self.model = model or config.model
        self.base_url = config.ollama_base_url
    
    def chat(self, system: str, user: str, temperature: float = 0.7) -> str:
        """调用 LLM 生成回复"""
        import requests
        
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": temperature
        }
        
        try:
            response = requests.post(url, json=payload, timeout=180)
            # 处理多行 JSON 响应
            text = response.text
            # 找到第一个完整的 JSON 对象
            lines = text.split('\n')
            for line in lines:
                if line.strip():
                    try:
                        data = json.loads(line)
                        return data.get("message", {}).get("content", "")
                    except:
                        continue
            return None
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return None
    
    def chat_with_json(self, system: str, user: str) -> Dict:
        """调用 LLM 并解析 JSON 响应"""
        response = self.chat(system, user)
        if not response:
            return {}
        
        # 尝试解析 JSON
        try:
            # 尝试提取 JSON 块
            import re
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return {"raw_response": response}


# ==================== 市场数据 ====================

class MarketData:
    """市场数据获取 (使用 CoinGecko 免费 API)"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_coin_data(self, coin_id: str = "bitcoin", days: int = 30) -> Dict:
        """获取币种数据"""
        import requests
        
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return self._get_mock_data(coin_id, days)
    
    def get_simple_price(self, coin_ids: List[str]) -> Dict:
        """获取简单价格"""
        import requests
        
        url = f"{self.base_url}/simple/price"
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            return response.json()
        except:
            return {coin: {"usd": 50000, "usd_24h_change": 0} for coin in coin_ids}
    
    def get_ohlc(self, coin_id: str = "bitcoin", days: int = 7) -> List:
        """获取 K 线数据"""
        import requests
        
        url = f"{self.base_url}/coins/{coin_id}/ohlc"
        params = {
            "vs_currency": "usd",
            "days": days
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            return response.json()
        except:
            return []
    
    def _get_mock_data(self, coin_id: str, days: int) -> Dict:
        """生成模拟数据"""
        base_price = 100000 if coin_id == "bitcoin" else 3000
        prices = []
        now = datetime.now()
        
        for i in range(days):
            ts = int((now - timedelta(days=days-i)).timestamp() * 1000)
            price = base_price * (1 + random.uniform(-0.1, 0.1))
            prices.append([ts, price, price, price, price])
        
        return {"prices": prices}


# ==================== 技术指标 ====================

class TechnicalAnalyzer:
    """技术指标分析"""
    
    @staticmethod
    def calculate_ma(prices: List, period: int) -> float:
        """计算移动平均线"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        return sum(prices[-period:]) / period
    
    @staticmethod
    def calculate_rsi(prices: List, period: int = 14) -> float:
        """计算 RSI"""
        if len(prices) < period + 1:
            return 50
        
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List) -> Dict:
        """计算 MACD"""
        if len(prices) < 26:
            return {"macd": 0, "signal": 0, "histogram": 0}
        
        # EMA12
        ema12 = sum(prices[-12:]) / 12
        # EMA26
        ema26 = sum(prices[-26:]) / 26
        # MACD 线
        macd = ema12 - ema26
        # Signal 线 (9日 EMA)
        signal = macd * 0.9  # 简化
        # 柱状图
        histogram = macd - signal
        
        return {"macd": macd, "signal": signal, "histogram": histogram}
    
    @staticmethod
    def calculate_bollinger(prices: List, period: int = 20) -> Dict:
        """计算布林带"""
        if len(prices) < period:
            return {"upper": 0, "middle": 0, "lower": 0}
        
        ma = sum(prices[-period:]) / period
        variance = sum((p - ma) ** 2 for p in prices[-period:]) / period
        std = variance ** 0.5
        
        return {
            "upper": ma + 2 * std,
            "middle": ma,
            "lower": ma - 2 * std
        }
    
    @staticmethod
    def analyze(prices: List) -> Dict:
        """综合技术分析"""
        return {
            "ma7": TechnicalAnalyzer.calculate_ma(prices, 7),
            "ma25": TechnicalAnalyzer.calculate_ma(prices, 25),
            "rsi": TechnicalAnalyzer.calculate_rsi(prices),
            "macd": TechnicalAnalyzer.calculate_macd(prices),
            "bollinger": TechnicalAnalyzer.calculate_bollinger(prices),
            "current_price": prices[-1] if prices else 0
        }


# ==================== 交易策略 ====================

@dataclass
class TradeSignal:
    """交易信号"""
    action: str  # buy, sell, hold
    confidence: float  # 置信度 0-1
    reason: str  # 理由
    price: float  # 当前价格
    stop_loss: float  # 止损价
    take_profit: float  # 止盈价


class Strategy:
    """交易策略基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.params = {}
    
    def generate_signal(self, prices: List, analysis: Dict) -> TradeSignal:
        raise NotImplementedError
    
    def to_dict(self) -> Dict:
        return {"name": self.name, "params": self.params}


class MACDStrategy(Strategy):
    """MACD 策略"""
    
    def __init__(self):
        super().__init__("MACD")
    
    def generate_signal(self, prices: List, analysis: Dict) -> TradeSignal:
        macd = analysis.get("macd", {})
        current = analysis["current_price"]
        
        if macd.get("histogram", 0) > 0 and macd.get("macd", 0) > macd.get("signal", 0):
            return TradeSignal(
                action="buy",
                confidence=0.7,
                reason="MACD 金叉形成",
                price=current,
                stop_loss=current * 0.95,
                take_profit=current * 1.15
            )
        elif macd.get("histogram", 0) < 0:
            return TradeSignal(
                action="sell",
                confidence=0.7,
                reason="MACD 死叉形成",
                price=current,
                stop_loss=None,
                take_profit=None
            )
        return TradeSignal(action="hold", confidence=0.5, reason="无明确信号", price=current, stop_loss=None, take_profit=None)


class RSIStrategy(Strategy):
    """RSI 策略"""
    
    def __init__(self):
        super().__init__("RSI")
    
    def generate_signal(self, prices: List, analysis: Dict) -> TradeSignal:
        rsi = analysis.get("rsi", 50)
        current = analysis["current_price"]
        
        if rsi < 30:
            return TradeSignal(
                action="buy",
                confidence=0.8,
                reason=f"RSI 超卖 ({rsi:.1f})",
                price=current,
                stop_loss=current * 0.95,
                take_profit=current * 1.15
            )
        elif rsi > 70:
            return TradeSignal(
                action="sell",
                confidence=0.8,
                reason=f"RSI 超买 ({rsi:.1f})",
                price=current,
                stop_loss=None,
                take_profit=None
            )
        return TradeSignal(action="hold", confidence=0.5, reason=f"RSI 中性 ({rsi:.1f})", price=current, stop_loss=None, take_profit=None)


class BollingerStrategy(Strategy):
    """布林带策略"""
    
    def __init__(self):
        super().__init__("Bollinger")
    
    def generate_signal(self, prices: List, analysis: Dict) -> TradeSignal:
        bb = analysis.get("bollinger", {})
        current = analysis["current_price"]
        
        if current < bb.get("lower", 0):
            return TradeSignal(
                action="buy",
                confidence=0.75,
                reason="价格触及布林下轨",
                price=current,
                stop_loss=current * 0.95,
                take_profit=current * 1.15
            )
        elif current > bb.get("upper", 0):
            return TradeSignal(
                action="sell",
                confidence=0.75,
                reason="价格触及布林上轨",
                price=current,
                stop_loss=None,
                take_profit=None
            )
        return TradeSignal(action="hold", confidence=0.5, reason="价格在布林带内", price=current, stop_loss=None, take_profit=None)


class LLMStrategy(Strategy):
    """LLM 驱动的策略 (基于 AI 分析)"""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("LLM")
        self.llm = llm_client
        self.prompt_template = """你是一个专业的加密货币交易分析师。
    
当前市场数据：
- 当前价格: ${current_price}
- MA7: ${ma7}
- MA25: ${ma25}
- RSI: {rsi}
- MACD: {macd_status}
- 布林带: 上轨 ${bb_upper}, 中轨 ${bb_middle}, 下轨 ${bb_lower}

历史价格趋势: {price_trend}

请分析并给出交易建议。

输出 JSON 格式：
{{
    "action": "buy/sell/hold",
    "confidence": 0.0-1.0,
    "reason": "分析理由",
    "stop_loss": 止损价(可选),
    "take_profit": 止盈价(可选)
}}"""
    
    def generate_signal(self, prices: List, analysis: Dict) -> TradeSignal:
        current = analysis["current_price"]
        macd = analysis.get("macd", {})
        
        prompt = self.prompt_template.format(
            current_price=current,
            ma7=analysis.get("ma7", 0),
            ma25=analysis.get("ma25", 0),
            rsi=analysis.get("rsi", 50),
            macd_status="金叉" if macd.get("histogram", 0) > 0 else "死叉",
            bb_upper=analysis.get("bollinger", {}).get("upper", 0),
            bb_middle=analysis.get("bollinger", {}).get("middle", 0),
            bb_lower=analysis.get("bollinger", {}).get("lower", 0),
            price_trend="上涨" if prices[-1] > prices[0] else "下跌"
        )
        
        result = self.llm.chat_with_json(
            "你是一个专业的量化交易分析师，给出明确的交易建议。",
            prompt
        )
        
        if result and result.get("action"):
            return TradeSignal(
                action=result.get("action", "hold"),
                confidence=result.get("confidence", 0.5),
                reason=result.get("reason", "LLM 分析"),
                price=current,
                stop_loss=result.get("stop_loss"),
                take_profit=result.get("take_profit")
            )
        
        # 默认返回 hold
        return TradeSignal(action="hold", confidence=0.5, reason="LLM 分析失败", price=current, stop_loss=None, take_profit=None)


# ==================== 模拟交易 ====================

@dataclass
class Position:
    """持仓"""
    coin: str
    amount: float
    entry_price: float
    current_price: float
    pnl: float  # 盈亏
    pnl_percent: float  # 盈亏百分比


@dataclass
class Trade:
    """交易记录"""
    id: str
    timestamp: str
    action: str  # buy/sell
    coin: str
    price: float
    amount: float
    value: float
    pnl: float = 0
    pnl_percent: float = 0


class PaperTrading:
    """模拟交易账户"""
    
    def __init__(self, initial_balance: float = 10000):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.trade_id = 0
    
    def buy(self, coin: str, price: float, amount: float = None) -> bool:
        """买入"""
        if amount is None:
            # 使用 10% 仓位
            amount = (self.balance * 0.1) / price
        
        value = amount * price
        
        if value > self.balance:
            logger.warning(f"余额不足: {value} > {self.balance}")
            return False
        
        self.balance -= value
        
        if coin in self.positions:
            old = self.positions[coin]
            new_amount = old.amount + amount
            avg_price = (old.amount * old.entry_price + amount * price) / new_amount
            self.positions[coin] = Position(
                coin=coin,
                amount=new_amount,
                entry_price=avg_price,
                current_price=price,
                pnl=0,
                pnl_percent=0
            )
        else:
            self.positions[coin] = Position(
                coin=coin,
                amount=amount,
                entry_price=price,
                current_price=price,
                pnl=0,
                pnl_percent=0
            )
        
        # 记录交易
        self.trade_id += 1
        self.trades.append(Trade(
            id=str(self.trade_id),
            timestamp=datetime.now().isoformat(),
            action="buy",
            coin=coin,
            price=price,
            amount=amount,
            value=value
        ))
        
        logger.info(f"买入 {coin}: {amount} @ ${price}")
        return True
    
    def sell(self, coin: str, price: float, amount: float = None) -> bool:
        """卖出"""
        if coin not in self.positions:
            return False
        
        position = self.positions[coin]
        
        if amount is None:
            amount = position.amount
        
        value = amount * price
        cost = amount * position.entry_price
        pnl = value - cost
        pnl_percent = (pnl / cost) * 100
        
        self.balance += value
        
        # 更新持仓
        position.amount -= amount
        if position.amount <= 0:
            del self.positions[coin]
        else:
            position.entry_price = price  # 更新为当前价格
        
        # 记录交易
        self.trade_id += 1
        self.trades.append(Trade(
            id=str(self.trade_id),
            timestamp=datetime.now().isoformat(),
            action="sell",
            coin=coin,
            price=price,
            amount=amount,
            value=value,
            pnl=pnl,
            pnl_percent=pnl_percent
        ))
        
        logger.info(f"卖出 {coin}: {amount} @ ${price}, PnL: ${pnl:.2f} ({pnl_percent:.2f}%)")
        return True
    
    def update_prices(self, prices: Dict[str, float]):
        """更新当前价格和盈亏"""
        for coin, position in self.positions.items():
            if coin in prices:
                position.current_price = prices[coin]
                position.pnl = (position.current_price - position.entry_price) * position.amount
                position.pnl_percent = ((position.current_price / position.entry_price) - 1) * 100
    
    def get_status(self) -> Dict:
        """获取账户状态"""
        total_value = self.balance
        for position in self.positions.values():
            total_value += position.amount * position.current_price
        
        total_pnl = total_value - self.initial_balance
        total_pnl_percent = (total_pnl / self.initial_balance) * 100
        
        return {
            "balance": self.balance,
            "positions_value": total_value - self.balance,
            "total_value": total_value,
            "initial_balance": self.initial_balance,
            "pnl": total_pnl,
            "pnl_percent": total_pnl_percent,
            "positions": [asdict(p) for p in self.positions.values()],
            "total_trades": len(self.trades)
        }


# ==================== 策略进化 ====================

class StrategyEvolver:
    """策略自我进化引擎"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.evolve_history: List[Dict] = []
    
    def analyze_performance(self, trades: List[Trade], account_status: Dict) -> Dict:
        """分析交易表现"""
        if not trades:
            return {"score": 0, "issues": [], "suggestions": []}
        
        # 计算各项指标
        winning_trades = [t for t in trades if t.pnl > 0]
        losing_trades = [t for t in trades if t.pnl < 0]
        
        win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = abs(sum(t.pnl for t in losing_trades) / len(losing_trades)) if losing_trades else 1
        
        profit_factor = avg_win / avg_loss if avg_loss > 0 else 0
        
        # 综合评分
        score = win_rate * 0.4 + min(profit_factor * 20, 60)
        
        issues = []
        suggestions = []
        
        if win_rate < 40:
            issues.append("胜率过低")
            suggestions.append("提高买入信号置信度阈值")
        
        if avg_loss > avg_win:
            issues.append("亏损大于盈利")
            suggestions.append("收紧止损幅度")
        
        if account_status.get("pnl_percent", 0) < -5:
            issues.append("账户亏损超过 5%")
            suggestions.append("降低仓位或暂停交易")
        
        return {
            "score": score,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "issues": issues,
            "suggestions": suggestions,
            "total_trades": len(trades),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades)
        }
    
    def evolve_strategy(self, current_strategy: str, analysis: Dict, market_data: Dict) -> Dict:
        """使用 LLM 进化策略"""
        
        prompt = f"""你是一个量化交易策略专家。请根据以下分析结果，优化交易策略。

当前策略: {current_strategy}

交易表现分析:
- 评分: {analysis.get('score', 0):.1f}/100
- 胜率: {analysis.get('win_rate', 0):.1f}%
- 盈亏比: {analysis.get('profit_factor', 0):.2f}
- 问题: {', '.join(analysis.get('issues', ['无']))}
- 建议: {', '.join(analysis.get('suggestions', ['无']))}

市场数据:
- 当前价格: ${market_data.get('price', 0)}
- 24h涨跌: {market_data.get('change_24h', 0)}%
- RSI: {market_data.get('rsi', 50)}

请给出优化后的策略配置，输出 JSON:
{{
    "strategy_name": "策略名称",
    "new_params": {{
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "macd_threshold": 0,
        "bollinger_multiplier": 2.0,
        "min_confidence": 0.7,
        "stop_loss_percent": 5,
        "take_profit_percent": 15
    }},
    "reasoning": "优化理由"
}}"""
        
        result = self.llm.chat_with_json(
            "你是一个专业的量化交易策略专家，擅长优化交易策略。",
            prompt
        )
        
        if result:
            self.evolve_history.append({
                "timestamp": datetime.now().isoformat(),
                "from": current_strategy,
                "to": result.get("strategy_name", current_strategy),
                "params": result.get("new_params", {}),
                "reasoning": result.get("reasoning", "")
            })
        
        return result or {"strategy_name": current_strategy, "new_params": {}, "reasoning": "无优化建议"}


# ==================== 主交易系统 ====================

class QuantTradingSystem:
    """量化交易系统主类"""
    
    def __init__(self, coin: str = "bitcoin"):
        self.coin = coin
        self.llm = LLMClient()
        self.market = MarketData()
        self.account = PaperTrading(config.initial_balance)
        self.evolver = StrategyEvolver(self.llm)
        
        # 策略
        self.strategies = {
            "MACD": MACDStrategy(),
            "RSI": RSIStrategy(),
            "Bollinger": BollingerStrategy(),
            "LLM": LLMStrategy(self.llm)
        }
        self.current_strategy = "LLM"
        
        # 状态
        self.state_file = config.reports_dir / f"{coin}_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    state = json.load(f)
                    self.current_strategy = state.get("strategy", "LLM")
                    # 恢复账户状态
                    self.account.balance = state.get("balance", config.initial_balance)
                    logger.info(f"已加载状态: 策略={self.current_strategy}, 余额=${self.account.balance:.2f}")
            except:
                pass
    
    def save_state(self):
        """保存状态"""
        state = {
            "coin": self.coin,
            "strategy": self.current_strategy,
            "balance": self.account.balance,
            "updated": datetime.now().isoformat()
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)
    
    def run_trading_cycle(self) -> Dict:
        """运行一个交易周期"""
        logger.info(f"=== 开始交易周期 ({self.coin}) ===")
        
        # 1. 获取市场数据
        coin_data = self.market.get_coin_data(self.coin, days=30)
        prices = []
        if coin_data and "prices" in coin_data:
            prices = [p[1] for p in coin_data["prices"]]
        
        if not prices:
            logger.error("无法获取价格数据")
            return {"error": "无法获取价格数据"}
        
        # 2. 技术分析
        analysis = TechnicalAnalyzer.analyze(prices)
        
        # 3. 获取简单价格
        price_data = self.market.get_simple_price([self.coin])
        current_price = price_data.get(self.coin, {}).get("usd", prices[-1])
        change_24h = price_data.get(self.coin, {}).get("usd_24h_change", 0)
        
        # 4. 更新账户价格
        self.account.update_prices({self.coin: current_price})
        
        # 5. 生成交易信号
        strategy = self.strategies.get(self.current_strategy, self.strategies["LLM"])
        signal = strategy.generate_signal(prices, analysis)
        
        # 6. 执行交易
        if signal.action == "buy":
            self.account.buy(self.coin, current_price)
        elif signal.action == "sell":
            self.account.sell(self.coin, current_price)
        
        # 7. 保存状态
        self.save_state()
        
        # 8. 返回结果
        account_status = self.account.get_status()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "coin": self.coin,
            "price": current_price,
            "change_24h": change_24h,
            "analysis": {
                "rsi": analysis.get("rsi", 50),
                "ma7": analysis.get("ma7", 0),
                "ma25": analysis.get("ma25", 0)
            },
            "signal": asdict(signal),
            "account": account_status,
            "strategy": self.current_strategy
        }
        
        logger.info(f"信号: {signal.action}, 价格: ${current_price}, 余额: ${account_status['balance']:.2f}")
        
        return result
    
    def check_and_evolve(self) -> Dict:
        """检查并进化策略"""
        trades = self.account.trades
        
        # 检查是否需要进化
        account_status = self.account.get_status()
        
        # 获取市场数据
        price_data = self.market.get_simple_price([self.coin])
        current_price = price_data.get(self.coin, {}).get("usd", 50000)
        
        should_evolve = (
            len(trades) >= config.min_trades_for_evolution and
            (
                account_status["pnl_percent"] < config.evolution_threshold * 100 or
                len(trades) % 10 == 0  # 每 10 笔交易进化一次
            )
        )
        
        if should_evolve:
            logger.info("🧬 开始策略进化...")
            
            # 分析表现
            analysis = self.evolver.analyze_performance(trades, account_status)
            
            # 进化策略
            market_data = {
                "price": current_price,
                "change_24h": price_data.get(self.coin, {}).get("usd_24h_change", 0),
                "rsi": analysis.get("rsi", 50)
            }
            
            evolution = self.evolver.evolve_strategy(self.current_strategy, analysis, market_data)
            
            # 应用新策略
            new_strategy = evolution.get("strategy_name", self.current_strategy)
            if new_strategy != self.current_strategy and new_strategy in self.strategies:
                logger.info(f"🔄 策略进化: {self.current_strategy} -> {new_strategy}")
                self.current_strategy = new_strategy
                self.save_state()
            
            return {
                "evolved": True,
                "analysis": analysis,
                "evolution": evolution
            }
        
        return {"evolved": False}
    
    def generate_report(self) -> str:
        """生成每日报告"""
        status = self.account.get_status()
        
        report = f"""
📊 每日量化交易报告
==================
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 市场状态
- 交易品种: {self.coin.upper()}
- 当前策略: {self.current_strategy}

💰 账户状态
- 初始资金: ${status['initial_balance']:.2f}
- 当前余额: ${status['balance']:.2f}
- 持仓价值: ${status['positions_value']:.2f}
- 总资产: ${status['total_value']:.2f}
- 总盈亏: ${status['pnl']:.2f} ({status['pnl_percent']:.2f}%)

📋 持仓明细
"""
        
        for pos in status["positions"]:
            report += f"- {pos['coin']}: {pos['amount']:.6f} @ ${pos['current_price']:.2f} (PnL: {pos['pnl_percent']:.2f}%)\n"
        
        report += f"""
📊 交易统计
- 总交易次数: {status['total_trades']}

🔧 策略状态
- 当前策略: {self.current_strategy}
"""
        
        return report


# ==================== 每日报告发送 ====================

def send_daily_report(report: str):
    """发送每日报告到 Feishu"""
    try:
        from pathlib import Path
        # 尝试发送到 Feishu
        # 这里需要配置 Feishu webhook
        logger.info("报告生成完成")
        print(report)
    except Exception as e:
        logger.error(f"发送报告失败: {e}")


# ==================== 主入口 ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="自我进化量化交易系统")
    parser.add_argument("--coin", default="bitcoin", help="交易币种")
    parser.add_argument("--mode", default="trade", choices=["trade", "report", "evolve"], help="运行模式")
    parser.add_argument("--strategy", help="指定策略")
    
    args = parser.parse_args()
    
    system = QuantTradingSystem(args.coin)
    
    if args.mode == "trade":
        # 运行交易
        result = system.run_trading_cycle()
        
        # 检查并进化
        evolution = system.check_and_evolve()
        result["evolution"] = evolution
        
        # 打印结果
        print(json.dumps(result, indent=2, default=str))
        
    elif args.mode == "report":
        # 生成报告
        report = system.generate_report()
        print(report)
        
    elif args.mode == "evolve":
        # 强制进化
        evolution = system.check_and_evolve()
        print(json.dumps(evolution, indent=2, default=str))
