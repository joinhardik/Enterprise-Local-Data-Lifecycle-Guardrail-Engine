from abc import ABC
from typing import Final, Any, Optional
from datetime import datetime, timezone


class PipelineRootException(Exception, ABC):
    """Abstract baseline for all pipeline infrastructure exceptions."""
    __slots__ = ("error_code", "timestamp", "details")

    def __init__(self, error_code: str, message: str, details: Optional[Any] = None) -> None:
        super().__init__(message)
        self.error_code: Final[str] = error_code
        self.timestamp: Final[datetime] = datetime.now(timezone.utc)
        self.details: Final[Optional[Any]] = details


class DataSchemaViolationException(PipelineRootException):
    """Raised when incoming dataset features fail Pydantic structural validation gates."""
    __slots__ = ()


class PipelineStageExecutionException(PipelineRootException):
    """Raised when an internal processing stage crashes mid-execution."""
    __slots__ = ()