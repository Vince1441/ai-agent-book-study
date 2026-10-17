# 上下文前缀生成

## 输入与方法

输入为真实教材 `chapter3/README.md`，原文保存于 `input.md`。使用教材 `ContextualChunker` 将文档分块，每个块携带全文信息，由 Moonshot `kimi-k3` 生成一段定位该块含义的上下文，再将前缀与原始块拼接。

## 配置

- 分块目标：1000 字符，重叠 100 字符。
- 最小分块：100 字符。
- 模型：`kimi-k3`，温度 1。
- 推理模型输出预算：4096 token，包含内部推理和最终前缀。

`source/contextual_chunking.py` 保存本次使用的教材模块，`run_experiments.py` 在本实验中优先导入该快照；其他配置与依赖来自指定的教材源码。

## 验证与范围

脚本要求每个分块都得到非空模型前缀，并核验 `contextualized_text = context + 原始文本`，完整保存输入、前缀、原始块和拼接结果。

本次仅验证真实前缀生成，没有构建向量索引、启动检索服务，也没有验证检索提升比例。`context_tokens` 是教材实现的粗略词数估算，不能当作模型精确 token 用量。

- `result.json`：分块、前缀、拼接文本与统计。
- `run.log`：真实 API 请求和前缀生成日志。
- `input.md`：完整输入文档。

## 运行

从教材源码根目录执行 `python -u learning-results/task2/run_experiments.py contextual-retrieval`。依赖与密钥读取方式见[总说明](../README.md)。
