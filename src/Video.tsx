import React, {useId} from 'react';
import {AbsoluteFill, Audio, Img, Sequence, getInputProps, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {SHOTS,SFX,TOTAL,Shot} from './timeline';

export const C={cream:'#FFF5EA',peach:'#E9ADA5',rose:'#CB8176',brown:'#4A3833',sage:'#51634B',muted:'#79685C'};
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const smooth=(x:number)=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
const rects=[[4,4,504,500],[516,4,504,500],[4,512,504,456],[516,512,504,456],[4,977,504,555],[516,977,504,555]];
export const AtlasPhoto:React.FC<{image?:number;width?:number;height?:number;progress?:number}> = ({image=0,width=936,height=780,progress=0})=>{
 const [x,y,w,h]=rects[image];
 const s=Math.max(width/w,height/h);
 const zoom=1.045+([0.035,0.025,0,-0.01,0.028,-0.025][image])*progress;
 const dx=([0,-8,18,0,-12,0][image])*progress;
 const dy=([0,0,0,15,-6,0][image])*progress;
 return <div style={{width,height,overflow:'hidden',position:'relative',background:'#eee0d1'}}>
  <div style={{position:'absolute',inset:0,transform:`translate(${dx}px,${dy}px) scale(${zoom})`}}>
   <Img src={staticFile('food-atlas.png')} style={{position:'absolute',width:1024*s,height:1536*s,maxWidth:'none',left:-x*s+(width-w*s)/2,top:-y*s+(height-h*s)/2}}/>
  </div>
 </div>
};
const Leaf:React.FC<{size?:number}>=({size=42})=><svg width={size} height={size} viewBox="0 0 50 50" fill="none"><path d="M11 35C6 16 26 5 41 9c3 19-9 33-25 29" fill={C.sage}/><path d="M11 44 32 20" stroke={C.cream} strokeWidth="3" strokeLinecap="round"/></svg>;
export const Brand:React.FC<{end?:boolean}>=({end=false})=><div style={{position:'absolute',left:72,right:126,top:144,display:'flex',alignItems:'center',gap:15,color:C.sage}}><Leaf/><span style={{fontSize:29,fontWeight:700,letterSpacing:1.4}}>MẸ BỈM THÔNG THÁI</span><span style={{marginLeft:'auto',fontSize:27,fontWeight:700}}>{end?'HẸN GẶP MẸ':'TẬP 01'}</span></div>;
// Adapted from MarkerUnderlineTitle.tsx: deterministic variable-width brush,
// settling 0–26 reference frames, draw at 32–42, original timing preserved at 24fps.
const brush=()=>{
 let a=77;const rand=()=>{let t=a+=0x6d2b79f5;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296};
 const top:string[]=[],bot:string[]=[];
 for(let i=0;i<=40;i++){const t=i/40,noise=rand()-.5;const x=t*640,mid=21-t*2+Math.sin(t*Math.PI*1.6+.4)*2.6+noise*1.6;const w=Math.max(2.2,14+Math.sin(t*Math.PI)*6-Math.max(0,t-.86)*46-Math.max(0,.06-t)*70+noise*3);top.push(`${x},${mid-w/2}`);bot.push(`${x},${mid+w/2}`)}
 return `M${top.join('L')}L${bot.reverse().join('L')}Z`;
};
const BRUSH=brush();
const Underline:React.FC=()=>{
 const f=useCurrentFrame()/0.8;const id=useId().replace(/[^a-zA-Z0-9]/g,'');
 const p=interpolate(f,[32,42],[0,1],clamp),draw=1-Math.pow(1-p,2.2);
 return <svg width="650" height="44" viewBox="0 0 650 44" style={{position:'absolute',left:190,top:1296}}><defs><clipPath id={`r${id}`}><rect width={draw*646} height={44}/></clipPath><filter id={`b${id}`} x="-5%" y="-40%" width="110%" height="180%" colorInterpolationFilters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.09 0.5" numOctaves={2} seed={7} result="noise"/><feDisplacementMap in="SourceGraphic" in2="noise" scale={1.8} xChannelSelector="R" yChannelSelector="G" result="rough"/><feTurbulence type="fractalNoise" baseFrequency="0.035 0.9" numOctaves={2} seed={19} result="grain"/><feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -16 11.4" result="holes"/><feComposite in="rough" in2="holes" operator="in"/></filter></defs><g clipPath={`url(#r${id})`}><path d={BRUSH} fill={C.peach} filter={`url(#b${id})`}/></g></svg>
};
export const Scene:React.FC<{shot?:Shot;title?:string;benefit?:string;safety?:string;tag?:string;background?:string;titleSize?:number;duration?:number}>=({shot=SHOTS[0],title=shot.title,benefit=shot.benefit,safety=shot.safety,tag=shot.tag,background=C.cream,titleSize=96,duration=shot.duration})=>{
 const f=useCurrentFrame();const p=smooth(f/Math.max(1,duration-30));
 const {plate=false}=getInputProps() as {plate?:boolean};
 const settle=(delay=0)=>{const e=smooth((f-delay)/(shot.id==='hook'?17.6:34));return {opacity:e,transform:`translateY(${24*(1-e)}px)`}};
 const isHook=shot.id==='hook',isSafe=shot.id==='safe',isEnd=shot.id==='cta';
 const entry=interpolate(f,[0,10],[0,1],clamp);
 const exit=interpolate(f,[duration-10,duration-1],[1,0],clamp);
 return <AbsoluteFill style={{background,fontFamily:'Mombite, sans-serif',color:C.brown}}>
  <style>{`@font-face{font-family:Mombite;src:url('${staticFile('NotoSans-Regular.ttf')}')}@font-face{font-family:Mombite;src:url('${staticFile('NotoSans-Bold.ttf')}');font-weight:700}`}</style>
  <div style={{position:'absolute',inset:0,opacity:Math.min(entry,exit)}}>
   <Brand end={isEnd}/>
   {!isEnd && <div style={{position:'absolute',left:72,top:255,width:936,height:isSafe?650:800,borderRadius:isHook?'260px 260px 38px 38px':'38px',overflow:'hidden'}}><AtlasPhoto image={shot.image} width={936} height={isSafe?650:800} progress={p}/></div>}
   {!isEnd && <div style={{position:'absolute',left:98,top:isSafe?839:989,padding:'8px 17px',borderRadius:14,background:'rgba(255,245,234,.94)',color:C.brown,fontSize:32}}>Ảnh minh họa AI</div>}
   {!plate && (isHook ? <>
    <div style={{position:'absolute',left:78,top:1103,fontSize:32,fontWeight:700,letterSpacing:3,...settle(2)}}>{tag}</div>
    <div style={{position:'absolute',left:72,top:1153,fontSize:112,fontWeight:700,letterSpacing:-4,...settle(0)}}><span style={{color:C.rose}}>5</span> thực phẩm</div>
    <Underline/>
    <div style={{position:'absolute',left:76,top:1325,fontSize:84,lineHeight:1.23,fontWeight:700,letterSpacing:-2.8,whiteSpace:'pre-line',...settle(4)}}>{benefit}</div>
    <div style={{position:'absolute',left:78,top:1580,fontSize:37,color:C.muted,...settle(8)}}>{safety}</div>
   </> : isSafe ? <>
    <div style={{position:'absolute',left:76,top:966,fontSize:78,lineHeight:1.25,fontWeight:700,letterSpacing:-2,...settle()}}>{title}<br/>{benefit}</div>
    <div style={{position:'absolute',left:78,right:140,top:1220,...settle(10)}}>
      {['Ăn đa dạng, đủ chất','Nấu chín thực phẩm','Vitamin bầu: theo bác sĩ'].map((t,i)=><div key={t} style={{display:'flex',gap:23,alignItems:'center',fontSize:46,padding:'17px 0',borderBottom:'1px solid #DCC9BA'}}><span style={{color:C.rose,fontSize:33,fontWeight:700}}>0{i+1}</span>{t}</div>)}
    </div>
    <div style={{position:'absolute',left:78,right:140,top:1542,fontSize:35,lineHeight:1.5,color:C.muted,...settle(12)}}>{safety}</div>
   </> : isEnd ? <>
    <div style={{position:'absolute',left:76,top:314,color:C.rose,fontSize:33,fontWeight:700,letterSpacing:3,...settle()}}>DINH DƯỠNG MẸ BẦU · 01</div>
    <div style={{position:'absolute',left:76,right:140,top:440,fontSize:96,lineHeight:1.28,fontWeight:700,letterSpacing:-3,whiteSpace:'pre-line',...settle(2)}}>{title}</div>
    <div style={{position:'absolute',left:76,top:776,width:150,height:8,borderRadius:6,background:C.peach,...settle(4)}}/>
    <div style={{position:'absolute',left:76,top:875,fontSize:49,lineHeight:1.55,color:C.sage,whiteSpace:'pre-line',...settle(6)}}>{benefit}</div>
    <div style={{position:'absolute',left:76,right:140,top:1158,padding:'34px 30px',background:'#F1E3D3',borderRadius:28,fontSize:40,lineHeight:1.6,whiteSpace:'pre-line',...settle(8)}}>{safety}</div>
    <div style={{position:'absolute',left:76,top:1470,fontSize:48,fontWeight:700,color:C.sage,...settle(10)}}>mombite.ai</div>
   </> : <>
    <div style={{position:'absolute',left:76,top:1094,fontSize:30,letterSpacing:3,fontWeight:700,color:C.rose,...settle()}}>0{shot.number} / 05</div>
    <div style={{position:'absolute',left:72,top:1140,fontSize:shot.id==='dairy'?79:titleSize,fontWeight:700,letterSpacing:-3,...settle(2)}}>{title}</div>
    <div style={{position:'absolute',left:76,top:1283,display:'inline-block',padding:'15px 29px',borderRadius:50,background:C.sage,color:'#FFF9F1',fontSize:37,fontWeight:700,letterSpacing:1,...settle(5)}}>{tag}</div>
    <div style={{position:'absolute',left:76,right:135,top:1398,fontSize:51,lineHeight:1.45,fontWeight:400,whiteSpace:'pre-line',...settle(8)}}>{benefit}</div>
    <div style={{position:'absolute',left:78,right:135,top:1580,paddingTop:20,borderTop:'2px solid #DEC7B6',fontSize:40,lineHeight:1.5,color:C.muted,whiteSpace:'pre-line',...settle(12)}}>{safety}</div>
   </>)}
   <div style={{position:'absolute',left:78,top:1760,fontSize:25,color:C.muted,letterSpacing:.5}}>Hình ảnh minh họa AI · Nội dung tham khảo</div>
   {!isEnd&&<div style={{position:'absolute',left:78,top:1806,fontSize:24,color:C.muted}}>mombite.ai</div>}
  </div>
 </AbsoluteFill>
};
export const Video:React.FC<{bgm?:boolean;plate?:boolean}>=({bgm=true,plate=false})=><AbsoluteFill style={{background:C.cream}}>
 <style>{`@font-face{font-family:Mombite;src:url('${staticFile('NotoSans-Regular.ttf')}')}@font-face{font-family:Mombite;src:url('${staticFile('NotoSans-Bold.ttf')}');font-weight:700}`}</style>
 {SHOTS.map(s=><Sequence key={s.id} from={s.from} durationInFrames={s.duration}><Scene shot={s}/></Sequence>)}
 {!plate&&SFX.map((s,i)=><Sequence key={i} from={s.from} durationInFrames={s.duration}><Audio src={staticFile(s.src)} volume={s.volume}/></Sequence>)}
 {bgm&&!plate&&<Audio src={staticFile('audio/morning-piano.wav')} volume={.65}/>}
</AbsoluteFill>;
