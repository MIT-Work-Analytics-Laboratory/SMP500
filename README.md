# Impact of AI on the S&P 500: Labor Market Impacts and Value Creation

**Prepared by Nicolò Piergiovanni Bagnoli**
**MIT Work Analytics Laboratory**
**Published: March 2026**

Acknowledgements: Yossi Sheffi, Pierre Bouquet

---

## Overview

This repository estimates the exposure of S&P 500 companies and their workforce to AI automation. It combines:

- **Eloundou et al. (2023)** rubric-based task exposure labels (E0–E3), updated with a 2026 agentic AI classification rubric via Gemini on Vertex AI
- **Anthropic Economic Index** observed Claude usage data to measure real-world AI task penetration
- **Revelio Labs** employee-level workforce microdata (via WRDS) with demographic, salary, seniority, and occupation detail
- **O\*NET** task inventories and **BLS** employment projections

The analysis produces occupation-level and company-level AI exposure scores, wage-value-at-risk estimates under multiple automation scenarios, and publication-ready figures.

## Repository Structure

### Notebooks — Pipeline Order

| # | Notebook | Purpose |
|---|----------|---------|
| 0 | `0 - sp500_Descriptive_Statistics.ipynb` | Weighted descriptive statistics of the S&P 500 workforce (demographics, salary, geography, remote work) |
| 0.4 | `0.4 - Exposure_Classification_Pipeline_batch.ipynb` | Batch classification of O\*NET tasks into E0–E3 exposure categories using Gemini on Vertex AI |
| 0.5 | `0.5 - Scores_comparison_and_occ_Classification.ipynb` | Rebuild Eloundou exposure scores (alpha, beta, gamma) from new task labels; compare old vs. new |
| 0.6 | `0.6 - Task_time_and_time_savings.ipynb` | Estimate weekly hours per O\*NET task using Gemini; produce normalized task-time distributions |
| 0.7 | `0.7 - Time correlations.ipynb` | Validate task-time estimates against the O\*NET-derived pi distribution |
| 0.8 | `0.8 - Penetration.ipynb` | Build task-level AI penetration scores from Anthropic usage data |
| 0.9 | `0.9 - New_occ_exposure.ipynb` | Recompute occupation-level scores (`time_based_score`, `observed_penetration_score`) and write to `occ_level_new.csv` |
| 1 | `1 - sp500_new_scores_task_analysis copy.ipynb` | Task-level wage exposure analysis: E0/E1/E2–E3 wage mass, automation scenarios (25/35/45%), and observed AI usage (81% efficiency gain) |
| 1.1 | `1.1 - sp500_new_scores_occ_analysis.ipynb` | Occupation- and company-level AI exposure rankings with demographic breakdowns, sector analysis, and WLS scatter plots |
| 1.2 | `1.2 - Figures_Anthropic.ipynb` | Publication-ready figures: radar chart, BLS scatter plots, Claude usage histograms |

### Data Notebooks

| Notebook | Purpose |
|----------|---------|
| `data/sp500.ipynb` | Obtain S&P 500 ticker list and Revelio Labs RCID identifiers |
| `data/get_compnay_info.ipynb` | Download employee-level position data from WRDS/Revelio (uses `ultimate_parent_rcid` for subsidiary inclusion) |

### Key Data Files

| File | Description |
|------|-------------|
| `data/sp500_company_data.parquet` | Employee-level S&P 500 workforce data with salary, occupation, demographics, and sampling `weight` |
| `data/job_task_time_distribution_30_0.csv` | Task-time shares (pi) per occupation × task |
| `data/Employment Projections.csv` | BLS employment projections 2024–2034 |
| `Eloundou_New/full_labelset_new.tsv` | Task-level exposure labels and scores (updated rubric) |
| `Eloundou_New/occ_level_new.csv` | Occupation-level exposure scores |
| `Anthropic/task_penetration.csv` | Task-level AI penetration from Anthropic Claude usage |
| `Anthropic/aei_raw_*.csv` | Raw Anthropic Economic Index usage data (Claude AI and 1P API, Aug/Nov 2025) |

### Output Directories

| Directory | Contents |
|-----------|----------|
| `Report images/` | Publication-ready PNGs with transparent backgrounds |
| `output/company_overview/` | Descriptive statistics charts |
| `Anthropic/` | Intermediate analysis figures |

## Key Metrics

- **`time_based_score`** — Rubric-based AI exposure: pi-weighted average of task-level `beta_new` scores. Occupations with > 5 missing pi values are excluded.
- **`observed_penetration_score`** — Observed AI exposure: pi-weighted average of `penetration_beta_new` from Anthropic Claude usage data.
- **`dv_rating_new`** — Equal-weight (unweighted) average of `beta_new` across an occupation's tasks.

## Weighting

All analyses use the `weight` column from the employee-level parquet file. Employee counts, demographic shares, salary averages, and exposure aggregations are computed as weighted sums or weighted means throughout. This ensures that sampling corrections from Revelio Labs are respected at every level of analysis.

## Data Access

The `data/` directory is gitignored. The employee-level parquet file is constructed from WRDS/Revelio Labs data and requires institutional access. The Anthropic AEI raw files are sourced from the Anthropic Economic Index. Contact the MIT Work Analytics Laboratory for data access.

## Requirements

The notebooks use the following Python packages:

- `pandas`, `numpy` — data manipulation
- `matplotlib` — visualization
- `pyarrow` — parquet I/O
- `statsmodels` — weighted least squares regression
- `scipy` — statistical tests
- `google-cloud-aiplatform`, `vertexai` — Gemini API (notebook 0.4 and 0.6 only)
- `wrds` — WRDS database access (data notebooks only)
- `plotly` — interactive maps (notebook 0 only)

## License

This project is part of research conducted at the MIT Work Analytics Laboratory. See institutional policies for usage terms.
