---
name: claude-code
version: 1.0.0
description: 在OpenClaw中调用Claude Code执行编码任务 - 通过CLI实现代码审查、bug修复、功能开发等
author: OpenClaw
---

# Claude Code 集成技能

本技能允许 OpenClaw 通过 `claude` CLI 调用 Claude Code 执行编码任务。

## 前置要求

1. **安装 Claude Code**: 
   - Windows: `irm https://claude.ai/install.ps1 | iex`
   - macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`

2. **登录认证**: 首次使用需运行 `claude auth login`

3. **确保 claude 命令可用**: 在终端中验证 `claude --version`

---

## 核心功能

### 1. 快速代码审查 (Review Code)

审查指定文件或整个代码库:

```
claude -p "审查 src/auth.ts 文件的代码质量和安全性"
```

### 2. Bug 修复 (Fix Bug)

描述 bug 症状，让 Claude Code 定位并修复:

```
claude -p "修复登录页面点击按钮无反应的bug，检查auth.ts和相关组件"
```

### 3. 功能开发 (Build Feature)

描述想要实现的功能:

```
claude -p "在用户管理模块添加忘记密码功能，包括邮件重置链接"
```

### 4. 编写测试 (Write Tests)

为指定模块编写测试用例:

```
claude -p "为 auth module 编写单元测试，覆盖登录、登出、token验证"
```

### 5. 代码重构 (Refactor)

重构现有代码:

```
claude -p "将 auth.ts 重构为使用class形式，增加错误处理"
```

### 6. 解释代码 (Explain)

解释特定代码段:

```
claude -p "解释 src/utils/parser.ts 中 parseJSON 函数的工作原理"
```

### 7. 探索代码库 (Explore)

了解项目结构:

```
claude -p "探索这个项目的架构，找出主要模块和依赖关系"
```

---

## 使用方法

### 通过 exec 工具调用

使用 OpenClaw 的 `exec` 工具执行 Claude Code CLI 命令:

```bash
# 基本用法 - 打印模式 (-p) 执行单次查询
claude -p "your task description"

# 指定模型
claude -p --model opus "your task"

# 限制执行轮次
claude -p --max-turns 5 "your task"

# 指定工作目录
claude -p --add-dir /path/to/project "your task"

# 输出JSON格式
claude -p --output-format json "your task"

# 继续上一次会话
claude -c -p "continue the task"

# 恢复指定会话
claude -r session-name "your task"
```

---

## 常用命令速查

| 场景 | 命令 |
|------|------|
| 快速审查 | `claude -p "review file:路径"` |
| 修复bug | `claude -p "fix bug: 描述症状"` |
| 写测试 | `claude -p "write tests for 文件"` |
| 解释代码 | `claude -p "explain 文件"` |
| 重构 | `claude -p "refactor 文件"` |
| 探索项目 | `claude -p "explore 项目结构"` |

---

## 注意事项

1. **认证状态**: 首次使用需运行 `claude auth login` 登录 Anthropic 账号
2. **权限模式**: 可用 `--permission-mode plan` 预览操作而不执行
3. **会话管理**: 使用 `-c` 继续会话，`-r` 恢复指定会话
4. **输出格式**: 生产环境建议用 `--output-format json` 便于解析

---

## 示例工作流

```
用户: 帮我审查 C:\project\src\auth\login.ts

执行:
claude -p --add-dir C:\project "审查 src/auth/login.ts 的代码质量和安全漏洞"

Claude Code 响应:
- 代码审查结果
- 发现的问题
- 改进建议
```

---

## 自动 Push 到 GitHub

完成编码任务后，自动将变更推送到 GitHub 仓库。

### 仓库配置

- **仓库 URL**: https://github.com/Tugiu123/openclaw-skills
- **本地路径**: C:\Users\Aaron\.agents\skills\claude-code
- **分支**: main

### 自动 Push 流程

每次完成编码任务后，执行以下步骤:

1. **检查变更**: `git status`
2. **添加文件**: `git add -A`
3. **提交**: `git commit -m "描述变更内容"`
4. **推送**: `git push origin main`

### 手动 Push 命令

```bash
# 提交所有变更
git add -A
git commit -m "Your commit message"
git push origin main

# 或者使用简写
git add -A && git commit -m "Update" && git push
```

### 在 OpenClaw 中执行

```bash
# 克隆仓库到本地
git clone https://github.com/Tugiu123/openclaw-skills.git C:\Users\Aaron\openclaw-skills

# 在工作目录中执行 Claude Code 任务后 push
cd C:\Users\Aaron\openclaw-skills
claude -p --add-dir C:\Users\Aaron\openclaw-skills "你的任务"
git add -A
git commit -m "完成任务描述"
git push origin main
```
