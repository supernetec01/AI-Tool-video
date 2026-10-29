import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Video} from './Video';
import {FPS,TOTAL} from './timeline';
const Root:React.FC=()=>React.createElement(Composition,{id:'MomBite01',component:Video,durationInFrames:TOTAL,fps:FPS,width:1080,height:1920,defaultProps:{bgm:true}});
registerRoot(Root);
