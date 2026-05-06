"""
InterviewKoi - AI Interview Assistant
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os

from app.routers import interview, user

# 创建FastAPI应用
app = FastAPI(
    title="面试锦鲤 InterviewKoi",
    description="AI驱动的智能面试助手，输入岗位和简历，AI帮你准备面试答案、模拟面试、预测考题",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(interview.router)
app.include_router(user.router)


@app.get("/", response_class=HTMLResponse)
async def root():
    """首页"""
    static_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    return HTMLResponse(content="""
    <html>
        <head><title>面试锦鲤</title></head>
        <body>
            <h1>🐟 面试锦鲤</h1>
            <p>每场面试，都如鱼得水</p>
            <p>请访问 <a href="/static/index.html">前端页面</a></p>
        </body>
    </html>
    """)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "InterviewKoi"}


@app.get("/api/info")
async def api_info():
    """API信息"""
    return {
        "name": "面试锦鲤 InterviewKoi",
        "version": "1.0.0",
        "description": "AI驱动的智能面试助手",
        "endpoints": {
            "predict": "/api/interview/predict",
            "answer": "/api/interview/answer",
            "simulate": "/api/interview/simulate",
            "usage": "/api/interview/usage",
            "upgrade": "/api/interview/upgrade/pro"
        }
    }


# 挂载静态文件目录
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
