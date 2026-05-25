# Annex — Study Limitations

The following is a non-exhaustive list of caveats relevant to the analyses in notebooks `1 - sp500_new_scores_task_analysis`, `1.1 - sp500_new_scores_occ_analysis`, and `1.2.1 - Figures_Anthropic_new`. They are meant for transparency in the report and do not, in our view, undermine the qualitative findings.

## 1. Sample and coverage

- **S&P 500 only.** All workforce statistics refer to publicly listed large-cap U.S. firms in the S&P 500 index. Small and medium enterprises, public-sector employers, education, public administration, and management-of-companies sectors are essentially absent. Three of the twenty NAICS sectors are not represented at all in the dataset.
- **Single snapshot.** The employee table is a stock of currently held positions, not a time series. End-dates are missing for 100 % of rows, so we cannot track entries, exits, or tenure dynamics.
- **U.S.-centric geography.** Roughly 55 % of weighted employees are matched to U.S. cities; non-U.S. employees are included in counts but not in the geographic visualizations.

## 2. Data quality of the workforce panel

- **Predicted demographics.** Gender and ethnicity are inferred from name and profile signals rather than self-reported. They are useful for aggregate comparisons but should be read as proxies, especially for ethnicity.
- **Imputed and estimated salaries.** Wages are model-estimated, not actual payroll. Where salaries are missing we impute the weighted occupation-level median, which compresses within-occupation variance.
- **Missing education.** The `highest_degree` field is missing for roughly 47 % of rows. Education statistics (e.g. share with a Bachelor's degree or above) are conditional on the half of the sample for which education is observed.
- **Population weights, not survey weights.** The `weight` column rescales rows to a population total but is not a probabilistic sampling weight, so it does not support design-based standard errors.

## 3. Occupation and task mapping

- **O*NET coverage gaps.** About 9 % of employee rows carry O*NET-SOC codes (mostly residual "All other …" codes, military codes, or status flags such as *Retired*) that have no entry in our task-rating reference, and are therefore dropped from task- and occupation-level analyses.
- **Renormalised task-time mix.** Within each occupation, task-time shares (π) are renormalised to sum to one across the labelled tasks. This implicitly assumes that unlabelled tasks have the same exposure profile as labelled ones.
- **Wage mass attribution.** Roughly 86 % of total S&P 500 wage mass is retained in the matched occupation × task grid; the remaining 14 % is excluded from the dollar-value tables.
- **Aggregation drift.** Numbers move from task → occupation → company → sector through several joins. Each step introduces small composition effects that accumulate at the sector level.

## 4. AI exposure measures

- **Two non-equivalent measures.** The "potential" score (Gemini / Eloundou-style rubric) and the "observed" score (Anthropic Claude penetration) are conceptually different — capability vs. realised use — and are not directly comparable in level. Most figures show them side by side rather than combining them.
- **Vintage of the rubric.** The Eloundou-style exposure labels were produced for an earlier generation of language models. Capability frontiers have moved since, so the rubric is best read as an ordinal indicator rather than a current capability map.
- **Anthropic data is Claude-specific.** The penetration figures reflect what users of Claude do, not the universe of AI use across all tools and providers. Tasks performed with other models, with embedded copilots, or outside chat interfaces are not visible.
- **Task matching across sources.** The Anthropic task list and the Eloundou task list are merged on text. We normalise whitespace and de-duplicate, but residual mismatches mean the merged set is slightly smaller than either source alone.
- **Pooling across snapshot windows.** Plot 2 of notebook 1.2.1 pools Claude usage across three release windows (Aug 2025, Nov 2025, Feb 2026). Pooling treats the three vintages as exchangeable; if the user mix or task distribution shifted across releases, the pooled shares blur that.

## 5. Methodological assumptions

- **Flat automation rates are illustrative.** The 40 % / 50 % / 60 % scenarios applied to the E1 + E2/E3 wage mass are stylised reference points, not forecasts. They quantify what the wage mass would be if a given share of exposed work were automated, holding everything else fixed.
- **Penetration as an efficiency proxy.** In notebook 1, observed penetration is treated as a per-task efficiency coefficient (savings = task value × penetration). This is an interpretive choice; penetration is empirically a usage share, not a measured productivity gain or labour-cost saving.
- **"Exposed" ≠ "automatable" ≠ "lost".** Exposure scores measure feasibility of AI assistance for a task. They do not distinguish between augmentation, partial substitution, and full automation, and they do not predict net employment outcomes.
- **Linear regressions with low explanatory power.** The salary-vs-exposure WLS fits in notebook 1.1 carry low R² (≈ 0.07 for observed penetration, ≈ 0.28 for potential exposure). Slopes are informative about direction and order of magnitude, not about deterministic relationships.
- **Modal NAICS per company.** Each company is assigned its single most-frequent NAICS 2-digit code. Diversified conglomerates therefore look like single-sector firms.

## 6. External comparisons

- **BLS projections are forward-looking on a different horizon.** The scatter plots against BLS employment-change projections compare a current cross-section of AI exposure to BLS's 2024–2034 projected change. Causality cannot be inferred — high-exposure occupations are not necessarily the ones BLS expects to shrink because of AI.
- **Cross-source unit consistency.** Eloundou betas, Anthropic penetration, BLS projections, and Revelio-derived headcounts come from different vintages and methodologies. We harmonise on O*NET-SOC codes (sometimes truncated to SOC-6) but residual incomparability remains.

## 7. Interpretation

- **Population vs. people.** Counts labelled `n_employees` are sums of weights over employee-position records, not unique individuals. The same person can contribute to multiple positions.
- **Salary disparities by exposure.** Differences in average salary across exposure quantiles partly reflect the underlying mix of industries, occupations, and seniority — not only AI exposure itself. The report should not read those gradients as causal.
- **The dollar figures are upper-bound proxies.** The "exposed wage mass" is the share of total S&P 500 wage mass attached to tasks deemed exposed. It is a labour-cost denominator, not a forecast of value at risk.

## 8. Reproducibility caveats

- **Pinned to local file paths.** Notebooks read inputs from absolute project paths. They are reproducible inside the project but not on a clean checkout without the same `data/`, `Eloundou_New/`, and `Anthropic/` folders.
- **No bootstrap or sensitivity analysis is reported in the figures.** Point estimates are shown without confidence bands; conclusions should be treated as descriptive rather than inferential.

---

These limitations should be read together: most of them are inherited from the underlying public datasets (Revelio, O*NET-SOC, Eloundou et al., Anthropic Economic Index, BLS) rather than introduced by our pipeline. Where the limitation materially changes the headline numbers, we have flagged it in-text alongside the relevant figure.
