# JD Resume Matching Agent

一个面向求职场景的轻量级 Agent 项目：输入简历和岗位 JD，输出匹配分析、技能缺口、项目改写建议和模拟面试题。

## 目标

这个项目的定位不是“万能求职助手”，而是一个 **可运行、可讲清楚、能写进简历** 的 MVP：

- 读取 `txt / md / docx` 简历与 JD
- 抽取关键词与技能标签
- 计算岗位匹配度
- 给出技能缺口与简历改写建议
- 生成模拟面试题
- 输出 Markdown 或 JSON 结果

## 为什么这个项目适合你现在做

- 和你当前求职目标直接相关
- 技术点贴近大模型 / Agent 岗
- MVP 成本低，3~7 天能持续迭代
- 面试里很好讲：为什么做、怎么拆任务、怎么控制输出质量

## 目录结构

```text
jd_resume_agent/
├── __init__.py
├── analyzer.py      # 核心分析逻辑
├── cli.py           # 命令行入口
└── parsers.py       # txt / md / docx 解析
examples/
├── sample_jd.txt
└── sample_resume.md
```

## 快速开始

在 workspace 根目录运行：

```bash
python3 -m jd_resume_agent.cli \
  --resume examples/sample_resume.md \
  --jd examples/sample_jd.txt \
  --format markdown
```

输出 JSON：

```bash
python3 -m jd_resume_agent.cli \
  --resume examples/sample_resume.md \
  --jd examples/sample_jd.txt \
  --format json
```

保存到文件：

```bash
python3 -m jd_resume_agent.cli \
  --resume examples/sample_resume.md \
  --jd examples/sample_jd.txt \
  --format markdown \
  --output outputs/report.md
```

## 当前实现

### 已完成
- 文本解析：`txt / md / docx`
- 关键词抽取：基于规则与词典
- 匹配度计算：命中率 + 加权覆盖
- 缺口分析：缺失技能、弱表达项
- 简历改写建议：基于现有经历的定向改写提示
- 模拟面试题：根据 JD 缺口与已命中技能生成

### 下一步建议
- 接入 LLM API 或本地模型，做更强的改写与问答
- 加入 FastAPI / Streamlit 页面
- 增加评测样例集，对 Prompt / 检索策略做 A/B 测试
- 增加经历片段库，实现更像 RAG 的内容重组

## 你可以怎么写进简历

### 求职场景简历优化智能体（JD-Resume Matching Agent）
- 设计面向求职场景的简历优化 Agent，支持 JD 解析、关键词抽取、匹配度分析、项目经历改写与模拟面试题生成
- 基于结构化规则与固定输出模板，提升岗位定制化建议的稳定性与可用性
- 引入基于真实经历的内容重组思路，降低泛化表达与虚构内容风险
- 对不同关键词规则与输出结构进行迭代优化，增强结果一致性与解释性

## 面试讲法

### 1. 为什么做
因为自己在转大模型 / Agent 岗，发现很多简历优化工具输出很空泛，所以做了一个更关注“岗位匹配分析 + 基于真实经历的改写建议”的 Agent。

### 2. 技术怎么拆
把任务拆成：
1. 文本解析
2. 关键词抽取
3. 匹配度计算
4. 缺口识别
5. 改写建议生成
6. 模拟面试题生成

### 3. 亮点在哪
- 不是直接让模型重写，而是先做结构化分析
- 优先基于真实经历给建议，减少幻觉
- 输出结构固定，便于后续接大模型做增强

## 注意
这是一个 **真实可运行的 MVP**，不是靠简历措辞硬包装的空项目。你后面完全可以继续把它升级成：
- Web 工具
- 支持 LLM 改写
- 支持多份 JD 批量分析
- 支持岗位匹配评分排行榜
