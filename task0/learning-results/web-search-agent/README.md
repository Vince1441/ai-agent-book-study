# Kimi 网络搜索实验

## 目的与环境

使用 Moonshot `kimi-k3` 查询 Context Caching 的作用和官方资料来源。使用项目 `.venv` Python 环境及该实验的依赖。

## 运行命令

从仓库根目录进入实验目录；在本机 `.env` 中配置 Moonshot API Key。

```bash
source .venv/Scripts/activate
cd chapter1/web-search-agent
python -u main.py '请搜索 Moonshot 官方资料，解释 Context Caching 的作用，并提供来源链接。' \
  --provider kimi --max-steps 5 \
  --output ../../learning-results/web-search-agent/result.json \
  2>&1 | tee ../../learning-results/web-search-agent/run.log
```

## 文件与结果

- `result.json`：复制自已完成的 `chapter1/web-search-agent/search-live.json`，保留回答、行动轨迹和 API 记录。
- `run.log`：从该 JSON 提取的结果摘要，包含完整回答与行动轨迹；原始终端输出没有保存。

运行产出了回答及来源链接。回答中的具体事实仍需结合来源核对。

## Agent 分析

- LLM：Kimi 理解问题并组织回答。
- Context：用户问题、检索返回内容和交互历史。
- Tools：Moonshot 网络搜索工具。
