# Yundu Life — Enterprise Retail Data Warehouse & Analytics System

> A complete, end-to-end enterprise data warehouse and business analytics platform built on the "Yundu Life" (云购生活) retail scenario: **raw CSV → ODS → cleansing → DWD → DWS → ADS → forecasting → NL2SQL → visualization → one-command deployment**.

![Architecture](docs/architecture.png)

## Overview

This project builds a four-layer dimensional data warehouse (Kimball star schema) on Hive 4.0, implements a full data-quality pipeline covering five classes of dirty data, layers analytics and AI capabilities on top (sales forecasting, NL2SQL powered by Zhipu GLM, automated business insights), and ships with a Superset dashboard, an ECharts big-screen wall, a Streamlit Q&A app, and a one-command Docker Compose deployment.

## Architecture

```
CSV Sources ──► ODS (raw) ──► Cleansing ──► DWD (star schema, monthly partitions)
                                                      │
                    ┌─────────────────────────────────┘
                    ▼
              DWS (aggregates) ──► ADS (KPIs) ──► Superset / ECharts / Streamlit
                    │                                    ▲
                    └──► Forecasting / NL2SQL / AI Insights ┘
```

**Warehouse layers**

| Layer | Purpose | Highlights |
|---|---|---|
| ODS | Raw landing (6 tables, ~115k rows) | TEXTFILE, no cleansing |
| DWD | Cleansed fact + dimension tables | Star schema, ORC, monthly partitions, 4 buckets |
| DWS | Light aggregates (day × store/category/channel) | 4 tables, monthly partitions |
| ADS | Business KPIs | GMV ¥14.15M, 5,642 orders, AOV ¥2,508.19, 997 active users |

**Data quality**: five classes of dirty data (missing values, duplicates, enum chaos, outliers, format inconsistencies) — all remediated with a 100% fix rate. Notable decision: P99 was polluted by extreme values (P99/P95 > 1000×), so a "business cap ¥100k + P95 truncation" strategy was adopted instead.

## Features

- 🧱 **Four-layer warehouse** with reproducible SQL scripts for every step
- 📊 **Superset dashboard** (Hive + MySQL dual sources, 6 charts) and an **ECharts big screen** (1920×1080, adaptive scaling, province map with standard China GeoJSON)
- 💬 **NL2SQL Q&A**: natural language → SQL (schema-injected prompts, SELECT-only interception, error-feedback self-repair) → Hive execution → charts; 4/4 test cases passed
- 📈 **Sales forecasting** with honest baseline comparison (MAPE 31.7% ≈ mean baseline — the simulated series has no learnable signal, and the report documents this boundary)
- 🐳 **One-command deployment**: 5 Docker services with healthchecks; the Hive warehouse is persisted in a named volume (full-pipeline replay verified — KPIs identical after recovery)

## Quick Start

```bash
# 1. Start the whole stack
docker compose up -d

# 2. Load & build the warehouse (ODS → ... → ADS)
bash sql/replay_all.sh

# 3. Register Superset datasources, charts and dashboard
python sql/superset_setup.py && python sql/superset_charts.py

# 4. Launch the NL2SQL Q&A app
streamlit run app/app.py
```

Configure your LLM key in `.env` (see `.env.example`):

```
ZHIPU_API_KEY=your.zhipu.api.key
ZHIPU_MODEL=glm-4-flash
```

## Tech Stack

Hive 4.0 / Tez · MySQL 8.0 · Kimball dimensional modeling · Python (pandas, scikit-learn) · Zhipu GLM (glm-4-flash) · Superset 6.1 · ECharts · Streamlit · Docker Compose

## Repository Layout

This project is organized as four weekly repositories mirroring the training program:

| Repo | Scope |
|---|---|
| [ydsh-week1](https://github.com/yuyu41-sg/ydsh-week1) | Environment, ODS ingestion, quality assessment, first-pass cleansing |
| [ydsh-week2](https://github.com/yuyu41-sg/ydsh-week2) | Advanced cleansing, DWD star-schema modeling, EDA |
| [ydsh-week3](https://github.com/yuyu41-sg/ydsh-week3) | DWS/ADS KPIs, forecasting, LLM integration, NL2SQL, Git collaboration (PR/Issue/conflict drills) |
| [ydsh-week4](https://github.com/yuyu41-sg/ydsh-week4) | Superset, ECharts big screen, Streamlit app, Compose orchestration, stress tests |

## Documentation

- 需求文档 (Requirements) · 数据质量清洗报告 (Data Quality Report) · 架构设计文档 (Architecture)
- 部署手册 (Deployment Guide) · API配置指南 (API Configuration Guide)
- Git 历史审查记录 (Git History Audit) — see `docs/`

## Team

- **张宇 (Yu Zhang)** — 20230308059, ydsh-team

## License

For educational purposes (enterprise project training program).
