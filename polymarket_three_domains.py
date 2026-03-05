#!/usr/bin/env python3
"""
Polymarket 三领域监控: 加密货币、体育、政治事件
专注于用户指定的三大领域
"""

import json
import re
import urllib.request
import ssl
from datetime import datetime

# SSL 配置
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 关键词配置
KEYWORDS = {
    'crypto': [
        'bitcoin', 'btc', 'ethereum', 'eth', 'solana', 'crypto',
        '加密', 'bitcoin', 'ether', 'ripple', 'bnb', 'cardano',
        'price', 'above', 'below', 'million', 'billion'
    ],
    'sports': [
        'vs', 'win', 'beat', 'gold medal', 'champion', 'final',
        'olympic', 'nba', 'nfl', 'football', 'soccer', 'tennis',
        'score', 'match', 'game', 'tournament', 'cup'
    ],
    'politics': [
        'trump', 'biden', 'president', 'election', 'congress',
        'senate', 'fed', 'government', 'shutdown', 'nominee',
        'republican', 'democrat', 'policy', 'law', 'bill'
    ]
}

def fetch_market_data():
    """从 Polymarket 获取数据"""
    urls = [
        "https://polymarket.com",
        "https://polymarket.com/category/crypto",
        "https://polymarket.com/category/politics",
        "https://polymarket.com/category/sports"
    ]
    
    all_markets = []
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive'
            })
            
            with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
                html = response.read().decode('utf-8', errors='ignore')
                markets = parse_html_markets(html)
                all_markets.extend(markets)
                print(f"✅ 从 {url.split('/')[-1] or 'homepage'} 获取 {len(markets)} 个市场")
                
        except Exception as e:
            print(f"❌ Error fetching {url}: {str(e)[:50]}")
            continue
    
    return all_markets

def parse_html_markets(html):
    """解析 HTML 中的市场数据"""
    markets = []
    
    # 提取问题、价格和交易量
    pattern = r'"question":"([^"]+)"[^}]*?"outcomePrices":(\[.*?\])[^}]*?"volume":([\d.]+)'
    matches = re.findall(pattern, html)
    
    for q, prices_str, vol in matches:
        try:
            vol_float = float(vol)
            prices = json.loads(prices_str.replace('"', '"'))
            
            if len(prices) >= 2:
                markets.append({
                    'question': q,
                    'volume': vol_float,
                    'yes_price': float(prices[0]),
                    'no_price': float(prices[1]),
                    'category': categorize_market(q)
                })
        except:
            continue
    
    return markets

def categorize_market(question):
    """判断市场类别"""
    q_lower = question.lower()
    
    for kw in KEYWORDS['crypto']:
        if kw in q_lower:
            return 'crypto'
    
    for kw in KEYWORDS['sports']:
        if kw in q_lower:
            return 'sports'
    
    for kw in KEYWORDS['politics']:
        if kw in q_lower:
            return 'politics'
    
    return 'other'

def analyze_opportunities(markets):
    """分析交易机会"""
    
    print("\n" + "=" * 70)
    print("🎯 POLYMARKET 三领域交易机会分析")
    print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 按类别分组
    categorized = {'crypto': [], 'sports': [], 'politics': [], 'other': []}
    for m in markets:
        categorized[m['category']].append(m)
    
    results = {}
    
    for category, items in categorized.items():
        if not items:
            continue
            
        items.sort(key=lambda x: x['volume'], reverse=True)
        results[category] = items
        
        icon = {'crypto': '₿', 'sports': '🏀', 'politics': '🏛️'}.get(category, '📊')
        title = {'crypto': '加密货币', 'sports': '体育赛事', 'politics': '政治事件'}.get(category, '其他')
        
        print(f"\n{icon} {title} - Top 10 高交易量市场")
        print("-" * 60)
        
        for i, m in enumerate(items[:10]):
            q = m['question'][:50]
            yes = m['yes_price']
            no = m['no_price']
            vol = m['volume']
            
            # 计算隐含概率
            total = yes + no if yes + no > 0 else 1
            yes_prob = yes / total * 100
            no_prob = no / total * 100
            
            # 标记机会
            opportunity = ""
            if no > 0.85:
                opportunity = " 🔥 NO机会"
            elif yes > 0.85:
                opportunity = " 🔥 YES机会"
            
            print(f"{i+1}. {q}...")
            print(f"   Yes: ${yes:.4f} ({yes_prob:.1f}%) | No: ${no:.4f} ({no_prob:.1f}%)")
            print(f"   💰 Vol: ${vol:,.0f}{opportunity}")
            print()

