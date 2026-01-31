"""ASX Symbol Universe Ingestion Job.

Implements Feature 011 - ASX Symbol Universe Ingestion.
"""

from datetime import datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger
from asx_jobs.providers.yahoo import YahooFinanceProvider

logger = get_logger(__name__)

ASX_300_SYMBOLS = [
    "A2M",
    "AAA",
    "ABC",
    "ABP",
    "AFI",
    "AGL",
    "AIA",
    "ALD",
    "ALL",
    "ALQ",
    "ALU",
    "ALX",
    "AMC",
    "AMP",
    "ANN",
    "ANZ",
    "APA",
    "APE",
    "APX",
    "ARB",
    "ARG",
    "ASX",
    "AWC",
    "AZJ",
    "BAP",
    "BEN",
    "BFL",
    "BGA",
    "BHP",
    "BKL",
    "BKW",
    "BLD",
    "BOQ",
    "BPT",
    "BRG",
    "BSL",
    "BWP",
    "CAR",
    "CBA",
    "CCL",
    "CCP",
    "CGF",
    "CHC",
    "CHN",
    "CIA",
    "CIM",
    "CLW",
    "CMW",
    "CNU",
    "COH",
    "COL",
    "CPU",
    "CQR",
    "CSL",
    "CSR",
    "CTD",
    "CWY",
    "DEG",
    "DHG",
    "DMP",
    "DOW",
    "DRR",
    "DXS",
    "EBO",
    "EDV",
    "ELD",
    "EML",
    "EVN",
    "EVT",
    "FBU",
    "FLT",
    "FMG",
    "FPH",
    "GMG",
    "GNE",
    "GOZ",
    "GPT",
    "GQG",
    "HLS",
    "HMC",
    "HUB",
    "HVN",
    "IAG",
    "IEL",
    "IFL",
    "IGO",
    "ILU",
    "IMB",
    "INA",
    "IPL",
    "IRE",
    "JBH",
    "JHX",
    "KAR",
    "KGN",
    "KMD",
    "LFG",
    "LIC",
    "LLC",
    "LNK",
    "LOV",
    "LYC",
    "MAQ",
    "MEZ",
    "MFG",
    "MGR",
    "MIN",
    "MMS",
    "MPL",
    "MQG",
    "MRM",
    "MTS",
    "NAB",
    "NCM",
    "NEC",
    "NHF",
    "NIC",
    "NSR",
    "NST",
    "NUF",
    "NWL",
    "NXT",
    "OML",
    "ORA",
    "ORG",
    "ORI",
    "OZL",
    "PBH",
    "PDL",
    "PLS",
    "PME",
    "PMV",
    "PNI",
    "PNV",
    "PPT",
    "PRN",
    "PTM",
    "QAN",
    "QBE",
    "QUB",
    "REA",
    "REH",
    "RHC",
    "RIO",
    "RMD",
    "RRL",
    "RWC",
    "S32",
    "SBM",
    "SCG",
    "SCP",
    "SDF",
    "SEK",
    "SFR",
    "SGM",
    "SGP",
    "SGR",
    "SHL",
    "SIQ",
    "SKC",
    "SLC",
    "SLR",
    "SNZ",
    "SOL",
    "SPK",
    "SQ2",
    "SRV",
    "SSM",
    "STO",
    "STW",
    "SUL",
    "SUN",
    "SVW",
    "TAH",
    "TCL",
    "TLC",
    "TLS",
    "TNE",
    "TPG",
    "TWE",
    "TYR",
    "UMG",
    "URW",
    "VCX",
    "VEA",
    "VNT",
    "VUK",
    "WBC",
    "WEB",
    "WES",
    "WHC",
    "WOR",
    "WOW",
    "WPR",
    "WTC",
    "XRO",
    "YAL",
    "ZIP",
]


class IngestSymbolsJob(BaseJob):
    """Ingest ASX symbols into the database.

    Currently uses a curated list of ASX 300 symbols.
    Future: scrape from ASX website or use official CSV.
    """

    def __init__(
        self,
        db: Database,
        provider: YahooFinanceProvider | None = None,
        symbols: list[str] | None = None,
        fetch_metadata: bool = True,
    ) -> None:
        """Initialize the job.

        Args:
            db: Database client.
            provider: Yahoo Finance provider for metadata.
            symbols: Custom symbol list (defaults to ASX 300).
            fetch_metadata: Whether to fetch metadata from Yahoo.
        """
        self.db = db
        self.provider = provider or YahooFinanceProvider()
        self.symbols = symbols or ASX_300_SYMBOLS
        self.fetch_metadata = fetch_metadata

    @property
    def name(self) -> str:
        return "ingest_symbols"

    def run(self) -> JobResult:
        """Execute symbol ingestion."""
        started_at = datetime.now()
        processed = 0
        failed = 0
        errors: list[str] = []

        logger.info("job_started", job=self.name, symbols_count=len(self.symbols))

        for symbol in self.symbols:
            try:
                metadata: dict[str, Any] = {}
                name: str | None = None
                sector: str | None = None
                industry: str | None = None
                market_cap: int | None = None

                if self.fetch_metadata:
                    info = self.provider.get_instrument_info(symbol)
                    if info:
                        name = info.get("name")
                        sector = info.get("sector")
                        industry = info.get("industry")
                        market_cap = info.get("market_cap")
                        metadata = {"yahoo": info}

                self.db.upsert_instrument(
                    symbol=symbol,
                    name=name,
                    sector=sector,
                    industry=industry,
                    market_cap=market_cap,
                    is_asx300=symbol in ASX_300_SYMBOLS,
                    metadata=metadata,
                )

                processed += 1
                logger.debug("symbol_ingested", symbol=symbol, name=name)

            except Exception as e:
                failed += 1
                error_msg = f"{symbol}: {str(e)}"
                errors.append(error_msg)
                logger.warning("symbol_failed", symbol=symbol, error=str(e))

        completed_at = datetime.now()

        logger.info(
            "job_completed",
            job=self.name,
            processed=processed,
            failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=failed == 0,
            started_at=started_at,
            completed_at=completed_at,
            records_processed=processed,
            records_failed=failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={"symbols_count": len(self.symbols)},
        )
