"""
Interview Router - Core interview API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PredictRequest, PredictResponse,
    AnswerRequest, AnswerResponse,
    SimulateRequest, SimulateResponse,
    UsageResponse,
    Question, StarAnswer
)
from app.services.generator import InterviewGenerator
from app.services.billing import BillingService

router = APIRouter(prefix="/api/interview", tags=["面试"])


@router.post("/predict", response_model=PredictResponse)
async def predict_questions(request: PredictRequest):
    """预测面试题目"""
    # 检查计费
    allowed, usage = BillingService.check_and_increment()
    if not allowed:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "免费次数已用完",
                "free_remaining": 0,
                "is_pro": False,
                "upgrade_url": "/#pro"
            }
        )
    
    # 生成预测题目
    questions = await InterviewGenerator.predict_questions(
        job_title=request.job_title,
        job_type=request.job_type,
        resume=request.resume,
        style=request.style,
        count=12
    )
    
    return PredictResponse(
        questions=questions,
        remaining=usage["count"]
    )


@router.post("/answer", response_model=AnswerResponse)
async def generate_answer(request: AnswerRequest):
    """生成STAR法则答案"""
    # 检查计费
    allowed, usage = BillingService.check_and_increment()
    if not allowed:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "免费次数已用完",
                "free_remaining": 0,
                "is_pro": False,
                "upgrade_url": "/#pro"
            }
        )
    
    # 生成答案
    result = await InterviewGenerator.generate_answer(
        job_title=request.job_title,
        job_type=request.job_type,
        question=request.question,
        resume=request.resume,
        style=request.style
    )
    
    return AnswerResponse(
        answer=result["answer"],
        overall_tips=result["overall_tips"]
    )


@router.post("/simulate", response_model=SimulateResponse)
async def simulate_interview(request: SimulateRequest):
    """模拟面试"""
    # 检查计费
    allowed, usage = BillingService.check_and_increment()
    if not allowed:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "免费次数已用完",
                "free_remaining": 0,
                "is_pro": False,
                "upgrade_url": "/#pro"
            }
        )
    
    # 模拟面试
    result = await InterviewGenerator.simulate_interview(
        job_title=request.job_title,
        job_type=request.job_type,
        resume=request.resume,
        style=request.style,
        history=request.history,
        user_answer=request.user_answer
    )
    
    return SimulateResponse(
        response=result["response"],
        next_question=result.get("next_question"),
        score=result.get("score"),
        feedback=result.get("feedback"),
        is_finished=result.get("is_finished", False)
    )


@router.get("/usage", response_model=UsageResponse)
async def get_usage():
    """获取使用情况"""
    usage = BillingService.get_remaining()
    return UsageResponse(**usage)


@router.post("/upgrade/pro")
async def upgrade_to_pro():
    """升级到Pro（演示）"""
    # 实际生产环境需要接入支付
    BillingService.activate_pro()
    return {"success": True, "message": "Pro已激活", "is_pro": True}
