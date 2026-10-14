# 实验 2-10：本地文本的历史摘要压缩

## 范围

本次直接调用教材 `ContextCompressor.compress_for_history`，由 Moonshot `kimi-k3` 对真实本地文件生成摘要。输入为 `chapter2/system-hint/config.py`，完整输入保存在 `input.txt`。

这次验证历史摘要压缩方法。没有执行 Serper 搜索、多策略联网研究或窗口溢出流程；这些完整实验仍需要真实 `SERPER_API_KEY`。

## 复现

需要教材源码和相应 Python 依赖。将本目录放在教材的 `learning-results/task1/context-compression` 中，使用本机 `chapter2/kv-cache/.env` 的有效 Moonshot Key：

```bash
source .venv/Scripts/activate
python -u learning-results/task1/context-compression/run.py \
  --source-root /d/AI/ai-agent-book \
  2>&1 | tee learning-results/task1/context-compression/run.log
```

脚本复用教材压缩实现，要求模型返回非空摘要，拒绝将截断结果当作成功摘要。脚本读取密钥后仅在进程中配置，不输出密钥。

## 结果

- 原始文本：4377 个字符。
- 摘要：1121 个字符，字符数减少约 74.4%。
- `cl100k_base` 估算 token：956 → 519，减少约 45.7%。这些是估算值，不能当作 Moonshot 计费 token。
- 模型调用返回 HTTP 200。

`result.json` 保存完整摘要与指标，`run.log` 保存真实终端输出，`input.txt` 保存真实输入，`run.py` 为复现脚本。摘要保留了五项功能、默认开关和配置读取方式；未进行独立模型评分。
