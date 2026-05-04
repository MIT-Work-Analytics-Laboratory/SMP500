# Prompt — Generate an Annex / Appendix on the S&P 500 Workforce Dataset

You are a research assistant helping to draft a methodological annex (appendix) for an academic / policy report on AI exposure of the U.S. workforce. The annex must describe, in formal but readable prose, the **S&P 500 employee-level dataset** that underpins the analysis. Use the structured information below as the single source of truth. Do **not** invent additional facts. If a quantity is missing, say so explicitly.

---

## 1. Output specification

- **Form**: an annex titled `Annex A — The S&P 500 Workforce Dataset` (markdown, with section headers).
- **Length**: ~1,000–1,400 words.
- **Tone**: academic, neutral, third person; concise but precise.
- **Required subsections** (in this order):
  1. *Source & scope* — what the data represents and where it comes from.
  2. *Unit of observation & weighting scheme* — what each row is, how the `weight` column is used.
  3. *Variables* — list of columns with brief description of each.
  4. *Coverage of the S&P 500 universe* — companies, tickers, sectors covered vs missing.
  5. *Workforce demographics* — gender, ethnicity, education (all weighted).
  6. *Occupational structure* — O*NET mapping, top occupations, mapping completeness.
  7. *Geography* — country/city distribution, US-matching rate.
  8. *Compensation* — salary distribution.
  9. *Industry / NAICS coverage* — sector distribution.
  10. *Limitations & caveats* — missingness, coverage gaps, weighting interpretation.
- **Tables**: include 2–4 small markdown tables (demographics, top occupations, sector distribution). Round percentages to one decimal. Use thousands separators.
- **No emojis**; do **not** mimic the bullet symbols (📊, ⚠️) used in the source notebook.
- Cite numeric facts inline (no footnotes), e.g. "(weighted N = 26,866,152)".

---

## 2. Source notebook

The dataset is described and summarised in `0 - sp500_Descriptive_Statistics.ipynb`. The annex must reflect what *that notebook computes*, not external sources.

Underlying parquet files referenced by the notebook:
- `data/sp500_company_data.parquet` — main employee-position table.
- `data/dwa_times_normalized.parquet` — O*NET reference (used to map `O*NET-SOC Code` → occupation `Title`).
- `data/simplemaps_worldcities_basicv1.901.zip` — city → (lat, lng) reference (used for US geocoding).

---

## 3. Dataset facts (authoritative numbers)

### 3.1 Headline counts

| Metric | Value |
|---|---|
| Companies (unique tickers) | 473 |
| Total employee-position rows | 23,244,615 |
| Weighted employee total | 26,866,152 |
| Unique employees (`user_id`) | 21,626,407 |
| Average positions per user | 1.07 |
| Unique occupations (`onet_code`) in employee data | 1,010 |
| O*NET codes available in reference (`dwa_times_normalized`) | 923 unique titles (~1,016 codes) |
| O*NET codes in employee data **not** in reference | 93 (excluded from position analysis — no task-rating data) |

### 3.2 Unit of observation & weighting

- Each **row** is one *employee–position record*. A single `user_id` may appear in multiple rows (job changes, multiple roles).
- All statistics use the `weight` column (Revelio-style population scaling). Missing weights are filled with 1.0.
- "n_employees" throughout the notebook therefore refers to **weighted position-records**, not unique individuals.

### 3.3 Columns / variables

The dataset has 16 base columns + 1 derived (`onets_title`). Types are `Float64`, `Int64`, `string[python]`, `object`.

| Column | Type | Description |
|---|---|---|
| `user_id` | Float64 | Person identifier (Revelio profile id). |
| `position_id` | Float64 | Unique job-spell id per `user_id`. |
| `rcid` | float64 | Revelio company id. |
| `seniority` | Int64 | Ordinal seniority level (1–7 typical). |
| `country` | string | Country of the position. |
| `salary` | Float64 | Estimated annual salary, USD. |
| `onet_code` | string | O*NET-SOC occupation code. |
| `startdate` | string | Position start date (YYYY-MM-DD). |
| `enddate` | string | Position end date. **100% missing in the snapshot.** |
| `weight` | Float64 | Population weight. |
| `highest_degree` | string | Highest completed degree (Bachelor / Master / MBA / Doctor / Associate / High School). |
| `sex_predicted` | string | Predicted gender ("M", "F", or "." placeholder). |
| `ethnicity_predicted` | string | Predicted ethnicity (White, API, Hispanic, Black, Multiple, Native). |
| `ticker` | string | Stock ticker of the employer. |
| `naics_code` | string | NAICS code (6-digit) of the employer. |
| `company` | string | Company name. |
| `onets_title` (derived) | object | O*NET title joined from reference data. |

