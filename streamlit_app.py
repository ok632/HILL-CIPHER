#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import numpy as np
from sympy import Matrix
import json
import os
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="HILL CIPHER PLATINUM - PRO",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ULTRA-MODERN PURE DARK CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Quicksand:wght@300;400;500;700&display=swap');

    :root {
        --neon-cyan: #00f2ff;
        --neon-purple: #bc13fe;
        --deep-dark: #020205; /* Deeper Dark base */
        --panel-dark: rgba(0, 0, 0, 0.7);
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    .stApp {
        background: radial-gradient(circle at center, #0a0a1a 0%, #000000 100%);
        color: #f8f8f8;
        font-family: 'Quicksand', sans-serif;
    }

    /* Main Header Styling */
    .title-container {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(180deg, rgba(0, 242, 255, 0.05), transparent);
        border-radius: 0 0 50% 50% / 0 0 10% 10%;
        margin-bottom: 3.5rem;
    }

    .main-title {
        font-family: 'Syncopate', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00f2ff, #bc13fe, #00f2ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        letter-spacing: 12px;
        margin: 0;
        text-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Deep Dark Glass Panel */
    .fancy-card {
        background: var(--panel-dark);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 35px;
        backdrop-filter: blur(40px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), 0 0 2px rgba(255, 255, 255, 0.05);
        margin-bottom: 24px;
        transition: all 0.4s ease;
    }

    .fancy-card:hover {
        border-color: rgba(0, 242, 255, 0.4);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), 0 0 15px rgba(0, 242, 255, 0.1);
    }

    .section-header {
        font-family: 'Syncopate', sans-serif;
        font-size: 1rem;
        color: var(--neon-cyan);
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 15px;
        opacity: 0.9;
    }

    .section-header::after {
        content: "";
        height: 1px;
        flex-grow: 1;
        background: linear-gradient(90deg, var(--neon-cyan), transparent);
        opacity: 0.2;
    }

    /* Input & Area Styling (Deep Contrast) */
    .stTextArea textarea, .stTextInput input {
        background: #000000 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #fff !important;
        font-size: 1.1rem !important;
        padding: 18px !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--neon-cyan) !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.1) !important;
    }

    /* Buttons (Cyber Glow) */
    .stButton>button {
        border-radius: 10px !important;
        height: 55px !important;
        font-family: 'Syncopate', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid transparent !important;
    }

    .btn-primary > button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.2) !important;
    }

    .btn-secondary > button {
        background: linear-gradient(45deg, #6a11cb, #2575fc) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(106, 17, 203, 0.2) !important;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        filter: brightness(1.2);
    }

    /* Sidebar - High End Dark */
    .stSidebar {
        background: #05050a !important;
        border-right: 1px solid var(--glass-border);
    }

    /* Custom Table/DataFrame (Dark Contrast) */
    [data-testid="stDataFrame"] {
        border: 1px solid #222 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        padding-bottom: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 12px 25px !important;
        background-color: transparent !important;
        color: #666 !important;
        font-family: 'Syncopate', sans-serif;
    }

    .stTabs [aria-selected="true"] {
        color: var(--neon-cyan) !important;
        border-bottom: 2px solid var(--neon-cyan) !important;
    }
</style>
""", unsafe_allow_html=True)

# CORE UTILITIES
def gcd(a, b):
    while b: a, b = b, a % b
    return a

def prepare_text(text, n):
    text = ''.join(c for c in text.upper() if c.isalpha()).replace('J', 'I')
    pad = (n - (len(text) % n)) % n
    text += 'X' * pad
    return [ord(c) - ord('A') for c in text]

def mod_inverse(matrix, mod=26):
    try:
        s_mat = Matrix(matrix)
        det = int(s_mat.det()) % mod
        if gcd(det, mod) != 1: return None
        det_inv = pow(det, -1, mod)
        inv = (det_inv * s_mat.adjugate()) % mod
        return np.array(inv).astype(int)
    except: return None

def hill_process(text, key, decrypt=False):
    n = key.shape[0]
    if decrypt:
        key = mod_inverse(key)
        if key is None: raise ValueError("Matrix is not invertible mod 26")
    
    vec = prepare_text(text, n)
    blocks = [vec[i:i+n] for i in range(0, len(vec), n)]
    res = []
    for b in blocks:
        proc = (key @ b) % 26
        res.extend(proc)
    return ''.join(chr(int(x) + ord('A')) for x in res)

import time

def hill_process_visual(text, key, decrypt=False):
    n = key.shape[0]
    if decrypt:
        key_inv = mod_inverse(key)
        if key_inv is None: raise ValueError("Matrix is not invertible mod 26")
        proc_key = key_inv
    else:
        proc_key = key
    
    vec = prepare_text(text, n)
    blocks = [vec[i:i+n] for i in range(0, len(vec), n)]
    
    steps = []
    final_res = []
    
    for i, b in enumerate(blocks):
        # Math Trace
        res_vec = (proc_key @ b) % 26
        block_text = ''.join(chr(int(x) + ord('A')) for x in b)
        res_text = ''.join(chr(int(x) + ord('A')) for x in res_vec)
        
        # Create LaTeX
        matrix_latex = r"\begin{bmatrix} " + r" \\ ".join([" & ".join(map(str, row)) for row in proc_key]) + r" \end{bmatrix}"
        vector_latex = r"\begin{bmatrix} " + r" \\ ".join(map(str, b)) + r" \end{bmatrix}"
        res_latex = r"\begin{bmatrix} " + r" \\ ".join(map(str, res_vec)) + r" \end{bmatrix}"
        
        formula = f"{matrix_latex} \times {vector_latex} = {res_latex} \pmod{{26}}"
        
        steps.append({
            "id": i + 1,
            "in": block_text,
            "out": res_text,
            "formula": formula
        })
        final_res.extend(res_vec)
        
    return ''.join(chr(int(x) + ord('A')) for x in final_res), steps

# SESSION INITIALIZATION
if 'output' not in st.session_state: st.session_state.output = ""
if 'history' not in st.session_state: st.session_state.history = []
if 'last_steps' not in st.session_state: st.session_state.last_steps = []

# SIDEBAR CONFIGURATION (The Workspace Settings)
with st.sidebar:
    st.markdown("<h2 style='font-family:Syncopate; color:#00f2ff; font-size:1.2rem;'>⚙️ WORKSPACE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    dim = st.selectbox("MATRIX DIMENSION", [2, 3, 4], key="dim_sel")
    
    st.markdown("<br><p style='font-family:Syncopate; font-size:0.7rem; color:#888;'>KEY MATRIX CONFIG</p>", unsafe_allow_html=True)
    
    if f'mat_{dim}' not in st.session_state:
        st.session_state[f'mat_{dim}'] = pd.DataFrame(np.zeros((dim, dim), dtype=int), columns=[f"C{i+1}" for i in range(dim)])
    
    ed_mat = st.data_editor(
        st.session_state[f'mat_{dim}'],
        num_rows="fixed",
        hide_index=True,
        key=f"editor_v3_{dim}",
        use_container_width=True
    )
    st.session_state[f'mat_{dim}'] = ed_mat
    matrix_raw = ed_mat.to_numpy()
    
    col_rnd, col_reset = st.columns(2)
    with col_rnd:
        if st.button("🎲 RANDOM", use_container_width=True):
            while True:
                rnd = np.random.randint(1, 26, (dim, dim))
                if mod_inverse(rnd) is not None: break
            st.session_state[f'mat_{dim}'] = pd.DataFrame(rnd, columns=[f"C{i+1}" for i in range(dim)])
            st.rerun()
    with col_reset:
        if st.button("🔄 RESET", use_container_width=True):
            st.session_state[f'mat_{dim}'] = pd.DataFrame(np.zeros((dim, dim), dtype=int), columns=[f"C{i+1}" for i in range(dim)])
            st.rerun()

    # Matrix Status
    det = int(Matrix(matrix_raw).det()) % 26
    is_inv = mod_inverse(matrix_raw) is not None
    
    st.markdown("---")
    if is_inv:
        st.markdown(f"<p class='status-success'>● MATRIX OPERATIONAL<br><small>Determinant: {det}</small></p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='status-error'>× MATRIX INVALID<br><small>Det not coprime with 26</small></p>", unsafe_allow_html=True)

    st.markdown("<br><br><p style='font-family:Syncopate; font-size:0.6rem; color:#444; text-align:center;'>PLATINUM V4.0 FINAL</p>", unsafe_allow_html=True)

# MAIN UI
st.markdown('<div class="title-container"><h1 class="main-title">HILL CIPHER PRO</h1></div>', unsafe_allow_html=True)

tab_enc, tab_viz, tab_file, tab_hist = st.tabs(["🔒 WORKSPACE", "🔬 VISUALIZER", "📂 ARCHIVES", "📜 LOGS"])

with tab_enc:
    col_in, col_out = st.columns(2, gap="large")
    
    with col_in:
        st.markdown('<div class="fancy-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📥 INPUT STREAM</div>', unsafe_allow_html=True)
        user_input = st.text_area("PAYLOAD:", height=200, placeholder="Enter text to encrypt or decrypt...", key="p_in")
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("ENCRYPT", use_container_width=True):
                if not user_input: st.warning("NO PAYLOAD")
                elif not is_inv: st.error("INVALID KEY")
                else:
                    res, steps = hill_process_visual(user_input, matrix_raw)
                    st.session_state.output = res
                    st.session_state.last_steps = steps
                    st.session_state.history.append({"time": datetime.now().strftime("%H:%M:%S"), "op": "ENC", "txt": user_input[:20]})
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("DECRYPT", use_container_width=True):
                if not user_input: st.warning("NO PAYLOAD")
                elif not is_inv: st.error("INVALID KEY")
                else:
                    try:
                        res, steps = hill_process_visual(user_input, matrix_raw, decrypt=True)
                        st.session_state.output = res
                        st.session_state.last_steps = steps
                        st.session_state.history.append({"time": datetime.now().strftime("%H:%M:%S"), "op": "DEC", "txt": user_input[:20]})
                        st.rerun()
                    except Exception as e: st.error(str(e))
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_out:
        st.markdown('<div class="fancy-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📤 OUTPUT STREAM</div>', unsafe_allow_html=True)
        st.text_area("RESULT:", value=st.session_state.output, height=200, disabled=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("📋 COPY", use_container_width=True):
                st.toast("RESULT CAPTURED")
        with cc2:
            if st.button("💾 EXPORT", use_container_width=True):
                fname = f"hc_out_{datetime.now().strftime('%H%M%S')}.txt"
                with open(fname,"w") as f: f.write(st.session_state.output)
                st.success(f"EXPORTED: {fname}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_viz:
    st.markdown('<div class="fancy-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🔬 MATHEMATICAL TRACE (LIVE)</div>', unsafe_allow_html=True)
    
    if st.session_state.last_steps:
        st.markdown("### Process Animation")
        anim_placeholder = st.empty()
        
        if st.button("▶️ RUN ANIMATION"):
            current_build = ""
            for step in st.session_state.last_steps:
                with anim_placeholder.container():
                    st.markdown(f"""
                    <div style="background:rgba(0,242,255,0.05); padding:20px; border-radius:15px; border-left: 5px solid #00f2ff;">
                        <h4 style="color:#00f2ff; margin:0;">Processing Block #{step['id']}</h4>
                        <p style="font-size:1.2rem; letter-spacing:3px;">
                            <span style="color:#888;">{step['in']}</span> 
                            <span style="color:#00f2ff;"> ➔ </span> 
                            <span style="font-weight:700; color:#bc13fe;">{step['out']}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.latex(step['formula'])
                time.sleep(1.2)
            st.success("Analysis Complete!")
        
        st.markdown("---")
        st.markdown("### Step-by-Step Breakdown")
        for step in st.session_state.last_steps:
            with st.expander(f"Block #{step['id']}: {step['in']} ➔ {step['out']}"):
                st.latex(step['formula'])
    else:
        st.info("Perform an encryption/decryption in the Workspace to see the visualization.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_file:
    st.markdown('<div class="fancy-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📂 FILE PROCESSOR</div>', unsafe_allow_html=True)
    f = st.file_uploader("UPLOAD SOURCE (.TXT)", type=['txt'])
    if f and is_inv:
        raw_f = f.read().decode()
        st.info(f"Loaded: {f.name} ({len(raw_f)} characters)")
        fc1, fc2 = st.columns(2)
        with fc1:
            if st.button("ENCRYPT FILE", use_container_width=True):
                out_f = hill_process(raw_f, matrix_raw)
                st.download_button("DOWNLOAD ENC", out_f, f"enc_{f.name}")
        with fc2:
            if st.button("DECRYPT FILE", use_container_width=True):
                try:
                    out_f = hill_process(raw_f, matrix_raw, decrypt=True)
                    st.download_button("DOWNLOAD DEC", out_f, f"dec_{f.name}")
                except Exception as e: st.error(str(e))
    st.markdown('</div>', unsafe_allow_html=True)

with tab_hist:
    st.markdown('<div class="fancy-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📜 OPERATION LOGS</div>', unsafe_allow_html=True)
    if st.session_state.history:
        st.table(st.session_state.history)
        if st.button("CLEAR LOGS", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("NO LOGS RECORDED")
    st.markdown('</div>', unsafe_allow_html=True)
