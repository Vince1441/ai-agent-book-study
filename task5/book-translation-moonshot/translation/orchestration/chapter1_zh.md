# 第 1 章：大语言模型推理基础

大语言模型在对任何内容进行推理之前，必须先将文本转换为数字。每一段文本首先被切分为**词元**，即模型处理的最小单位。随后，每个词元都被映射为一个**嵌入向量**，这是一个在高维空间中捕捉其语义的稠密向量。

当用户发送请求时，他们输入的文本称为**提示词**。让模型基于该提示词运行并生成答案的过程称为**推理**。从发送提示词到收到首个响应之间的时间，就是用户能直接感受到的**时延**。

一个最简单的推理调用如下所示：

```python
def generate(prompt: str, model) -> str:
    tokens = model.tokenize(prompt)      # split prompt into tokens
    embeddings = model.embed(tokens)     # map each token to an embedding
    output = model.forward(embeddings)   # run inference
    return model.detokenize(output)
```

有两个数字主导着用户体验。第一个是提示词中的词元数量，因为提示词越长，所需的计算量就越大。第二个是首个词元的时延，因为首个词元一旦缓慢，整个系统就会给人迟滞的感觉。在本书中，我们将不断回到这些概念：词元、嵌入向量、提示词、推理和时延。现在就把它们的定义弄清楚，可以为后续的学习避免许多困惑。