from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import uuid

from models.user import User
from models.document import Document
from models.image import ImageAnalysis
from models.processing import ProcessingTask, Report
from utils.pdf_processor import PDFProcessor
from utils.image_analyzer import ImageAnalyzer

advanced_bp = Blueprint('advanced', __name__)
pdf_processor = PDFProcessor()
image_analyzer = ImageAnalyzer()

@advanced_bp.route('/pdf/merge', methods=['POST'])
@jwt_required()
def merge_pdfs():
    """Merge multiple PDF files into one"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        document_ids = data.get('document_ids', [])
        
        if len(document_ids) < 2:
            return jsonify({'error': 'At least 2 documents required for merging'}), 400
        
        # Get documents
        documents = Document.query.filter(
            Document.id.in_(document_ids),
            Document.user_id == current_user_id
        ).all()
        
        if len(documents) != len(document_ids):
            return jsonify({'error': 'Some documents not found'}), 404
        
        # Create processing task
        task = ProcessingTask(
            task_type='pdf_merge',
            status='processing',
            input_data={'document_ids': document_ids},
            user_id=current_user_id
        )
        
        from models.user import db
        db.session.add(task)
        db.session.commit()
        
        # Merge PDFs
        pdf_paths = [doc.file_path for doc in documents]
        output_filename = f"merged_{int(datetime.now().timestamp())}.pdf"
        output_path = os.path.join('uploads', 'documents', output_filename)
        
        result = pdf_processor.merge_pdfs(pdf_paths, output_path)
        
        if result.get('success'):
            # Create new document record
            merged_doc = Document(
                filename=output_filename,
                original_filename=f"merged_{len(documents)}_files.pdf",
                file_path=output_path,
                file_size=os.path.getsize(output_path),
                mime_type='application/pdf',
                user_id=current_user_id
            )
            
            db.session.add(merged_doc)
            
            # Update task
            task.status = 'completed'
            task.output_data = {
                'merged_document_id': merged_doc.id,
                'original_count': len(documents)
            }
            task.completed_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({
                'message': 'PDFs merged successfully',
                'task_id': task.id,
                'document_id': merged_doc.id,
                'download_url': f'/api/documents/{merged_doc.id}/download'
            })
        else:
            task.status = 'failed'
            task.output_data = result
            db.session.commit()
            return jsonify({'error': 'PDF merge failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/pdf/split', methods=['POST'])
@jwt_required()
def split_pdf():
    """Split PDF into multiple files"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        document_id = data.get('document_id')
        pages_per_split = data.get('pages_per_split', 1)
        
        document = Document.query.filter_by(id=document_id, user_id=current_user_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Create processing task
        task = ProcessingTask(
            task_type='pdf_split',
            status='processing',
            input_data={'document_id': document_id, 'pages_per_split': pages_per_split},
            user_id=current_user_id
        )
        
        from models.user import db
        db.session.add(task)
        db.session.commit()
        
        # Split PDF
        output_dir = os.path.join('uploads', 'documents', f'split_{document_id}')
        os.makedirs(output_dir, exist_ok=True)
        
        result = pdf_processor.split_pdf(document.file_path, output_dir, pages_per_split)
        
        if result.get('success'):
            # Create document records for split files
            split_documents = []
            for split_file in result['split_files']:
                split_doc = Document(
                    filename=split_file['filename'],
                    original_filename=f"split_{split_file['filename']}",
                    file_path=split_file['path'],
                    file_size=os.path.getsize(split_file['path']),
                    mime_type='application/pdf',
                    user_id=current_user_id
                )
                db.session.add(split_doc)
                split_documents.append({
                    'filename': split_file['filename'],
                    'pages': split_file['pages'],
                    'document_id': split_doc.id
                })
            
            # Update task
            task.status = 'completed'
            task.output_data = {
                'split_files': split_documents,
                'total_splits': len(split_documents)
            }
            task.completed_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({
                'message': 'PDF split successfully',
                'task_id': task.id,
                'split_files': split_documents
            })
        else:
            task.status = 'failed'
            task.output_data = result
            db.session.commit()
            return jsonify({'error': 'PDF split failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/pdf/watermark', methods=['POST'])
@jwt_required()
def add_watermark():
    """Add watermark to PDF"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        document_id = data.get('document_id')
        watermark_text = data.get('watermark_text', 'CONFIDENTIAL')
        opacity = data.get('opacity', 0.3)
        
        document = Document.query.filter_by(id=document_id, user_id=current_user_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Create processing task
        task = ProcessingTask(
            task_type='pdf_watermark',
            status='processing',
            input_data={'document_id': document_id, 'watermark_text': watermark_text},
            user_id=current_user_id
        )
        
        from models.user import db
        db.session.add(task)
        db.session.commit()
        
        # Add watermark
        output_filename = f"watermarked_{int(datetime.now().timestamp())}.pdf"
        output_path = os.path.join('uploads', 'documents', output_filename)
        
        result = pdf_processor.add_watermark(document.file_path, watermark_text, output_path, opacity)
        
        if result.get('success'):
            # Create new document record
            watermarked_doc = Document(
                filename=output_filename,
                original_filename=f"watermarked_{document.original_filename}",
                file_path=output_path,
                file_size=os.path.getsize(output_path),
                mime_type='application/pdf',
                user_id=current_user_id
            )
            
            db.session.add(watermarked_doc)
            
            # Update task
            task.status = 'completed'
            task.output_data = {
                'watermarked_document_id': watermarked_doc.id,
                'watermark_text': watermark_text
            }
            task.completed_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({
                'message': 'Watermark added successfully',
                'task_id': task.id,
                'document_id': watermarked_doc.id,
                'download_url': f'/api/documents/{watermarked_doc.id}/download'
            })
        else:
            task.status = 'failed'
            task.output_data = result
            db.session.commit()
            return jsonify({'error': 'Watermark addition failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/image/batch-analyze', methods=['POST'])
@jwt_required()
def batch_analyze_images():
    """Analyze multiple images in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        image_ids = data.get('image_ids', [])
        
        if not image_ids:
            return jsonify({'error': 'No images provided'}), 400
        
        # Get images
        images = ImageAnalysis.query.filter(
            ImageAnalysis.id.in_(image_ids),
            ImageAnalysis.user_id == current_user_id
        ).all()
        
        if len(images) != len(image_ids):
            return jsonify({'error': 'Some images not found'}), 404
        
        # Create processing task
        task = ProcessingTask(
            task_type='batch_image_analysis',
            status='processing',
            input_data={'image_ids': image_ids},
            user_id=current_user_id
        )
        
        from models.user import db
        db.session.add(task)
        db.session.commit()
        
        # Batch analyze
        image_paths = [img.file_path for img in images]
        result = image_analyzer.batch_analyze(image_paths)
        
        if result.get('success'):
            # Update task
            task.status = 'completed'
            task.output_data = result
            task.completed_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({
                'message': 'Batch analysis completed',
                'task_id': task.id,
                'results': result
            })
        else:
            task.status = 'failed'
            task.output_data = result
            db.session.commit()
            return jsonify({'error': 'Batch analysis failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/image/compare', methods=['POST'])
@jwt_required()
def compare_images():
    """Compare two images and generate comparison report"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        image1_id = data.get('image1_id')
        image2_id = data.get('image2_id')
        
        # Get images
        image1 = ImageAnalysis.query.filter_by(id=image1_id, user_id=current_user_id).first()
        image2 = ImageAnalysis.query.filter_by(id=image2_id, user_id=current_user_id).first()
        
        if not image1 or not image2:
            return jsonify({'error': 'One or both images not found'}), 404
        
        # Create processing task
        task = ProcessingTask(
            task_type='image_comparison',
            status='processing',
            input_data={'image1_id': image1_id, 'image2_id': image2_id},
            user_id=current_user_id
        )
        
        from models.user import db
        db.session.add(task)
        db.session.commit()
        
        # Compare images
        analysis1 = image1.analysis_data
        analysis2 = image2.analysis_data
        
        comparison_result = {
            'image1': {
                'filename': image1.filename,
                'analysis': analysis1
            },
            'image2': {
                'filename': image2.filename,
                'analysis': analysis2
            },
            'comparison': {
                'color_similarity': calculate_color_similarity(analysis1, analysis2),
                'size_comparison': compare_sizes(analysis1, analysis2),
                'brightness_difference': compare_brightness(analysis1, analysis2)
            }
        }
        
        # Generate comparison report
        report_filename = f"comparison_report_{int(datetime.now().timestamp())}.pdf"
        report_path = os.path.join('uploads', 'reports', report_filename)
        
        report_content = [
            {'type': 'heading', 'text': 'Image Comparison Report'},
            {'type': 'paragraph', 'text': f'Comparison between {image1.filename} and {image2.filename}'},
            {'type': 'heading', 'text': 'Analysis Results'},
            {'type': 'paragraph', 'text': f"Color similarity: {comparison_result['comparison']['color_similarity']:.2f}%"},
            {'type': 'paragraph', 'text': f"Size comparison: {comparison_result['comparison']['size_comparison']}"},
            {'type': 'paragraph', 'text': f"Brightness difference: {comparison_result['comparison']['brightness_difference']:.2f}"}
        ]
        
        pdf_result = pdf_processor.create_report_pdf(
            title="Image Comparison Report",
            content=report_content,
            output_path=report_path
        )
        
        if pdf_result.get('success'):
            # Create report record
            report = Report(
                title=f"Image Comparison: {image1.filename} vs {image2.filename}",
                report_type='image_comparison',
                file_path=report_path,
                generated_for_id=f"{image1_id},{image2_id}",
                user_id=current_user_id
            )
            
            db.session.add(report)
            
            # Update task
            task.status = 'completed'
            task.output_data = comparison_result
            task.completed_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({
                'message': 'Image comparison completed',
                'task_id': task.id,
                'comparison': comparison_result,
                'report_id': report.id,
                'download_url': f'/api/reports/{report.id}/download'
            })
        else:
            task.status = 'failed'
            task.output_data = {'error': 'Report generation failed'}
            db.session.commit()
            return jsonify({'error': 'Comparison report generation failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_color_similarity(analysis1, analysis2):
    """Calculate color similarity between two image analyses"""
    try:
        if 'color_analysis' not in analysis1 or 'color_analysis' not in analysis2:
            return 0.0
        
        color1 = analysis1['color_analysis'].get('average_color', {}).get('rgb', [0, 0, 0])
        color2 = analysis2['color_analysis'].get('average_color', {}).get('rgb', [0, 0, 0])
        
        # Calculate Euclidean distance
        distance = sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5
        max_distance = (255 ** 2 * 3) ** 0.5
        
        # Convert to similarity percentage
        similarity = (1 - distance / max_distance) * 100
        return max(0, similarity)
    except:
        return 0.0

def compare_sizes(analysis1, analysis2):
    """Compare sizes of two images"""
    try:
        size1 = analysis1.get('file_info', {}).get('dimensions', {})
        size2 = analysis2.get('file_info', {}).get('dimensions', {})
        
        if not size1 or not size2:
            return "Size information not available"
        
        area1 = size1.get('width', 0) * size1.get('height', 0)
        area2 = size2.get('width', 0) * size2.get('height', 0)
        
        if area1 > area2:
            ratio = area1 / area2 if area2 > 0 else 1
            return f"Image 1 is {ratio:.2f}x larger"
        elif area2 > area1:
            ratio = area2 / area1 if area1 > 0 else 1
            return f"Image 2 is {ratio:.2f}x larger"
        else:
            return "Images are the same size"
    except:
        return "Size comparison failed"

def compare_brightness(analysis1, analysis2):
    """Compare brightness of two images"""
    try:
        brightness1 = analysis1.get('brightness_contrast', {}).get('brightness', 0)
        brightness2 = analysis2.get('brightness_contrast', {}).get('brightness', 0)
        
        return abs(brightness1 - brightness2)
    except:
        return 0.0

