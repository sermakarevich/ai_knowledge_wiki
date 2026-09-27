> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Dashboard: static data + web UI

**In one sentence:** The dashboard is a React web app (a user interface that runs in the browser) plus a Python script that pre-builds JSON data files so the same app can run live against an API server or as a static site on GitHub Pages.

## Key points

- The static generator `scripts/generate_static_data.py:89` (`gen_agents`), `:112` (`gen_leaderboard`), `:187` (`gen_agent_detail`), `:223` (`gen_agent_tasks`), `:297` (`gen_agent_learning`), `:319` (`gen_agent_economic`), `:346` (`gen_artifacts`), `:406` (`gen_settings`) mirrors the server API as JSON files under `frontend/public/data/` (`scripts/generate_static_data.py:13`).
- The frontend switches between live and static data sources with one flag, `VITE_STATIC_DATA`, read in `frontend/src/api.js:9`, with URL helpers `staticUrl`/`liveUrl` at `frontend/src/api.js:12-13`.
- The app shell `frontend/src/App.jsx:14` holds agent list, selected agent, hidden-agent set, and display names, polls `fetchAgentsData` every 5 seconds (`frontend/src/App.jsx:49`), and routes 6 views (`frontend/src/App.jsx:102-130`).
- Real-time updates use a WebSocket hook (a reusable live-connection function) `frontend/src/hooks/useWebSocket.js:4` that is disabled in static mode with status `github-pages` (`frontend/src/hooks/useWebSocket.js:6`), otherwise reconnects every 3 seconds (`frontend/src/hooks/useWebSocket.js:35`).
- The sidebar `frontend/src/components/Sidebar.jsx:6` provides 5 navigation links (`frontend/src/components/Sidebar.jsx:21-27`), an agent list with survival-status dots (`frontend/src/components/Sidebar.jsx:29-42`), and an agent-visibility settings panel (`frontend/src/components/Sidebar.jsx:123-170`).
- The Dashboard page `frontend/src/pages/Dashboard.jsx:8` shows metric cards, a balance chart, a domain-earnings chart split by a quality cutoff `QUALITY_CLIFF = 0.6` (`frontend/src/pages/Dashboard.jsx:127`), and recent decisions (`frontend/src/pages/Dashboard.jsx:380-396`).
- Work, learning, leaderboard, and artifact pages each map to one pre-generated JSON file per agent, with file previews for PDF/XLSX/DOCX/PPTX shared in `frontend/src/components/FilePreview.jsx:201-217` (`renderFilePreview`).

---

## Static data generator

Script entry: `scripts/generate_static_data.py:424` (`def main():`) runs in this order (`scripts/generate_static_data.py:428-441`):

```python
gen_agents()
gen_leaderboard()
gen_artifacts()
gen_settings()
```

then per agent:

```python
gen_agent_detail(agent_dir)
gen_agent_tasks(agent_dir)
gen_agent_learning(agent_dir)
gen_agent_economic(agent_dir)
gen_terminal_logs(agent_dir)
```

Input and output roots are fixed at the top of the file (`scripts/generate_static_data.py:11-14`):

```python
REPO_ROOT        = Path(__file__).parent.parent
DATA_PATH        = REPO_ROOT / "livebench" / "data" / "agent_data"
OUT_PATH         = REPO_ROOT / "frontend" / "public" / "data"
TASK_VALUES_PATH = REPO_ROOT / "scripts" / "task_value_estimates" / "task_values.jsonl"
```

What each generator writes:

- `gen_agents` (`scripts/generate_static_data.py:89`) reads `economic/balance.jsonl` and `decisions/decisions.jsonl` per agent directory (`scripts/generate_static_data.py:93-97`) and writes `agents.json` with `signature`, `balance`, `net_worth`, `survival_status`, `current_activity`, `current_date`, `total_token_cost` (`scripts/generate_static_data.py:99-107`).
- `gen_leaderboard` (`scripts/generate_static_data.py:112`) adds percent change vs initial balance (`scripts/generate_static_data.py:120-122`), average evaluation score (`scripts/generate_static_data.py:124-126`), a stripped balance history joined with wall-clock seconds per date (`scripts/generate_static_data.py:132-140`), and a `wc_series` list built from completions sorted by timestamp (`scripts/generate_static_data.py:150-165`), sorted by current balance descending (`scripts/generate_static_data.py:182`).
- `gen_agent_detail` (`scripts/generate_static_data.py:187`) writes `agents/{sig}.json` with `current_status`, full `balance_history`, `decisions`, and `evaluation_scores` (`scripts/generate_static_data.py:202-218`).
- `gen_agent_tasks` (`scripts/generate_static_data.py:223`) treats `economic/task_completions.jsonl` as authoritative (stated in the docstring at `scripts/generate_static_data.py:224-227`), merges metadata from `work/tasks.jsonl` (`scripts/generate_static_data.py:232-235`) and evaluations (`scripts/generate_static_data.py:238-242`), attaches `task_value_usd` (`scripts/generate_static_data.py:256-257`), then appends unattempted pool tasks so the UI can show untapped potential (`scripts/generate_static_data.py:281-291`).
- `gen_agent_learning` (`scripts/generate_static_data.py:297`) flattens `memory/memory.jsonl` into `{topic, timestamp, date, content}` entries plus one joined markdown string (`scripts/generate_static_data.py:302-315`).
- `gen_agent_economic` (`scripts/generate_static_data.py:319`) splits `balance.jsonl` rows into parallel `dates`, `balance_history`, `token_costs`, `work_income` arrays (`scripts/generate_static_data.py:323-327`).
- `gen_artifacts` (`scripts/generate_static_data.py:346`) walks each agent `sandbox/` date folder (`scripts/generate_static_data.py:355-357`), keeps only `.pdf`, `.docx`, `.xlsx`, `.pptx` (`scripts/generate_static_data.py:343`), skips `code_exec`, `videos`, `reference_files` (`scripts/generate_static_data.py:344`), copies files under `data/files/` (`scripts/generate_static_data.py:378-380`), and writes `artifacts.json` (`scripts/generate_static_data.py:382`).
- `gen_terminal_logs` (`scripts/generate_static_data.py:387`) converts each `terminal_logs/*.log` into `agents/{sig}/terminal-logs/{date}.json` with `{date, content}` (`scripts/generate_static_data.py:396-399`).
- `gen_settings` (`scripts/generate_static_data.py:406`) copies `hidden_agents.json` and `displaying_names.json` into `settings/hidden-agents.json` and `settings/displaying-names.json` (`scripts/generate_static_data.py:413-421`).

