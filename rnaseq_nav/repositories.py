"""
RNASeq Navigator

Repository Manager

Version 1.0

Routes accession requests to the
appropriate public repository.
"""

from rnaseq_nav.accession import detect_accession


class RepositoryManager:
    """
    Determine which repository should
    provide metadata for an accession.
    """

    def __init__(self):

        self.repositories = {
            "NCBI": self.fetch_ncbi,
            "ENA": self.fetch_ena,
            "DDBJ": self.fetch_ddbj,
        }

    def fetch(self, accession):
        """
        Route accession to the correct repository.
        """

        info = detect_accession(accession)

        database = info["database"]

        if database not in self.repositories:

            raise ValueError(
                f"Unsupported accession: {accession}"
            )

        return self.repositories[database](accession)

    def fetch_ncbi(self, accession):

        print(f"[NCBI] Retrieving {accession}")

        return {
            "database": "NCBI",
            "accession": accession,
        }

    def fetch_ena(self, accession):

        print(f"[ENA] Retrieving {accession}")

        return {
            "database": "ENA",
            "accession": accession,
        }

    def fetch_ddbj(self, accession):

        print(f"[DDBJ] Retrieving {accession}")

        return {
            "database": "DDBJ",
            "accession": accession,
        }


if __name__ == "__main__":

    manager = RepositoryManager()

    tests = [
        "PRJNA1493258",
        "PRJEB12345",
        "PRJDB42722",
        "SRX34444857",
        "ERX16608090",
    ]

    for accession in tests:

        print(manager.fetch(accession))
