#!/bin/bash
# 🧠 Smart Daily Learning System v2
# Uses web search + deep fetch + AI understanding

DATE=$(date +"%Y-%m-%d")
REPORT_FILE=~/.openclaw/workspace/daily_learning_report.md
MEMORY_FILE=~/.openclaw/workspace/memory/${DATE}.md

echo "🧠 开始智能学习..."

# ============================================
# 1️⃣ OpenClaw 官方更新追踪
# ============================================
echo "📡 抓取 OpenClaw 官方动态..."

# 获取最新 release
RELEASE=$(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null)
VERSION=$(echo "$RELEASE" | grep -o '"tag_name": *"[^"]*"' | cut -d'"' -f4)
RELEASE_NOTES=$(echo "$RELEASE" | grep -o '"body": *"[^"]*"' | head -c 500 | cut -d'"' -f4 | tr -d '\\n\\r')

# 获取重要 commits
COMMITS=$(curl -s "https://api.github.com/repos/openclaw/openclaw/commits?per_page=10" 2>/dev/null)
TOP_COMMITS=$(echo "$COMMITS" | grep -o '"message": *"[^"]*"' | head -5 | cut -d'"' -f4 | sed 's/"/\\"/g')

# ============================================
# 2️⃣ GitHub 热门项目探索（AI/Agent 领域）
# ============================================
echo "🔥 搜索 AI/Agent 热门项目..."

# 使用正确的 GitHub Search API 格式
SEARCH_RESULTS=$(curl -s "https://api.github.com/search/repositories?q=language:python+topic:agent+stars:>1000\&sort=stars\&per_page=5" 2>/dev/null)
TOP_REPOS=$(echo "$SEARCH_RESULTS" | grep -o '"full_name": *"[^"]*"' | head -5 | cut -d'"' -f4)

# 如果搜索失败，使用备用列表
if [[ -z "$TOP_REPOS" ]]; then
    echo "⚠️ GitHub API 受限，使用手动热门列表..."
    TOP_REPOS="anthropics/claude-code
langchain-ai/langchain
openai/openai-realtime-api
autoGPT/autogpt
microsoft/autogen"
fi

# 抓取 1-2 个最相关的项目深度学习
DEEP_LEARNING=""
KIMI_ANALYSIS=""

for REPO in $(echo "$TOP_REPOS" | head -2); do
    echo "📖 深度学习: $REPO"
    README=$(curl -s "https://raw.githubusercontent.com/$REPO/main/README.md" 2>/dev/null | head -c 1500)
    DESC=$(curl -s "https://api.github.com/repos/$REPO" 2>/dev/null | grep -o '"description": *"[^"]*"' | cut -d'"' -f4)
    
    DEEP_LEARNING="${DEEP_LEARNING}\n### 📦 $REPO\n**描述**: $DESC\n\n**README 摘要**:\n\`\`\`\n${README:0:800}\n\`\`\`\n"
    
    # 可选：调用 Kimi/GLM 深度分析（如果配置了 API key）
    if [[ -n "$KIMI_API_KEY" ]]; then
        echo "🤖 调用 Kimi 深度分析..."
        ANALYSIS=$(curl -s -X POST "https://api.m1/chat/comoonshot.cn/vpletions" \
            -H "Authorization: Bearer $KIMI_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{"model": "kimi-128k", "messages": [{"role": "system", "content": "你是技术架构分析师。请分析以下开源项目，用中文总结：1) 核心功能 2) 技术架构 3) 与 OpenClaw 的结合点"}, {"role": "user", "content": "'"$DESC $README"'"}]}' 2>/dev/null | grep -o '"content": *"[^"]*"' | head -1 | cut -d'"' -f4 || echo "")
        
        if [[ -n "$ANALYSIS" ]]; then
            KIMI_ANALYSIS="${KIMI_ANALYSIS}\n### 🔬 $REPO (Kimi 分析)\n$ANALYSIS\n"
        fi
    fi
done

# ============================================
# 3️⃣ 生成智能摘要（用 OpenClaw 自身理解）
# ============================================

# 计算学习洞察
cat > "$REPORT_FILE" << EOF
# 🧠 每日智能学习报告 - $DATE

## 🎯 OpenClaw 官方动态

**最新版本**: $VERSION

**版本更新**:
\`\`\`
$RELEASE_NOTES
\`\`\`

**关键 Commits**:
$TOP_COMMITS

## 🔥 GitHub 热门项目（AI/Agent 领域）

**本周热门**:
$TOP_REPOS

## 📖 深度学习

$DEEP_LEARNING

$KIMI_ANALYSIS

## 💡 今日洞察

EOF

# 添加智能洞察
if [[ "$VERSION" == *"v2026"* ]]; then
    echo "- OpenClaw 更新频繁，建议保持关注" >> "$REPORT_FILE"
fi

if echo "$TOP_COMMITS" | grep -qi "security\|fix"; then
    echo "- 本次更新包含安全/修复，建议评估影响" >> "$REPORT_FILE"
fi

if [[ -n "$DEEP_LEARNING" ]]; then
    echo "- 发现 $TOP_REPOS 个相关项目，值得研究其架构设计" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*学习完成: $(date)*" >> "$REPORT_FILE"

# ============================================
# 4️⃣ 记忆存储
# ============================================
echo "💾 存储到记忆..."
cat > "$MEMORY_FILE" << EOF
# $DATE 学习记录

## OpenClaw 更新
- 版本: $VERSION
- 关键改动: ${TOP_COMMITS:0:200}

## 学到的新项目
$(echo "$TOP_REPOS" | head -3)

## 今日洞察
$(tail -n 5 "$REPORT_FILE" | head -4)
EOF

echo "✅ 学习完成！"
echo ""
cat "$REPORT_FILE"
