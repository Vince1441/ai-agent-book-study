# 记忆评估：一个真实模型回答的评分

## 用例与方法

使用仓库评估集中的 `layer1_01_bank_account`，原始历史、问题和评分要求保存于 `input.json`。其中的账号等数字属于仓库自带用例内容。

先将完整历史与当前问题交给 Moonshot `kimi-k3` 生成回答，再调用教材 `LLMEvaluator`，同样使用 `kimi-k3`，对实际生成的回答评分。

## 结果

此次评分 `reward=1.0`、`passed=true`。评委未检测出幻觉，精确性、召回、推理与主动性四个维度均为最高等级。完整依据和模型用量记录见 `result.json`。

这是一个基础回忆用例的完整历史基线，未接入前一项实验生成的记忆，也未覆盖全部 60 个用例。回答模型和评委为同一模型，评分不能作为独立验证或总体准确率。

- `input.json`：实际使用的内置用例。
- `result.json`：真实回答 API 响应及结构化评分。
- `report.txt`：教材评估框架生成的报告。
- `run.log`：真实终端输出。

## 运行

从教材源码根目录执行 `python -u learning-results/task2/run_experiments.py user-memory-evaluation`。依赖与密钥读取方式见[总说明](../README.md)。
