# ============================================
# SM-AI Backend - FastAPI Application
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS, API_PREFIX
import os

# FastAPI 앱 생성
app = FastAPI(
    title="SM-AI Backend",
    description="Soundmind AI System Backend API",
    version="0.1.0"
)

# ============================================
# CORS 설정
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 라우터 등록
# ============================================

from app.chat_api import router as chat_router
from app.rag_api import router as rag_router

app.include_router(chat_router, prefix=f"{API_PREFIX}/chat", tags=["chat"])
app.include_router(rag_router, prefix=f"{API_PREFIX}/rag", tags=["rag"])

# ============================================
# 기본 엔드포인트
# ============================================

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "SM-AI Backend API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

# ============================================
# 서버 실행 (개발용)
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True  # 개발 시 자동 리로드
    )
