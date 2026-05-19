"""
app/views/demographics.py — Demographics view.

Three sections: age distribution, ethnicity distribution, and the
disparity chart (CCO referral shares vs Census 2021 child population shares).

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data.loader import (
    chart_data_age_distribution,
    chart_data_ethnicity_distribution,
    chart_data_ethnicity_disparity,
    plotly_axis_style,
    PLOTLY_FONT,
    INK,
)


def render():
    _render_age()
    _render_ethnicity()
    _render_disparity()


def _render_age():
    st.markdown(
        '<div class="ace-section-title">Open list by age group</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_age_distribution()
    latest = data["date_start"].iloc[0]

    st.markdown(
        f'<div class="ace-section-intro">'
        f'Open ADHD referrals by age group at {latest.strftime("%B %Y")}. '
        f'Adults aged 25+ are the majority of the list. ADHD is no longer accurately '
        f'framed as a primarily childhood condition.'
        f'</div>',
        unsafe_allow_html=True,
    )

    data = data.copy()
    data["label"] = data.apply(lambda r: f"{r['value']:,.0f} ({r['share']:.1%})", axis=1)

    fig = px.bar(
        data,
        x="age_band_short",
        y="value",
        text="label",
        color="age_band_short",
        color_discrete_sequence=px.colors.sequential.Teal[2:],
        labels={"age_band_short": "", "value": "Open referrals"},
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        textfont=dict(color=INK, size=12),
    )
    fig.update_layout(
        showlegend=False,
        height=440,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        xaxis=plotly_axis_style(title_text=""),
        yaxis={
            **plotly_axis_style(title_text="Open referrals", tickformat=","),
            "range": [0, data["value"].max() * 1.22],
        },
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS England MI-ADHD (February 2026 release), indicator ADHD003 by Age Group breakdown. '
        'See <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/03_mi_adhd_eda.ipynb" '
        'style="color: #1F4E79;">notebook 03</a>, Chart 3.'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_ethnicity():
    st.markdown(
        '<div class="ace-section-title">Open list by ethnicity</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_ethnicity_distribution()
    latest = data["date_start"].iloc[0]

    st.markdown(
        f'<div class="ace-section-intro">'
        f'Open ADHD referrals by ethnicity at {latest.strftime("%B %Y")}. '
        f'Raw counts only — per-capita disparity is in the next section. '
        f'"UNKNOWN" and "Not stated" combined account for around 22.8% of the list, '
        f'a ceiling on per-capita disparity analysis from MI-ADHD alone.'
        f'</div>',
        unsafe_allow_html=True,
    )

    data = data.copy()
    data["label"] = data.apply(
        lambda r: f"{r['value']:,.0f} ({r['share']:.1%})", axis=1
    )

    fig = px.bar(
        data,
        x="value",
        y="ethnicity_raw",
        text="label",
        orientation="h",
        color="value",
        color_continuous_scale="Teal",
        labels={"value": "Open referrals", "ethnicity_raw": ""},
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        textfont=dict(color=INK, size=11),
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        height=max(440, 28 * data.shape[0] + 40),
        margin=dict(l=10, r=100, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        xaxis={
            **plotly_axis_style(title_text="Open referrals", tickformat=","),
            "range": [0, data["value"].max() * 1.20],
        },
        yaxis=plotly_axis_style(title_text=""),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS England MI-ADHD (February 2026 release), indicator ADHD003 by Ethnicity breakdown. '
        'See <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/03_mi_adhd_eda.ipynb" '
        'style="color: #1F4E79;">notebook 03</a>, Chart 4.'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_disparity():
    st.markdown(
        '<div class="ace-section-title">The disparity finding: ADHD referrals vs population</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_ethnicity_disparity()

    st.markdown(
        '<div class="ace-section-intro">'
        'Children\'s Commissioner October 2024 report, page 108: ADHD child referral shares by ethnicity, '
        'compared to Census 2021 child population shares. Asian children are ~12% of the child population '
        'but 1.4% of ADHD referrals — an under-representation ratio of roughly 9 to 1. The pattern is '
        'present across most non-White groups; sharpest for Asian children. Bars sorted by under-representation '
        '(most under-represented at top). This is the analytical centrepiece of the project.'
        '</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=data["ethnicity"],
        x=data["adhd_referral_share"],
        orientation="h",
        name="Share of ADHD referrals (CCO 2024)",
        marker_color="#1F4E79",
        text=[f"{v:.1f}%" for v in data["adhd_referral_share"]],
        textposition="outside",
        textfont=dict(color=INK, size=11),
        cliponaxis=False,
    ))
    fig.add_trace(go.Bar(
        y=data["ethnicity"],
        x=data["child_population_share"],
        orientation="h",
        name="Share of child population (Census 2021)",
        marker_color="#9BC2E6",
        text=[f"{v:.1f}%" for v in data["child_population_share"]],
        textposition="outside",
        textfont=dict(color=INK, size=11),
        cliponaxis=False,
    ))
    fig.update_layout(
        barmode="group",
        height=480,
        margin=dict(l=10, r=60, t=30, b=10),
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
            font=dict(size=12, color=INK),
        ),
        xaxis={
            **plotly_axis_style(title_text="Share of children", tickformat=".0f"),
            "ticksuffix": "%",
            "range": [0, max(data["child_population_share"].max(), data["adhd_referral_share"].max()) * 1.18],
        },
        yaxis={**plotly_axis_style(title_text=""), "autorange": "reversed"},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Sources: Children\'s Commissioner for England, "Waiting times for assessment and support for '
        'autism, ADHD and other neurodevelopmental conditions" (October 2024), page 108. Population '
        'denominators from ONS Census 2021. See '
        '<a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/04_uk_neurodev_consolidation.ipynb" '
        'style="color: #1F4E79;">notebook 04</a>.'
        '</div>',
        unsafe_allow_html=True,
    )
