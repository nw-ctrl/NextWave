from .user import db
from datetime import datetime
import json

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    document_type = db.Column(db.Enum('pdf', 'word', 'visio', 'other', name='document_types'), default='other')
    status = db.Column(db.Enum('uploaded', 'processing', 'completed', 'error', name='document_status'), default='uploaded')
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    meta_data = db.Column(db.Text)  # JSON string
    tags = db.Column(db.Text)

    # Relationships
    versions = db.relationship('DocumentVersion', backref='document', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Document {self.filename}>'

    def set_metadata(self, metadata_dict):
        """Set document metadata as JSON"""
        self.meta_data = json.dumps(metadata_dict)

    def get_metadata(self):
        """Get document metadata from JSON"""
        if self.meta_data:
            return json.loads(self.meta_data)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'document_type': self.document_type,
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'metadata': self.get_metadata(),
            'tags': self.tags
        }

class DocumentVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    changes_description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('document_id', 'version_number'),)

    def __repr__(self):
        return f'<DocumentVersion {self.document_id}v{self.version_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'version_number': self.version_number,
            'file_path': self.file_path,
            'changes_description': self.changes_description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

