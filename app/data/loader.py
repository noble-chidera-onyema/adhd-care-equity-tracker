"""
app/data/loader.py — reads the harmonised fact table and exposes
helper functions for the dashboard.

Functions are wrapped with @st.cache_data so the parquet is read once per
process and shared across all user sessions on the same Streamlit container.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

from pathlib import Path
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PARQUET_PATH = PROJECT_ROOT / "data" / "processed" / "adhd_atlas_fact.parquet"


# Census 2021 child ethnic-group shares for England, approximate.
# Used as the denominator side of the disparity ratio.
CENSUS_2021_CHILD_SHARES = {
    "white": 73.0,
    "asian": 12.0,
    "black": 6.0,
    "mixed": 7.0,
    "other": 1.5,
}


# Waiting-band labels and chart-friendly order. Matches notebook 03 Chart 1.
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


@st.cache_data(ttl=3600)
def load_fact_table() -> pd.DataFrame:
    """Load the harmonised fact table from data/processed/. Cached one hour."""
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(
            f"adhd_atlas_fact.parquet not found at {PARQUET_PATH}. "
            "Run notebooks/06_harmonisation_duckdb.ipynb to generate it."
        )
    return pd.read_parquet(PARQUET_PATH)


# --- KPI computations ---

@st.cache_data(ttl=3600)
def kpi_open_referrals() -> dict:
    """Open ADHD referrals (ADHD003) from MI-ADHD at the latest date with full data."""
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
    """Combined MHSDS + CHS waiting list, from Commons Library CBP-10551."""
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
    """Share of open list waiting 104+ weeks at the latest date."""
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
    """Female ADHD diagnosis rate growth multiplier, OpenSAFELY 9-year series."""
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
    """Asian children under-representation: Census share divided by referral share."""
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
    """
    Time series of open ADHD referrals by waiting band, England.
    One row per (date, band). Summed across age groups.
    """
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


# --- Formatters for display ---

def fmt_count(n) -> str:
    """562480 -> '562,480'."""
    if n is None:
        return "—"
    return f"{n:,}"


def fmt_count_short(n) -> str:
    """2759626 -> '2.76M', 562480 -> '562K'."""
    if n is None:
        return "—"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def fmt_pct(x, decimals: int = 0) -> str:
    """0.348 -> '35%'."""
    if x is None:
        return "—"
    return f"{x * 100:.{decimals}f}%"


def fmt_multiplier(x, decimals: int = 1) -> str:
    """5.77 -> '5.8x'."""
    if x is None:
        return "—"
    return f"{x:.{decimals}f}x"


def fmt_ratio(x) -> str:
    """8.57 -> '~9 : 1'."""
    if x is None:
        return "—"
    return f"~{round(x)} : 1"
