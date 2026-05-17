# ADHD Care Equity Tracker UK

> ⚠️ Educational research artefact, not a clinical tool. Findings are aggregate and must not be used in individual clinical decisions.

A consolidation and analysis of publicly available UK ADHD waiting time data, with documented data quality limitations.

**Author:** Noble Chidera Onyema
**Project status:** in development, Week 1 of 3 (May 2026)
**Contact:** onyemanoble1628@gmail.com

---

## What this project is

ADHD waiting time data in the UK is fragmented across multiple sources, three jurisdictions, and two access mechanisms (routine publications and FOI requests). No single public dashboard consolidates them. This project does that consolidation, working primarily with NHS England's ADHD Management Information (MI-ADHD) publication, first released in May 2025 and scheduled to become official statistics in 2026/27.

## What's built so far

| Notebook | Source | Status |
|---|---|---|
| `notebooks/01_ingestion.ipynb` | NHS England MHSDS time series (broad mental health activity, April 2016 to February 2026) | Complete |
| `notebooks/02_mi_adhd_ingestion.ipynb` | NHS England ADHD Management Information (February 2026 release) | Complete; load validated to the unit against the official 562,480 figure |
| `notebooks/03_mi_adhd_eda.ipynb` | Initial exploratory analysis, seven charts | Complete |

## What's planned

| Notebook | Source | Reason |
|---|---|---|
| `notebooks/04_adhd_uk_survey.ipynb` | ADHD UK annual patient survey | Patient-reported waits to triangulate against NHS-reported figures |
| `notebooks/05_right_to_choose.ipynb` | Public Right-to-Choose provider wait-time pages | ICB-level geographic granularity that MI-ADHD does not publish |
| `notebooks/06_harmonisation.ipynb` | DuckDB join across all sources | Single consistent schema for downstream analysis |
| `notebooks/07_modelling.ipynb` | Six-month illustrative projection | Heavily caveated, not predictive forecasting |
| `app/streamlit_app.py` | Interactive viewer over the harmonised dataset | Final deliverable |

## Headline findings from MI-ADHD analysis

All findings drawn from the February 2026 MI-ADHD release, covering data through December 2025. Chart numbers refer to PNGs in `docs/screenshots/`.

- **The open ADHD referral list in England grew from ~366,000 to ~562,000 over 12 months**, a 53% increase. ([Chart 1](docs/screenshots/chart_01_open_referrals_by_band.png))
- **The 104+ weeks waiting band grew fastest** in both absolute terms and as a share of the total. By December 2025 it represented around 35% of the open list, up from 29% twelve months earlier. ([Chart 2](docs/screenshots/chart_02_share_by_band.png))
- **Adults aged 25+ are 52% of the open list.** ADHD is no longer accurately described as a primarily childhood condition. ([Chart 3](docs/screenshots/chart_03_open_referrals_by_age.png))
- **22.8% of records have unknown or unstated ethnicity**, setting a ceiling on per-capita disparity analysis until ONS census denominators are joined. ([Chart 4](docs/screenshots/chart_04_open_referrals_by_ethnicity.png))
- **Inflow exceeds outflow in 11 of 13 months**, but published net flow accounts for only ~20% of the actual monthly change in the open list. The remaining ~80% (about 163,000 referrals over the 13-month period) is unexplained by the published flow indicators. ([Chart 5](docs/screenshots/chart_05_inflow_outflow.png), [Chart 6](docs/screenshots/chart_06_stock_vs_flow_reconciliation.png))
- **Roughly 1.9 million people in England may have ADHD but are not on the open referral list at all.** Some are diagnosed and stable on medication; some use private routes; most are undiagnosed and unreferred. ([Chart 7](docs/screenshots/chart_07_prevalence_vs_referrals.png))

## Method notes

- **Load validated against the official figure.** The December 2025 open referral total computed from `data/processed/mi_adhd_feb2026.parquet` reproduces NHS England's published headline of 562,480 exactly. See `notebooks/02_mi_adhd_ingestion.ipynb`.
- **Stock-vs-flow reconciliation.** MI-ADHD's flow indicators (ADHD006 closed, ADHD007 new) explain only about 20% of the observed change in the stock indicator (ADHD003 open). The remaining 80% appears to be retrospective adjustments under MHSDS's multiple-submission window model, definitional overlap between indicators, or provider submission incompleteness. Anyone using MI-ADHD for forecasting needs to model this explicitly. See `notebooks/03_mi_adhd_eda.ipynb`, Chart 6.
- **Data quality flags surfaced and handled.** Mixed date formats in the same column (UK `DD/MM/YYYY` and ISO `YYYY-MM-DD`), `*` suppression for small-count cells (240 cells in the February 2026 release), and a 10-row discrepancy between age-group and ethnicity sums of the same indicator at the same month. Documented in Notebooks 02 and 03.

## Limitations

- MI-ADHD publishes national-level data only. There is no regional, ICB, or Sub-ICB breakdown. Geographic inequity analysis requires joining separate sources, planned in Notebooks 05 and 06.
- The 13-month time series (December 2024 onward) is too short for meaningful long-horizon forecasting. Any projection work in Notebook 07 will be illustrative, not predictive.
- ADHD waiting time data is fragmented across UK jurisdictions. Scotland's neurodevelopmental waits are not routinely published; Wales and Northern Ireland data is not covered in this iteration.
- 22.8% of MI-ADHD records have unknown or unstated ethnicity. Per-capita disparity analysis is bounded by this missingness.
- This is an educational research artefact built as part of an MSc Applied AI portfolio. It is not a clinical tool, not a peer-reviewed analysis, and not a substitute for official NHS statistics.

## Data sources

All data used is aggregate and publicly published. No individual patient data appears anywhere in this project.

| Source | Used in | Source licence |
|---|---|---|
| NHS England Mental Health Services Monthly Statistics (MHSDS) | Notebook 01 | Open Government Licence v3.0 |
| NHS England ADHD Management Information (MI-ADHD) | Notebooks 02, 03 | Open Government Licence v3.0 |
| ADHD UK patient survey *(planned)* | Notebook 04 | Per ADHD UK terms |
| Right-to-Choose provider public pages *(planned)* | Notebook 05 | Public web pages |
| ONS Census 2021 ethnic-group population *(planned)* | Notebook 06 | Open Government Licence v3.0 |

## Tech stack

Python 3.11 · pandas · DuckDB · scikit-learn · Plotly · Streamlit · JupyterLab

## How to reproduce

```bash
git clone https://github.com/noble-chidera-onyema/adhd-care-equity-tracker.git
cd adhd-care-equity-tracker
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Open the notebooks in numerical order. Notebooks 01 to 03 are self-contained and will download their source data from NHS England on first run.

## Project structure

```
adhd-care-equity-tracker/
├── data/               raw, processed, geo (gitignored contents)
├── notebooks/          01 to 03 complete; 04 to 07 planned
├── src/                shared pipeline modules
├── app/                Streamlit dashboard (Week 3)
├── docs/               methodology, data_sources, screenshots
├── tests/
├── LICENSE             All Rights Reserved
├── NOTICE.md           plain-English IP notice
├── README.md
└── requirements.txt
```

## Licence

**All Rights Reserved.** See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). No commercial use, derivative works, redistribution, or use as machine learning training data is permitted without written permission.

---

© 2026 Noble Chidera Onyema · onyemanoble1628@gmail.com
