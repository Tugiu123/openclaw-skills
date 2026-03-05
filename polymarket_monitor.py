#!/usr/bin/env python3
"""
Polymarket 实时监控脚本
使用 API 获取市场数据
"""

import json
import urllib.request
import ssl
from datetime import datetime

# SSL 配置
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# API 端点
API_BASE = "https://gamma-api.polymarket.com"

def fetch_markets(limit=200):
    """获取活跃市场列表"""
    
    # 使用多个端点获取数据
    urls = [
        f"{API_BASE}/markets?limit={limit//2}&order=volume24hr&order_direction=desc",
        f"{API_BASE}/markets?open=true&limit={limit//2}&order=volume&order_direction=desc"
    ]
    
    all_markets = []
    
    for i, url in enumerate(urls, 1):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
            
            print(f"🌐 正在获取市场数据 (源 {i}/{len(urls)})...")
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            markets = []
            if 'data' in data:
                markets = data['data']
            elif isinstance(data, list):
                markets = data
            elif isinstance(data, dict):
                markets = [data]
            
            # 去重（基于ID）
            seen_ids = {m['id'] for m in all_markets}
            for m in markets:
                if m.get('id') not in seen_ids:
                    all_markets.append(m)
                    seen_ids.add(m.get('id'))
            
            print(f"  ✓ 获取 {len(markets)} 个市场")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
            continue
    
    # 按交易量排序（优先使用volume24hr）
    all_markets.sort(key=lambda x: float(x.get('volume24hr', x.get('volume', 0))), reverse=True)
    
    return all_markets[:limit]

def categorize_market(title):
    """判断市场类别"""
    title_lower = title.lower()
    
    crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'solana', 'crypto', 'xrp', 
                      'dogecoin', 'cardano', 'ada', 'price', 'million', 'billion',
                      '加密', '币', 'debut', 'launch', 'token', 'nft']
    
    sports_keywords = ['vs', 'win', 'beat', 'gold medal', 'champion', 'final',
                      'olympic', 'nba', 'nfl', 'football', 'soccer', 'tennis',
                      'score', 'match', 'game', 'tournament', 'cup', 'team',
                      'wins', 'will win', 'win the', 'olympics', 'super bowl',
                      'mlb', 'nhl', 'ufc', 'fight', 'race', 'grand prix']
    
    politics_keywords = ['trump', 'biden', 'president', 'election', 'congress',
                        'senate', 'fed', 'government', 'shutdown', 'nominee',
                        'republican', 'democrat', 'policy', 'law', 'bill',
                        'will be elected', 'presidential', 'house', 'senate seat',
                        'governor', 'mayor', 'cabinet', 'visit', 'inauguration']
    
    for kw in crypto_keywords:
        if kw in title_lower:
            return 'crypto'
    
    for kw in sports_keywords:
        if kw in title_lower:
            return 'sports'
    
    for kw in politics_keywords:
        if kw in title_lower:
            return 'politics'
    
    return 'other'

def format_price(price):
    """格式化价格"""
    if price is None:
        return "N/A"
    return f"${price:.4f}"

def format_volume(vol):
    """格式化交易量"""
    if vol is None:
        return "$0"
    try:
        vol_num = float(vol)
    except (ValueError, TypeError):
        return "N/A"
    if vol_num == 0:
        return "$0"
    if vol_num >= 1000000:
        return f"${vol_num/1000000:.1f}M"
    if vol_num >= 1000:
        return f"${vol_num/1000:.0f}K"
    return f"${vol_num:.0f}"

def get_opportunity_tag(yes_price, no_price):
    """获取机会标签"""
    if yes_price is None or no_price is None:
        return ""
    
    if no_price >= 0.85:
        return " 🔥 NO高概率"
    elif yes_price >= 0.85:
        return " 🔥 YES高概率"
    elif no_price >= 0.70:
        return " ⚡ NO机会"
    elif yes_price >= 0.70:
        return " ⚡ YES机会"
    return ""

def analyze_markets(markets):
    """分析市场数据"""
    
    # 分类
    categories = {'crypto': [], 'sports': [], 'politics': [], 'other': []}
    
    for market in markets:
        title = market.get('question') or market.get('title', '')
        category = categorize_market(title)
        
        # 解析 outcomePrices (JSON字符串数组)
        yes_price = None
        no_price = None
        
        outcome_prices = market.get('outcomePrices')
        if outcome_prices:
            try:
                prices = json.loads(outcome_prices.replace('"', '"'))
                if len(prices) >= 2:
                    yes_price = float(prices[0])
                    no_price = float(prices[1])
            except:
                pass
        
        # 使用volume作为主要指标
        total_volume = float(market.get('volume', 0))
        volume_24hr = float(market.get('volume24hr', 0))
        
        categories[category].append({
            'title': title,
            'volume_24hr': volume_24hr,
            'volume': total_volume,
            'yes_price': yes_price,
            'no_price': no_price,
            'best_bid': market.get('bestBid'),
            'best_ask': market.get('bestAsk'),
            'last_trade_price': market.get('lastTradePrice'),
            'id': market.get('id', ''),
            'slug': market.get('slug', ''),
            'end_date': market.get('endDateIso', ''),
            'liquidity': market.get('liquidity', 0),
            'active': market.get('active', False),
            'outcome_prices': outcome_prices
        })
    
    # 按交易量排序
    for cat in categories:
        categories[cat].sort(key=lambda x: x['volume'], reverse=True)
    
    return categories

