# ============================================
# SM-AI Backend Configuration
# ============================================

import os
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드 (루트 디렉토리의 .env 파일 사용)
root_dir = Path(__file__).parent.parent.parent  # sm-ai/ 루트
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

# ============================================
# API Keys
# ============================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# ============================================
# LangSmith 설정
# ============================================

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "SM-AI")

# ============================================
# LLM 모델 설정
# ============================================

AVAILABLE_MODELS = [
    "gpt-4.1",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
]

DEFAULT_MODEL = "gpt-4.1"
DEFAULT_TEMPERATURE = 0.0

# ============================================
# RAG 설정
# ============================================

RAG_CHUNK_SIZE = 1000
RAG_CHUNK_OVERLAP = 50

# ============================================
# 경로 설정
# ============================================

CACHE_DIR = ".cache"
FILES_DIR = os.path.join(CACHE_DIR, "files")
EMBEDDINGS_DIR = os.path.join(CACHE_DIR, "embeddings")

PROMPTS_DIR = "/prompts"
CHATBOT_PROMPTS_DIR = os.path.join(PROMPTS_DIR, "chatbot")
RAG_PROMPTS_DIR = os.path.join(PROMPTS_DIR, "rag")

# ============================================
# API 설정
# ============================================

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# CORS 허용 도메인
CORS_ORIGINS = [
    "http://localhost:8501",  # Streamlit 기본 포트
    "http://localhost:3000",  # React 개발 서버 (향후)
]
