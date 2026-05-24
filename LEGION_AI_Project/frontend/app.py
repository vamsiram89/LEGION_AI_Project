"""
Modern Streamlit frontend for LEGION AI — Life Emergency Guardian Agent.

This version keeps the same backend API calls from the MVP, but redesigns
the frontend with a premium dark dashboard / landing-page style UI.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import requests
import streamlit as st


# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="LEGION AI — Life Emergency Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# Safe API URL loading
# Fixes Streamlit FileNotFoundError when secrets.toml is missing.
# ---------------------------------------------------------------------
try:
    API_URL = st.secrets.get("api_url", "http://localhost:8000")
except Exception:
    API_URL = "http://localhost:8000"


# ---------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #03040a;
            --panel: rgba(255, 255, 255, 0.065);
            --panel-strong: rgba(255, 255, 255, 0.095);
            --border: rgba(168, 128, 255, 0.24);
            --border-blue: rgba(74, 172, 255, 0.22);
            --text: #f6f7fb;
            --muted: #aeb3c8;
            --purple: #8b5cf6;
            --blue: #38bdf8;
            --pink: #ec4899;
            --green: #22c55e;
            --yellow: #facc15;
            --red: #fb7185;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(139, 92, 246, 0.32), transparent 34%),
                radial-gradient(circle at 72% 18%, rgba(56, 189, 248, 0.22), transparent 30%),
                radial-gradient(circle at 88% 82%, rgba(236, 72, 153, 0.17), transparent 28%),
                linear-gradient(135deg, #02030a 0%, #070818 42%, #03040a 100%);
            color: var(--text);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                radial-gradient(rgba(255,255,255,0.13) 1px, transparent 1px),
                linear-gradient(120deg, rgba(139,92,246,0.08), rgba(56,189,248,0.04), transparent);
            background-size: 36px 36px, 100% 100%;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.9), rgba(0,0,0,0.15));
            z-index: 0;
        }

        section.main > div {
            max-width: 1480px;
            padding-top: 1.2rem;
            position: relative;
            z-index: 2;
        }

        [data-testid="stSidebar"] {
            background: rgba(3, 4, 10, 0.84);
            border-right: 1px solid rgba(168, 128, 255, 0.18);
            backdrop-filter: blur(22px);
        }

        [data-testid="stSidebar"] * {
            color: #f6f7fb !important;
        }

        [data-testid="stSidebar"] .stRadio > label {
            color: #aeb3c8 !important;
            font-weight: 700;
        }

        h1, h2, h3 {
            letter-spacing: -0.04em;
        }

        h1 {
            font-size: 4.2rem !important;
            line-height: 0.96 !important;
            font-weight: 900 !important;
        }

        h2 {
            font-size: 2.2rem !important;
            font-weight: 850 !important;
        }

        h3 {
            font-weight: 780 !important;
        }

        .gradient-text {
            background: linear-gradient(90deg, #ffffff 0%, #c4b5fd 30%, #60a5fa 65%, #f0abfc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 22px;
            margin-bottom: 26px;
            border: 1px solid rgba(255,255,255,0.09);
            background: rgba(255,255,255,0.055);
            box-shadow: 0 22px 70px rgba(0,0,0,0.38);
            border-radius: 26px;
            backdrop-filter: blur(24px);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 900;
            letter-spacing: 0.08em;
            font-size: 1.05rem;
        }

        .logo-orb {
            width: 38px;
            height: 38px;
            border-radius: 13px;
            background:
                radial-gradient(circle at 30% 25%, #fff, transparent 22%),
                linear-gradient(135deg, #8b5cf6, #38bdf8 52%, #ec4899);
            box-shadow: 0 0 32px rgba(139,92,246,0.75);
        }

        .nav-links {
            display: flex;
            gap: 22px;
            color: #c8cce0;
            font-size: 0.92rem;
        }

        .nav-pill {
            padding: 10px 16px;
            border-radius: 999px;
            color: #d8dcf2;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.035);
        }

        .glass-card {
            border: 1px solid rgba(255,255,255,0.10);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.092), rgba(255,255,255,0.045));
            box-shadow:
                0 32px 90px rgba(0,0,0,0.40),
                inset 0 1px 0 rgba(255,255,255,0.13);
            border-radius: 28px;
            padding: 26px;
            backdrop-filter: blur(20px);
        }

        .glass-card:hover {
            border-color: rgba(139,92,246,0.44);
            transform: translateY(-2px);
            transition: 0.25s ease;
            box-shadow:
                0 42px 110px rgba(0,0,0,0.48),
                0 0 38px rgba(139,92,246,0.13);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1fr 1.1fr;
            gap: 30px;
            align-items: center;
            margin-bottom: 26px;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 14px;
            border: 1px solid rgba(139,92,246,0.34);
            border-radius: 999px;
            background: rgba(139,92,246,0.11);
            color: #d9d4ff;
            font-weight: 700;
            font-size: 0.86rem;
            margin-bottom: 18px;
        }

        .hero-sub {
            color: #bdc2d8;
            font-size: 1.12rem;
            line-height: 1.75;
            max-width: 720px;
            margin-top: 18px;
            margin-bottom: 24px;
        }

        .cta-row {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 22px;
        }

        .primary-btn, .secondary-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 22px;
            border-radius: 16px;
            font-weight: 800;
            text-decoration: none;
        }

        .primary-btn {
            color: white !important;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
            box-shadow: 0 18px 45px rgba(139,92,246,0.35);
        }

        .secondary-btn {
            color: #f5f7ff !important;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.13);
        }

        .mini-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-top: 18px;
        }

        .metric-card {
            padding: 16px;
            border-radius: 20px;
            background: rgba(255,255,255,0.055);
            border: 1px solid rgba(255,255,255,0.09);
        }

        .metric-label {
            color: #9ea5bf;
            font-size: 0.78rem;
            font-weight: 650;
            margin-bottom: 6px;
        }

        .metric-value {
            color: #ffffff;
            font-size: 1.55rem;
            font-weight: 900;
        }

        .metric-delta {
            color: #4ade80;
            font-size: 0.75rem;
            margin-top: 4px;
        }

        .dashboard-shell {
            border-radius: 30px;
            padding: 18px;
            border: 1px solid rgba(96,165,250,0.25);
            background:
                radial-gradient(circle at top right, rgba(139,92,246,0.20), transparent 36%),
                rgba(7, 10, 24, 0.82);
            box-shadow: 0 0 70px rgba(59,130,246,0.15), 0 45px 110px rgba(0,0,0,0.55);
        }

        .dashboard-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .search-bar {
            width: 42%;
            padding: 12px 16px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            color: #8f96ad;
            font-size: 0.84rem;
        }

        .chart {
            height: 210px;
            position: relative;
            border-radius: 22px;
            overflow: hidden;
            background:
                linear-gradient(180deg, rgba(139,92,246,0.12), rgba(56,189,248,0.025)),
                rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.09);
        }

        .chart svg {
            width: 100%;
            height: 100%;
        }

        .donut {
            width: 164px;
            height: 164px;
            border-radius: 50%;
            background: conic-gradient(#8b5cf6 0 42%, #38bdf8 42% 64%, #ec4899 64% 82%, #22c55e 82% 100%);
            display: grid;
            place-items: center;
            margin: 16px auto 6px;
            box-shadow: 0 0 42px rgba(139,92,246,0.24);
        }

        .donut-inner {
            width: 94px;
            height: 94px;
            border-radius: 50%;
            background: #090b16;
            display: grid;
            place-items: center;
            font-weight: 900;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-top: 18px;
        }

        .feature-icon {
            width: 46px;
            height: 46px;
            border-radius: 16px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, rgba(139,92,246,0.28), rgba(56,189,248,0.14));
            border: 1px solid rgba(255,255,255,0.10);
            font-size: 1.25rem;
            margin-bottom: 12px;
        }

        .section-title {
            text-align: center;
            margin: 48px 0 10px;
        }

        .section-sub {
            text-align: center;
            color: #aeb3c8;
            margin-bottom: 26px;
        }

        .form-card {
            max-width: 820px;
            margin: 0 auto;
        }

        .risk-pill {
            display: inline-flex;
            padding: 8px 14px;
            border-radius: 999px;
            font-weight: 900;
            background: rgba(250, 204, 21, 0.14);
            color: #fde68a;
            border: 1px solid rgba(250, 204, 21, 0.25);
        }

        .history-item {
            padding: 18px;
            border-radius: 20px;
            margin-bottom: 14px;
            background: rgba(255,255,255,0.055);
            border: 1px solid rgba(255,255,255,0.09);
        }

        .testimonial-grid, .pricing-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-top: 20px;
        }

        .price {
            font-size: 2.6rem;
            font-weight: 900;
            letter-spacing: -0.06em;
        }

        .footer {
            margin-top: 46px;
            padding: 28px;
            border-radius: 26px;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.08);
            color: #aeb3c8;
        }

        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background: rgba(255,255,255,0.06) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(168,128,255,0.24) !important;
            border-radius: 14px !important;
        }

        .stTextInput label, .stTextArea label, .stNumberInput label {
            color: #d8dcf2 !important;
            font-weight: 700 !important;
        }

        .stButton button {
            border-radius: 16px !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899) !important;
            color: white !important;
            font-weight: 850 !important;
            padding: 0.75rem 1.2rem !important;
            box-shadow: 0 18px 42px rgba(139,92,246,0.27) !important;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 22px 54px rgba(139,92,246,0.39) !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 18px;
        }

        @media (max-width: 1050px) {
            .hero-grid,
            .feature-grid,
            .testimonial-grid,
            .pricing-grid {
                grid-template-columns: 1fr;
            }

            .mini-stats {
                grid-template-columns: repeat(2, 1fr);
            }

            h1 {
                font-size: 3.1rem !important;
            }

            .nav-links {
                display: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def post_json(endpoint: str, payload: dict[str, Any]) -> requests.Response:
    return requests.post(f"{API_URL}{endpoint}", json=payload, timeout=20)


def get_json(endpoint: str) -> requests.Response:
    return requests.get(f"{API_URL}{endpoint}", timeout=20)


def show_nav() -> None:
    st.markdown(
        """
        <div class="nav">
            <div class="brand">
                <div class="logo-orb"></div>
                <div>LEGION AI</div>
            </div>
            <div class="nav-links">
                <span>Guardian</span>
                <span>Health</span>
                <span>Mood</span>
                <span>Finance</span>
                <span>Risk Engine</span>
            </div>
            <div class="nav-pill">Life Emergency Guardian MVP</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def landing_page() -> None:
    show_nav()

    left, right = st.columns([0.92, 1.08], gap="large")

    with left:
        st.markdown(
            """
            <div class="badge">⚡ AI safety copilot is live</div>
            <h1>Protect life before <span class="gradient-text">risk becomes emergency.</span></h1>
            <p class="hero-sub">
                LEGION AI monitors health, mood, spending and emergency signals to estimate life-risk
                patterns early. This MVP demonstrates the full workflow from user data to risk scoring.
            </p>
            <div class="cta-row">
                <a class="primary-btn" href="#register">Start Guardian Setup →</a>
                <a class="secondary-btn" href="#features">Explore Features</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="mini-stats">
                <div class="metric-card">
                    <div class="metric-label">Risk Domains</div>
                    <div class="metric-value">3</div>
                    <div class="metric-delta">Health · Mood · Finance</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Mode</div>
                    <div class="metric-value">MVP</div>
                    <div class="metric-delta">Prototype ready</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">API</div>
                    <div class="metric-value">FastAPI</div>
                    <div class="metric-delta">Local backend</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">UI</div>
                    <div class="metric-value">Streamlit</div>
                    <div class="metric-delta">Premium dashboard</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="dashboard-shell">
                <div class="dashboard-top">
                    <div>
                        <div style="font-size:1.35rem;font-weight:900;">Guardian Command Center</div>
                        <div style="color:#aeb3c8;font-size:0.9rem;">Live risk intelligence dashboard</div>
                    </div>
                    <div class="search-bar">Search health, mood, alerts...</div>
                </div>

                <div class="mini-stats">
                    <div class="metric-card">
                        <div class="metric-label">Current Risk</div>
                        <div class="metric-value">33.7</div>
                        <div class="metric-delta">Watch level</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Health</div>
                        <div class="metric-value">Normal</div>
                        <div class="metric-delta">Stable vitals</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Mood</div>
                        <div class="metric-value">Watch</div>
                        <div class="metric-delta">Negative sentiment</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Finance</div>
                        <div class="metric-value">Safe</div>
                        <div class="metric-delta">No anomaly</div>
                    </div>
                </div>

                <div style="display:grid;grid-template-columns:1.45fr 0.85fr;gap:16px;margin-top:16px;">
                    <div class="chart">
                        <svg viewBox="0 0 600 220" preserveAspectRatio="none">
                            <defs>
                                <linearGradient id="lineGrad" x1="0" x2="1">
                                    <stop offset="0%" stop-color="#38bdf8"/>
                                    <stop offset="50%" stop-color="#8b5cf6"/>
                                    <stop offset="100%" stop-color="#ec4899"/>
                                </linearGradient>
                                <linearGradient id="areaGrad" x1="0" x2="0" y1="0" y2="1">
                                    <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.42"/>
                                    <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
                                </linearGradient>
                            </defs>
                            <path d="M0,170 C80,140 90,70 160,95 C230,120 235,48 310,70 C380,92 392,155 470,112 C530,80 545,40 600,56 L600,220 L0,220 Z" fill="url(#areaGrad)"/>
                            <path d="M0,170 C80,140 90,70 160,95 C230,120 235,48 310,70 C380,92 392,155 470,112 C530,80 545,40 600,56" fill="none" stroke="url(#lineGrad)" stroke-width="5"/>
                            <circle cx="470" cy="112" r="8" fill="#fff"/>
                        </svg>
                    </div>
                    <div class="glass-card" style="padding:18px;">
                        <div style="font-weight:900;">Signal Mix</div>
                        <div class="donut"><div class="donut-inner">3 Signals</div></div>
                        <div style="color:#aeb3c8;font-size:0.85rem;">Health · Mood · Finance</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">
            <h2>Powerful Features for <span class="gradient-text">Human Safety</span></h2>
        </div>
        <div class="section-sub">A premium MVP interface for emergency-prevention intelligence.</div>
        <div class="feature-grid">
            <div class="glass-card">
                <div class="feature-icon">❤️</div>
                <h3>Health Risk Signals</h3>
                <p style="color:#aeb3c8;">Track heart rate, sleep, steps and blood pressure to detect abnormal patterns.</p>
            </div>
            <div class="glass-card">
                <div class="feature-icon">🧠</div>
                <h3>Mood Intelligence</h3>
                <p style="color:#aeb3c8;">Analyze journal entries and emotional signals for stress or negative sentiment.</p>
            </div>
            <div class="glass-card">
                <div class="feature-icon">💳</div>
                <h3>Finance Watch</h3>
                <p style="color:#aeb3c8;">Log spending behavior and detect unusual money patterns in the MVP flow.</p>
            </div>
            <div class="glass-card">
                <div class="feature-icon">🚨</div>
                <h3>Emergency Contacts</h3>
                <p style="color:#aeb3c8;">Store trusted contacts for future alert automation and escalation workflows.</p>
            </div>
            <div class="glass-card">
                <div class="feature-icon">📊</div>
                <h3>Risk Dashboard</h3>
                <p style="color:#aeb3c8;">View overall risk, domain-level scores and explanations from the backend.</p>
            </div>
            <div class="glass-card">
                <div class="feature-icon">🛡️</div>
                <h3>Guardian History</h3>
                <p style="color:#aeb3c8;">Review previous risk calculations and understand changing risk patterns.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">
            <h2>Trusted Guardian Experience</h2>
        </div>
        <div class="testimonial-grid">
            <div class="glass-card">
                <p style="font-size:1.05rem;">“A futuristic MVP for showing how AI can detect human risk before crisis.”</p>
                <b>AI Product Reviewer</b><br><span style="color:#aeb3c8;">Prototype feedback</span>
            </div>
            <div class="glass-card">
                <p style="font-size:1.05rem;">“The dashboard makes health, mood and finance signals easy to understand.”</p>
                <b>Safety Analyst</b><br><span style="color:#aeb3c8;">UX validation</span>
            </div>
            <div class="glass-card">
                <p style="font-size:1.05rem;">“A strong foundation for building a real life-protection AI agent.”</p>
                <b>AI Engineer</b><br><span style="color:#aeb3c8;">MVP review</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">
            <h2>Roadmap Pricing Style Section</h2>
        </div>
        <div class="pricing-grid">
            <div class="glass-card">
                <h3>MVP</h3>
                <div class="price">Free</div>
                <p style="color:#aeb3c8;">Local testing and demo mode.</p>
                <p>✓ Streamlit UI</p><p>✓ FastAPI backend</p><p>✓ Basic risk scoring</p>
            </div>
            <div class="glass-card" style="border-color:rgba(139,92,246,0.55);box-shadow:0 0 55px rgba(139,92,246,0.18);">
                <h3>Pro Guardian</h3>
                <div class="price">Future</div>
                <p style="color:#aeb3c8;">Advanced AI and alert workflows.</p>
                <p>✓ OpenAI explanations</p><p>✓ Real notifications</p><p>✓ Personal baseline learning</p>
            </div>
            <div class="glass-card">
                <h3>Enterprise</h3>
                <div class="price">Future</div>
                <p style="color:#aeb3c8;">Hospitals, insurance and elderly care.</p>
                <p>✓ Team dashboards</p><p>✓ Compliance controls</p><p>✓ Cloud deployment</p>
            </div>
        </div>
        <div class="footer">
            <b>LEGION AI</b><br>
            Life Emergency Guardian Agent MVP · Built for early risk awareness, safety workflows and future autonomous protection.
        </div>
        """,
        unsafe_allow_html=True,
    )


