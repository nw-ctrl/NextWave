from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.Enum('admin', 'user', 'viewer', name='user_roles'), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profile_image_url = db.Column(db.String(255))
    preferences = db.Column(db.Text)  # JSON string

    # Relationships
    documents = db.relationship('Document', backref='owner', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('ImageAnalysis', backref='owner', lazy=True, cascade='all, delete-orphan')
    workflows = db.relationship('WorkflowModel', backref='owner', lazy=True, cascade='all, delete-orphan')
    processing_tasks = db.relationship('ProcessingTask', backref='user', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def set_preferences(self, preferences_dict):
        """Set user preferences as JSON"""
        self.preferences = json.dumps(preferences_dict)

    def get_preferences(self):
        """Get user preferences from JSON"""
        if self.preferences:
            return json.loads(self.preferences)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile_image_url': self.profile_image_url,
            'preferences': self.get_preferences()
        }

    def to_dict_safe(self):
        """Return user data without sensitive information"""
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'profile_image_url': self.profile_image_url
        }

