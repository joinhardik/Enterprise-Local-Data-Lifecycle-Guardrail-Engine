import uuid
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


class DocumentChunkSchema(BaseModel):
    """Enforces strict structural validation on raw document text chunks."""
    model_config = ConfigDict(strict=True, frozen=True)

    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_channel: str = Field(..., min_length=3, max_length=50)
    raw_text: str = Field(..., min_length=10)
    word_count: int = Field(..., gt=0)

    @field_validator("raw_text")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Raw text content cannot consist solely of whitespace.")
        return stripped


class VectorEmbeddingPayloadSchema(BaseModel):
    """Validates vector array dimension outputs before writing features to cache."""
    model_config = ConfigDict(strict=True, frozen=True)

    chunk_id: str = Field(...)
    embedding_vector: List[float] = Field(...)
    embedding_dim: int = Field(..., eq=768)

    @field_validator("embedding_vector")
    @classmethod
    def verify_exact_dimensions(cls, value: List[float]) -> List[float]:
        if len(value) != 768:
            raise ValueError(f"Vector array dimension must be exactly 768 floats. Received: {len(value)}")
        return value