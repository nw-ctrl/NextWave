# NextWave - AI-Powered Document & Workflow Management Platform

![NextWave Logo](https://img.shields.io/badge/NextWave-AI%20Platform-blue?style=for-the-badge&logo=react)

A comprehensive web application with advanced admin capabilities for PDF editing, Visio conversion, AI-powered image analysis, and animated workflow simulation with modern glassmorphism design.

## 🚀 Features

### 🔧 Admin Panel Capabilities
- **PDF Processing**: Extract text, convert to images, merge/split PDFs, add watermarks
- **Document Conversion**: PDF to Word, Word to PDF, Visio integration
- **Advanced PDF Editing**: Comprehensive PDF manipulation tools
- **User Management**: Role-based access control and user administration
- **System Monitoring**: Real-time logs and performance metrics

### 🤖 AI Vision & Analysis
- **Image Analysis**: AI-powered color detection, texture analysis, object recognition
- **Batch Processing**: Analyze multiple images simultaneously
- **Image Comparison**: Advanced similarity analysis and reporting
- **Natural Language Descriptions**: Auto-generated image descriptions
- **Custom Report Generation**: PDF reports with analysis results

### 🔄 Animated Workflow Simulation
- **Visual Workflow Builder**: Drag-and-drop interface for creating workflows
- **Real-time Animation**: Step-by-step execution visualization
- **Flow Simulation**: Animated data flow between processing steps
- **Status Monitoring**: Live execution tracking with detailed logging
- **Template System**: Pre-built workflow templates

### 🎨 Modern Design
- **Glassmorphism UI**: Modern glass-effect design with backdrop blur
- **Responsive Layout**: Mobile-first design with touch support
- **Smooth Animations**: Framer Motion powered transitions
- **Dark Theme**: Professional dark theme with gradient accents
- **Interactive Elements**: Hover effects and micro-interactions

## 🏗️ Architecture

### Backend (Flask)
```
nextwave-backend/
├── src/
│   ├── main.py                 # Main Flask application
│   ├── models/                 # Database models
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── image.py
│   │   ├── workflow.py
│   │   └── processing.py
│   ├── routes/                 # API routes
│   │   ├── auth.py
│   │   ├── document.py
│   │   ├── image.py
│   │   ├── workflow.py
│   │   ├── admin.py
│   │   └── advanced_processing.py
│   └── utils/                  # Utility modules
│       ├── pdf_processor.py
│       ├── image_analyzer.py
│       └── workflow_engine.py
└── requirements.txt
```

### Frontend (React + Vite)
```
nextwave-frontend/
├── src/
│   ├── App.jsx                 # Main application
│   ├── components/             # React components
│   │   ├── Header.jsx
│   │   ├── Hero.jsx
│   │   ├── Services.jsx
│   │   ├── Dashboard.jsx
│   │   ├── DocumentProcessor.jsx
│   │   ├── ImageAnalyzer.jsx
│   │   ├── WorkflowBuilder.jsx
│   │   ├── WorkflowCanvas.jsx
│   │   └── AdminPanel.jsx
│   ├── contexts/               # React contexts
│   │   └── AuthContext.jsx
│   └── App.css                 # Glassmorphism styles
└── package.json
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **JWT** - Authentication
- **OpenCV** - Computer vision
- **PyPDF2** - PDF processing
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **PyMuPDF** - Advanced PDF operations

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool
- **Framer Motion** - Animations
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **React Router** - Navigation

### AI & Processing
- **Computer Vision** - Image analysis and object detection
- **Natural Language Processing** - Automated descriptions
- **Workflow Engine** - Custom workflow execution system
- **Real-time Processing** - Live status updates and monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm or yarn

### Backend Setup
```bash
cd nextwave-backend
pip install -r requirements.txt
python src/main.py
```

### Frontend Setup
```bash
cd nextwave-frontend
npm install
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health

## 🔐 Default Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@nextwave.au`

### Demo Account
- **Username**: `demo`
- **Password**: `demo123`
- **Email**: `demo@nextwave.au`

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Document Processing
- `POST /api/documents/upload` - Upload document
- `POST /api/documents/{id}/process` - Process document
- `POST /api/pdf/merge` - Merge PDFs
- `POST /api/pdf/split` - Split PDF
- `POST /api/pdf/watermark` - Add watermark

### Image Analysis
- `POST /api/images/upload` - Upload and analyze image
- `POST /api/images/{id}/report` - Generate analysis report
- `POST /api/image/batch-analyze` - Batch analyze images
- `POST /api/image/compare` - Compare two images

### Workflow Management
- `GET /api/workflows` - List workflows
- `POST /api/workflows` - Create workflow
- `POST /api/workflows/{id}/execute` - Execute workflow
- `GET /api/workflows/executions/{id}` - Get execution status

### Admin Panel
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/users` - List users
- `GET /api/admin/system/logs` - System logs

## 🎯 Key Features Demo

### 1. PDF Processing
```python
# Extract text from PDF
result = pdf_processor.extract_text_from_pdf('document.pdf')

# Convert PDF to images
result = pdf_processor.pdf_to_images('document.pdf', 'output_dir/')

# Add watermark
result = pdf_processor.add_watermark('input.pdf', 'CONFIDENTIAL', 'output.pdf')
```

### 2. AI Image Analysis
```python
# Analyze image
result = image_analyzer.analyze_image('image.jpg')
# Returns: color analysis, texture detection, object recognition, description

# Batch analysis
result = image_analyzer.batch_analyze(['img1.jpg', 'img2.jpg'])
```

### 3. Workflow Automation
```javascript
// Create and execute workflow
const workflow = await createWorkflow('Document Processing Pipeline')
const execution = await executeWorkflow(workflow.id, inputData)
// Real-time animated execution with status updates
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///nextwave.db

# Frontend
VITE_API_BASE_URL=http://localhost:5000
```

### Database Schema
The application uses SQLite by default with the following models:
- **Users** - Authentication and user management
- **Documents** - File storage and metadata
- **Images** - Image analysis results
- **Workflows** - Workflow definitions
- **Processing Tasks** - Background job tracking
- **Reports** - Generated reports

## 🧪 Testing

### Integration Tests
```bash
python test_integration.py
```

### Test Coverage
- ✅ PDF Processing: Text extraction, image conversion, watermarking
- ✅ Image Analysis: Color detection, texture analysis, object recognition
- ✅ Workflow Engine: Creation, execution, monitoring
- ✅ API Endpoints: Authentication, CRUD operations
- ✅ Frontend Components: UI rendering, user interactions

## 🚀 Deployment

### Production Setup
1. **Backend**: Use Gunicorn or uWSGI for production WSGI server
2. **Frontend**: Build with `npm run build` and serve with nginx
3. **Database**: Migrate to PostgreSQL for production
4. **Security**: Configure HTTPS, CORS, and environment variables

### Docker Support
```dockerfile
# Backend Dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]

# Frontend Dockerfile
FROM node:20
COPY . /app
WORKDIR /app
RUN npm install && npm run build
CMD ["npm", "run", "preview"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** community for the excellent web framework
- **React** team for the powerful UI library
- **OpenCV** for computer vision capabilities
- **Framer Motion** for smooth animations
- **Tailwind CSS** for utility-first styling

## 📞 Support

For support, email support@nextwave.au or create an issue in the GitHub repository.

---

**NextWave** - Transforming document processing and workflow automation with AI-powered intelligence and modern design.

![Built with Love](https://img.shields.io/badge/Built%20with-❤️-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-19+-61DAFB?style=for-the-badge&logo=react)
![AI Powered](https://img.shields.io/badge/AI-Powered-green?style=for-the-badge&logo=artificial-intelligence)

