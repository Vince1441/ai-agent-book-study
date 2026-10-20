# 实验 4-4：Execution Tools MCP

## 目标与环境

验证执行工具的 MCP 调用、文件边界、模型审批、终端执行、长输出持久化及模型摘要。

- Windows，项目 `.venv` Python 3.12，Git Bash。
- 教材服务：`chapter4/execution-tools/server.py`。
- 传输：真实 MCP stdio。
- 审批与摘要模型：Moonshot 官方接口 `kimi-k3`。
- `workspace/` 为本次工具工作目录。
- 运行日期：2026-10-20。

## 实际检查

| 检查 | 核验内容 |
|---|---|
| 文本写入 | 使用 `file_write` 创建 `notes.txt` |
| 文本编辑 | 使用 `file_edit` 修改内容，随后读取文件核验 |
| 覆盖审批 | 对已有实验文件请求真实模型审批，批准后核验覆盖内容 |
| 工作目录边界 | 请求写入工作目录外部，核验工具拒绝且外部文件未创建 |
| 终端计算 | 通过 `virtual_terminal` 执行已保存的 `calculate.py`，核验退出状态和结果 4000 |
| 长输出与摘要 | 真实生成 260 行输出，核验完整输出文件与模型生成的摘要 |

这些调用由实验脚本通过 MCP 发起。模型承担审批与摘要职责；本次没有验证自主规划与自动选择工具。

## 文件

本次六项检查均通过。完整输出为 260 行，计算结果为 4000，覆盖审批保存了一次真实模型调用记录。

- `run.log`：真实终端输出和 MCP 服务日志。
- `result.json`：各项 MCP 请求参数与实际工具返回。
- `verification.json`：独立文件检查、计算结果与输出哈希。
- `catalog.json`：MCP 服务实际返回的工具目录。
- `llm_receipts.json`：模型覆盖审批的请求、响应和 token 用量，不包含密钥。
- `full-output.txt`：完整的 260 行执行输出。
- `workspace/notes.txt`：文件操作的最终产物。
- `workspace/calculate.py`：通过终端执行的计算脚本。
- `run.py`：复现入口。
- `source/server.py`、`source/execution_tools.py`：本次 MCP 服务入口和终端实现快照；其余模块来自指定的教材源码。

长输出工具先截断并保存全文，再对仍超过阈值的返回内容生成摘要。教材摘要函数仅读取传入内容的前 5000 个字符，摘要没有覆盖完整输出；需要完整记录时读取 `full-output.txt`。

## 复现

将本目录放在教材源码的 `learning-results/task3/execution-tools`，在本机配置有效 Moonshot Key，按实际 Git 安装位置指定 `--bash-dir`：

```bash
cd /d/AI/ai-agent-book
source .venv/Scripts/activate
python -u learning-results/task3/execution-tools/run.py \
  --source-root /d/AI/ai-agent-book --bash-dir /d/Git/bin \
  2>&1 | tee learning-results/task3/execution-tools/run.log
```

脚本读取实验 `.env`，也可复用 `chapter2/kv-cache/.env` 或 `chapter1/context/.env` 中有效的 Moonshot Key。凭据仅在进程中设置，不包含在提交中。临时产物保存在本目录已忽略的 `.intermediate/`。

终端子进程使用空标准输入，不继承 MCP 协议输入流。工具的模型审批、代码校验和长输出摘要配置均保持启用。

依赖包括 `mcp>=1,<2`（本次 1.30.0）、`openai`、`python-dotenv`、`psutil` 及服务导入的 Google API、PyGithub 等包。

## 范围

这是本地执行与模型审批、摘要的试运行。没有调用 `code_interpreter`，没有验证 Docker 隔离、多语言执行、浏览器或桌面/移动端工具，也没有创建日历事件或通过工具创建 GitHub PR。完整正文协议的全部项目未在此次执行。
