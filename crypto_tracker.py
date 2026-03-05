#!/usr/bin/env python3
"""
CoinGecko 加密货币市场数据获取
免费 API: https://api.coingecko.com/api/v3
"""

import json
import urllib.request
import urllib.error
import ssl
import time
from datetime import datetime

# 请求间隔（秒）- 免费 API 建议 1.5-3 秒
REQUEST_DELAY = 2

# SSL 上下文
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BASE_URL = "https://api.coingecko.com/api/v3"

def get_trending():
    """获取 trending 加密货币"""
    url = f"{BASE_URL}/search/trending"
    try:
        time.sleep(REQUEST_DELAY)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            return data.get('coins', [])[:10]
    except Exception as e:
        print(f"Error fetching trending: {e}")
        return []

def get_market_data(ids=None, currency='usd', limit=20):
    """获取市场数据"""
    if ids:
        ids_str = ','.join(ids)
        url = f"{BASE_URL}/coins/markets?vs_currency={currency}&ids={ids_str}&order=market_cap_desc&per_page={limit}&page=1&sparkline=false"
    else:
        url = f"{BASE_URL}/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={limit}&page=1&sparkline=false"
    
    try:
        time.sleep(REQUEST_DELAY)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return []

def get_simple_price(ids, currency='usd'):
    """获取简单价格"""
    ids_str = ','.join(ids)
    url = f"{BASE_URL}/simple/price?ids={ids_str}&vs_currencies={currency}&include_24hr_change=true"
    try:
        time.sleep(REQUEST_DELAY)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching price: {e}")
        return {}

def get_global_data():
    """获取全球市场数据"""
    url = f"{BASE_URL}/global"
    try:
        time.sleep(REQUEST_DELAY)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            return json.loads(response.read().decode()).get('data', {})
    except Exception as e:
        print(f"Error fetching global data: {e}")
        return {}

def format_num(num):
    """格式化数字"""
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"

def analyze_crypto():
    """分析加密市场"""
    print("=" * 60)
    print("📊 COINGECKO 加密货币市场分析")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 1. 全球市场概览
    print("🌍 全球市场概览")
    print("-" * 40)
    global_data = get_global_data()
    if global_data:
        total_market_cap = global_data.get('market_cap_percentage', {})
        btc_dominance = total_market_cap.get('btc', 0)
        eth_dominance = total_market_cap.get('eth', 0)
        
        print(f"  BTC 市占率: {btc_dominance:.1f}%")
        print(f"  ETH 市占率: {eth_dominance:.1f}%")
        print(f"  活跃加密货币: {global_data.get('active_cryptocurrencies', 'N/A')}")
        print()
    
    # 2. Top 10 市场数据
    print("💎 Top 10 加密货币")
    print("-" * 40)
    top_coins = get_market_data(limit=10)
    
    if top_coins:
        for coin in top_coins:
            name = coin.get('name', 'Unknown')
            symbol = coin.get('symbol', '').upper()
            price = coin.get('current_price', 0)
            change_24h = coin.get('price_change_percentage_24h', 0)
            market_cap = coin.get('market_cap', 0)
            volume = coin.get('total_volume', 0)
            
            trend = "📈" if change_24h > 0 else "📉"
            print(f"  {name} ({symbol})")
            print(f"    价格: ${price:,.2f} {trend} {change_24h:+.2f}%")
            print(f"    市值: {format_num(market_cap)} | 24h量: {format_num(volume)}")
            print()
    
    # 3. 实时价格追踪
    print("💰 实时价格追踪")
    print("-" * 40)
    track_ids = ['bitcoin', 'ethereum', 'solana', 'ripple', 'cardano']
    prices = get_simple_price(track_ids)
    
    for coin_id, data in prices.items():
        price = data.get('usd', 0)
        change = data.get('usd_24h_change', 0)
        trend = "📈" if change > 0 else "📉"
        print(f"  {coin_id.capitalize()}: ${price:,.2f} {trend} {change:+.2f}%")
    print()
    
    # 4. Trending 热门币
    print("🔥 Trending 热门币")
    print("-" * 40)
    trending = get_trending()
    
    for item in trending[:5]:
        coin = item.get('item', {})
        name = coin.get('name', 'Unknown')
        symbol = coin.get('symbol', '').upper()
        market_cap_rank = coin.get('market_cap_rank', 'N/A')
        print(f"  #{market_cap_rank} {name} ({symbol})")
    print()
    
    # 5. 交易信号
    print("🎯 交易信号")
    print("-" * 40)
    
    # 找出 24h 涨幅最大的
    if top_coins:
        sorted_by_change = sorted(top_coins, key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)
        
        top_gainer = sorted_by_change[0]
        top_loser = sorted_by_change[-1]
        
        print(f"  📈 涨幅最大: {top_gainer['name']} ({top_gainer.get('price_change_percentage_24h', 0):+.2f}%)")
        print(f"  📉 跌幅最大: {top_loser['name']} ({top_loser.get('price_change_percentage_24h', 0):+.2f}%)")
    print()
    
    print("=" * 60)
    print("💡 提示: CoinGecko 免费 API 限制 10-50 次/分钟")
    print("=" * 60)

def main():
    """主函数"""
    analyze_crypto()
    
    # 保存数据
    try:
        top_coins = get_market_data(limit=50)
        global_data = get_global_data()
        
        with open('crypto_data.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'global': global_data,
                'markets': top_coins
            }, f, indent=2)
        print("\n📁 数据已保存到 crypto_data.json")
    except Exception as e:
        print(f"\n保存数据失败: {e}")

if __name__ == "__main__":
    main()
