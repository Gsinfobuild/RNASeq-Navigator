"""
RNASeq Navigator

Console Formatter

Version 1.0

Converts a DatasetReport into a formatted
terminal report.

This formatter NEVER prints directly.

Instead it returns a string.
"""

from rnaseq_nav.intelligence.report import (
    DatasetReport,
)


class ConsoleFormatter:

    WIDTH = 70

    # -------------------------------------------------

    def divider(self):

        return "=" * self.WIDTH

    # -------------------------------------------------

    def subsection(self):

        return "-" * self.WIDTH

    # -------------------------------------------------

    def render_section(
        self,
        section,
    ):

        if section.empty:

            return ""

        lines = []

        lines.append(section.title)

        lines.append(self.subsection())

        for key, value in section.fields.items():

            lines.append(
                f"{key:<20}: {value}"
            )

        lines.append("")

        return "\n".join(lines)

    # -------------------------------------------------

    def render(
        self,
        report: DatasetReport,
    ) -> str:

        lines = []

        lines.append(self.divider())

        lines.append("RNASeq Navigator")

        lines.append(self.divider())

        lines.append("")

        lines.append(
            f"Accession : {report.accession}"
        )

        lines.append(
            f"Version   : {report.version}"
        )

        lines.append("")

        for section in report.sections():

            text = self.render_section(
                section
            )

            if text:

                lines.append(text)

        return "\n".join(lines)
