"""
Interview Question Generator Service
Core Prompt Engineering for InterviewKoi
"""
import os
import json
import httpx
from typing import List, Optional
from app.models.schemas import JobType, InterviewStyle, Question, StarAnswer


class InterviewGenerator:
    """面试问题生成器 - 核心Prompt工程"""
    
    # DeepSeek API配置
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL = "deepseek-chat"
    
    @classmethod
    def _get_api_key(cls) -> str:
        """获取API Key"""
        return os.getenv("DEEPSEEK_API_KEY", "")
    
    @classmethod
    async def _call_deepseek(cls, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """调用DeepSeek API"""
        api_key = cls._get_api_key()
        
        if not api_key:
            # Demo模式，返回示例数据
            return cls._get_demo_response(user_prompt)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": cls.DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                cls.DEEPSEEK_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    @classmethod
    def _get_demo_response(cls, user_prompt: str) -> str:
        """演示模式响应"""
        if "预测" in user_prompt or "predict" in user_prompt.lower():
            return json.dumps({
                "questions": [
                    {"title": "请介绍一下你自己", "type": "行为题", "frequency": "必考", "tips": "控制在2-3分钟内，突出与岗位相关的经历"},
                    {"title": "你最大的优点是什么？", "type": "行为题", "frequency": "必考", "tips": "结合具体事例说明，避免空洞"},
                    {"title": "为什么离职？", "type": "行为题", "frequency": "高频", "tips": "积极正面，避免负面评价前公司"},
                    {"title": "你的职业规划是什么？", "type": "行为题", "frequency": "高频", "tips": "与应聘岗位发展路径结合"},
                    {"title": "期望薪资是多少？", "type": "情景题", "frequency": "高频", "tips": "给出一个合理范围而非具体数字"}
                ]
            })
        elif "STAR" in user_prompt or "答案" in user_prompt:
            return json.dumps({
                "answer": {
                    "situation": "在我上一家公司担任产品经理时，公司正在开发一款新的移动应用",
                    "task": "我需要在3个月内完成从需求分析到产品上线的全流程",
                    "action": "1. 深入调研用户需求\n2. 协调设计和开发团队\n3. 制定详细的产品Roadmap\n4. 每日站会跟进进度",
                    "result": "产品提前1周上线，首月活跃用户达到10万+，获得用户好评"
                },
                "overall_tips": "回答时注意用数据说话，保持逻辑清晰"
            })
        else:
            return "面试中，请继续回答。"
    
    @classmethod
    def _get_style_instruction(cls, style: InterviewStyle) -> str:
        """获取面试风格指令"""
        styles = {
            InterviewStyle.PRESSURE: """你正在扮演一位严格的面试官，采用压力面试风格：
- 会质疑候选人的回答
- 追问细节，不给模糊回答的机会
- 语气犀利，但公正专业
- 会在你回答后说"真的吗？"、"这个不太可信"等质疑性语言""",
            
            InterviewStyle.FRIENDLY: """你正在扮演一位友善的面试官，采用轻松聊天风格：
- 语气温和，像朋友聊天
- 给你鼓励和正向反馈
- 引导你展示真实自我
- 会说"没关系，放轻松"等安抚性语言""",
            
            InterviewStyle.BEHAVIORAL: """你正在扮演一位专业的面试官，采用STAR行为面试法：
- 深挖你的具体经历
- 关注你在情境中的具体行动
- 追问可量化的成果
- 评估你的能力与岗位的匹配度""",
            
            InterviewStyle.TECHNICAL_DEEP: """你正在扮演一位技术专家面试官，采用技术深挖风格：
- 追问技术实现的底层原理
- 要求讲解技术方案的选择原因
- 会问"如果...你会怎么做"等假设性问题
- 评估技术深度和解决问题的能力"""
        }
        return styles.get(style, styles[InterviewStyle.BEHAVIORAL])
    
    @classmethod
    def _get_job_type_context(cls, job_type: JobType) -> str:
        """获取岗位类型上下文"""
        contexts = {
            JobType.TECHNICAL: """岗位类型：技术岗
核心技术问题可能包括：
- 编程语言基础（Python/Java/JavaScript等）
- 数据结构与算法
- 系统设计能力
- 数据库知识
- 项目经验和技术难点""",
            
            JobType.PRODUCT: """岗位类型：产品岗
核心能力问题可能包括：
- 产品设计思维
- 用户需求分析
- 数据驱动决策
- 项目管理能力
- 跨团队协作经验""",
            
            JobType.MANAGEMENT: """岗位类型：管理岗
核心能力问题可能包括：
- 团队管理经验
- 项目统筹能力
- 跨部门协调
- 目标拆解与执行
- 绩效管理和激励""",
            
            JobType.GENERAL: """岗位类型：通用岗
核心能力问题可能包括：
- 沟通表达能力
- 问题解决能力
- 学习适应能力
- 团队协作精神
- 职业素养和态度"""
        }
        return contexts.get(job_type, contexts[JobType.GENERAL])
    
    @classmethod
    async def predict_questions(
        cls,
        job_title: str,
        job_type: JobType,
        resume: str,
        style: InterviewStyle,
        count: int = 12
    ) -> List[Question]:
        """预测面试题目"""
        system_prompt = f"""你是一位资深HR面试专家，擅长预测各类岗位的面试问题。
你需要根据岗位信息和候选人简历，预测最可能被问到的面试题。

要求：
1. 生成 {count} 道预测题目
2. 按出现概率排序：必考 > 高频 > 中频 > 低频
3. 分类：行为题/技术题/情景题/文化题
4. 每道题给出简短的答题提示

{cls._get_job_type_context(job_type)}

输出格式（JSON）：
{{
    "questions": [
        {{"title": "问题", "type": "类型", "frequency": "频率", "tips": "提示"}}
    ]
}}"""
        
        user_prompt = f"""岗位：{job_title}

候选人简历/经历：
{resume}

请预测面试中可能问到的{count}道题目。"""
        
        try:
            response = await cls._call_deepseek(system_prompt, user_prompt)
            # 尝试解析JSON
            data = json.loads(response)
            questions = [
                Question(
                    title=q.get("title", ""),
                    type=q.get("type", "行为题"),
                    frequency=q.get("frequency", "中频"),
                    tips=q.get("tips", "")
                )
                for q in data.get("questions", [])
            ]
            return questions[:count]
        except (json.JSONDecodeError, KeyError):
            # 解析失败，返回默认题库
            return cls._get_default_questions(job_type)
    
    @classmethod
    def _get_default_questions(cls, job_type: JobType) -> List[Question]:
        """获取默认题目"""
        defaults = {
            JobType.TECHNICAL: [
                Question(title="请介绍一下你最满意的项目", type="技术题", frequency="必考", tips="突出技术难点和解决方案"),
                Question(title="你遇到过最困难的技术问题是什么？", type="技术题", frequency="必考", tips="展示问题解决能力"),
                Question(title="如何保证代码质量？", type="技术题", frequency="高频", tips="涉及测试、Code Review等"),
                Question(title="介绍一下你熟悉的设计模式", type="技术题", frequency="高频", tips="结合实际使用场景"),
                Question(title="如何进行性能优化？", type="技术题", frequency="高频", tips="给出具体案例和数据"),
                Question(title="你有带过团队吗？", type="管理题", frequency="中频", tips="展示协作和领导力"),
                Question(title="为什么想加入我们？", type="文化题", frequency="必考", tips="展示对公司了解"),
                Question(title="你的职业规划是什么？", type="行为题", frequency="高频", tips="与岗位发展结合"),
                Question(title="离职原因是什么？", type="行为题", frequency="高频", tips="积极正面的理由"),
                Question(title="期望薪资是多少？", type="情景题", frequency="高频", tips="给范围而非具体数字"),
                Question(title="你最近在学什么新技术？", type="技术题", frequency="中频", tips="展示学习能力"),
                Question(title="手撕算法：反转链表", type="技术题", frequency="必考", tips="提前练习高频题型"),
            ],
            JobType.PRODUCT: [
                Question(title="请介绍一下你做过的最成功的产品", type="产品题", frequency="必考", tips="用数据说明成果"),
                Question(title="如何进行需求优先级排序？", type="产品题", frequency="必考", tips="展示方法论"),
                Question(title="你如何理解产品经理这个岗位？", type="产品题", frequency="必考", tips="展示认知深度"),
                Question(title="介绍一下你的产品设计思路", type="产品题", frequency="高频", tips="从用户需求出发"),
                Question(title="如何进行用户调研？", type="产品题", frequency="高频", tips="展示方法论"),
                Question(title="和开发团队有冲突怎么办？", type="情景题", frequency="高频", tips="展示沟通能力"),
                Question(title="为什么想做产品经理？", type="行为题", frequency="高频", tips="热情+能力匹配"),
                Question(title="你平时的产品感从哪里来？", type="产品题", frequency="中频", tips="展示对产品的热爱"),
                Question(title="你觉得自己适合做产品吗？", type="行为题", frequency="高频", tips="自信但不自大"),
                Question(title="期望薪资是多少？", type="情景题", frequency="高频", tips="给范围"),
                Question(title="职业规划是什么？", type="行为题", frequency="高频", tips="与公司发展结合"),
                Question(title="用过我们的产品吗？有什么建议？", type="文化题", frequency="中频", tips="提前体验并准备建议"),
            ],
            JobType.MANAGEMENT: [
                Question(title="你有多少人的团队管理经验？", type="管理题", frequency="必考", tips="具体数字+团队构成"),
                Question(title="如何进行绩效管理？", type="管理题", frequency="必考", tips="展示方法论和实践"),
                Question(title="团队成员出现冲突怎么处理？", type="情景题", frequency="必考", tips="案例+方法"),
                Question(title="如何培养下属？", type="管理题", frequency="高频", tips="因材施教的方法"),
                Question(title="做过的最困难的管理决定是什么？", type="行为题", frequency="高频", tips="展示决策能力"),
                Question(title="如何设定团队目标？", type="管理题", frequency="高频", tips="SMART原则"),
                Question(title="为什么离开现在的公司？", type="行为题", frequency="高频", tips="寻找更好的发展"),
                Question(title="你的管理风格是什么？", type="行为题", frequency="高频", tips="真实+符合公司文化"),
                Question(title="期望薪资是多少？", type="情景题", frequency="高频", tips="给范围"),
                Question(title="如何说服老板增加资源？", type="情景题", frequency="中频", tips="展示影响力"),
                Question(title="职业规划是什么？", type="行为题", frequency="高频", tips="与管理岗位发展结合"),
                Question(title="如何面对上级的不合理要求？", type="情景题", frequency="中频", tips="展示沟通和原则性"),
            ],
            JobType.GENERAL: [
                Question(title="请做一个自我介绍", type="行为题", frequency="必考", tips="2-3分钟，突出优势"),
                Question(title="你最大的优点是什么？", type="行为题", frequency="必考", tips="结合具体事例"),
                Question(title="你最大的缺点是什么？", type="行为题", frequency="必考", tips="真实但不影响工作"),
                Question(title="为什么想加入我们公司？", type="行为题", frequency="必考", tips="展示了解和热情"),
                Question(title="你还有什么问题想问我的？", type="情景题", frequency="必考", tips="准备3-5个好问题"),
                Question(title="你如何处理压力？", type="行为题", frequency="高频", tips="展示抗压能力"),
                Question(title="职业规划是什么？", type="行为题", frequency="高频", tips="与岗位结合"),
                Question(title="离职原因是什么？", type="行为题", frequency="高频", tips="积极正面"),
                Question(title="期望薪资是多少？", type="情景题", frequency="高频", tips="给范围"),
                Question(title="你有团队协作的经验吗？", type="行为题", frequency="高频", tips="具体案例"),
                Question(title="如何快速学习新技能？", type="行为题", frequency="中频", tips="展示学习能力"),
                Question(title="你的抗压能力如何？", type="行为题", frequency="中频", tips="用事例说明"),
            ]
        }
        return defaults.get(job_type, defaults[JobType.GENERAL])
    
    @classmethod
    async def generate_answer(
        cls,
        job_title: str,
        job_type: JobType,
        question: str,
        resume: str,
        style: InterviewStyle
    ) -> dict:
        """生成STAR法则答案"""
        system_prompt = f"""你是一位资深面试教练，擅长用STAR法则帮助候选人准备面试答案。

STAR法则结构：
- S (Situation) 情境：描述背景和环境
- T (Task) 任务：明确你的职责和目标
- A (Action) 行动：详细描述你采取的具体行动（重点部分，3-5个步骤）
- R (Result) 结果：量化你的成果（用数据说话）

要求：
1. 答案要基于候选人真实经历定制
2. 语言口语化，自然流畅
3. 突出可量化的成果
4. 连接词自然过渡

{cls._get_job_type_context(job_type)}

输出格式（JSON）：
{{
    "answer": {{
        "situation": "情境描述",
        "task": "任务目标",
        "action": "具体行动步骤（用换行分隔）",
        "result": "量化结果"
    }},
    "overall_tips": "整体答题技巧"
}}"""
        
        user_prompt = f"""岗位：{job_title}
问题：{question}

候选人简历/经历：
{resume}

请用STAR法则生成一个面试答案。"""
        
        try:
            response = await cls._call_deepseek(system_prompt, user_prompt)
            data = json.loads(response)
            return {
                "answer": StarAnswer(
                    situation=data["answer"]["situation"],
                    task=data["answer"]["task"],
                    action=data["answer"]["action"],
                    result=data["answer"]["result"]
                ),
                "overall_tips": data.get("overall_tips", "回答时注意用数据说话，保持逻辑清晰。")
            }
        except (json.JSONDecodeError, KeyError):
            return cls._get_default_answer(question, resume)
    
    @classmethod
    def _get_default_answer(cls, question: str, resume: str) -> dict:
        """获取默认答案"""
        return {
            "answer": StarAnswer(
                situation="在我上一段工作经历中，我负责了一个重要项目",
                task="需要在规定时间内完成项目目标，并确保质量",
                action="1. 深入了解需求和背景\n2. 制定详细的执行计划\n3. 协调各方资源推进\n4. 及时解决问题和风险\n5. 总结复盘优化流程",
                result="项目成功完成，达到了预期目标，获得了客户好评"
            ),
            "overall_tips": "建议结合自己的真实经历来回答，突出你在其中的具体行动和成果。"
        }
    
    @classmethod
    async def simulate_interview(
        cls,
        job_title: str,
        job_type: JobType,
        resume: str,
        style: InterviewStyle,
        history: List[dict],
        user_answer: Optional[str] = None
    ) -> dict:
        """模拟面试"""
        # 构建对话历史
        conversation = []
        for msg in history:
            role = "面试官" if msg.get("role") == "interviewer" else "候选人"
            conversation.append(f"{role}：{msg.get('content', '')}")
        
        history_text = "\n".join(conversation) if conversation else "面试刚开始"
        
        system_prompt = f"""你是一位专业的面试官，正在对候选人进行面试。

{cls._get_style_instruction(style)}

{cls._get_job_type_context(job_type)}

岗位：{job_title}

要求：
1. 第一轮：问一个开场问题（如自我介绍或基本信息）
2. 用户回答后：追问细节或问下一个问题
3. 3轮后给出总体评价
4. 每次回复都要评估用户表现并给出建议
5. 使用中文对话

输出格式（JSON）：
{{
    "response": "面试官的回复",
    "next_question": "下一道问题（如果没有则为空）",
    "score": 评分(0-100),
    "feedback": "对该轮回答的评价和建议",
    "is_finished": false
}}"""
        
        user_prompt = f"""面试历史：
{history_text}

候选人简历：
{resume}
"""
        if user_answer:
            user_prompt += f"\n\n候选人回答：\n{user_answer}"
        
        try:
            response = await cls._call_deepseek(system_prompt, user_prompt, temperature=0.8)
            data = json.loads(response)
            return {
                "response": data.get("response", ""),
                "next_question": data.get("next_question"),
                "score": data.get("score"),
                "feedback": data.get("feedback"),
                "is_finished": data.get("is_finished", False)
            }
        except (json.JSONDecodeError, KeyError):
            return cls._get_default_simulate_response(history, user_answer)
    
    @classmethod
    def _get_default_simulate_response(cls, history: List[dict], user_answer: Optional[str]) -> dict:
        """获取默认模拟面试响应"""
        round_num = len([h for h in history if h.get("role") == "interviewer"]) + 1
        
        if round_num == 1:
            return {
                "response": "你好，请先做一个简短的自我介绍吧，重点说一下你和这个岗位相关的工作经历。",
                "next_question": "请介绍你自己",
                "score": None,
                "feedback": None,
                "is_finished": False
            }
        elif user_answer:
            return {
                "response": "好的，了解到你的经历了。能否具体说说在XXX项目中，你具体负责了什么？遇到了什么困难？",
                "next_question": "请详细说说你的项目经历",
                "score": 75,
                "feedback": "回答整体不错，建议多使用具体数据和成果来支撑你的观点。",
                "is_finished": False
            }
        else:
            return {
                "response": "感谢你的回答，本轮面试到此结束。",
                "next_question": None,
                "score": 78,
                "feedback": "整体表现不错，建议：1. 多用数据说话；2. 突出与岗位匹配的技能；3. 保持自信但不自大。",
                "is_finished": True
            }
