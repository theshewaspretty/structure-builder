# 🛠️ AI Agent Workflow Builder (Canvas)

This project is a No-code based AI Agent Architecture Canvas, implemented using pure HTML, CSS, and Vanilla JavaScript without relying on complex frameworks (such as React Flow). It was created to reflect the needs of field departments—such as those in manufacturing companies—where categorizing raw data is complex or adopting AI agents is difficult.

Users can freely place and connect agent nodes in a web browser to design workflows. The ultimate goal is to automatically generate structured Markdown (`.md`) and ASCII architecture documents via AI (AWS Bedrock) based on the designed diagram, formatted in a way that AI can most accurately interpret and understand.

## ✨ Key Features

* **Infinite Canvas Support:** Work freely without screen constraints, scrolling across a vast canvas of 4000px or more.
* **Intuitive Node Creation:** Instantly create agent boxes at desired locations using simple shortcuts and mouse clicks.
* **Inline Text Editing:** Double-click a box to immediately edit the agent's name or role.
* **1:N Multiple Connections (Routing):** Supports orthogonal routing (Manhattan Routing) style SVG lines, easily drawing branched flows from a single Out-port to multiple In-ports.
* **Safe Deletion Guard:** Supports a shortcut-based deletion mode (with visual hover effects). When a node is deleted, its connected orphan edges are automatically cleaned up. Core nodes (Start, End) are protected from deletion.

## 🚀 How to Use

No separate `npm install` or build process is required.

1.  Download the `index.html`, `main.py` file.
2.  Open the file in a modern web browser like Chrome, Safari, or Edge.
3.  Draw your diagram according to the controls below.
4.  create `.env` include with boto3's bedrock token,region.
5.  install packages
```
pip install requirements.txt
```
6.  excute `main.py` with command 
```
uvicorn main:app --reload --port 8000
```

### ⌨️ Shortcuts & Control Guide

| Action | Control Method | Description |
| :--- | :--- | :--- |
| **Create Node** | `Ctrl` (or Mac `Cmd ⌘`) + Click empty space | Creates a new agent box at the clicked location. |
| **Rename** | Double-click node | Enters text editing mode. Press `Enter` or click the background to save. |
| **Move Node** | Drag and drop node | Freely moves the node within the screen. Connected lines follow in real-time. |
| **Connect Line** | Drag from bottom dot (Out) ➔ top dot (In) | Drags the mouse from the source node's bottom port to the target node's top port to connect a line. |
| **Delete Element** | `Ctrl` (or Mac `Cmd ⌘`) + Click node/line | Activates deletion mode (target turns red), and deletes the element with a confirmation prompt upon clicking. |

## 🏗️ Architecture & Tech Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
* **Rendering:** DOM Elements (Nodes), SVG `<path>` (Edges)
* **Backend (Planned):** Python FastAPI
* **AI Engine (Planned):** AWS Bedrock (Claude 3 Sonnet)

## 🔜 Roadmap

- [x] Implement Vanilla JS-based drag-and-drop canvas engine
- [x] Apply SVG orthogonal routing algorithm and node dependency management logic
- [x] UX improvements (shortcut deletion, inline editing, canvas expansion, etc.)
- [ ] **Python FastAPI server integration (In Progress):** Send on-screen JSON state (`nodes`, `edges`) to the backend
- [ ] **AWS Bedrock pipeline construction:** Parse JSON to automatically generate an `architecture.md` document including ASCII diagrams


## Result_example
~~~
# Workflow Architecture Document

---

## 1. Overview

본 문서는 UI 캔버스에서 구성된 Agent 워크플로우의 위상(Topology) 데이터를 분석하여, 시스템 구조를 완벽하게 재현할 수 있도록 작성된 아키텍처 문서입니다.

---

## 2. Workflow Architecture Diagram

```
                    ┌─────────────────┐
                    │   Start_node    │
                    └────────┬────────┘
                             │
               ┌─────────────┴─────────────┐
               │                           │
               ▼                           ▼
     ┌──────────────────┐       ┌──────────────────┐
     │    [Agent 1]     │       │    [Agent 3]     │
     └────────┬─────────┘       └────────┬─────────┘
              │                          │
              └──────────┬───────────────┘
                         │
                         ▼
               ┌──────────────────┐
               │    [Agent 2]     │
               └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │    End_node      │
               └──────────────────┘
```

---

## 3. Node Definitions (노드 정의)

