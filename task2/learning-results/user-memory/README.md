# 用户记忆：跨会话召回

## 目的与输入

验证教材的会话 Agent 与记忆处理器能将用户信息保存到磁盘，并在新会话中使用。输入为本次学习已使用的项目名称、项目路径、Windows、Git Bash 和 `.venv` 环境信息。

调用教材 `ConversationalAgent`、`BackgroundMemoryProcessor`，使用 `notes` 记忆模式和真实 Moonshot `kimi-k3`。

## 流程

1. 创建独立用户和空记忆目录。
2. 发送学习环境信息，获得真实模型回复。
3. 调用记忆处理器，由模型实际执行 `add_memory`。
4. 开始新会话并询问学习项目和环境。

## 结果

实际新增三条记忆：学习项目与路径、Windows 与 Git Bash、项目 `.venv`。新会话回答召回了这些信息。

- `result.json`：输入、初次回复、记忆操作、保存的记忆和新会话回复。
- `run.log`：完整真实终端输出，包含模型请求和实际工具操作。
- `storage/memories/`：实际保存的记忆文件。
- `storage/conversations/`：实际会话记录。

这是一个用户、一次记忆写入与一次新会话召回的功能验证，未测试长期冲突更新和多用户隔离。

## 运行

从教材源码根目录执行 `python -u learning-results/task2/run_experiments.py user-memory`。依赖与密钥读取方式见[总说明](../README.md)。
