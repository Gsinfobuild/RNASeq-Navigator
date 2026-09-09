"""
RNASeq Navigator
Streamlit User Interface
Version 1.2

Purpose
-------
Provides a clean web interface for inspecting SRA accessions
through the RNASeq Navigator API.

Supported accessions
--------------------
SRR...
SRX...
ERR...
ERX...
DRR...
DRX...

Exports
-------
JSON
PDF
"""

# ==========================================================
# Standard Library
# ==========================================================

import sys
import json
import os
import re

from pathlib import Path
from dataclasses import asdict, is_dataclass
from io import BytesIO
from html import escape, unescape


# ==========================================================
# Make project root importable
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================================
# Third-party
# ==========================================================

import streamlit as st


# ==========================================================
# RNASeq Navigator
# ==========================================================

from rnaseq_nav import RNASeqNavigator


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="RNASeq Navigator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# Global UI Styling
# ==========================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------- */
    /* Main page */
    /* -------------------------------------------------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* -------------------------------------------------- */
    /* Main title */
    /* -------------------------------------------------- */

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.35rem;
    }


    .subtitle {
        font-size: 1rem;
        color: #9aa0aa;
        margin-bottom: 1.4rem;
    }


    /* -------------------------------------------------- */
    /* Section headings */
    /* -------------------------------------------------- */

    .section-title {
        font-size: 1.55rem;
        font-weight: 650;
        line-height: 1.3;
        margin-top: 1.8rem;
        margin-bottom: 0.35rem;
    }


    .section-description {
        font-size: 0.92rem;
        color: #9298a3;
        margin-bottom: 1rem;
    }


    /* -------------------------------------------------- */
    /* Metadata cards */
    /* -------------------------------------------------- */

    .metadata-card {
        background: #191c23;
        border: 1px solid #30343d;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 14px;
        min-height: 105px;
        box-sizing: border-box;
    }


    .metadata-label {
        font-size: 0.82rem;
        font-weight: 500;
        color: #aeb4bf;
        margin-bottom: 9px;
        line-height: 1.3;
    }


    .metadata-value {
        font-size: 1rem;
        font-weight: 500;
        color: #f2f4f7;
        line-height: 1.5;
        overflow-wrap: anywhere;
        word-break: break-word;
    }


    /* -------------------------------------------------- */
    /* Long metadata values */
    /* -------------------------------------------------- */

    .metadata-card-long {
        min-height: 125px;
    }


    .metadata-value-long {
        font-size: 0.94rem;
        line-height: 1.55;
    }


    /* -------------------------------------------------- */
    /* Accessions */
    /* -------------------------------------------------- */

    .accession-value {
        font-family: monospace;
        font-size: 1rem;
        letter-spacing: 0.2px;
    }


    /* -------------------------------------------------- */
    /* Report text */
    /* -------------------------------------------------- */

    .report-text {
        font-size: 1rem;
        line-height: 1.65;
        color: #e7e9ed;
        margin-bottom: 1rem;
    }


    /* -------------------------------------------------- */
    /* Export buttons */
    /* -------------------------------------------------- */

    div.stDownloadButton > button {
        min-height: 42px;
        font-size: 0.92rem;
    }


    /* -------------------------------------------------- */
    /* Metric consistency */
    /* -------------------------------------------------- */

    [data-testid="stMetricLabel"] {
        font-size: 0.82rem;
    }


    [data-testid="stMetricValue"] {
        font-size: 1.65rem;
    }


    /* -------------------------------------------------- */
    /* Hide Streamlit footer */
    /* -------------------------------------------------- */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Helper Functions
# ==========================================================

def get_value(
    obj,
    attribute,
    default="—",
):
    """
    Safely retrieve a value from either an object or dictionary.
    """

    if obj is None:
        return default

    if isinstance(obj, dict):
        value = obj.get(attribute, default)

    else:
        value = getattr(
            obj,
            attribute,
            default,
        )

    if value is None:
        return default

    if value == "":
        return default

    return value


# ----------------------------------------------------------


