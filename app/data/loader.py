"""
app/data/loader.py — reads the harmonised fact table and exposes
helper functions for the dashboard.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PARQUET_PATH = PROJECT_ROOT / "data" / "processed" / "adhd_atlas_fact.parquet"


INK         = "#1A1A1A"
INK_DIM     = "#555555"
GRID        = "#E5E5E0"
NAVY        = "#1F4E79"

PLOTLY_FONT = dict(
    family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    color=INK,
    size=12,
)


def plotly_axis_style(title_text: str = "", tickformat: str = None) -> dict:
    style = dict(
        title=dict(text=title_text, font=dict(color=INK, size=13)),
        tickfont=dict(color=INK_DIM, size=11),
        showgrid=False,
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
    )
    if tickformat is not None:
        style["tickformat"] = tickformat
    return style


CENSUS_2021_CHILD_SHARES = {
    "white": 73.0,
    "asian": 12.0,
    "black": 6.0,
    "mixed": 7.0,
    "other": 1.5,
}


WAITING_BAND_MAP = {
    "ADHD003a": "Up to 13 weeks",
    "ADHD003b": "13 to 52 weeks",
    "ADHD003c": "52 to 104 weeks",
    "ADHD003d": "104 weeks or more",
}
WAITING_BAND_ORDER = ["Up to 13 weeks", "13 to 52 weeks", "52 to 104 weeks", "104 weeks or more"]
WAITING_BAND_COLOURS = {
    "Up to 13 weeks":    "#2E7D32",
    "13 to 52 weeks":    "#FBC02D",
    "52 to 104 weeks":   "#EF6C00",
    "104 weeks or more": "#C62828",
}


AGE_BAND_ORDER = [
    "People aged 0 to 4",
    "People aged 5 to 17",
    "People aged 18 to 24",
    "People aged 25+",
    "People aged Unknown",
]


@st.cache_data(ttl=3600)
def load_fact_table() -> pd.DataFrame:
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(
            f"adhd_atlas_fact.parquet not found at {PARQUET_PATH}. "
            "Run notebooks/06_harmonisation_duckdb.ipynb to generate it."
        )
    return pd.read_parquet(PARQUET_PATH)


# --- Data freshness ---

@st.cache_data(ttl=3600)
def data_freshness() -> dict:
    df = load_fact_table()
    sources_latest = {}
    for src in ["mi_adhd", "opensafely", "cco", "commons_library"]:
        sub = df[df["source"] == src]
        if not sub.empty:
            sources_latest[src] = sub["date_start"].max()
    parquet_mtime = datetime.fromtimestamp(PARQUET_PATH.stat().st_mtime)
    return {
        "sources_latest": sources_latest,
        "parquet_built": parquet_mtime,
    }


# --- KPI computations ---

@st.cache_data(ttl=3600)
def kpi_open_referrals() -> dict:
    df = load_fact_table()
    mask = (
        (df["source"] == "mi_adhd")
        & (df["measure_code"] == "ADHD003")
        & (df["age_band_raw"].notna())
    )
    latest = df.loc[mask, "date_start"].max()
    total = df.loc[mask & (df["date_start"] == latest), "value"].sum()
    return {"value": int(total), "date": latest}


@st.cache_data(ttl=3600)
def kpi_total_waiting_list() -> dict:
    df = load_fact_table()
    mask = (
        (df["source"] == "commons_library")
        & (df["measure_name"].str.contains("Total people", case=False, na=False))
    )
    row = df.loc[mask, ["value", "date_start"]]
    if row.empty:
        return {"value": None, "date": None}
    return {"value": int(row["value"].iloc[0]), "date": row["date_start"].iloc[0]}


@st.cache_data(ttl=3600)
def kpi_share_104_weeks() -> dict:
    df = load_fact_table()
    mask_total = (
        (df["source"] == "mi_adhd")
        & (df["measure_code"] == "ADHD003")
        & (df["age_band_raw"].notna())
    )
    latest = df.loc[mask_total, "date_start"].max()
    total = df.loc[mask_total & (df["date_start"] == latest), "value"].sum()

    band = df.loc[
        (df["source"] == "mi_adhd")
        & (df["measure_code"] == "ADHD003d")
        & (df["date_start"] == latest)
        & (df["age_band_raw"].notna()),
        "value"
    ].sum()

    share = band / total if total > 0 else 0
    return {"value": share, "date": latest}


@st.cache_data(ttl=3600)
def kpi_female_diagnosis_growth() -> dict:
    df = load_fact_table()
    sub = df.loc[
        (df["source"] == "opensafely")
        & (df["measure_code"] == "ADHD_recorded_prevalence")
        & (df["sex"] == "female")
    ].copy()

    sub["num"] = sub["value"] / 100.0 * sub["denominator"]
    annual = (
        sub.groupby("date_start", as_index=False)
           .agg(numerator=("num", "sum"), denominator=("denominator", "sum"))
    )
    annual["rate_pct"] = annual["numerator"] / annual["denominator"] * 100
    annual = annual.sort_values("date_start")

    if len(annual) < 2:
        return {"multiplier": None}

    first = annual.iloc[0]
    last = annual.iloc[-1]
    return {
        "multiplier": last["rate_pct"] / first["rate_pct"] if first["rate_pct"] > 0 else None,
        "first_rate_pct": float(first["rate_pct"]),
        "last_rate_pct": float(last["rate_pct"]),
        "first_date": first["date_start"],
        "last_date": last["date_start"],
    }


@st.cache_data(ttl=3600)
def kpi_asian_underrepresentation() -> dict:
    df = load_fact_table()
    row = df.loc[
        (df["source"] == "cco")
        & (df["measure_code"] == "ADHD_referral_share_by_ethnicity")
        & (df["ethnicity_coarse"] == "asian"),
        "value"
    ]
    if row.empty:
        return {"ratio": None}

    referral_share = float(row.iloc[0])
    census_share = CENSUS_2021_CHILD_SHARES["asian"]
    return {
        "ratio": census_share / referral_share,
        "referral_share_pct": referral_share,
        "census_share_pct": census_share,
    }


# --- Chart data ---

@st.cache_data(ttl=3600)
def chart_data_open_referrals_by_band() -> pd.DataFrame:
    df = load_fact_table()
    sub = df.loc[
        (df["source"] == "mi_adhd")
        & (df["measure_code"].isin(WAITING_BAND_MAP.keys()))
        & (df["age_band_raw"].notna())
    ]
    out = (
        sub.groupby(["date_start", "measure_code"], as_index=False)
           .agg(value=("value", "sum"))
    )
    out["band"] = out["measure_code"].map(WAITING_BAND_MAP)
    return out


@st.cache_data(ttl=3600)
def chart_data_share_by_band() -> pd.DataFrame:
    raw = chart_data_open_referrals_by_band()
    totals = (
        raw.groupby("date_start", as_index=False)["value"].sum()
           .rename(columns={"value": "total"})
    )
    out = raw.merge(totals, on="date_start")
    out["share"] = out["value"] / out["total"]
    return out


@st.cache_data(ttl=3600)
def chart_data_inflow_outflow() -> pd.DataFrame:
    df = load_fact_table()
    sub = df.loc[
        (df["source"] == "mi_adhd")
        & (df["measure_code"].isin(["ADHD006", "ADHD007"]))
        & (df["age_band_raw"].notna())
    ]
    out = (
        sub.groupby(["date_start", "measure_code"], as_index=False)
           .agg(value=("value", "sum"))
    )
    out["flow"] = out["measure_code"].map({
        "ADHD007": "New referrals received (inflow)",
        "ADHD006": "Referrals closed (outflow)",
    })
    return out


@st.cache_data(ttl=3600)
def chart_data_stock_vs_flow() -> pd.DataFrame:
    df = load_fact_table()

    stock = (
        df.loc[
            (df["source"] == "mi_adhd")
            & (df["measure_code"] == "ADHD003")
            & (df["age_band_raw"].notna())
        ]
        .groupby("date_start", as_index=False)["value"]
        .sum()
        .rename(columns={"value": "open_list"})
    )
    stock["observed_change"] = stock["open_list"].diff()

    flow = (
        df.loc[
            (df["source"] == "mi_adhd")
            & (df["measure_code"].isin(["ADHD006", "ADHD007"]))
            & (df["age_band_raw"].notna())
        ]
        .groupby(["date_start", "measure_code"], as_index=False)["value"]
        .sum()
    )
    flow_pivot = flow.pivot(index="date_start", columns="measure_code", values="value").reset_index()
    flow_pivot["net_flow"] = flow_pivot.get("ADHD007", 0) - flow_pivot.get("ADHD006", 0)

    out = stock.merge(flow_pivot[["date_start", "net_flow"]], on="date_start", how="left")
    return out


@st.cache_data(ttl=3600)
def chart_data_age_distribution() -> pd.DataFrame:
    """Open list (ADHD003) by age group at the latest date with full data."""
    df = load_fact_table()
    mask = (
        (df["source"] == "mi_adhd")
        & (df["measure_code"] == "ADHD003")
        & (df["age_band_raw"].notna())
    )
    latest = df.loc[mask, "date_start"].max()
    sub = df.loc[
        mask & (df["date_start"] == latest),
        ["age_band_raw", "value", "date_start"]
    ].copy()
    sub["age_band_raw"] = pd.Categorical(sub["age_band_raw"], categories=AGE_BAND_ORDER, ordered=True)
    sub = sub.sort_values("age_band_raw")
    total = sub["value"].sum()
    sub["share"] = sub["value"] / total if total > 0 else 0
    sub["age_band_short"] = sub["age_band_raw"].astype(str).str.replace("People aged ", "", regex=False)
    return sub


@st.cache_data(ttl=3600)
def chart_data_ethnicity_distribution() -> pd.DataFrame:
    """Open list (ADHD003) by ethnicity at the latest date with ethnicity breakdown."""
    df = load_fact_table()
    mask = (
        (df["source"] == "mi_adhd")
        & (df["measure_code"] == "ADHD003")
        & (df["ethnicity_raw"].notna())
    )
    latest = df.loc[mask, "date_start"].max()
    sub = df.loc[
        mask & (df["date_start"] == latest),
        ["ethnicity_raw", "value", "date_start"]
    ].copy()
    sub = sub.sort_values("value", ascending=True)
    total = sub["value"].sum()
    sub["share"] = sub["value"] / total if total > 0 else 0
    return sub


@st.cache_data(ttl=3600)
def chart_data_ethnicity_disparity() -> pd.DataFrame:
    """
    Children's Commissioner p108 ADHD referral shares by ethnicity vs
    Census 2021 child population shares. Excludes 'unknown' since Census has no
    matching category. Sorted by under-representation (smallest ratio at top).
    """
    df = load_fact_table()
    cco = df.loc[
        (df["source"] == "cco")
        & (df["measure_code"] == "ADHD_referral_share_by_ethnicity")
    ].copy()

    rows = []
    for _, r in cco.iterrows():
        coarse = r["ethnicity_coarse"]
        if coarse == "unknown" or coarse not in CENSUS_2021_CHILD_SHARES:
            continue
        rows.append({
            "ethnicity":               r["ethnicity_raw"],
            "ethnicity_coarse":        coarse,
            "adhd_referral_share":     float(r["value"]),
            "child_population_share":  CENSUS_2021_CHILD_SHARES[coarse],
        })

    out = pd.DataFrame(rows)
    out["under_rep_ratio"] = out["child_population_share"] / out["adhd_referral_share"]
    out = out.sort_values("under_rep_ratio", ascending=False).reset_index(drop=True)
    return out


# --- Formatters for display ---

def fmt_count(n) -> str:
    if n is None:
        return "—"
    return f"{n:,}"


def fmt_count_short(n) -> str:
    if n is None:
        return "—"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def fmt_pct(x, decimals: int = 0) -> str:
    if x is None:
        return "—"
    return f"{x * 100:.{decimals}f}%"


def fmt_multiplier(x, decimals: int = 1) -> str:
    if x is None:
        return "—"
    return f"{x:.{decimals}f}x"


def fmt_ratio(x) -> str:
    if x is None:
        return "—"
    return f"~{round(x)} : 1"
