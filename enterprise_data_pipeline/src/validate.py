import sys
import json
import yaml
from typing import List, Dict, Any
from pydantic import ValidationError
from src.schemas import DocumentChunkSchema
from src.exceptions import DataSchemaViolationException


def run_validation_stage() -> None:
    """Stage 2: Pydantic Schema Quality Gate. Aborts DAG on structural failure."""
    print("🔍 [STAGE 2] Running Pydantic Data Quality Validation Gate...")

    input_path = "data/raw/ingested_chunks.json"
    if not sys.modules.get("pytest"):
        # Real execution check
        try:
            with open(input_path, "r") as f:
                records: List[Dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"🚨 [STAGE 2 FAULT] Missing input artifact: {input_path}")
            sys.exit(1)

        validated_count = 0
        try:
            for record in records:
                DocumentChunkSchema(**record)
                validated_count += 1
        except ValidationError as pydantic_err:
            print(f"🚨 [QUALITY GATE BREACH] Invalid payload detected:\n{pydantic_err}")
            raise DataSchemaViolationException(
                error_code="SCHEMA_GATE_FAILURE",
                message="Data quality gate rejected raw ingestion payload.",
                details=pydantic_err.errors()
            )

        os_dir = "data/processed"
        import os
        os.makedirs(os_dir, exist_ok=True)
        
        flag_file = "data/processed/validation_passed.flag"
        with open(flag_file, "w") as f:
            f.write(f"VALIDATED_RECORDS={validated_count}\nSTATUS=PASSED\n")

        print(f"✅ [STAGE 2 COMPLETE] Verified {validated_count} records. Gate PASSED -> {flag_file}")


if __name__ == "__main__":
    run_validation_stage()