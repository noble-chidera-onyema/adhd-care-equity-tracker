"""
Visual identity for ADHD Care Equity Tracker UK (ACE).
Locks palette, typography, CSS injection, page configuration.
Imported once at the top of streamlit_app.py.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

from pathlib import Path
import streamlit as st


# Project palette. Locked. Matches notebook 03 chart colours so PNGs and
# in-app charts share a single visual language.
PALETTE = {
    "bg":               "#FAFAF8",
    "surface":          "#FFFFFF",
    "ink":              "#1A1A1A",
    "ink_dim":          "#555555",
    "border":           "#E5E5E0",
    "navy":             "#1F4E79",
    "navy_dim":         "#3B6FA0",

    # Waiting-band scale — green, amber, orange, red — identical to chart 1/2
    "band_short":       "#2E7D32",
    "band_mid":         "#FBC02D",
    "band_long":        "#EF6C00",
    "band_extreme":     "#C62828",

    # Skeleton shimmer
    "skeleton_bg":      "#EDEDE8",
    "skeleton_shimmer": "#F5F5F0",
}

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def apply_theme():
    """Call once at the top of streamlit_app.py, before any other Streamlit calls."""

    st.set_page_config(
        page_title="ACE | ADHD Care Equity Tracker UK",
        page_icon=str(ASSETS_DIR / "favicon.svg"),
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(_css(), unsafe_allow_html=True)


def _css() -> str:
    p = PALETTE
    return f"""
    <style>

    /* === Hide Streamlit default chrome === */
    #MainMenu {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent;
        height: 0;
    }}

    /* === Typography === */
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                     "Helvetica Neue", Arial, sans-serif;
        color: {p['ink']};
        background: {p['bg']};
        -webkit-font-smoothing: antialiased;
    }}

    h1, h2, h3, h4 {{
        font-weight: 600;
        letter-spacing: -0.01em;
        color: {p['ink']};
        margin-top: 0;
    }}

    h1 {{ font-size: 1.875rem; line-height: 1.2; }}
    h2 {{ font-size: 1.375rem; line-height: 1.3; }}
    h3 {{ font-size: 1.125rem; line-height: 1.4; }}

    /* === Background === */
    .stApp {{
        background: {p['bg']};
    }}

    [data-testid="stSidebar"] {{
        background: {p['surface']};
        border-right: 1px solid {p['border']};
    }}

    /* === Sidebar nav buttons === */
    [data-testid="stSidebar"] .stButton button {{
        background: transparent;
        color: {p['ink']};
        border: none;
        border-left: 3px solid transparent;
        border-radius: 0;
        text-align: left;
        padding: 0.6rem 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.15s ease;
    }}

    [data-testid="stSidebar"] .stButton button:hover {{
        background: {p['bg']};
        border-left-color: {p['navy_dim']};
    }}

    [data-testid="stSidebar"] .stButton button:focus {{
        box-shadow: none;
        outline: none;
    }}

    /* === Brand header === */
    .ace-header {{
        padding: 1rem 0 1.75rem 0;
        border-bottom: 1px solid {p['border']};
        margin-bottom: 2rem;
    }}

    .ace-brand {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {p['navy']};
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}

    .ace-tagline {{
        font-size: 0.95rem;
        color: {p['ink_dim']};
        margin-top: 0.4rem;
    }}

    /* === KPI card === */
    .kpi-card {{
        background: {p['surface']};
        border: 1px solid {p['border']};
        border-radius: 6px;
        padding: 1.25rem 1.5rem;
        height: 100%;
        transition: border-color 0.2s ease;
    }}

    .kpi-card:hover {{
        border-color: {p['navy']};
    }}

    .kpi-label {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {p['ink_dim']};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.6rem;
    }}

    .kpi-value {{
        font-size: 1.875rem;
        font-weight: 700;
        line-height: 1.1;
        color: {p['navy']};
        font-variant-numeric: tabular-nums;
    }}

    .kpi-note {{
        font-size: 0.8rem;
        color: {p['ink_dim']};
        margin-top: 0.5rem;
        line-height: 1.4;
    }}

    /* === Skeleton loader === */
    .skeleton {{
        background: {p['skeleton_bg']};
        background-image: linear-gradient(
            90deg,
            {p['skeleton_bg']} 0%,
            {p['skeleton_shimmer']} 50%,
            {p['skeleton_bg']} 100%
        );
        background-size: 200% 100%;
        animation: shimmer 1.4s ease-in-out infinite;
        border-radius: 4px;
    }}

    .skeleton-kpi {{
        height: 7.5rem;
        border-radius: 6px;
    }}

    .skeleton-chart {{
        height: 24rem;
        border-radius: 6px;
        margin-top: 1rem;
    }}

    @keyframes shimmer {{
        0%   {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    /* === Section header === */
    .ace-section-title {{
        font-size: 1.25rem;
        font-weight: 600;
        color: {p['ink']};
        margin: 2.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid {p['border']};
    }}

    .ace-section-intro {{
        font-size: 0.95rem;
        color: {p['ink_dim']};
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }}

    /* === Footer === */
    .ace-footer {{
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid {p['border']};
        color: {p['ink_dim']};
        font-size: 0.8rem;
        line-height: 1.6;
    }}

    .ace-footer a {{
        color: {p['navy']};
        text-decoration: none;
    }}

    .ace-footer a:hover {{
        text-decoration: underline;
    }}

    /* === Block container === */
    .main .block-container {{
        max-width: 1320px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }}

    /* === Selection colour === */
    ::selection {{
        background: {p['navy']};
        color: {p['bg']};
    }}

    </style>
    """


def kpi_card(label: str, value: str, note: str = "") -> str:
    """Return HTML string for a KPI card. Caller wraps with st.markdown(unsafe_allow_html=True)."""
    note_html = f'<div class="kpi-note">{note}</div>' if note else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {note_html}
    </div>
    """


def skeleton(height_class: str = "skeleton-kpi") -> str:
    """Return HTML for a skeleton loader. height_class is one of 'skeleton-kpi', 'skeleton-chart'."""
    return f'<div class="skeleton {height_class}"></div>'
