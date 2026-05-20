import io
import requests
import streamlit as st
from PIL import Image

# ── Configuration ─────────────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Teachable Machine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* Root variables */
    :root {
        --primary: #00ff88;
        --primary-dim: #00cc6a;
        --bg-dark: #0d0f14;
        --bg-card: #161b24;
        --bg-card2: #1c2333;
        --text-main: #e8eaf0;
        --text-muted: #6b7a99;
        --border: #2a3347;
        --danger: #ff4d6d;
        --warning: #ffb347;
    }

    /* Global overrides */
    .stApp {
        background-color: var(--bg-dark);
        font-family: 'DM Sans', sans-serif;
        color: var(--text-main);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-card) !important;
        border-right: 1px solid var(--border);
    }

    /* Headings */
    h1, h2, h3 { font-family: 'Space Mono', monospace; }

    h1 {
        color: var(--primary);
        font-size: 1.6rem;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }

    /* Cards */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.8rem;
    }

    /* Stat badges */
    .stat-row {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }

    .stat-badge {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.5rem 0.9rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.78rem;
    }

    .stat-badge .val {
        color: var(--primary);
        font-size: 1.1rem;
        font-weight: 700;
        display: block;
    }

    .stat-badge .lbl {
        color: var(--text-muted);
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Class pills */
    .class-pill {
        display: inline-block;
        background: #1a2640;
        border: 1px solid #2a4080;
        color: #7aacff;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-family: 'Space Mono', monospace;
        margin: 3px;
    }

    /* Prediction result */
    .prediction-box {
        background: linear-gradient(135deg, #0d1f14, #0a1a2e);
        border: 1px solid var(--primary);
        border-radius: 12px;
        padding: 1.4rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    .prediction-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-muted);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .prediction-class {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0.3rem 0;
    }

    .prediction-conf {
        font-size: 1rem;
        color: var(--text-muted);
    }

    /* Confidence bar wrapper */
    .conf-bar-row {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.6rem;
    }

    .conf-bar-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-main);
        width: 110px;
        flex-shrink: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .conf-bar-track {
        flex: 1;
        background: var(--bg-card2);
        border-radius: 4px;
        height: 10px;
        overflow: hidden;
    }

    .conf-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.6s ease;
    }

    .conf-bar-pct {
        font-family: 'Space Mono', monospace;
        font-size: 0.68rem;
        color: var(--text-muted);
        width: 38px;
        text-align: right;
        flex-shrink: 0;
    }

    /* Status pills */
    .status-ok {
        color: var(--primary);
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
    }

    .status-warn {
        color: var(--warning);
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
    }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0;
    }

    /* Override streamlit button styles */
    .stButton > button {
        font-family: 'Space Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 1px;
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--bg-card2);
        color: var(--text-main);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: var(--primary);
        color: var(--primary);
        background: #0d1f14;
    }

    /* File uploader area */
    [data-testid="stFileUploader"] {
        border: 1px dashed var(--border);
        border-radius: 10px;
        background: var(--bg-card2);
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        color: var(--text-main);
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide streamlit menu/footer */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Camera input */
    [data-testid="stCameraInput"] > div {
        border: 1px dashed var(--border);
        border-radius: 10px;
        background: var(--bg-card2);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    /* Info / warning / success boxes */
    .stAlert {
        border-radius: 10px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Session State Defaults ────────────────────────────────────────────────────
if "model_trained" not in st.session_state:
    st.session_state.model_trained = False

if "dataset_info" not in st.session_state:
    st.session_state.dataset_info = None

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


# ── Helper Functions ──────────────────────────────────────────────────────────
def fetch_dataset_info():
    """Fetch current dataset stats from backend."""
    try:
        r = requests.get(f"{BACKEND_URL}/dataset-info", timeout=5)
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.ConnectionError:
        return None
    return None


def check_backend():
    """Return True if backend is reachable."""
    try:
        r = requests.get(f"{BACKEND_URL}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def color_for_index(i, total):
    """Return a colour from green → blue gradient based on rank."""
    colors = ["#00ff88", "#00e57a", "#00cc6a", "#00b35b", "#009948",
              "#4da6ff", "#3d8fef", "#2d78df", "#1d61cf", "#0d4abf"]
    return colors[min(i, len(colors) - 1)]


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Teachable\nMachine")
    st.markdown("---")

    # Backend status
    backend_alive = check_backend()
    if backend_alive:
        st.markdown('<p class="status-ok">● Backend connected</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-warn">● Backend offline — start FastAPI first</p>', unsafe_allow_html=True)
        st.code("uvicorn main:app --reload", language="bash")
        st.stop()

    st.markdown("---")

    # Dataset summary
    info = fetch_dataset_info()
    st.session_state.dataset_info = info

    if info and info["total_images"] > 0:
        classes = info["classes"]
        num_classes = len(classes)
        total_imgs = info["total_images"]

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-badge">
                <span class="val">{num_classes}</span>
                <span class="lbl">Classes</span>
            </div>
            <div class="stat-badge">
                <span class="val">{total_imgs}</span>
                <span class="lbl">Images</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="card-title">Loaded Classes</p>', unsafe_allow_html=True)
        pills_html = "".join(
            f'<span class="class-pill">{cls} <b style="color:#00ff88">({cnt})</b></span>'
            for cls, cnt in classes.items()
        )
        st.markdown(pills_html, unsafe_allow_html=True)

        if st.session_state.model_trained:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="status-ok">✓ Model trained & ready</p>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<p style="color:#6b7a99; font-size:0.82rem;">No dataset yet.<br>Upload images to get started.</p>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown(
        '<p style="color:#3d4d66; font-size:0.7rem; font-family: Space Mono, monospace;">'
        'MobileNetV3 + LogisticRegression<br>Transfer Learning Pipeline</p>',
        unsafe_allow_html=True
    )


# ── Main Layout ───────────────────────────────────────────────────────────────
st.markdown("# 🧠 Teachable Machine")
st.markdown(
    '<p style="color:#6b7a99; margin-top:-0.5rem; margin-bottom:1.5rem;">'
    'Train a custom image classifier in seconds — no GPU required.</p>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["📁 Step 1 · Upload", "⚡ Step 2 · Train", "🔍 Step 3 · Predict"])


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — UPLOAD
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Upload Training Images")
    st.markdown(
        "Give each category a name, then upload images for it. "
        "Repeat for every class you want to recognise. **Aim for 10+ images per class.**"
    )

    col_form, col_preview = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">Class Setup</p>', unsafe_allow_html=True)

        class_name = st.text_input(
            "Class name",
            placeholder="e.g. cat, dog, thumbs_up …",
            label_visibility="collapsed"
        )

        input_mode = st.radio(
            "Image source",
            ["📂 Upload files", "📷 Webcam"],
            horizontal=True,
            label_visibility="collapsed"
        )

        uploaded_files = []
        webcam_image = None

        if input_mode == "📂 Upload files":
            uploaded_files = st.file_uploader(
                "Drop images here",
                type=["jpg", "jpeg", "png", "webp", "bmp"],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
        else:
            webcam_image = st.camera_input("Take a photo", label_visibility="collapsed")

        # Collect all images to send
        images_to_send = []
        if uploaded_files:
            images_to_send = uploaded_files
        elif webcam_image:
            images_to_send = [webcam_image]

        # Upload button
        upload_disabled = not class_name.strip() or not images_to_send
        if st.button(
            f"⬆ Upload {len(images_to_send)} image(s) as '{class_name or '…'}'" if images_to_send
            else "⬆ Upload Images",
            disabled=upload_disabled,
            use_container_width=True
        ):
            with st.spinner("Uploading …"):
                files_payload = [
                    ("files", (f.name, f.getvalue(), f.type))
                    for f in images_to_send
                ]
                try:
                    resp = requests.post(
                        f"{BACKEND_URL}/upload-sample",
                        data={"class_name": class_name.strip()},
                        files=files_payload,
                        timeout=30,
                    )
                    if resp.status_code == 200:
                        result = resp.json()
                        st.success(f"✓ {result['message']}")
                        # Invalidate training state — new data means old model is stale
                        st.session_state.model_trained = False
                        st.session_state.last_prediction = None
                        st.rerun()
                    else:
                        st.error(f"Upload failed: {resp.json().get('detail', resp.text)}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">Dataset Overview</p>', unsafe_allow_html=True)

        info = st.session_state.dataset_info
        if info and info["total_images"] > 0:
            for cls, count in info["classes"].items():
                pct = count / info["total_images"]
                bar_color = "#00ff88" if pct >= 0.2 else "#ffb347"
                st.markdown(f"""
                <div class="conf-bar-row">
                    <span class="conf-bar-label">{cls}</span>
                    <div class="conf-bar-track">
                        <div class="conf-bar-fill" style="width:{pct*100:.0f}%; background:{bar_color};"></div>
                    </div>
                    <span class="conf-bar-pct">{count} img</span>
                </div>
                """, unsafe_allow_html=True)

            min_cls = min(info["classes"], key=info["classes"].get)
            min_cnt = info["classes"][min_cls]
            if len(info["classes"]) < 2:
                st.warning("⚠ Need at least **2 classes** before training.")
            elif min_cnt < 5:
                st.warning(f"⚠ Class **{min_cls}** has only {min_cnt} image(s). More data = better accuracy.")
            else:
                st.success("✓ Dataset looks good! Head to Step 2 to train.")
        else:
            st.markdown(
                '<p style="color:#3d4d66; font-size:0.85rem;">No images uploaded yet.</p>',
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — TRAIN
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Train Your Model")

    info = st.session_state.dataset_info
    has_enough = info and len(info.get("classes", {})) >= 2 and info.get("total_images", 0) > 0

    if not has_enough:
        st.info("Upload images for at least 2 classes in Step 1 before training.")
    else:
        col_info, col_btn = st.columns([2, 1], gap="large")

        with col_info:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">Training Plan</p>', unsafe_allow_html=True)

            classes = info["classes"]
            for cls, cnt in classes.items():
                st.markdown(f"""
                <div class="conf-bar-row">
                    <span class="conf-bar-label">{cls}</span>
                    <div class="conf-bar-track">
                        <div class="conf-bar-fill" style="width:100%; background:#1d4ed8;"></div>
                    </div>
                    <span class="conf-bar-pct">{cnt} img</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <hr class="divider">
            <p style="color:#6b7a99; font-size:0.8rem;">
                🔧 Backbone: <b style="color:#e8eaf0">MobileNetV3-Small</b> (feature extractor)<br>
                📐 Classifier: <b style="color:#e8eaf0">Logistic Regression</b><br>
                🖼 Input size: <b style="color:#e8eaf0">224 × 224 px</b>
            </p>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_btn:
            st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown(
                f'<p style="font-size:2rem; margin:0;">🚀</p>'
                f'<p style="font-family: Space Mono, monospace; font-size:0.72rem; color:#6b7a99; margin:0.3rem 0 1rem;">'
                f'{info["total_images"]} images · {len(classes)} classes</p>',
                unsafe_allow_html=True
            )

            if st.button("⚡ Train Model", use_container_width=True, type="primary"):
                with st.spinner("Extracting features & training …"):
                    try:
                        resp = requests.post(f"{BACKEND_URL}/train", timeout=120)
                        if resp.status_code == 200:
                            result = resp.json()
                            st.session_state.model_trained = True
                            st.session_state.last_prediction = None
                            st.success(
                                f"✓ Training complete! "
                                f"{result['total_images']} images · {len(result['classes'])} classes"
                            )
                        else:
                            st.error(f"Training failed: {resp.json().get('detail', resp.text)}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

            if st.session_state.model_trained:
                st.markdown(
                    '<p class="status-ok" style="margin-top:0.8rem; text-align:center;">✓ Model ready</p>',
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — PREDICT
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Live Prediction")

    if not st.session_state.model_trained:
        st.info("Train your model in Step 2 before running predictions.")
    else:
        col_input, col_result = st.columns([1, 1], gap="large")

        with col_input:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">Test Image</p>', unsafe_allow_html=True)

            pred_mode = st.radio(
                "Source",
                ["📂 Upload file", "📷 Webcam"],
                horizontal=True,
                label_visibility="collapsed"
            )

            test_image = None
            if pred_mode == "📂 Upload file":
                test_image = st.file_uploader(
                    "Upload test image",
                    type=["jpg", "jpeg", "png", "webp", "bmp"],
                    label_visibility="collapsed",
                    key="pred_uploader"
                )
            else:
                test_image = st.camera_input("Capture", label_visibility="collapsed", key="pred_cam")

            if test_image:
                img_preview = Image.open(test_image)
                st.image(img_preview, use_container_width=True, caption="Test image")

                test_image.seek(0)  # Reset file pointer after PIL read

                if st.button("🔍 Classify", use_container_width=True, type="primary"):
                    with st.spinner("Running inference …"):
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/predict",
                                files={"file": (test_image.name, test_image.getvalue(), test_image.type)},
                                timeout=30,
                            )
                            if resp.status_code == 200:
                                st.session_state.last_prediction = resp.json()
                            else:
                                st.error(f"Prediction error: {resp.json().get('detail', resp.text)}")
                        except Exception as e:
                            st.error(f"Connection error: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

        with col_result:
            pred = st.session_state.last_prediction

            if pred:
                conf_pct = int(pred["confidence"] * 100)

                # Prediction result box
                st.markdown(f"""
                <div class="prediction-box">
                    <p class="prediction-label">Predicted Class</p>
                    <p class="prediction-class">{pred['predicted_class']}</p>
                    <p class="prediction-conf">{conf_pct}% confidence</p>
                </div>
                """, unsafe_allow_html=True)

                # Confidence bars for all classes
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<p class="card-title">All Class Scores</p>', unsafe_allow_html=True)

                # Sort by score descending
                sorted_scores = sorted(
                    pred["all_scores"].items(), key=lambda x: x[1], reverse=True
                )
                total = len(sorted_scores)

                for i, (cls, score) in enumerate(sorted_scores):
                    is_winner = (cls == pred["predicted_class"])
                    bar_color = color_for_index(i, total)
                    score_pct = score * 100
                    label_style = "color:#00ff88; font-weight:700;" if is_winner else ""

                    st.markdown(f"""
                    <div class="conf-bar-row">
                        <span class="conf-bar-label" style="{label_style}">
                            {"▶ " if is_winner else ""}{cls}
                        </span>
                        <div class="conf-bar-track">
                            <div class="conf-bar-fill"
                                 style="width:{score_pct:.1f}%; background:{bar_color};">
                            </div>
                        </div>
                        <span class="conf-bar-pct">{score_pct:.1f}%</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # Quick bar chart via Streamlit native (bonus visual)
                st.markdown('<p class="card-title" style="margin-top:0.5rem;">Score Chart</p>', unsafe_allow_html=True)
                chart_data = {cls: score for cls, score in sorted_scores}
                st.bar_chart(chart_data)

            else:
                st.markdown(
                    '<div class="card" style="text-align:center; padding:3rem 1rem;">'
                    '<p style="font-size:2.5rem; margin:0;">🔍</p>'
                    '<p style="color:#6b7a99; font-size:0.85rem; margin-top:0.5rem;">'
                    'Upload or capture an image<br>and click Classify.</p>'
                    '</div>',
                    unsafe_allow_html=True
                )