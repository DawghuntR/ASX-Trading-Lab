"""Configuration management for ASX Jobs Runner."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class SupabaseConfig:
    """Supabase connection configuration."""

    url: str
    service_role_key: str

    def validate(self) -> None:
        """Validate Supabase configuration."""
        if not self.url or self.url == "https://your-project.supabase.co":
            raise ValueError("SUPABASE_URL is not configured")
        if not self.service_role_key or self.service_role_key == "your-service-role-key-here":
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY is not configured")


@dataclass
class YahooConfig:
    """Yahoo Finance provider configuration."""

    rate_limit_delay: float = 0.5
    batch_size: int = 10
    timeout: int = 30


@dataclass
class JobConfig:
    """Job runner configuration."""

    log_level: str = "INFO"
    batch_size: int = 50
    retry_attempts: int = 3
    retry_delay: float = 5.0


@dataclass
class Config:
    """Main configuration container."""

    supabase: SupabaseConfig
    yahoo: YahooConfig = field(default_factory=YahooConfig)
    job: JobConfig = field(default_factory=JobConfig)

    def validate(self) -> None:
        """Validate all configuration."""
        self.supabase.validate()


def load_config(env_file: Path | None = None) -> Config:
    """Load configuration from environment variables.

    Args:
        env_file: Optional path to .env file. If not provided,
                  looks for .env in current directory.

    Returns:
        Fully populated Config object.

    Raises:
        ValueError: If required configuration is missing.
    """
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    supabase_config = SupabaseConfig(
        url=os.getenv("SUPABASE_URL", ""),
        service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
    )

    yahoo_config = YahooConfig(
        rate_limit_delay=float(os.getenv("YAHOO_RATE_LIMIT_DELAY", "0.5")),
        batch_size=int(os.getenv("YAHOO_BATCH_SIZE", "10")),
        timeout=int(os.getenv("YAHOO_TIMEOUT", "30")),
    )

    job_config = JobConfig(
        log_level=os.getenv("ASX_JOBS_LOG_LEVEL", "INFO"),
        batch_size=int(os.getenv("ASX_JOBS_BATCH_SIZE", "50")),
        retry_attempts=int(os.getenv("ASX_JOBS_RETRY_ATTEMPTS", "3")),
        retry_delay=float(os.getenv("ASX_JOBS_RETRY_DELAY", "5")),
    )

    return Config(
        supabase=supabase_config,
        yahoo=yahoo_config,
        job=job_config,
    )
