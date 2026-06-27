"""
RNASeq Navigator

Shared Tokenizer

Version 1.0
"""

import re


def tokenize(text: str) -> list:
    """
    Convert text into normalized tokens.
    """

    if not text:
        return []

    text = text.lower()

    text = text.replace("_", " ")
    text = text.replace("-", " ")

    text = re.sub(r"[^\w\s]", " ", text)

    return text.split()


def collect_tokens(study: dict) -> set:
    """
    Collect searchable tokens from study metadata.
    """

    tokens = []

    tokens.extend(
        tokenize(
            study.get("scientific_name", "")
        )
    )

    for run in study.get("run_metadata", []):

        tokens.extend(
            tokenize(
                run.get("experiment_title", "")
            )
        )

        tokens.extend(
            tokenize(
                run.get("sample_alias", "")
            )
        )

    return set(tokens)
