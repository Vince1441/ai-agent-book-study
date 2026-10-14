# 实验 2-9：系统状态提示

## 任务与环境

Moonshot `kimi-k3`，Python 3.12 项目虚拟环境。让 Agent 建立 TODO，读取真实 `config.py`，找出默认启用的五项状态提示功能，并更新任务状态。

## 运行命令

在教材源码仓库执行；本机 `chapter2/system-hint/.env` 需要配置有效的 `KIMI_API_KEY` 或 `MOONSHOT_API_KEY`，不要保留会优先选中的示例密钥。

```bash
source .venv/Scripts/activate
cd chapter2/system-hint
python -u main.py --mode single --provider kimi --model kimi-k3 \
  --task '建立一个TODO列表，读取当前目录的 config.py，列出默认启用的五项状态提示功能，完成后更新TODO并简短回答。只读取文件，不修改任何文件。' \
  --output ../../learning-results/task1/system-hint/result.json \
  2>&1 | tee ../../learning-results/task1/system-hint/run.log
```

本次执行在进程中复用了 `chapter2/kv-cache/.env` 的有效 Moonshot Key，同时设置两个密钥变量以避免示例值覆盖；密钥未写入提交文件。

## 结果

共 5 轮交互、5 次工具调用。Agent 完成文件读取和 TODO 更新，三个 TODO 项目全部为 `completed`。识别出的五项功能为时间戳、工具计数器、TODO 列表、详细错误和系统状态。

- `run.log`：真实完整终端输出。
- `result.json`：真实对话轨迹、工具结果、TODO 状态与运行配置。

这是单个任务的功能验证，未执行启用与关闭提示的统计对照。
