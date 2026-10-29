import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {mkdirSync,writeFileSync} from 'node:fs';
import {SHOTS,SFX,CAPTIONS,FPS,TOTAL} from '../src/timeline.ts';
mkdirSync('out/jianying-qa',{recursive:true});
const browserExecutable='/usr/bin/chromium';
const chromiumOptions={gl:'angle',enableMultiProcessOnLinux:true};
const browser=await openBrowser('chrome',{browserExecutable,chromiumOptions});
try{
 const serveUrl=await bundle({entryPoint:'src/index.ts'});
 const inputProps={bgm:false,plate:true};
 const composition=await selectComposition({serveUrl,id:'MomBite01',inputProps,browserExecutable,puppeteerInstance:browser,timeoutInMilliseconds:60000});
 for(const frame of [81,250,650,1250,1401]){
  await renderStill({serveUrl,composition,inputProps,frame,output:`out/jianying-qa/plate-f${frame}.png`,timeoutInMilliseconds:60000,browserExecutable,puppeteerInstance:browser});
 }
 const original=await selectComposition({serveUrl,id:'MomBite01',inputProps:{bgm:false},browserExecutable,puppeteerInstance:browser});
 for(const frame of [81,250,650,1250]){
  await renderStill({serveUrl,composition:original,inputProps:{bgm:false},frame,output:`out/jianying-qa/original-f${frame}.png`,timeoutInMilliseconds:60000,browserExecutable,puppeteerInstance:browser});
 }
 writeFileSync('out/jianying-timeline.json',JSON.stringify({SHOTS,SFX,CAPTIONS,FPS,TOTAL},null,2));
 let last=-1;
 await renderMedia({serveUrl,composition,inputProps,outputLocation:'out/jianying-plate.mp4',codec:'h264',crf:19,pixelFormat:'yuv420p',muted:true,concurrency:2,browserExecutable,puppeteerInstance:browser,chromiumOptions,onProgress:({progress})=>{const n=Math.floor(progress*10);if(n!==last){last=n;console.log('Jianying plate',n*10+'%')}}});
}finally{await browser.close({silent:true})}
