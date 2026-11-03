import os
import sys
from pathlib import Path
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

# Add report_sections to sys.path
docs_dir = Path(__file__).resolve().parent
if str(docs_dir) not in sys.path:
    sys.path.insert(0, str(docs_dir))

from report_sections.styles_and_canvas import setup_academic_styles, NumberedCanvas
from report_sections.cover_and_prelims import (
    generate_cover_page,
    generate_certificate_page,
    generate_acknowledgements_and_abstract,
    generate_index_page
)
from report_sections.ch1_introduction import generate_ch1
from report_sections.ch2_requirements import generate_ch2
from report_sections.ch3_system_design import generate_ch3
from report_sections.ch4_coding_implementation import generate_ch4
from report_sections.ch5_testing import generate_ch5
from report_sections.ch6_deployment_docs import generate_ch6
from report_sections.ch7_references import generate_ch7
from report_sections.ch8_appendices import generate_ch8

def build_pdf(output_pdf_path: Path):
    logo_path = docs_dir / "extracted_template" / "image1.png"
    styles = setup_academic_styles()

    # Document setup: A4, 54pt (0.75 in) margins
    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    story = []

    # 1. Preliminaries (Pages 1-5)
    story.extend(generate_cover_page(styles, logo_path))
    story.extend(generate_certificate_page(styles))
    story.extend(generate_acknowledgements_and_abstract(styles))
    story.extend(generate_index_page(styles))

    # 2. Main Chapters
    story.extend(generate_ch1(styles))
    story.extend(generate_ch2(styles))
    story.extend(generate_ch3(styles))
    story.extend(generate_ch4(styles))
    story.extend(generate_ch5(styles))
    story.extend(generate_ch6(styles))
    story.extend(generate_ch7(styles))
    story.extend(generate_ch8(styles))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)

    # Verify actual page count with PyPDF
    reader = PdfReader(str(output_pdf_path))
    actual_pages = len(reader.pages)
    print(f"PDF successfully built: {output_pdf_path}")
    print(f"Total Page Count: {actual_pages} pages")
    return actual_pages

if __name__ == "__main__":
    pdf_out = docs_dir / "AI_Tools_Project_Report_DKTE_AI_Model_Forge.pdf"
    pages = build_pdf(pdf_out)