### 3.4 Missing values (top columns, %)

| Column | Missing count | Missing % |
|---|---|---|
| `enddate` | 23,244,615 | 100.00 |
| `highest_degree` | 10,852,691 | 46.69 |
| `startdate` | 4,541,995 | 19.54 |
| `onets_title` | 2,151,535 | 9.26 |
| `country` | 330,136 | 1.42 |
| `onet_code` | 10,767 | 0.05 |
| `ethnicity_predicted` | 4,853 | 0.02 |
| `salary` | 3,624 | 0.02 |

### 3.5 O*NET mapping completeness

- Successfully mapped to an O*NET title: **21,093,080 / 23,244,615 rows (90.7 %)**.
- 93 O*NET codes in employee data have no corresponding reference row (mostly "All other …" residual codes such as `11-9039.00`, `13-1199.00`, plus military codes `55-…`, and labels like `On Leave`, `Retired`, `unknown`). These rows are excluded from position-level analyses.

### 3.6 Demographics (weighted)

**Gender** (excluding "." placeholder):

| Gender | Weighted count | Share |
|---|---|---|
| Male | 16,292,131 | 61.2 % |
| Female | 10,352,542 | 38.9 % |

**Ethnicity** (`ethnicity_predicted`):

| Group | Weighted count | Share |
|---|---|---|
| White | 14,748,715 | 54.9 % |
| API (Asian / Pacific Islander) | 6,809,620 | 25.4 % |
| Hispanic | 3,031,346 | 11.3 % |
| Black | 2,097,674 | 7.8 % |
| Multiple | 153,002 | 0.6 % |
| Native | 20,399 | 0.1 % |

**Education** (`highest_degree`, conditional on non-missing — coverage ≈ 53 %):

| Degree | Weighted count | Share of non-missing |
|---|---|---|
| Bachelor | 7,658,310 | 54.0 % |
| Master | 3,175,245 | 22.4 % |
| MBA | 1,539,461 | 10.9 % |
| Associate | 731,033 | 5.2 % |
| High School | 541,933 | 3.8 % |
| Doctor | 536,872 | 3.8 % |

% with Bachelor's or above (weighted, non-missing): **91.0 %**.

### 3.7 Compensation (weighted, USD)

- Mean salary: **$70,882**
- Median: **$51,583**
- Std. dev.: **$61,399**
- 25th percentile: **$27,481**
- 75th percentile: **$98,331**
- Min / Max: **$0 / $2,327,948**
- Salary observations: **26,862,112** weighted (≈ 99.98 % of total weighted N).

### 3.8 Average seniority (weighted)

- Mean ordinal seniority: **2.59**.

### 3.9 Top occupations (weighted, top 10 of 20 reported)

| # | O*NET title | Weighted count | Share of mapped |
|---|---|---|---|
| 1 | Software Developers | 1,480,407 | 6.1 % |
| 2 | Information Technology Project Managers | 717,751 | 3.0 % |
| 3 | Sales Representatives, Wholesale & Manufacturing | 659,936 | 2.7 % |
| 4 | Computer Systems Engineers / Architects | 584,220 | 2.4 % |
| 5 | Sales Managers | 559,778 | 2.3 % |
| 6 | Business Intelligence Analysts | 539,746 | 2.2 % |
| 7 | Marketing Managers | 532,220 | 2.2 % |
| 8 | Customer Service Representatives | 524,255 | 2.2 % |
| 9 | Treasurers and Controllers | 427,307 | 1.8 % |
| 10 | Retail Salespersons | 381,232 | 1.6 % |

### 3.10 Geography

- World cities reference (`simplemaps`): 48,059 cities loaded.
- US cities post-deduplication (largest population kept per ambiguous name): **5,344 → 4,361**.
- US-matched workforce: **14,748,715 / 26,866,152 weighted (54.9 %)**. The remainder is non-US or city name mismatches.
- The map is restricted to the United States; international employees are reported but not geocoded for the choropleth.

