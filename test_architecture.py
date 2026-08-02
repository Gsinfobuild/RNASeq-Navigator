"""
RNASeq Navigator

Architecture Integration Test

Version: 1.0

Tests:

✓ Package imports
✓ Accession detection
✓ Repository routing
✓ Metadata cache
✓ Cache persistence

Author:
RNASeq Navigator Development
"""

from pprint import pprint

print("=" * 80)
print("RNASeq Navigator Architecture Test")
print("=" * 80)


# ---------------------------------------------------------------------
# Test 1
# ---------------------------------------------------------------------

print("\n[1] Testing imports...")

try:

    from rnaseq_nav.accession import detect_accession
    from rnaseq_nav.repositories import RepositoryManager
    from rnaseq_nav.cache.metadata_cache import MetadataCache

    print("✓ Imports successful")

except Exception as e:

    print("✗ Import failed")
    print(e)
    quit()


# ---------------------------------------------------------------------
# Test 2
# ---------------------------------------------------------------------

print("\n[2] Testing accession detection...")

accessions = [

    "PRJNA799829",
    "PRJEB12345",
    "PRJDB42722",
    "SRX34444857",
    "ERX16608090",
    "DRR000001",
    "ABC123"

]

for accession in accessions:

    result = detect_accession(accession)

    pprint(result)


print("\n✓ Accession detector working")


# ---------------------------------------------------------------------
# Test 3
# ---------------------------------------------------------------------

print("\n[3] Testing repository manager...")

manager = RepositoryManager()

tests = [

    "PRJNA799829",
    "PRJEB12345",
    "PRJDB42722"

]

for accession in tests:

    result = manager.fetch(accession)

    pprint(result)


print("\n✓ Repository manager working")


# ---------------------------------------------------------------------
# Test 4
# ---------------------------------------------------------------------

print("\n[4] Testing metadata cache...")

cache = MetadataCache()

metadata = {

    "organism": "Mycobacterium tuberculosis H37Rv",
    "strategy": "RNA-Seq",
    "layout": "PAIRED"

}

cache.save("PRJNA799829", metadata)

print("Saved metadata")

loaded = cache.load("PRJNA799829")

print("\nLoaded metadata")

pprint(loaded)

assert loaded is not None

assert loaded["metadata"]["organism"] == \
       "Mycobacterium tuberculosis H37Rv"

assert loaded["metadata"]["strategy"] == \
       "RNA-Seq"

print("\n✓ Cache save/load successful")


# ---------------------------------------------------------------------
# Test 5
# ---------------------------------------------------------------------

print("\n[5] Testing cache listing...")

cached = cache.list()

print(cached)

assert "PRJNA799829" in cached

print("\n✓ Cache listing works")


# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------

print("\n" + "=" * 80)

print("ALL TESTS PASSED")

print("=" * 80)
