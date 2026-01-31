# Forecasting Financial Inclusion in Ethiopia

## 10 Academy – Artificial Intelligence Mastery (Week 10 Challenge)

---

## Executive Summary
This project develops a data-driven forecasting system to analyze and predict Ethiopia’s financial inclusion trajectory, focusing on **Access** (account ownership) and **Usage** (digital payment adoption) as defined by the World Bank Global Findex.

Despite rapid growth in digital financial services such as Telebirr and M-Pesa, recent Global Findex data shows that financial inclusion growth has slowed. This project investigates the drivers of inclusion, estimates the impact of key national events and policies, and forecasts financial inclusion outcomes for **2025–2027** under multiple scenarios.

The final outputs include enriched datasets, analytical notebooks, event-impact models, forecasts with uncertainty bounds, and an interactive dashboard for policymakers and financial sector stakeholders.

---

## Business Context
Ethiopia is undergoing a major digital financial transformation:
- Telebirr has exceeded 54 million registered users since 2021
- M-Pesa entered the Ethiopian market in 2023
- Interoperable digital transfers have surpassed ATM cash withdrawals

However, according to the **2024 Global Findex**, only **49%** of Ethiopian adults have a financial account — an increase of just **3 percentage points** since 2021.

Stakeholders seek answers to:
- What drives financial inclusion in Ethiopia?
- How do policies, infrastructure, and product launches affect outcomes?
- What will inclusion levels look like in 2025–2027?

---

## Key Indicators (Global Findex Definitions)

### 1. Access — Account Ownership
Percentage of adults (15+) who have an account at a financial institution or personally use a mobile money service.

### 2. Usage — Digital Payments
Percentage of adults who made or received a digital payment in the past 12 months.

---

## Data Description

### Unified Dataset Design
The project uses a **unified data schema**, where all records share the same structure but represent different concepts based on the `record_type` field:

| record_type | Description |
|------------|-------------|
| Observation | Measured data points (survey, operator, infrastructure data) |
| Event | Policies, product launches, regulatory changes, milestones |
| impact_link | Modeled relationships between events and indicators |
| Target | Official policy or strategic targets |

Events are **pillar-neutral**. Their effects on specific indicators are modeled through `impact_link` records to avoid analytical bias.

### Data Sources
- World Bank Global Findex
- National Bank of Ethiopia
- IMF Financial Access Survey
- GSMA Mobile Economy Reports
- Ethio Telecom
- EthSwitch
- Fayda Digital ID Program
- Shega Media

---

## Project Structure
```text
ethiopia-fi-forecast/
├── .github/workflows/
│   └── unittests.yml
├── data/
│   ├── raw/
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/
├── notebooks/
│   ├── task_1_data_exploration.ipynb
│   ├── task_2_eda.ipynb
│   ├── task_3_event_impact.ipynb
│   └── task_4_forecasting.ipynb
├── src/
│   └── __init__.py
├── dashboard/
│   └── app.py
├── tests/
│   └── __init__.py
├── models/
├── reports/
│   └── figures/
├── requirements.txt
├── README.md
└── .gitignore

Methodology Overview
Task 1: Data Exploration & Enrichment

Explored unified schema and reference codes

Assessed temporal coverage and data gaps

Enriched dataset with infrastructure, technology, and policy indicators

Documented all additions with sources and confidence levels

Task 2: Exploratory Data Analysis

Analyzed trends in account ownership and digital payments

Investigated gender, urban–rural, and usage gaps where data allowed

Examined relationships between infrastructure and inclusion

Visualized event timelines alongside indicator trends

Task 3: Event Impact Modeling

Modeled how events affect indicators using impact_link records

Built an event–indicator association matrix

Incorporated evidence from comparable countries where local data was sparse

Validated estimated impacts against historical outcomes

Task 4: Forecasting (2025–2027)

Developed baseline trend forecasts

Built event-augmented forecasts

Produced optimistic, base, and pessimistic scenarios

Quantified uncertainty using confidence intervals

Task 5: Dashboard Development

Built an interactive Streamlit dashboard

Visualized trends, event impacts, and forecasts

Enabled scenario selection and data download

Key Outputs

Enriched financial inclusion dataset

Event–indicator impact matrix

Forecasts for Access and Usage (2025–2027)

Interactive dashboard for stakeholders

Final analytical report (blog-style)