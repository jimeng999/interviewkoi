"""
Billing Service - User usage tracking and billing logic
"""
import os
import time
from typing import Optional

# Simple in-memory storage for demo (in production, use Redis/DB)
_usage_store: dict = {}


class BillingService:
    """计费服务"""
    
    FREE_LIMIT = 3  # 免费次数
    PRO_PRICE = 49  # Pro价格
    PRO_UNLIMITED = -1  # Pro无限次
    
    @classmethod
    def _get_user_key(cls, user_id: Optional[str] = None) -> str:
        """获取用户标识"""
        if user_id:
            return f"user:{user_id}"
        # 使用时间戳作为临时用户ID（演示用）
        return f"temp:{int(time.time() // 3600)}"
    
    @classmethod
    def get_usage(cls, user_id: Optional[str] = None) -> dict:
        """获取用户使用情况"""
        key = cls._get_user_key(user_id)
        data = _usage_store.get(key, {
            "count": 0,
            "is_pro": False,
            "reset_date": cls._get_reset_date()
        })
        return data
    
    @classmethod
    def _get_reset_date(cls) -> str:
        """获取重置日期（每月1日）"""
        return time.strftime("%Y-%m")
    
    @classmethod
    def check_and_increment(cls, user_id: Optional[str] = None) -> tuple[bool, dict]:
        """
        检查并增加使用次数
        返回: (是否成功, 当前使用情况)
        """
        key = cls._get_user_key(user_id)
        data = cls.get_usage(user_id)
        
        # 检查是否需要重置（月度重置）
        current_month = cls._get_reset_date()
        if data.get("reset_date") != current_month:
            data = {
                "count": 0,
                "is_pro": data.get("is_pro", False),
                "reset_date": current_month
            }
        
        # Pro用户无限次
        if data.get("is_pro"):
            data["count"] += 1
            _usage_store[key] = data
            return True, data
        
        # 检查免费次数
        if data.get("count", 0) >= cls.FREE_LIMIT:
            return False, data
        
        # 增加使用次数
        data["count"] += 1
        _usage_store[key] = data
        return True, data
    
    @classmethod
    def activate_pro(cls, user_id: Optional[str] = None) -> bool:
        """激活Pro会员"""
        key = cls._get_user_key(user_id)
        data = cls.get_usage(user_id)
        data["is_pro"] = True
        _usage_store[key] = data
        return True
    
    @classmethod
    def get_remaining(cls, user_id: Optional[str] = None) -> dict:
        """获取剩余次数"""
        data = cls.get_usage(user_id)
        if data.get("is_pro"):
            return {
                "free_remaining": -1,  # 无限
                "is_pro": True,
                "usage_limit": -1
            }
        
        used = data.get("count", 0)
        remaining = max(0, cls.FREE_LIMIT - used)
        
        return {
            "free_remaining": remaining,
            "is_pro": False,
            "usage_limit": cls.FREE_LIMIT
        }
