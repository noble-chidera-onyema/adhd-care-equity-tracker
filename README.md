# ADHD Care Equity Tracker UK

> ⚠️ **Educational research artefact — not a clinical tool.**

An open analysis of inequity in UK ADHD diagnostic services, and a
forecast of where unmet need is projected to grow worst by 2029.

**Author:** Noble Chidera Onyema · MSc Applied AI, Abertay University
**Live dashboard:** _coming Week 3_
**Walkthrough video:** _coming Week 3_

---

## The problem

ADHD diagnostic services in the UK are in crisis. Adult assessment
waiting lists exceed five years in many NHS Trusts, child waits run two
to three years in some regions, and the wait time someone faces depends
heavily on their postcode — patients in some areas wait several times
longer than patients elsewhere for the same service. Demand has grown
roughly fourfold over the past decade while assessment capacity has
barely moved.

This project consolidates the publicly available data into a single
dashboard and trains a forecast model to identify where the gap between
need and capacity will widen most over the next three years.

## What's inside

- **SQL pipeline** harmonising NHS England MHSDS, Public Health Scotland
  CAMHS, and ONS census data using DuckDB.
- **Random Forest model** predicting waiting time by region and
  demographic factors, validated with k-fold cross-validation.
- **Prophet time-series forecast** of regional wait times, 2026–2029.
- **Equity index** combining wait time, population, and deprivation by
  region.
- **Streamlit dashboard** with an interactive UK map, region picker,
  forecast view, and a patient persona simulator.

## Data sources

All data used is aggregate and publicly published. No individual patient
data appears anywhere in this project. Full provenance lives in
[`docs/data_sources.md`](docs/data_sources.md).

- NHS England — Mental Health Services Monthly Statistics (MHSDS)
- NHS England — Mental Health Bulletin (annual)
- Public Health Scotland — CAMHS Waiting Times
- Public Health Scotland — Psychological Therapies Waiting Times
- ADHD UK — patient-reported waiting time data
- Office for National Statistics — Census 2021 by region

## Tech stack

Python 3.11 · pandas · DuckDB · scikit-learn · Prophet · Streamlit ·
Plotly · Folium

## Project structure

```
adhd-care-equity-tracker/
├── data/               raw · processed · geo
├── notebooks/          01_ingestion → 05_forecasting
├── src/                data_pipeline · features · model · forecast
├── app/                streamlit_app.py + components
├── docs/               methodology · data_sources · screenshots
├── tests/
├── LICENSE             All Rights Reserved
├── README.md
└── requirements.txt
```

## How to run locally

_Filled in once the pipeline exists (Week 1, Day 4)._

## Findings

_Populated at the end of Week 1 EDA._

## Model performance

_Populated at the end of Week 2._

## Limitations

- Data is reported by NHS bodies and may have completeness gaps,
  particularly for ADHD-specific codes within broader mental health
  datasets.
- Forecasts are illustrative, not deterministic. They assume current
  capacity and referral patterns continue without major policy
  intervention.
- Results are aggregate. They **must not** be used in individual
  clinical decisions.
- The dashboard is an educational research artefact, not a clinical
  tool.

## Ethics

All data used is aggregate and publicly published by NHS bodies, Public
Health Scotland, and the Office for National Statistics. No individual
patient data appears anywhere in this project. Findings present
comparative information about services; they make no clinical claims
about any individual.

## Licence

**All Rights Reserved.** See [`LICENSE`](LICENSE). No commercial use,
derivative works, redistribution, or use as ML training data is
permitted without written permission.

---

© 2026 Noble Chidera Onyema · onyemanoble1628@gmail.com
