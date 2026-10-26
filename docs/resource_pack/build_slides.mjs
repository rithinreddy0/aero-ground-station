// Editable native PowerPoint objects, authored inside the viewer-bound session.
const C={navy:'#132C46',teal:'#087E8B',gray:'#4C6073',light:'#EDF5F7',white:'#FFFFFF'};
const points=[
['ArduCopter closes the flight-control loop onboard.','The laptop combines video, AI, maps, incident evidence and bounded route feedback.','A human pilot retains takeoff, landing, flight-mode and takeover authority.'],
['User-reported: sensor calibration, radio modes and corrected motor tests.','Implemented: telemetry, video upload, AI review, tracking and incident storage.','Pending evidence: reliable GPS fix, live capture hardware, battery calibration and flight validation.'],
['SpeedyBee F405 AIO V1 running ArduCopter; 3-inch propellers.','4S 650 mAh LiPo, marked 95C; motor/KV and aircraft mass still need recording.','GM10 Mini V3 GPS, ELRS radio link and analog FPV equipment.','Receiver model, ELRS versions, camera/VTX and compass variant remain to be identified.'],
['AIO: processor, IMU, barometer, regulators and electrical interfaces.','ArduCopter: state estimation, stabilization, motor mixing and onboard failsafes.','Mission Planner: setup, parameter readback, diagnostics and log review.','Custom application: supervised observations and constrained movement requests.'],
['The battery feeds propulsion; regulated rails supply the FC, GPS and receiver.','DShot signals command the ESC; motor phase wires carry propulsion power.','4S reaches 16.8 V when full. A 12 V-only receiver needs suitable regulated power.','Endurance requires measured hover current, aircraft mass and usable battery capacity.'],
['GNSS position: GPS TX -> AIO R5; GPS RX <- AIO T5; check supply and ground.','A compass, if fitted, communicates separately over SDA/SCL.','A powered LED does not prove a 3D fix or valid EKF position.','Verify GPS status, satellites, HDOP and message age in telemetry.'],
null,
['Native ELRS MAVLink carries RC plus bidirectional MAVLink over a supported RF setup.','The laptop may connect through a TX Backpack UDP bridge or supported transmitter USB.','Ordinary CRSF telemetry alone is not a general laptop MAVLink bridge.','Record the actual TX/RX models, firmware versions, bridge and serial settings.'],
['UART5: GM10 GPS, with crossed TX/RX and correct regulated power.','UART6: aircraft ELRS receiver; confirm actual wiring and firmware transport.','I2C: separate external compass interface, only if the sensor is present.','USB: direct FC setup. RF video reaches the laptop through a separate capture path.'],
null,null,
['Channel 6, three positions: 1000 Stabilize / 1500 Loiter / 2000 GUIDED.','Channel 5 high: RTL request. Channel 7 high: AltHold request.','Channel 8 high: Land request. Return auxiliary switches low after use.','Check all switch interactions on the bench; GPS-dependent modes need valid position.'],
null,
['Read back the actual FC parameters and save a baseline before changing them.','Verify orientation, radio mapping, sensor calibration and current pre-arm messages.','Test each motor location and rotation with props removed.','Confirm voltage/current measurement, failsafe behavior and manual takeover.'],
['HEARTBEAT: armed state and mode. GLOBAL_POSITION_INT: position and velocity.','GPS_RAW_INT: fix, satellites and HDOP. SYS_STATUS: battery state.','EKF_STATUS_REPORT: estimator checks; STATUSTEXT: diagnostic messages.','Freshness is per message family; a heartbeat cannot substitute for fresh GPS or battery.'],
null,
['Pilot selects GUIDED; the operator explicitly leases application control.','Fresh telemetry, GPS/EKF, battery, video and bounded limits gate movement.','Velocity-only BODY_NED setpoints use mask 0x0DC7; body Z is positive down.','The current application does not autonomously arm, take off or land.'],
null,
['Route A: analog VTX -> 5.8 GHz USB/UVC receiver -> laptop.','Route B: analog VTX -> RC805 -> composite USB capture -> laptop.','The receiver frequency must match the VTX; RC805 only supports its listed eight channels.','A goggles memory-card slot is not a live USB video output.'],
['The analog path has RF, capture, decode, inference and display delays.','Use the detector result on its corresponding frame; avoid drawing stale boxes on a newer frame.','Uploaded clips provide repeatable tests before a live receiver is available.','CPU processing throughput is not the same as end-to-end video latency.'],
null,null,null,
['AURA integration includes the VisDrone model and a configurable lightweight YOLO alternative.','CLAHE and hybrid enhancement are available; choose processing explicitly.','The saved checkpoint does not demonstrate a separately integrated CBAM or Zero-DCE model.','Recorded CPU timings and one detection example are observations, not accuracy validation.'],
null,
['Track people over distinct source frames; require persistence before confirming a lead.','IoU association and expiry rules reduce repeated or isolated detections.','Human review is still required; detections are not confirmed survivors.','A detected person can pause a mission; recovery remains an explicit operator decision.'],
null,null,null,
['Onboard protection: arming checks, radio failsafe, GCS failsafe and battery actions.','Application protection: message freshness, video age, lease, mode, GPS/EKF and motion bounds.','Pilot intervention or a protective event pauses route execution.','Evaluate link-loss behavior and mode recovery on the actual configured aircraft.'],
['Historical files document changes; they are not a complete current FC snapshot.','Groups cover frame/motors, RC modes, GPS/UARTs, telemetry and onboard protection.','Later motor mapping and tuning corrections differ from the first exported baseline.','Read back the aircraft before relying on any parameter value in this report.'],
['Bench acceptance: power, wiring, sensors, motor mapping, RC, telemetry and failsafes.','Flight acceptance: supervised stability, vibration, hover current, GNSS quality and takeover.','Application acceptance: bounded movement, stale-data stops, video loss and incident policy.','Progress only after the preceding stage has recorded evidence.'],
['The last recorded suite had 46 passing tests; this is historical software evidence.','Repeatable clip tests cover upload, model selection, frame alignment and review.','Measure real GNSS quality, RF range, voltage/current calibration and full video latency.','No field search accuracy, endurance or autonomous-flight certification is claimed.'],
['GPS: check fix/satellites/HDOP, supply, crossed UART wires and serial configuration.','Radio failsafe: verify the transmitter, live RC input and receiver link status.','Battery: compare FC voltage against a meter; do not bypass pre-arm protection.','Video: separate RF/frequency problems from USB driver, device selection and AI issues.'],
['Start with offline incident review, operator notes, mission replay and exportable evidence.','An ESP32 plus DFPlayer/amplifier can play prerecorded messages; a bare ESP32 is not a loudspeaker.','Payload power, mass, mounting and RF effects need a separate bench and flight evaluation.','Thermal imaging, relay networking and precise survivor geolocation are future integrations.'],
['MAVLink is the message protocol; ELRS is the RF transport; ArduCopter is the autopilot.','GPS measures position; the compass measures magnetic heading; EKF fuses sensor evidence.','AI boxes suggest candidates. Aircraft coordinates are not the person’s ground coordinates.','Explain the confirmed prototype, its remaining tests and its limits during the viva.'],
['Primary references: ArduPilot board, motor, Guided-control and failsafe documentation.','Transport references: ExpressLRS native MAVLink and MAVLink common messages.','Implementation references: application repository and pinned team AURA revision.','All 18 links and detailed section notes are included in the PDF and editable source pack.']
];

