import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import dotenv_values

parser = argparse.ArgumentParser()
parser.add_argument("experiment", choices=["user-memory", "user-memory-evaluation", "agentic-rag", "contextual-retrieval"])
parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[2])
args = parser.parse_args()
root = args.source_root.resolve()
output = Path(__file__).resolve().parent / args.experiment
output.mkdir(parents=True, exist_ok=True)
source = root / "chapter3" / args.experiment

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
key = None
for env_file in [source / ".env", root / "chapter2/kv-cache/.env", root / "chapter1/context/.env"]:
    values = dotenv_values(env_file)
    candidates = [values.get("MOONSHOT_API_KEY"), values.get("KIMI_API_KEY")]
    usable = [v for v in candidates if v and not any(x in v.lower() for x in ["your", "example", "xxx", "你的"])]
    if usable:
        key = usable[0]
        break
assert key, "缺少有效的 Moonshot Key"
os.environ.update({"MOONSHOT_API_KEY": key, "KIMI_API_KEY": key, "PROVIDER": "kimi", "LLM_PROVIDER": "kimi", "MODEL_NAME": "kimi-k3", "LLM_MODEL": "kimi-k3", "KIMI_MODEL": "kimi-k3"})
sys.path.insert(0, str(source))
os.chdir(source)


def save(name, value):
    (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


if args.experiment == "user-memory":
    from config import Config, MemoryMode
    from conversational_agent import ConversationalAgent, ConversationConfig
    from background_memory_processor import BackgroundMemoryProcessor, MemoryProcessorConfig

    storage = output / "storage"
    Config.MEMORY_STORAGE_DIR = str(storage / "memories")
    Config.CONVERSATION_HISTORY_DIR = str(storage / "conversations")
    Config.LOCOMO_OUTPUT_DIR = str(storage / "locomo")
    Config.LOG_FILE = str(storage / "agent.log")
    Config.create_directories()
    user_id = datetime.now().strftime("task2_%Y%m%d_%H%M%S")
    agent = ConversationalAgent(user_id, provider="kimi", model="kimi-k3", memory_mode=MemoryMode.NOTES, config=ConversationConfig(), verbose=True)
    processor = BackgroundMemoryProcessor(user_id, provider="kimi", model="kimi-k3", memory_mode=MemoryMode.NOTES, config=MemoryProcessorConfig(), verbose=True)
    message = "我在参加 DataWhale Agent-book 学习，项目位于 D:\\AI\\ai-agent-book，使用 Windows 和 Git Bash，Python 环境是项目里的 .venv。请记住这些信息，简短回复。"
    print("用户输入：", message, flush=True)
    answer = agent.chat(message)
    print("首次回答：", answer, flush=True)
    processor.increment_conversation_count()
    processing = processor.process_recent_conversations()
    agent.memory_manager.load_memory()
    memory = agent.memory_manager.get_context_string()
    print("保存的记忆：", memory, flush=True)
    assert processing.get("operations"), "没有实际记忆操作"
    time.sleep(1)
    agent.reset_session()
    question = "你记得我的学习项目、项目目录和运行环境吗？只根据保存的记忆回答。"
    recall = agent.chat(question)
    print("新会话回答：", recall, flush=True)
    assert "DataWhale" in recall or "ai-agent-book" in recall
    save("result.json", {"scope": "single_user_cross_session_smoke", "model": "kimi-k3", "input": message, "initial_answer": answer, "memory_processing": processing, "stored_memory": memory, "recall_question": question, "recall_answer": recall, "new_session_id": agent.get_session_id()})

elif args.experiment == "user-memory-evaluation":
    from framework import UserMemoryEvaluationFramework
    from evaluator import LLMEvaluator
    from openai import OpenAI

    framework = UserMemoryEvaluationFramework()
    case = framework.list_test_cases("layer1")[0]
    save("input.json", case.model_dump(mode="json"))
    histories = [[m.to_dict() for m in h.messages] for h in case.conversation_histories]
    client = OpenAI(api_key=key, base_url="https://api.moonshot.cn/v1")
    response = client.chat.completions.create(model="kimi-k3", temperature=1, max_tokens=4096, messages=[{"role": "system", "content": "根据给定的真实评估集对话历史回答当前问题。缺少信息时说明，不得编造。"}, {"role": "user", "content": json.dumps({"histories": histories, "question": case.user_question}, ensure_ascii=False)}])
    answer = response.choices[0].message.content
    assert answer
    print("测试用例：", case.test_id, case.title, flush=True)
    print("模型回答：", answer, flush=True)
    judge = LLMEvaluator("kimi", model="kimi-k3")
    result = judge.evaluate(case, answer)
    print("评估结果：", result.model_dump_json(indent=2), flush=True)
    save("result.json", {"scope": "one_builtin_layer1_case_full_history_baseline", "model": "kimi-k3", "answer_response": response.model_dump(mode="json"), "evaluation": result.model_dump(mode="json")})
    (output / "report.txt").write_text(framework.generate_report({case.test_id: result}), encoding="utf-8")

elif args.experiment == "agentic-rag":
    from config import Config, KnowledgeBaseType
    from agent import AgenticRAG

    config = Config.from_env()
    config.llm.provider = "kimi"
    config.llm.model = "kimi-k3"
    config.knowledge_base.type = KnowledgeBaseType.OFFLINE
    config.knowledge_base.offline_corpus_path = str(source / "laws")
    config.agent.max_iterations = 8
    config.agent.verbose = True
    query = "根据知识库中的刑法条文，故意杀人罪的法定刑是什么？请引用条文。"
    agent = AgenticRAG(config)
    answer = agent.query(query, stream=False)
    assert answer and not answer.startswith("Error processing query")
    assert "I need more iterations" not in answer
    print("Agentic 回答：", answer, flush=True)
    baseline_agent = AgenticRAG(config)
    baseline = baseline_agent.query_non_agentic(query, stream=False)
    assert baseline and not baseline.startswith("Error")
    print("单次检索回答：", baseline, flush=True)
    save("result.json", {"scope": "one_legal_query_live_llm_local_bm25", "model": "kimi-k3", "knowledge_base": "local laws corpus; offline BM25", "query": query, "agentic_answer": answer, "non_agentic_answer": baseline, "agentic_conversation": agent.conversation_history, "baseline_conversation": baseline_agent.conversation_history})

elif args.experiment == "contextual-retrieval":
    sys.path.insert(0, str(output / "source"))
    from config import LLMConfig, ChunkingConfig
    from contextual_chunking import ContextualChunker

    # 使用真实教材说明文件，保留原始输入便于核验前缀。
    text = (root / "chapter3/README.md").read_text(encoding="utf-8")
    (output / "input.md").write_text(text, encoding="utf-8")
    llm = LLMConfig(provider="kimi", model="kimi-k3")
    chunking = ChunkingConfig(chunk_size=1000, max_chunk_size=1500, min_chunk_size=100, chunk_overlap=100, respect_paragraph_boundary=False)
    chunker = ContextualChunker(chunking_config=chunking, llm_config=llm)
    chunks = chunker.chunk_document(text, "chapter3_readme", {"source": "chapter3/README.md"})
    assert chunks and all(c.context.strip() for c in chunks), "存在未成功生成前缀的分块"
    assert all(c.contextualized_text == c.context + "\n\n" + c.text for c in chunks)
    for c in chunks:
        print(c.chunk_id, "前缀：", c.context, flush=True)
    save("result.json", {"scope": "live_context_prefix_generation_only", "model": llm.model, "source": "chapter3/README.md", "chunks": [c.to_dict() for c in chunks], "stats": chunker.stats, "retrieval_index_built": False, "note": "未执行索引、召回与重排序评估。context_tokens 为教材代码的词数估算，非模型精确计费 token。"})

print("结果已保存：", output / "result.json", flush=True)
