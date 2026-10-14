import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[3])
root = parser.parse_args().source_root.resolve()
experiment = root / "chapter2" / "context-compression"
load_dotenv(root / "chapter2" / "kv-cache" / ".env", override=True)
os.environ["KIMI_API_KEY"] = os.environ["MOONSHOT_API_KEY"]
os.environ["LLM_PROVIDER"] = "kimi"
os.environ["MODEL_NAME"] = "kimi-k3"
sys.path.insert(0, str(experiment))

from compression_strategies import ContextCompressor, CompressionStrategy

source = root / "chapter2" / "system-hint" / "config.py"
content = source.read_text(encoding="utf-8")
output = Path(__file__).resolve().parent
(output / "input.txt").write_text(content, encoding="utf-8")
query = "概括配置文件的五项状态提示功能、默认开关和模型配置读取方式。"
compressor = ContextCompressor(
    CompressionStrategy.WINDOWED_CONTEXT,
    os.environ["MOONSHOT_API_KEY"],
    enable_streaming=False,
)
result = compressor.compress_for_history(content, "read_file", query, preserve_citations=False)
assert result.content and "[Content truncated for history...]" not in result.content
assert result.compressed_length < result.original_length
record = {
    "scope": "local_text_history_compression",
    "live_search_executed": False,
    "model": compressor.model,
    "source_file": "chapter2/system-hint/config.py",
    "query": query,
    "original_characters": result.original_length,
    "compressed_characters": result.compressed_length,
    "original_tokens_estimate": compressor.count_tokens(content),
    "compressed_tokens_estimate": compressor.count_tokens(result.content),
    "token_estimator": "cl100k_base，非 Moonshot 精确计费 token",
    "compressed_content": result.content,
    "strategy": result.strategy.value,
    "timestamp": result.timestamp,
}
(output / "result.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
