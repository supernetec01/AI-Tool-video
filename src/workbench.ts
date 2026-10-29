import {Scene,Video,C} from './Video';
import {SHOTS,SFX,FPS,TOTAL} from './timeline';
export const WORKBENCH={
 name:'Mẹ Bỉm Thông Thái · Dinh dưỡng mẹ bầu 01',fps:FPS,width:1080,height:1920,total:TOTAL,background:C.cream,
 shots:SHOTS.map(s=>({id:s.id,label:s.title.replace('\n',' '),from:s.from,duration:s.duration,component:Scene,props:{shot:s,title:s.title,benefit:s.benefit,safety:s.safety,tag:s.tag,duration:s.duration},durationProp:'duration',cardId:s.id,schema:[{type:'textarea',key:'title',label:'Tiêu đề',default:s.title},{type:'textarea',key:'benefit',label:'Nội dung',default:s.benefit},{type:'textarea',key:'safety',label:'Lưu ý',default:s.safety},{type:'text',key:'tag',label:'Dưỡng chất',default:s.tag},{type:'color',key:'background',label:'Màu nền',default:C.cream}]})),
 transitions:[],captions:[],overlays:[],sfx:SFX,
 bgm:[{from:0,duration:TOTAL,src:'audio/morning-piano.wav',volume:.65}],
 order:['transitions','captions','overlays'],original:Video,
};
