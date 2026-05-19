"""
app/views/waiting_times.py — Waiting Times view.

Three sections: composition of the queue, inflow vs outflow,
stock-vs-flow reconciliation (the 80% data-quality finding).

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data.loader import (
    chart_data_share_by_band,
    chart_data_inflow_outflow,
    chart_data_stock_vs_flow,
    plotly_axis_style,
    PLOTLY_FONT,
    WAITING_BAND_ORDER,
    WAITING_BAND_COLOURS,
)


def render():
    _render_share_by_band()
    _render_inflow_outflow()
    _render_reconciliation()


def _render_share_by_band():
    st.markdown(
        '<div class="ace-section-title">Composition of the queue over time</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ace-section-intro">'
        'Same open list as the Overview chart, normalised so each month sums to 100%. '
        'Strips out list size; just shows composition. The 104+ band is both larger and '
        'more dominant by Dec 2025 than 12 months earlier.'
        '</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_share_by_band()
    fig = px.area(
        data,
        x="date_start",
        y="share",
        color="band",
        category_orders={"band": WAITING_BAND_ORDER},
        color_discrete_map=WAITING_BAND_COLOURS,
        groupnorm="fraction",
        labels={"date_start": "Month", "share": "Share of open list", "band": ""},
    )
    fig.update_layout(
        height=460,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="left",
            x=0,
            title_text="",
            font=dict(size=12, color="#1A1A1A"),
        ),
        hovermode="x unified",
        xaxis=plotly_axis_style(title_text="Month", tickformat="%b %Y"),
        yaxis={**plotly_axis_style(title_text="Share of open list", tickformat=".0%"), "range": [0, 1]},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS England MI-ADHD (February 2026 release), indicators ADHD003a–d. '
        'See <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/03_mi_adhd_eda.ipynb" '
        'style="color: #1F4E79;">notebook 03</a>, Chart 2.'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_inflow_outflow():
    st.markdown(
        '<div class="ace-section-title">Monthly inflow and outflow</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ace-section-intro">'
        'ADHD007 (inflow, new referrals received) versus ADHD006 (outflow, referrals closed). '
        'Inflow exceeds outflow in 11 of 13 months. Under a simple bathtub model the queue should '
        'grow each month by inflow minus outflow.'
        '</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_inflow_outflow()
    fig = px.line(
        data,
        x="date_start",
        y="value",
        color="flow",
        markers=True,
        color_discrete_map={
            "New referrals received (inflow)": "#C62828",
            "Referrals closed (outflow)":      "#2E7D32",
        },
        labels={"date_start": "Month", "value": "Referrals per month", "flow": ""},
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig.update_layout(
        height=440,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.24,
            xanchor="left",
            x=0,
            title_text="",
            font=dict(size=12, color="#1A1A1A"),
        ),
        hovermode="x unified",
        xaxis=plotly_axis_style(title_text="Month", tickformat="%b %Y"),
        yaxis=plotly_axis_style(title_text="Referrals per month", tickformat=","),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS England MI-ADHD (February 2026 release), indicators ADHD006 and ADHD007. '
        'See <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/03_mi_adhd_eda.ipynb" '
        'style="color: #1F4E79;">notebook 03</a>, Chart 5.'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_reconciliation():
    st.markdown(
        '<div class="ace-section-title">Stock vs flow reconciliation: the data quality finding</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ace-section-intro">'
        'If the bathtub model held, the observed monthly change in the open list would equal that '
        'month\'s net flow. It doesn\'t. Net flow accounts for only ~20% of the actual queue movement. '
        'The remaining ~80% (~163,000 referrals over 13 months) is unexplained by the published flow '
        'indicators. Anyone using MI-ADHD for forecasting must model this gap explicitly.'
        '</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_stock_vs_flow().dropna(subset=["observed_change"])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["date_start"],
        y=data["observed_change"],
        name="Observed change in open list",
        marker_color="#1F4E79",
    ))
    fig.add_trace(go.Bar(
        x=data["date_start"],
        y=data["net_flow"],
        name="Net flow (inflow minus outflow)",
        marker_color="#9BC2E6",
    ))
    fig.update_layout(
        barmode="group",
        height=440,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.24,
            xanchor="left",
            x=0,
            title_text="",
            font=dict(size=12, color="#1A1A1A"),
        ),
        hovermode="x unified",
        xaxis=plotly_axis_style(title_text="Month", tickformat="%b %Y"),
        yaxis={**plotly_axis_style(title_text="Referrals", tickformat=","), "zeroline": True, "zerolinecolor": "#A0A0A0"},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'The gap between bars each month is unexplained by published flow data. '
        'See <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/03_mi_adhd_eda.ipynb" '
        'style="color: #1F4E79;">notebook 03</a>, Chart 6.'
        '</div>',
        unsafe_allow_html=True,
    )
