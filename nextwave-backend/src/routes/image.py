from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from src.models.user import db, User
from src.models.image import Image, ImageAnalysisResult
from src.models.processing import ProcessingTask
import os
import uuid
from datetime import datetime
import mimetypes
from PIL import Image as PILImage
import cv2
import numpy as np

image_bp = Blueprint('image', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image_basic(image_path):
    """Basic image analysis using OpenCV and PIL"""
    try:
        # Load image with PIL for basic info
        pil_image = PILImage.open(image_path)
        width, height = pil_image.size
        format_name = pil_image.format
        
        # Load image with OpenCV for analysis
        cv_image = cv2.imread(image_path)
        
        # Basic characteristics
        characteristics = {
            'dimensions': {'width': width, 'height': height},
            'format': format_name,
            'aspect_ratio': round(width / height, 2),
            'total_pixels': width * height
        }
        
        if cv_image is not None:
            # Color analysis
            mean_color = cv_image.mean(axis=(0, 1))
            characteristics['average_color'] = {
                'blue': int(mean_color[0]),
                'green': int(mean_color[1]),
                'red': int(mean_color[2])
            }
            
            # Brightness analysis
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            brightness = gray.mean()
            characteristics['brightness'] = round(brightness, 2)
            
            # Edge detection for complexity
            edges = cv2.Canny(gray, 50, 150)
            edge_density = (edges > 0).sum() / (width * height)
            characteristics['edge_density'] = round(edge_density, 4)
        
        # Generate description
        description = f"Image with dimensions {width}x{height} pixels"
        if 'brightness' in characteristics:
            if characteristics['brightness'] > 150:
                description += ", bright lighting"
            elif characteristics['brightness'] < 100:
                description += ", dark/low lighting"
            else:
                description += ", moderate lighting"
        
        if 'edge_density' in characteristics:
            if characteristics['edge_density'] > 0.1:
                description += ", high detail/complexity"
            elif characteristics['edge_density'] < 0.05:
                description += ", low detail/simple"
            else:
                description += ", moderate detail"
        
        return description, characteristics, 0.85  # Mock confidence score
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}", {}, 0.0

@image_bp.route('/', methods=['GET'])
@jwt_required()
def get_images():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        query = Image.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        images = query.order_by(Image.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'images': [img.to_dict() for img in images.items],
            'total': images.total,
            'pages': images.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@image_bp.route('/', methods=['POST'])
@jwt_required()
def upload_image():
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Save file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get image info
        try:
            pil_image = PILImage.open(file_path)
            width, height = pil_image.size
            format_name = pil_image.format
        except Exception:
            width = height = None
            format_name = None
        
        file_size = os.path.getsize(file_path)
        
        # Create image record
        image = Image(
            user_id=user_id,
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            width=width,
            height=height,
            format=format_name
        )
        
        db.session.add(image)
        db.session.commit()
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'image': image.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@image_bp.route('/<int:image_id>/analyze', methods=['POST'])
@jwt_required()
def analyze_image(image_id):
    try:
        user_id = get_jwt_identity()
        image = Image.query.filter_by(id=image_id, user_id=user_id).first()
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        if not os.path.exists(image.file_path):
            return jsonify({'error': 'Image file not found on disk'}), 404
        
        # Update image status
        image.status = 'analyzing'
        db.session.commit()
        
        # Perform analysis
        description, characteristics, confidence = analyze_image_basic(image.file_path)
        
        # Create analysis result
        analysis_result = ImageAnalysisResult(
            image_id=image_id,
            description=description,
            confidence_score=confidence,
            analysis_model='basic_opencv_pil'
        )
        analysis_result.set_characteristics(characteristics)
        
        # Update image status
        image.status = 'analyzed'
        image.analyzed_at = datetime.utcnow()
        
        db.session.add(analysis_result)
        db.session.commit()
        
        return jsonify({
            'message': 'Image analysis completed',
            'analysis': analysis_result.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        image.status = 'error'
        db.session.commit()
        return jsonify({'error': str(e)}), 500

@image_bp.route('/<int:image_id>/analysis', methods=['GET'])
@jwt_required()
def get_image_analysis(image_id):
    try:
        user_id = get_jwt_identity()
        image = Image.query.filter_by(id=image_id, user_id=user_id).first()
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        analysis_results = ImageAnalysisResult.query.filter_by(image_id=image_id).all()
        
        return jsonify({
            'image': image.to_dict(),
            'analysis_results': [result.to_dict() for result in analysis_results]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@image_bp.route('/<int:image_id>', methods=['DELETE'])
@jwt_required()
def delete_image(image_id):
    try:
        user_id = get_jwt_identity()
        image = Image.query.filter_by(id=image_id, user_id=user_id).first()
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        # Delete file from disk
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
        
        # Delete image record (analysis results will be deleted by cascade)
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({'message': 'Image deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