Shared helpers: `read_jsonl` tolerates missing files and skips bad JSON lines (`scripts/generate_static_data.py:36-48`), `write_json` creates parent folders and prints the relative path (`scripts/generate_static_data.py:51-55`), and `agent_dirs` lists sorted agent folders (`scripts/generate_static_data.py:58-61`).

## API abstraction: one flag, two backends

`frontend/src/api.js:1-7` explains the two modes: live mode talks to the FastAPI backend (a Python server that answers data requests) at `/api/...`, static mode reads pre-built JSON at `{BASE_URL}data/...`. The switch (`frontend/src/api.js:9-13`):

```js
const STATIC   = import.meta.env.VITE_STATIC_DATA === 'true'
const BASE_URL = import.meta.env.BASE_URL || '/'
const staticUrl = (path) => `${BASE_URL}data/${path}`
const liveUrl   = (path) => `/api/${path}`
```

Endpoint mapping (`frontend/src/api.js:19-50`): `fetchAgents` → `agents.json`, `fetchLeaderboard` → `leaderboard.json`, `fetchAgentDetail` → `agents/{sig}.json`, `fetchAgentEconomic` → `agents/{sig}/economic.json`, `fetchAgentTasks` → `agents/{sig}/tasks.json`, `fetchAgentLearning` → `agents/{sig}/learning.json`, `fetchHiddenAgents`/`fetchDisplayNames` → `settings/...`, `fetchArtifacts` → `artifacts.json` (static) vs `artifacts/random?count=30` (live), `fetchTerminalLog` → `agents/{sig}/terminal-logs/{date}.json`. Artifact file URLs resolve via `getArtifactFileUrl` (`frontend/src/api.js:53-56`), and `saveHiddenAgents` is a no-op in static mode because a static site cannot persist settings (`frontend/src/api.js:59-66`).

## App shell and routing

`frontend/src/main.jsx:6-10` mounts `App` inside `React.StrictMode`. `App` (`frontend/src/App.jsx:14`) keeps four pieces of state: `agents`, `selectedAgent`, `hiddenAgents` (a `Set`), and `displayNames` (`frontend/src/App.jsx:15-18`), auto-selects the first visible agent (`frontend/src/App.jsx:23-30`), and polls the agent list every 5 seconds (`frontend/src/App.jsx:47-51`).

Routes (`frontend/src/App.jsx:102-130`): `/` → `Leaderboard`, `/dashboard` → `Dashboard`, `/agent/:signature` → `AgentDetail`, `/artifacts` → `Artifacts`, `/work` → `WorkView`, `/learning` → `LearningView`. The layout is a flex row with `Sidebar` plus a scrollable `main` (`frontend/src/App.jsx:90-99`), wrapped in `DisplayNamesContext.Provider` (`frontend/src/App.jsx:88`) so any component can resolve a human-readable name via `useDisplayName()` (`frontend/src/DisplayNamesContext.jsx:14-17`).

## Real-time hook

`export const useWebSocket = () => {` (`frontend/src/hooks/useWebSocket.js:4`) returns `{ lastMessage, connectionStatus }` (`frontend/src/hooks/useWebSocket.js:46`). In static builds it returns immediately with status `github-pages` (`frontend/src/hooks/useWebSocket.js:6-11`); in live mode it opens `ws://<host>/ws` (`frontend/src/hooks/useWebSocket.js:15`), sets `connected`/`error`/`disconnected` (`frontend/src/hooks/useWebSocket.js:19-35`), parses each message as JSON (`frontend/src/hooks/useWebSocket.js:23-27`), and retries after 3 seconds on close (`frontend/src/hooks/useWebSocket.js:35`). `App` refreshes agents on `balance_update`/`activity_update` messages (`frontend/src/App.jsx:67-74`).

