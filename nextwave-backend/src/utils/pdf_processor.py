import os
import io
import time
import PyPDF2
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import fitz  # PyMuPDF for advanced PDF operations

class PDFProcessor:
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'doc', 'txt']
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF file"""
        try:
            text_content = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content.append({
                        'page': page_num + 1,
                        'text': page.extract_text()
                    })
            return {
                'success': True,
                'content': text_content,
                'total_pages': len(text_content)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def pdf_to_images(self, pdf_path, output_dir, dpi=150):
        """Convert PDF pages to images"""
        try:
            doc = fitz.open(pdf_path)
            images = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                mat = fitz.Matrix(dpi/72, dpi/72)
                pix = page.get_pixmap(matrix=mat)
                
                img_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
                pix.save(img_path)
                images.append({
                    'page': page_num + 1,
                    'image_path': img_path,
                    'width': pix.width,
                    'height': pix.height
                })
            
            doc.close()
            return {
                'success': True,
                'images': images,
                'total_pages': len(images)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def merge_pdfs(self, pdf_paths, output_path):
        """Merge multiple PDF files into one"""
        try:
            pdf_writer = PyPDF2.PdfWriter()
            
            for pdf_path in pdf_paths:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return {
                'success': True,
                'output_path': output_path,
                'total_files_merged': len(pdf_paths)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def split_pdf(self, pdf_path, output_dir, pages_per_split=1):
        """Split PDF into multiple files"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                split_files = []
                for i in range(0, total_pages, pages_per_split):
                    pdf_writer = PyPDF2.PdfWriter()
                    
                    end_page = min(i + pages_per_split, total_pages)
                    for page_num in range(i, end_page):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)
                    
                    output_filename = f'split_{i//pages_per_split + 1}.pdf'
                    output_path = os.path.join(output_dir, output_filename)
                    
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    
                    split_files.append({
                        'filename': output_filename,
                        'path': output_path,
                        'pages': f'{i+1}-{end_page}'
                    })
            
            return {
                'success': True,
                'split_files': split_files,
                'total_splits': len(split_files)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_watermark(self, pdf_path, watermark_text, output_path, opacity=0.3):
        """Add watermark to PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get page dimensions
                rect = page.rect
                
                # Add watermark text
                text_rect = fitz.Rect(50, rect.height - 100, rect.width - 50, rect.height - 50)
                page.insert_textbox(
                    text_rect,
                    watermark_text,
                    fontsize=36,
                    color=(0.5, 0.5, 0.5),
                    overlay=True
                )
            
            doc.save(output_path)
            doc.close()
            
            return {
                'success': True,
                'output_path': output_path,
                'watermark_text': watermark_text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_report_pdf(self, title, content, images=None, output_path=None):
        """Create a formatted PDF report"""
        try:
            if not output_path:
                output_path = f"report_{int(time.time())}.pdf"
            
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=HexColor('#2563eb'),
                alignment=1  # Center alignment
            )
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Content sections
            for section in content:
                if section.get('type') == 'heading':
                    heading_style = ParagraphStyle(
                        'CustomHeading',
                        parent=styles['Heading2'],
                        fontSize=16,
                        spaceAfter=12,
                        textColor=HexColor('#1f2937')
                    )
                    story.append(Paragraph(section['text'], heading_style))
                
                elif section.get('type') == 'paragraph':
                    para_style = ParagraphStyle(
                        'CustomParagraph',
                        parent=styles['Normal'],
                        fontSize=12,
                        spaceAfter=12,
                        textColor=HexColor('#374151')
                    )
                    story.append(Paragraph(section['text'], para_style))
                
                elif section.get('type') == 'list':
                    for item in section['items']:
                        bullet_style = ParagraphStyle(
                            'BulletPoint',
                            parent=styles['Normal'],
                            fontSize=11,
                            leftIndent=20,
                            bulletIndent=10,
                            spaceAfter=6
                        )
                        story.append(Paragraph(f"• {item}", bullet_style))
            
            # Add images if provided
            if images:
                story.append(Spacer(1, 20))
                story.append(Paragraph("Images", styles['Heading2']))
                
                for img_path in images:
                    if os.path.exists(img_path):
                        img = RLImage(img_path, width=4*inch, height=3*inch)
                        story.append(img)
                        story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            return {
                'success': True,
                'output_path': output_path,
                'title': title
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Utility functions for document conversion
def convert_docx_to_pdf(docx_path, output_path):
    """Convert DOCX to PDF (placeholder - requires python-docx and additional libraries)"""
    # This would require additional libraries like python-docx and pandoc
    # For now, return a placeholder response
    return {
        'success': False,
        'error': 'DOCX to PDF conversion requires additional setup'
    }

def convert_pdf_to_docx(pdf_path, output_path):
    """Convert PDF to DOCX (placeholder - requires additional libraries)"""
    # This would require libraries like pdf2docx
    # For now, return a placeholder response
    return {
        'success': False,
        'error': 'PDF to DOCX conversion requires additional setup'
    }

