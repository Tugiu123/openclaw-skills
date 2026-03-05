---
name: claude-code
description: Delegate coding tasks to Claude Code CLI for code generation, refactoring, code review, bug fixes, and test writing. Use when: (1) needing Claude Code's coding capabilities, (2) complex code generation tasks, (3) code review, (4) multi-file refactoring. Requires Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code` or `brew install --cask claude-code`).
metadata: { "openclaw": { "emoji": "🧑‍💻", "requires": { "bins": ["claude"] } } }
---

# Claude Code Skill

Delegate coding tasks to Claude Code CLI for advanced code generation, refactoring, and analysis.

## When to Use

✅ **USE this skill when:**
- Complex code generation across multiple files
- Code review and security auditing
- Bug fixing with root cause analysis
- Writing tests (unit, integration, e2e)
- Refactoring large codebases
- Explaining complex codebases
- Creating commits and PRs

❌ **DO NOT use when:**
- Simple one-liner fixes (just use edit tool)
- Reading files (use read tool)
- Non-coding tasks
- Quick questions about code

## Core Commands

### 1. Interactive Session
```bash
cd /path/to/project
claude
```

### 2. One-shot Query (non-interactive)
```bash
claude -p "write tests for auth module"
```

### 3. Continue Last Session
```bash
claude -c
```

### 4. Resume Specific Session
```bash
claude -r "session-name" "finish the PR"
```

### 5. Pipe Content for Analysis
```bash
cat error.log | claude -p "analyze these errors"
```

## Integration with OpenClaw

### Running Claude Code Tasks

```bash
# Basic coding task
claude -p "explain this function" --path /workspace/project

# Write tests
claude -p "write unit tests for user service" --path /workspace/project

# Code review
git diff main | claude -p "review these changes for security issues"

# Fix bug
claude -p "find and fix the memory leak in server.js" --path /workspace/project
```

### Claude Code Flags

| Flag | Description |
|------|-------------|
| `-p` | Prompt mode, exits after response |
| `-c` | Continue last session |
| `-r` | Resume specific session |
| `--path` | Working directory |
| `--model` | Model to use (e.g., claude-3-5-sonnet-20241022) |
| `--add-dir` | Additional directories to access |
| `--append-system-prompt` | Add custom instructions |

## Best Practices

1. **Be Specific**: Clear prompts get better results
2. **Provide Context**: Include relevant files or error messages
3. **Use Sessions**: For multi-step tasks, use `-c` or `-r`
4. **Review Output**: Always review Claude Code's changes

## Examples

### Code Review
```bash
claude -p "review this PR for security vulnerabilities" --path /workspace
```

### Write Tests
```bash
claude -p "write comprehensive tests for the payment module" --path /workspace
```

### Bug Fix
```bash
claude -p "debug this error: Cannot read property 'id' of undefined" --path /workspace
```

### Explain Code
```bash
claude -p "explain how the authentication flow works in this codebase" --path /workspace
```

## MCP Integration

Claude Code supports MCP servers. Configure in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

## Notes

- Claude Code requires authentication (Anthropic account)
- Use `--permission-mode plan` for dry-run
- Check auth status: `claude auth status`
