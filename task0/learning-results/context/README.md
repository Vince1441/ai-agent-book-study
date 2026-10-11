# Context 实验：调用计算器

## 实验目的

观察 Agent 如何结合完整上下文调用计算器，再根据工具结果回答问题。

## 实验环境

- Windows，项目 Python 虚拟环境 `.venv`
- Python 3.12
- 模型服务：Moonshot / Kimi
- 模型：`kimi-k3`
- 上下文模式：`full`

API Key 保存在本机 `chapter1/context/.env`，不包含在本目录中。

## 运行命令

在 Git Bash 中，从仓库根目录执行：

```bash
source .venv/Scripts/activate
cd chapter1/context
python -u main.py --mode single --provider kimi --context-mode full \
  --task '请调用计算器计算 (125 + 375) * 8，并给出结果。' \
  --output ../../learning-results/context/result.json \
  2>&1 | tee ../../learning-results/context/run.log
```

## 文件说明

- `run.log`：本次实际运行的完整终端输出。
- `result.json`：程序直接生成的结构化结果，包含最终回答、工具调用及 API 交互记录。

## 结果检查

预期结果为 `4000`。同时检查 `result.json` 中的 `tool_calls`，确认计算器实际参与计算。`success` 表示程序记录的完成状态；`task_success` 如果为 `null`，表示该字段没有独立判定结果。

## LLM、Context、Tools

- LLM：Kimi 理解任务并决定调用计算器。
- Context：用户任务、工具说明、交互历史和计算器返回值。
- Tools：计算器执行表达式计算。
