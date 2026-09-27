> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Scheduler, API server, run configs

**In one sentence:** LiveBench run scheduling is configured by `default_config.json` date/agent/economic settings while `api/server.py` serves all agent data over REST plus WebSocket, and the `scheduler/` package itself is currently an empty placeholder.

## Key points

- The `scheduler/` package contains only an empty `scheduler/__init__.py` (0 lines), so no scheduling logic lives there yet (`scheduler/__init__.py:1`).
- The API server is a FastAPI app defined as `app = FastAPI(title="LiveBench API", version="1.0.0")` in `api/server.py:23`.
- Run date range, economics, agents, and data paths are all set in `configs/default_config.json`, e.g. `init_date: 2025-01-20` through `end_date: 2025-01-31` (`configs/default_config.json:3-6`).
- Agent task data is served authoritatively from per-agent `task_completions.jsonl`, merged with `tasks.jsonl` metadata and `evaluations.jsonl` scores (`api/server.py:311-316`).
- Real-time frontend updates flow through the `/ws` WebSocket, the `ConnectionManager.broadcast()` fan-out, and the `watch_agent_files()` polling loop (`api/server.py:713-714`, `api/server.py:167-173`, `api/server.py:748-804`).
- Economic/token accounting uses `initial_balance: 1000.0` plus `input_per_1m: 2.5 / output_per_1m: 10.0` pricing from the run config (`configs/default_config.json:8-13`).

---

## Scheduler package

The scheduler directory holds a single empty file (`scheduler/__init__.py:1`):

```
(empty file, 0 lines)
```

There are no classes, functions, or scheduling routines in `scheduler/` at this snapshot. Any date-looping or per-day task assignment behavior is therefore driven by configuration (see below) and by external runner code, not by this package.

## API server application

The server module docstring in `api/server.py:1-8` states its purpose verbatim:

```
"""
LiveBench API Server - Real-time updates and data access for frontend

This FastAPI server provides:
- WebSocket endpoint for live agent activity streaming
- REST endpoints for agent data, tasks, and economic metrics
- Real-time updates as agents work and learn
"""
```

App construction and CORS setup are verbatim (`api/server.py:23-32`):

```python
app = FastAPI(title="LiveBench API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Key data-source constants (`api/server.py:35-39`):

```python
DATA_PATH = Path(__file__).parent.parent / "data" / "agent_data"
HIDDEN_AGENTS_PATH = Path(__file__).parent.parent / "data" / "hidden_agents.json"
_TASK_VALUES_PATH = Path(__file__).parent.parent.parent / "scripts" / "task_value_estimates" / "task_values.jsonl"
```

Pydantic request/response models (`api/server.py:118-152`):

```python
class AgentStatus(BaseModel):
    """Agent status model"""
    signature: str
    balance: float
    net_worth: float
    survival_status: str
    current_activity: Optional[str] = None
    current_date: Optional[str] = None
```

```python
class WorkTask(BaseModel):
    """Work task model"""
    task_id: str
    sector: str
    occupation: str
    prompt: str
    date: str
    status: str = "assigned"
```

```python
class EconomicMetrics(BaseModel):
    """Economic metrics model"""
    balance: float
    total_token_cost: float
    total_work_income: float
    net_worth: float
    dates: List[str]
    balance_history: List[float]
```

## REST endpoints

Root index (`api/server.py:179-193`) returns the endpoint map verbatim:

```python
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "LiveBench API",
        "version": "1.0.0",
        "endpoints": {
            "agents": "/api/agents",
            "agent_detail": "/api/agents/{signature}",
            "tasks": "/api/agents/{signature}/tasks",
            "learning": "/api/agents/{signature}/learning",
            "economic": "/api/agents/{signature}/economic",
            "websocket": "/ws"
        }
    }
