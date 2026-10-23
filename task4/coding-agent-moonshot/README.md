# Coding Agent：Moonshot 实验记录

## 实验环境

- 运行日期：2026-10-23，Windows，项目 `.venv` Python 环境。
- 模型：`kimi-k3`；供应商：Moonshot；接口：`https://api.moonshot.cn/v1`。
- 使用新目录 `chapter5/coding-agent-moonshot`，保留教材原目录。
- 依赖列表见 `source/requirements.txt`。密钥从本地 `.env` 读取，上传文件不包含密钥。

## 实验任务

先调用 Read 读取 README.md，再调用 Read 读取 config.py，核对默认模型名称和密钥变量名称，最后用中文简短回答。只读取这两个文件，不读取 `.env`，不修改文件。

## 实际结果

- 真实 Moonshot API 调用完成，验证进程退出码为 0。
- 成功执行两次 Read，分别读取 README.md 和 config.py。
- 最终回答确认默认模型为 `kimi-k3`，密钥变量为 `MOONSHOT_API_KEY`，兼容 `KIMI_API_KEY`。
- 获得两条包含 `reasoning_content` 的助手消息，转换后的请求消息完整保留这些内容。
- 检查未出现工具错误、API 错误或达到最大迭代次数的事件。

本次验证覆盖文件读取、多轮工具调用和推理内容传递。文件写入、Shell 命令、网络检索等工具没有在此次实验中执行。

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `run.log` | 实际执行日志，包含工具调用、读取结果和最终回答 |
| `result.json` | 结构化结果，包含模型名称、工具次数、事件和消息记录 |
| `source/` | 本次使用的代码、工具、配置模板与验证脚本 |

## 复现方法

在 Git Bash 中进入下载后的实验目录，使用已经创建的 Python 虚拟环境：

```bash
cd source
python -m pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env`，填写 `MOONSHOT_API_KEY`，保存后运行：

```bash
python -X utf8 -u verify_live.py --env-file .env
```

验证成功后生成 `source/validation/live-result.json`。脚本会设置 Moonshot、`kimi-k3` 和代码所在工作目录，执行本文所述的两次读取任务。

通过教材命令入口运行单个任务：

```bash
python main.py --provider moonshot --model kimi-k3 \
  -p '读取 README.md，简要说明配置方法。只读取文件。' \
  --max-iterations 6 --no-color
```

结果中的绝对路径和时间戳来自本次实际运行环境，复现时随本机目录与运行时间变化。
