"""
app/views/methodology.py — Methodology view.

Seven sections: about, sources, live validation queries, definitions,
limitations, scope decisions, reproducibility.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

import pandas as pd
import streamlit as st

from data.loader import (
    data_freshness,
    load_fact_table,
    kpi_open_referrals,
    kpi_female_diagnosis_growth,
)


# Style constants
PROSE_STYLE = "font-size: 0.95rem; line-height: 1.7; color: #1A1A1A;"


def _prose(*paragraphs: str) -> str:
    """Render multiple paragraphs as continuous HTML — no blank lines between <p> tags."""
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    return f'<div style="{PROSE_STYLE}">{body}</div>'


def render():
    _render_about()
    _render_sources()
    _render_validation()
    _render_definitions()
    _render_limitations()
    _render_scope_decisions()
    _render_reproducibility()


def _render_about():
    st.markdown(
        '<div class="ace-section-title">About this project</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        _prose(
            "The ADHD Care Equity Tracker UK consolidates publicly available UK ADHD waiting-time "
            "data across multiple sources, documenting both the headline findings and the data "
            "quality limitations.",

            "The analytical work is in six numbered Jupyter notebooks (in <code>notebooks/</code>) "
            "which ingest, clean, validate, and harmonise data from NHS England MI-ADHD, the "
            "Children's Commissioner for England, OpenSAFELY, and the House of Commons Library. "
            "The resulting fact table reproduces every source's published headline figure to the unit.",

            "<strong>This is an educational research artefact built as part of an MSc Applied AI "
            "portfolio.</strong> It is not a clinical tool, not a peer-reviewed analysis, and not "
            "a substitute for official NHS statistics.",
        ),
        unsafe_allow_html=True,
    )


def _render_sources():
    st.markdown(
        '<div class="ace-section-title">Data sources</div>',
        unsafe_allow_html=True,
    )

    fresh = data_freshness()

    sources = [
        ("NHS England MI-ADHD",
         "Open referral counts, waiting bands, flow, age and ethnicity breakdowns",
         fresh["sources_latest"].get("mi_adhd"),
         "Open Government Licence v3.0"),
        ("OpenSAFELY ADHD analysis",
         "9-year diagnosis prevalence, medication prevalence, time to prescription",
         fresh["sources_latest"].get("opensafely"),
         "Open Government Licence v3.0"),
        ("Children's Commissioner ND report (Oct 2024)",
         "Ethnicity referral shares (p108), waiting time headlines",
         fresh["sources_latest"].get("cco"),
         "Crown Copyright (fair dealing for research)"),
        ("Commons Library briefing CBP-10551",
         "Combined MHSDS + CHS SitRep waiting list total (2.76M)",
         fresh["sources_latest"].get("commons_library"),
         "Open Parliament Licence v3.0"),
    ]

    rows_html = ""
    for name, used_for, latest, licence in sources:
        latest_str = latest.strftime("%b %Y") if pd.notna(latest) else "—"
        rows_html += f"""
        <tr>
            <td style="padding: 0.75rem 1rem; border-bottom: 1px solid #E5E5E0; font-weight: 600; color: #1A1A1A; vertical-align: top;">{name}</td>
            <td style="padding: 0.75rem 1rem; border-bottom: 1px solid #E5E5E0; color: #1A1A1A; vertical-align: top;">{used_for}</td>
            <td style="padding: 0.75rem 1rem; border-bottom: 1px solid #E5E5E0; color: #555555; vertical-align: top; white-space: nowrap;">{latest_str}</td>
            <td style="padding: 0.75rem 1rem; border-bottom: 1px solid #E5E5E0; color: #555555; vertical-align: top;">{licence}</td>
        </tr>"""

    table_html = f"""
    <div style="background: #FFFFFF; border: 1px solid #E5E5E0; border-radius: 6px; overflow: hidden;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
            <thead>
                <tr style="background: #FAFAF8;">
                    <th style="text-align: left; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: #555555; border-bottom: 1px solid #E5E5E0;">Source</th>
                    <th style="text-align: left; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: #555555; border-bottom: 1px solid #E5E5E0;">Used for</th>
                    <th style="text-align: left; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: #555555; border-bottom: 1px solid #E5E5E0;">Latest data</th>
                    <th style="text-align: left; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: #555555; border-bottom: 1px solid #E5E5E0;">Licence</th>
                </tr>
            </thead>
            <tbody>{rows_html}
            </tbody>
        </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)


