# Task1 实验结果

| 实验 | 实际执行范围 | 文件目录 |
|---|---|---|
| KV Cache | 同一任务的六种上下文模式比较 | [kv-cache](kv-cache/README.md) |
| 系统提示 | 真实文件读取、TODO 管理与状态提示 | [system-hint](system-hint/README.md) |
| 上下文压缩 | 真实本地文本经 Moonshot 生成历史摘要 | [context-compression](context-compression/README.md) |

运行日期：2026-10-14。模型：Moonshot `kimi-k3`。

各目录包含实验说明、真实终端日志和结果 JSON。上下文压缩目录还包含输入文本和复现脚本。

上下文压缩未执行联网研究流程，仍需配置真实 Serper Key。各实验结果的范围与限制在对应 README 中说明。密钥和 `.env` 不包含在提交中。
