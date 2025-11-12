# ============================================
# RAG API - RAG System REST API
# ============================================

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
from app.chain_factory import create_rag_retriever, create_rag_chain, get_available_prompts
from app.config import FILES_DIR

router = APIRouter()

# ============================================
# 세션별 Retriever 저장소
# ============================================

retriever_store = {}

# ============================================
# 데이터 모델
# ============================================

class RAGQueryRequest(BaseModel):
    """RAG 질의 요청 모델"""
    session_id: str
    question: str
    model: str = "gpt-4o"
    prompt_file: str
    temperature: Optional[float] = 0.0


class RAGUploadResponse(BaseModel):
    """RAG 파일 업로드 응답 모델"""
    message: str
    filename: str
    session_id: str
    file_path: str


# ============================================
# API 엔드포인트
# ============================================

@router.post("/upload", response_model=RAGUploadResponse)
async def upload_pdf(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    PDF 파일 업로드 및 임베딩 처리

    업로드된 PDF 파일을 저장하고, 벡터 DB로 변환하여
    세션에 연결된 retriever를 생성합니다.
    """
    try:
        # 파일 확장자 확인
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        # 파일 저장 디렉토리 생성
        os.makedirs(FILES_DIR, exist_ok=True)

        # 파일 저장
        file_path = os.path.join(FILES_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Retriever 생성 (RAG 1~5단계)
        retriever = create_rag_retriever(file_path)

        # 세션에 저장
        retriever_store[session_id] = {
            "retriever": retriever,
            "filename": file.filename,
            "file_path": file_path
        }

        return RAGUploadResponse(
            message="File uploaded and processed successfully",
            filename=file.filename,
            session_id=session_id,
            file_path=file_path
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def rag_query(request: RAGQueryRequest):
    """
    RAG 기반 질의응답 (스트리밍)

    업로드된 문서를 바탕으로 사용자의 질문에 답변합니다.
    실시간 스트리밍 방식으로 응답을 반환합니다.
    """
    try:
        # Retriever 가져오기
        session_data = retriever_store.get(request.session_id)

        if not session_data:
            raise HTTPException(
                status_code=400,
                detail="No file uploaded for this session. Please upload a PDF file first."
            )

        retriever = session_data["retriever"]

        # Chain 생성 (RAG 6~8단계)
        chain = create_rag_chain(
            prompt_file=request.prompt_file,
            retriever=retriever,
            model=request.model,
            temperature=request.temperature
        )

        # 스트리밍 응답
        async def generate():
            try:
                async for chunk in chain.astream(request.question):
                    yield f"data: {json.dumps({'token': chunk})}\n\n"

                # 스트리밍 종료 신호
                yield "data: [DONE]\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prompts")
async def list_rag_prompts():
    """
    사용 가능한 RAG 프롬프트 파일 목록 조회
    """
    try:
        prompts = get_available_prompts("rag")
        return {"prompts": prompts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}/document")
async def get_session_document(session_id: str):
    """
    세션에 업로드된 문서 정보 조회
    """
    session_data = retriever_store.get(session_id)

    if not session_data:
        return {
            "session_id": session_id,
            "has_document": False,
            "filename": None
        }

    return {
        "session_id": session_id,
        "has_document": True,
        "filename": session_data["filename"],
        "file_path": session_data["file_path"]
    }


@router.delete("/session/{session_id}")
async def delete_rag_session(session_id: str):
    """
    RAG 세션 삭제 (retriever 제거)
    """
    if session_id in retriever_store:
        del retriever_store[session_id]
        return {"message": "RAG session deleted successfully", "session_id": session_id}
    else:
        return {"message": "RAG session not found", "session_id": session_id}
