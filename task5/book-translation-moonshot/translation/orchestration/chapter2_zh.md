# 第 2 章：Transformer（变换器）与注意力机制

现代语言模型建立在 **Transformer（变换器）** 架构之上。其核心思想是**注意力机制**：模型不再严格地按从左到右的顺序读取序列，而是让每个词元都能观察所有其他词元，并判断哪些词元是重要的。这正是 Transformer 能够将代词与出现在许多词元之前的名词关联起来的原因。

注意力机制作用于每个词元的**嵌入向量**。对于每个词元，模型会计算三个向量——查询（query）、键（key）和值（value）——并用它们来权衡每个词元应在多大程度上关注其他词元。

```python
def attention(query, key, value):
    scores = query @ key.T          # similarity between tokens
    weights = softmax(scores)       # attention weights
    return weights @ value          # weighted embedding
```

由于注意力机制需要将每个词元与其他所有词元进行比较，其计算开销会随着提示词变长而迅速增长。这正是我们将在下一章中着手解决的时延问题的根源。尽管如此，注意力机制赋予了 Transformer 强大的能力：在推理过程中，它使模型能够在整个提示词范围内灵活地传递信息，而不是受限于固定的流水线。