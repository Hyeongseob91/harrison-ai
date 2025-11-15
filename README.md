# SM-AI (Soundmind AI System)

LangChain과 OpenAI를 활용한 AI 솔루션 플랫폼

## 📁 프로젝트 구조

```
sm-ai/
├── backend/                 # FastAPI 백엔드 서버
│   ├── app/                # API 애플리케이션
│   ├── prompts/            # 프롬프트 파일
│   ├── .cache/             # 캐시 및 업로드 파일
│   ├── pyproject.toml      # Backend 의존성
│   └── README.md           # Backend 가이드
│
├── frontend/               # Streamlit 프론트엔드
│   ├── pages/              # Streamlit 페이지
│   ├── images/             # 로고 이미지
│   ├── api_client.py       # Backend API 클라이언트
│   └── README.md           # Frontend 가이드
│
├── legacy/                 # 기존 코드 보관 (참고용)
│   ├── main.py
│   ├── pages/
│   ├── images/
│   ├── prompts_chatbot/
│   └── prompts_rag/
│
├── .env                    # 환경 변수 (Backend와 공유)
├── .gitignore              # Git 제외 파일
├── LICENSE                 # MIT 라이선스
└── README.md               # 이 파일
```

## 🏗️ 아키텍처

### Before (Monolithic)
```
Streamlit App
  ↓
LangChain (직접 호출)
  ↓
OpenAI API
```

### After (Microservices)
```
Streamlit Frontend → FastAPI Backend → LangChain → OpenAI API
  (Port: 8501)         (Port: 8000)
```

## 🚀 빠른 시작

### 1. Backend 서버 실행

```bash
cd backend
poetry install
poetry run python -m app.main
```

서버 확인:
- API: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 2. Frontend 실행

```bash
cd frontend
streamlit run app.py
```

프론트엔드 확인:
- Streamlit: http://localhost:8501

## 📚 주요 기능

### AI Chatbot
- 대화형 AI 챗봇
- 프롬프트 커스터마이징
- 역할 설정
- 다양한 LLM 모델 선택
- 실시간 스트리밍 응답

### RAG System
- PDF 파일 업로드
- 문서 기반 질의응답
- FAISS 벡터 검색
- 실시간 스트리밍 응답

## 🔧 기술 스택

### Backend
- **FastAPI**: REST API 프레임워크
- **LangChain**: LLM 애플리케이션 개발
- **OpenAI**: GPT 모델 API
- **FAISS**: 벡터 유사도 검색
- **Uvicorn**: ASGI 서버

### Frontend
- **Streamlit**: 웹 UI 프레임워크
- **Requests**: HTTP 클라이언트

## 📖 상세 가이드

- [Backend README](./backend/README.md) - Backend API 개발 가이드
- [Frontend README](./frontend/README.md) - Frontend 개발 가이드

## 📂 Legacy 폴더

`legacy/` 폴더에는 리팩토링 이전의 Monolithic 구조 코드가 보관되어 있습니다.
참고용으로만 사용하고, 실제 개발은 `backend/`와 `frontend/`를 사용하세요.

## 🔄 마이그레이션 진행 상태

- ✅ Backend API 구조 완성
- ✅ Chatbot API 구현
- ✅ RAG API 구현
- ✅ API 클라이언트 구현
- ⏳ Frontend 페이지 리팩토링 (진행 예정)
- ⏳ 통합 테스트

## 📝 환경 변수

프로젝트 **루트**에 `.env` 파일을 생성하세요 (Backend에서 자동으로 참조):

```env
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=sm-ai-backend
```

**참고**: Backend의 `config.py`가 자동으로 루트의 `.env`를 찾아서 로드합니다.

## 🤝 Contributing

TBD

## 📄 License

MIT License - [LICENSE](./LICENSE)

## 🔗 Links

- [Soundmind](https://soundmind.life)
