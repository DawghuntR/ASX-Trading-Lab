"""Base job interface for ASX Jobs Runner."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class JobResult:
    """Result of a job execution."""

    job_name: str
    success: bool
    started_at: datetime
    completed_at: datetime
    records_processed: int = 0
    records_failed: int = 0
    error_message: str | None = None
    metadata: dict[str, Any] | None = None

    @property
    def duration_seconds(self) -> float:
        """Calculate job duration in seconds."""
        return (self.completed_at - self.started_at).total_seconds()


class BaseJob(ABC):
    """Base class for all jobs."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Job name for logging and identification."""
        ...

    @abstractmethod
    def run(self) -> JobResult:
        """Execute the job.

        Returns:
            JobResult with execution details.
        """
        ...
