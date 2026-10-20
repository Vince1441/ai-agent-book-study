import argparse
import asyncio
import hashlib
import json
import logging
import os
import shlex
import sys
from pathlib import Path

from dotenv import dotenv_values
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

parser = argparse.ArgumentParser()
parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[3])
parser.add_argument("--bash-dir", type=Path, default=Path("D:/Git/bin"))
args = parser.parse_args()
root = args.source_root.resolve()
output = Path(__file__).resolve().parent
source = root / "chapter4/execution-tools"
workspace = output / "workspace"
intermediate = output / ".intermediate"
intermediate.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

key = None
for path in [source / ".env", root / "chapter2/kv-cache/.env", root / "chapter1/context/.env"]:
    values = dotenv_values(path)
    for name in ["KIMI_API_KEY", "MOONSHOT_API_KEY"]:
        value = values.get(name)
        if value and not any(t in value.lower() for t in ["your", "example", "xxx", "你的"]):
            key = value
            break
    if key:
        break
assert key, "缺少有效 Moonshot Key"
assert (args.bash_dir / "bash.exe").is_file(), "需要指定 Git Bash 目录"
env = os.environ.copy()
env.update({"KIMI_API_KEY": key, "MOONSHOT_API_KEY": key, "PROVIDER": "kimi", "MODEL": "kimi-k3", "WORKSPACE_DIR": str(workspace), "MAX_TOKENS": "4096", "REQUIRE_APPROVAL_FOR_DANGEROUS_OPS": "true", "AUTO_VERIFY_CODE": "true", "AUTO_SUMMARIZE_COMPLEX_OUTPUT": "true", "EXECUTION_LLM_RECEIPT_PATH": str(output / "llm_receipts.json"), "TEMP": str(intermediate), "TMP": str(intermediate), "TMPDIR": str(intermediate)})
env["PATH"] = str(args.bash_dir) + os.pathsep + env.get("PATH", "")
env["PYTHONPATH"] = str(source) + os.pathsep + env.get("PYTHONPATH", "")


def save(name, data):
    (output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


async def main():
    save("llm_receipts.json", [])
    parameters = StdioServerParameters(command=sys.executable, args=[str(output / "source/server.py")], env=env, cwd=str(source))
    records = []
    async with stdio_client(parameters) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            catalog = await session.list_tools()
            save("catalog.json", {"server": initialized.serverInfo.model_dump(mode="json"), "tools": [t.model_dump(mode="json") for t in catalog.tools]})
            print("MCP 连接成功，工具数量：", len(catalog.tools), flush=True)

            async def call(name, tool, arguments):
                raw = await session.call_tool(tool, arguments=arguments)
                assert not raw.isError, raw
                texts = [c.text for c in raw.content if c.type == "text"]
                assert len(texts) == 1
                result = json.loads(texts[0])
                records.append({"case": name, "tool": tool, "arguments": arguments, "result": result})
                save("result.json", {"transport": "mcp-stdio", "scope": "local_execution_and_llm_review_summary", "model": "kimi-k3", "checks": records})
                print(name, json.dumps(result, ensure_ascii=False), flush=True)
                return result

            first = await call("text_write", "file_write", {"path": "notes.txt", "content": "execution-tools: initial\n", "overwrite": True})
            assert first["success"]
            edited = await call("text_edit", "file_edit", {"path": "notes.txt", "search": "initial", "replace": "edited"})
            assert edited["success"]
            assert (workspace / "notes.txt").read_text(encoding="utf-8") == "execution-tools: edited\n"
            approved = await call("llm_overwrite_review", "file_write", {"path": "notes.txt", "content": "execution-tools: approved overwrite\n", "overwrite": False})
            assert approved["success"], "模型审批未允许覆盖"
            assert (workspace / "notes.txt").read_text(encoding="utf-8") == "execution-tools: approved overwrite\n"
            denied = await call("workspace_boundary", "file_write", {"path": "../outside.txt", "content": "boundary check", "overwrite": True})
            assert not denied["success"] and not (output / "outside.txt").exists()
            command = shlex.quote(Path(sys.executable).as_posix()) + " " + shlex.quote((workspace / "calculate.py").as_posix())
            calculated = await call("terminal_calculation", "virtual_terminal", {"command": command, "timeout": 30})
            assert calculated["success"] and calculated["stdout"].strip() == "4000"
            long_command = "for i in {1..260}; do printf 'LINE-%03d %0160d\\n' \"$i\" \"$i\"; done"
            summarized = await call("long_output_summary", "virtual_terminal", {"command": long_command, "timeout": 120})
            assert summarized["success"] and summarized["stdout_file"]
            full_output = Path(summarized["stdout_file"]).read_text(encoding="utf-8")
            assert len(full_output.splitlines()) == 260
            assert summarized["stdout"].startswith("[SUMMARIZED OUTPUT]")
            (output / "full-output.txt").write_text(full_output, encoding="utf-8")
            receipts = json.loads((output / "llm_receipts.json").read_text(encoding="utf-8"))
            assert any(r["purpose"] == "dangerous_operation_review" for r in receipts)
            save("verification.json", {"checks_passed": 6, "calculation": 4000, "full_output_lines": 260, "full_output_sha256": hashlib.sha256(full_output.encode()).hexdigest(), "approval_receipts": len(receipts), "workspace_boundary_enforced": True, "summary_generated": True, "not_executed": ["code_interpreter", "Docker sandbox", "Google Calendar", "GitHub PR tool", "browser and desktop/mobile tools", "multi-language execution"]})
    print("实验完成：6 项实际检查通过。", flush=True)


asyncio.run(main())
