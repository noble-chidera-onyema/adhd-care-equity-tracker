"""
app/views/overview.py — Overview view for the dashboard.

Renders the project's headline chart (open ADHD referrals by waiting band)
live from the harmonised fact table. Future scope: chart 2 (share by band)
and chart 7 (prevalence vs referrals) added here as additional sections.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

import plotly.express as px
import streamlit as st

from data.loader import (
    chart_data_open_referrals_by_band,
    WAITING_BAND_ORDER,
    WAITING_BAND_COLOURS,
)


def render():
    """Render the Overview view content. KPI strip is rendered at app level."""

    st.markdown(
        '<div class="ace-section-title">Open ADHD referrals by waiting band, England</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ace-section-intro">'
        'Monthly stock of open ADHD referrals in NHS Mental Health Services, split by how long each '
        'has been waiting. December 2024 to the latest published month. The 104+ weeks band has '
        'grown fastest in both absolute terms and as a share of the total.'
        '</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_open_referrals_by_band()

    fig = px.area(
        data,
        x="date_start",
        y="value",
        color="band",
        category_orders={"band": WAITING_BAND_ORDER},
        color_discrete_map=WAITING_BAND_COLOURS,
        labels={"date_start": "Month", "value": "Open referrals", "band": ""},
    )
    fig.update_layout(
        height=480,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            color="#1A1A1A",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="left",
            x=0,
            title_text="",
        ),
        hovermode="x unified",
        xaxis=dict(
            showgrid=False,
            tickformat="%b %Y",
        ),
        yaxis=dict(
            tickformat=",",
            gridcolor="#E5E5E0",
            zeroline=False,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS England MI-ADHD (February 2026 release), indicators ADHD003a–d summed across age groups. '
        'Validated against the official 562,480 December 2025 figure in '
        '<a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/02_mi_adhd_ingestion.ipynb" '
        'style="color: #1F4E79;">notebook 02</a>.'
        '</div>',
        unsafe_allow_html=True,
    )