def format_number(value):
    """
    Format numeric values with thousands separators.
    """

    if value is None:
        return "—"

    try:
        return f"{int(value):,}"

    except (
        TypeError,
        ValueError,
    ):
        return str(value)


# ----------------------------------------------------------


def object_to_dict(obj):
    """
    Convert dataclasses, objects, dictionaries,
    lists and tuples into JSON-compatible structures.
    """

    if obj is None:
        return None

    if is_dataclass(obj):

        data = asdict(obj)

        return {
            str(key): object_to_dict(value)
            for key, value in data.items()
        }

    if isinstance(obj, dict):

        return {
            str(key): object_to_dict(value)
            for key, value in obj.items()
        }

    if isinstance(obj, (list, tuple)):

        return [
            object_to_dict(item)
            for item in obj
        ]

    if hasattr(obj, "__dict__"):

        return {
            str(key): object_to_dict(value)
            for key, value in vars(obj).items()
        }

    return obj


# ----------------------------------------------------------


def clean_ui_value(value):
    """
    Convert a metadata value into clean plain text.

    This is the important fix for the current UI problem.

    Some values can arrive from upstream layers containing
    HTML fragments such as:

        <div class="small-value">
            SRX35160763
        </div>

    Those fragments must never be inserted directly into
    the Streamlit HTML.

    This function:
        1. Converts structured objects to text.
        2. Removes HTML tags.
        3. Decodes HTML entities.
        4. Normalizes whitespace.
    """

    if value is None:
        return "—"

    # Structured objects
    if isinstance(value, (dict, list, tuple)):

        try:

            text = json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            )

        except Exception:

            text = str(value)

    else:

        text = str(value)

    # Decode entities first
    text = unescape(text)

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    # Normalize excessive whitespace
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text,
    )

    text = text.strip()

    if not text:
        return "—"

    return text


# ----------------------------------------------------------


def display_value(value):
    """
    Public formatting helper for UI/PDF output.
    """

    return clean_ui_value(value)


# ----------------------------------------------------------


