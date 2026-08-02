"""
RNASeq Navigator

Metadata Cache

Version: 1.1

Persistent cache for repository metadata.

Each accession is stored as a JSON file.

Example:

cache/
    PRJNA799829.json
    SRP356545.json
    SRX34444857.json
"""

from pathlib import Path
from datetime import datetime, UTC
import json
from typing import Optional, Dict, List

# Cache directory
CACHE_DIR = Path(__file__).parent


class MetadataCache:
    """
    Persistent metadata cache.

    Each accession is stored as an individual JSON file.
    """

    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _filename(self, accession: str) -> Path:
        """
        Return cache filename for an accession.
        """
        return CACHE_DIR / f"{accession.upper()}.json"

    def exists(self, accession: str) -> bool:
        """
        Check whether metadata is already cached.
        """
        return self._filename(accession).exists()

    def load(self, accession: str) -> Optional[Dict]:
        """
        Load cached metadata.

        Returns
        -------
        dict or None
        """
        file = self._filename(accession)

        if not file.exists():
            return None

        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:
            print(f"Warning: Corrupted cache file: {file}")
            return None

    def save(self, accession: str, metadata: Dict) -> None:
        """
        Save metadata to cache.
        """

        payload = {
            "cached_at": datetime.now(UTC).isoformat(),
            "metadata": metadata
        }

        with open(self._filename(accession), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)

    def delete(self, accession: str) -> bool:
        """
        Delete a cached accession.

        Returns
        -------
        bool
            True if deleted, False otherwise.
        """
        file = self._filename(accession)

        if file.exists():
            file.unlink()
            return True

        return False

    def clear(self) -> None:
        """
        Remove all cached metadata.
        """
        for file in CACHE_DIR.glob("*.json"):
            file.unlink()

    def list(self) -> List[str]:
        """
        Return all cached accessions.
        """
        return sorted(
            file.stem
            for file in CACHE_DIR.glob("*.json")
        )

    def cache_size(self) -> int:
        """
        Return the number of cached accessions.
        """
        return len(self.list())


if __name__ == "__main__":

    cache = MetadataCache()

    example_metadata = {
        "organism": "Mycobacterium tuberculosis H37Rv",
        "strategy": "RNA-Seq",
        "layout": "PAIRED"
    }

    accession = "PRJNA799829"

    print("\nSaving metadata...")
    cache.save(accession, example_metadata)

    print("\nExists?")
    print(cache.exists(accession))

    print("\nLoaded metadata:")
    print(cache.load(accession))

    print("\nCached accessions:")
    print(cache.list())

    print("\nTotal cached:")
    print(cache.cache_size())