def generate_report(categories):
    """生成报告"""
    
    print("\n" + "=" * 80)
    print("🎯 POLYMARKET 三领域市场监控简报")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S (Asia/Shanghai)')}")
    print("=" * 80)
    
    category_names = {
        'crypto': ('💰 加密货币', '₿'),
        'sports': ('⚽ 体育赛事', '🏀'),
        'politics': ('🏛️ 政治事件', '🗳️'),
        'other': ('📊 其他', '📈')
    }
    
    highlights = []
    
    for cat in ['crypto', 'sports', 'politics', 'other']:
        if not categories[cat]:
            continue
            
        name, icon = category_names[cat]
        
        print(f"\n{icon} {name} (共 {len(categories[cat])} 个市场)")
        print("-" * 80)
        
        # 显示所有市场，但优先显示有合理价格的市场
        # 过滤掉已经解析的市场（prices是1和0）
        reasonable_markets = [m for m in categories[cat] 
                             if m['yes_price'] is not None and m['no_price'] is not None
                             and m['outcome_prices'] not in ['["1", "0"]', '["0", "1"]']
                             and 0.01 < m['yes_price'] < 0.99]
        
        if reasonable_markets:
            markets_to_show = reasonable_markets[:10]
        else:
            markets_to_show = categories[cat][:10]
        
        for i, m in enumerate(markets_to_show):
            title_short = m['title'][:55] + "..." if len(m['title']) > 55 else m['title']
            vol = m['volume']
            yes_price = m['yes_price']
            no_price = m['no_price']
            
            opportunity = get_opportunity_tag(yes_price, no_price)
            
            if opportunity and vol >= 1000:  # 只记录有意义的交易量
                highlights.append({
                    'category': cat,
                    'title': m['title'],
                    'opportunity': opportunity,
                    'volume': vol
                })
            
            print(f"{i+1:2d}. {title_short}")
            if yes_price is not None and no_price is not None:
                total = yes_price + no_price
                yes_prob = (yes_price / total * 100) if total > 0 else 0
                no_prob = (no_price / total * 100) if total > 0 else 0
                
                print(f"    YES: {format_price(yes_price)} ({yes_prob:.1f}%) | NO: {format_price(no_price)} ({no_prob:.1f}%)")
            else:
                print(f"    价格数据不可用")
            print(f"    💰 总交易量: {format_volume(vol)}{opportunity}")
            print()
        
        if not markets_to_show:
            print("  暂无活跃市场\n")
    
    # 生成简报摘要
    print("=" * 80)
    print("🔍 重点交易机会 (高交易量 + 极端价格)")
    print("=" * 80)
    
    if highlights:
        # 按交易量排序
        highlights.sort(key=lambda x: x['volume'], reverse=True)
        
        for i, h in enumerate(highlights[:20]):
            category_cn = {'crypto': '加密货币', 'sports': '体育', 'politics': '政治'}.get(h['category'], '其他')
            print(f"{i+1:2d}. [{category_cn}] {h['title'][:60]}...")
            print(f"    {h['opportunity']} | {format_volume(h['volume'])}")
            print()
    else:
        print("   未发现高交易量的极端价格机会")
        print()
    
    # 策略建议
    print("=" * 80)
    print("💡 交易策略建议")
    print("=" * 80)
    print()
    print("1️⃣  高胜率策略: 押注 NO (价格 > 0.70)")
    print("   • 查找 NO 价格高于 $0.70 的市场")
    print("   • 重点关注高交易量市场 (24H交易量 >$10K)")
    print("   • 理性评估事件发生的实际概率")
    print()
    print("2️⃣  极端价格套利: 价格 > 0.85")
    print(f"   • 当前发现 {len([h for h in highlights if '高概率' in h['opportunity']])} 个极端价格机会")
    print("   • 可考虑小额反向押注对冲风险")
    print()
    print("3️⃣  交易量优先策略")
    print("   • 优先选择24H交易量 >$50K 的市场")
    print("   • 流动性好，便于进出")
    print()
    
    return highlights

def save_report(markets, highlights):
    """保存报告"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_markets': len(markets),
        'highlights_count': len(highlights),
        'highlights': highlights,
        'data': markets
    }
    
    filename = f"polymarket_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📁 完整数据已保存: {filename}")

def main():
    """主函数"""
    
    print("\n⏳ Polymarket 市场扫描启动...")
    print("   领域: 加密货币 | 体育赛事 | 政治事件\n")
    
    # 获取市场数据
    markets = fetch_markets(200)
    
    if not markets:
        print("\n❌ 无法获取市场数据")
        return
    
    print(f"\n✅ 获取到 {len(markets)} 个市场")
    
    # 分析市场
    categories = analyze_markets(markets)
    
    # 显示统计
    print(f"\n📊 市场分类:")
    print(f"   💰 加密货币: {len(categories['crypto'])} 个")
    print(f"   ⚽ 体育赛事: {len(categories['sports'])} 个")
    print(f"   🏛️ 政治事件: {len(categories['politics'])} 个")
    print(f"   📊 其他: {len(categories['other'])} 个")
    
    # 生成报告
    highlights = generate_report(categories)
    
    # 保存报告
    save_report(markets, highlights)
    
    print("\n" + "=" * 80)
    print("✅ 扫描完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
