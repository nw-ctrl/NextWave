# NextWave Database Schema Design

## Database Overview

The NextWave application uses a relational database design optimized for document processing, image analysis, and workflow management. The schema is designed to be scalable, maintainable, and supports complex relationships between users, documents, and processing tasks.

## Core Tables

### 1. Users Table
Stores user account information and authentication data.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role ENUM('admin', 'user', 'viewer') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_image_url VARCHAR(255),
    preferences JSON
);
```

### 2. Documents Table
Manages all document files including PDFs, Word documents, and Visio files.

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    document_type ENUM('pdf', 'word', 'visio', 'other') NOT NULL,
    status ENUM('uploaded', 'processing', 'completed', 'error') DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    metadata JSON,
    tags TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 3. Images Table
Stores image files and their analysis results.

```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    width INTEGER,
    height INTEGER,
    format VARCHAR(10),
    status ENUM('uploaded', 'analyzing', 'analyzed', 'error') DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyzed_at TIMESTAMP,
    metadata JSON,
    tags TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 4. Image Analysis Results Table
Stores AI-generated descriptions and characteristics of images.

```sql
CREATE TABLE image_analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id INTEGER NOT NULL,
    description TEXT,
    characteristics JSON,
    confidence_score DECIMAL(3,2),
    analysis_model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);
```

### 5. Workflows Table
Manages animated flow simulations and process definitions.

```sql
CREATE TABLE workflows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    workflow_data JSON NOT NULL,
    status ENUM('draft', 'active', 'paused', 'completed') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_run TIMESTAMP,
    run_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 6. Workflow Executions Table
Tracks individual workflow runs and their results.

```sql
CREATE TABLE workflow_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id INTEGER NOT NULL,
    execution_data JSON,
    status ENUM('running', 'completed', 'failed', 'cancelled') DEFAULT 'running',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    result_data JSON,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
);
```

### 7. Processing Tasks Table
Manages background processing tasks for documents and images.

```sql
CREATE TABLE processing_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_type ENUM('pdf_edit', 'pdf_to_visio', 'visio_to_pdf', 'visio_edit', 'pdf_to_word', 'image_analysis') NOT NULL,
    source_file_id INTEGER,
    target_file_id INTEGER,
    parameters JSON,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    result_data JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 8. Reports Table
Stores generated PDF reports and their configurations.

```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    report_type VARCHAR(100) NOT NULL,
    template_config JSON,
    source_data JSON,
    file_path VARCHAR(500),
    status ENUM('generating', 'completed', 'error') DEFAULT 'generating',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 9. Admin Logs Table
Tracks administrative activities and system events.

```sql
CREATE TABLE admin_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
```

### 10. System Settings Table
Stores application configuration and admin preferences.

```sql
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationship Tables

### 11. Document Versions Table
Tracks version history of edited documents.

```sql
CREATE TABLE document_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    changes_description TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(document_id, version_number)
);
```

### 12. User Sessions Table
Manages user authentication sessions.

```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 13. File Shares Table
Manages file sharing between users.

```sql
CREATE TABLE file_shares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    shared_with_id INTEGER NOT NULL,
    resource_type ENUM('document', 'image', 'workflow', 'report') NOT NULL,
    resource_id INTEGER NOT NULL,
    permissions JSON,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Indexes for Performance

```sql
-- User-related indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- Document-related indexes
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_created_at ON documents(created_at);

-- Image-related indexes
CREATE INDEX idx_images_user_id ON images(user_id);
CREATE INDEX idx_images_status ON images(status);
CREATE INDEX idx_images_created_at ON images(created_at);

-- Workflow-related indexes
CREATE INDEX idx_workflows_user_id ON workflows(user_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflow_executions_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);

-- Processing task indexes
CREATE INDEX idx_processing_tasks_user_id ON processing_tasks(user_id);
CREATE INDEX idx_processing_tasks_type ON processing_tasks(task_type);
CREATE INDEX idx_processing_tasks_status ON processing_tasks(status);
CREATE INDEX idx_processing_tasks_created_at ON processing_tasks(created_at);

-- Admin and logging indexes
CREATE INDEX idx_admin_logs_user_id ON admin_logs(user_id);
CREATE INDEX idx_admin_logs_action ON admin_logs(action);
CREATE INDEX idx_admin_logs_created_at ON admin_logs(created_at);

-- Session management indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
```

## Data Relationships

The database schema implements the following key relationships:

1. **Users to Documents**: One-to-many relationship where users can own multiple documents
2. **Users to Images**: One-to-many relationship for image ownership
3. **Images to Analysis Results**: One-to-many relationship for multiple analysis runs
4. **Users to Workflows**: One-to-many relationship for workflow ownership
5. **Workflows to Executions**: One-to-many relationship tracking workflow runs
6. **Documents to Versions**: One-to-many relationship for version control
7. **Users to Processing Tasks**: One-to-many relationship for task ownership
8. **Users to Reports**: One-to-many relationship for report generation

## Data Integrity Constraints

The schema enforces data integrity through:

- **Primary Keys**: Unique identifiers for all tables
- **Foreign Key Constraints**: Maintain referential integrity
- **Unique Constraints**: Prevent duplicate usernames and emails
- **Check Constraints**: Validate enum values and data ranges
- **Not Null Constraints**: Ensure required fields are populated

## Security Considerations

Database security is implemented through:

- **Password Hashing**: User passwords stored as secure hashes
- **Session Management**: Secure token-based authentication
- **Access Control**: Role-based permissions system
- **Audit Trail**: Comprehensive logging of user actions
- **Data Encryption**: Sensitive data encrypted at rest

## Backup and Maintenance

The schema supports:

- **Regular Backups**: Automated backup procedures
- **Data Archiving**: Historical data management
- **Performance Monitoring**: Query performance tracking
- **Index Maintenance**: Regular index optimization
- **Data Cleanup**: Automated removal of expired sessions and temporary files

This database schema provides a robust foundation for the NextWave application, supporting all required features while maintaining data integrity, security, and performance.

