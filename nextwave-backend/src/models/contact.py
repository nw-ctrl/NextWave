from .user import db
from datetime import datetime
import json

class ContactSubmission(db.Model):
    __tablename__ = 'contact_submission'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(50))
    company = db.Column(db.String(255))
    service_type = db.Column(db.String(100))
    status = db.Column(db.Enum('new', 'in_progress', 'completed', 'closed', name='contact_status'), default='new')
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent', name='contact_priority'), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    responded_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.subject}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'phone': self.phone,
            'company': self.company,
            'service_type': self.service_type,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'notes': self.notes,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }
    
    def to_dict_safe(self):
        """Return contact data without sensitive information"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'service_type': self.service_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

