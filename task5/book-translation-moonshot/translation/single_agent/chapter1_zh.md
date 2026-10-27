# 第 1 章：LLM 推理基础

大语言模型在对任何内容进行推理之前，会先把文本转换成数字。每一段文本首先被切分为一个个 **token（词元）**，这是模型处理的最小单位。随后，每个 token 会被映射为一个 **embedding（嵌入）**，即一个在高维空间中捕捉其含义的稠密向量。

当用户发送请求时，他们输入的文本称为 **prompt（提示词）**。让模型基于该 prompt 运行并生成回答的过程称为 **inference（推理）**。从发送 prompt 到收到第一个响应之间的时间，就是用户能直接感受到的 **latency（延迟）**。

一个最简的推理调用如下所示：

```python
def generate(prompt: str, model) -> str:
    tokens = model.tokenize(prompt)      # split prompt into tokens
    embeddings = model.embed(tokens)     # map each token to an embedding
    output = model.forward(embeddings)   # run inference
    return model.detokenize(output)
```

有两个数字主导着用户体验。第一是 prompt 中的 token 数量，因为 prompt 越长，消耗的计算量就越大。第二是第一个 token 的延迟，因为首 token 太慢会让整个系统显得迟钝。在本书中，我们会反复回到这些概念：token、embedding、prompt、inference 和 latency。现在就把它们的定义弄清楚，能为后面避免很多困惑。