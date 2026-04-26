with open("demo/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. Modal CSS ──────────────────────────────────────────────────────
html = html.replace(
    ".key-gate{position:fixed;inset:0;background:rgba(5,6,11,0.97);display:flex;align-items:center;justify-content:center;z-index:100}",
    """.key-gate{position:fixed;inset:0;background:rgba(5,6,11,0.97);display:flex;align-items:center;justify-content:center;z-index:100}
  .modal-overlay{position:fixed;inset:0;background:rgba(5,6,11,0.92);display:flex;align-items:center;justify-content:center;z-index:50;padding:20px}
  .modal-box{background:#090c17;border:1px solid #262f4a;border-radius:12px;width:100%;max-width:920px;max-height:85vh;display:flex;flex-direction:column;overflow:hidden}
  .modal-header{padding:14px 18px;border-bottom:1px solid #1b2035;display:flex;align-items:center;gap:10px;flex-shrink:0}
  .modal-body{overflow-y:auto}
  .permit-row:hover{background:#0d1120}
  .badge-btn{cursor:pointer;transition:opacity .15s}
  .badge-btn:hover{opacity:0.75}"""
)

# ── 2. PermitTableModal component (inserted before KeyGate) ───────────
modal_component = '''function PermitTableModal({onClose}){
  const [filter,setFilter]=useState('');
  const filtered=PERMITS.filter(p=>
    p.id.toLowerCase().includes(filter.toLowerCase())||
    p.applicant.toLowerCase().includes(filter.toLowerCase())||
    p.address.toLowerCase().includes(filter.toLowerCase())||
    p.type.toLowerCase().includes(filter.toLowerCase())
  );
  const cols=[['ID',100],['Antragsteller',145],['Adresse',195],['Typ',105],['Status',118],['Frist',80],['Sachb.',95],['Docs',48]];
  return h('div',{className:'modal-overlay',onClick:e=>{if(e.target===e.currentTarget)onClose()}},
    h('div',{className:'modal-box'},
      h('div',{className:'modal-header'},
        h('span',{style:{fontSize:14,fontWeight:600,letterSpacing:'-0.02em'}},'Permit-Datenbank'),
        h('span',{style:{fontFamily:C.mono,fontSize:10,color:C.green,background:C.greenD,border:`1px solid ${C.green}35`,padding:'2px 8px',borderRadius:4}},`${PERMITS.length} Eintraege`),
        h('input',{value:filter,onChange:e=>setFilter(e.target.value),placeholder:'Filtern nach ID, Name, Adresse...',style:{marginLeft:'auto',background:C.bg2,border:`1px solid ${C.border}`,borderRadius:6,padding:'5px 10px',color:C.text,fontFamily:C.mono,fontSize:11,width:220}}),
        h('button',{onClick:onClose,style:{marginLeft:8,background:'none',border:`1px solid ${C.border}`,borderRadius:6,color:C.dim,cursor:'pointer',padding:'4px 10px',fontSize:12,fontFamily:C.sans}},'x Schliessen')
      ),
      h('div',{className:'modal-body'},
        h('table',{style:{width:'100%',borderCollapse:'collapse',fontSize:11,fontFamily:C.mono}},
          h('thead',null,
            h('tr',{style:{position:'sticky',top:0,background:C.bg1,zIndex:1}},
              ...cols.map(([t,w])=>h('th',{key:t,style:{textAlign:'left',color:C.muted,padding:'10px 12px',fontWeight:500,minWidth:w,borderBottom:`1px solid ${C.border}`,whiteSpace:'nowrap'}},t))
            )
          ),
          h('tbody',null,
            filtered.length===0
              ? h('tr',null,h('td',{colSpan:8,style:{padding:'24px',textAlign:'center',color:C.muted,fontFamily:C.sans}},'Keine Ergebnisse'))
              : filtered.map(p=>
                  h('tr',{key:p.id,className:'permit-row',style:{borderBottom:`1px solid ${C.border}`}},
                    h('td',{style:{padding:'8px 12px',color:C.blue,whiteSpace:'nowrap'}},p.id),
                    h('td',{style:{padding:'8px 12px',color:C.text}},p.applicant),
                    h('td',{style:{padding:'8px 12px',color:C.dim,fontSize:10}},p.address),
                    h('td',{style:{padding:'8px 12px',color:C.purple,fontSize:10}},p.type),
                    h('td',{style:{padding:'8px 12px'}},h(StatusBadge,{status:p.status,small:true})),
                    h('td',{style:{padding:'8px 12px',color:p.status==='ueberfaellig'?C.red:C.dim,whiteSpace:'nowrap'}},p.deadline.slice(5)),
                    h('td',{style:{padding:'8px 12px',color:C.dim}},p.clerk.split(' ')[0]),
                    h('td',{style:{padding:'8px 12px',color:p.missing.length>0?C.amber:C.green,textAlign:'center'}},p.missing.length>0?`${p.missing.length} !`:'ok')
                  )
                )
          )
        )
      )
    )
  );
}

'''

html = html.replace("function KeyGate({onKey}){", modal_component + "function KeyGate({onKey}){")

# ── 3. Add showTable state to App ─────────────────────────────────────
html = html.replace(
    "  const [activeTool,setActiveTool]=useState(null);",
    "  const [activeTool,setActiveTool]=useState(null);\n  const [showTable,setShowTable]=useState(false);"
)

# ── 4. Make the Permits badge clickable ───────────────────────────────
html = html.replace(
    "h('span',{style:{fontFamily:C.mono,fontSize:10,color:C.dim,background:C.bg2,border:`1px solid ${C.border}`,padding:'2px 8px',borderRadius:4}},`${PERMITS.length} Permits`),",
    "h('span',{className:'badge-btn',onClick:()=>setShowTable(true),style:{fontFamily:C.mono,fontSize:10,color:C.blue,background:C.blueD,border:`1px solid ${C.blue}35`,padding:'2px 8px',borderRadius:4,userSelect:'none'}},`${PERMITS.length} Permits \u2197`),"
)

# ── 5. Render modal at top of App return ──────────────────────────────
html = html.replace(
    "  return h('div',{style:{fontFamily:C.sans,background:C.bg0,color:C.text,height:'100vh',display:'flex',flexDirection:'column',overflow:'hidden'}},",
    "  return h('div',{style:{fontFamily:C.sans,background:C.bg0,color:C.text,height:'100vh',display:'flex',flexDirection:'column',overflow:'hidden'}},\n    showTable&&h(PermitTableModal,{onClose:()=>setShowTable(false)}),"
)

with open("demo/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Checking patches:")
checks = ["modal-overlay", "PermitTableModal", "showTable", "Permits \\u2197", "badge-btn"]
for c in checks:
    found = c.replace("\\u2197", "\u2197") in html
    print(f"  {'ok' if found else 'MISSING'} — {c}")
