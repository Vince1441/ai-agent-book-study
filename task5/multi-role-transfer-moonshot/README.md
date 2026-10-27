# Moonshot 多角色转换实验

## 环境与任务

2026-10-27，Windows，项目 `.venv` Python 环境。模型为 Moonshot `kimi-k3`，联网检索使用 Tavily。分别从实验目录 `.env` 读取密钥，上传文件不包含密钥。

本次执行两个真实任务：

1. 角色移交：检索中国 2021—2023 年新能源汽车销量，调用计算工具计算复合增长率，再形成不超过 120 字的投资人摘要。
2. 成对比较：使用同一计算任务，分别运行角色移交和按需加载 Skill，要求调用 calculate 计算 `(125+375)*8`，最终回答 4000。两条路径各运行一次，没有运行边界用例集。

## 本次结果

- 检索任务运行 10 轮，移交顺序为 `triage → research → data_analysis → writing → triage`。
- 真实 Tavily 检索、计算、字符统计等 9 项行为检查全部通过，结果状态为 `complete`。
- 最后一次字符统计得到 109 字的投资人摘要。
- 计算对比两条路径均通过：角色移交调用模型 3 次，Skill 路径调用模型 4 次。

## 产物与检查方式

| 文件 | 内容 |
| --- | --- |
| `run.log` | 两项任务的实际控制台日志 |
| `result.json` | 检索任务的完整消息、角色移交、工具活动、API usage 和行为检查 |
| `comparison.json` | 两条计算路径的消息、调用回执和任务检查结果 |
| `source/` | 本次运行代码、角色、Skill、配置模板、任务定义和依赖列表 |

检索任务是否完成全部要求，以 `result.json` 的 `status` 和 `acceptance_gates` 为准。来源 URL 和检索内容保存在工具消息中，可用于复核。

一次配对运行用于检查两条实现能否工作，不能据此得出哪条路径整体效果更好。检索服务的摘要仍需结合原始来源核对，尤其需要检查数值单位。

## 复现

激活 Python 环境，进入 `source/`，安装 `requirements.txt` 中的依赖，将 `env.example` 复制为 `.env` 并填写 `MOONSHOT_API_KEY` 和 `TAVILY_API_KEY`。

```bash
python demo.py --model kimi-k3 --max-steps 20 --output ../result.json
python run_comparison.py --task-file tasks.moonshot.json \
  --trials 1 --skip-boundary --max-steps 12 --output ../comparison.json
```

模型服务地址为 `https://api.moonshot.cn/v1`。角色移交会改变系统提示与可见工具，Skill 路径保持工具目录并逐步加载角色规程；两者均保留共享历史。
