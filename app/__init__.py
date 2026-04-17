from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.api import media, tags, categories
from app.db.session import init_db
from app.config import settings


def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    print(f"✓ 媒体目录：{settings.MEDIA_DIR}")
    print(f"✓ 上传目录：{settings.UPLOAD_DIR}")


# 确保必要的目录存在
ensure_directories()

# 初始化数据库
init_db()

# 创建FastAPI应用
app = FastAPI(
    title="Media Management API",
    description="API for managing media files and tags",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(tags.router, prefix="/api/tags", tags=["tags"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Media Management API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )