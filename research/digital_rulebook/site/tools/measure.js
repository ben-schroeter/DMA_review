const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});const out={};
for(const f of process.argv.slice(2)){let s=fs.readFileSync(f,'utf8');s=s.replace(/<script[\s\S]*?<\/script>/g,'').replace(/<\/?helmet>/g,'').replace(/<\/?sc-(if|for)[^>]*>/g,'');
const t=require('os').tmpdir()+'/m_'+f.split('/').pop()+'.html';fs.writeFileSync(t,s);await p.goto('file://'+t);await p.waitForTimeout(300);
out[f]=await p.evaluate(()=>document.body.scrollHeight);await p.screenshot({path:require('os').tmpdir()+'/m_'+f.split('/').pop().replace('.dc.html','')+'.png',fullPage:true});}
console.log(JSON.stringify(out));await b.close()})()
