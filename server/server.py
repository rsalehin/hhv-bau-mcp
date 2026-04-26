import sqlite3, json
from datetime import date
from pathlib import Path
from fastmcp import FastMCP

DB_PATH = Path(__file__).parent.parent / "db" / "permits.db"

mcp = FastMCP(
    name="hhv-bau-mcp",
    instructions="MCP server for HHV-Bau Bauamt Leipzig. Provides tools to search permits, retrieve details, get KPIs, and prepare data entry forms."
)

def get_con():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


@mcp.tool()
def search_permits(
    applicant_name: str = "",
    address: str = "",
    status_filter: str = "",
    type_filter: str = ""
) -> dict:
    """
    Sucht Baugenehmigungen nach Antragsteller, Adresse, Status oder Vorhabentyp.
    Gibt eine gefilterte Liste zurück.
    status_filter: genehmigt | in_bearbeitung | ausstehend | ueberfaellig | abgelehnt
    type_filter: Neubau | Umbau | Abriss | Nutzungsaenderung
    """
    query = "SELECT * FROM permits WHERE 1=1"
    params = []
    if applicant_name:
        query += " AND applicant LIKE ?"
        params.append(f"%{applicant_name}%")
    if address:
        query += " AND address LIKE ?"
        params.append(f"%{address}%")
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
    if type_filter:
        query += " AND type = ?"
        params.append(type_filter)

    con = get_con()
    rows = con.execute(query, params).fetchall()
    con.close()

    permits = []
    for r in rows:
        permits.append({
            "id": r["id"],
            "applicant": r["applicant"],
            "address": r["address"],
            "type": r["type"],
            "status": r["status"],
            "submitted_date": r["submitted_date"],
            "deadline": r["deadline"],
            "missing_count": len(json.loads(r["missing_documents"])),
            "assigned_clerk": r["assigned_clerk"],
        })

    return {"count": len(permits), "permits": permits}


@mcp.tool()
def get_permit_details(permit_id: str) -> dict:
    """
    Gibt vollständige Details zu einer Baugenehmigung zurück,
    inkl. fehlender Dokumente und Überfälligkeitstage.
    Beispiel permit_id: BG-2024-0015
    """
    con = get_con()
    row = con.execute(
        "SELECT * FROM permits WHERE id = ?", (permit_id,)
    ).fetchone()
    con.close()

    if not row:
        return {"error": f"Genehmigung {permit_id} nicht gefunden."}

    deadline = date.fromisoformat(row["deadline"])
    today = date.today()
    days_overdue = (today - deadline).days

    return {
        "id": row["id"],
        "applicant": row["applicant"],
        "address": row["address"],
        "type": row["type"],
        "status": row["status"],
        "submitted_date": row["submitted_date"],
        "deadline": row["deadline"],
        "missing_documents": json.loads(row["missing_documents"]),
        "missing_count": len(json.loads(row["missing_documents"])),
        "assigned_clerk": row["assigned_clerk"],
        "note": row["note"],
        "days_overdue": max(0, days_overdue),
        "is_overdue": days_overdue > 0,
    }


@mcp.tool()
def get_kpi_summary(
    overdue_days: int = 0,
    status_filter: str = ""
) -> dict:
    """
    Gibt KPI-Übersicht zurück: Statusverteilung, überfällige Anträge,
    fehlende Dokumente, Sachbearbeiter-Workload.
    overdue_days: Mindestanzahl Überfälligkeitstage (Standard 0)
    """
    con = get_con()
    all_rows = con.execute("SELECT * FROM permits").fetchall()
    con.close()

    today = date.today()

    by_status = {}
    by_type = {}
    by_clerk = {}
    overdue_list = []
    with_missing = 0

    for r in all_rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
        by_clerk[r["assigned_clerk"]] = by_clerk.get(r["assigned_clerk"], 0) + 1

        missing = json.loads(r["missing_documents"])
        if missing:
            with_missing += 1

        deadline = date.fromisoformat(r["deadline"])
        days_over = (today - deadline).days
        if days_over > overdue_days:
            overdue_list.append({
                "id": r["id"],
                "applicant": r["applicant"],
                "deadline": r["deadline"],
                "days_overdue": days_over,
                "assigned_clerk": r["assigned_clerk"],
                "status": r["status"],
            })

    overdue_list.sort(key=lambda x: x["days_overdue"], reverse=True)

    return {
        "total": len(all_rows),
        "by_status": by_status,
        "by_type": by_type,
        "by_clerk": by_clerk,
        "overdue_count": len(overdue_list),
        "overdue_list": overdue_list,
        "with_missing_docs": with_missing,
        "query_date": today.isoformat(),
        "overdue_threshold_days": overdue_days,
    }


@mcp.tool()
def prepare_data_entry(
    permit_id: str,
    field_updates: dict = {}
) -> dict:
    """
    Bereitet ein Genehmigungsformular vor: befüllt Felder mit aktuellem Datum,
    Sachbearbeiter und Antragstellerdaten. Gibt ein druckfertiges Formularobjekt zurück.
    field_updates: optionale Felder die überschrieben werden sollen (als dict)
    """
    con = get_con()
    row = con.execute(
        "SELECT * FROM permits WHERE id = ?", (permit_id,)
    ).fetchone()
    con.close()

    if not row:
        return {"error": f"Genehmigung {permit_id} nicht gefunden."}

    today = date.today().isoformat()
    missing = json.loads(row["missing_documents"])

    pre_filled = {
        "genehmigungsnummer": row["id"],
        "antragsteller": row["applicant"],
        "adresse": row["address"],
        "vorhabentyp": row["type"],
        "eingangsdatum": row["submitted_date"],
        "frist": row["deadline"],
        "bearbeitungsdatum": today,
        "sachbearbeiter": row["assigned_clerk"],
        "genehmigungsdatum": today,
        "unterschrift_datum": today,
        "formular_version": "VwVfG §73 — Ausg. 2024",
        **field_updates,
    }

    return {
        "status": "bereit",
        "permit_id": row["id"],
        "antragsteller": row["applicant"],
        "vollstaendig": len(missing) == 0,
        "fehlende_dokumente": missing,
        "pre_filled": pre_filled,
    }


if __name__ == "__main__":
    mcp.run()
