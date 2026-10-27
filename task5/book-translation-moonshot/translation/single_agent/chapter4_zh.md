# 第 4 章：微调与部署

通用模型很少能直接满足特定产品的需求。通常的解决办法是 **fine-tuning（微调）**：在一个规模较小、针对特定任务的数据集上继续训练模型，使其在保持通用能力的同时适应你的领域。

微调会改变模型将 **prompt（提示词）** 转化为回答的方式，但不会改变基本流程：文本变成 **token（词元）**，每个 token 变成 **embedding（嵌入）**，再由 **inference（推理）** 生成结果。改变的是模型学到的权重。

```python
def fine_tune(model, dataset):
    for prompt, target in dataset:
        loss = model.loss(prompt, target)   # compare output to target
        model.update(loss)                  # adjust weights
    return model
```

微调之后便是 **deployment（部署）**：将模型封装在 API 之后，让真实用户可以发送 prompt 并获得回答。此时，之前讨论过的问题会以更大的力度重新浮现。延迟必须保持低水平，吞吐量必须保持高水平，而上一章介绍的 KV 缓存和批处理则承担了主要的工作。

完整的旅程——token、embedding、prompt、inference、latency、微调和部署——至此已经走完。一个曾经只是研究成果的模型，已经变成了人们可以真正使用的服务。