```

Additional endpoints and their source lines:

- `GET /api/agents` lists agents from per-directory `economic/balance.jsonl` plus latest `decisions/decisions.jsonl` activity (`api/server.py:196-240`).
- `GET /api/agents/{signature}` returns current status, full `balance_history`, `decisions`, and evaluation scores, with task count from `task_completions.jsonl` (`api/server.py:243-308`).
- `GET /api/agents/{signature}/tasks` merges `work/tasks.jsonl` metadata with `economic/task_completions.jsonl` wall-clock/payment data and appends unattempted GDPVal pool tasks (`api/server.py:311-410`).
- `GET /api/agents/{signature}/terminal-log/{date}` serves `terminal_logs/{date}.log` content (`api/server.py:413-423`).
- `GET /api/agents/{signature}/learning` parses `memory/memory.jsonl` into `{topic, timestamp, date, content}` entries (`api/server.py:426-461`).
- `GET /api/agents/{signature}/economic` reduces `economic/balance.jsonl` to date/balance/token-cost/work-income series (`api/server.py:464-502`).
- `GET /api/leaderboard` aggregates balances, evaluation averages, stripped histories, and timestamp-sorted `wc_series`, sorted by `current_balance` descending (`api/server.py:505-608`).
- `GET /api/artifacts/random` samples up to `count` files with PDF/DOCX/XLSX/PPTX extensions from agent `sandbox/` trees (`api/server.py:611-660`).
- `GET /api/artifacts/file?path=...` serves one artifact with `..` rejection and `DATA_PATH`-containment check (`api/server.py:663-679`).
- `GET/PUT /api/settings/hidden-agents` and `GET /api/settings/displaying-names` persist frontend display settings to `data/hidden_agents.json` and `data/displaying_names.json` (`api/server.py:682-710`).
- `POST /api/broadcast` forwards a JSON body to all WebSocket clients (`api/server.py:736-743`).

## Real-time streaming

Connection manager (`api/server.py:156-176`):

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass
```

WebSocket handler (`api/server.py:713-733`) accepts at `/ws`, sends a `{"type": "connected", ...}` greeting, then echoes received text. The background watcher `watch_agent_files()` (`api/server.py:748-804`) polls every second (`api/server.py:804`) and broadcasts `balance_update` / `activity_update` messages on `balance.jsonl` / `decisions.jsonl` mtime changes; it is launched at startup (`api/server.py:807-810`):

```python
@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    asyncio.create_task(watch_agent_files())
```

Standalone launch (`api/server.py:813-815`):

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Run configuration

Full `configs/default_config.json` content, quoted verbatim (`configs/default_config.json:1-36`):

```json
{
  "livebench": {
    "date_range": {
      "init_date": "2025-01-20",
      "end_date": "2025-01-31"
    },
    "economic": {
      "initial_balance": 1000.0,
      "task_values_path": "./scripts/task_value_estimates/task_values.jsonl",
      "token_pricing": {
        "input_per_1m": 2.5,
        "output_per_1m": 10.0
      }
    },
    "agents": [
      {
        "signature": "gpt-4-agent",
        "basemodel": "gpt-4-turbo-preview",
        "enabled": true,
        "tasks_per_day": 1
      }
    ],
    "agent_params": {
      "max_steps": 20,
      "max_retries": 3,
      "base_delay": 0.5,
      "tasks_per_day": 1
    },
    "evaluation": {
      "use_llm_evaluation": true,
      "meta_prompts_dir": "./eval/meta_prompts"
    },
    "data_path": "./livebench/data/agent_data",
    "gdpval_path": "./gdpval"
  }
}
```

What each block controls:

- `date_range` (`configs/default_config.json:3-6`): 12-day simulated run from `2025-01-20` to `2025-01-31`.
- `economic` (`configs/default_config.json:7-14`): starting balance `1000.0`, task-value table path, and per-million-token input/output prices.
- `agents` (`configs/default_config.json:15-22`): single enabled `gpt-4-agent` on `gpt-4-turbo-preview` doing `1` task per day.
- `agent_params` (`configs/default_config.json:23-28`): `max_steps: 20`, `max_retries: 3`, `base_delay: 0.5`, `tasks_per_day: 1`.
- `evaluation` (`configs/default_config.json:29-32`): LLM-based evaluation on, prompts from `./eval/meta_prompts`.
- `data_path` / `gdpval_path` (`configs/default_config.json:33-34`): agent outputs under `./livebench/data/agent_data`, task pool under `./gdpval`.

**Covers:** component 04
