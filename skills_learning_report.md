# 学习技能报告 - 2026-02-12

## 学习来源

1. **Skills.sh** - AI Agent技能目录
2. **SkillsMP.com** - 中文技能市场（访问受限）
3. **Awesome OpenClaw Skills** - 2,999+ 社区技能

---

## 从 Skills.sh 学到的技能

### Top 10 最热门技能

| 排名 | 技能 | 安装量 | 用途 |
|------|------|--------|------|
| 1 | find-skills | 195.2K | 查找安装AI技能 |
| 2 | vercel-react-best-practices | 122.5K | React最佳实践 |
| 3 | web-design-guidelines | 92.8K | Web设计指南 |
| 4 | remotion-best-practices | 84.4K | 视频生成 |
| 5 | frontend-design | 62.2K | 前端设计 |
| 6 | vercel-composition-patterns | 36.1K | 组合模式 |
| 7 | agent-browser | 31.4K | 浏览器自动化 |
| 8 | skill-creator | 30.8K | 创建技能 |
| 9 | browser-use | 28.1K | 浏览器使用 |
| 10 | react-native-skills | 26.1K | React Native |

### 实用技能分类

#### 🔧 开发工具
- **coding-agent** - 运行Codex CLI、Claude Code
- **mcp-builder** - 创建MCP服务器
- **test-runner** - 编写运行测试
- **docker-essentials** - Docker容器化
- **git-essentials** - Git版本控制

#### 📊 数据分析
- **context7** - 数据库查询
- **supabase-postgres** - PostgreSQL最佳实践
- **python-testing** - Python测试模式

#### 🎨 UI/UX
- **canvas-design** - 画布设计
- **tailwind-design-system** - Tailwind设计系统
- **shadcn-ui** - UI组件库

#### 🚀 部署运维
- **vercel/ai-sdk** - AI部署
- **turborepo** - Monorepo管理
- **github-actions** - CI/CD自动化

---

## 从 Awesome OpenClaw Skills 学到的技能

### Data & Analytics (46个)

| 技能 | 用途 |
|------|------|
| budget-variance-analyzer | 预算vs实际分析 |
| copilot-money | 个人财务数据查询 |
| openinsider | SEC内部交易数据 |
| financial-calculator | 高级财务计算器 |
| multi-factor-strategy | 多因子股票策略 |

### 可用于量化交易的技能

1. **multi-factor-strategy** - 多因子选股策略
   - 创建多因子股票交易策略
   - 可用于加密货币因子分析

2. **openinsider** - SEC内部交易数据
   - 获取内部人员交易信息
   - 可参考大户动向

3. **financial-calculator** - 财务计算器
   - 计算未来值、现值
   - 投资回报率计算

### Coding Agents & IDEs (133个)

| 技能 | 用途 |
|------|------|
| coding-agent | 运行各种编码代理 |
| coding-opencode | OpenCode集成 |
| cursor-agent | Cursor CLI代理 |
| multi-coding-agent | 多编码代理并行 |
| tdd-guide | 测试驱动开发 |

### DevOps & Cloud (212个)

- Docker/Kubernetes
- GitHub Actions
- 部署管道
- 云服务集成

---

## 本地模型调用测试

### 可用本地模型

1. **GLM-4.7** (OpenCode)
   - 位置: `ollama/glm-4.7:cloud`
   - 用途: 复杂推理、编码

2. **MiniMax-M2.1** (Minimax Portal)
   - 位置: `minimax-portal/MiniMax-M2.1`
   - 用途: 快速推理

3. **Kimi-K2.5** (Moonshot AI)
   - 位置: `ollama/kimi-k2.5:cloud`
   - 用途: 长文本处理

### 调用方式

```python
# 在OpenCode中使用GLM-4.7
model = "ollama/glm-4.7:cloud"

# 或使用会话覆盖
/session --model=ollama/glm-4.7:cloud
```

---

## 应用于交易系统的改进

### 1. 使用 TDD 开发策略模块
```python
# test_strategy.py
def test_mtf_strategy():
    assert win_rate > 0.6
    assert max_drawdown < 0.2
```

### 2. 使用 Docker 容器化交易系统
```dockerfile
FROM python:3.10
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "trader.py"]
```

### 3. 使用 MCP 集成外部数据
```json
{
  "mcpServers": {
    "coingecko": {
      "command": "python",
      "args": ["-m", "mcp_coingecko"]
    }
  }
}
```

---

## 技能安装命令

```bash
# 安装技能
npx skills add <owner/repo>

# 示例
npx skills add anthropics/skill-creator
npx skills add vercel-labs/agent-browser
npx skills add anthropics/frontend-design
```

---

## 总结

### 已学到的核心技能

1. ✅ **技能发现与安装** - find-skills
2. ✅ **创建技能** - skill-creator
3. ✅ **测试驱动开发** - tdd-guide
4. ✅ **多编码代理** - multi-coding-agent
5. ✅ **Docker容器化** - docker-essentials

### 待学习的技能

1. 🔄 **MCP服务器构建** - mcp-builder
2. 🔄 **GitHub Actions** - github-actions-templates
3. 🔄 **AI SDK集成** - vercel/ai-sdk
4. 🔄 **财务计算器** - financial-calculator

### 下一步

1. 创建一个新的OpenClaw技能
2. 使用GLM-4.7模型优化交易策略
3. 将交易系统容器化
4. 添加CI/CD自动化

---

*学习时间: 2026-02-12 17:25*
