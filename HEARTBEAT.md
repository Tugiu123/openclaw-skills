# HEARTBEAT.md - 定期检查清单

## 自我进化系统检查 (每5分钟)

### 检查清单
1. ✅ 检查所有服务状态
2. ✅ 检测是否有阻塞 (>2min)
3. ✅ 记录错误模式
4. ✅ 统计任务成功率
5. ✅ 输出健康报告 (每6小时)

### 命令
```bash
python3 ~/.openclaw/services/self_healing_v2.py check   # 健康检查
python3 ~/.openclaw/services/self_healing_v2.py report  # 完整报告
python3 ~/.openclaw/services/self_healing_v2.py evolve  # 手动进化
```

## 长期记忆蒸馏 (已禁用，改用知识库)

### 旧方案 (已停止)
❌ 不再使用 self_healing_v2.py distill

### 新方案: 使用知识库存储
✅ 使用 LangChain 知识库存储学习成果

**命令：**
```bash
# 手动导入记忆到知识库
python3 ~/.openclaw/services/knowledge_importer.py

# 或使用轻量版
python3 ~/.openclaw/services/simple_knowledge_base.py --import
```

**工作流程：**
1. 每日学习 → 存储到 memory/YYYY-MM-DD.md
2. 定期运行知识库导入脚本
3. 自动向量化并存储到 knowledge_base/
4. 后续查询直接从知识库检索

### 基于 Leontius 的学习循环 (已更新)
1. **Capture**: 收集原始错误数据 → 存储到 memory/*.md
2. **Distill**: 提炼为最佳实践 → 导入知识库
3. **Try**: 小规模测试优化方案
4. **Recruit**: 借鉴其他 agent 的经验

## 阻塞处理流程

### 当检测到阻塞时
1. 记录阻塞类型
2. 应用修复策略:
   - 发送 SIGHUP 刷新配置
   - 重启进程
   - 指数退避重试
3. 记录修复结果
4. 更新错误模式库

### 预防措施
- 定期检查 CPU/内存占用
- 监控日志更新频率
- 自动优化超时配置

---
*基于 Moltbook 最佳实践 v2.0*
