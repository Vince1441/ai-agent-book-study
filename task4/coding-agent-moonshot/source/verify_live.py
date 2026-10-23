import argparse
import json
import os
from pathlib import Path

from dotenv import dotenv_values

parser = argparse.ArgumentParser()
parser.add_argument("--env-file", type=Path, required=True)
args = parser.parse_args()
values = dotenv_values(args.env_file)
key = values.get("MOONSHOT_API_KEY") or values.get("KIMI_API_KEY")
assert key and not any(x in key.lower() for x in ["your", "example", "xxx"])
directory = Path(__file__).resolve().parent
os.environ.update({"MOONSHOT_API_KEY": key, "PROVIDER": "moonshot", "DEFAULT_MODEL": "kimi-k3", "WORKING_DIRECTORY": str(directory)})

from config import Config
from agent import CodingAgent

Config.validate()
resolved = Config.resolve()
agent = CodingAgent(api_key=resolved["api_key"], model=resolved["model"], base_url=resolved["base_url"], provider=resolved["provider"])
task = "先调用 Read 读取 README.md，再调用 Read 读取 config.py，核对默认模型名称和密钥变量名称，最后用中文简短回答。只能读取这两个文件，不得读取 .env 或修改任何文件。"
events = []
for event in agent.run(task, max_iterations=6):
    events.append(event)
    if event["type"] in ["tool_call", "tool_execution_complete", "done", "error"]:
        print(json.dumps(event, ensure_ascii=False), flush=True)
    assert event["type"] not in ["error", "max_iterations_reached"], event
completed = [event for event in events if event["type"] == "tool_execution_complete"]
assert len(completed) >= 2
assert all("error" not in event["result"] for event in completed)
assert any(event["type"] == "done" for event in events)
converted = agent._convert_to_openai_format(agent.messages)
reasoned = [m for m in agent.messages if m.get("reasoning_content")]
assert reasoned, "没有获得推理消息，无法验证多轮保留"
assert sum(bool(m.get("reasoning_content")) for m in converted) == len(reasoned)
output = directory / "validation"
output.mkdir(exist_ok=True)
(output / "live-result.json").write_text(json.dumps({"model": agent.model, "tool_executions": len(completed), "reasoning_messages": len(reasoned), "events": events, "messages": agent.messages}, ensure_ascii=False, indent=2), encoding="utf-8")
print("真实多轮工具调用验证通过。", flush=True)