function text(slide,name,value,x,y,w,h,size=26,color=C.navy,bold=false,align='left',fill='none'){
  const sh=slide.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});
  sh.text=value;
  sh.text.style={typeface:'Arial',fontSize:size,color,bold,alignment:align,verticalAlignment:'middle',insets:0,wrap:'square'};
  return sh;
}
function rect(slide,name,x,y,w,h,fill=C.light,line=C.navy,geometry='rect'){
  return slide.shapes.add({geometry,name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:line,width:1.5}});
}
function line(slide,name,x1,y1,x2,y2,dashed=false,arrow=false){
  return slide.shapes.add({geometry:'custom',name,position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.max(1,Math.abs(x2-x1)),height:Math.max(1,Math.abs(y2-y1))},fill:'none',line:{fill:C.teal,width:2,style:dashed?'dashed':'solid'},customPaths:[{width:Math.max(1,Math.abs(x2-x1)),height:Math.max(1,Math.abs(y2-y1)),commands:[{moveTo:{x:x1<=x2?0:Math.abs(x2-x1),y:y1<=y2?0:Math.abs(y2-y1)}},{lineTo:{x:x1<=x2?Math.abs(x2-x1):0,y:y1<=y2?Math.abs(y2-y1):0}}]}]});
}
function endArrow(slide,x1,y1,x2,y2){
  const a=Math.atan2(y2-y1,x2-x1),L=10;
  line(slide,'arrow-head',x2,y2,x2-L*Math.cos(a-.45),y2-L*Math.sin(a-.45));
  line(slide,'arrow-head',x2,y2,x2-L*Math.cos(a+.45),y2-L*Math.sin(a+.45));
}
function sides(a,b){
  const ax=a.x+a.w/2,ay=a.y+a.h/2,bx=b.x+b.w/2,by=b.y+b.h/2,dx=bx-ax,dy=by-ay;
  return Math.abs(dx)>Math.abs(dy)*1.25?[[a.x+(dx>0?a.w:0),ay],[b.x+(dx>0?0:b.w),by]]:[[ax,a.y+(dy>0?a.h:0)],[bx,b.y+(dy>0?0:b.h)]];
}
function diagram(slide,d){
  const ox=80,oy=177,sx=1.1,sy=.86,X=x=>ox+x*sx,Y=y=>oy+y*sy;
  const arrow=(a,b,label='',dash=false)=>{
    line(slide,'relationship',X(a[0]),Y(a[1]),X(b[0]),Y(b[1]),dash);endArrow(slide,X(a[0]),Y(a[1]),X(b[0]),Y(b[1]));
    if(label){const mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;
      const isHorizontal=Math.abs(a[1]-b[1])<15;
      const width=isHorizontal&&d.kind!=='sequence'?Math.max(75,Math.abs(a[0]-b[0])*sx-12):Math.min(720,Math.max(120,Math.max(...label.split('\n').map(x=>x.length))*10+22));
      const height=label.split('\n').length*21+9;
      text(slide,'relationship-label',label,X(mx)-width/2,Y(my)-(isHorizontal&&d.kind!=='sequence'?58:height),width,isHorizontal&&d.kind!=='sequence'?56:height,17,C.gray,false,'center',C.white);
    }
  };
  if(d.kind==='sequence'){
    const xs=d.actors.map((_,i)=>100+i*800/(d.actors.length-1));
    d.actors.forEach((actor,i)=>{
      rect(slide,'participant',X(xs[i]-95),Y(10),190*sx,65*sy);
      text(slide,'participant-name',actor,X(xs[i]-90),Y(14),180*sx,57*sy,20,C.navy,true,'center');
      line(slide,'lifeline',X(xs[i]),Y(75),X(xs[i]),Y(485),true);
    });
    const step=370/d.steps.length;
    d.steps.forEach(([a,b,label],i)=>{
      const y=105+i*step;
      if(a===b){line(slide,'self-call',X(xs[a]),Y(y),X(xs[a]+45),Y(y));line(slide,'self-call',X(xs[a]+45),Y(y),X(xs[a]+45),Y(y+22));arrow([xs[a]+45,y+22],[xs[a],y+22]);
        const width=Math.min(650,(label.length*10)+28);let left=X(xs[a]+8);if(left+width>1200)left=1200-width;
        text(slide,'self-call-label',label,left,Y(y)-28,width,25,17,C.gray,false,'left',C.white);
      }else arrow([xs[a],y+15],[xs[b],y+15],`${i+1}. ${label}`);
    });
  }else{
    const nodes=Object.fromEntries(d.nodes.map(n=>[n.id,n]));
    d.edges.forEach(e=>{const [a,b]=sides(nodes[e.a],nodes[e.b]);
      if(d.id==='state'&&((e.a==='run'&&e.b==='pause')||(e.a==='pause'&&e.b==='run'))){const off=e.a==='run'?-24:24;a[1]+=off;b[1]+=off;}
      arrow(a,b,e.label,e.style==='dashed');
      if(d.id==='architecture'&&['radio','rx','laptop','bridge'].includes(e.a))endArrow(slide,X(b[0]),Y(b[1]),X(a[0]),Y(a[1]));
    });
    d.nodes.forEach(n=>{
      rect(slide,n.id,X(n.x),Y(n.y),n.w*sx,n.h*sy,C.light,C.navy,['ellipse','diamond'].includes(n.kind)?n.kind:'rect');
      text(slide,n.id+'-label',n.label,X(n.x)+8,Y(n.y)+4,n.w*sx-16,n.h*sy-8,n.w>=200?21:19,C.navy,false,'center');
    });
  }
  text(slide,'diagram-caption',d.caption,80,620,1120,49,19,C.gray);
}
function base(p,sec,index,total){
  const slide=p.slides.add();slide.background.fill=C.white;
  text(slide,'section-index',`AERO  /  ${String(index).padStart(2,'0')}`,64,23,500,24,14,C.teal,true);
  text(slide,'title',sec.title,64,62,1152,67,sec.title.length>51?36:40,C.navy,true);
  text(slide,'summary',sec.summary,66,133,1148,34,23,C.teal);
  text(slide,'footer','Hardware implementation  |  26 October 2026',64,687,800,19,13,C.gray);
  text(slide,'page',`${index+1} / ${total}`,1106,687,110,19,13,C.gray,false,'right');
  return slide;
}
export function build(p,data,start,end){
  const total=data.sections.length+1;
  if(start===0){
    const sl=p.slides.add();sl.background.fill=C.navy;
    text(sl,'eyebrow','AERO / PROJECT RESOURCE PACK',72,74,1100,35,20,'#6DD5DD',true);
    text(sl,'cover-title','Aero Ground\nStation',72,153,1100,182,76,C.white,true);
    text(sl,'cover-subtitle','Hardware implementation, communication\nand system architecture',76,376,1100,106,36,C.white);
    text(sl,'cover-scope','3-inch quadcopter  |  ArduCopter  |  ELRS  |  Laptop AI',76,544,1100,40,25,'#B6D9E4');
    text(sl,'cover-date',data.date+'  •  Evidence-based project documentation',76,641,1100,30,19,'#B6D9E4');
    sl.speakerNotes.text='A comprehensive project resource pack. The PDF carries full engineering explanations, source links and acceptance criteria. Slides are editable; additional detail is in speaker notes. Hardware behavior that has not been validated is marked as pending.';
  }
  for(let i=start;i<Math.min(end,data.sections.length);i++){
    const sec=data.sections[i],slide=base(p,sec,i+1,total);
    if(sec.diagram)diagram(slide,data.diagrams[sec.diagram]);
    else{
      const ps=points[i]||sec.paragraphs.map(p=>p.split(/(?<=\.)\s/)[0]).slice(0,4);
      const gap=ps.length===3?135:110,top=202;
      ps.forEach((t,j)=>{
        text(slide,'point-index',String(j+1).padStart(2,'0'),68,top+j*gap,55,48,25,C.teal,true);
        text(slide,'point',t,145,top+j*gap-1,1035,gap-20,28,C.navy);
      });
    }
    const refs=data.sources.filter(s=>sec.sources?.includes(s[0])).map(s=>s.join(' | '));
    slide.speakerNotes.text=[sec.summary,...sec.paragraphs,...(sec.bullets||[]),sec.table?sec.table.map(r=>r.join(' | ')).join('\n'):'',sec.callout||'',sec.diagram?data.diagrams[sec.diagram].caption:'',...refs,i===data.sections.length-1?data.sources.map(s=>s.join(' | ')).join('\n'):''].filter(Boolean).join('\n\n');
  }
  return {slides:p.slides.items.length};
}
