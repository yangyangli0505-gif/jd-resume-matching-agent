from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from typing import Dict, List, Sequence

SKILL_PATTERNS: Dict[str, Sequence[str]] = {
    "python": [r"\bpython\b"],
    "sql": [r"\bsql\b"],
    "pandas": [r"\bpandas\b"],
    "numpy": [r"\bnumpy\b"],
    "scikit-learn": [r"scikit-learn", r"sklearn"],
    "pytorch": [r"\bpytorch\b"],
    "lightgbm": [r"\blightgbm\b"],
    "xgboost": [r"\bxgboost\b"],
    "llm": [r"\bllm\b", r"大模型"],
    "prompt engineering": [r"prompt engineering", r"prompt"],
    "rag": [r"\brag\b", r"检索增强", r"知识库"],
    "agent": [r"\bagent\b", r"智能体"],
    "tool calling": [r"tool calling", r"工具调用"],
    "multi-agent": [r"multi-agent", r"多 agent", r"多智能体"],
    "embedding": [r"embedding", r"向量化"],
    "rerank": [r"rerank"],
    "ollama": [r"ollama"],
    "ragflow": [r"ragflow"],
    "openclaw": [r"openclaw"],
    "claude code": [r"claude code"],
    "fastapi": [r"fastapi"],
    "flask": [r"\bflask\b"],
    "docker": [r"\bdocker\b"],
    "api": [r"\bapi\b"],
    "evaluation": [r"评测", r"测试样例", r"a/b", r"效果对比"],
    "vector retrieval": [r"向量检索", r"vector retrieval"],
}

ACTION_VERBS = [
    "设计", "搭建", "构建", "实现", "优化", "开发", "完成", "负责", "迭代", "部署"
]


@dataclass
class AnalysisResult:
    overall_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    resume_highlights: List[str]
    rewrite_suggestions: List[str]
    interview_questions: List[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)



def _normalize(text: str) -> str:
    return text.lower()



def extract_skills(text: str) -> List[str]:
    normalized = _normalize(text)
    hits = []
    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            hits.append(skill)
    return sorted(set(hits))



def extract_highlights(resume_text: str, limit: int = 5) -> List[str]:
    lines = [line.strip(" -•\t") for line in resume_text.splitlines() if line.strip()]
    scored = []
    for line in lines:
        score = 0
        if any(verb in line for verb in ACTION_VERBS):
            score += 2
        if re.search(r"\d", line):
            score += 1
        if len(line) >= 18:
            score += 1
        scored.append((score, line))
    scored.sort(key=lambda item: (-item[0], len(item[1])))
    return [line for _, line in scored[:limit]]



def score_match(jd_skills: Sequence[str], resume_skills: Sequence[str]) -> int:
    if not jd_skills:
        return 60
    overlap = len(set(jd_skills) & set(resume_skills))
    ratio = overlap / max(len(set(jd_skills)), 1)
    return int(round(55 + ratio * 45))



def build_rewrite_suggestions(missing_skills: Sequence[str], matched_skills: Sequence[str]) -> List[str]:
    suggestions = []
    if "agent" in matched_skills:
        suggestions.append("把 Agent 相关项目提前到工作经历之前，并明确写出任务拆解、工具调用、上下文管理等关键词。")
    if "rag" in matched_skills:
        suggestions.append("把 RAG 项目写成完整链路：文档解析、切分、向量化、召回、Rerank、生成，而不是只写‘搭了知识库’。")
    if "evaluation" in missing_skills:
        suggestions.append("补一条评测描述，例如：构建测试样例集，对不同 Prompt / 检索策略进行效果对比，提升稳定性。")
    if "fastapi" in missing_skills or "api" in missing_skills:
        suggestions.append("补一个服务化标签，例如 FastAPI / API 封装，哪怕是简单接口，也能显著增强工程感。")
    if "docker" in missing_skills:
        suggestions.append("如果这周能补 Docker 打包与部署说明，简历会更像真正的应用工程项目。")
    if not suggestions:
        suggestions.append("整体匹配已经不错，下一步重点是把项目写得更结果导向，增加指标、评测与工程化细节。")
    return suggestions[:5]



def build_interview_questions(jd_skills: Sequence[str], missing_skills: Sequence[str], matched_skills: Sequence[str]) -> List[str]:
    questions = []
    if "agent" in jd_skills:
        questions.append("你在 Agent 工作流里是怎么做任务拆解和上下文管理的？")
    if "rag" in jd_skills:
        questions.append("你做 RAG 系统时，怎么平衡召回数量、上下文长度和回答准确性？")
    if "tool calling" in jd_skills:
        questions.append("如果模型要调用外部工具，你会如何设计工具选择与失败兜底机制？")
    for skill in list(missing_skills)[:2]:
        questions.append(f"你目前对 {skill} 的理解和实践到什么程度？如果入职后让你补齐，你会怎么推进？")
    if "openclaw" in matched_skills or "claude code" in matched_skills:
        questions.append("你用 OpenClaw / Claude Code 做过哪些真实任务？效果是怎么验证的？")
    return questions[:6]



def analyze(resume_text: str, jd_text: str) -> AnalysisResult:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    missing_skills = sorted(set(jd_skills) - set(resume_skills))
    matched_skills = sorted(set(jd_skills) & set(resume_skills))
    highlights = extract_highlights(resume_text)
    overall_score = score_match(jd_skills, resume_skills)
    rewrite_suggestions = build_rewrite_suggestions(missing_skills, matched_skills)
    interview_questions = build_interview_questions(jd_skills, missing_skills, matched_skills)

    return AnalysisResult(
        overall_score=overall_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        resume_highlights=highlights,
        rewrite_suggestions=rewrite_suggestions,
        interview_questions=interview_questions,
    )



def _bullet_lines(items: Sequence[str]) -> List[str]:
    if not items:
        return ["- 暂无"]
    return [f"- {item}" for item in items]



def to_markdown(result: AnalysisResult) -> str:
    sections: List[str] = []
    sections.append("# JD / Resume 匹配分析")
    sections.append("")
    sections.append(f"**综合匹配度：{result.overall_score}/100**")
    sections.append("")
    sections.append("## 已命中技能")
    sections.extend(_bullet_lines(result.matched_skills))
    sections.append("")
    sections.append("## 技能缺口")
    sections.extend(_bullet_lines(result.missing_skills))
    sections.append("")
    sections.append("## 简历亮点摘取")
    sections.extend(_bullet_lines(result.resume_highlights))
    sections.append("")
    sections.append("## 改写建议")
    sections.extend(_bullet_lines(result.rewrite_suggestions))
    sections.append("")
    sections.append("## 模拟面试题")
    sections.extend(_bullet_lines(result.interview_questions))
    return "\n".join(sections)
