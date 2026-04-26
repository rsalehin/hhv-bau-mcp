# HHV-Bau MCP Demo

> "Das HHV-Bau-System war bisher nur über die eigene Oberfläche nutzbar. Als MCP-Server kann Claude direkt Permits abfragen, KPIs ziehen, und Dateneingaben vorbereiten — ohne dass der Sachbearbeiter das System auch nur öffnen muss."

A working proof-of-concept showing how a German Bauamt permit system can be exposed as an MCP server — letting Claude query, analyse, and prepare data through natural German conversation instead of manual UI navigation.

---

## What this demonstrates

A clerk currently opens the permit system, navigates menus, searches for a number, reads the status, copies a KPI into a report. With MCP, that entire sequence happens in one sentence.

This is the **"no longer confined to its own interface"** pattern in practice.

---

## Project structure
hhv-bau-mcp/
├── db/
│   ├── seed.py          # Creates SQLite DB + seeds 50 permits
│   ├── permits.db       # Generated database (gitignored)
│   └── test_tools.py    # Validates all 4 tools against live DB
├── server/
│   ├── server.py        # FastMCP server — 4 tools
│   └── requirements.txt
└── demo/
└── index.html       # Standalone browser demo (no server needed)
---

## The 4 MCP tools

| Tool | What it does | Example prompt |
|---|---|---|
| `search_permits` | Filter by status, address, applicant, type | *"Zeig alle offenen Neubauten in Bearbeitung"* |
| `get_permit_details` | Full record + missing documents + overdue days | *"Was fehlt noch bei BG-2024-0015?"* |
| `get_kpi_summary` | Status breakdown, overdue list, clerk workload | *"Wie viele Genehmigungen sind 30+ Tage überfällig?"* |
| `prepare_data_entry` | Pre-fill approval form with today's date | *"Bereite das Formular für BG-2024-0024 vor"* |

---

## Run the browser demo

1. Open `demo/index.html` in Chrome
2. Enter your Anthropic API key (`sk-ant-...`) from [console.anthropic.com](https://console.anthropic.com)
3. Ask anything in German — Claude will call the tools automatically

**Suggested demo sequence:**
1. Click `50 Permits ↗` in the header — shows the full database
2. *"Zeig alle überfälligen Genehmigungen"* — `search_permits` fires
3. *"Was fehlt noch bei BG-2024-0015?"* — `get_permit_details` fires
4. *"Wie viele Genehmigungen sind dieses Quartal mehr als 30 Tage überfällig?"* — `get_kpi_summary` fires
5. *"Bereite das Genehmigungsformular für BG-2024-0024 vor"* — `prepare_data_entry` fires

Watch the **MCP Inspector** panel on the right — it shows every tool call, its inputs, and the structured result in real time.

---

## Run the MCP server locally

```bash
pip install fastmcp
python db/seed.py
python server/server.py
```

The server exposes all 4 tools over MCP and can be connected to any MCP-compatible client (Claude Desktop, etc.).

---

## Why MCP and not just an API?

An API requires a developer to write the integration. An MCP server means Claude can **discover and use the tools without any custom glue code** — a Bauamt clerk can ask Claude in German and get structured permit data back immediately.

The demo runs entirely in the browser with no backend — the MCP tool logic is embedded directly. In production, `server/server.py` would connect to the real permit database.

---

## Tech stack

- **MCP server:** Python + FastMCP + SQLite
- **Demo:** Vanilla React (esm.sh) + Anthropic API with tool use
- **Data:** 50 synthetic Leipzig Baugenehmigungen across 5 clerks

---