def register_user() -> None:
    show_nav()
    st.markdown('<div id="register"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.05, 0.95], gap="large")

    with col1:
        st.markdown(
            """
            <div class="glass-card">
                <div class="badge">🛡️ Guardian onboarding</div>
                <h1>Start your <span class="gradient-text">Life Guardian</span> profile.</h1>
                <p class="hero-sub">
                    Register first to unlock the dashboard menu: emergency contacts, health data,
                    mood logs, spending logs, risk score and risk history.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        with st.container():
            st.markdown('<div class="glass-card form-card">', unsafe_allow_html=True)
            st.subheader("Create Guardian Profile")
            name = st.text_input("Name", placeholder="Vamsi")
            email = st.text_input("Email", placeholder="vamsi@example.com")
            phone = st.text_input("Phone (optional)", placeholder="9999999999")

            if st.button("Register & Open Dashboard", use_container_width=True):
                if not name or not email:
                    st.error("Please enter name and email.")
                else:
                    try:
                        resp = post_json("/users", {"name": name, "email": email, "phone": phone})
                        if resp.status_code == 200:
                            st.session_state.user = resp.json()
                            st.success("User registered successfully!")
                            st.rerun()
                        else:
                            try:
                                detail = resp.json().get("detail", "Registration failed")
                            except Exception:
                                detail = "Registration failed"
                            st.error(detail)
                    except requests.exceptions.RequestException as exc:
                        st.error(f"Backend connection failed. Make sure FastAPI is running on {API_URL}. Error: {exc}")
            st.markdown("</div>", unsafe_allow_html=True)

    landing_page()


def add_contact(user_id: int) -> None:
    st.markdown('<div class="glass-card form-card">', unsafe_allow_html=True)
    st.subheader("🚨 Add Emergency Contact")
    name = st.text_input("Contact Name", placeholder="Father / Mother / Friend")
    relation = st.text_input("Relation", placeholder="Father")
    phone = st.text_input("Phone", placeholder="9876543210")
    email = st.text_input("Email", placeholder="contact@example.com")

    if st.button("Add Contact", use_container_width=True):
        payload = {"name": name, "relation": relation, "phone": phone, "email": email}
        try:
            resp = post_json(f"/users/{user_id}/contacts", payload)
            if resp.status_code == 200:
                st.success("Contact added successfully.")
            else:
                st.error(resp.json().get("detail", "Failed to add contact"))
        except requests.exceptions.RequestException as exc:
            st.error(f"Backend connection failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)


def submit_health(user_id: int) -> None:
    st.markdown('<div class="glass-card form-card">', unsafe_allow_html=True)
    st.subheader("❤️ Submit Health Data")

    c1, c2 = st.columns(2)
    with c1:
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=30.0, max_value=200.0, value=70.0)
        sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=7.0)
        steps = st.number_input("Steps", min_value=0, value=4000)
    with c2:
        bp_systolic = st.number_input("BP Systolic", min_value=50.0, max_value=250.0, value=120.0)
        bp_diastolic = st.number_input("BP Diastolic", min_value=30.0, max_value=180.0, value=80.0)
        st.info("Try high-risk test: HR 135, Sleep 2, Steps 500, BP 170/110.")

    if st.button("Submit Health", use_container_width=True):
        payload = {
            "heart_rate": heart_rate,
            "sleep_hours": sleep_hours,
            "steps": steps,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
        }
        try:
            resp = post_json(f"/users/{user_id}/health", payload)
            if resp.status_code == 200:
                st.success("Health data recorded.")
            else:
                st.error(resp.json().get("detail", "Failed to record health data"))
        except requests.exceptions.RequestException as exc:
            st.error(f"Backend connection failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)


def submit_mood(user_id: int) -> None:
    st.markdown('<div class="glass-card form-card">', unsafe_allow_html=True)
    st.subheader("🧠 Submit Mood Journal")
    text = st.text_area(
        "How are you feeling today?",
        placeholder="Example: I feel calm, focused and motivated today.",
        height=160,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.caption("Normal test: I feel calm, happy, energetic and hopeful.")
    with c2:
        st.caption("Watch test: I feel lonely, hopeless, stressed and exhausted.")

    if st.button("Submit Mood", use_container_width=True):
        try:
            resp = post_json(f"/users/{user_id}/mood", {"text": text})
            if resp.status_code == 200:
                st.success("Mood entry recorded.")
            else:
                st.error(resp.json().get("detail", "Failed to record mood"))
        except requests.exceptions.RequestException as exc:
            st.error(f"Backend connection failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)


def submit_spending(user_id: int) -> None:
    st.markdown('<div class="glass-card form-card">', unsafe_allow_html=True)
    st.subheader("💳 Submit Spending")
    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input("Amount", min_value=0.0, value=10.0)
    with c2:
        category = st.text_input("Category", placeholder="Food / Medical / Shopping / Bills")

    st.caption("This means: how much money was spent and what type of spending it was.")

    if st.button("Submit Spending", use_container_width=True):
        try:
            resp = post_json(f"/users/{user_id}/spending", {"amount": amount, "category": category})
            if resp.status_code == 200:
                st.success("Spending log recorded.")
            else:
                st.error(resp.json().get("detail", "Failed to record spending"))
        except requests.exceptions.RequestException as exc:
            st.error(f"Backend connection failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)


def score_color(score: float) -> str:
    if score >= 70:
        return "#fb7185"
    if score >= 35:
        return "#facc15"
    return "#22c55e"


def score_card(label: str, value: float) -> None:
    color = score_color(value)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color};">{value:.1f}</div>
            <div class="metric-delta">Risk score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def view_risk(user_id: int) -> None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Calculate Current Risk")
    st.write("Click once after adding health, mood or spending data. Repeated clicks without new data can create duplicate history rows.")

    if st.button("Get Risk Score", use_container_width=True):
        try:
            resp = get_json(f"/users/{user_id}/risk")
            if resp.status_code == 200:
                st.session_state.latest_risk = resp.json()
            else:
                st.error(resp.json().get("detail", "Failed to compute risk"))
        except requests.exceptions.RequestException as exc:
            st.error(f"Backend connection failed: {exc}")

    data = st.session_state.get("latest_risk")
    if data:
        st.markdown(
            f"""
            <div style="margin-top:20px;">
                <span class="risk-pill">Overall: {data['overall_score']:.1f} · {data['level']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            score_card("Overall", float(data["overall_score"]))
        with c2:
            score_card("Health", float(data["health_score"]))
        with c3:
            score_card("Mood", float(data["mood_score"]))
        with c4:
            score_card("Finance", float(data["finance_score"]))

        st.info(data["explanation"])

    st.markdown("</div>", unsafe_allow_html=True)


def view_history(user_id: int) -> None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🕒 Risk History")

    try:
        resp = get_json(f"/users/{user_id}/history")
        if resp.status_code == 200:
            history = resp.json()
            if not history:
                st.info("No risk history yet. Go to View Risk and click Get Risk Score.")
            for entry in history:
                st.markdown(
                    f"""
                    <div class="history-item">
                        <b>{entry['timestamp']}</b>
                        <span class="risk-pill" style="margin-left:10px;">{entry['overall_score']:.1f} · {entry['level']}</span>
                        <p style="color:#aeb3c8;margin-top:10px;">{entry['explanation']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.error(resp.json().get("detail", "Failed to load history"))
    except requests.exceptions.RequestException as exc:
        st.error(f"Backend connection failed: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)


def sidebar_menu(user: dict[str, Any]) -> str:
    st.sidebar.markdown(
        f"""
        <div style="padding:18px;border-radius:22px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);margin-bottom:16px;">
            <div style="font-weight:900;font-size:1.1rem;">🛡️ Guardian Active</div>
            <div style="color:#aeb3c8;margin-top:8px;">{user['name']}</div>
            <div style="color:#aeb3c8;font-size:0.84rem;">{user['email']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return st.sidebar.radio(
        "Command Center",
        [
            "Dashboard",
            "Add Contact",
            "Submit Health",
            "Submit Mood",
            "Submit Spending",
            "View Risk",
            "Risk History",
            "Logout",
        ],
    )


def dashboard_home(user: dict[str, Any]) -> None:
    show_nav()
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="badge">✅ Logged in guardian profile</div>
            <h1>Welcome back, <span class="gradient-text">{user['name']}</span></h1>
            <p class="hero-sub">
                Use the command center to submit health, mood and spending signals. Then open View Risk
                to calculate the current safety score from your FastAPI backend.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-grid">
            <div class="glass-card"><div class="feature-icon">1</div><h3>Submit Signals</h3><p style="color:#aeb3c8;">Add health, mood and spending records.</p></div>
            <div class="glass-card"><div class="feature-icon">2</div><h3>Calculate Risk</h3><p style="color:#aeb3c8;">Generate overall and domain scores.</p></div>
            <div class="glass-card"><div class="feature-icon">3</div><h3>Review History</h3><p style="color:#aeb3c8;">Track previous risk calculations.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_css()

    if "user" not in st.session_state:
        register_user()
        return

    user = st.session_state.user
    menu = sidebar_menu(user)

    if menu == "Dashboard":
        dashboard_home(user)
    elif menu == "Add Contact":
        show_nav()
        add_contact(user["id"])
    elif menu == "Submit Health":
        show_nav()
        submit_health(user["id"])
    elif menu == "Submit Mood":
        show_nav()
        submit_mood(user["id"])
    elif menu == "Submit Spending":
        show_nav()
        submit_spending(user["id"])
    elif menu == "View Risk":
        show_nav()
        view_risk(user["id"])
    elif menu == "Risk History":
        show_nav()
        view_history(user["id"])
    elif menu == "Logout":
        st.session_state.clear()
        st.rerun()


if __name__ == "__main__":
    main()
