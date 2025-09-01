from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
import uuid
import logging
from functools import wraps

# Import our models and utilities
from models.user import User, db
from models.document import Document
from models.image import ImageAnalysis
from models.workflow import WorkflowModel
from models.processing import ProcessingTask, Report
from utils.pdf_processor import PDFProcessor
from utils.image_analyzer import ImageAnalyzer
from utils.workflow_engine import WorkflowEngine

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nextwave-secret-key-2024'
app.config['JWT_SECRET_KEY'] = 'nextwave-jwt-secret-2024'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nextwave.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Initialize extensions
CORS(app, origins="*")
jwt = JWTManager(app)
db.init_app(app)

# Initialize utilities
pdf_processor = PDFProcessor()
image_analyzer = ImageAnalyzer()
workflow_engine = WorkflowEngine()

# Create upload directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'reports'), exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Admin required decorator
def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            role='user'
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Update last login
        user.last_login = datetime.now()
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        })
        
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile'}), 500

# Document Processing Routes
@app.route('/api/documents/upload', methods=['POST'])
@jwt_required()
def upload_document():
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'documents', filename)
        file.save(file_path)
        
        # Create document record
        document = Document(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            mime_type=file.content_type,
            user_id=current_user_id
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Create processing task
        task = ProcessingTask(
            task_type='document_upload',
            status='completed',
            input_data={'document_id': document.id},
            user_id=current_user_id
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': {
                'id': document.id,
                'filename': document.filename,
                'file_size': document.file_size,
                'uploaded_at': document.uploaded_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        return jsonify({'error': 'Document upload failed'}), 500

@app.route('/api/documents/<int:document_id>/process', methods=['POST'])
@jwt_required()
def process_document(document_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        operation = data.get('operation', 'extract_text')
        
        document = Document.query.filter_by(id=document_id, user_id=current_user_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Create processing task
        task = ProcessingTask(
            task_type='document_processing',
            status='processing',
            input_data={'document_id': document_id, 'operation': operation},
            user_id=current_user_id
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Process document based on operation
        if operation == 'extract_text':
            result = pdf_processor.extract_text_from_pdf(document.file_path)
        elif operation == 'convert_to_images':
            output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images', str(document_id))
            os.makedirs(output_dir, exist_ok=True)
            result = pdf_processor.pdf_to_images(document.file_path, output_dir)
        else:
            result = {'success': False, 'error': 'Unknown operation'}
        
        # Update task status
        task.status = 'completed' if result.get('success') else 'failed'
        task.output_data = result
        task.completed_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Document processing completed',
            'task_id': task.id,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        return jsonify({'error': 'Document processing failed'}), 500

# Image Analysis Routes
@app.route('/api/images/upload', methods=['POST'])
@jwt_required()
def upload_image():
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename)
        file.save(file_path)
        
        # Analyze image
        analysis_result = image_analyzer.analyze_image(file_path)
        
        # Create image analysis record
        image_analysis = ImageAnalysis(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            analysis_data=analysis_result,
            user_id=current_user_id
        )
        
        db.session.add(image_analysis)
        db.session.commit()
        
        return jsonify({
            'message': 'Image uploaded and analyzed successfully',
            'image': {
                'id': image_analysis.id,
                'filename': image_analysis.filename,
                'analysis': analysis_result
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Image upload error: {str(e)}")
        return jsonify({'error': 'Image upload failed'}), 500

@app.route('/api/images/<int:image_id>/report', methods=['POST'])
@jwt_required()
def generate_image_report(image_id):
    try:
        current_user_id = get_jwt_identity()
        
        image_analysis = ImageAnalysis.query.filter_by(id=image_id, user_id=current_user_id).first()
        if not image_analysis:
            return jsonify({'error': 'Image not found'}), 404
        
        # Generate report
        report_filename = f"image_report_{image_id}_{int(datetime.now().timestamp())}.pdf"
        report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'reports', report_filename)
        
        # Create report content
        report_content = [
            {'type': 'heading', 'text': f'Image Analysis Report: {image_analysis.filename}'},
            {'type': 'paragraph', 'text': f'Analysis Date: {image_analysis.analyzed_at.strftime("%Y-%m-%d %H:%M:%S")}'},
            {'type': 'heading', 'text': 'Analysis Results'},
            {'type': 'paragraph', 'text': image_analysis.analysis_data.get('description', 'No description available')}
        ]
        
        # Add characteristics if available
        if 'color_analysis' in image_analysis.analysis_data:
            color_data = image_analysis.analysis_data['color_analysis']
            report_content.append({'type': 'heading', 'text': 'Color Analysis'})
            report_content.append({'type': 'paragraph', 'text': f"Dominant colors detected with color variance of {color_data.get('color_variance', 'N/A')}"})
        
        result = pdf_processor.create_report_pdf(
            title=f"Image Analysis Report",
            content=report_content,
            output_path=report_path
        )
        
        if result.get('success'):
            # Create report record
            report = Report(
                title=f"Image Analysis Report - {image_analysis.filename}",
                report_type='image_analysis',
                file_path=report_path,
                generated_for_id=image_id,
                user_id=current_user_id
            )
            
            db.session.add(report)
            db.session.commit()
            
            return jsonify({
                'message': 'Report generated successfully',
                'report_id': report.id,
                'download_url': f'/api/reports/{report.id}/download'
            })
        else:
            return jsonify({'error': 'Report generation failed'}), 500
        
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        return jsonify({'error': 'Report generation failed'}), 500

# Workflow Routes
@app.route('/api/workflows', methods=['GET'])
@jwt_required()
def list_workflows():
    try:
        workflows = workflow_engine.list_workflows()
        return jsonify({'workflows': workflows})
    except Exception as e:
        logger.error(f"List workflows error: {str(e)}")
        return jsonify({'error': 'Failed to list workflows'}), 500

@app.route('/api/workflows', methods=['POST'])
@jwt_required()
def create_workflow():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Workflow name is required'}), 400
        
        # Create workflow in engine
        workflow = workflow_engine.create_workflow(name, description)
        
        # Create database record
        workflow_model = WorkflowModel(
            workflow_id=workflow.id,
            name=name,
            description=description,
            definition=workflow.to_dict(),
            user_id=current_user_id
        )
        
        db.session.add(workflow_model)
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow created successfully',
            'workflow': workflow.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Create workflow error: {str(e)}")
        return jsonify({'error': 'Failed to create workflow'}), 500

@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
@jwt_required()
def execute_workflow(workflow_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        input_data = data.get('input_data', {})
        
        # Execute workflow
        execution = workflow_engine.execute_workflow(workflow_id, input_data)
        
        return jsonify({
            'message': 'Workflow execution started',
            'execution_id': execution.execution_id,
            'status': execution.status.value
        })
        
    except Exception as e:
        logger.error(f"Execute workflow error: {str(e)}")
        return jsonify({'error': 'Failed to execute workflow'}), 500

@app.route('/api/workflows/executions/<execution_id>', methods=['GET'])
@jwt_required()
def get_execution_status(execution_id):
    try:
        execution = workflow_engine.get_execution(execution_id)
        if not execution:
            return jsonify({'error': 'Execution not found'}), 404
        
        return jsonify({'execution': execution.to_dict()})
        
    except Exception as e:
        logger.error(f"Get execution error: {str(e)}")
        return jsonify({'error': 'Failed to get execution status'}), 500

# Admin Routes
@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_admin_stats():
    try:
        stats = {
            'total_users': User.query.count(),
            'active_users': User.query.filter(User.last_login.isnot(None)).count(),
            'total_documents': Document.query.count(),
            'total_images': ImageAnalysis.query.count(),
            'total_workflows': WorkflowModel.query.count(),
            'total_reports': Report.query.count(),
            'processing_tasks': {
                'total': ProcessingTask.query.count(),
                'completed': ProcessingTask.query.filter_by(status='completed').count(),
                'failed': ProcessingTask.query.filter_by(status='failed').count(),
                'processing': ProcessingTask.query.filter_by(status='processing').count()
            }
        }
        
        return jsonify({'stats': stats})
        
    except Exception as e:
        logger.error(f"Admin stats error: {str(e)}")
        return jsonify({'error': 'Failed to get admin stats'}), 500

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def list_users():
    try:
        users = User.query.all()
        users_data = []
        
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': True  # Simplified for demo
            })
        
        return jsonify({'users': users_data})
        
    except Exception as e:
        logger.error(f"List users error: {str(e)}")
        return jsonify({'error': 'Failed to list users'}), 500

@app.route('/api/admin/system/logs', methods=['GET'])
@admin_required
def get_system_logs():
    try:
        # In a real application, you would read from actual log files
        # For demo purposes, we'll return sample logs
        logs = [
            {
                'id': 1,
                'timestamp': datetime.now().isoformat(),
                'level': 'INFO',
                'message': 'System backup completed successfully',
                'source': 'system'
            },
            {
                'id': 2,
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                'level': 'WARNING',
                'message': 'High CPU usage detected',
                'source': 'monitoring'
            },
            {
                'id': 3,
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                'level': 'ERROR',
                'message': 'Failed to process document: timeout',
                'source': 'processing'
            }
        ]
        
        return jsonify({'logs': logs})
        
    except Exception as e:
        logger.error(f"System logs error: {str(e)}")
        return jsonify({'error': 'Failed to get system logs'}), 500

# Report Download Route
@app.route('/api/reports/<int:report_id>/download', methods=['GET'])
@jwt_required()
def download_report(report_id):
    try:
        current_user_id = get_jwt_identity()
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        if not os.path.exists(report.file_path):
            return jsonify({'error': 'Report file not found'}), 404
        
        return send_file(report.file_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Download report error: {str(e)}")
        return jsonify({'error': 'Failed to download report'}), 500

# Initialize database and create sample data
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Create admin user if not exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@nextwave.au',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        db.session.add(admin_user)
    
    # Create demo user if not exists
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@nextwave.au',
            password_hash=generate_password_hash('demo123'),
            first_name='Demo',
            last_name='User',
            role='user'
        )
        db.session.add(demo_user)
    
    db.session.commit()
    
    # Create sample workflows
    workflow_engine.create_sample_workflows()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

