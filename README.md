Ethiopia Financial Inclusion Forecasting – Capstone Project
Project Overview

This capstone project focuses on analyzing and forecasting financial inclusion in Ethiopia, leveraging the Global Findex Database 2025 along with supplementary regional and gender-disaggregated data. The project aims to provide actionable insights for policymakers, financial institutions, and stakeholders to improve account ownership, mobile money adoption, and overall digital payment usage across the country.

Objectives

Assess historical trends in financial inclusion metrics: account ownership, formal accounts, and mobile money adoption.

Identify gaps in the dataset, including temporal, regional, and gender-specific data gaps.

Enrich data with event impacts (e.g., Telebirr launch) to analyze adoption drivers.

Develop forecasts for financial inclusion indicators (2025–2027) under baseline and scenario assumptions.

Create an interactive dashboard to visualize trends, forecast projections, and scenario comparisons.

Success Metrics

The success of this project is evaluated against the following indicators:

Account Ownership (Access): Projected growth to ~68–70% by 2027.

Digital Payment Usage (Mobile Money): Upward trend with ~66% active users by 2027.

Event Impact Modeling: Alignment with historical adoption patterns (e.g., policy and product launches).

Project Scope

Historical Analysis: Trends in account ownership, formal account adoption, and mobile money usage from 2011 to 2025.

Disaggregation: Data analyzed by gender and region to identify inclusion gaps.

Forecasting: Baseline and scenario projections to support strategic financial planning.

Event Analysis: Integration of key events and product launches to understand adoption dynamics.

Dashboard: Interactive visualization of historical trends, forecasts, and scenario comparisons.

Deliverables Completed (Interim Submission)

Reviewed the original dataset and project report.

Identified gaps in historical and disaggregated data, including missing values in MobileMoney_Overall, Account_Overall, and FI_Account_Overall.

Documented key columns critical to the improvement plan.

Collected supplementary data:

Gender-disaggregated statistics

Regional-level adoption metrics

Usage frequency details

Documented all data sources and transformations.

Saved the cleaned and enriched dataset for further analysis.

Next Steps

 Refine Event-Indicator Matrix, incorporate new evidence, implement dynamic lag effects.
 Update forecasting models using enriched data; generate improved baseline and scenario projections.

 Enhance the dashboard with updated visualizations, confidence intervals, and scenario comparisons; finalize documentation for final submission.

Data Summary

Original Dataset: Global Findex Database 2025

Supplementary Data: Gender, regional, and usage frequency metrics.

Cleaned Dataset Shape: ~8,500 rows × 7 columns (Year, Adult_Population, Account_Overall, FI_Account_Overall, MobileMoney_Overall, Gender, Group)

Missing Values: Interpolated for most indicators; MobileMoney_Overall has minimal remaining gaps to be addressed in forecasting.

Tools & Methods

Python: pandas, numpy, matplotlib, seaborn

Data Cleaning & Preprocessing: Interpolation, handling missing values, numeric conversions

Exploratory Analysis: National, regional, and gender trends visualization

Event-Indicator Analysis: Linking policy/product launches to adoption trends

Forecasting: Baseline and scenario projections for 2025–2027

Dashboard Development: Interactive visualizations to communicate insights

✅ Interim Status: Data cleaning and enrichment completed; national and regional datasets prepared for trend analysis and forecasting. Project is on track for subsequent steps (event modeling, forecasting, and dashboard enhancement).