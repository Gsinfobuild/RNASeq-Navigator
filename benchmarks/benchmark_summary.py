"""
RNASeq Navigator

Benchmark Summary Generator

Creates publication-ready benchmark reports.

Version: 2.0
"""

from pathlib import Path
from datetime import datetime
import json
import csv

RESULTS_DIR = Path("benchmarks/results")


def write_markdown_report(summary,
                          class_stats,
                          benchmark_name,
                          software_version,
                          results):
    """
    Write a publication-ready Markdown benchmark report.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    report_file = RESULTS_DIR / "benchmark_report.md"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(report_file, "w", encoding="utf-8") as f:

        f.write("# RNASeq Navigator Benchmark Report\n\n")

        f.write("## Benchmark Information\n\n")
        f.write(f"- **Software Version:** {software_version}\n")
        f.write(f"- **Benchmark Dataset:** {benchmark_name}\n")
        f.write(f"- **Generated:** {now}\n\n")

        f.write("---\n\n")

        f.write("## Overall Performance\n\n")

        f.write(f"- Projects Tested: **{summary['tested']}**\n")
        f.write(f"- Correct: **{summary['correct']}**\n")
        f.write(f"- Incorrect: **{summary['incorrect']}**\n")
        f.write(f"- Accuracy: **{summary['accuracy']:.2f}%**\n\n")

        f.write("---\n\n")

        f.write("## Per-Class Statistics\n\n")

        for study_type in sorted(class_stats):

            stats = class_stats[study_type]

            f.write(f"### {study_type}\n\n")

            f.write(f"- Projects: {stats['projects']}\n")
            f.write(f"- Correct: {stats['correct']}\n")
            f.write(f"- Incorrect: {stats['incorrect']}\n")
            f.write(f"- Accuracy: {stats['accuracy']:.2f}%\n\n")

        f.write("---\n\n")

        f.write("## Tested Projects\n\n")

        f.write("| Accession | Expected | Predicted | Result |\n")
        f.write("|-----------|----------|-----------|--------|\n")

        for r in results:

            status = "PASS" if r["correct"] else "FAIL"

            f.write(
                f"| {r['accession']} | "
                f"{r['expected']} | "
                f"{r['predicted']} | "
                f"{status} |\n"
            )

        f.write("\n---\n\n")

        failures = [r for r in results if not r["correct"]]

        f.write("## Misclassification Report\n\n")

        if not failures:

            f.write("No misclassifications detected.\n")

        else:

            for r in failures:

                f.write(f"### {r['accession']}\n\n")
                f.write(f"- Expected: {r['expected']}\n")
                f.write(f"- Predicted: {r['predicted']}\n\n")

    print(f"✓ Markdown report saved to: {report_file}")


def write_json_report(summary,
                      class_stats,
                      benchmark_name,
                      software_version,
                      results):
    """
    Save benchmark report as JSON.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    report_file = RESULTS_DIR / "benchmark_results.json"

    report = {
        "software_version": software_version,
        "benchmark_dataset": benchmark_name,
        "generated": datetime.now().isoformat(),
        "summary": summary,
        "class_statistics": class_stats,
        "results": results,
    }

    with open(report_file, "w", encoding="utf-8") as f:

        json.dump(report, f, indent=4)

    print(f"✓ JSON report saved to: {report_file}")


def write_csv_report(results):
    """
    Save project-level benchmark results as CSV.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    report_file = RESULTS_DIR / "benchmark_results.csv"

    with open(report_file,
              "w",
              newline="",
              encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Accession",
            "Expected",
            "Predicted",
            "Correct"
        ])

        for r in results:

            writer.writerow([
                r["accession"],
                r["expected"],
                r["predicted"],
                r["correct"],
            ])

    print(f"✓ CSV report saved to: {report_file}")
