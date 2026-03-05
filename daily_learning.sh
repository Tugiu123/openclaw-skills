#!/bin/bash
# Daily Learning Report Generator
# Runs at 8:00 AM daily

DATE=$(date +"%Y-%m-%d %H:%M")
REPORT_FILE=~/.openclaw/workspace/daily_learning_report.md

echo "# 📚 每日学习报告 - $DATE" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1. ClawHub Skills 学习
echo "## 🦞 ClawHub 技能市场" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "### 搜索热门技能..." >> "$REPORT_FILE"
CLAWHUB_SKILLS=$(curl -s "https://clawhub.com/api/skills/popular" 2>/dev/null | head -c 2000 || echo "无法连接 ClawHub")
echo "$CLAWHUB_SKILLS" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 2. GitHub 学习
echo "## 🐙 OpenClaw GitHub 更新" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "### 最新 Release" >> "$REPORT_FILE"
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null | grep -E '"tag_name"|"name"|"body"' | head -6 || echo "无法获取 Release")
echo "$LATEST_RELEASE" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "### 最近 Commits" >> "$REPORT_FILE"
RECENT_COMMITS=$(curl -s "https://api.github.com/repos/openclaw/openclaw/commits?per_page=5" 2>/dev/null | grep -E '"message"|"author"' | head -20 || echo "无法获取 Commits")
echo "$RECENT_COMMITS" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "### 新增 Issues" >> "$REPORT_FILE"
OPEN_ISSUES=$(curl -s "https://api.github.com/repos/openclaw/openclaw/issues?state=open&per_page=3" 2>/dev/null | grep -E '"title"|"number"' | head -10 || echo "无法获取 Issues")
echo "$OPEN_ISSUES" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 3. 技能更新统计
echo "## 📊 技能统计" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

INSTALLED_SKILLS=$(ls -la ~/.openclaw/workspace/skills/ 2>/dev/null | wc -l || echo 0)
echo "- 已安装技能数: $INSTALLED_SKILLS" >> "$REPORT_FILE"

# 4. 今日学习总结
echo "## 💡 今日学习总结" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "- [待补充] 本日学到的关键知识点" >> "$REPORT_FILE"
echo "- [待补充] 值得尝试的新功能" >> "$REPORT_FILE"
echo "- [待补充] 可改进现有工作流的方式" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "---" >> "$REPORT_FILE"
echo "*报告生成时间: $(date)*" >> "$REPORT_FILE"

# 输出到控制台
cat "$REPORT_FILE"

# 发送通知
echo "✅ 学习报告已生成: $REPORT_FILE"
