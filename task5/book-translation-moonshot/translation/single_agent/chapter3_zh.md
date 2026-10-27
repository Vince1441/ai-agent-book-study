# 第 3 章：优化推理延迟

模型能跑起来之后，下一场战役就是速度。目标是在降低 **latency（延迟）** 的同时提高 **throughput（吞吐量）**——即系统每秒完成的请求数量。这两者往往相互制约。

最重要的技巧是 **KV cache（KV 缓存）**。在推理过程中，如果不做优化，模型每生成一步都要对所有之前的 token 重新计算一遍注意力。通过缓存过去 token 的键向量和值向量，模型只需处理最新的 token，从而大幅降低了长 prompt 场景下的延迟。

```python
def decode_step(new_token, kv_cache):
    q, k, v = project(new_token)         # only the new token
    kv_cache.append(k, v)                # reuse past keys and values
    return attention(q, kv_cache.keys, kv_cache.values)
```

第二个技巧是 **batching（批处理）**：将多个 prompt 组合在一起，让硬件保持高利用率。更大的批次能提高吞吐量，但可能会增加单个请求的延迟，因此服务系统需要仔细调节批次大小。

其中的道理在于，推理性能是一种平衡。我们避免重复计算的每一个 token，以及我们合理批处理的每一个 prompt，都在推动系统同时朝着更低延迟和更高吞吐量的方向前进。