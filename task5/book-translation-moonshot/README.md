# Moonshot 书籍翻译实验

## 运行环境与任务

2026-10-27，在 Windows 项目 `.venv` 中使用 Moonshot `kimi-k3`。输入为教材内置 `sample_book/` 四个英文 Markdown 章节，目标语言为中文。

执行术语提取、四章独立上下文翻译、全书审校、Manager 修订决策，以及单 Agent 连续翻译对照。使用真实 API，进程凭据来自实验目录的 `.env`。

## 本次结果

| 指标 | 多 Agent 管理者模式 | 单 Agent |
| --- | --- | --- |
| 主 / Manager 上下文峰值 | 1259 token | 2126 token |
| 全流程总用量 | 11385 token | 6116 token |
| 术语内部一致率 | 89% | 78% |
| 指定术语遵从率 | 100% | 36% |

以上数据来自本次真实运行日志。Manager 状态峰值与单 Agent 请求峰值使用不同统计来源，需要结合下方统计口径理解。

## 产物

| 文件 | 内容 |
| --- | --- |
| `run.log` | 本次控制台原始日志，包含协作过程、用量和统计表 |
| `result.json` | 完成状态、模型、运行时间及产物 SHA-256 |
| `translation/orchestration/` | 术语表、四章译文和审校报告 |
| `translation/single_agent/` | 四章对照译文及进度记录 |
| `source/` | 本次源代码、配置模板、样例书和依赖列表 |

Manager 状态的 token 统计使用 `tiktoken` 估算，API 调用用量使用返回的 usage。译文质量和术语遵从程度请结合实际译文、审校报告及日志查看；进程完成不能证明全部翻译内容准确。

## 复现

激活 Python 环境，进入 `source/`，安装 `requirements.txt` 中的依赖，将 `env.example` 复制为 `.env`，填写自己的 `MOONSHOT_API_KEY`。

```bash
python demo.py --out-dir ../translation
```

配置模板默认使用 `MOONSHOT_MODEL=kimi-k3` 和 `MOONSHOT_BASE_URL=https://api.moonshot.cn/v1`。本实验无需 Tavily。密钥文件不包含在上传内容中。
