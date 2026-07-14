import os
import json
import yaml
import uuid
from typing import Dict, Any, List
from src.schemas import DocumentChunkSchema


def run_ingestion_stage() -> None:
    """Stage 1: Simulates downloading raw compliance text chunks and generating raw data."""
    print("📥 [STAGE 1] Ingesting raw compliance document chunks...")

    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)["ingest"]

    os.makedirs("data/raw", exist_ok=True)
    
    sample_count = params["raw_sample_count"]
    channel = params["source_channel"]
    
    records: List[Dict[str, Any]] = []
    for i in range(sample_count):
        text_content = f"Compliance Regulatory Audit Log Item #{i}: Transaction verified under protocol 2026."
        chunk = DocumentChunkSchema(
            chunk_id=str(uuid.uuid4()),
            source_channel=channel,
            raw_text=text_content,
            word_count=len(text_content.split())
        )
        records.append(chunk.model_dump())

    output_path = "data/raw/ingested_chunks.json"
    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)

    print(f"✅ [STAGE 1 COMPLETE] Ingested {len(records)} records -> {output_path}")


if __name__ == "__main__":
    run_ingestion_stage()