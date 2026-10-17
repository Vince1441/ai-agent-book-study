# Task2：用户记忆与知识检索试运行

运行日期：2026-10-18。Python：项目 `.venv` 的 Python 3.12。模型服务：Moonshot 官方接口；模型：`kimi-k3`。

| 实验 | 实际运行范围 | 记录 |
|---|---|---|
| 用户记忆 | 输入学习环境、模型提取记忆、新会话召回 | [user-memory](user-memory/README.md) |
| 记忆评估 | 内置 layer1 用例，模型回答后由模型评委评分 | [user-memory-evaluation](user-memory-evaluation/README.md) |
| Agentic RAG | 本地法律 BM25 检索，比较智能体多轮检索与单次检索 | [agentic-rag](agentic-rag/README.md) |
| 上下文前缀 | 真实教材文档分块，每块由模型生成上下文前缀 | [contextual-retrieval](contextual-retrieval/README.md) |

各实验目录中的 `run.log` 为实际终端输出，`result.json` 为真实结果。此次是有限范围的功能试运行，没有完成全量基准、神经向量索引或检索指标评估。

## 复现

需要教材源码仓库及 Python 依赖。将此目录放在教材源码的 `learning-results/task2` 中，配置有效 Moonshot Key 后运行：

```bash
cd /d/AI/ai-agent-book
source .venv/Scripts/activate
python -u learning-results/task2/run_experiments.py user-memory \
  2>&1 | tee learning-results/task2/user-memory/run.log
```

将最后的实验名称替换为 `user-memory-evaluation`、`agentic-rag` 或 `contextual-retrieval`，分别运行其余三项。也可以使用 `--source-root` 指定教材源码根目录。

脚本依次在当前实验 `.env`、`chapter2/kv-cache/.env`、`chapter1/context/.env` 中选择有效 Moonshot Key；本次复用了此前实验的有效密钥。密钥仅在进程中设置，`.env` 不包含在本目录。

前缀生成使用本目录保存的教材模块快照，推理模型输出预算为 4096 token。`context_tokens` 是原实现的粗略词数估算，不可作为 API 计费依据。
