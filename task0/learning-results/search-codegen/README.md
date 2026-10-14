# 网络搜索与代码计算实验

## 目的与环境

搜索澳大利亚和新西兰的首都坐标，使用代码解释器计算距离，并提供来源。使用项目 `.venv` Python 环境、百炼 `qwen3.7-plus` 和 Responses API。

## 运行命令

在本机 `chapter1/search-codegen/.env` 配置百炼密钥和对应地域接口。

```bash
source .venv/Scripts/activate
cd chapter1/search-codegen
python -u main.py --backend dashscope --mode single \
  --request '搜索澳大利亚与新西兰的首都坐标，用Python计算距离，附来源。' \
  --output ../../learning-results/search-codegen/result.json \
  2>&1 | tee ../../learning-results/search-codegen/run.log
```

## 文件与结果

- `result.json`：复制自已完成的 `chapter1/search-codegen/search-codegen-result.json`。
- `run.log`：从结果 JSON 提取的结果摘要；原始终端输出没有保存。

结果中的 `success` 为 `true`，`status` 为 `completed`，`web_search_call` 和 `code_interpreter_call` 均已完成。具体计算过程、回答与来源保存在结果文件中。

## Agent 分析

- LLM：千问理解任务并选择工具。
- Context：用户请求、查询内容及代码计算结果。
- Tools：服务端网络搜索与代码解释器。