def _render_validation():
    st.markdown(
        '<div class="ace-section-title">Validation queries</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ace-section-intro">'
        'Three checks executed live against the harmonised parquet on every page load. '
        'All three must pass; if any fails the data pipeline has drifted from source and '
        'the dashboard\'s numbers cannot be trusted.'
        '</div>',
        unsafe_allow_html=True,
    )

    df = load_fact_table()

    # Validation 1
    k1 = kpi_open_referrals()
    v1_ok = k1["value"] == 562480
    _render_validation_row(
        "1. MI-ADHD ADHD003 open referrals at Dec 2025",
        f"computed: {k1['value']:,}",
        "official: 562,480",
        v1_ok,
    )

    # Validation 2
    k4 = kpi_female_diagnosis_growth()
    v2_ok = (
        k4["multiplier"] is not None
        and 5.5 < k4["multiplier"] < 6.0
        and 0.15 < k4["first_rate_pct"] < 0.17
        and 0.85 < k4["last_rate_pct"] < 0.95
    )
    _render_validation_row(
        "2. OpenSAFELY female ADHD prevalence growth",
        f"computed: {k4['first_rate_pct']:.3f}% to {k4['last_rate_pct']:.3f}% ({k4['multiplier']:.2f}x)",
        "expected: 0.160% to 0.923% (5.8x)",
        v2_ok,
    )

    # Validation 3
    cco_shares = df.loc[
        (df["source"] == "cco")
        & (df["measure_code"] == "ADHD_referral_share_by_ethnicity"),
        "value"
    ]
    eth_sum = cco_shares.sum()
    v3_ok = 99.5 <= eth_sum <= 100.5
    _render_validation_row(
        "3. CCO p108 ethnicity shares sum to 100%",
        f"computed: {eth_sum:.1f}%",
        "expected: 100.0% (small rounding allowed)",
        v3_ok,
    )


def _render_validation_row(title, computed, expected, passed):
    status_color = "#2E7D32" if passed else "#C62828"
    status_text = "PASS" if passed else "FAIL"
    st.markdown(
        f'<div style="background: #FFFFFF; border: 1px solid #E5E5E0; border-left: 3px solid {status_color}; '
        f'border-radius: 4px; padding: 0.85rem 1rem; margin-bottom: 0.75rem; font-size: 0.9rem; line-height: 1.5;">'
        f'<div style="display: flex; justify-content: space-between; align-items: baseline;">'
        f'<strong style="color: #1A1A1A;">{title}</strong>'
        f'<span style="color: {status_color}; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.06em;">{status_text}</span>'
        f'</div>'
        f'<div style="color: #555555; margin-top: 0.4rem; font-family: Consolas, Monaco, monospace; font-size: 0.85rem;">'
        f'<div>{computed}</div><div>{expected}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_definitions():
    st.markdown(
        '<div class="ace-section-title">Definitions</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        _prose(
            "<strong>Open referral</strong> — a referral for ADHD assessment that has been received "
            "by NHS services and not yet closed. Includes both children and adults across all NHS "
            "Mental Health Services in England.",

            "<strong>ADHD003</strong> — NHS England MI-ADHD indicator: number of open referrals at "
            "the end of the reporting month. Stratified into ADHD003a (up to 13 weeks), "
            "ADHD003b (13–52 weeks), ADHD003c (52–104 weeks), ADHD003d (104 weeks or more).",

            "<strong>ADHD006</strong> / <strong>ADHD007</strong> — closed and new referrals "
            "respectively, each month. The flow indicators.",

            "<strong>MHSDS</strong> — Mental Health Services Dataset, the data feed underlying "
            "MI-ADHD. Captures referrals through Mental Health Services. Does not include "
            "Community Health Services referrals, which is why MI-ADHD's 562k and the Commons "
            "Library's 2.76m differ.",

            "<strong>CHS SitRep</strong> — Community Health Services Situation Report. Includes "
            "children and young people waiting for community-based ADHD assessment that does not "
            "route through Mental Health Services.",

            "<strong>OpenSAFELY</strong> — NHS Digital's federated GP-data analytics platform. "
            "ADHD analyses cover patients registered at TPP-system GP practices, approximately "
            "44% of England's GP-registered population.",

            "<strong>Diagnosis prevalence</strong> — share of patients in the GP-registered "
            "population with an ADHD diagnosis recorded in their primary-care record. Different "
            "from incidence (new diagnoses per year).",

            "<strong>Under-representation ratio</strong> — for a population subgroup, (share of "
            "child population) divided by (share of ADHD referrals). Asian children: 12% / 1.4% "
            "≈ 8.6, presented as ~9 : 1.",
        ),
        unsafe_allow_html=True,
    )