def generate_strategy(category, markets):
    """生成策略建议"""
    
    print("=" * 70)
    print(f"📈 {category.upper()} 交易策略建议")
    print("=" * 70)
    
    # 策略1: 押注 NO（高胜率）
    no_bets = [m for m in markets if m['no_price'] > 0.70 and m['volume'] > 500]
    no_bets.sort(key=lambda x: x['no_price'], reverse=True)
    
    print("\n📌 策略1: 押注 NO（高胜率）")
    print("-" * 40)
    
    if no_bets:
        for m in no_bets[:5]:
            q = m['question'][:45]
            no_p = m['no_price']
            vol = m['volume']
            expected_roi = (no_p / (1 - no_p)) * 100 if no_p < 0.99 else 0
            
            print(f"  • {q}...")
            print(f"    No 价格: ${no_p:.2f} | Vol: ${vol:,.0f}")
            print(f"    预期回报率: {expected_roi:.0f}%")
            print()
    else:
        print("  暂无符合条件的 NO 押注机会")
    
    # 策略2: 极端价格套利
    extreme = [m for m in markets if m['yes_price'] > 0.95 or m['no_price'] > 0.95]
    
    print("\n📌 策略2: 极端价格套利")
    print("-" * 40)
    
    for m in extreme[:5]:
        q = m['question'][:45]
        yes = m['yes_price']
        no = m['no_price']
        side = "YES" if yes > no else "NO"
        
        print(f"  • {q}...")
        print(f"    {side}: ${max(yes, no):.4f} (极端价格)")
        print(f"    建议: {'小额反向押注' if side == 'YES' else '小额反向押注'}")
        print()

def save_results(markets, categorized):
    """保存结果"""
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_markets': len(markets),
        'by_category': {k: len(v) for k, v in categorized.items()},
        'top_opportunities': []
    }
    
    # 保存高机会市场
    for m in markets:
        if m['volume'] > 1000 and (m['yes_price'] > 0.80 or m['no_price'] > 0.80):
            output['top_opportunities'].append({
                'question': m['question'],
                'category': m['category'],
                'yes_price': m['yes_price'],
                'no_price': m['no_price'],
                'volume': m['volume']
            })
    
    with open('polymarket_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 结果已保存到 polymarket_analysis.json")
    print(f"   共分析 {len(markets)} 个市场")

def main():
    """主函数"""
    
    print("⏳ 正在获取 Polymarket 三领域数据...")
    print("   关注: 加密货币 | 体育赛事 | 政治事件\n")
    
    markets = fetch_market_data()
    
    if not markets:
        print("\n❌ 无法获取数据")
        print("建议: 直接访问 polymarket.com 查看实时市场")
        return
    
    print(f"\n✅ 共获取 {len(markets)} 个市场")
    
    # 分类统计
    categorized = {'crypto': [], 'sports': [], 'politics': [], 'other': []}
    for m in markets:
        categorized[m['category']].append(m)
    
    for cat, items in categorized.items():
        if items:
            icon = {'crypto': '₿', 'sports': '🏀', 'politics': '🏛️'}.get(cat, '📊')
            title = {'crypto': '加密货币', 'sports': '体育赛事', 'politics': '政治事件'}.get(cat, '其他')
            print(f"   {icon} {title}: {len(items)} 个市场")
    
    # 分析机会
    analyze_opportunities(markets)
    
    # 生成策略
    for cat in ['crypto', 'sports', 'politics']:
        if categorized[cat]:
            generate_strategy(cat, categorized[cat])
    
    # 保存结果
    save_results(markets, categorized)
    
    print("\n" + "=" * 70)
    print("💡 提示")
    print("=" * 70)
    print("1. 访问 polymarket.com 查看完整市场列表")
    print("2. 选择高交易量 + 极端价格的市场")
    print("3. 使用策略1押注 NO，获取高胜率")
    print("4. 监控逻辑套利机会（政府公告、新闻）")

if __name__ == "__main__":
    main()
