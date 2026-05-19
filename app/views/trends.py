"""
app/views/trends.py — Trends view.

Three sections from the OpenSAFELY 9-year analysis:
1. ADHD diagnosis prevalence by sex (the 5.8x female growth story)
2. 6-month medication prevalence among diagnosed
3. Time from diagnosis to first prescription, by age band

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

import plotly.express as px
import streamlit as st

from data.loader import (
    chart_data_diagnosis_prevalence_by_sex,
    chart_data_medication_6month_by_sex,
    chart_data_time_to_prescription,
    plotly_axis_style,
    PLOTLY_FONT,
    INK,
)


SEX_COLOURS = {
    "male":   "#1F4E79",
    "female": "#C62828",
}

SEX_PRETTY = {
    "male":   "Male",
    "female": "Female",
}

AGE_BAND_COLOURS = {
    "0 to 9":      "#2E7D32",
    "10 to 17":    "#558B2F",
    "18 to 24":    "#FBC02D",
    "25 to 34":    "#EF6C00",
    "35 and over": "#C62828",
}

KEY_AGE_BANDS = ["0 to 9", "10 to 17", "18 to 24", "25 to 34", "35 and over"]


def render():
    _render_prevalence()
    _render_medication()
    _render_time_to_prescription()


def _render_prevalence():
    st.markdown(
        '<div class="ace-section-title">Recorded ADHD diagnosis prevalence, by sex</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_diagnosis_prevalence_by_sex().copy()
    data["sex_pretty"] = data["sex"].map(SEX_PRETTY)

    st.markdown(
        '<div class="ace-section-intro">'
        'Annual rate of ADHD diagnosis recorded in GP records, from OpenSAFELY '
        '(TPP-system GPs only, covers ~44% of England). Female rate has grown 5.8x over nine years, '
        'male rate 2.3x. Female rate in 2024/25 is approaching the male rate of 2016/17. '
        'The trajectories converge slowly.'
        '</div>',
        unsafe_allow_html=True,
    )

    fig = px.line(
        data,
        x="date_start",
        y="rate_pct",
        color="sex_pretty",
        markers=True,
        color_discrete_map={SEX_PRETTY["male"]: SEX_COLOURS["male"],
                            SEX_PRETTY["female"]: SEX_COLOURS["female"]},
        labels={"date_start": "Year (April start)", "rate_pct": "Diagnosis prevalence", "sex_pretty": ""},
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig.update_layout(
        height=440,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="left", x=0,
                    title_text="", font=dict(size=12, color=INK)),
        hovermode="x unified",
        xaxis={**plotly_axis_style(title_text="Year (April start)", tickformat="%Y"), "dtick": "M12"},
        yaxis={**plotly_axis_style(title_text="Diagnosis prevalence", tickformat=".2f"), "ticksuffix": "%"},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS Digital OpenSAFELY ADHD analysis (Nov 2025 release), table 1, '
        'ADHD_recorded_prevalence. Rate is population-weighted across age bands within each '
        'year-sex. See <a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/05_opensafely_and_commons_library.ipynb" '
        'style="color: #1F4E79;">notebook 05</a>.'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_medication():
    st.markdown(
        '<div class="ace-section-title">Medication prevalence among diagnosed, six-month rolling</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_medication_6month_by_sex().copy()
    data["sex_pretty"] = data["sex"].map(SEX_PRETTY)

    st.markdown(
        '<div class="ace-section-intro">'
        'Share of patients with an ADHD diagnosis who received any ADHD medication in the '
        'previous six months. Around 27-29% by 2024/25. The remaining 70%+ either had '
        'medication treatment paused, never started, or were intentionally untreated. '
        'The data does not distinguish these cases.'
        '</div>',
        unsafe_allow_html=True,
    )

    fig = px.line(
        data,
        x="date_start",
        y="rate_pct",
        color="sex_pretty",
        markers=True,
        color_discrete_map={SEX_PRETTY["male"]: SEX_COLOURS["male"],
                            SEX_PRETTY["female"]: SEX_COLOURS["female"]},
        labels={"date_start": "Month", "rate_pct": "% diagnosed on medication", "sex_pretty": ""},
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    fig.update_layout(
        height=440,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="left", x=0,
                    title_text="", font=dict(size=12, color=INK)),
        hovermode="x unified",
        xaxis=plotly_axis_style(title_text="Month", tickformat="%b %Y"),
        yaxis={**plotly_axis_style(title_text="Share of diagnosed on medication", tickformat=".0f"), "ticksuffix": "%"},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS Digital OpenSAFELY ADHD analysis (Nov 2025 release), table 4, '
        'ADHD_patients_with_medication_prev_6_months. See '
        '<a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/05_opensafely_and_commons_library.ipynb" '
        'style="color: #1F4E79;">notebook 05</a>.'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_time_to_prescription():
    st.markdown(
        '<div class="ace-section-title">Time from ADHD diagnosis to first prescription</div>',
        unsafe_allow_html=True,
    )

    data = chart_data_time_to_prescription()
    data = data[data["age_band_raw"].isin(KEY_AGE_BANDS)].copy()

    st.markdown(
        '<div class="ace-section-intro">'
        'Median weeks between ADHD diagnosis and first medication prescription, by age band, '
        'by year. For ages 10-17 the median has doubled from 18 weeks in 2016/17 to 36 weeks '
        'in 2024/25. Treatment access bottlenecks even after diagnosis: ~9 months waiting between '
        'diagnosis and first prescription is now typical for children.'
        '</div>',
        unsafe_allow_html=True,
    )

    fig = px.line(
        data,
        x="date_start",
        y="weeks",
        color="age_band_raw",
        markers=True,
        category_orders={"age_band_raw": KEY_AGE_BANDS},
        color_discrete_map=AGE_BAND_COLOURS,
        labels={"date_start": "Year (April start)", "weeks": "Median weeks", "age_band_raw": "Age band"},
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig.update_layout(
        height=460,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOTLY_FONT,
        legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="left", x=0,
                    title_text="", font=dict(size=12, color=INK)),
        hovermode="x unified",
        xaxis={**plotly_axis_style(title_text="Year (April start)", tickformat="%Y"), "dtick": "M12"},
        yaxis=plotly_axis_style(title_text="Median weeks", tickformat=".0f"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div style="font-size: 0.8rem; color: #555555; margin-top: 0.5rem; line-height: 1.5;">'
        'Source: NHS Digital OpenSAFELY ADHD analysis (Nov 2025 release), table 5, '
        'Median_time_diagnosis_to_medication_weeks. Values shown are the mean of male and '
        'female medians within each year-band; approximate but illustrative. See '
        '<a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker/blob/main/notebooks/05_opensafely_and_commons_library.ipynb" '
        'style="color: #1F4E79;">notebook 05</a>.'
        '</div>',
        unsafe_allow_html=True,
    )
