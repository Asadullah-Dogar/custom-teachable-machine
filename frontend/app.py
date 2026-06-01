import io
import requests
import pandas as pd
import altair as alt
import streamlit as st
from PIL import Image
import textwrap

# ── Configuration & Setup ─────────────────────────────────────────────────────
# BACKEND_URL = "http://localhost:8000"
BACKEND_URL = "https://asadullahdogarr-teachable-machine-api.hf.space" 

st.set_page_config(
    page_title="Teachable Machine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS Injection (Strict AI Research Lab Theme) ───────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700;800&display=swap');

    :root {
        --bg: #080b12;
        --surface: #0d1117;
        --elevated: #111827;
        --border: rgba(255,255,255,0.06);
        --border-hover: rgba(139,92,246,0.5);
        --primary: #7c3aed;
        --secondary: #2563eb;
        --gradient: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
        --success: #059669;
        --warning: #d97706;
        --text-pri: #f1f5f9;
        --text-sec: #64748b;
        --text-mut: #334155;
    }

    /* Global Theme Overrides */
    .stApp {
        background-color: var(--bg) !important;
        background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    #MainMenu, footer, [data-testid="stHeader"] { visibility: hidden !important; display: none !important; }

    /* Typography */
    h1, h2, h3, h4, p, span, div { font-family: 'Space Grotesk', sans-serif !important; }
    h3 { font-size: 1.3rem !important; font-weight: 700 !important; color: var(--text-pri) !important; }
    p, span { color: var(--text-sec); font-size: 0.95rem; }

    /* Custom Hero Section */
    .hero-wrapper {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; padding: 3rem 2rem; margin-bottom: 2rem;
        background: radial-gradient(circle at 80% 50%, rgba(124, 58, 237, 0.15) 0%, transparent 60%);
        position: relative; overflow: hidden; border-radius: 24px;
        border: 1px solid var(--border); background-color: var(--surface);
    }
    .hero-wrapper::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><filter id="noiseFilter"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(%23noiseFilter)" opacity="0.03"/></svg>');
        pointer-events: none;
    }
    .hero-pills { display: flex; gap: 10px; margin-bottom: 1rem; }
    .hero-pill { 
        font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase;
        background: rgba(255,255,255,0.03); border: 1px solid var(--border);
        padding: 6px 12px; border-radius: 20px; color: var(--text-sec); font-weight: 700;
    }
    .hero-title {
        font-size: 3rem !important; font-weight: 800 !important; margin: 0 0 10px 0;
        background: linear-gradient(135deg, #ffffff 30%, #7c3aed 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.1;
    }
    .hero-sub { color: var(--text-sec); font-size: 1.1rem; max-width: 500px; font-weight: 500; }
    
    /* Animated SVG Brain Icon */
    .brain-icon { width: 140px; height: 140px; }
    .brain-path {
        fill: none; stroke: var(--secondary); stroke-width: 2;
        stroke-dasharray: 100; stroke-dashoffset: 100;
        animation: drawBrain 3s ease-in-out infinite alternate, glowBrain 2s infinite alternate;
    }
    .brain-node { fill: var(--primary); animation: pulseNode 1.5s infinite alternate; }
    @keyframes drawBrain { to { stroke-dashoffset: 0; } }
    @keyframes glowBrain { from { filter: drop-shadow(0 0 2px var(--secondary)); } to { filter: drop-shadow(0 0 15px var(--primary)); } }
    @keyframes pulseNode { from { transform: scale(1); opacity: 0.7; } to { transform: scale(1.5); opacity: 1; } }

    /* Sidebar Redesign */
    section[data-testid="stSidebar"] {
        background-color: #060810 !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] > div { padding: 0 !important; }
    .sidebar-top-bar { height: 3px; width: 100%; transition: background 0.3s; }
    .sidebar-status-box { padding: 10px 24px; display: flex; align-items: center; gap: 8px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; border-bottom: 1px solid var(--border); }
    .sidebar-logo-area { padding: 32px 24px 24px 24px; display: flex; align-items: center; gap: 16px; }
    .tm-monogram {
        width: 48px; height: 48px; border-radius: 12px; background: var(--gradient);
        display: flex; justify-content: center; align-items: center;
        font-weight: 800; font-size: 1.2rem; color: white; box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    }
    .tm-title { font-weight: 800; color: var(--text-pri); font-size: 1.1rem; line-height: 1.2; }
    .tm-version { font-size: 0.75rem; color: var(--text-sec); font-weight: 500; }
    .sidebar-content-padding { padding: 0 24px; }

    /* Readiness Segmented Meter */
    .readiness-container { display: flex; justify-content: space-between; align-items: center; margin: 15px 0 30px 0; position: relative; }
    .readiness-line { position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: var(--border); z-index: 0; transform: translateY(-50%); }
    .readiness-line-fill { position: absolute; top: 50%; left: 0; height: 2px; background: var(--gradient); z-index: 0; transform: translateY(-50%); transition: width 0.5s; }
    .readiness-dot { width: 14px; height: 14px; border-radius: 50%; background: var(--surface); border: 2px solid var(--text-mut); z-index: 1; transition: all 0.3s; }
    .readiness-dot.active { border-color: var(--primary); background: var(--primary); box-shadow: 0 0 10px var(--primary); }

    /* Dataset Mini Cards */
    .mini-class-card {
        background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
        padding: 12px; margin-bottom: 10px; display: flex; flex-direction: column; gap: 8px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .mini-class-card:hover { transform: translateY(-2px); border-color: var(--border-hover); box-shadow: 0 4px 15px rgba(124, 58, 237, 0.1); }
    .mcc-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; font-weight: 700; color: var(--text-pri); }
    .mcc-badge { background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; color: var(--text-sec); }
    .mcc-bar-bg { width: 100%; height: 4px; background: var(--elevated); border-radius: 2px; overflow: hidden; }
    .mcc-bar-fill { height: 100%; background: var(--gradient); }

    /* Custom Pill Navigation (Radio Hack) */
    div[role="radiogroup"] {
        display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;
        background: var(--surface); padding: 8px; border-radius: 20px; border: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    div[role="radiogroup"] > label {
        background: var(--elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[role="radiogroup"] > label:hover { border-color: var(--border-hover) !important; transform: translateY(-2px); }
    div[role="radiogroup"] > label[data-checked="true"] {
        background: var(--gradient) !important;
        border-color: transparent !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4) !important;
    }
    div[role="radiogroup"] > label > div:first-child { display: none !important; /* Hide radio circle */ }
    div[role="radiogroup"] p { font-weight: 700 !important; font-size: 1.05rem !important; margin: 0 !important; }
    div[role="radiogroup"] > label[data-checked="true"] p { color: white !important; }

    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2) !important;
        padding: 1.5rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: var(--border-hover) !important;
        transform: translateY(-3px);
    }

    /* Primary Buttons & Animations */
    button[kind="primary"] {
        background: var(--gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
        position: relative; overflow: hidden;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:active { transform: scale(0.98) !important; }
    
    /* Shimmer Sweep */
    button[kind="primary"]::after {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.25), transparent);
        transform: skewX(-20deg); animation: shimmer 3s infinite;
    }
    @keyframes shimmer { 0% { left: -100%; } 100% { left: 200%; } }

    /* Train Button Specific Massive Style */
    .train-btn-container button[kind="primary"] {
        height: 60px !important; font-size: 1.2rem !important;
        animation: pulseRing 2s infinite cubic-bezier(0.66, 0, 0, 1) !important;
    }
    @keyframes pulseRing {
        0% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0.6); }
        70% { box-shadow: 0 0 0 20px rgba(124, 58, 237, 0); }
        100% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0); }
    }

    /* Input & Floating Label Hacks */
    div[data-baseweb="input"] {
        background-color: var(--elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }
    
    /* File Uploader "Marching Ants" */
    div[data-testid="stFileUploaderDropzone"] {
        background-color: rgba(255,255,255,0.02) !important;
        border: none !important;
        border-radius: 12px;
        padding: 32px 24px !important;
        background-image: 
            linear-gradient(90deg, var(--primary) 50%, transparent 50%),
            linear-gradient(90deg, var(--primary) 50%, transparent 50%),
            linear-gradient(0deg, var(--primary) 50%, transparent 50%),
            linear-gradient(0deg, var(--primary) 50%, transparent 50%);
        background-repeat: repeat-x, repeat-x, repeat-y, repeat-y;
        background-size: 16px 2px, 16px 2px, 2px 16px, 2px 16px;
        background-position: left top, right bottom, left bottom, right top;
        animation: border-dance 1s infinite linear;
        transition: background-color 0.3s;
    }
    div[data-testid="stFileUploaderDropzone"]:hover { background-color: rgba(124, 58, 237, 0.05) !important; }
    @keyframes border-dance { 100% { background-position: left 16px top, right 16px bottom, left bottom 16px, right top 16px; } }

    /* Hide Streamlit's default SVG/font icon and 'Drag and drop' text to fix overlapping */
    div[data-testid="stFileUploaderDropzone"] > section > svg,
    div[data-testid="stFileUploaderDropzone"] > section > span,
    div[data-testid="stFileUploaderDropzone"] > section > div:first-of-type {
        display: none !important;
    }

    /* Style the browse files button inside the dropzone */
    div[data-testid="stFileUploaderDropzone"] button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: var(--text-pri) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 4px 16px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        z-index: 10;
        margin-top: 10px !important;
    }
    div[data-testid="stFileUploaderDropzone"] button:hover {
        border-color: var(--primary) !important;
        background: rgba(124, 58, 237, 0.1) !important;
    }

    /* Masonry Grid Preview */
    [data-testid="stImage"] { margin-bottom: 12px; border-radius: 8px; overflow: hidden; }
    div[data-testid="column"]:nth-child(1) [data-testid="stImage"] img { height: 160px; object-fit: cover; }
    div[data-testid="column"]:nth-child(2) [data-testid="stImage"] img { height: 100px; object-fit: cover; }
    div[data-testid="column"]:nth-child(3) [data-testid="stImage"] img { height: 140px; object-fit: cover; }

    /* Metrics Styling */
    [data-testid="stMetricValue"] { font-size: 2.8rem !important; font-weight: 800 !important; color: var(--text-pri) !important; line-height: 1.1 !important; }
    [data-testid="stMetricLabel"] { font-size: 0.7rem !important; font-weight: 700 !important; color: var(--text-sec) !important; text-transform: uppercase; letter-spacing: 0.15em; }

    /* Architecture Timeline */
    .timeline { position: relative; padding-left: 30px; margin-top: 1rem; }
    .timeline::before { content: ''; position: absolute; left: 15px; top: 10px; bottom: 20px; width: 2px; border-left: 2px dashed var(--border); }
    .tl-item { position: relative; margin-bottom: 24px; }
    .tl-dot {
        position: absolute; left: -30px; top: 0px; width: 32px; height: 32px; border-radius: 50%;
        background: var(--gradient); display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 800; font-size: 0.9rem; box-shadow: 0 0 10px rgba(124, 58, 237, 0.4);
        z-index: 2;
    }
    .tl-content { padding-left: 16px; }
    .tl-title { font-weight: 700; color: var(--text-pri); font-size: 1.1rem; margin-bottom: 4px; }
    .tl-desc { font-size: 0.85rem; color: var(--text-sec); line-height: 1.4; }

    /* Success Card (Train) */
    .success-card {
        border: 1px solid var(--success); background: rgba(5, 150, 105, 0.05);
        border-radius: 16px; padding: 24px; text-align: center;
        box-shadow: 0 0 30px rgba(5, 150, 105, 0.1); animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .success-icon { font-size: 3rem; margin-bottom: 10px; animation: scaleBounce 1s infinite alternate; }
    .success-title { font-size: 1.5rem; font-weight: 800; color: var(--success); margin-bottom: 10px; }
    .chip-container { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
    .class-chip { background: var(--elevated); border: 1px solid var(--border); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; color: var(--text-pri); font-weight: 600; }
    @keyframes popIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes scaleBounce { from { transform: scale(1); } to { transform: scale(1.1); } }

    /* Scanner Loading State */
    .scanner-container { width: 100%; height: 300px; border-radius: 16px; border: 1px solid var(--border); background: var(--surface); position: relative; overflow: hidden; display: flex; justify-content: center; align-items: center;}
    .scanner-line { position: absolute; top: 0; left: 0; bottom: 0; width: 4px; background: var(--secondary); box-shadow: 0 0 20px 10px rgba(37, 99, 235, 0.4); animation: scanLine 2s infinite ease-in-out; }
    .scanner-text { color: var(--secondary); font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; animation: pulseText 1s infinite; }
    @keyframes scanLine { 0% { left: 0%; } 50% { left: 100%; } 100% { left: 0%; } }
    @keyframes pulseText { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }

    /* Prediction Result Hero */
    .result-hero-wrapper {
        padding: 2px; border-radius: 24px; background: var(--gradient);
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.25); margin-bottom: 2rem;
        animation: fadeInSlide 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .result-hero-inner {
        background: var(--surface); border-radius: 22px; padding: 2.5rem 2rem;
        display: flex; flex-direction: column; align-items: center; text-align: center;
    }
    .rh-label { font-size: 0.7rem; font-weight: 700; color: var(--text-sec); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 10px; }
    .rh-class { font-size: 4rem; font-weight: 800; letter-spacing: -0.02em; color: var(--text-pri); margin-bottom: 20px; line-height: 1; text-shadow: 0 4px 20px rgba(255,255,255,0.1); }
    
    /* Pure CSS Circular Progress */
    .circle-wrap { width: 120px; height: 120px; position: relative; }
    .circle-chart { width: 100%; height: 100%; transform: rotate(-90deg); }
    .circle-bg { fill: none; stroke: var(--elevated); stroke-width: 2.5; }
    .circle-fill { fill: none; stroke: url(#grad); stroke-width: 2.5; stroke-linecap: round; animation: fillRing 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    .circle-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.4rem; font-weight: 800; color: var(--text-pri); }
    @keyframes fillRing { 0% { stroke-dasharray: 0, 100; } }

    /* Custom Animated HTML Bar Chart */
    .custom-bar-chart { display: flex; flex-direction: column; gap: 12px; margin-top: 1rem; }
    .cb-row { display: flex; align-items: center; gap: 12px; }
    .cb-label { width: 100px; font-weight: 700; font-size: 0.9rem; color: var(--text-pri); text-align: right; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
    .cb-track { flex-grow: 1; height: 8px; background: var(--elevated); border-radius: 4px; overflow: hidden; }
    .cb-fill { height: 100%; width: 0%; border-radius: 4px; animation: growBar 1s cubic-bezier(0.4, 0, 0.2, 1) forwards 0.2s; }
    .cb-fill.winner { background: var(--gradient); box-shadow: 0 0 10px rgba(124, 58, 237, 0.4); }
    .cb-fill.loser { background: var(--text-mut); }
    .cb-val { width: 45px; font-size: 0.8rem; font-weight: 700; color: var(--text-sec); }
    @keyframes growBar { to { width: var(--target-width); } }
    @keyframes fadeInSlide { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

</style>
""", unsafe_allow_html=True)


# ── Session State Management ──────────────────────────────────────────────────
if "model_trained" not in st.session_state:
    st.session_state.model_trained = False
if "model_accuracy" not in st.session_state:
    st.session_state.model_accuracy = None
if "dataset_info" not in st.session_state:
    st.session_state.dataset_info = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


# ── API Helper Functions ──────────────────────────────────────────────────────
@st.cache_data(ttl=2)
def fetch_dataset_info():
    """Fetch current dataset stats from backend."""
    try:
        r = requests.get(f"{BACKEND_URL}/dataset-info", timeout=2)
        return r.json() if r.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

def check_backend():
    """Return True if backend is reachable."""
    try:
        r = requests.get(f"{BACKEND_URL}/", timeout=2)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ── UI Layout: Sidebar (Full Redesign) ────────────────────────────────────────
with st.sidebar:
    backend_alive = check_backend()
    status_color = "var(--success)" if backend_alive else "#ef4444"
    status_text = "SYSTEM ONLINE" if backend_alive else "SYSTEM OFFLINE"
    status_icon = "🟢" if backend_alive else "🔴"

    st.markdown(f"""
<div class="sidebar-top-bar" style="background: {status_color}"></div>
<div class="sidebar-status-box">
  <span>{status_icon}</span> <span style="color: {status_color}">{status_text}</span>
</div>
<div class="sidebar-logo-area">
  <div class="tm-monogram">TM</div>
  <div>
    <div class="tm-title">Teachable<br>Machine</div>
    <div class="tm-version">v1.0 · AI Research Lab</div>
  </div>
</div>
""", unsafe_allow_html=True)
    
    if not backend_alive:
        st.markdown("<div class='sidebar-content-padding'>", unsafe_allow_html=True)
        st.error("FastAPI backend is offline. Run `uvicorn main:app --reload`")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    info = fetch_dataset_info()
    st.session_state.dataset_info = info

    st.markdown("<div class='sidebar-content-padding'>", unsafe_allow_html=True)
    
    # 4-Dot Readiness Indicator
    num_classes = len(info.get("classes", {})) if info else 0
    c1 = num_classes >= 1
    c2 = num_classes >= 2
    c3 = st.session_state.model_trained
    c4 = st.session_state.model_trained

    w1 = "100%" if c2 else ("50%" if c1 else "0%")
    w2 = "100%" if c3 else "0%"
    w3 = "100%" if c4 else "0%"

    st.markdown(f"""
<div style="font-size:0.7rem; font-weight:700; color:var(--text-sec); letter-spacing:0.15em; text-transform:uppercase;">Deployment Readiness</div>
<div class="readiness-container">
  <div class="readiness-line"></div>
  <div class="readiness-dot {'active' if c1 else ''}"></div>
  <div style="flex-grow:1; position:relative; height:2px;">
    <div class="readiness-line-fill" style="width:{w1}"></div>
  </div>
  <div class="readiness-dot {'active' if c2 else ''}"></div>
  <div style="flex-grow:1; position:relative; height:2px;">
    <div class="readiness-line-fill" style="width:{w2}"></div>
  </div>
  <div class="readiness-dot {'active' if c3 else ''}"></div>
  <div style="flex-grow:1; position:relative; height:2px;">
    <div class="readiness-line-fill" style="width:{w3}"></div>
  </div>
  <div class="readiness-dot {'active' if c4 else ''}"></div>
</div>
<div style="font-size:0.75rem; color:var(--text-sec); display:flex; justify-content:space-between; margin-top:-20px; margin-bottom:30px;">
  <span>Add</span><span>Train</span><span>Ready</span>
</div>
""", unsafe_allow_html=True)

    # Dataset Mini Cards
    if info and info.get("total_images", 0) > 0:
        st.markdown("<div style='font-size:0.7rem; font-weight:700; color:var(--text-sec); letter-spacing:0.15em; text-transform:uppercase; margin-bottom:10px;'>Classes Embedded</div>", unsafe_allow_html=True)
        total = info["total_images"]
        for cls, count in info["classes"].items():
            pct = (count / total) * 100
            st.markdown(f"""
<div class="mini-class-card">
  <div class="mcc-header">
    <span>{cls}</span>
    <span class="mcc-badge">{count} imgs</span>
  </div>
  <div class="mcc-bar-bg"><div class="mcc-bar-fill" style="width: {pct}%;"></div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── Main UI: Full-Width Hero ──────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div>
        <div class="hero-pills">
            <span class="hero-pill">3 Steps</span>
            <span class="hero-pill">No GPU Required</span>
        </div>
        <h1 class="hero-title">Teachable<br>Machine</h1>
        <p class="hero-sub">Train a production-grade image classifier in seconds directly in the browser via Transfer Learning.</p>
    </div>
    <div style="position:relative; margin-right: 2rem;">
        <svg class="brain-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path class="brain-path" d="M50 90 C30 90 10 70 10 50 C10 30 25 15 40 10 C45 25 55 25 60 10 C75 15 90 30 90 50 C90 70 70 90 50 90 Z M50 15 V90 M25 35 Q50 50 75 35 M30 65 Q50 50 70 65" />
            <circle class="brain-node" cx="50" cy="50" r="4" />
            <circle class="brain-node" cx="25" cy="35" r="3" style="animation-delay: 0.2s;" />
            <circle class="brain-node" cx="75" cy="35" r="3" style="animation-delay: 0.4s;" />
            <circle class="brain-node" cx="30" cy="65" r="3" style="animation-delay: 0.6s;" />
            <circle class="brain-node" cx="70" cy="65" r="3" style="animation-delay: 0.8s;" />
        </svg>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Main UI: Tab Navigation ───────────────────────────────────────────────────
# 1. Initialize the tab state
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "1️⃣ Dataset Configuration"

# We avoid using key="active_tab" here. We use an index based on the session state.
# This detaches the internal widget state lock from our manual control logic.
tabs = ["1️⃣ Dataset Configuration", "2️⃣ Model Compilation", "3️⃣ Live Inference"]
current_index = tabs.index(st.session_state.active_tab) if st.session_state.active_tab in tabs else 0

selected_tab = st.radio(
    "Navigation", 
    tabs, 
    index=current_index,
    horizontal=True, 
    label_visibility="collapsed"
)

# Update our session state manually if the user clicks a different tab
if selected_tab != st.session_state.active_tab:
    st.session_state.active_tab = selected_tab
    st.rerun()


# ── TAB 1: UPLOAD ─────────────────────────────────────────────────────────────
if st.session_state.active_tab == "1️⃣ Dataset Configuration":
    col_form, col_preview = st.columns([1, 1], gap="large")

    with col_form:
        with st.container(border=True):
            st.markdown("<h3>Data Ingestion</h3>", unsafe_allow_html=True)
            class_name = st.text_input("Class Label", placeholder="e.g., Target_A")
            
            input_mode = st.radio("Source Stream", ["📂 File System", "📷 Web Camera"], horizontal=True)
            
            images_to_send = []
            if input_mode == "📂 File System":
                uploaded_files = st.file_uploader("Drop images to ingest", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
                if uploaded_files: images_to_send = uploaded_files
            else:
                webcam_image = st.camera_input("Capture Stream")
                if webcam_image: images_to_send = [webcam_image]

            if images_to_send:
                st.markdown("<p style='font-size:0.7rem; font-weight:700; text-transform:uppercase; margin-top:15px;'>Stream Preview</p>", unsafe_allow_html=True)
                grid_cols = st.columns(3)
                for i, img_file in enumerate(images_to_send[:6]): 
                    with grid_cols[i % 3]:
                        st.image(Image.open(img_file), use_container_width=True)
                if len(images_to_send) > 6: st.caption(f"+ {len(images_to_send)-6} more items")

            upload_disabled = not class_name.strip() or not images_to_send
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Initialize Upload Sequence", disabled=upload_disabled, use_container_width=True, type="primary"):
                with st.spinner(f"Transmitting to server..."):
                    files_payload = [("files", (f.name, f.getvalue(), f.type)) for f in images_to_send]
                    try:
                        resp = requests.post(
                            f"{BACKEND_URL}/upload-sample",
                            data={"class_name": class_name.strip()}, files=files_payload, timeout=30
                        )
                        if resp.status_code == 200:
                            st.toast(f"Synchronized {len(images_to_send)} vectors to {class_name}", icon="✅")
                            st.session_state.model_trained = False
                            st.rerun()
                        else: st.error("Ingestion failed.")
                    except Exception as e: st.error(f"Network error: {e}")

    with col_preview:
        with st.container(border=True):
            st.markdown("<h3>Volume Distribution</h3>", unsafe_allow_html=True)
            info = st.session_state.dataset_info
            
            if info and info.get("total_images", 0) > 0:
                df = pd.DataFrame(list(info["classes"].items()), columns=["Class", "Images"])
                
                # Testing that st.altair_chart still renders beautifully
                chart = alt.Chart(df).mark_bar(cornerRadiusEnd=6, height=35).encode(
                    x=alt.X('Images:Q', title="Data Volume", axis=alt.Axis(gridColor="rgba(255,255,255,0.05)", labelColor="#64748b", titleColor="#64748b", labelFont="Space Grotesk")),
                    y=alt.Y('Class:N', sort='-x', title="", axis=alt.Axis(labelColor="#f1f5f9", labelFontWeight="bold", labelFont="Space Grotesk")),
                    color=alt.Color('Images:Q', scale=alt.Scale(range=['#2563eb', '#7c3aed']), legend=None),
                    tooltip=['Class', 'Images']
                ).properties(height=350).configure_view(strokeWidth=0)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.markdown("""
<div style='height: 300px; display:flex; flex-direction:column; justify-content:center; align-items:center; opacity:0.5;'>
  <div style='font-size:3rem; margin-bottom:15px;'>📊</div>
  <p>No data ingested yet.</p>
</div>
""", unsafe_allow_html=True)


# ── TAB 2: TRAIN ──────────────────────────────────────────────────────────────
elif st.session_state.active_tab == "2️⃣ Model Compilation":
    info = st.session_state.dataset_info
    has_enough_data = info and len(info.get("classes", {})) >= 2 and info.get("total_images", 0) > 0

    if not has_enough_data:
        st.warning("⚠️ Insufficient vector volume. Ingest at least 2 target classes before compilation.")
    else:
        col_train, col_arch = st.columns([1, 1], gap="large")
        
        with col_train:
            with st.container(border=True):
                # Using st.metric to verify it renders correctly with new CSS
                st.metric("Total Parameters", info["total_images"])
                st.metric("Target Output Nodes", len(info["classes"]))
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.session_state.model_trained:
                    # Custom Success State
                    classes_chips = "".join([f"<span class='class-chip'>{c}</span>" for c in info['classes'].keys()])
                    
                    accuracy_val = st.session_state.get('model_accuracy', 'N/A')
                    accuracy_html = f"<h2 style='color: var(--primary); margin-bottom: 10px;'>{accuracy_val}% Overall Accuracy</h2>" if accuracy_val != "N/A" and accuracy_val is not None else ""

                    st.markdown(f"""
<div class="success-card">
  <div class="success-icon">✨</div>
  <div class="success-title">Model Compiled</div>
  {accuracy_html}
  <p style="color:var(--text-pri); margin-bottom:15px;">Weights saved and ready for inference.</p>
  <div class="chip-container">{classes_chips}</div>
</div>
""", unsafe_allow_html=True)
                else:
                    st.markdown('<div class="train-btn-container">', unsafe_allow_html=True)
                    if st.button("⚡ Execute Training Sequence", use_container_width=True, type="primary"):
                        with st.spinner("Extracting features and optimizing gradients..."):
                            try:
                                resp = requests.post(f"{BACKEND_URL}/train", timeout=120)
                                if resp.status_code == 200:
                                    resp_data = resp.json()
                                    st.session_state.model_trained = True
                                    # Capture the accuracy sent by backend
                                    st.session_state.model_accuracy = resp_data.get("accuracy", "N/A") 
                                    st.session_state.active_tab = "3️⃣ Live Inference" # <-- Auto Switch tab here!
                                    st.rerun()
                                else: st.error("Compilation failed.")
                            except Exception as e: st.error(f"Network error: {e}")
                    st.markdown('</div>', unsafe_allow_html=True)

        with col_arch:
            with st.container(border=True):
                st.markdown("<h3>Architecture Pipeline</h3>", unsafe_allow_html=True)
                # Vertical Timeline HTML
                st.markdown("""
<div class="timeline">
  <div class="tl-item">
    <div class="tl-dot">1</div>
    <div class="tl-content">
      <div class="tl-title">Feature Extraction</div>
      <div class="tl-desc">Pre-trained MobileNetV3 extracts a 960-dimensional vector for each image, skipping raw pixel training.</div>
    </div>
  </div>
  <div class="tl-item">
    <div class="tl-dot">2</div>
    <div class="tl-content">
      <div class="tl-title">Logistic Classification</div>
      <div class="tl-desc">An SKLearn Logistic Regression model calculates boundary weights across the extracted feature space.</div>
    </div>
  </div>
  <div class="tl-item">
    <div class="tl-dot">3</div>
    <div class="tl-content">
      <div class="tl-title">Serialization</div>
      <div class="tl-desc">Model topology and computed weights are pickled and persisted to the backend disk.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TAB 3: PREDICT ────────────────────────────────────────────────────────────
elif st.session_state.active_tab == "3️⃣ Live Inference":
    if not st.session_state.model_trained:
        st.info("⚠️ Weights not found. Execute compilation sequence in Step 2.")
    else:
        col_input, col_result = st.columns([1, 1], gap="large")
        
        # 1. First, define the scanner placeholder in the right column BEFORE using it in the left column
        with col_result:
            scanner_ph = st.empty()

        # 2. Then, define the input logic in the left column
        with col_input:
            with st.container(border=True):
                st.markdown("<h3>Input Tensor</h3>", unsafe_allow_html=True)
                pred_mode = st.radio("Source", ["📂 File Upload", "📷 Camera Capture"], horizontal=True, label_visibility="collapsed")
                
                test_image = None
                if pred_mode == "📂 File Upload": test_image = st.file_uploader("Upload test tensor", type=["jpg", "jpeg", "png"])
                else: test_image = st.camera_input("Capture tensor")

                if test_image:
                    st.image(Image.open(test_image), use_container_width=True, output_format="PNG")
                    test_image.seek(0)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔍 Run Inference", use_container_width=True, type="primary"):
                        
                        # Clear old prediction off screen while scanning
                        st.session_state.last_prediction = None 

                        # Show CSS Scanner inside placeholder
                        scanner_ph.markdown("""
<div class="scanner-container">
  <div class="scanner-text">Processing Tensor</div>
  <div class="scanner-line"></div>
</div>
""", unsafe_allow_html=True)
                        
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/predict",
                                files={"file": (test_image.name, test_image.getvalue(), test_image.type)}, timeout=30
                            )
                            if resp.status_code == 200:
                                st.session_state.last_prediction = resp.json()
                            else: st.error("Inference error.")
                        except Exception as e: st.error(f"Network error: {e}")
                        finally:
                            scanner_ph.empty() # Remove scanner

        # 3. Finally, render the actual results in the right column if they exist
        with col_result:
            pred = st.session_state.last_prediction
            if pred:
                # Math for SVG circular progress
                conf_val = pred['confidence']
                dash_array = f"{conf_val * 100}, 100"

                st.markdown(f"""
<svg width="0" height="0">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7c3aed" />
      <stop offset="100%" stop-color="#2563eb" />
    </linearGradient>
  </defs>
</svg>
<div class="result-hero-wrapper">
  <div class="result-hero-inner">
    <div class="rh-label">Inference Output</div>
    <div class="rh-class">{pred['predicted_class']}</div>
    <div class="circle-wrap">
      <svg class="circle-chart" viewBox="0 0 36 36">
        <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
        <path class="circle-fill" stroke-dasharray="{dash_array}" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
      </svg>
      <div class="circle-text">{conf_val*100:.0f}%</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.markdown("<h3>Softmax Activation Scores</h3>", unsafe_allow_html=True)
                    
                    # Custom Pure HTML/CSS Animated Bar Chart
                    sorted_scores = sorted(pred["all_scores"].items(), key=lambda x: x[1], reverse=True)
                    bars_html = "<div class='custom-bar-chart'>"
                    
                    for cls, score in sorted_scores:
                        pct = score * 100
                        is_winner = cls == pred["predicted_class"]
                        fill_class = "winner" if is_winner else "loser"
                        label_color = "var(--text-pri)" if is_winner else "var(--text-sec)"
                        
                        bars_html += f"""
<div class="cb-row">
  <div class="cb-label" style="color:{label_color}">{cls}</div>
  <div class="cb-track">
    <div class="cb-fill {fill_class}" style="--target-width: {pct}%;"></div>
  </div>
  <div class="cb-val">{pct:.1f}%</div>
</div>
"""
                    bars_html += "</div>"
                    st.markdown(bars_html, unsafe_allow_html=True)
            elif not st.session_state.last_prediction:
                st.markdown("""
<div style="height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; color:var(--text-mut); min-height: 400px; border: 1px dashed var(--border); border-radius: 24px;">
  <div style="font-size:3rem; margin-bottom:10px;">🎯</div>
  <div style="text-align:center;">Awaiting input tensor...</div>
</div>
""", unsafe_allow_html=True)