def _render_limitations():
    st.markdown(
        '<div class="ace-section-title">Data quality and limitations</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        _prose(
            "<strong>National-level data only.</strong> MI-ADHD publishes England-level numbers "
            "with breakdowns by age, ethnicity, and waiting band but no regional, ICB, or Sub-ICB "
            "stratification. The Children's Commissioner October 2024 report partly fills the "
            "demographic dimensions but not the geographic one.",

            "<strong>Short MI-ADHD activity time series.</strong> Activity indicators (ADHD003, "
            "ADHD006, ADHD007) have 13 months of data at the time of writing. Too short for "
            "credible long-horizon forecasting, particularly given the unresolved stock-flow "
            "reconciliation gap.",

            "<strong>22.8% unknown ethnicity in MI-ADHD.</strong> The MI-ADHD ethnicity breakdown "
            "includes \"UNKNOWN\" and \"Not stated\" categories that together represent "
            "approximately 22.8% of records. Per-capita disparity analysis from MI-ADHD alone is "
            "bounded by this missingness, which is why the disparity finding uses the Children's "
            "Commissioner report instead.",

            "<strong>Stock-flow reconciliation gap.</strong> MI-ADHD's published flow indicators "
            "(ADHD006 closed, ADHD007 new) account for only about 20% of the observed monthly "
            "change in the stock indicator (ADHD003 open). The remaining ~80% appears to be "
            "retrospective adjustments under MHSDS's multiple-submission window model, "
            "definitional overlap, or provider submission incompleteness. Documented in "
            "notebook 03, chart 6.",

            "<strong>OpenSAFELY 44% coverage.</strong> OpenSAFELY's ADHD analyses use TPP GP "
            "practice data, covering approximately 44% of England's GP-registered population. "
            "The remaining 56% (predominantly EMIS) is not in this analysis. Findings on "
            "diagnosis and prescribing rates may not perfectly generalise to the full population, "
            "though TPP coverage is broadly representative geographically.",

            "<strong>UK jurisdiction gaps.</strong> Scotland, Wales, and Northern Ireland data is "
            "not covered in the current iteration. Scotland's neurodevelopmental waits are not "
            "routinely published; Welsh and Northern Irish data is fragmented across different "
            "publishers.",

            "<strong>Approximate values in some sections.</strong> Where source data provides "
            "medians broken down by both sex and age, the dashboard averages those medians for "
            "display (in the time-to-prescription chart). This is statistically imperfect — "
            "medians cannot be cleanly averaged — but the alternative of doubling the chart with "
            "sex-split lines harms readability. Flagged in the relevant chart's source line.",
        ),
        unsafe_allow_html=True,
    )


def _render_scope_decisions():
    st.markdown(
        '<div class="ace-section-title">Scope decisions</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        _prose(
            "<strong>Notebook 04 was originally scoped as ADHD UK patient survey ingestion.</strong> "
            "Replaced with the Children's Commissioner October 2024 report — a statutory body's "
            "analysis joining MHSDS with CSDS, containing the geographic and demographic "
            "breakdowns that MI-ADHD does not publish. ADHD UK is a campaigning charity; their "
            "published material is narrative rather than structured.",

            "<strong>Notebook 05 was originally scoped as Right to Choose provider data "
            "scraping.</strong> Replaced with OpenSAFELY's 9-year analysis of ADHD diagnosis and "
            "prescribing rates published alongside MI-ADHD, plus headline figures from House of "
            "Commons Library briefing CBP-10551. OpenSAFELY's series is longer, cleaner, and more "
            "authoritative than scraped provider pages.",

            "<strong>Notebook 07 (forecasting) was dropped from scope.</strong> MI-ADHD's "
            "13-month activity series is too short, and the 80% stock-flow reconciliation gap is "
            "too large, to support credible long-horizon projection. A short illustrative "
            "extrapolation with heavy caveats was considered and rejected: dressing noisy data in "
            "modelling polish would weaken the project, not strengthen it.",
        ),
        unsafe_allow_html=True,
    )


def _render_reproducibility():
    st.markdown(
        '<div class="ace-section-title">Reproducibility</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        _prose(
            'Source code and notebooks are public at '
            '<a href="https://github.com/noble-chidera-onyema/adhd-care-equity-tracker" '
            'style="color: #1F4E79;">github.com/noble-chidera-onyema/adhd-care-equity-tracker</a>. '
            'Licence: All Rights Reserved.',

            'To reproduce locally:',
        ),
        unsafe_allow_html=True,
    )

    st.code(
        '''git clone https://github.com/noble-chidera-onyema/adhd-care-equity-tracker.git
cd adhd-care-equity-tracker
py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

# Run notebooks 02-06 in order — they download source data on first run
jupyter lab

# After notebooks 02-06 finish, launch the dashboard
cd app
streamlit run streamlit_app.py''',
        language="bash",
    )

    st.markdown(
        _prose(
            "Notebooks 01 to 05 download their source data from NHS England and other publishers "
            "on first run. Notebook 06 reads the processed outputs of 02, 04, and 05 and builds "
            "the harmonised DuckDB fact table and parquet.",

            "<strong>Contact:</strong> Noble Chidera Onyema, onyemanoble1628@gmail.com",
        ),
        unsafe_allow_html=True,
    )
