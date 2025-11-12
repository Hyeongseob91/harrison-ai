# ============================================
# Session Manager - 세션 관리
# ============================================

from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict

# ============================================
# 세션 저장소 (메모리 기반)
# ============================================

session_store: Dict[str, ChatMessageHistory] = {}

# ============================================
# 세션 관리 함수
# ============================================

def get_session_history(session_id: str) -> ChatMessageHistory:
    """
    세션 ID로 대화 히스토리 가져오기

    Args:
        session_id: 세션 ID

    Returns:
        ChatMessageHistory: 대화 히스토리 객체
    """
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


def clear_session(session_id: str) -> bool:
    """
    세션 초기화

    Args:
        session_id: 세션 ID

    Returns:
        bool: 성공 여부
    """
    if session_id in session_store:
        session_store[session_id].clear()
        return True
    return False


def get_all_sessions() -> list:
    """
    모든 세션 ID 목록 반환

    Returns:
        list: 세션 ID 리스트
    """
    return list(session_store.keys())


def session_exists(session_id: str) -> bool:
    """
    세션 존재 여부 확인

    Args:
        session_id: 세션 ID

    Returns:
        bool: 존재 여부
    """
    return session_id in session_store