## Sidebar

`const Sidebar = ({ agents, allAgents, hiddenAgents, onUpdateHiddenAgents, selectedAgent, onSelectAgent, connectionStatus }) => {` (`frontend/src/components/Sidebar.jsx:6`). Navigation items are a fixed array of 5 entries (`frontend/src/components/Sidebar.jsx:21-27`): Leaderboard, Dashboard, Artifacts, Work Tasks, Learning. Status dots map `thriving/stable/struggling/bankrupt` to green/blue/yellow/red (`frontend/src/components/Sidebar.jsx:29-42`); connection status maps `connected/connecting/github-pages/disconnected/error` to colors and labels (`frontend/src/components/Sidebar.jsx:44-64`). The visibility panel stages changes in `pendingHidden` and only writes back on Apply (`frontend/src/components/Sidebar.jsx:66-84`).

## Pages

- Dashboard (`frontend/src/pages/Dashboard.jsx:8`) fetches detail, economic, and tasks for the selected agent (`frontend/src/pages/Dashboard.jsx:15-21`), renders 7 metric cards (`frontend/src/pages/Dashboard.jsx:182-233`), a balance `AreaChart` (`frontend/src/pages/Dashboard.jsx:270-305`), a stacked vertical `BarChart` of earned/failed/untapped per occupation (`frontend/src/pages/Dashboard.jsx:326-365`), and the last 5 decisions (`frontend/src/pages/Dashboard.jsx:380-396`).
- Leaderboard (`frontend/src/pages/Leaderboard.jsx:184`) polls every 10 seconds (`frontend/src/pages/Leaderboard.jsx:208`), draws a neon multi-agent wall-clock-hours line chart (`frontend/src/pages/Leaderboard.jsx:553-602`), a scrolling ticker (`frontend/src/pages/Leaderboard.jsx:86-125`), and a sortable dark table with pay-rate computed from `wc_series` (`frontend/src/pages/Leaderboard.jsx:256-272`, table at `frontend/src/pages/Leaderboard.jsx:647-798`).
- WorkView (`frontend/src/pages/WorkView.jsx:242`) paginates at `TASKS_PER_PAGE = 20` (`frontend/src/pages/WorkView.jsx:7`), sorts by date or score (`frontend/src/pages/WorkView.jsx:322-335`), shows a `QualityBadge` cliffed at `QUALITY_CLIFF = 0.6` (`frontend/src/pages/WorkView.jsx:8`, badge at `frontend/src/pages/WorkView.jsx:47-94`), artifact chips (`frontend/src/pages/WorkView.jsx:98-121`), and terminal-log modals via `fetchTerminalLog` (`frontend/src/pages/WorkView.jsx:173-238`).
- LearningView (`frontend/src/pages/LearningView.jsx:7`) polls every 5 seconds (`frontend/src/pages/LearningView.jsx:16`), renders entries as a timeline (`frontend/src/pages/LearningView.jsx:104-185`) with a detail modal (`frontend/src/pages/LearningView.jsx:189-238`).
- AgentDetail (`frontend/src/pages/AgentDetail.jsx:4-7`) is a thin wrapper that reads `:signature` from the URL and renders `Dashboard` for it.
- Artifacts (`frontend/src/pages/Artifacts.jsx:464`) filters by extension (`frontend/src/pages/Artifacts.jsx:9-15`, filtering at `frontend/src/pages/Artifacts.jsx:480`), shows cards with `formatBytes` sizes (`frontend/src/components/FilePreview.jsx:17-18`), and previews via the shared renderer.
- File previews (`frontend/src/components/FilePreview.jsx:10-15` `EXT_CONFIG`, `frontend/src/components/FilePreview.jsx:201-217` `renderFilePreview`): PDF via blob iframe (`frontend/src/components/FilePreview.jsx:33-51`), XLSX parsed in-browser with sheet tabs capped at 500 rows (`frontend/src/components/FilePreview.jsx:55-121`), DOCX via `docx-preview` (`frontend/src/components/FilePreview.jsx:125-165`), PPTX via Office Online except on localhost (`frontend/src/components/FilePreview.jsx:171-197`).

## Tech stack and layout

Stack and scripts come from `frontend/README.md:13-21` (React 18, Vite, Tailwind CSS, Recharts, Framer Motion, React Router, Lucide React) and `frontend/README.md:86-90` (`dev`/`build`/`preview`). Project layout is documented at `frontend/README.md:63-84`: `components/Sidebar.jsx`, `pages/` with Dashboard/WorkView/LearningView/AgentDetail, `hooks/useWebSocket.js`, `App.jsx`, `main.jsx`, `index.css`. Global styles set Tailwind directives plus custom gradients, glass effects, and scrollbar rules (`frontend/src/index.css:1-3`, `:61-90`). The README notes the dev backend runs at `http://localhost:8000` with the frontend proxying `/api` to it (`frontend/README.md:42-57`).

**Covers:** component 06
