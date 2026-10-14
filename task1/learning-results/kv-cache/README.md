# 实验 2-3：KV Cache 六种上下文模式

## 环境与任务

Moonshot 官方接口、`kimi-k3`、Python 3.12。六种模式使用同一任务：读取真实 `main.py` 并说明文件作用。运行范围限定在 `chapter2/kv-cache`，密钥通过本机 `.env` 读取。

## 复现命令

在教材源码仓库执行，确保已创建输出目录并在实验 `.env` 中配置真实 Moonshot Key：

```bash
source .venv/Scripts/activate
cd chapter2/kv-cache
python -u main.py --compare --model kimi-k3 --root-dir . \
  --task '读取 main.py，说明此文件的作用。必须实际调用文件工具，最后简短回答。' \
  --output ../../learning-results/task1/kv-cache/result.json \
  2>&1 | tee ../../learning-results/task1/kv-cache/run.log
```

## 文件

- `run.log`：完整真实终端输出。
- `result.json`：六种模式的完成状态、工具调用数量和缓存指标。回答与工具执行过程记录在 `run.log` 中。

模式包括 `correct`、`dynamic_system`、`shuffled_tools`、`dynamic_profile`、`sliding_window`、`text_format`。

本次六种模式均记录为完成。

| 模式 | 交互轮数 | 输入 token 总数 | 缓存 token 总数 |
|---|---:|---:|---:|
| correct | 5 | 21787 | 12800 |
| dynamic_system | 6 | 32607 | 3072 |
| shuffled_tools | 5 | 22782 | 512 |
| dynamic_profile | 5 | 22628 | 2560 |
| sliding_window | 5 | 23078 | 6144 |
| text_format | 19 | 247334 | 222464 |

`text_format` 出现重复读取行为，累计输入明显增加。缓存 token 数量高时也需要结合任务轮数和总输入分析，不能直接视为任务效率高。

## 分析方法

查看各模式的 `metrics`：输入 token、缓存 token、总耗时、每轮 TTFT；同时检查任务完成状态和重复工具调用。

本次顺序执行每种模式各一次，未实施多次重复采样或服务端缓存清空；模式间的调用轮数也可能不同。结果用于观察上下文构造与缓存记录，不能据此得出稳定的速度排名。

程序的 TTFT 是客户端记录的测量值。日志中的固定说明是教学文字，具体结论需要以实际 `result.json` 为依据。
