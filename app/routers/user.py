"""
User Router - User management and preferences
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.get("/profile")
async def get_profile():
    """获取用户信息（演示）"""
    return {
        "id": "demo_user",
        "name": "面试锦鲤用户",
        "is_pro": False,
        "created_at": "2024-01-01T00:00:00Z"
    }


@router.post("/preferences")
async def save_preferences(preferences: dict):
    """保存用户偏好"""
    return {"success": True, "message": "偏好已保存"}
