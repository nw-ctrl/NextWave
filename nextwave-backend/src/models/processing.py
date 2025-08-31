from src.models.user import db
from datetime import datetime
import json

class ProcessingTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_type = db.Column(db.Enum('pdf_edit', 'pdf_to_visio', 'visio_to_pdf', 'visio_edit', 'pdf_to_word', 'image_analysis', name='task_types'), nullable=False)
    source_file_id = db.Column(db.Integer)
    target_file_id = db.Column(db.Integer)
    parameters = db.Column(db.Text)  # JSON string
    status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed', name='task_status'), default='pending')
    progress = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    result_data = db.Column(db.Text)  # JSON string

    def __repr__(self):
        return f'<ProcessingTask {self.task_type}:{self.id}>'

    def set_parameters(self, parameters_dict):
        """Set task parameters as JSON"""
        self.parameters = json.dumps(parameters_dict)

    def get_parameters(self):
        """Get task parameters from JSON"""
        if self.parameters:
            return json.loads(self.parameters)
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
            'user_id': self.user_id,
            'task_type': self.task_type,
            'source_file_id': self.source_file_id,
            'target_file_id': self.target_file_id,
            'parameters': self.get_parameters(),
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'result_data': self.get_result_data()
        }

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    report_type = db.Column(db.String(100), nullable=False)
    template_config = db.Column(db.Text)  # JSON string
    source_data = db.Column(db.Text)  # JSON string
    file_path = db.Column(db.String(500))
    status = db.Column(db.Enum('generating', 'completed', 'error', name='report_status'), default='generating')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Report {self.name}>'

    def set_template_config(self, config_dict):
        """Set template configuration as JSON"""
        self.template_config = json.dumps(config_dict)

    def get_template_config(self):
        """Get template configuration from JSON"""
        if self.template_config:
            return json.loads(self.template_config)
        return {}

    def set_source_data(self, data_dict):
        """Set source data as JSON"""
        self.source_data = json.dumps(data_dict)

    def get_source_data(self):
        """Get source data from JSON"""
        if self.source_data:
            return json.loads(self.source_data)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'report_type': self.report_type,
            'template_config': self.get_template_config(),
            'source_data': self.get_source_data(),
            'file_path': self.file_path,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # JSON string
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AdminLog {self.action}:{self.id}>'

    def set_details(self, details_dict):
        """Set details as JSON"""
        self.details = json.dumps(details_dict)

    def get_details(self):
        """Get details from JSON"""
        if self.details:
            return json.loads(self.details)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.get_details(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SystemSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.Enum('string', 'integer', 'boolean', 'json', name='setting_types'), default='string')
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SystemSetting {self.setting_key}>'

    def get_typed_value(self):
        """Get setting value with proper type conversion"""
        if self.setting_type == 'integer':
            return int(self.setting_value) if self.setting_value else 0
        elif self.setting_type == 'boolean':
            return self.setting_value.lower() == 'true' if self.setting_value else False
        elif self.setting_type == 'json':
            return json.loads(self.setting_value) if self.setting_value else {}
        else:
            return self.setting_value

    def to_dict(self):
        return {
            'id': self.id,
            'setting_key': self.setting_key,
            'setting_value': self.get_typed_value(),
            'setting_type': self.setting_type,
            'description': self.description,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