def render_field(
    label,
    value,
    long=False,
    accession=False,
):
    """
    Render one clean metadata card.

    IMPORTANT:
    Values are HTML-escaped before insertion into the
    surrounding HTML. This prevents raw HTML fragments
    from appearing as code in the UI.
    """

    clean_label = clean_ui_value(label)
    clean_value = clean_ui_value(value)

    label_html = escape(
        clean_label,
        quote=True,
    )

    value_html = escape(
        clean_value,
        quote=True,
    )

    card_class = "metadata-card"

    if long:
        card_class += " metadata-card-long"

    value_class = "metadata-value"

    if long:
        value_class += " metadata-value-long"

    if accession:
        value_class += " accession-value"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="metadata-label">
                {label_html}
            </div>
            <div class="{value_class}">
                {value_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------


def render_section_title(
    title,
    description=None,
):
    """
    Render a consistent section heading.
    """

    title_html = escape(
        clean_ui_value(title),
        quote=True,
    )

    st.markdown(
        f"""
        <div class="section-title">
            {title_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if description:

        description_html = escape(
            clean_ui_value(description),
            quote=True,
        )

        st.markdown(
            f"""
            <div class="section-description">
                {description_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================================
# PDF Export
# ==========================================================

def build_pdf(
    result,
    accession,
):
    """
    Build a PDF inspection report.

    Returns
    -------
    bytes
        PDF document bytes.
    """

    try:

        from reportlab.lib import colors

        from reportlab.lib.enums import TA_CENTER

        from reportlab.lib.pagesizes import A4

        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle,
        )

        from reportlab.lib.units import mm

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            PageBreak,
        )

    except ImportError as exc:

        raise RuntimeError(
            "PDF export requires reportlab. "
            "Install it with: pip install reportlab"
        ) from exc


    # ======================================================
    # Extract objects
    # ======================================================

    report = getattr(
        result,
        "report",
        None,
    )

    metadata = getattr(
        result,
        "metadata",
        None,
    )

    validation = getattr(
        result,
        "validation",
        None,
    )

    normalization = getattr(
        result,
        "normalization",
        None,
    )


    # ======================================================
    # Dataset identity
    # ======================================================

    run = get_value(
        report,
        "run",
        None,
    )

    if run is None:
        run = get_value(
            report,
            "experiment",
            accession,
        )

    run = clean_ui_value(run)

    study = clean_ui_value(
        get_value(
            report,
            "study",
        )
    )

    experiment = clean_ui_value(
        get_value(
            report,
            "experiment",
        )
    )

    organism = clean_ui_value(
        get_value(
            report,
            "organism",
        )
    )

    project = clean_ui_value(
        get_value(
            report,
            "project",
        )
    )


    # ======================================================
    # BioSample
    # ======================================================

    sample = "—"

    if metadata is not None:

        sample_object = get_value(
            metadata,
            "sample",
            None,
        )

        sample = get_value(
            sample_object,
            "accession",
        )

    sample = clean_ui_value(sample)


    # ======================================================
    # Experiment information
    # ======================================================

    title = clean_ui_value(
        get_value(
            report,
            "title",
        )
    )

    strategy = clean_ui_value(
        get_value(
            report,
            "strategy",
        )
    )

    layout = clean_ui_value(
        get_value(
            report,
            "layout",
        )
    )

    sequencing_description = clean_ui_value(
        get_value(
            report,
            "sequencing",
        )
    )


    # ======================================================
    # Sequencing
    # ======================================================

    platform = clean_ui_value(
        get_value(
            report,
            "platform",
        )
    )

    instrument = clean_ui_value(
        get_value(
            report,
            "instrument",
        )
    )


    # ======================================================
    # Statistics
    # ======================================================

    total_spots = get_value(
        report,
        "total_spots",
        None,
    )

    total_bases = get_value(
        report,
        "total_bases",
        None,
    )


    # ======================================================
    # Public status
    # ======================================================

    public = "—"

    if metadata is not None:

        run_object = get_value(
            metadata,
            "run",
            None,
        )

        public_value = get_value(
            run_object,
            "public",
            None,
        )

        if public_value is not None:

            if isinstance(
                public_value,
                bool,
            ):

                public = (
                    "Yes"
                    if public_value
                    else "No"
                )

            else:

                public = str(
                    public_value
                )

    public = clean_ui_value(public)


    # ======================================================
    # Quality
    # ======================================================

    validation_score = clean_ui_value(
        get_value(
            report,
            "validation_score",
            None,
        )
    )

    normalization_changes = clean_ui_value(
        get_value(
            report,
            "normalization_changes",
            None,
        )
    )


    # ======================================================
    # Report text
    # ======================================================

    summary = clean_ui_value(
        get_value(
            report,
            "summary",
            "",
        )
    )

    sequencing = clean_ui_value(
        get_value(
            report,
            "sequencing",
            "",
        )
    )

    strengths = get_value(
        report,
        "strengths",
        [],
    )

    limitations = get_value(
        report,
        "limitations",
        [],
    )

    if strengths is None:
        strengths = []

    if limitations is None:
        limitations = []


    # ======================================================
    # PDF document
    # ======================================================

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=(
            f"{accession} - "
            "RNASeq Navigator Report"
        ),
        author="RNASeq Navigator",
    )


    # ======================================================
    # PDF styles
    # ======================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "RNASeqReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    section_style = ParagraphStyle(
        "RNASeqReportSection",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "RNASeqReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
    )

    heading_style = ParagraphStyle(
        "RNASeqReportHeading",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        spaceBefore=5,
        spaceAfter=4,
    )


    # ======================================================
    # Story
    # ======================================================

    story = []


    # ======================================================
    # PDF title
    # ======================================================

    story.append(
        Paragraph(
            "RNASeq Navigator",
            title_style,
        )
    )

    story.append(
        Paragraph(
            (
                "Dataset inspection report: "
                f"{escape(str(accession))}"
            ),
            body_style,
        )
    )

    story.append(
        Spacer(
            1,
            8,
        )
    )


    # ======================================================
    # PDF table helper
    # ======================================================

    def add_table(rows):

        table_rows = []

        for label, value in rows:

            label_text = clean_ui_value(
                label
            )

            value_text = clean_ui_value(
                value
            )

            table_rows.append(
                [
                    Paragraph(
                        f"<b>{escape(label_text)}</b>",
                        body_style,
                    ),
                    Paragraph(
                        escape(value_text).replace(
                            "\n",
                            "<br/>",
                        ),
                        body_style,
                    ),
                ]
            )

        table = Table(
            table_rows,
            colWidths=[
                52 * mm,
                122 * mm,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                8,
            )
        )


    # ======================================================
    # Dataset Overview
    # ======================================================

    story.append(
        Paragraph(
            "Dataset Overview",
            section_style,
        )
    )

    add_table(
        [
            ("Run", run),
            ("Study", study),
            ("Experiment", experiment),
            ("Organism", organism),
        ]
    )


    # ======================================================
    # Dataset Identity
    # ======================================================

    story.append(
        Paragraph(
            "Dataset Identity",
            section_style,
        )
    )

    add_table(
        [
            (
                "Input / Run accession",
                run,
            ),
            (
                "Study accession",
                study,
            ),
            (
                "Experiment accession",
                experiment,
            ),
            (
                "BioProject",
                project,
            ),
            (
                "BioSample",
                sample,
            ),
            (
                "Organism",
                organism,
            ),
        ]
    )


    # ======================================================
    # Experiment Information
    # ======================================================

    story.append(
        Paragraph(
            "Experiment Information",
            section_style,
        )
    )

    add_table(
        [
            (
                "Experiment title",
                title,
            ),
            (
                "Library strategy",
                strategy,
            ),
            (
                "Layout",
                layout,
            ),
            (
                "Sequencing description",
                sequencing_description,
            ),
        ]
    )


    # ======================================================
    # Sequencing Information
    # ======================================================

    story.append(
        Paragraph(
            "Sequencing Information",
            section_style,
        )
    )

    add_table(
        [
            (
                "Platform",
                platform,
            ),
            (
                "Instrument",
                instrument,
            ),
            (
                "Layout",
                layout,
            ),
        ]
    )


    # ======================================================
    # Dataset Statistics
    # ======================================================

    story.append(
        Paragraph(
            "Dataset Statistics",
            section_style,
        )
    )

    add_table(
        [
            (
                "Reads / Spots",
                format_number(total_spots),
            ),
            (
                "Bases",
                format_number(total_bases),
            ),
            (
                "Public",
                public,
            ),
        ]
    )


    # ======================================================
    # Metadata Quality
    # ======================================================

    story.append(
        Paragraph(
            "Metadata Quality",
            section_style,
        )
    )

    add_table(
        [
            (
                "Validation score",
                validation_score,
            ),
            (
                "Normalization changes",
                normalization_changes,
            ),
        ]
    )


    # ======================================================
    # Dataset Report
    # ======================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "Dataset Report",
            section_style,
        )
    )


    if summary and summary != "—":

        story.append(
            Paragraph(
                "Summary",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                escape(summary).replace(
                    "\n",
                    "<br/>",
                ),
                body_style,
            )
        )

        story.append(
            Spacer(
                1,
                6,
            )
        )


    if sequencing and sequencing != "—":

        story.append(
            Paragraph(
                "Sequencing interpretation",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                escape(sequencing).replace(
                    "\n",
                    "<br/>",
                ),
                body_style,
            )
        )

        story.append(
            Spacer(
                1,
                6,
            )
        )


    # ======================================================
    # Strengths
    # ======================================================

    if strengths:

        story.append(
            Paragraph(
                "Strengths",
                heading_style,
            )
        )

        for item in strengths:

            text = clean_ui_value(item)

            story.append(
                Paragraph(
                    "• "
                    + escape(text),
                    body_style,
                )
            )

        story.append(
            Spacer(
                1,
                6,
            )
        )


    # ======================================================
    # Limitations
    # ======================================================

    if limitations:

        story.append(
            Paragraph(
                "Limitations",
                heading_style,
            )
        )

        for item in limitations:

            text = clean_ui_value(item)

            story.append(
                Paragraph(
                    "• "
                    + escape(text),
                    body_style,
                )
            )


    # ======================================================
    # Validation Details
    # ======================================================

    story.append(
        Paragraph(
            "Validation Details",
            section_style,
        )
    )

    validation_text = json.dumps(
        object_to_dict(validation),
        indent=2,
        ensure_ascii=False,
        default=str,
    )

    story.append(
        Paragraph(
            escape(validation_text).replace(
                "\n",
                "<br/>",
            ),
            body_style,
        )
    )


    # ======================================================
    # Normalization Details
    # ======================================================

    story.append(
        Paragraph(
            "Normalization Details",
            section_style,
        )
    )

    normalization_text = json.dumps(
        object_to_dict(normalization),
        indent=2,
        ensure_ascii=False,
        default=str,
    )

    story.append(
        Paragraph(
            escape(normalization_text).replace(
                "\n",
                "<br/>",
            ),
            body_style,
        )
    )


    # ======================================================
    # Build PDF
    # ======================================================

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ==========================================================
# Header
# ==========================================================

