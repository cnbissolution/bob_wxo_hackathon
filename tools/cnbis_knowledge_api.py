from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="C&bis Knowledge Base API",
    description="해커톤용 C&bis 사내 지식 검색 및 RAG 시뮬레이션 API",
    version="1.0.0"
)

# 1. 내장된 Mock 지식 데이터베이스
KNOWLEDGE_BASE = [
    {
        "id": "kb_aspice",
        "category": "ASPICE",
        "title": "ASPICE CL2/CL3 컨설팅 가이드라인",
        "content": "씨엔비스(C&bis)는 Automotive SPICE(ASPICE) 프로세스 모델에 따른 자동차 소프트웨어 개발 프로세스 심사 및 컨설팅 서비스를 제공합니다. 갭 분석부터 프로세스 내재화, 최종 심사 대응까지 전 과정을 지원하여 품질 표준 인증을 보장합니다."
    },
    {
        "id": "kb_doors",
        "category": "ALM",
        "title": "IBM DOORS Next 요구사항 관리 구축 사례",
        "content": "엔지니어링 시스템 솔루션 전문 기업으로서 IBM DOORS Next 기반의 복잡한 요구사항 추적성(Traceability) 확보 및 리뷰 프로세스 자동화를 성공적으로 구축했습니다. 이를 통해 개발 리드타임을 단축하고 리스크를 최소화합니다."
    },
    {
        "id": "kb_rotem",
        "category": "Project",
        "title": "현대로템 라이선스 복원 및 시스템 재구축 프로젝트",
        "content": "현대로템 RNE1606 프로젝트를 통해 기존 DOORS 시스템의 라이선스 복원 및 엔지니어링 인프라 재구축 작업을 성공적으로 수행했습니다. 단기간에 안정적인 개발 환경을 복구하여 프로젝트 연속성을 확보한 대표적 성공 사례입니다."
    },
    {
        "id": "kb_codebeamer",
        "category": "MBSE",
        "title": "PTC codeBeamer 커스터마이징 및 AI 통합",
        "content": "PTC codeBeamer 솔루션의 고급 설정 및 커스터마이징 역량을 바탕으로 시스템 엔지니어링 개발 환경 최적화를 지원합니다. 최근 AI 모델 통합을 통한 하이브리드 MBSE 환경 구현 기술을 선도하고 있습니다."
    }
]

# 2. 데이터 구조 정의
class SearchResult(BaseModel):
    id: str
    category: str
    title: str
    content: str

class RAGResponse(BaseModel):
    query: str
    found: bool
    references: List[SearchResult]
    summary: str

# 3. Bob(Agent)이 호출할 지식 검색 엔드포인트
@app.get("/search", response_model=RAGResponse, summary="사내 지식베이스 검색 및 RAG 요약")
def search_knowledge(
    query: str = Query(..., description="검색할 키워드 (예: ASPICE, 현대로템, DOORS)")
) -> RAGResponse:
    matched_docs = []

    # 간단한 키워드 매칭 로직 (RAG의 검색 단계 시뮬레이션)
    for doc in KNOWLEDGE_BASE:
        if (
            query.lower() in doc["content"].lower()
            or query.lower() in doc["title"].lower()
            or query.lower() in doc["category"].lower()
        ):
            matched_docs.append(SearchResult(**doc))

    if matched_docs:
        # 검색된 문서를 기반으로 한 답변 생성 (RAG의 생성 단계 시뮬레이션)
        ref_titles = ", ".join([d.title for d in matched_docs])
        summary_text = (
            f"[참조문서: {ref_titles}] 문의하신 내용과 관련하여, 씨엔비스는 관련 레퍼런스와 "
            f"고도화된 컨설팅 역량을 보유하고 있습니다. 상세 내용은 다음과 같습니다: "
            + " ".join([d.content for d in matched_docs])
        )
        return RAGResponse(query=query, found=True, references=matched_docs, summary=summary_text)

    # 매칭되는 데이터가 없을 때의 기본 답변
    fallback_text = (
        f"'{query}'에 대한 구체적인 내부 문서는 발견되지 않았습니다. "
        "하지만 씨엔비스는 ALM, PLM, MBSE 전반의 전문 엔지니어링 그룹이므로, "
        "상세 사항은 전문 컨설턴트와의 미팅을 통해 해결책을 제시해 드릴 수 있습니다."
    )
    return RAGResponse(query=query, found=False, references=[], summary=fallback_text)
