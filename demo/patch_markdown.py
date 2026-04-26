with open("demo/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the plain text message bubble with a markdown-rendering version
old_bubble = """function MessageBubble({msg}){
  const isUser=msg.role==='user';
  return h('div',{className:'fade-in',style:{marginBottom:16,display:'flex',flexDirection:isUser?'row-reverse':'row',alignItems:'flex-start',gap:8}},
    h('div',{style:{width:26,height:26,borderRadius:6,background:isUser?C.blue:C.bg3,border:`1px solid ${C.borderHi}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:12,flexShrink:0}},
      isUser?'👤':'🏗'
    ),
    h('div',{style:{maxWidth:'82%',padding:'10px 14px',background:isUser?`${C.blue}18`:C.bg2,border:`1px solid ${isUser?C.blue+'40':C.border}`,borderRadius:isUser?'10px 2px 10px 10px':'2px 10px 10px 10px',fontSize:12,lineHeight:1.6,color:C.text,fontFamily:C.sans,whiteSpace:'pre-wrap'}},
      msg.text
    )
  );
}"""

new_bubble = """function renderMarkdown(text){
  const lines = text.split('\\n');
  const elements = [];
  let i = 0;
  while(i < lines.length){
    const line = lines[i];
    // H3
    if(line.startsWith('### ')){
      elements.push(h('div',{key:i,style:{fontWeight:600,fontSize:13,color:C.text,marginTop:10,marginBottom:3}},parseLine(line.slice(4))));
    }
    // H2
    else if(line.startsWith('## ')){
      elements.push(h('div',{key:i,style:{fontWeight:600,fontSize:14,color:C.text,marginTop:12,marginBottom:4,borderBottom:`1px solid ${C.border}`,paddingBottom:4}},parseLine(line.slice(3))));
    }
    // Bullet
    else if(line.match(/^[-*] /)){
      elements.push(h('div',{key:i,style:{display:'flex',gap:6,marginTop:2}},
        h('span',{style:{color:C.blue,flexShrink:0,marginTop:1}},'›'),
        h('span',null,parseLine(line.slice(2)))
      ));
    }
    // Numbered list
    else if(line.match(/^\\d+\\. /)){
      const num=line.match(/^(\\d+)\\. /)[1];
      elements.push(h('div',{key:i,style:{display:'flex',gap:6,marginTop:2}},
        h('span',{style:{color:C.blue,flexShrink:0,fontFamily:C.mono,fontSize:11,marginTop:1}},num+'.'),
        h('span',null,parseLine(line.replace(/^\\d+\\. /,'')))
      ));
    }
    // Horizontal rule
    else if(line.match(/^---+$/)){
      elements.push(h('hr',{key:i,style:{border:'none',borderTop:`1px solid ${C.border}`,margin:'8px 0'}}));
    }
    // Empty line
    else if(line.trim()===''){
      elements.push(h('div',{key:i,style:{height:6}}));
    }
    // Normal paragraph
    else {
      elements.push(h('div',{key:i,style:{marginTop:1}},parseLine(line)));
    }
    i++;
  }
  return elements;
}

function parseLine(text){
  // Split on **bold** and render spans
  const parts = text.split(/\\*\\*(.*?)\\*\\*/g);
  if(parts.length===1) return text;
  return parts.map((p,i)=>
    i%2===1
      ? h('strong',{key:i,style:{color:C.text,fontWeight:600}},p)
      : p
  );
}

function MessageBubble({msg}){
  const isUser=msg.role==='user';
  return h('div',{className:'fade-in',style:{marginBottom:16,display:'flex',flexDirection:isUser?'row-reverse':'row',alignItems:'flex-start',gap:8}},
    h('div',{style:{width:26,height:26,borderRadius:6,background:isUser?C.blue:C.bg3,border:`1px solid ${C.borderHi}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:12,flexShrink:0}},
      isUser?'👤':'🏗'
    ),
    h('div',{style:{maxWidth:'82%',padding:'10px 14px',background:isUser?`${C.blue}18`:C.bg2,border:`1px solid ${isUser?C.blue+'40':C.border}`,borderRadius:isUser?'10px 2px 10px 10px':'2px 10px 10px 10px',fontSize:12,lineHeight:1.8,color:C.dim,fontFamily:C.sans}},
      isUser ? msg.text : renderMarkdown(msg.text)
    )
  );
}"""

html = html.replace(old_bubble, new_bubble)

with open("demo/index.html", "w", encoding="utf-8") as f:
    f.write(html)

found = "renderMarkdown" in html
print("ok — markdown renderer patched" if found else "MISSING — patch failed")
