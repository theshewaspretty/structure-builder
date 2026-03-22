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
    # os.getenv를 통해 .env 파일의 값을 안전하게 주입합니다.
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
    id: str = Field(..., description="에이전트 노드의 고유 ID")
    label: str = Field(..., description="사용자가 지정한 에이전트 이름")

class Edge(BaseModel):
    from_node: str = Field(..., alias="from", description="출발지 노드 ID")
    to_node: str = Field(..., alias="to", description="도착지 노드 ID")
    
    class Config:
        populate_by_name = True

class FlowData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class ExportResponse(BaseModel):
    markdown: str

# --- 4. 시스템 프롬프트 ---
AGENT_MISSION = """
당신은 시스템 아키텍처와 데이터 플로우를 분석하여 구조화된 마크다운(.md) 문서를 생성하는 엘리트 Software Architecture Agent입니다.

[임무]
1. 사용자가 제공하는 노드(Nodes)와 연결선(Edges)의 JSON 위상 데이터를 분석하십시오.
2. 데이터의 흐름과 1:N 분기 처리 로직을 완벽하게 이해하십시오.
3. 'Workflow Architecture Diagram' 이라는 제목 아래에 매우 정교하고 직관적인 **ASCII Art Flow 다이어그램**을 반드시 포함해야 합니다.
4. ASCII 다이어그램은 단순한 수직 나열이 아닌, 여러 갈래로 뻗어나가는 복잡한 분기를 ┌, ┐, └, ┘, ├, ┤, │, ─, ▼ 등의 문자를 활용하여 정확하게 렌더링해야 합니다.
5. 다른 AI 에이전트나 개발자가 이 문서만 보고도 시스템 구조를 100% 재현할 수 있도록 논리적으로 작성하십시오.
"""

# --- 5. API 엔드포인트 ---
@app.post("/api/export-md", response_model=ExportResponse)
async def generate_architecture_documentation(data: FlowData):
    logger.info(f"📥 데이터 수신: 노드 {len(data.nodes)}개, 연결선 {len(data.edges)}개.")

    nodes_dict = [node.model_dump() for node in data.nodes]
    edges_dict = [edge.model_dump(by_alias=True) for edge in data.edges]

    user_content = f"""
    다음은 UI 캔버스에서 구성된 Agent 워크플로우의 JSON 데이터입니다.
    이를 바탕으로 완벽한 ASCII 아키텍처 다이어그램이 포함된 문서를 생성해 주십시오.

    [Input Flow Topology JSON]
    Nodes:
    {json.dumps(nodes_dict, ensure_ascii=False, indent=2)}

    Edges:
    {json.dumps(edges_dict, ensure_ascii=False, indent=2)}
    """

    # .env에서 모델 ID를 동적으로 가져옵니다.
    model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

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
        generated_md = response_body.get('content')[0].get('text')
        
        logger.info(f"✅ Bedrock 문서 생성 완료 (사용 모델: {model_id}).")
        return ExportResponse(markdown=generated_md)

    except bedrock_client.exceptions.AccessDeniedException:
        logger.error("❌ AWS Bedrock 접근 권한이 없습니다.")
        raise HTTPException(status_code=403, detail="AWS Access Denied. IAM 권한과 키를 확인하세요.")
    except Exception as e:
        logger.error(f"❌ Bedrock 호출 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
