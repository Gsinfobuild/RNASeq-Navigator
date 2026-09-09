"""
RNASeq Navigator

Dataset Discovery Engine

Version 3.0
API STATUS: STABLE

Public API
----------
fetch(accession)

search(
    organism,
    strategy="RNA-Seq",
    layout=None,
    platform=None,
    source=None,
    selection=None,
    max_results=20,
    diversity="project",
)

NOTE
----
The search() signature is frozen for backward compatibility.
New filters should only be added as OPTIONAL keyword arguments.
Existing parameters must never be removed.
"""

from __future__ import annotations

from typing import Optional

from rnaseq_nav.clients.ncbi import NCBIClient
from rnaseq_nav.parsers.sra_parser import SRAParser
from rnaseq_nav.discovery.diversity import DatasetDiversity
from rnaseq_nav.discovery.ranker import DatasetRanker


class DatasetDiscovery:
    """
    Stable public interface for dataset discovery.
    """

    API_VERSION = "1.0"

    def __init__(
        self,
        email: str,
        api_key: Optional[str] = None,
        verbose: bool = False,
    ):

        self.client = NCBIClient(
            email=email,
            api_key=api_key,
            verbose=verbose,
        )

        self.parser = SRAParser()

    # ---------------------------------------------------------
    # PUBLIC API (STABLE)
    # ---------------------------------------------------------

    def fetch(self, accession: str):
        """
        Retrieve one accession.

        Parameters
        ----------
        accession
            SRR / ERR / DRR / SRX / SRP / PRJNA ...

        Returns
        -------
        Metadata
        """

        summary = self.client.fetch(accession)

        return self.parser.parse(summary)

    # ---------------------------------------------------------
    # PUBLIC API (STABLE)
    # ---------------------------------------------------------

    def search(
        self,
        organism: str,
        strategy: str = "RNA-Seq",
        layout: Optional[str] = None,
        platform: Optional[str] = None,
        source: Optional[str] = None,
        selection: Optional[str] = None,
        max_results: int = 20,
        diversity: str = "project",
    ):
        """
        Search public RNA-seq datasets.

        Parameters kept intentionally stable.
        Unimplemented filters are accepted for
        forward compatibility.
        """

        query = (
            f'"{organism}"[Organism] '
            f'AND "{strategy}" '
            f'AND public[Access]'
        )

        summaries = self.client.search(
            query=query,
            max_results=max_results,
        )

        metadata_list = []

        for summary in summaries:

            try:
                metadata = self.parser.parse(summary)
                metadata_list.append(metadata)

            except Exception:
                continue

        # Reserved filters
        if layout is not None:
            pass

        if platform is not None:
            pass

        if source is not None:
            pass

        if selection is not None:
            pass

        # Diversity selection
        if diversity == "project":

            metadata_list = DatasetRanker.best_per_project(
                metadata_list
            )

        elif diversity == "study":

            metadata_list = DatasetDiversity.unique_studies(
                metadata_list
            )

        elif diversity == "run":

            pass

        return metadata_list
