# 从经验中学习：Q-learning 实验

## 目的与环境

在本地寻宝游戏中训练 Q-learning Agent，观察成功率随训练变化。使用项目 `.venv` Python 环境；这部分无需模型 API。

## 运行命令

```bash
source .venv/Scripts/activate
cd chapter1/learning-from-experience
python -u experiment.py --mode qlearning --rl-episodes 10000 --seed 42 \
  2>&1 | tee ../../learning-results/learning-from-experience/run.log
```

程序会在 `results/<运行时间>/experiment_results.json` 保存结果。将所需运行的结果复制到本提交目录并命名为 `result.json`。

## 文件与结果

- `result.json`：复制自已有的 `results/20261011_162310/experiment_results.json`。
- `run.log`：从该 JSON 提取的指标与学习曲线摘要；原始终端输出没有保存。

训练 10000 局，训练成功 4510 局；评估 100 局全部成功。Q 表包含 142 个状态。最后 1000 局训练成功率为 98.1%。

训练阶段包含随机探索，评估阶段使用贪婪策略，因此两个阶段的成功率具有不同含义。上述数据仅描述此次运行。

## 学习方式

本次完成的是 Q-learning：通过游戏反馈更新 Q 表。LLM 上下文学习的对比部分尚未包含在这些结果中。