| Node ID      | Label       | Type      | 설명                                      |
|--------------|-------------|-----------|-------------------------------------------|
| `start_node` | Start_node  | 시작 노드  | 워크플로우의 진입점. 두 개의 병렬 분기를 트리거 |
| `node_1`     | [Agent 1]   | 에이전트   | Start_node로부터 분기된 첫 번째 처리 에이전트 |
| `node_3`     | [Agent 3]   | 에이전트   | Start_node로부터 분기된 두 번째 처리 에이전트 |
| `node_2`     | [Agent 2]   | 에이전트   | Agent 1과 Agent 3의 결과를 수렴하는 합류 에이전트 |
| `end_node`   | End_node    | 종료 노드  | 워크플로우의 최종 종료점                    |

---

## 4. Edge Definitions (연결선 정의)

| Edge # | From         | To           | 설명                                  |
|--------|--------------|--------------|---------------------------------------|
| E-01   | `start_node` | `node_1`     | 시작 → Agent 1 (병렬 분기 #1)          |
| E-02   | `start_node` | `node_3`     | 시작 → Agent 3 (병렬 분기 #2)          |
| E-03   | `node_1`     | `node_2`     | Agent 1 → Agent 2 (합류 입력 #1)      |
| E-04   | `node_3`     | `node_2`     | Agent 3 → Agent 2 (합류 입력 #2)      |
| E-05   | `node_2`     | `end_node`   | Agent 2 → 종료 (최종 출력)             |

---

## 5. Data Flow Analysis (데이터 흐름 분석)

### 5-1. 실행 단계 (Execution Phases)

```
Phase 1 │ [Start_node] 실행 → 두 개의 하위 에이전트로 동시 분기
────────┼──────────────────────────────────────────────────────────
Phase 2 │ [Agent 1] 과 [Agent 3] 병렬(Parallel) 실행
────────┼──────────────────────────────────────────────────────────
Phase 3 │ [Agent 2] 에서 두 에이전트의 결과 수렴(Merge/Join)
────────┼──────────────────────────────────────────────────────────
Phase 4 │ [End_node] 에서 워크플로우 종료
```

### 5-2. 분기 패턴 (Branching Pattern)

- **패턴 유형**: `Fork → Join` (분기 후 합류)
- **분기 지점 (Fork Point)**: `Start_node` → 1:2 분기
- **합류 지점 (Join Point)**: `node_2 (Agent 2)` ← 2:1 합류
- **병렬 처리 경로**:
  - **Path A**: `Start_node` → `[Agent 1]` → `[Agent 2]`
  - **Path B**: `Start_node` → `[Agent 3]` → `[Agent 2]`

### 5-3. 의존성 그래프 (Dependency Graph)

```
Start_node  (선행 조건 없음)
├── [Agent 1]  depends on → Start_node
├── [Agent 3]  depends on → Start_node
└── [Agent 2]  depends on → [Agent 1] AND [Agent 3]
        └── End_node  depends on → [Agent 2]
```

---

## 6. Critical Path (임계 경로)

> 워크플로우의 전체 실행 시간을 결정하는 가장 긴 경로입니다.

```
Start_node ──▶ [Agent 1 or Agent 3 중 더 느린 쪽] ──▶ [Agent 2] ──▶ End_node
```

- Agent 1과 Agent 3은 **병렬 실행**되므로, 둘 중 **처리 시간이 더 긴 에이전트**가 전체 임계 경로를 결정합니다.
- Agent 2는 반드시 **두 에이전트가 모두 완료된 후** 실행되어야 합니다. (동기화 장벽, Synchronization Barrier)

---

## 7. Architectural Notes (아키텍처 주의사항)

| # | 항목 | 내용 |
|---|------|------|
| 1 | **병렬성** | Agent 1과 Agent 3은 독립적으로 실행 가능하며, 상호 의존성이 없습니다. |
| 2 | **합류 조건** | Agent 2는 Agent 1과 Agent 3이 **모두 성공적으로 완료**되어야 실행됩니다. |
| 3 | **단일 장애점** | Agent 2와 End_node는 단일 경로로, 해당 노드 실패 시 전체 워크플로우가 중단됩니다. |
| 4 | **확장 가능성** | Start_node의 분기를 추가하여 N개의 병렬 에이전트로 수평 확장이 가능합니다. |

---

*본 문서는 JSON Topology 데이터를 기반으로 자동 생성되었습니다.*

~~~
