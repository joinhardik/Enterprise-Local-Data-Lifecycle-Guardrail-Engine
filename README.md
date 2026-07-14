# Enterprise-Local-Data-Lifecycle-Guardrail-Engine

An enterprise-grade, deterministic MLOps data feature pipeline designed for automated financial compliance document parsing and vector feature embedding generation.
This project demonstrates a production Zero-Data-in-Git Boundary using Data Version Control (DVC), zero-copy content-addressable storage (CAS), Pydantic V2 quality gates, and automated cache key invalidation across a multi-stage Directed Acyclic Graph (DAG).

Architectural Overview
[ Raw Regulatory Inputs ]
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Stage 1: Ingestion    │ ──► [data/raw/ingested_chunks.json]
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Stage 2: Schema Gate   │ (Fails $O(1)$ on validation errors)
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
