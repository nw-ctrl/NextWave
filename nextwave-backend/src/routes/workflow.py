from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.workflow import Workflow, WorkflowExecution
from datetime import datetime
import json

workflow_bp = Blueprint('workflow', __name__)

@workflow_bp.route('/', methods=['GET'])
@jwt_required()
def get_workflows():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        query = Workflow.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        workflows = query.order_by(Workflow.updated_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'workflows': [wf.to_dict() for wf in workflows.items],
            'total': workflows.total,
            'pages': workflows.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/', methods=['POST'])
@jwt_required()
def create_workflow():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Workflow name is required'}), 400
        
        if not data.get('workflow_data'):
            return jsonify({'error': 'Workflow data is required'}), 400
        
        workflow = Workflow(
            user_id=user_id,
            name=data['name'],
            description=data.get('description'),
            status=data.get('status', 'draft')
        )
        workflow.set_workflow_data(data['workflow_data'])
        
        db.session.add(workflow)
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow created successfully',
            'workflow': workflow.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/<int:workflow_id>', methods=['GET'])
@jwt_required()
def get_workflow(workflow_id):
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        return jsonify({'workflow': workflow.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/<int:workflow_id>', methods=['PUT'])
@jwt_required()
def update_workflow(workflow_id):
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            workflow.name = data['name']
        if 'description' in data:
            workflow.description = data['description']
        if 'status' in data:
            workflow.status = data['status']
        if 'workflow_data' in data:
            workflow.set_workflow_data(data['workflow_data'])
        
        workflow.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow updated successfully',
            'workflow': workflow.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/<int:workflow_id>', methods=['DELETE'])
@jwt_required()
def delete_workflow(workflow_id):
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        db.session.delete(workflow)
        db.session.commit()
        
        return jsonify({'message': 'Workflow deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/<int:workflow_id>/execute', methods=['POST'])
@jwt_required()
def execute_workflow(workflow_id):
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        data = request.get_json()
        
        # Create execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            status='running'
        )
        
        if data and data.get('execution_data'):
            execution.set_execution_data(data['execution_data'])
        
        # Update workflow stats
        workflow.last_run = datetime.utcnow()
        workflow.run_count += 1
        
        db.session.add(execution)
        db.session.commit()
        
        # Simulate workflow execution (in real implementation, this would be async)
        try:
            workflow_data = workflow.get_workflow_data()
            
            # Basic workflow simulation
            result = {
                'status': 'completed',
                'steps_executed': len(workflow_data.get('steps', [])),
                'execution_time': '2.5s',
                'output': 'Workflow executed successfully'
            }
            
            execution.status = 'completed'
            execution.completed_at = datetime.utcnow()
            execution.set_result_data(result)
            
        except Exception as exec_error:
            execution.status = 'failed'
            execution.completed_at = datetime.utcnow()
            execution.error_message = str(exec_error)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow execution started',
            'execution': execution.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/<int:workflow_id>/executions', methods=['GET'])
@jwt_required()
def get_workflow_executions(workflow_id):
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        executions = WorkflowExecution.query.filter_by(workflow_id=workflow_id)\
            .order_by(WorkflowExecution.started_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'executions': [exec.to_dict() for exec in executions.items],
            'total': executions.total,
            'pages': executions.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workflow_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_workflow_templates():
    """Get predefined workflow templates"""
    templates = [
        {
            'id': 'document_processing',
            'name': 'Document Processing Flow',
            'description': 'Template for processing documents through multiple stages',
            'workflow_data': {
                'steps': [
                    {'id': 'upload', 'name': 'Upload Document', 'type': 'input'},
                    {'id': 'validate', 'name': 'Validate Format', 'type': 'validation'},
                    {'id': 'process', 'name': 'Process Content', 'type': 'processing'},
                    {'id': 'output', 'name': 'Generate Output', 'type': 'output'}
                ],
                'connections': [
                    {'from': 'upload', 'to': 'validate'},
                    {'from': 'validate', 'to': 'process'},
                    {'from': 'process', 'to': 'output'}
                ]
            }
        },
        {
            'id': 'image_analysis',
            'name': 'Image Analysis Flow',
            'description': 'Template for analyzing images and generating reports',
            'workflow_data': {
                'steps': [
                    {'id': 'upload', 'name': 'Upload Image', 'type': 'input'},
                    {'id': 'analyze', 'name': 'AI Analysis', 'type': 'ai_processing'},
                    {'id': 'extract', 'name': 'Extract Features', 'type': 'feature_extraction'},
                    {'id': 'report', 'name': 'Generate Report', 'type': 'report_generation'}
                ],
                'connections': [
                    {'from': 'upload', 'to': 'analyze'},
                    {'from': 'analyze', 'to': 'extract'},
                    {'from': 'extract', 'to': 'report'}
                ]
            }
        }
    ]
    
    return jsonify({'templates': templates}), 200

