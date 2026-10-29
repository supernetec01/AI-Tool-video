import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {mkdirSync,writeFileSync} from 'node:fs';
import {SHOTS,CAPTIONS,FPS} from '../src/timeline.ts';

mkdirSync('out/qa',{recursive:true});
const browserExecutable='/usr/bin/chromium';
const browser=await openBrowser('chrome',{browserExecutable,chromiumOptions:{gl:'angle'}});
try {
 const serveUrl=await bundle({entryPoint:'src/index.ts'});
 const composition=await selectComposition({serveUrl,id:'MomBite01',browserExecutable,puppeteerInstance:browser});
 const frames=SHOTS.flatMap(s=>[s.from+18,s.from+Math.floor(s.duration*.68)]);
 for(const frame of frames){
  await renderStill({serveUrl,composition,frame,output:`out/qa/f${frame}.png`,imageFormat:'png',browserExecutable,puppeteerInstance:browser});
  console.log('QA frame',frame);
 }
 const stamp=f=>{const ms=Math.round(f/FPS*1000);return `${String(Math.floor(ms/3600000)).padStart(2,'0')}:${String(Math.floor(ms/60000)%60).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')},${String(ms%1000).padStart(3,'0')}`};
 writeFileSync('out/mombite-01.vi.srt',CAPTIONS.map((c,i)=>`${i+1}\n${stamp(c.from)} --> ${stamp(c.from+c.duration)}\n${c.text}\n`).join('\n'));
 writeFileSync('out/loi-thoai.txt',CAPTIONS.map(c=>`[${c.from/FPS}–${(c.from+c.duration)/FPS}s]\n${c.text}\n`).join('\n'));
 writeFileSync('out/qa/frames.json',JSON.stringify(frames));
 if(process.argv.includes('--stills-only')) process.exitCode=0;
 else for(const bgm of [true,false]){
  const outputLocation=`out/mombite-01${bgm?'':'-khong-nhac'}.mp4`;
  let last=-1;
  const resolved=await selectComposition({serveUrl,id:'MomBite01',inputProps:{bgm},browserExecutable,puppeteerInstance:browser});
  await renderMedia({serveUrl,composition:resolved,inputProps:{bgm},outputLocation,codec:'h264',crf:19,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',concurrency:3,browserExecutable,puppeteerInstance:browser,chromiumOptions:{gl:'angle'},onProgress:({progress})=>{const n=Math.floor(progress*10);if(n!==last){last=n;console.log(outputLocation,n*10+'%')}}});
  console.log('Rendered',outputLocation);
 }
}finally{await browser.close({silent:true})}
