# 第 2 章：Transformer 与注意力机制

现代语言模型建立在 **transformer（变换器）** 架构之上。其核心思想是 **attention（注意力）**：模型不再严格地按从左到右的顺序读取序列，而是让每个 token 都能"看到"其他所有 token，并判断哪些 token 更重要。正因如此，transformer 才能把一个代词与许多 token 之前出现的名词联系起来。

注意力机制作用于每个 token 的 **embedding（嵌入）** 之上。对于每个 token，模型会计算三个向量——查询（query）、键（key）和值（value）——并用它们来权衡每个 token 应该对其他 token 投入多少关注。

```python
def attention(query, key, value):
    scores = query @ key.T          # similarity between tokens
    weights = softmax(scores)       # attention weights
    return weights @ value          # weighted embedding
```

由于注意力机制要将每个 token 与其他所有 token 进行比较，其开销会随着 prompt 变长而迅速增长。这正是我们将在下一章中着手解决的延迟问题的根源。尽管如此，注意力机制正是 transformer 强大能力的来源：在推理过程中，它让模型能够在整个 prompt 范围内灵活地传递信息，而不是被限制在一条固定的流水线中。