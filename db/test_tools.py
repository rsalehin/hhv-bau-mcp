import sys, json
sys.path.insert(0, "server")
from server import search_permits, get_permit_details, get_kpi_summary, prepare_data_entry

PASS = "✓"
FAIL = "✗"

def check(label, result, expect_key):
    ok = expect_key in result
    print(f"  {PASS if ok else FAIL}  {label}")
    if not ok:
        print(f"     Got: {json.dumps(result, ensure_ascii=False)[:120]}")
    return ok

print("\n── Tool 1: search_permits ──────────────────────────")
r = search_permits(status_filter="überfällig")
check("returns count key",         r, "count")
check("returns permits list",      r, "permits")
print(f"     überfällig count: {r.get('count')}")

r2 = search_permits(address="Hauptstraße")
check("address filter works",      r2, "count")
print(f"     Hauptstraße hits: {r2.get('count')}")

print("\n── Tool 2: get_permit_details ──────────────────────")
r = get_permit_details("BG-2024-0015")
check("found permit",              r, "applicant")
check("has missing_documents",     r, "missing_documents")
check("has is_overdue flag",       r, "is_overdue")
print(f"     Applicant: {r.get('applicant')}")
print(f"     Missing docs: {r.get('missing_documents')}")
print(f"     Overdue: {r.get('is_overdue')} ({r.get('days_overdue')} days)")

r_bad = get_permit_details("BG-9999-0000")
check("bad id returns error key",  r_bad, "error")

print("\n── Tool 3: get_kpi_summary ─────────────────────────")
r = get_kpi_summary()
check("has total",                 r, "total")
check("has by_status",             r, "by_status")
check("has overdue_list",          r, "overdue_list")
print(f"     Total permits: {r.get('total')}")
print(f"     By status: {json.dumps(r.get('by_status'), ensure_ascii=False)}")
print(f"     Overdue (0+ days): {r.get('overdue_count')}")

r2 = get_kpi_summary(overdue_days=30)
print(f"     Overdue (30+ days): {r2.get('overdue_count')}")

print("\n── Tool 4: prepare_data_entry ──────────────────────")
r = prepare_data_entry("BG-2024-0024")
check("status is bereit",          r, "status")
check("has pre_filled",            r, "pre_filled")
check("vollstaendig flag present", r, "vollstaendig")
print(f"     Permit: {r.get('permit_id')}  Complete: {r.get('vollstaendig')}")
print(f"     Bearbeitungsdatum: {r.get('pre_filled', {}).get('bearbeitungsdatum')}")

r2 = prepare_data_entry("BG-2024-0015", field_updates={"sachbearbeiter": "Max Mustermann"})
print(f"     Override clerk: {r2.get('pre_filled', {}).get('sachbearbeiter')}")

print("\n────────────────────────────────────────────────────")
print("All tool tests complete.\n")
