from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.document import Document
from src.models.image import Image
from src.models.workflow import Workflow
from src.models.processing import ProcessingTask, Report, AdminLog, SystemSetting
from datetime import datetime, timedelta
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def log_admin_action(action, resource_type=None, resource_id=None, details=None):
    """Log admin actions"""
    try:
        user_id = get_jwt_identity()
        log_entry = AdminLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        if details:
            log_entry.set_details(details)
        db.session.add(log_entry)
        db.session.commit()
    except Exception:
        pass  # Don't fail the main operation if logging fails

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    try:
        # Get system statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_documents = Document.query.count()
        total_images = Image.query.count()
        total_workflows = Workflow.query.count()
        pending_tasks = ProcessingTask.query.filter_by(status='pending').count()
        
        # Get recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_users = User.query.filter(User.created_at >= week_ago).count()
        recent_documents = Document.query.filter(Document.created_at >= week_ago).count()
        recent_images = Image.query.filter(Image.created_at >= week_ago).count()
        
        # Get storage usage
        upload_folder = current_app.config.get('UPLOAD_FOLDER', '')
        total_storage = 0
        if os.path.exists(upload_folder):
            for root, dirs, files in os.walk(upload_folder):
                total_storage += sum(os.path.getsize(os.path.join(root, file)) for file in files)
        
        dashboard_data = {
            'statistics': {
                'total_users': total_users,
                'active_users': active_users,
                'total_documents': total_documents,
                'total_images': total_images,
                'total_workflows': total_workflows,
                'pending_tasks': pending_tasks,
                'storage_used_bytes': total_storage
            },
            'recent_activity': {
                'new_users': recent_users,
                'new_documents': recent_documents,
                'new_images': recent_images
            }
        }
        
        log_admin_action('view_dashboard')
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role')
        is_active = request.args.get('is_active')
        
        query = User.query
        
        if role:
            query = query.filter_by(role=role)
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        
        users = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        log_admin_action('view_users')
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        old_data = user.to_dict()
        
        # Update allowed fields
        allowed_fields = ['role', 'is_active', 'first_name', 'last_name', 'email']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        log_admin_action('update_user', 'user', user_id, {
            'old_data': old_data,
            'new_data': user.to_dict()
        })
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/processing-tasks', methods=['GET'])
@admin_required
def get_processing_tasks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        task_type = request.args.get('task_type')
        
        query = ProcessingTask.query
        
        if status:
            query = query.filter_by(status=status)
        
        if task_type:
            query = query.filter_by(task_type=task_type)
        
        tasks = query.order_by(ProcessingTask.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        log_admin_action('view_processing_tasks')
        return jsonify({
            'tasks': [task.to_dict() for task in tasks.items],
            'total': tasks.total,
            'pages': tasks.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reports', methods=['POST'])
@admin_required
def generate_report():
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('report_type'):
            return jsonify({'error': 'Report name and type are required'}), 400
        
        user_id = get_jwt_identity()
        
        report = Report(
            user_id=user_id,
            name=data['name'],
            report_type=data['report_type']
        )
        
        if data.get('template_config'):
            report.set_template_config(data['template_config'])
        
        if data.get('source_data'):
            report.set_source_data(data['source_data'])
        
        db.session.add(report)
        db.session.commit()
        
        # Simulate report generation (in real implementation, this would be async)
        try:
            # Generate report based on type
            if data['report_type'] == 'user_activity':
                source_data = {
                    'total_users': User.query.count(),
                    'active_users': User.query.filter_by(is_active=True).count(),
                    'recent_logins': User.query.filter(User.last_login >= datetime.utcnow() - timedelta(days=7)).count()
                }
            elif data['report_type'] == 'system_usage':
                source_data = {
                    'total_documents': Document.query.count(),
                    'total_images': Image.query.count(),
                    'total_workflows': Workflow.query.count(),
                    'pending_tasks': ProcessingTask.query.filter_by(status='pending').count()
                }
            else:
                source_data = {'message': 'Custom report generated'}
            
            report.set_source_data(source_data)
            report.status = 'completed'
            report.completed_at = datetime.utcnow()
            
        except Exception as report_error:
            report.status = 'error'
            report.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        log_admin_action('generate_report', 'report', report.id, {
            'report_type': data['report_type'],
            'report_name': data['name']
        })
        
        return jsonify({
            'message': 'Report generation started',
            'report': report.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reports', methods=['GET'])
@admin_required
def get_reports():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        reports = Report.query.order_by(Report.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reports': [report.to_dict() for report in reports.items],
            'total': reports.total,
            'pages': reports.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/settings', methods=['GET'])
@admin_required
def get_settings():
    try:
        settings = SystemSetting.query.all()
        
        return jsonify({
            'settings': [setting.to_dict() for setting in settings]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/settings', methods=['POST'])
@admin_required
def create_setting():
    try:
        data = request.get_json()
        
        if not data.get('setting_key'):
            return jsonify({'error': 'Setting key is required'}), 400
        
        # Check if setting already exists
        existing = SystemSetting.query.filter_by(setting_key=data['setting_key']).first()
        if existing:
            return jsonify({'error': 'Setting already exists'}), 400
        
        setting = SystemSetting(
            setting_key=data['setting_key'],
            setting_value=data.get('setting_value', ''),
            setting_type=data.get('setting_type', 'string'),
            description=data.get('description'),
            is_public=data.get('is_public', False)
        )
        
        db.session.add(setting)
        db.session.commit()
        
        log_admin_action('create_setting', 'system_setting', setting.id, {
            'setting_key': data['setting_key']
        })
        
        return jsonify({
            'message': 'Setting created successfully',
            'setting': setting.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/logs', methods=['GET'])
@admin_required
def get_admin_logs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        action = request.args.get('action')
        
        query = AdminLog.query
        
        if action:
            query = query.filter_by(action=action)
        
        logs = query.order_by(AdminLog.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'total': logs.total,
            'pages': logs.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

