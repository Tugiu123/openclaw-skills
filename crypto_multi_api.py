#!/usr/bin/env python3
"""
多源加密货币数据获取器
支持 API 备用，当一个失败时自动切换下一个
"""

import json
import urllib.request
import ssl
import time

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# ========== API 配置 ==========
APIS = {
    "coingecko": {
        "name": "CoinGecko",
        "url": "https://api.coingecko.com/api/v3/simple/price",
        "params": "ids={coins}&vs_currencies=usd&include_24hr_change=true",
        "delay": 1.5,
        "limit": "10-50/min"
    },
    "coincap": {
        "name": "CoinCap",
        "url": "https://api.coincap.io/v2/assets",
        "params": "ids={coins}",
        "delay": 0,
        "limit": "无限制"
    },
    "binance": {
        "name": "Binance",
        "url": "https://api.binance.com/api/v3/ticker/24hr",
        "params": "symbol={symbol}USDT",
        "delay": 0,
        "limit": "1200/min"
    },
    "cryptocompare": {
        "name": "CryptoCompare",
        "url": "https://min-api.cryptocompare.com/data/pricemulti",
        "params": "fsyms={coins}&tsyms=USD",
        "delay": 0,
        "limit": "高级"
    }
}

COINS = ["bitcoin", "ethereum", "solana", "ripple", "cardano", "dogecoin"]
SYMBOLS = ["BTC", "ETH", "SOL", "XRP", "ADA", "DOGE"]

def fetch_coingecko():
    """CoinGecko API"""
    coins = ",".join(COINS)
    url = f"{APIS['coingecko']['url']}?{APIS['coingecko']['params'].format(coins=coins)}"
    time.sleep(APIS['coingecko']['delay'])
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        result = {}
        for coin in COINS:
            if coin in data:
                result[coin] = {
                    'price': data[coin].get('usd', 0),
                    'change_24h': data[coin].get('usd_24h_change', 0)
                }
        return result

def fetch_coincap():
    """CoinCap API - 完全免费，无限制"""
    ids = ",".join(COINS)
    url = f"{APIS['coincap']['url']}?ids={ids}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        result = {}
        for item in data.get('data', []):
            result[item['id']] = {
                'price': float(item.get('priceUsd', 0)),
                'change_24h': float(item.get('changePercent24Hr', 0))
            }
        return result

def fetch_binance():
    """Binance API - 官方交易所数据"""
    result = {}
    for symbol in SYMBOLS[:6]:
        url = f"{APIS['binance']['url']}?symbol={symbol}USDT"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                coin_id = symbol.lower()
                result[coin_id] = {
                    'price': float(data.get('lastPrice', 0)),
                    'change_24h': float(data.get('priceChangePercent', 0))
                }
        except:
            continue
    return result

def fetch_cryptocompare():
    """CryptoCompare API"""
    coins = ",".join([s.upper() for s in COINS])
    url = f"{APIS['cryptocompare']['url']}?fsyms={coins}&tsyms=USD"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        result = {}
        for coin in COINS:
            symbol = coin.upper()
            if symbol in data:
                result[coin] = {
                    'price': data[symbol].get('USD', 0),
                    'change_24h': 0  # 需要额外请求
                }
        return result

def get_price_auto():
    """自动切换获取价格"""
    
    print("=" * 60)
    print("💰 多源加密货币价格获取")
    print("=" * 60)
    
    # 按优先级尝试
    apis_to_try = [
        ("CoinGecko", fetch_coingecko),
        ("CoinCap", fetch_coincap),
        ("Binance", fetch_binance),
        ("CryptoCompare", fetch_cryptocompare),
    ]
    
    for name, func in apis_to_try:
        print(f"\n尝试: {name}...", end=" ")
        try:
            data = func()
            if data:
                print(f"✅ 成功!")
                print(f"\n📊 {name} 价格数据:")
                print("-" * 40)
                
                for coin, info in data.items():
                    price = info['price']
                    change = info.get('change_24h', 0)
                    trend = "📈" if change > 0 else "📉"
                    print(f"  {coin.capitalize():12} ${price:>12,.2f}  {trend} {change:+.2f}%")
                
                return data
        except Exception as e:
            print(f"❌ 失败: {str(e)[:30]}")
            continue
    
    print("\n❌ 所有 API 都失败了")
    return None

def show_api_comparison():
    """显示 API 对比"""
    print("\n" + "=" * 60)
    print("📋 可用加密货币 API 对比")
    print("=" * 60)
    
    for key, api in APIS.items():
        print(f"\n🔹 {api['name']}")
        print(f"   限流: {api['limit']}")
        print(f"   特点: ", end="")
        if key == "coingecko":
            print("免费全面，热门币种首选")
        elif key == "coincap":
            print("完全免费，无限制，数据简洁")
        elif key == "binance":
            print("官方交易所数据，最实时")
        elif key == "cryptocompare":
            print("专业级数据，支持更多币种")

if __name__ == "__main__":
    get_price_auto()
    show_api_comparison()
