# MEMORY.md - 长期记忆

## 服务管理偏好

- **语音服务**: 不使用，已删除 voice_wakeup 和 voice_keyboard
- **长期记忆**: 保留并使用，用于学习用户偏好

## 系统配置

- **时区**: Asia/Shanghai
- **语言偏好**: zh-CN
- **工作时间**: 09:00 - 22:00

## 重要发现

- launchd 服务在某些情况下会加载失败 (Input/output error)
- 备用方案: 使用 nohup 直接后台启动 Python 进程
- self_healing_v2 使用 memory.pid 文件检测 longterm_memory

## 学习到的用户偏好

- 简洁直接的沟通风格
- 不需要语音功能
- 注重系统稳定性和故障修复
- **交易策略查询规则（待确认）**: MEMORY.md 记录要求回复交易策略详情，但实际检查发现系统中**没有交易监控脚本或 FinLab CLI**。此规则可能来自用户期望而非当前状态。需要与用户确认是否需要搭建交易监控体系。

## 新发现 (2026-02-16)

### 交易系统状态
- **当前状态**: 无交易系统
- **检查结果**:
  - 工作区中没有交易相关脚本
  - 未安装 FinLab CLI
  - 没有找到回测/量化交易文件
- **待确认**: 用户是否需要帮助搭建交易监控体系

## 系统能力扩展 (2026-02-15)

### 新增知识库系统
- **LangChain 知识库**: 支持 memory/*.md 向量化存储和语义搜索
- **轻量级知识库**: simple_knowledge_base.py，简化部署
- **知识库导入器**: knowledge_importer.py，一键导入记忆

### 新增多Agent系统
- **AutoGen 多Agent框架**: multi_agent_system.py
- **架构设计**: 5个Agent角色（Researcher/Analyst/Coder/Coordinator/Chief）
- **任务流转**: 创建→分配→执行→完成的完整工作流

### 自动化变更
- **停止**: self_healing_v2.py distill 自动蒸馏
- **改为**: 手动导入到知识库
- **命令**: python3 ~/.openclaw/services/simple_knowledge_base.py --import

### 技术债务
- **依赖兼容性问题**: langchain v1.x vs v2.x, pydantic v1 vs v2
- **解决方案**: 使用 try/except 进行版本兼容导入
