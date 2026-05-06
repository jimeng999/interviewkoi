"""
Pydantic Data Models for InterviewKoi
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum


class JobType(str, Enum):
    """岗位类型"""
    TECHNICAL = "technical"      # 技术岗
    PRODUCT = "product"           # 产品岗
    MANAGEMENT = "management"    # 管理岗
    GENERAL = "general"          # 通用岗


class InterviewStyle(str, Enum):
    """面试风格"""
    PRESSURE = "pressure"        # 压力面试
    FRIENDLY = "friendly"        # 友善聊天
    BEHAVIORAL = "behavioral"    # 行为面试
    TECHNICAL_DEEP = "technical_deep"  # 技术深挖


class FunctionType(str, Enum):
    """功能类型"""
    PREDICT = "predict"          # 考题预测
    ANSWER = "answer"            # 答案生成
    SIMULATE = "simulate"        # 模拟面试


# ============ Request Models ============

class InterviewRequest(BaseModel):
    """面试请求基类"""
    job_title: str = Field(..., description="目标岗位，如'字节跳动 高级产品经理'")
    job_type: JobType = Field(..., description="岗位类型")
    resume: str = Field(..., description="个人简历/经历")
    style: InterviewStyle = Field(InterviewStyle.BEHAVIORAL, description="面试风格")


class PredictRequest(InterviewRequest):
    """考题预测请求"""
    pass


class AnswerRequest(InterviewRequest):
    """答案生成请求"""
    question: str = Field(..., description="面试问题")


class SimulateRequest(InterviewRequest):
    """模拟面试请求"""
    history: List[dict] = Field(default_factory=list, description="对话历史")
    user_answer: Optional[str] = Field(None, description="用户回答")


# ============ Response Models ============

class Question(BaseModel):
    """预测的面试题"""
    title: str = Field(..., description="问题标题")
    type: str = Field(..., description="题目类型：行为题/技术题/情景题/文化题")
    frequency: str = Field(..., description="出现频率：必考/高频/中频/低频")
    tips: str = Field(..., description="回答提示")


class PredictResponse(BaseModel):
    """考题预测响应"""
    questions: List[Question] = Field(..., description="预测题目列表")


class StarAnswer(BaseModel):
    """STAR法则答案"""
    situation: str = Field(..., description="S - 情境")
    task: str = Field(..., description="T - 任务")
    action: str = Field(..., description="A - 行动")
    result: str = Field(..., description="R - 结果")


class AnswerResponse(BaseModel):
    """答案生成响应"""
    answer: StarAnswer = Field(..., description="STAR结构化答案")
    overall_tips: str = Field(..., description="整体回答技巧")


class SimulateResponse(BaseModel):
    """模拟面试响应"""
    response: str = Field(..., description="AI面试官回复")
    next_question: Optional[str] = Field(None, description="下一道题")
    score: Optional[int] = Field(None, ge=0, le=100, description="评分 0-100")
    feedback: Optional[str] = Field(None, description="反馈建议")
    is_finished: bool = Field(False, description="是否结束")


class ApiResponse(BaseModel):
    """通用API响应"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[dict] = None


class UsageResponse(BaseModel):
    """使用次数响应"""
    free_remaining: int = Field(..., description="剩余免费次数")
    is_pro: bool = Field(False, description="是否为Pro用户")
    usage_limit: int = Field(3, description="免费次数限制")
