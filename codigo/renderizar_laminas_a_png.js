const { chromium } = require('playwright');
const fs = require('fs');
(async()=>{
const files = fs.readdirSync('entrega2_svg').filter(f=>f.endsWith('.svg')).sort();
const b = await chromium.launch();
const p = await b.newPage({viewport:{width:1920,height:1080}, deviceScaleFactor:1});
fs.mkdirSync('entrega2_png',{recursive:true});
for(const f of files){
  const svg = fs.readFileSync('entrega2_svg/'+f,'utf8');
  await p.setContent(`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap"><style>html,body{margin:0;padding:0}svg{display:block}</style>`+svg,{waitUntil:'networkidle'});
  await p.waitForTimeout(250);
  await p.screenshot({path:'entrega2_png/'+f.replace('.svg','.png')});
}
await b.close();console.log('rendered',files.length);
})();
