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
| `notebooks/01_ingestion.ipynb` | NHS England MHSDS time series (April 2016 to February 2026) | Complete |
| `notebooks/02_mi_adhd_ingestion.ipynb` | NHS England ADHD Management Information (February 2026 release) | Complete; validated to the unit against 562,480 |
| `notebooks/03_mi_adhd_eda.ipynb` | MI-ADHD initial analysis, seven analytical charts | Complete |
| `notebooks/04_uk_neurodev_consolidation.ipynb` | Children's Commissioner ND waiting times report (October 2024) | Complete; eleven tables extracted, demographic equity finding surfaced |
| `notebooks/05_opensafely_and_commons_library.ipynb` | OpenSAFELY ADHD diagnosis and prescribing analysis (9-year series) + House of Commons Library briefing CBP-10551 | Complete; one prevalence trend chart |
| `notebooks/06_harmonisation_duckdb.ipynb` | DuckDB join across all four data sources | Complete; 9,909-row fact table; validated to the unit |

## What's planned

| Component | Reason |
|---|---|
| `app/streamlit_app.py` | Interactive viewer over the harmonised fact table. Five views: Overview, Waiting Times, Demographics, Trends, Methodology. |
| Deployment to Streamlit Community Cloud | Public access without local Python setup. |

## Scope decisions worth flagging

- **Notebook 04 was originally scoped as ADHD UK patient survey ingestion.** Replaced with the Children's Commissioner October 2024 report — a statutory body's analysis joining MHSDS with CSDS, containing the geographic and demographic breakdowns that MI-ADHD does not publish. ADHD UK is a campaigning charity; their published material is narrative rather than structured.
- **Notebook 05 was originally scoped as Right to Choose provider data scraping.** Replaced with OpenSAFELY's 9-year analysis of ADHD diagnosis and prescribing rates published alongside MI-ADHD, plus transcribed headline figures from House of Commons Library briefing CBP-10551. OpenSAFELY's series is longer, cleaner, and more authoritative than scraped provider pages.
- **Notebook 07 (forecasting) was dropped from scope.** MI-ADHD's 13-month activity series is too short, and the 80% stock-flow reconciliation gap (see Notebook 03) too large, to support credible long-horizon projection. A short illustrative extrapolation with heavy caveats was considered and rejected: dressing noisy data in modelling polish would weaken the project, not strengthen it.

## Headline findings

All figures drawn from the source datasets listed above. Chart numbers refer to PNGs in `docs/screenshots/`.

