from src.models.user import db
from datetime import datetime
import json

class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    workflow_data = db.Column(db.Text, nullable=False)  # JSON string
    status = db.Column(db.Enum('draft', 'active', 'paused', 'completed', name='workflow_status'), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_run = db.Column(db.DateTime)
    run_count = db.Column(db.Integer, default=0)

    # Relationships
    executions = db.relationship('WorkflowExecution', backref='workflow', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Workflow {self.name}>'

    def set_workflow_data(self, workflow_dict):
        """Set workflow data as JSON"""
        self.workflow_data = json.dumps(workflow_dict)

    def get_workflow_data(self):
        """Get workflow data from JSON"""
        if self.workflow_data:
            return json.loads(self.workflow_data)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'workflow_data': self.get_workflow_data(),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'run_count': self.run_count
        }

class WorkflowExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    execution_data = db.Column(db.Text)  # JSON string
    status = db.Column(db.Enum('running', 'completed', 'failed', 'cancelled', name='execution_status'), default='running')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    result_data = db.Column(db.Text)  # JSON string

    def __repr__(self):
        return f'<WorkflowExecution {self.workflow_id}:{self.id}>'

    def set_execution_data(self, execution_dict):
        """Set execution data as JSON"""
        self.execution_data = json.dumps(execution_dict)

    def get_execution_data(self):
        """Get execution data from JSON"""
        if self.execution_data:
            return json.loads(self.execution_data)
        return {}

    def set_result_data(self, result_dict):
        """Set result data as JSON"""
        self.result_data = json.dumps(result_dict)

    def get_result_data(self):
        """Get result data from JSON"""
        if self.result_data:
            return json.loads(self.result_data)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'execution_data': self.get_execution_data(),
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'result_data': self.get_result_data()
        }

