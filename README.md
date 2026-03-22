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

1.  Download the `index.html` file.
2.  Open the file in a modern web browser like Chrome, Safari, or Edge.
3.  Draw your diagram according to the controls below.

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