- **The open ADHD referral list in England grew from ~366,000 to ~562,000 over 12 months**, a 53% increase. ([Chart 1](docs/screenshots/chart_01_open_referrals_by_band.png))
- **The 104+ weeks waiting band grew fastest** in both absolute terms and as a share of the total. By December 2025 it represented around 35% of the open list, up from 29% twelve months earlier. ([Chart 2](docs/screenshots/chart_02_share_by_band.png))
- **Adults aged 25+ are 52% of the open list.** ADHD is no longer accurately described as a primarily childhood condition. ([Chart 3](docs/screenshots/chart_03_open_referrals_by_age.png))
- **22.8% of records have unknown or unstated ethnicity** in MI-ADHD, setting a ceiling on per-capita disparity analysis. ([Chart 4](docs/screenshots/chart_04_open_referrals_by_ethnicity.png))
- **Inflow exceeds outflow in 11 of 13 months**, but published net flow accounts for only ~20% of the actual monthly change in the open list. The remaining ~80% (about 163,000 referrals over the period) is unexplained by published flow indicators. ([Chart 5](docs/screenshots/chart_05_inflow_outflow.png), [Chart 6](docs/screenshots/chart_06_stock_vs_flow_reconciliation.png))
- **Roughly 1.9 million people in England may have ADHD but are not on the open referral list at all.** ([Chart 7](docs/screenshots/chart_07_prevalence_vs_referrals.png))
- **The full UK ADHD waiting list is closer to 2.76 million.** MI-ADHD's published 562,480 captures only the Mental Health Services Dataset slice; Community Health Services SitRep adds another 2,197,176 children and young people, per House of Commons Library briefing CBP-10551 (December 2025 data).
- **Asian children are under-represented in ADHD referrals by roughly 8:1 relative to population share.** 1.4% of ADHD referrals are Asian or Asian British (Children's Commissioner October 2024 report, p108) vs ~12% of the child population per Census 2021. The under-representation is sharpest for Asian children but present across most non-White groups.
- **Recorded ADHD diagnosis rates in GP records have roughly tripled in nine years.** Female rate grew 5.8x (0.16% to 0.92%), male rate 2.3x (0.69% to 1.63%) between 2016/17 and 2024/25. Female rate in 2024/25 is approaching where the male rate sat in 2016/17. ([Chart 8](docs/screenshots/chart_08_opensafely_prevalence_trend.png))
- **Median wait from ADHD diagnosis to first medication prescription for ages 10–17 doubled** from 18 weeks (2016/17) to 36 weeks (2024/25), per OpenSAFELY analysis.

## Method notes

- **Load validated against the official figure.** The December 2025 open referral total computed from `data/processed/mi_adhd_feb2026.parquet` reproduces NHS England's published 562,480 exactly. See `notebooks/02_mi_adhd_ingestion.ipynb`.
- **Harmonised fact table reproduces every source's headline figure to the unit.** The DuckDB-built `adhd_atlas_fact.parquet` reconstructs the 562,480 ADHD003 total, the OpenSAFELY 0.16%/0.92% female prevalence endpoints, and the Children's Commissioner ethnicity shares (sum to 100%). Validation queries in `notebooks/06_harmonisation_duckdb.ipynb`.
- **Stock-vs-flow reconciliation.** MI-ADHD's flow indicators (ADHD006 closed, ADHD007 new) explain only about 20% of the observed change in the stock indicator (ADHD003 open). The remaining 80% appears to be retrospective adjustments under MHSDS's multiple-submission window model, definitional overlap between indicators, or provider submission incompleteness. Documented in `notebooks/03_mi_adhd_eda.ipynb`, Chart 6.
- **Data quality flags surfaced and handled.** Mixed date formats in the same column (UK `DD/MM/YYYY` and ISO `YYYY-MM-DD`), `*` suppression for small-count cells (240 cells in the MI-ADHD February 2026 release), a 10-row discrepancy between age-group and ethnicity sums of the same indicator at the same month, and messy multi-row PDF table headers in the Children's Commissioner report.

## Limitations

- MI-ADHD publishes national-level data only. There is no regional, ICB, or Sub-ICB breakdown. The Children's Commissioner report partly fills the demographic dimensions but not the geographic one.
- The 13-month MI-ADHD activity time series is too short for meaningful long-horizon forecasting. The 9-year OpenSAFELY series covers diagnosis and prescribing, not the waiting list.
- ADHD waiting time data is fragmented across UK jurisdictions. Scotland's neurodevelopmental waits are not routinely published; Wales and Northern Ireland data is not covered in this iteration.
- 22.8% of MI-ADHD records have unknown or unstated ethnicity. Per-capita disparity analysis from MI-ADHD alone is bounded by this missingness.
- OpenSAFELY covers ~44% of England's GP-registered population (those using the TPP system); the other 56% (predominantly EMIS) is not in this analysis.
- The Children's Commissioner report draws on data through 2023/24. Not as current as MI-ADHD.
- This is an educational research artefact built as part of an MSc Applied AI portfolio. It is not a clinical tool, not a peer-reviewed analysis, and not a substitute for official NHS statistics.

## Data sources

All data used is aggregate and publicly published. No individual patient data appears anywhere in this project.

| Source | Used in | Source licence |
|---|---|---|
| NHS England Mental Health Services Monthly Statistics (MHSDS) | Notebook 01 | Open Government Licence v3.0 |
| NHS England ADHD Management Information (MI-ADHD, Feb 2026 release) | Notebooks 02, 03 | Open Government Licence v3.0 |
| Children's Commissioner for England, "Waiting times for assessment and support for autism, ADHD and other neurodevelopmental conditions" (October 2024) | Notebook 04 | Crown Copyright; quoted under fair dealing for research |
| OpenSAFELY ADHD analysis (NHS Digital, November 2025 release) | Notebook 05 | Open Government Licence v3.0 |
| House of Commons Library briefing CBP-10551 | Notebook 05 | Open Parliament Licence v3.0 |

## Tech stack

Python 3.11 · pandas · DuckDB · scikit-learn · Plotly · pdfplumber · Streamlit · JupyterLab

## How to reproduce

```bash
git clone https://github.com/noble-chidera-onyema/adhd-care-equity-tracker.git
cd adhd-care-equity-tracker
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Open the notebooks in numerical order. Notebooks 01 to 05 download their source data from NHS England and other publishers on first run. Notebook 06 reads the processed outputs of 02, 04, and 05.

## Project structure

```
adhd-care-equity-tracker/
├── data/               raw, processed (gitignored contents)
├── notebooks/          six complete notebooks (01 to 06)
├── src/                shared pipeline modules
├── app/                Streamlit dashboard (in progress)
├── docs/               screenshots and source-of-truth chart PNGs
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
