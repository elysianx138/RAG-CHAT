"""
文件名：app/main.py
最后修改时间：2026-04-16
模块功能：项目启动入口，创建 FastAPI 应用并挂载聊天、上传和文档管理接口。
模块相关技术：FastAPI、Uvicorn、Lifespan、健康检查接口。
"""

from contextlib import asynccontextmanager
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI

from api.chat_routers import router as chat_router
from api.ingest_routers import router as ingest_router
from app.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.validate_runtime()
    yield


app = FastAPI(title=settings.APP_NAME, version="0.2.1", lifespan=lifespan)

app.include_router(chat_router)
app.include_router(ingest_router)


@app.get("/")
def index():
    return {
        "message": "中文 RAG Chat 服务正在运行。",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": settings.runtime_mode(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
