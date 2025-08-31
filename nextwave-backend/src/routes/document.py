from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from src.models.user import db, User
from src.models.document import Document, DocumentVersion
from src.models.processing import ProcessingTask
import os
import uuid
from datetime import datetime
import mimetypes

document_bp = Blueprint('document', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'vsd', 'vsdx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_document_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return 'pdf'
    elif ext in ['doc', 'docx']:
        return 'word'
    elif ext in ['vsd', 'vsdx']:
        return 'visio'
    else:
        return 'other'

@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_documents():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        document_type = request.args.get('type')
        status = request.args.get('status')
        
        query = Document.query.filter_by(user_id=user_id)
        
        if document_type:
            query = query.filter_by(document_type=document_type)
        
        if status:
            query = query.filter_by(status=status)
        
        documents = query.order_by(Document.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'documents': [doc.to_dict() for doc in documents.items],
            'total': documents.total,
            'pages': documents.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@document_bp.route('/', methods=['POST'])
@jwt_required()
def upload_document():
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
        
        # Get file info
        file_size = os.path.getsize(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        document_type = get_document_type(original_filename)
        
        # Create document record
        document = Document(
            user_id=user_id,
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            document_type=document_type
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': document.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    try:
        user_id = get_jwt_identity()
        document = Document.query.filter_by(id=document_id, user_id=user_id).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Delete file from disk
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete document record
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@document_bp.route('/<int:document_id>/process', methods=['POST'])
@jwt_required()
def process_document(document_id):
    try:
        user_id = get_jwt_identity()
        document = Document.query.filter_by(id=document_id, user_id=user_id).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        data = request.get_json()
        task_type = data.get('task_type')
        
        if not task_type:
            return jsonify({'error': 'Task type is required'}), 400
        
        # Create processing task
        task = ProcessingTask(
            user_id=user_id,
            task_type=task_type,
            source_file_id=document_id,
            status='pending'
        )
        
        if data.get('parameters'):
            task.set_parameters(data['parameters'])
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Processing task created',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

