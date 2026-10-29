import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
const serveUrl=await bundle({entryPoint:'src/index.ts'});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium',chromiumOptions:{enableMultiProcessOnLinux:false}});
try {
const composition=await selectComposition({serveUrl,id:'MomBite01',inputProps:{bgm:false},browserExecutable:'/usr/bin/chromium',puppeteerInstance:browser});
console.log('Resolved audio props',composition.props);
// Render the no-music audio from the same composition, including all transition cues.
// Reuse the verified picture stream. No audio is extracted or removed from a mixed recording.
await renderMedia({serveUrl,composition,inputProps:{bgm:false},outputLocation:'out/no-music-timeline.wav',codec:'wav',browserExecutable:'/usr/bin/chromium',puppeteerInstance:browser,concurrency:1});
execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-y','-i','out/mombite-01.mp4','-i','out/no-music-timeline.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','out/mombite-01-khong-nhac.mp4'],{stdio:'inherit'});
console.log('No-music audio rendered from original timeline; picture stream copied exactly.');
} finally {await browser.close({silent:true})}
