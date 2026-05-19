"""
ADHD Care Equity Tracker UK — Streamlit app entry.

v0.9: Methodology view wired. All five views now live. Dashboard
feature-complete. Next: deployment to Streamlit Community Cloud.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
See LICENSE and NOTICE.md in the project root.
"""

import streamlit as st

from components.theme import apply_theme, kpi_card
from data.loader import (
    data_freshness,
    kpi_open_referrals,
    kpi_total_waiting_list,
    kpi_share_104_weeks,
    kpi_female_diagnosis_growth,
    kpi_asian_underrepresentation,
    fmt_count,
    fmt_count_short,
    fmt_pct,
    fmt_multiplier,
    fmt_ratio,
)
from views.overview import render as render_overview
from views.waiting_times import render as render_waiting_times
from views.demographics import render as render_demographics
from views.trends import render as render_trends
from views.methodology import render as render_methodology

# --- Page setup ---
apply_theme()


# --- View routing ---
if "view" not in st.session_state:
    st.session_state["view"] = "overview"


# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 1rem 0.5rem 1.5rem 0.5rem;">
            <div style="font-size: 1.125rem; font-weight: 700; color: #1F4E79;
                        letter-spacing: -0.01em;">ACE</div>
            <div style="font-size: 0.75rem; color: #555555; margin-top: 0.2rem;
                        line-height: 1.4;">ADHD Care Equity<br>Tracker UK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Overview", key="nav_overview", use_container_width=True):
        st.session_state["view"] = "overview"
    if st.button("Waiting Times", key="nav_wait", use_container_width=True):
        st.session_state["view"] = "waiting_times"
    if st.button("Demographics", key="nav_demo", use_container_width=True):
        st.session_state["view"] = "demographics"
    if st.button("Trends", key="nav_trends", use_container_width=True):
        st.session_state["view"] = "trends"
    if st.button("Methodology", key="nav_method", use_container_width=True):
        st.session_state["view"] = "methodology"

    st.markdown(
        """
        <div style="margin-top: 3rem; padding: 1.5rem 0.5rem 0 0.5rem;
                    border-top: 1px solid #E5E5E0;
                    font-size: 0.75rem; color: #555555; line-height: 1.6;">
            Noble Chidera Onyema<br>
            MSc Applied AI portfolio<br>
            <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker"
               style="color: #1F4E79; text-decoration: none;">Source on GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- Header ---
st.markdown(
    """
    <div class="ace-header">
        <div class="ace-brand">ADHD Care Equity Tracker UK</div>
        <div class="ace-tagline">
            A consolidation of public UK ADHD waiting-time data. Built on NHS England,
            Children's Commissioner, OpenSAFELY, and Commons Library sources through May 2026.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --- Data freshness banner ---
fresh = data_freshness()
SOURCE_PRETTY = {
    "mi_adhd":         "NHS England MI-ADHD",
    "opensafely":      "OpenSAFELY",
    "cco":             "Children's Commissioner",
    "commons_library": "Commons Library CBP-10551",
}

freshness_parts = []
for src_key, src_name in SOURCE_PRETTY.items():
    latest = fresh["sources_latest"].get(src_key)
    if latest is not None:
        freshness_parts.append(f"<strong>{src_name}</strong> through {latest.strftime('%b %Y')}")

freshness_html = " · ".join(freshness_parts)
parquet_str = fresh["parquet_built"].strftime("%d %b %Y")

st.markdown(
    f"""
    <div class="ace-freshness">
        {freshness_html}<br>
        Harmonised fact table built {parquet_str}. Data refreshes when source publishers release new files.
    </div>
    """,
    unsafe_allow_html=True,
)


# --- KPI strip ---
k1 = kpi_open_referrals()
k2 = kpi_total_waiting_list()
k3 = kpi_share_104_weeks()
k4 = kpi_female_diagnosis_growth()
k5 = kpi_asian_underrepresentation()

KPI_CARDS = [
    {
        "label": "Open ADHD referrals, England",
        "value": fmt_count(k1["value"]),
        "note":  f"MHSDS, {k1['date'].strftime('%b %Y')}. Validated to the unit against NHS England.",
    },
    {
        "label": "Total UK waiting list, estimated",
        "value": fmt_count_short(k2["value"]),
        "note":  "MHSDS plus CHS SitRep, per Commons Library CBP-10551.",
    },
    {
        "label": "Share waiting 104+ weeks",
        "value": fmt_pct(k3["value"]),
        "note":  "Up from 29% twelve months earlier.",
    },
    {
        "label": "Female ADHD diagnosis growth, 9 years",
        "value": fmt_multiplier(k4["multiplier"]),
        "note":  f"OpenSAFELY, {k4['first_date'].strftime('%b %Y')} to {k4['last_date'].strftime('%b %Y')}.",
    },
    {
        "label": "Asian children, under-representation ratio",
        "value": fmt_ratio(k5["ratio"]),
        "note":  f"{k5['referral_share_pct']:.1f}% of ADHD referrals vs ~{k5['census_share_pct']:.0f}% of child population, CCO Oct 2024.",
    },
]

cols = st.columns(5, gap="medium")
for col, kpi in zip(cols, KPI_CARDS):
    with col:
        st.markdown(kpi_card(**kpi), unsafe_allow_html=True)


# --- View content ---
view = st.session_state["view"]
if view == "overview":
    render_overview()
elif view == "waiting_times":
    render_waiting_times()
elif view == "demographics":
    render_demographics()
elif view == "trends":
    render_trends()
elif view == "methodology":
    render_methodology()


# --- Footer ---
st.markdown(
    """
    <div class="ace-footer">
        ADHD Care Equity Tracker UK · Educational research artefact, not a clinical tool ·
        © 2026 Noble Chidera Onyema. All Rights Reserved.
        Data: NHS England, Children's Commissioner for England, OpenSAFELY, House of Commons Library.
        Source code under All Rights Reserved licence;
        <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker">repository</a>.
    </div>
    """,
    unsafe_allow_html=True,
)