### 3.11 Industry / NAICS coverage (sector = NAICS 2-digit, modal sector per company)

- Sector taxonomy: 20 standard 2-digit-derived labels.
- Sectors **present**: 17 / 20.
- Sectors **missing** from the S&P 500 sample: **Education**, **Mgmt of Companies**, **Public Admin**.

| Sector | Companies | Weighted employees | Share |
|---|---|---|---|
| Manufacturing | 170 | 7,817,695 | 29.1 % |
| Finance & Insurance | 69 | 4,869,353 | 18.1 % |
| Information & Tech | 51 | 3,889,352 | 14.5 % |
| Retail Trade | 23 | 3,291,508 | 12.3 % |
| Professional Services | 12 | 1,766,452 | 6.6 % |
| Accommodation & Food | 11 | 1,321,670 | 4.9 % |
| Transportation | 21 | 1,222,636 | 4.6 % |
| Mining & Oil/Gas | 18 | 656,760 | 2.4 % |
| Healthcare | 5 | 415,349 | 1.5 % |
| Real Estate | 32 | 392,189 | 1.5 % |
| Utilities | 31 | 389,005 | 1.4 % |
| Wholesale Trade | 9 | 292,310 | 1.1 % |
| Admin & Support | 9 | 229,525 | 0.9 % |
| Construction | 8 | 156,484 | 0.6 % |
| Agriculture | 2 | 76,481 | 0.3 % |
| Arts & Entertainment | 1 | 48,247 | 0.2 % |
| Other Services | 1 | 31,137 | 0.1 % |
| **TOTAL** | **473** | **26,866,152** | **100.0 %** |

### 3.12 Methodological helpers used in the notebook

The annex should mention that the notebook implements weighted analogues of the standard descriptive statistics, since simple unweighted counts would over-represent low-weight rows:

- `weighted_value_counts(df, col)` — sum of `weight` per category.
- `weighted_mean(df, col)` — `np.average(values, weights=weight)`.
- `weighted_percentile(df, col, p)` — cumulative-weight interpolation; handles empty input and `p ≥ 1`.
- `weighted_std(df, col)` — `sqrt(Σ w·(x − x̄)² / Σ w)`.
- `valid_sex_mask` — excludes both `NaN` and the `"."` placeholder before computing gender shares.

---

## 4. Limitations to mention explicitly

1. **Predicted demographics**: gender and ethnicity are model-inferred from names/profile signals, not self-reported. Treat ethnicity in particular as a noisy proxy.
2. **Education missingness** (≈ 47 %): the *Bachelor's-or-above* share of 91 % refers only to the half of rows where `highest_degree` is observed.
3. **Position-record vs person**: 23.2 M rows correspond to ~21.6 M unique users (1.07 positions/user). Aggregations that sum weights count *position-records*, not people.
4. **Snapshot timing**: `enddate` is 100 % missing — the table represents a stock of currently-held positions rather than a flow of past spells.
5. **O*NET mapping gaps**: 9.3 % of rows lack a mapped occupation title (mostly "All other …" residual SOC codes, military codes 55-xx, and status flags). These are dropped from occupation-level outputs.
6. **Sector coverage**: 3 of 20 NAICS sectors (Education, Mgmt of Companies, Public Admin) have no S&P 500 representation; results cannot speak to those segments.
7. **Geography**: only US cities are matched against the simplemaps reference; the 45 % of weighted employees with no US match are either non-US or have unresolvable city names.
8. **Weights**: weights scale 23.2 M rows up to 26.9 M weighted records (factor ≈ 1.16). They are population reweighting factors, not sampling probabilities, and do not produce design-based standard errors.

---

## 5. Style rules for the generated annex

- Use full sentences in the body; reserve tables for parts §3.6, §3.9, §3.11.
- Always specify "weighted" when reporting shares, mean, median, percentiles.
- Round percentages to **one decimal place**, weighted counts to whole numbers with thousands separators, salary figures to whole USD.
- Refer to the data source as "the S&P 500 employee-position panel" or "the S&P 500 workforce dataset". Do not call it a survey.
- When mentioning O*NET, write "O*NET-SOC".
- Do not introduce numbers that are not in §3 of this prompt.

---

## 6. Final instruction

Produce the annex now, in markdown, following the structure in §1 and using only the facts in §3. End with a one-paragraph "Limitations" subsection that paraphrases §4 (do not copy verbatim).
