#!/usr/bin/env python3
"""
每日加密货币市场分析报告
自动推送到 Feishu
"""

import json
import urllib.request
import ssl
import time
import sys

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/你的机器人ID"  # 需替换

def get_data(url):
    time.sleep(1.2)  # 避免 API 限流
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error: {e}")
        return None

def format_num(num):
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    else:
        return f"${num:,.0f}"

def generate_report():
    """生成市场分析报告"""
    
    print("📊 正在获取市场数据...")
    
    # 获取数据
    global_data = get_data("https://api.coingecko.com/api/v3/global")
    markets = get_data("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false")
    trending = get_data("https://api.coingecko.com/api/v3/search/trending")
    
    if not markets:
        print("❌ 无法获取数据")
        return None
    
    # 构建报告
    report = f"""📊 **每日加密货币市场分析**
🕐 {time.strftime('%Y-%m-%d %H:%M', time.localtime())}

---

**🌍 全球概览**
"""
    
    if global_data and global_data.get('data'):
        data = global_data['data']
        report += f"| BTC 市占 | ETH 市占 | 活跃币种 |\n"
        report += f"| {data.get('market_cap_percentage', {}).get('btc', 0):.1f}% | {data.get('market_cap_percentage', {}).get('eth', 0):.1f}% | {data.get('active_cryptocurrencies', 0):,} |\n"
    
    report += f"\n**💎 Top 10 市值排行**\n"
    report += f"| # | 币种 | 价格 | 24h | 市值 |\n"
    report += f"|---|------|------|-----|-----|\n"
    
    for i, coin in enumerate(markets, 1):
        name = coin['symbol'].upper()
        price = coin['current_price']
        change = coin['price_change_percentage_24h']
        cap = coin['market_cap']
        trend = "📈" if change > 0 else "📉"
        report += f"| {i} | {name:6} | ${price:>10,} | {trend}{change:+.1f}% | {format_num(cap):>8} |\n"
    
    # Trending
    report += f"\n**🔥 Trending 热门 (前5)**\n"
    if trending:
        for item in trending.get('coins', [])[:5]:
            coin = item.get('item', {})
            rank = coin.get('market_cap_rank', '-')
            name = coin.get('symbol', '').upper()
            report += f"- #{rank} {name}\n"
    
    # 交易信号
    report += f"\n**🎯 今日信号**\n"
    gainers = sorted(markets, key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)[:2]
    losers = sorted(markets, key=lambda x: x.get('price_change_percentage_24h', 0))[:2]
    
    if gainers:
        report += f"📈 涨幅: {gainers[0]['symbol'].upper()} (+{gainers[0]['price_change_percentage_24h']:.1f}%)\n"
    if losers:
        report += f"📉 跌幅: {losers[0]['symbol'].upper()} ({losers[0]['price_change_percentage_24h']:.1f}%)\n"
    
    report += f"\n---\n*自动生成 by CoinGecko API*"
    
    return report

def send_to_feishu(content):
    """发送到 Feishu"""
    # 简化版：只打印
    print("\n" + "=" * 60)
    print(content)
    print("=" * 60)
    
    # TODO: 实现 Feishu webhook 推送
    # webhook_url = FEISHU_WEBHOOK
    # data = {"msg_type": "text", "content": {"text": content}}
    # requests.post(webhook_url, json=data)

def main():
    report = generate_report()
    if report:
        send_to_feishu(report)
        print("\n✅ 报告生成完成")

if __name__ == "__main__":
    main()
