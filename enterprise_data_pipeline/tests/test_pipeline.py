import pytest
import os
import json
from src.schemas import DocumentChunkSchema, VectorEmbeddingPayloadSchema
from pydantic import ValidationError


def test_document_chunk_schema_valid() -> None:
    """Verifies that pristine chunk payload passes validation."""
    payload = {
        "chunk_id": "12345678-1234-5678-1234-567812345678",
        "source_channel": "compliance_stream",
        "raw_text": "Valid compliance record text meeting minimum length.",
        "word_count": 7
    }
    chunk = DocumentChunkSchema(**payload)
    assert chunk.source_channel == "compliance_stream"


def test_document_chunk_schema_invalid_short_text() -> None:
    """Verifies that short/empty text fails quality gate."""
    payload = {
        "chunk_id": "12345678-1234-5678-1234-567812345678",
        "source_channel": "compliance_stream",
        "raw_text": "Too short",
        "word_count": 2
    }
    with pytest.raises(ValidationError):
        DocumentChunkSchema(**payload)


def test_vector_embedding_schema_dimension_mismatch() -> None:
    """Verifies that vector arrays not matching 768 dimensions fail validation."""
    payload = {
        "chunk_id": "12345678-1234-5678-1234-567812345678",
        "embedding_vector": [0.1] * 512,  # Wrong dimension (512 instead of 768)
        "embedding_dim": 768
    }
    with pytest.raises(ValidationError):
        VectorEmbeddingPayloadSchema(**payload)