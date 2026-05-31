import streamlit as st

st.set_page_config(page_title="Simulasi Kopi Kenangan Kaliurang", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');

body, .stApp {
    background-color: #FAF4EC !important;
    color: #1C0F08 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSidebar {
    background-color: #F2E8D9 !important;
    border-right: 1px solid #E8D5BE !important;
}
.stSelectbox > div > div {
    background-color: #FDFAF6 !important;
    color: #1C0F08 !important;
    border: 1px solid #E8D5BE !important;
    border-radius: 9px !important;
}
.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within,
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
  background-color: #EFE0C9 !important;
  border-color: #C9B08E !important;
}
.stSelectbox [role="option"]:hover,
div[role="option"]:hover {
  background-color: #E6D0B1 !important;
  color: #1C0F08 !important;
}
.stSelectbox input,
.stSelectbox textarea {
  caret-color: transparent !important;
}
.stSelectbox input::selection,
.stSelectbox textarea::selection {
  background: transparent !important;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #1C0F08 !important;
}
div[data-testid="stMarkdownContainer"] p {
    color: #7A4A2E !important;
}
</style>
""", unsafe_allow_html=True)

st.title("☕ Kopi Kenangan Kaliurang Simulation")
st.markdown("Visualization of agent movement using stochastic physics based on empirical observation data.")

st.sidebar.header("Scenario Settings")
hari = st.sidebar.selectbox("Day Type", ["Weekday", "Weekend"], index=0)
waktu = st.sidebar.selectbox(
  "Time Shift",
  ["Morning (09:00–12:00)", "Afternoon (12:00–15:00)", "Evening (15:00–18:00)", "Night (18:00–20:00)"],
  index=0,
  accept_new_options=False,
)
shift_key_map = {
  "Morning (09:00–12:00)": "Morning",
  "Afternoon (12:00–15:00)": "Afternoon",
  "Evening (15:00–18:00)": "Evening",
  "Night (18:00–20:00)": "Night",
}
shift_key = shift_key_map[waktu]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'DM Sans', sans-serif; background: #FAF4EC; color: #1C0F08; padding: 5px; }}

#app {{
  display: flex; flex-direction: column; width: 100%;
  padding-top: 80px;
  height: 100%;
  overflow: auto;
}}

#hdr {{
  position: fixed;
  top: 5px;
  left: 5px;
  right: 5px;
  z-index: 10000;
  background: #1C0F08; height: 56px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px; border-radius: 12px; margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
#hdr-title-panel {{ display: flex; align-items: center; gap: 10px; }}
#hdr-title {{ font-size: 15px; color: #E8D5BE; font-weight: 600; letter-spacing: 0.5px; }}
#hdr-sub {{ font-size: 10px; color: #7A4A2E; text-transform: uppercase; letter-spacing: 1px; }}
#hdr-right {{ display: flex; align-items: center; gap: 20px; }}
#hdr-clock {{ text-align: right; }}
#hdr-time {{ font-family: 'Share Tech Mono', monospace; color: #E8D5BE; font-size: 24px; line-height: 1; }}
#hdr-shift {{ font-size: 10px; color: #7A4A2E; text-transform: uppercase; margin-top: 2px; }}

.live-badge {{ display: flex; align-items: center; gap: 6px; background: rgba(107,143,113,0.15); padding: 4px 10px; border-radius: 20px; }}
.live-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #6B8F71; animation: pulse 2s ease-in-out infinite; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
#live-label {{ font-size: 10px; color: #6B8F71; font-weight: 600; letter-spacing: 0.5px; }}

.hbtn {{
  font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 12px;
  border: none; border-radius: 8px; cursor: pointer; padding: 8px 16px; transition: all 0.2s;
}}
.hbtn-primary {{ background: #A86B3C; color: #FDFAF6; }}
.hbtn-primary:hover {{ background: #C06B35; }}
.hbtn-pause {{ background: #F2E8D9; color: #C4847A; border: 1px solid #E8D5BE; }}
.hbtn-pause:hover {{ background: #F5DDD9; }}

#metrics {{ display: flex; gap: 12px; margin-bottom: 16px; width: 100%; }}
.mcard {{
  background: #FDFAF6; border: 1px solid #E8D5BE; border-radius: 14px;
  padding: 14px 16px; flex: 1; min-width: 150px;
}}
.mcard-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }}
.mcard-lbl {{ font-size: 10px; color: #7A4A2E; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
.mcard-icon {{ font-size: 14px; opacity: 0.6; }}
.mcard-val {{ font-size: 24px; font-weight: 600; color: #1C0F08; line-height: 1.1; }}
.mcard-sub {{ font-size: 11px; color: #C8956C; margin-top: 2px; }}
.mbar {{ height: 4px; border-radius: 2px; background: #E8D5BE; overflow: hidden; margin-top: 8px; }}
.mbar-fill {{ height: 100%; width: 0%; transition: width 0.5s ease; }}

#mid-row {{ display: flex; gap: 14px; margin-bottom: 16px; width: 100%; }}
#occ-panel {{ background: #FDFAF6; border: 1px solid #E8D5BE; border-radius: 14px; padding: 16px; flex: 1.8; }}
#event-panel {{ background: #FDFAF6; border: 1px solid #E8D5BE; border-radius: 14px; padding: 16px; flex: 1.2; }}
.panel-title {{ font-size: 11px; font-weight: 600; color: #A86B3C; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }}

.occ-row {{ margin-bottom: 10px; }}
.occ-top {{ display: flex; justify-content: space-between; margin-bottom: 3px; font-size: 12px; }}
.occ-lbl {{ color: #7A4A2E; font-weight: 500; }}
.occ-pct {{ font-weight: 600; }}
.occ-bar {{ height: 6px; background: #E8D5BE; border-radius: 3px; overflow: hidden; }}
.occ-fill {{ height: 100%; width: 0%; transition: width 0.5s ease; }}
.occ-sub {{ font-size: 11px; color: #C8956C; margin-top: 2px; }}
.occ-total {{ border-top: 1px solid #F2E8D9; padding-top: 8px; margin-top: 6px; display: flex; justify-content: space-between; align-items: center; }}
.occ-total-lbl {{ font-size: 12px; color: #7A4A2E; font-weight: 500; }}
.occ-total-val {{ font-size: 14px; font-weight: 700; color: #1C0F08; }}

#event-log {{ max-height: 95px; overflow-y: auto; }}
.event-row {{ display: flex; align-items: center; gap: 8px; padding: 6px 0; border-bottom: 1px solid #F2E8D9; font-size: 12px; }}
.event-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
.event-msg {{ color: #7A4A2E; flex: 1; font-weight: 500; }}
.event-time {{ color: #C8956C; font-family: 'Share Tech Mono', monospace; font-size: 11px; }}
.event-empty {{ font-size: 11px; color: #C8956C; text-align: center; padding: 10px 0; }}

.barista-row {{ margin-top: 10px; padding-top: 8px; border-top: 1px solid #F2E8D9; display: flex; align-items: center; justify-content: space-between; }}
.barista-lbl {{ font-size: 11px; color: #C8956C; }}
.barista-icons {{ display: flex; gap: 4px; }}
.barista-icon {{ width: 24px; height: 24px; border-radius: 50%; background: #2D1810; display: flex; align-items: center; justify-content: center; font-size: 11px; }}

#canvas-panel {{ background: #FDFAF6; border: 1px solid #E8D5BE; border-radius: 16px; padding: 16px; width: 100%; }}
#canvas-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }}
#canvas-title {{ font-size: 13px; font-weight: 600; color: #1C0F08; }}
#canvas-sub {{ font-size: 11px; color: #C8956C; }}

#speed-row {{ display: flex; gap: 4px; align-items: center; }}
#speed-lbl {{ font-size: 11px; color: #C8956C; margin-right: 4px; }}
.spd-btn {{ padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 500; border: 1px solid #E8D5BE; cursor: pointer; background: #FDFAF6; color: #7A4A2E; transition: all 0.15s; }}
.spd-btn.active {{ background: #A86B3C; color: #FDFAF6; border-color: #A86B3C; font-weight: 600; }}

#canvas-wrap {{ position: relative; border-radius: 12px; overflow: hidden; background: #1A0A02; width: 100%; aspect-ratio: 1160 / 800; }}
#c {{ display: block; width: 100%; height: 100%; object-fit: contain; }}

#warmup-ov {{
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(10,4,2,0.93); display: flex; flex-direction: column;
  align-items: center; justify-content: center; z-index: 20; border-radius: 12px;
}}
#wu-title {{ font-family: 'Share Tech Mono', monospace; font-size: 18px; color: #E8D5BE; letter-spacing: 1.5px; }}
#wu-sub {{ font-size: 11px; color: #7A4A2E; margin-top: 4px; }}
#wu-detail {{ font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #C8956C; margin-top: 4px; }}
#wu-bar-wrap {{ margin-top: 12px; width: 240px; height: 5px; background: #3D2314; border-radius: 3px; overflow: hidden; }}
#wu-bar {{ height: 100%; width: 0%; background: #C8956C; border-radius: 3px; transition: width 0.05s; }}
</style>
</head>
<body>
<div id="app">
  <header id="hdr">
    <div id="hdr-title-panel">
      <span style="font-size:18px">☕</span>
      <div>
        <div id="hdr-title">Kopi Kenangan Kaliurang</div>
        <div id="hdr-sub">Discrete Event Simulation Dashboard</div>
      </div>
    </div>
    <div id="hdr-right">
      <div class="live-badge">
        <span class="live-dot"></span>
        <span id="live-label">READY</span>
      </div>
      <div id="hdr-clock">
        <div id="hdr-time">09:00</div>
        <div id="hdr-shift">{shift_key} · {hari}</div>
      </div>
      <div style="display:flex; gap:6px">
        <button class="hbtn hbtn-primary" id="btn-start" onclick="simStart()">▶ Start</button>
        <button class="hbtn hbtn-pause" id="btn-pause" onclick="simPause()" style="display:none">⏸ Pause</button>
      </div>
    </div>
  </header>

  <div id="metrics">
    <div class="mcard">
      <div class="mcard-header"><span class="mcard-lbl">Active Customers</span><span class="mcard-icon">👥</span></div>
      <div class="mcard-val" id="m-active">0</div>
      <div class="mcard-sub">inside the cafe</div>
      <div class="mbar"><div class="mbar-fill" id="mb-active" style="background:#A86B3C"></div></div>
    </div>
    <div class="mcard">
      <div class="mcard-header"><span class="mcard-lbl">Cashier Queue</span><span class="mcard-icon">🧾</span></div>
      <div class="mcard-val" id="m-queue">0</div>
      <div class="mcard-sub">waiting to order</div>
      <div class="mbar"><div class="mbar-fill" id="mb-queue" style="background:#D4844A"></div></div>
    </div>
    <div class="mcard">
      <div class="mcard-header"><span class="mcard-lbl">Served (Total)</span><span class="mcard-icon">✓</span></div>
      <div class="mcard-val" id="m-served">0</div>
      <div class="mcard-sub">successful transactions</div>
      <div class="mbar"><div class="mbar-fill" id="mb-served" style="background:#6B8F71"></div></div>
    </div>
    <div class="mcard">
      <div class="mcard-header"><span class="mcard-lbl">Loss (Balking)</span><span class="mcard-icon">↗</span></div>
      <div class="mcard-val" id="m-loss">0</div>
      <div class="mcard-sub">left because it was crowded</div>
      <div class="mbar"><div class="mbar-fill" id="mb-loss" style="background:#C4847A"></div></div>
    </div>
  </div>

  <div id="mid-row">
    <div id="occ-panel">
      <div class="panel-title">Real-Time Seat Occupancy</div>
      <div class="occ-row">
        <div class="occ-top"><span class="occ-lbl">Floor 1 — Indoor</span><span class="occ-pct" id="op1" style="color:#A86B3C">0%</span></div>
        <div class="occ-bar"><div class="occ-fill" id="ob1" style="background:#A86B3C"></div></div>
        <div class="occ-sub" id="os1">0 / 44 seats</div>
      </div>
      <div class="occ-row">
        <div class="occ-top"><span class="occ-lbl">Floor 2 — Indoor</span><span class="occ-pct" id="op2" style="color:#D4844A">0%</span></div>
        <div class="occ-bar"><div class="occ-fill" id="ob2" style="background:#D4844A"></div></div>
        <div class="occ-sub" id="os2">0 / 42 seats</div>
      </div>
      <div class="occ-row">
        <div class="occ-top"><span class="occ-lbl">Floor 2 — Outdoor</span><span class="occ-pct" id="op3" style="color:#6B8F71">0%</span></div>
        <div class="occ-bar"><div class="occ-fill" id="ob3" style="background:#6B8F71"></div></div>
        <div class="occ-sub" id="os3">0 / 32 seats</div>
      </div>
      <div class="occ-total">
        <div class="occ-total-lbl">Total Seat Utilization (Maximum Cafe Capacity)</div>
        <div class="occ-total-val" id="occ-total-pct">0%</div>
      </div>
    </div>

    <div id="event-panel">
      <div class="panel-title">Agent Activity Event Log</div>
      <div id="event-log"><div class="event-empty">Click Start to trigger the stochastic event log...</div></div>
      <div class="barista-row">
        <div class="barista-lbl">Active Baristas on Duty:</div>
        <div class="barista-icons" id="barista-icons"></div>
      </div>
    </div>
  </div>

  <div id="canvas-panel">
    <div id="canvas-header">
      <div>
        <div id="canvas-title">Spatial Layout & Movement</div>
        <div id="canvas-sub">Integrated 2D floor 1 and floor 2 map</div>
      </div>
      <div id="speed-row">
        <span id="speed-lbl">Speed:</span>
        <button class="spd-btn active" onclick="setSpeed(1,this)">1×</button>
        <button class="spd-btn" onclick="setSpeed(2,this)">2×</button>
        <button class="spd-btn" onclick="setSpeed(3,this)">3×</button>
        <button class="spd-btn" onclick="setSpeed(5,this)">5×</button>
      </div>
    </div>

    <div id="canvas-wrap">
      <canvas id="c" width="1160" height="800"></canvas>
      <div id="warmup-ov">
        <div id="wu-title">⚙️ PREPARING INITIAL CAFE CONDITIONS...</div>
        <div id="wu-sub">Fast-forwarding spatially to the selected operating hours</div>
        <div id="wu-detail"></div>
        <div id="wu-bar-wrap"><div id="wu-bar"></div></div>
      </div>
    </div>
  </div>
</div>

<script>
let SIM_SPEED = 1;
let simRunning = false;
let rafId = null;
let served_total = 0;
let lossCustomer = 0;
let eventLog = [];
let uiThrottle = 0;

const cv = document.getElementById('c');
const ctx = cv.getContext('2d');
const W = 1160, H = 800;

const FPS = 60;
const FRAMES_PER_SIM_MINUTE = 120;
const COLAB_FRAME_RATE = 30;

const C = {{
  bg1:'#1C0D05', bg2:'#221005', bgOut:'#182608',
  divider:'#6C4E31', table:'#FFEAC5', tableStroke:'#FFDBB5', tableText:'#603F26',
  seatFree:'#A3C47C', seatRes:'#F59E0B', seatTaken:'#C0392B',
  kasirBg:'#3D1A08', kasirStroke:'#FFDBB5', kasirBlock:'#603F26', pkupBlock:'#7C3A14',
  barista:'#FFEAC5', baristaStroke:'#FFDBB5',
  stair:'#2A1508', stairStroke:'#6C4E31', stairText:'#FFDBB5',
  door:'#6C4E31', doorText:'#FFEAC5',
  outdoorLine:'#4CAF50', outdoorText:'#A3C47C',
  custM:'#03cffc', custF:'#d672a7', custD:'#6B8F71', custShadow:'rgba(0,0,0,0.4)'
}};

const KASIR_MENIT_MIN = 0.2, KASIR_MENIT_MAX = 3.0;
const PICKUP_MENIT_MIN = 0.1, PICKUP_MENIT_MAX = 3.0;
const DX = 550, OY = 520;
const P1 = {{x:275, y:60}};
const TG1 = {{x:80, y:640, w:320, h:42}};
const TG2 = {{x:668, y:72, w:292, h:42}};
const P2 = {{x:660, y:515}};
const PMBX = 810;
const KSR = {{x:360, y:180, w:72, h:164}};
const PKUP = {{x:360, y:350, w:72, h:36}};

const HARI_AKTIF = "{hari}";
const SHIFT_AWAL = "{shift_key}";

const CONFIG_PROB_HARI = {{
  "Weekday": {{ spawnDriver:0.114, groupFemale:0.688, groupMale:0.26, groupMixed:0.052, takeAway:0.154, pilihOutdoor:0.167, peluangBalkingSaatPadat:0.000 }},
  "Weekend": {{ spawnDriver:0.082, groupFemale:0.686, groupMale:0.268, groupMixed:0.046, takeAway:0.197, pilihOutdoor:0.286, peluangBalkingSaatPadat:0.105 }}
}};

const PETA_KERAMAIAN = {{
  "Weekday": {{
    "Morning":  {{laju:159, durasiMin:60,  durasiMax:660, mulai:9,  selesai:12}},
    "Afternoon": {{laju:159, durasiMin:90,  durasiMax:660, mulai:12, selesai:15}},
    "Evening":  {{laju:150, durasiMin:90,  durasiMax:660, mulai:15, selesai:18}},
    "Night": {{laju:168, durasiMin:60,  durasiMax:660, mulai:18, selesai:20}}
  }},
  "Weekend": {{
    "Morning":  {{laju:127, durasiMin:120, durasiMax:660, mulai:9,  selesai:12}},
    "Afternoon": {{laju:115, durasiMin:120, durasiMax:660, mulai:12, selesai:15}},
    "Evening":  {{laju:176, durasiMin:120, durasiMax:660, mulai:15, selesai:18}},
    "Night": {{laju:112, durasiMin:120, durasiMax:660, mulai:18, selesai:20}}
  }}
}};

const POS_L1=[
  {{x:80,y:100}},{{x:148,y:100}},{{x:216,y:100}},{{x:360,y:100}},{{x:430,y:100}},
  {{x:80,y:175}},{{x:148,y:175}},{{x:80,y:245}},{{x:80,y:315}},{{x:80,y:385}},
  {{x:80,y:455}},{{x:80,y:525}},{{x:360,y:430}},{{x:430,y:430}},{{x:360,y:500}},
  {{x:430,y:500}},{{x:430,y:640}},{{x:80,y:595}},{{x:150,y:595}},{{x:220,y:595}},
  {{x:290,y:595}},{{x:360,y:595}}
];
const POS_L2=[
  {{x:590,y:80}},{{x:590,y:150}},{{x:590,y:220,dir:'h'}},{{x:590,y:260,dir:'h'}},
  {{x:590,y:320,dir:'h'}},{{x:590,y:360,dir:'h'}},{{x:590,y:420,dir:'h'}},{{x:590,y:460,dir:'h'}},
  {{x:740,y:240,dir:'4'}},{{x:740,y:340,dir:'4'}},{{x:740,y:440,dir:'4'}},
  {{x:850,y:240,dir:'h'}},{{x:850,y:280,dir:'h'}},{{x:850,y:380,dir:'h'}},{{x:850,y:420,dir:'h'}},
  {{x:980,y:150,dir:'h'}},{{x:980,y:220,dir:'h'}},{{x:980,y:260,dir:'h'}},{{x:980,y:330,dir:'h'}},
  {{x:980,y:370,dir:'h'}},{{x:980,y:440,dir:'h'}},
  {{x:590,y:540,dir:'h'}},{{x:590,y:580,dir:'h'}},{{x:740,y:540,dir:'h'}},{{x:740,y:580,dir:'h'}},
  {{x:865,y:540,dir:'h'}},{{x:865,y:580,dir:'h'}},{{x:980,y:540,dir:'h'}},{{x:980,y:580,dir:'h'}},
  {{x:590,y:640,dir:'h'}},{{x:590,y:680,dir:'h'}},{{x:740,y:640,dir:'h'}},{{x:740,y:680,dir:'h'}},
  {{x:865,y:640,dir:'h'}},{{x:865,y:680,dir:'h'}},{{x:980,y:640,dir:'h'}},{{x:980,y:680,dir:'h'}}
];

function menitKeFrame(m) {{ return Math.round(m * FRAMES_PER_SIM_MINUTE); }}

function buildTables(){{
  const tables=[]; let tid=1;
  POS_L1.forEach(p=>{{
    tables.push({{id:tid,floor:1,ref:p,seats:[
      {{x:p.x-9,y:p.y+15,taken:false,reserved:false}},
      {{x:p.x+38,y:p.y+15,taken:false,reserved:false}}
    ]}});tid++;
  }});
  POS_L2.forEach(p=>{{
    let sArr=[];
    if(p.dir==='4') sArr=[
      {{x:p.x+15,y:p.y-11,taken:false,reserved:false}},
      {{x:p.x+15,y:p.y+40,taken:false,reserved:false}},
      {{x:p.x-11,y:p.y+15,taken:false,reserved:false}},
      {{x:p.x+40,y:p.y+15,taken:false,reserved:false}}
    ];
    else if(p.dir==='h') sArr=[
      {{x:p.x-11,y:p.y+15,taken:false,reserved:false}},
      {{x:p.x+40,y:p.y+15,taken:false,reserved:false}}
    ];
    else sArr=[
      {{x:p.x+15,y:p.y-11,taken:false,reserved:false}},
      {{x:p.x+15,y:p.y+40,taken:false,reserved:false}}
    ];
    tables.push({{id:tid,floor:2,ref:p,seats:sArr}});tid++;
  }});
  return tables;
}}

let jamTarget = PETA_KERAMAIAN[HARI_AKTIF][SHIFT_AWAL].mulai;
let jamMulaiSimulasi = 9, totalFrameSimulasi = 0;
let currentConfig, LAJU, BARISTA, spawnT;
let allTables, customers, kasirQ, pickupQ, nextId, nextGroupId, seatPopulation=[];

function initSimState() {{
  currentConfig = getConfigAktif(9);
  LAJU = currentConfig.laju;
  BARISTA = hitungJumlahBarista(HARI_AKTIF, 9);
  
  let lajuMenit = LAJU / COLAB_FRAME_RATE;
  spawnT = menitKeFrame(lajuMenit * (0.6 + Math.random() * 0.8));
  
  if (allTables && allTables.length > 0) {{
    allTables.forEach(t => {{
      t.seats.forEach(s => {{
        s.taken = false;
        s.reserved = false;
      }});
    }});
  }} else {{
    allTables = buildTables();
  }}
  customers = []; kasirQ = []; pickupQ = [];
  nextId = 0; lossCustomer = 0; nextGroupId = 100;
  seatPopulation = []; served_total = 0; eventLog = [];
}}

function getConfigAktif(jam){{
  const d=PETA_KERAMAIAN[HARI_AKTIF];
  if(jam>=9&&jam<12) return {{key:"Morning",...d["Morning"]}};
  if(jam>=12&&jam<15) return {{key:"Afternoon",...d["Afternoon"]}};
  if(jam>=15&&jam<18) return {{key:"Evening",...d["Evening"]}};
  return {{key:"Night",...d["Night"]}};
}}

function hitungJumlahBarista(hari, jam) {{
  if (hari === "Weekday") {{
    if (jam>=9&&jam<12) return 2;
    if (jam>=12&&jam<15) return 1;
    if (jam>=15&&jam<18) return 2;
    return 2;
  }} else {{
    return 3;
  }}
}}

function isFree(s){{return !s.taken&&!s.reserved;}}

function buatTimerDuduk(cfg) {{
  let durasi = cfg.durasiMin + Math.random()*(cfg.durasiMax-cfg.durasiMin);
  const totalMenitSim = totalFrameSimulasi / FRAMES_PER_SIM_MINUTE;
  const waktuSkrgMenit = (jamMulaiSimulasi * 60) + totalMenitSim;
  const waktuTutupMenit = 20 * 60;
  
  const sisaWaktuBuka = waktuTutupMenit - waktuSkrgMenit;
  if (durasi > sisaWaktuBuka) {{
    durasi = Math.max(1, sisaWaktuBuka);
  }}
  return menitKeFrame(durasi);
}}

function alokasikanKursi(tipeK,ukuranK,areaPilihan){{
  const prob=CONFIG_PROB_HARI[HARI_AKTIF];
  let meja=allTables.filter(t=>{{
    let isOut=(t.floor===2&&t.ref.y>=520);
    return areaPilihan==='OUTDOOR'?isOut:!isOut;
  }});
  if(!meja.length||meja.reduce((a,t)=>a+t.seats.filter(s=>isFree(s)).length,0)<ukuranK) meja=allTables;
  const mejaKosong=meja.filter(t=>t.seats.every(s=>isFree(s)));
  if(mejaKosong.length>0){{
    const t=mejaKosong[Math.floor(Math.random()*mejaKosong.length)];
    const k=t.seats.filter(s=>isFree(s)).slice(0,ukuranK);
    k.forEach(s=>s.reserved=true); return k;
  }}
  if(Math.random()<prob.peluangBalkingSaatPadat) return null;
  const mejaCukup=meja.filter(t=>t.seats.filter(s=>isFree(s)).length>=ukuranK);
  if(mejaCukup.length>0){{
    const t=mejaCukup[Math.floor(Math.random()*mejaCukup.length)];
    const k=t.seats.filter(s=>isFree(s)).slice(0,ukuranK);
    k.forEach(s=>s.reserved=true); return k;
  }}
  const semua=[];
  meja.forEach(t=>t.seats.filter(s=>isFree(s)).forEach(s=>semua.push(s)));
  if(semua.length>=ukuranK){{
    semua.sort(()=>Math.random()-0.5);
    const k=semua.slice(0,ukuranK);
    k.forEach(s=>s.reserved=true); return k;
  }}
  return null;
}}

function bebaskanKursi(s){{if(s){{s.taken=false;s.reserved=false;}}}}

class Cust {{
  constructor(id,gId,tipeK,seat,timerDuduk,g,isTakeAway,area){{
    this.id=id;this.groupId=gId;this.tipeK=tipeK;
    this.timerDuduk=timerDuduk;this.timer=0;this.spd=4.5;
    this.x=P1.x+26;this.y=P1.y+14;
    this.assignedSeat=seat||null;this.scoutTimer=100;
    this.g=g;this.isTakeAway=isTakeAway;this.area=area;
    this.col=g==='D'?C.custD:g==='M'?C.custM:C.custF;
    if(tipeK==='DRIVER'){{
      this.st='TO_PICKUP';
      this.timerPickup=menitKeFrame(PICKUP_MENIT_MIN+Math.random()*(PICKUP_MENIT_MAX-PICKUP_MENIT_MIN));
      this.timerKasir=0;
      pickupQ.push(this);
    }} else if(isTakeAway||seat){{
      this.st='TO_KASIR';
      this.timerKasir  = menitKeFrame(KASIR_MENIT_MIN  + Math.random()*(KASIR_MENIT_MAX-KASIR_MENIT_MIN));
      this.timerPickup = menitKeFrame(PICKUP_MENIT_MIN + Math.random()*(PICKUP_MENIT_MAX-PICKUP_MENIT_MIN));
      kasirQ.push(this);
    }} else {{
      this.st='SCOUT_GO_UP';
      this.timerKasir=0; this.timerPickup=0;
    }}
  }}

  static buatDuduk(id,gId,seat,timerSisa,g,cfg){{
    const inst=Object.create(Cust.prototype);
    inst.id=id; inst.groupId=gId; inst.tipeK='KELOMPOK_SOLO';
    inst.g=g; inst.col=g==='D'?C.custD:g==='M'?C.custM:C.custF;
    inst.isTakeAway=false; inst.area='INDOOR';
    inst.spd=4.5; inst.scoutTimer=100; 
    inst.assignedSeat=seat;
    inst.timerDuduk=timerSisa;
    inst.timer=timerSisa;
    inst.timerKasir=0; inst.timerPickup=0;
    inst.x=seat.x; inst.y=seat.y;
    inst.st='SIT';
    seat.reserved=false; seat.taken=true;
    return inst;
  }}

  mv(tx,ty){{
    const dx=tx-this.x,dy=ty-this.y,d=Math.sqrt(dx*dx+dy*dy);
    if(d<this.spd){{this.x=tx;this.y=ty;return true;}}
    this.x+=dx/d*this.spd;this.y+=dy/d*this.spd;return false;
  }}

  upd() {{
    const qi=kasirQ.indexOf(this);
    if(this.st==='SCOUT_GO_UP'){{
      if(this.mv(TG1.x+300,TG1.y+21)){{this.x=TG2.x+30;this.y=TG2.y+21;this.st='SCOUTING';this.scoutTimer=100;}}
    }}
    else if(this.st==='SCOUTING'){{if(this.mv(700,180)){{if(--this.scoutTimer<=0)this.st='SCOUT_GO_DOWN';}}}}
    else if(this.st==='SCOUT_GO_DOWN'){{
      if(this.mv(TG2.x+30,TG2.y+21)){{this.x=TG1.x+300;this.y=TG1.y+21;this.st='SCOUT_LEAVE';}}
    }}
    else if(this.st==='SCOUT_LEAVE'){{
      if(this.mv(P1.x+26,P1.y+40)){{lossCustomer++;addEvent('balking');this.st='LEAVE';}}
    }}
    else if(this.st==='TO_KASIR'){{
      if(qi>=0){{
        const targetX=KSR.x-40-(qi*25), targetY=KSR.y+70;
        if(this.mv(targetX,targetY)&&qi===0) this.st='AT_KASIR';
      }}
    }}
    else if(this.st==='AT_KASIR'){{
      if(kasirQ.indexOf(this)>0){{this.st='TO_KASIR';}}
      else{{if(--this.timerKasir<=0){{kasirQ.splice(0,1);pickupQ.push(this);this.st='TO_PICKUP';}}}}
    }}
    else if(this.st==='TO_PICKUP'){{
      const pi=pickupQ.indexOf(this);
      const ok=this.mv(PKUP.x-30-pi*22,PKUP.y+19);
      if(pi===0&&ok){{
        if(--this.timerPickup<=0){{
          pickupQ.splice(0,1);
          served_total++;
          addEvent('served');
          if(this.tipeK==='DRIVER'||this.isTakeAway){{
            this.st='LEAVE';}}
          else{{
            this.assignedSeat.reserved=false;this.assignedSeat.taken=true;
            this.timer=this.timerDuduk;
            const m=allTables.find(t=>t.seats.includes(this.assignedSeat));
            this.st=m.floor===1?'TO_S1':'UP_STAIR';
          }}
        }}
      }}
    }}
    else if(this.st==='TO_S1'){{if(this.mv(this.assignedSeat.x,this.assignedSeat.y))this.st='SIT';}}
    else if(this.st==='UP_STAIR'){{
      if(this.mv(TG1.x+300,TG1.y+21)){{
        this.x=TG2.x+30;this.y=TG2.y+21;
        const m=allTables.find(t=>t.seats.includes(this.assignedSeat));
        this.st=m&&m.ref.y>=520?'TO_P2_IN':'TO_S2';
      }}
    }}
    else if(this.st==='TO_P2_IN'){{if(this.mv(P2.x+24,P2.y))this.st='TO_S2';}}
    else if(this.st==='TO_S2'){{if(this.mv(this.assignedSeat.x,this.assignedSeat.y))this.st='SIT';}}
    else if(this.st==='SIT'){{
      if(--this.timer<=0){{
        const m=allTables.find(t=>t.seats.includes(this.assignedSeat));
        this.st=m&&m.floor===1?'LEAVE':'LEAVE_OUTDOOR_CHECK';
      }}
    }}
    else if(this.st==='LEAVE_OUTDOOR_CHECK'){{
      const m=allTables.find(t=>t.seats.includes(this.assignedSeat));
      this.st=m&&m.ref.y>=520?'TO_P2_OUT':'DN_STAIR';
    }}
    else if(this.st==='TO_P2_OUT'){{if(this.mv(P2.x+24,P2.y))this.st='DN_STAIR';}}
    else if(this.st==='DN_STAIR'){{
      if(this.assignedSeat){{bebaskanKursi(this.assignedSeat);this.assignedSeat=null;}}
      if(this.mv(TG2.x+30,TG2.y+21)){{this.x=TG1.x+300;this.y=TG1.y+21;this.st='LEAVE';}}
    }}
    else if(this.st==='LEAVE'){{
      if(this.assignedSeat){{bebaskanKursi(this.assignedSeat);this.assignedSeat=null;}}
      return this.mv(P1.x+26,P1.y-20);
    }}
    return false;
  }}

  draw() {{
    ctx.beginPath();ctx.arc(this.x+1,this.y+2,10,0,Math.PI*2);
    ctx.fillStyle=C.custShadow;ctx.fill();
    let r=10;
    if(this.st==='SCOUTING'&&this.scoutTimer<100) r=10+Math.sin(this.scoutTimer*0.35)*1.5;
    ctx.beginPath();ctx.arc(this.x,this.y,r,0,Math.PI*2);
    ctx.fillStyle=this.col;ctx.fill();
    ctx.strokeStyle='rgba(255,234,197,0.7)';ctx.lineWidth=1.5;ctx.stroke();
    ctx.fillStyle='#fff';ctx.font='bold 9px DM Sans';
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(this.g,this.x,this.y);ctx.textBaseline='alphabetic';
    if(this.st==='SCOUTING'&&this.scoutTimer<100){{
      ctx.fillStyle='#D4844A';ctx.font='bold 13px serif';ctx.textAlign='center';
      ctx.fillText('❓',this.x,this.y-r-7+Math.sin(this.scoutTimer*0.35)*2);
    }}
  }}
}}

function addEvent(type) {{
  const totalMenitSim = totalFrameSimulasi / FRAMES_PER_SIM_MINUTE;
  const jam = jamMulaiSimulasi + Math.floor(totalMenitSim / 60);
  const min = Math.floor(totalMenitSim % 60);
  const t = String(jam).padStart(2,'0')+':'+String(min).padStart(2,'0');
  const msgs = {{served:'Customer served', balking:'Customer left (balking)', arrival:'Customer arrived'}};
  const colors = {{served:'#6B8F71', balking:'#C4847A', arrival:'#A86B3C'}};
  eventLog.unshift({{msg: msgs[type]||type, t, color: colors[type]||'#A86B3C'}});
  if (eventLog.length > 12) eventLog.pop();
  renderEventLog();
}}

function renderEventLog() {{
  const el = document.getElementById('event-log');
  if (!eventLog.length) {{
    el.innerHTML = '<div class="event-empty">Click Start to trigger the stochastic event log...</div>';
    return;
  }}
  let html = '';
  for (let i = 0; i < Math.min(eventLog.length, 6); i++) {{
    const e = eventLog[i];
        html += '<div class="event-row">' +
          '<span class="event-dot" style="background:' + e.color + '"></span>' +
          '<span class="event-msg">' + e.msg + '</span>' +
          '<span class="event-time">' + e.t + '</span>' +
          '</div>';
  }}
  el.innerHTML = html;
}}

function spawnGelombang_warmup() {{
  const prob=CONFIG_PROB_HARI[HARI_AKTIF];
  if(Math.random()<prob.spawnDriver) return;
  const ukuranK=Math.random()<0.81?1:2;
  if(Math.random()<prob.takeAway) return;
  const area=Math.random()<prob.pilihOutdoor?'OUTDOOR':'INDOOR';
  const pG=Math.random();
  let g='F';
  if(pG>=prob.groupFemale&&pG<prob.groupFemale+prob.groupMale) g='M';
  else if(pG>=prob.groupFemale+prob.groupMale) g='X';
  const kursi=alokasikanKursi('KELOMPOK',ukuranK,area);
  if(!kursi) return;
  
  let timerMenit = currentConfig.durasiMin + Math.random()*(currentConfig.durasiMax-currentConfig.durasiMin);
  const jamSkrgWarmup = currentConfig.mulai;
  const waktuTutupMenit = 20 * 60;
  const sisaWaktuBuka = waktuTutupMenit - (jamSkrgWarmup * 60);
  if (timerMenit > sisaWaktuBuka) {{
    timerMenit = Math.max(1, sisaWaktuBuka);
  }}

  kursi.forEach(s=>{{
    const gender=g==='X'?(Math.random()<0.5?'M':'F'):g;
    s.reserved=false; s.taken=true;
    seatPopulation.push({{seat:s, g:gender, timerSisa:timerMenit}});
  }});
}}

function spawnGelombangLive() {{
  const prob=CONFIG_PROB_HARI[HARI_AKTIF];
  if(Math.random()<prob.spawnDriver){{
    customers.push(new Cust(++nextId,nextGroupId++,'DRIVER',null,0,'D',true,'NONE'));
    addEvent('arrival'); return;
  }}
  const ukuranK=Math.random()<0.81?1:2;
  const gId=nextGroupId++, td=buatTimerDuduk(currentConfig);
  const isTW=Math.random()<prob.takeAway;
  const area=Math.random()<prob.pilihOutdoor?'OUTDOOR':'INDOOR';
  const pG=Math.random();
  let jenisGender='F';
  if(pG<prob.groupFemale) jenisGender='F';
  else if(pG<prob.groupFemale+prob.groupMale) jenisGender='M';
  else jenisGender='X';
  const kursi=isTW?null:alokasikanKursi('KELOMPOK',ukuranK,area);
  for(let k=0;k<ukuranK;k++){{
    const g=jenisGender==='X'?(Math.random()<0.5?'M':'F'):jenisGender;
    customers.push(new Cust(++nextId,gId,'KELOMPOK',kursi?kursi[k]:null,td,g,isTW,area));
  }}
  addEvent('arrival');
}}

function doWarmUp(autoResume = false) {{
  const ov=document.getElementById('warmup-ov');
  if(jamTarget<=9){{
    ov.style.display='none';
    if(autoResume) simStart();
    return;
  }}
  const selisihMenit=(jamTarget-9)*60;
  const bar=document.getElementById('wu-bar');
  const detail=document.getElementById('wu-detail');
  ov.style.display='flex';ov.style.opacity='1';
  let menitDiproses=0;
  const BATCH=15;

  function tick() {{
    for(let b=0;b<BATCH&&menitDiproses<selisihMenit;b++,menitDiproses++){{
      const jamSkrg=9+Math.floor(menitDiproses/60);
      currentConfig=getConfigAktif(jamSkrg);
      LAJU=currentConfig.laju;
      BARISTA=hitungJumlahBarista(HARI_AKTIF,jamSkrg);
      
      const lajuMenit = LAJU / COLAB_FRAME_RATE;
      const spawnPerMenit = 1 / lajuMenit;
      const nSpawn = Math.floor(spawnPerMenit) + (Math.random() < (spawnPerMenit % 1) ? 1 : 0);
      for(let s=0;s<nSpawn;s++) spawnGelombang_warmup();
      
      for(let i=seatPopulation.length-1;i>=0;i--){{
        seatPopulation[i].timerSisa -= 1;
        if(seatPopulation[i].timerSisa<=0){{
          const s=seatPopulation[i].seat;
          s.taken=false; s.reserved=false;
          seatPopulation.splice(i,1);
        }}
      }}
    }}
    bar.style.width=Math.round((menitDiproses/selisihMenit)*100)+'%';
    detail.textContent='Menghitung Kepadatan Jam '+
      String(9+Math.floor(menitDiproses/60)).padStart(2,'0')+':'+
      String(menitDiproses%60).padStart(2,'0');

    if(menitDiproses<selisihMenit){{requestAnimationFrame(tick);}}
    else{{
      kasirQ=[];pickupQ=[];customers=[];
      seatPopulation.forEach(entry=>{{
        const timerFrame = menitKeFrame(entry.timerSisa);
        const timerSisa = Math.max(
          menitKeFrame(1),
          Math.floor(timerFrame*(0.3+Math.random()*0.6))
        );
        customers.push(Cust.buatDuduk(++nextId, nextGroupId++, entry.seat, timerSisa, entry.g, currentConfig));
      }});
      seatPopulation=[];
      jamMulaiSimulasi=jamTarget; totalFrameSimulasi=0; 
      currentConfig=getConfigAktif(jamTarget);
      LAJU=currentConfig.laju; BARISTA=hitungJumlahBarista(HARI_AKTIF,jamTarget);
      
      let lajuMenit = LAJU / COLAB_FRAME_RATE;
      spawnT = menitKeFrame(lajuMenit * (0.6 + Math.random() * 0.8));
      
      ov.style.transition='opacity .4s';ov.style.opacity='0';
      setTimeout(()=>{{
        ov.style.display='none';
        if(autoResume) simStart();
      }},400);
    }}
  }}
  tick();
}}

function fillRR(x,y,w,h,r,fill,stroke,lw){{
  ctx.beginPath();ctx.roundRect(x,y,w,h,r);
  if(fill){{ctx.fillStyle=fill;ctx.fill();}}
  if(stroke){{ctx.strokeStyle=stroke;ctx.lineWidth=lw||1.5;ctx.stroke();}}
}}

function drawBG() {{
  ctx.fillStyle=C.bg1;ctx.fillRect(0,0,DX,H);
  ctx.fillStyle=C.bg2;ctx.fillRect(DX,0,W-DX,H);
  ctx.fillStyle=C.bgOut;ctx.fillRect(DX,OY,W-DX,H-OY);
  ctx.strokeStyle=C.divider;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(DX,0);ctx.lineTo(DX,H);ctx.stroke();
  ctx.strokeStyle='#2D5016';ctx.lineWidth=1.5;ctx.setLineDash([6,4]);
  ctx.beginPath();ctx.moveTo(PMBX,190);ctx.lineTo(PMBX,OY-10);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle=C.tableStroke;ctx.font='bold 12px DM Sans';ctx.textAlign='left';
  ctx.fillText('FLOOR 1 — INDOOR',16,20);
  ctx.fillText('FLOOR 2 — INDOOR & OUTDOOR',DX+16,20);
  fillRR(P1.x,P1.y,52,11,3,C.door,C.tableStroke,1.5);
  fillRR(KSR.x-10,KSR.y-12,KSR.w+20,KSR.h+PKUP.h+38,10,C.kasirBg,C.kasirStroke,1.5);
  fillRR(KSR.x,KSR.y,KSR.w,KSR.h,6,C.kasirBlock,null);
  fillRR(PKUP.x,PKUP.y,PKUP.w,PKUP.h,6,C.pkupBlock,null);
  ctx.fillStyle=C.tableStroke;ctx.font='bold 10px DM Sans';ctx.textAlign='center';
  ctx.fillText('CASHIER',KSR.x+36,KSR.y+90);
  ctx.fillText('PICK-UP',PKUP.x+36,PKUP.y+24);
  for(let b=0;b<BARISTA;b++){{
    const bx=KSR.x+KSR.w+24,by=KSR.y+16+b*32;
    ctx.beginPath();ctx.ellipse(bx,by,30,13,0,0,Math.PI*2);
    ctx.fillStyle=C.kasirBg;ctx.fill();
    ctx.strokeStyle=C.baristaStroke;ctx.lineWidth=1.5;ctx.stroke();
    ctx.fillStyle=C.barista;ctx.font='bold 8px DM Sans';ctx.textBaseline='middle';
    ctx.fillText('Barista '+(b+1),bx,by);ctx.textBaseline='alphabetic';
  }}
  function drawTangga(x,y,w,h,lbl,n){{
    fillRR(x,y,w,h,6,C.stair,C.stairStroke,1.5);
    for(let s=0;s<n;s++){{
      ctx.strokeStyle=C.stairStroke;ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(x+22+s*38,y+5);ctx.lineTo(x+22+s*38,y+h-5);ctx.stroke();
    }}
    ctx.fillStyle=C.stairText;ctx.font='bold 9px DM Sans';ctx.fillText(lbl,x+w/2,y+26);
  }}
  drawTangga(TG1.x,TG1.y,TG1.w,TG1.h,'STAIRS TO 2nd FLOOR',8);
  drawTangga(TG2.x,TG2.y,TG2.w,TG2.h,'STAIRS TO 1st FLOOR',7);
  ctx.strokeStyle=C.outdoorLine;ctx.lineWidth=2;ctx.setLineDash([10,6]);
  ctx.beginPath();ctx.moveTo(DX+2,OY);ctx.lineTo(W,OY);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle=C.outdoorText;ctx.font='10px DM Sans';ctx.fillText('OUTDOOR AREA',DX+50,OY-7);
  fillRR(P2.x,P2.y,48,11,3,C.door,C.tableStroke,1.5);
}}

function drawTables() {{
  allTables.forEach(t=>{{
    ctx.beginPath();ctx.roundRect(t.ref.x+2,t.ref.y+3,30,30,4);ctx.fillStyle='rgba(0,0,0,0.4)';ctx.fill();
    fillRR(t.ref.x,t.ref.y,30,30,4,C.table,C.tableStroke,1.5);
    ctx.fillStyle=C.tableText;ctx.font='bold 7px DM Sans';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText('T'+t.id,t.ref.x+15,t.ref.y+15);ctx.textBaseline='alphabetic';
    t.seats.forEach(s=>{{
      ctx.beginPath();ctx.arc(s.x,s.y,6,0,Math.PI*2);
      ctx.fillStyle=s.taken?C.seatTaken:s.reserved?C.seatRes:C.seatFree;ctx.fill();
      ctx.strokeStyle='rgba(255,234,197,0.5)';ctx.lineWidth=1.2;ctx.stroke();
    }});
  }});
}}

function updateUI(jam,menit,l1,l2,tot) {{
  uiThrottle++; if(uiThrottle%3!==0) return;
  const pad=n=>String(n).padStart(2,'0');
  document.getElementById('hdr-time').textContent=pad(jam)+':'+pad(menit);
  const active=customers.length; const queue=kasirQ.length;
  document.getElementById('m-active').textContent=active;
  document.getElementById('mb-active').style.width=Math.min(100,active*2.2)+'%';
  document.getElementById('m-queue').textContent=queue;
  document.getElementById('mb-queue').style.width=Math.min(100,queue*12)+'%';
  document.getElementById('m-served').textContent=served_total;
  document.getElementById('mb-served').style.width=Math.min(100,(served_total/Math.max(1,served_total+lossCustomer))*100)+'%';
  document.getElementById('m-loss').textContent=lossCustomer;
  document.getElementById('mb-loss').style.width=Math.min(100,lossCustomer*6)+'%';
  const SEATS_L1=44, SEATS_L2IN=42, SEATS_L2OUT=32;
  let l2in=0,l2out=0;
  allTables.filter(t=>t.floor===2).forEach(t=>{{
    const isOut=t.ref.y>=520;
    t.seats.forEach(s=>{{if(s.taken){{if(isOut)l2out++;else l2in++;}}}});
  }});
  const p1=Math.min(100,Math.round(l1/SEATS_L1*100));
  const p2i=Math.min(100,Math.round(l2in/SEATS_L2IN*100));
  const p2o=Math.min(100,Math.round(l2out/SEATS_L2OUT*100));
  const pAll=Math.min(100,Math.round((l1+l2)/tot*100));
  document.getElementById('op1').textContent=p1+'%'; document.getElementById('ob1').style.width=p1+'%';
  document.getElementById('os1').textContent=l1+' / '+SEATS_L1+' seats';
  document.getElementById('op2').textContent=p2i+'%'; document.getElementById('ob2').style.width=p2i+'%';
  document.getElementById('os2').textContent=l2in+' / '+SEATS_L2IN+' seats';
  document.getElementById('op3').textContent=p2o+'%'; document.getElementById('ob3').style.width=p2o+'%';
  document.getElementById('os3').textContent=l2out+' / '+SEATS_L2OUT+' seats';
  document.getElementById('occ-total-pct').textContent=pAll+'%';
  
  const bi=document.getElementById('barista-icons');
  bi.innerHTML=Array.from({{length:BARISTA}}).map(()=>'<div class="barista-icon">☕</div>').join('');
}}

function loop() {{
  if(!simRunning){{rafId=null;return;}}
  for(let step=0;step<SIM_SPEED;step++){{
    totalFrameSimulasi++;
    const totalMenitSim = totalFrameSimulasi / FRAMES_PER_SIM_MINUTE;
    let jamSkrg = jamMulaiSimulasi + Math.floor(totalMenitSim / 60);
    let menitSkrg = Math.floor(totalMenitSim % 60);
    
    if(jamSkrg>=20){{
      simRunning = false;
      cancelAnimationFrame(rafId);
      rafId = null;
      
      totalFrameSimulasi = 0; 
      jamMulaiSimulasi = 9; 
      
      customers=[]; kasirQ=[]; pickupQ=[]; seatPopulation=[];
      allTables.forEach(t=>t.seats.forEach(s=>{{s.taken=false;s.reserved=false;}}));
      served_total = 0;
      lossCustomer = 0;
      eventLog = [];
      renderEventLog();
      
      document.getElementById('btn-start').style.display = 'flex';
      document.getElementById('btn-pause').style.display = 'none';
      document.querySelector('.live-badge').style.background = 'rgba(196,132,122,0.15)';
      document.getElementById('live-label').textContent = 'RESETTING...';

      doWarmUp(true);
      return; 
    }}
    
    currentConfig=getConfigAktif(jamSkrg);
    LAJU=currentConfig.laju; 
    BARISTA=hitungJumlahBarista(HARI_AKTIF,jamSkrg);
    
    if(--spawnT<=0){{
      spawnGelombangLive();
      let lajuMenit = LAJU / COLAB_FRAME_RATE;
      spawnT = menitKeFrame(lajuMenit * (0.6 + Math.random() * 0.8));
    }}
    
    for(let i=customers.length-1;i>=0;i--){{
      if(customers[i].upd()) customers.splice(i,1);
    }}
  }}
  ctx.clearRect(0,0,W,H); drawBG(); drawTables();
  for(let i=0;i<customers.length;i++) customers[i].draw();
  let l1=0,l2=0,tot=0;
  allTables.forEach(t=>t.seats.forEach(s=>{{tot++;if(s.taken){{if(t.floor===1)l1++;else l2++;}}}}));
  
  const totalMenitSim2 = totalFrameSimulasi / FRAMES_PER_SIM_MINUTE;
  const jamSkrg2 = jamMulaiSimulasi + Math.floor(totalMenitSim2 / 60);
  const menitSkrg2 = Math.floor(totalMenitSim2 % 60);
  updateUI(jamSkrg2, menitSkrg2, l1, l2, tot);
  
  rafId=requestAnimationFrame(loop);
}}

function simStart() {{
  if (simRunning) return; simRunning = true;
  document.getElementById('btn-start').style.display = 'none';
  document.getElementById('btn-pause').style.display = 'flex';
  document.querySelector('.live-badge').style.background = 'rgba(107,143,113,0.3)';
  document.getElementById('live-label').textContent = 'RUNNING';
  if (!rafId) rafId = requestAnimationFrame(loop);
}}

function simPause() {{
  simRunning = false;
  document.getElementById('btn-start').style.display = 'flex';
  document.getElementById('btn-pause').style.display = 'none';
  document.querySelector('.live-badge').style.background = 'rgba(196,132,122,0.15)';
  document.getElementById('live-label').textContent = 'PAUSED';
  if (rafId) {{ cancelAnimationFrame(rafId); rafId = null; }}
}}

function setSpeed(s, btn) {{
  SIM_SPEED = s;
  document.querySelectorAll('.spd-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
}}

initSimState(); drawBG(); drawTables(); doWarmUp();
</script>
</body>
</html>
"""

st.iframe(html_code, height=700)

st.sidebar.markdown("---")
st.sidebar.markdown("### Legend — Agent Types")
st.sidebar.markdown(
    '''
    <div style="display:flex;flex-direction:column;gap:6px">
      <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#6B8F71;margin-right:8px;vertical-align:middle;"></span><strong>D</strong> — Driver</div>
      <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#03cffc;margin-right:8px;vertical-align:middle;"></span><strong>M</strong> — Male</div>
      <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#d672a7;margin-right:8px;vertical-align:middle;"></span><strong>F</strong> — Female</div>
    </div>
    ''', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Legend — Seats")
st.sidebar.markdown(
    '''
    <div style="display:flex;flex-direction:column;gap:6px">
      <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#A3C47C;margin-right:8px;vertical-align:middle;"></span>Available</div>
      <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#F59E0B;margin-right:8px;vertical-align:middle;"></span>Reserved</div>
      <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#C0392B;margin-right:8px;vertical-align:middle;"></span>Occupied</div>
    </div>
    ''', unsafe_allow_html=True)