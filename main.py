
# main.py
import json
import logging
import os
from typing import List

import boto3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# --- 환경 변수 로드 (.env) ---
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentArchitect")

app = FastAPI(title="AI Agent Builder Backend PoC")

# --- 1. CORS 설정 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. AWS Bedrock 클라이언트 설정 (.env 적용) ---
try:
    bedrock_client = boto3.client(
        service_name='bedrock-runtime', 
        region_name=os.getenv("AWS_REGION", "ap-northeast-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    logger.info("✅ AWS Bedrock 클라이언트 초기화 완료 (.env 적용).")
except Exception as e:
    logger.error(f"❌ Bedrock 클라이언트 초기화 실패: {e}")

# --- 3. 데이터 모델 ---
class Node(BaseModel):
    id: str = Field(..., description="에이전트 고유 ID")
    label: str = Field(..., description="에이전트 이름")
    tools: List[str] = Field(default_factory=list, description="할당된 MCP 도구 목록") # 도구 속성 추가

class Edge(BaseModel):
    from_node: str = Field(..., alias="from")
    to_node: str = Field(..., alias="to")
    class Config:
        populate_by_name = True

class FlowData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class ExportResponse(BaseModel):
    markdown: str  # 프론트엔드가 파일로 저장할 단일 Markdown 문자열

# --- 4. 시스템 프롬프트 (명령어 자체 내장) ---
AGENT_MISSION = """
당신은 시스템 아키텍처와 데이터 플로우를 분석하여 구조화된 마크다운(.md) 문서를 생성하는 엘리트 Software Architecture Agent입니다.

[핵심 임무]
1. 사용자가 제공하는 노드(Nodes)와 연결선(Edges) 데이터를 분석하여 아키텍처 문서를 작성하십시오. 노드에 MCP tools가 할당되어 있다면, 해당 에이전트가 어떤 도구를 사용하는지도 명시하십시오.
2. 데이터의 흐름과 1:N 분기 처리 로직을 이해하여 직관적인 **ASCII Art Flow 다이어그램**을 그리십시오.
3. 분석된 아키텍처를 바탕으로 실제 프로젝트의 **폴더 및 파일 구조 트리(ASCII 형태)**를 문서 내에 포함하십시오.
   - 폴더 트리 구조 규칙:
     - Agent/
       - Agent_groups/ (Start, End를 제외한 실제 에이전트 .py 파일)
       - Agent_instructions/ (모든 노드의 .txt 페르소나 파일)
       - main.py
4. **[가장 중요한 임무] 문서의 맨 마지막 섹션에**, 위에서 정의한 폴더와 파일을 사용자의 로컬 OS 환경에서 한 번에 생성할 수 있는 CLI 명령어를 **코드 블록(Code block)** 형태로 반드시 포함하십시오.
   - Windows (PowerShell) 환경을 위한 명령어 (예: New-Item 사용)
   - macOS / Linux (Bash) 환경을 위한 명령어 (예: mkdir, touch 사용)

출력은 어떠한 JSON 래핑 없이 **오직 순수한 Markdown 텍스트**로만 응답하십시오.
"""

# --- 5. API 엔드포인트 ---
@app.post("/api/export-md", response_model=ExportResponse)
async def generate_architecture_documentation(data: FlowData):
    logger.info(f"📥 데이터 수신: 노드 {len(data.nodes)}개, 연결선 {len(data.edges)}개.")

    nodes_dict = [node.model_dump() for node in data.nodes]
    edges_dict = [edge.model_dump(by_alias=True) for edge in data.edges]

    user_content = f"""
    다음은 UI 캔버스에서 구성된 Agent 워크플로우의 JSON 데이터입니다.
    이 데이터를 기반으로 아키텍처 다이어그램, 폴더 구조 트리, 그리고 파일 자동 생성 OS 커맨드를 모두 포함하는 하나의 마크다운 문서를 작성해주세요.

    [Input Flow Topology JSON]
    Nodes:
    {json.dumps(nodes_dict, ensure_ascii=False, indent=2)}

    Edges:
    {json.dumps(edges_dict, ensure_ascii=False, indent=2)}
    """

    model_id = os.getenv("BEDROCK_MODEL_ID")

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0.1,  
        "system": AGENT_MISSION,
        "messages": [
            {"role": "user", "content": user_content}
        ]
    })

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id, 
            body=body,
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get('body').read())
        # 순수 마크다운 텍스트 결과만 추출
        generated_md = response_body.get('content')[0].get('text')
        
        logger.info(f"✅ Bedrock 문서 생성 완료 (사용 모델: {model_id}).")
        
        # 단일 마크다운 문자열 반환 (프론트엔드에서 바로 .md 로 저장됨)
        return ExportResponse(markdown=generated_md)

    except Exception as e:
        logger.error(f"❌ Bedrock 호출 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