st.markdown(
    """
    <div class="main-title">
        🧬 RNASeq Navigator
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Explore information associated with an RNA-seq/SRA accession.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Introduction
# ==========================================================

st.write(
    "Enter any valid SRA accession to inspect the available "
    "dataset metadata."
)

st.caption(
    "Examples: SRR17730393, SRR17730394, SRR17730395, "
    "SRX35161265"
)


# ==========================================================
# Dataset Accession
# ==========================================================

render_section_title(
    "Dataset accession"
)

accession = st.text_input(
    "Enter an SRA accession",
    value="SRR17730393",
    placeholder="e.g. SRR17730393",
)


# ==========================================================
# NCBI Configuration
# ==========================================================
#
# IMPORTANT:
# The email is used internally only.
# It is NOT displayed anywhere in the Streamlit UI.
#

NCBI_EMAIL = os.environ.get(
    "NCBI_EMAIL",
    "gshankar.bbaul@gmail.com",
)


# ==========================================================
# Inspect Button
# ==========================================================

inspect_clicked = st.button(
    "🔍 Inspect Dataset",
    type="primary",
    use_container_width=True,
)


# ==========================================================
# Inspection
# ==========================================================

if inspect_clicked:

    accession = accession.strip().upper()


    # ------------------------------------------------------
    # Input validation
    # ------------------------------------------------------

    if not accession:

        st.error(
            "Please enter an SRA accession number."
        )

        st.stop()


    # ------------------------------------------------------
    # Run inspection
    # ------------------------------------------------------

    with st.spinner(
        f"Retrieving dataset information for {accession}..."
    ):

        try:

            navigator = RNASeqNavigator(
                email=NCBI_EMAIL
            )

            result = navigator.inspect(
                accession
            )

        except Exception as exc:

            st.error(
                "RNASeq Navigator encountered an unexpected error."
            )

            st.exception(exc)

            st.stop()


    # ------------------------------------------------------
    # Inspection failure
    # ------------------------------------------------------

    if not result.success:

        st.error(
            f"RNASeq Navigator could not inspect {accession}."
        )

        if result.error:

            st.code(
                str(result.error)
            )

        st.stop()


    # ------------------------------------------------------
    # Success
    # ------------------------------------------------------

    st.success(
        f"Dataset information retrieved for {accession}"
    )


    # ======================================================
    # Extract objects
    # ======================================================

    report = result.report

    metadata = result.metadata

    normalization = result.normalization

    validation = result.validation


    # ======================================================
    # Dataset Overview
    # ======================================================

    render_section_title(
        "Dataset Overview",
        "Basic identity and biological information.",
    )


    # ------------------------------------------------------
    # Accession handling
    # ------------------------------------------------------

    run = get_value(
        report,
        "run",
        None,
    )

    if run is None:
        run = get_value(
            report,
            "experiment",
            accession,
        )


    study = get_value(
        report,
        "study",
    )

    experiment = get_value(
        report,
        "experiment",
    )

    organism = get_value(
        report,
        "organism",
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Run",
            clean_ui_value(run),
        )


    with col2:

        st.metric(
            "Study",
            clean_ui_value(study),
        )


    with col3:

        st.metric(
            "Experiment",
            clean_ui_value(experiment),
        )


    with col4:

        st.metric(
            "Organism",
            clean_ui_value(organism),
        )


    # ======================================================
    # Dataset Identity
    # ======================================================

    render_section_title(
        "Dataset Identity"
    )


    project = get_value(
        report,
        "project",
    )


    # ------------------------------------------------------
    # BioSample
    # ------------------------------------------------------

    sample = "—"

    if metadata is not None:

        sample_object = get_value(
            metadata,
            "sample",
            None,
        )

        sample = get_value(
            sample_object,
            "accession",
        )


    col1, col2 = st.columns(2)


    with col1:

        render_field(
            "Input / Run accession",
            run,
            accession=True,
        )

        render_field(
            "Study accession",
            study,
            accession=True,
        )

        render_field(
            "Experiment accession",
            experiment,
            accession=True,
        )


    with col2:

        render_field(
            "BioProject",
            project,
            accession=True,
        )

        render_field(
            "BioSample",
            sample,
            accession=True,
        )

        render_field(
            "Organism",
            organism,
        )


    # ======================================================
    # Experiment Information
    # ======================================================

    render_section_title(
        "Experiment Information",
        "Information describing the sequencing experiment.",
    )


    title = get_value(
        report,
        "title",
    )

    strategy = get_value(
        report,
        "strategy",
    )

    layout = get_value(
        report,
        "layout",
    )

    sequencing_description = get_value(
        report,
        "sequencing",
    )


    col1, col2 = st.columns(2)


    with col1:

        render_field(
            "Experiment title",
            title,
            long=True,
        )

        render_field(
            "Library strategy",
            strategy,
        )


    with col2:

        render_field(
            "Layout",
            layout,
        )

        render_field(
            "Sequencing description",
            sequencing_description,
            long=True,
        )


    # ======================================================
    # Sequencing Information
    # ======================================================

    render_section_title(
        "Sequencing Information"
    )


    platform = get_value(
        report,
        "platform",
    )

    instrument = get_value(
        report,
        "instrument",
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Platform",
            clean_ui_value(platform),
        )


    with col2:

        st.metric(
            "Instrument",
            clean_ui_value(instrument),
        )


    with col3:

        st.metric(
            "Layout",
            clean_ui_value(layout),
        )


    # ======================================================
    # Dataset Statistics
    # ======================================================

    render_section_title(
        "Dataset Statistics",
        "Sequencing statistics reported for the run.",
    )


    total_spots = get_value(
        report,
        "total_spots",
        None,
    )

    total_bases = get_value(
        report,
        "total_bases",
        None,
    )


    # ------------------------------------------------------
    # Public status
    # ------------------------------------------------------

    public = "—"

    if metadata is not None:

        run_object = get_value(
            metadata,
            "run",
            None,
        )

        public_value = get_value(
            run_object,
            "public",
            None,
        )

        if public_value is not None:

            if isinstance(
                public_value,
                bool,
            ):

                public = (
                    "Yes"
                    if public_value
                    else "No"
                )

            else:

                public = str(
                    public_value
                )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Reads / Spots",
            format_number(total_spots),
        )


    with col2:

        st.metric(
            "Bases",
            format_number(total_bases),
        )


    with col3:

        st.metric(
            "Public",
            clean_ui_value(public),
        )


    # ======================================================
    # Metadata Quality
    # ======================================================

    render_section_title(
        "Metadata Quality",
        "Information produced by the validation and normalization layers.",
    )


    validation_score = get_value(
        report,
        "validation_score",
        None,
    )

    normalization_changes = get_value(
        report,
        "normalization_changes",
        None,
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "Validation"
        )

        st.metric(
            "Validation score",
            (
                clean_ui_value(validation_score)
                if validation_score is not None
                else "—"
            ),
        )

        if validation is not None:

            issues = get_value(
                validation,
                "issues",
                None,
            )

            if issues is not None:

                try:
                    issue_count = len(issues)
                except TypeError:
                    issue_count = 0

                st.write(
                    f"Issues reported: {issue_count}"
                )


    with col2:

        st.subheader(
            "Normalization"
        )

        st.metric(
            "Normalization changes",
            (
                clean_ui_value(normalization_changes)
                if normalization_changes is not None
                else "—"
            ),
        )


    # ======================================================
    # Dataset Report
    # ======================================================

    render_section_title(
        "Dataset Report",
        "Integrated information available from the reporting layer.",
    )


    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    summary = get_value(
        report,
        "summary",
        "",
    )

    if summary:

        st.subheader(
            "Summary"
        )

        st.markdown(
            f"""
            <div class="report-text">
                {escape(clean_ui_value(summary))}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ------------------------------------------------------
    # Sequencing interpretation
    # ------------------------------------------------------

    sequencing = get_value(
        report,
        "sequencing",
        "",
    )

    if sequencing:

        st.subheader(
            "Sequencing interpretation"
        )

        st.markdown(
            f"""
            <div class="report-text">
                {escape(clean_ui_value(sequencing))}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ------------------------------------------------------
    # Strengths
    # ------------------------------------------------------

    strengths = get_value(
        report,
        "strengths",
        [],
    )

    if strengths:

        st.subheader(
            "Strengths"
        )

        for strength in strengths:

            st.markdown(
                f"- {escape(clean_ui_value(strength))}",
                unsafe_allow_html=True,
            )


    # ------------------------------------------------------
    # Limitations
    # ------------------------------------------------------

    limitations = get_value(
        report,
        "limitations",
        [],
    )

    if limitations:

        st.subheader(
            "Limitations"
        )

        for limitation in limitations:

            st.markdown(
                f"- {escape(clean_ui_value(limitation))}",
                unsafe_allow_html=True,
            )


    # ======================================================
    # Structured Metadata
    # ======================================================

    with st.expander(
        "View structured metadata"
    ):

        metadata_dict = object_to_dict(
            metadata
        )

        st.json(
            metadata_dict
        )


    # ======================================================
    # Normalization Details
    # ======================================================

    with st.expander(
        "View normalization details"
    ):

        normalization_dict = object_to_dict(
            normalization
        )

        st.json(
            normalization_dict
        )


    # ======================================================
    # Validation Details
    # ======================================================

    with st.expander(
        "View validation details"
    ):

        validation_dict = object_to_dict(
            validation
        )

        st.json(
            validation_dict
        )


    # ======================================================
    # Complete Inspection Result
    # ======================================================

    with st.expander(
        "View complete inspection result"
    ):

        result_dict = object_to_dict(
            result
        )

        st.json(
            result_dict
        )


    # ======================================================
    # Export
    # ======================================================

    render_section_title(
        "Export"
    )


    result_dict = object_to_dict(
        result
    )


    # ------------------------------------------------------
    # JSON
    # ------------------------------------------------------

    json_data = json.dumps(
        result_dict,
        indent=2,
        ensure_ascii=False,
        default=str,
    )


    col1, col2 = st.columns(2)


    with col1:

        st.download_button(
            label="⬇️ Download inspection result (JSON)",
            data=json_data,
            file_name=f"{accession}_inspection.json",
            mime="application/json",
            use_container_width=True,
        )


    # ------------------------------------------------------
    # PDF
    # ------------------------------------------------------

    with col2:

        try:

            pdf_data = build_pdf(
                result,
                accession,
            )

            st.download_button(
                label="⬇️ Download inspection report (PDF)",
                data=pdf_data,
                file_name=f"{accession}_inspection.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except RuntimeError as exc:

            st.warning(
                str(exc)
            )

        except Exception:

            st.error(
                "PDF report could not be generated."
            )


# ==========================================================
# Initial State
# ==========================================================

else:

    st.info(
        "Enter an SRA accession above and click "
        "'Inspect Dataset' to begin."
    )
