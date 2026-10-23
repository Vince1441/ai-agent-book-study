# Moonshot Coding Agent

独立目录，使用 Moonshot 官方 OpenAI 兼容接口。默认模型 `kimi-k3`，支持流式正文、工具调用以及多轮消息中的 `reasoning_content` 保留与回传。

## 配置

在本目录复制 `.env.example` 为 `.env`，填写有效的 Moonshot Key：

```dotenv
PROVIDER=moonshot
MOONSHOT_API_KEY=你的Moonshot密钥
MOONSHOT_BASE_URL=https://api.moonshot.cn/v1
DEFAULT_MODEL=kimi-k3
MAX_ITERATIONS=20
MAX_TOKENS=8192
```

也支持 `KIMI_API_KEY` 和 `PROVIDER=kimi`。进程环境变量优先于本目录 `.env`。缺少 Moonshot Key 时直接报错。

## 运行

在 Git Bash 中执行：

```bash
cd /d/AI/ai-agent-book
source .venv/Scripts/activate
cd chapter5/coding-agent-moonshot
test -f .env || cp .env.example .env
python main.py --list-tools
python main.py --provider moonshot --model kimi-k3 \
  --prompt '读取 README.md，简要说明配置方法。只读取文件。' \
  --max-iterations 6 --no-color
```

启动前填写 `.env` 中的密钥。依赖见 `requirements.txt`。Moonshot 请求使用温度 1，并使用 `MAX_TOKENS` 控制输出预算。

工作目录决定工具读写目标。可在 `.env` 中通过 `WORKING_DIRECTORY` 指定，留空则使用启动时的当前目录。工具权限和文件检查沿用教材实现，本目录没有新增系统级隔离。
