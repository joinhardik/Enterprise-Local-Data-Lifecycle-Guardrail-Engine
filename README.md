# Enterprise Local Data Lifecycle & Guardrail Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-red.svg)](https://docs.pydantic.dev/)
[![DVC Tracked](https://img.shields.io/badge/DVC-Enabled-9cf.svg)](https://dvc.org/)
[![Code Style: Strict Type-Checked](https://img.shields.io/badge/mypy-strict-green.svg)](https://mypy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, deterministic MLOps data feature pipeline designed for automated financial compliance document parsing and vector feature embedding generation. 

This project demonstrates a production **Zero-Data-in-Git Boundary** using Data Version Control (DVC), zero-copy content-addressable storage (CAS), Pydantic V2 quality gates, and automated cache key invalidation across a multi-stage Directed Acyclic Graph (DAG).

---

## 🏗️ Architectural Overview

```text
                      [ Raw Regulatory Inputs ]
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Stage 1: Ingestion    │ ──► [data/raw/ingested_chunks.json]
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Stage 2: Schema Gate   │ (Fails O(1) on validation errors)
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Stage 3: Feature Embed  │
                    └────────────┬────────────┘
                                 │
            ┌────────────────────┴────────────────────┐
            ▼                                         ▼
[data/processed/vector_features.json]        [metrics/eval.json & loss_curve.csv]
