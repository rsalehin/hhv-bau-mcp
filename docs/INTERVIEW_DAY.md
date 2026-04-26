# Interview Day — HHV-Bau MCP Demo
### Personal runbook for Julius Janda / FuseSoftware

---

## 30 minutes before

- [ ] Open `demo/index.html` in Chrome — **not Edge, not Firefox**
- [ ] Enter API key at the prompt (`sk-ant-...`)
- [ ] Send one test message to confirm it works: *"Zeig alle überfälligen Genehmigungen"*
- [ ] Clear the chat (refresh the page) — start clean for Julius
- [ ] Have this file open on your phone or a second screen

---

## The one-line pitch

> "Das HHV-Bau-System war bisher nur über die eigene Oberfläche nutzbar.
> Als MCP-Server kann Claude direkt Permits abfragen, KPIs ziehen, und
> Dateneingaben vorbereiten — ohne dass der Sachbearbeiter das System
> auch nur öffnen muss."

Say this **before** touching the demo. Then open the screen.

---

## Demo sequence — 5 beats

Run these in order. Each one is one sentence. Let the response finish before explaining.

---

### Beat 1 — Show the data (30 seconds)

**Action:** Click `50 Permits ↗` badge in the header

**Say:**
> "Das sind 50 echte Baugenehmigungen aus Leipzig — Antragsteller,
> Adressen, Status, fehlende Dokumente. Das ist die Datenbank,
> die ein Sachbearbeiter normalerweise nur im System sieht."

**Point to:** The table, the status badges, the missing docs column (⚠)

---

### Beat 2 — Search (45 seconds)

**Type:** `Zeig alle überfälligen Genehmigungen`

**While it loads, say:**
> "Ich stelle die Frage auf Deutsch. Claude entscheidet selbst,
> welches Tool es aufrufen muss."

**After response, point to the right panel and say:**
> "Hier sehen Sie den MCP Inspector — das Tool `search_permits` wurde
> aufgerufen, mit dem Parameter `status_filter: überfällig`.
> Das ist kein Hardcoding — Claude hat das selbst entschieden."

---

### Beat 3 — Details (45 seconds)

**Type:** `Was fehlt noch bei BG-2024-0015?`

**Say:**
> "Jetzt ein konkreter Antrag. Claude ruft `get_permit_details` auf —
> bekommt die fehlenden Dokumente, die Frist, den Sachbearbeiter.
> Alles strukturiert, direkt aus der Datenbank."

**Point to:** The missing documents list in the inspector result

---

### Beat 4 — KPI (45 seconds)

**Type:** `Wie viele Genehmigungen sind dieses Quartal mehr als 30 Tage überfällig?`

**Say:**
> "Das ist die Frage, für die ein Sachbearbeiter heute 20 Minuten
> braucht — manuell filtern, zählen, in Excel übertragen.
> Hier: eine Frage, eine Antwort."

**Point to:** The KPI grid in the inspector — numbers by status, overdue list

---

### Beat 5 — The wow moment (45 seconds)

**Type:** `Bereite das Genehmigungsformular für BG-2024-0024 vor`

**Say:**
> "Und jetzt der letzte Schritt — das Tool `prepare_data_entry`
> füllt das Formular vor: heutiges Datum, Sachbearbeiter, alle
> Antragstellerdaten. Druckfertig. Der Sachbearbeiter hat das
> System nie geöffnet."

**Point to:** The pre-filled fields in the inspector, especially `bearbeitungsdatum` and `genehmigungsdatum`

---

## If Julius asks a question mid-demo

| Question | Answer |
|---|---|
| "Ist das wirklich MCP?" | "Der Server läuft in `server/server.py` — FastMCP, 4 Tools, direkt an SQLite. Die Demo hier emuliert den MCP-Aufruf im Browser, der Server ist produktionsbereit." |
| "Könnte das mit dem echten System verbunden werden?" | "Ja — `server.py` hat eine `get_con()` Funktion. SQLite austauschen gegen Postgres oder den echten DB-Connector, fertig." |
| "Warum MCP und nicht einfach eine API?" | "Eine API braucht einen Entwickler der die Integration schreibt. MCP bedeutet Claude entdeckt und nutzt die Tools selbst — kein Glue Code." |
| "Kann Claude auch schreiben, nicht nur lesen?" | "`prepare_data_entry` bereitet das vor. Ein fünftes Tool `submit_permit_update` wäre der nächste Schritt — bewusst weggelassen für die Demo." |
| "Wie lange hat das gedauert?" | "Ca. 3-4 Stunden. DB, Server, Demo, README." |

---

## If something breaks

| Problem | Fix |
|---|---|
| "Failed to fetch" | Check API key — refresh page, re-enter key |
| Blank response | Refresh, try again — sometimes the API is slow |
| Page looks broken | Open in Chrome specifically |
| Tool call not showing | Scroll the right panel down |

---

## Repo

**github.com/rsalehin/hhv-bau-mcp**

Show this after the demo — not before. Let the live demo speak first.

---

## Closing line

> "Das Muster funktioniert für jedes Legacy-System das eine Datenbank hat —
> Bauamt, Finanzamt, Krankenhaus. MCP ist die Schicht die das System
> aus seiner eigenen Oberfläche befreit."

---

*Good luck. You built this. You know it inside out.*
