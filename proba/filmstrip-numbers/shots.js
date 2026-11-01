// usage: node shots.js <outdir> <tag>
const {chromium}=require('playwright');const fs=require('fs');
const [out,tag]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
const VP=[[375,812],[390,844],[1440,900]];
(async()=>{
 const b=await chromium.launch();
 for(const page of ['films.html','commercial.html']) for(const [w,h] of VP) for(const mode of ['loading','loaded']){
  const mob=w<800;
  const ctx=await b.newContext({viewport:{width:w,height:h},isMobile:mob,hasTouch:mob,deviceScaleFactor:mob?3:1});
  const p=await ctx.newPage();
  if(mode==='loading') await p.route(/\.(jpg|jpeg|png)$/,async r=>{const u=r.request().url(); if(/img\/films\/|site\/films\/frames/.test(u)) return; await r.continue();}); // still images never arrive: slow network
  await p.goto('http://localhost:8765/'+page,{waitUntil:mode==='loaded'?'networkidle':'domcontentloaded'});
  await p.waitForTimeout(1500);
  const s=p.locator('.strip').first();await s.scrollIntoViewIfNeeded();await p.waitForTimeout(400);
  const name=`${page.replace('.html','')}-${w}-${mode}-${tag}.png`;
  await s.screenshot({path:`${out}/${name}`});
  // also a whole-page shot at desktop for the pixel compare
  if(w===1440&&mode==='loaded') await p.screenshot({path:`${out}/${page.replace('.html','')}-1440-fullpage-${tag}.png`,fullPage:true});
  // overlap check: any two .fn in the first visible set overlapping?
  const ov=await p.evaluate(()=>{let n=0;document.querySelectorAll('.strip .set:first-child').forEach(set=>{const r=[...set.querySelectorAll('.fn')].map(e=>e.getBoundingClientRect());for(let i=1;i<r.length;i++)if(r[i].left<r[i-1].right-0.5)n++;});return n});
  console.log(name,'overlaps:',ov);
  await ctx.close();
 }
 await b.close();})();
