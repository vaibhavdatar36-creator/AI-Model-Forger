from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas that accumulates all pages to compute the true total page count
    and renders academic running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Suppress header and footer on cover page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))

        # Running Header
        header_text = "D.K.T.E. Society's Textile and Engineering Institute, Ichalkaranji | Department of CSE"
        self.drawString(54, 804, header_text)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(541, 804, "AI Model Forge: Universal Multimodal AutoML Platform")

        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 796, 541, 796)

        # Running Footer
        self.line(54, 46, 541, 46)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 34, "AI Tools for Software Development Project Report | Shivaji University, Kolhapur")
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#1e293b"))
        self.drawRightString(541, 34, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()

def setup_academic_styles():
    base_styles = getSampleStyleSheet()

    styles = {
        'CoverInstitution': ParagraphStyle(
            'CoverInstitution',
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            alignment=1, # Center
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=4
        ),
        'CoverSubInstitution': ParagraphStyle(
            'CoverSubInstitution',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            alignment=1,
            textColor=colors.HexColor('#334155'),
            spaceAfter=3
        ),
        'CoverDept': ParagraphStyle(
            'CoverDept',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            alignment=1,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=4
        ),
        'CoverYear': ParagraphStyle(
            'CoverYear',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            alignment=1,
            textColor=colors.HexColor('#475569'),
            spaceAfter=15
        ),
        'CoverType': ParagraphStyle(
            'CoverType',
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            alignment=1,
            textColor=colors.HexColor('#d97706'), # Gold accent
            spaceAfter=10
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=23,
            alignment=1,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=12
        ),
        'CoverTagline': ParagraphStyle(
            'CoverTagline',
            fontName='Helvetica-Oblique',
            fontSize=10.5,
            leading=15,
            alignment=1,
            textColor=colors.HexColor('#475569'),
            spaceAfter=20
        ),
        'CoverLabel': ParagraphStyle(
            'CoverLabel',
            fontName='Helvetica-Bold',
            fontSize=10.5,
            leading=14,
            alignment=1,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=4
        ),
        'CoverSignerName': ParagraphStyle(
            'CoverSignerName',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            alignment=1,
            textColor=colors.HexColor('#0f172a')
        ),
        'CoverSignerRole': ParagraphStyle(
            'CoverSignerRole',
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            alignment=1,
            textColor=colors.HexColor('#475569')
        ),
        # Document Headings
        'ChapterHeader': ParagraphStyle(
            'ChapterHeader',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=23,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=12,
            spaceAfter=10,
            keepWithNext=True
        ),
        'SectionHeader': ParagraphStyle(
            'SectionHeader',
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            textColor=colors.HexColor('#1e3a8a'), # Navy blue
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True
        ),
        'SubSectionHeader': ParagraphStyle(
            'SubSectionHeader',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#334155'),
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        ),
        'Paragraph': ParagraphStyle(
            'Paragraph',
            fontName='Helvetica',
            fontSize=10,
            leading=14.5,
            textColor=colors.HexColor('#1e293b'),
            alignment=4, # Justified
            spaceAfter=7
        ),
        'ParagraphBold': ParagraphStyle(
            'ParagraphBold',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14.5,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        ),
        'BulletItem': ParagraphStyle(
            'BulletItem',
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#1e293b'),
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4
        ),
        'CodeBlock': ParagraphStyle(
            'CodeBlock',
            fontName='Courier',
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor('#0f172a'),
            leftIndent=10,
            rightIndent=10,
            spaceBefore=4,
            spaceAfter=6
        ),
        'TableHead': ParagraphStyle(
            'TableHead',
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.white,
            alignment=0
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            fontName='Helvetica',
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor('#1e293b'),
            alignment=0
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold',
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor('#0f172a'),
            alignment=0
        ),
        'PromptBoxLabel': ParagraphStyle(
            'PromptBoxLabel',
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#1e3a8a')
        ),
        'PromptBoxContent': ParagraphStyle(
            'PromptBoxContent',
            fontName='Courier',
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor('#1e293b')
        ),
        'CalloutTitle': ParagraphStyle(
            'CalloutTitle',
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=2
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText',
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#334155')
        )
    }
    return styles

def create_callout_box(title: str, text: str, styles, width=487):
    content = [
        Paragraph(title, styles['CalloutTitle']),
        Paragraph(text, styles['CalloutText'])
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t

def create_prompt_box(prompt_title: str, prompt_text: str, response_summary: str, styles, width=487):
    data = [
        [Paragraph(f"<b>ENGINEERING PROMPT:</b> {prompt_title}", styles['PromptBoxLabel'])],
        [Paragraph(prompt_text, styles['PromptBoxContent'])],
        [Paragraph(f"<b>AI REASONING & OUTPUT:</b> {response_summary}", styles['TableCell'])]
    ]
    t = Table(data, colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e7ff')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#faf5ff')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t
