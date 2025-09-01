from src.models.user import db
from datetime import datetime
import json

class ImageAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    format = db.Column(db.String(10))
    status = db.Column(db.Enum('uploaded', 'analyzing', 'analyzed', 'error', name='image_status'), default='uploaded')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    analyzed_at = db.Column(db.DateTime)
    meta_data = db.Column(db.Text)  # JSON string
    tags = db.Column(db.Text)

    # Relationships
    analysis_results = db.relationship('ImageAnalysisResult', backref='image', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ImageAnalysis {self.filename}>'

    def set_metadata(self, metadata_dict):
        """Set image metadata as JSON"""
        self.meta_data = json.dumps(metadata_dict)

    def get_metadata(self):
        """Get image metadata from JSON"""
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
            'width': self.width,
            'height': self.height,
            'format': self.format,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None,
            'metadata': self.get_metadata(),
            'tags': self.tags
        }

class ImageAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    description = db.Column(db.Text)
    characteristics = db.Column(db.Text)  # JSON string
    confidence_score = db.Column(db.Numeric(3, 2))
    analysis_model = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ImageAnalysisResult {self.image_id}>'

    def set_characteristics(self, characteristics_dict):
        """Set image characteristics as JSON"""
        self.characteristics = json.dumps(characteristics_dict)

    def get_characteristics(self):
        """Get image characteristics from JSON"""
        if self.characteristics:
            return json.loads(self.characteristics)
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'image_id': self.image_id,
            'description': self.description,
            'characteristics': self.get_characteristics(),
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'analysis_model': self.analysis_model,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

