import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, Download, Settings, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

const DocumentProcessor = () => {
  const [documents, setDocuments] = useState([
    {
      id: 1,
      name: 'Annual Report 2024.pdf',
      type: 'pdf',
      size: '2.4 MB',
      status: 'completed',
      uploadedAt: '2024-01-15'
    },
    {
      id: 2,
      name: 'Contract_v2.docx',
      type: 'word',
      size: '1.2 MB',
      status: 'processing',
      uploadedAt: '2024-01-14'
    }
  ])

  const [dragOver, setDragOver] = useState(false)

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    // Handle file drop logic here
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            Document Processing
          </h1>
          <p className="text-white/70 text-lg">
            Upload, process, and manage your documents with AI-powered tools.
          </p>
        </motion.div>

        {/* Upload Area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="glass-card p-8 mb-8"
        >
          <div
            className={`file-upload-area p-12 text-center rounded-lg transition-all duration-300 ${
              dragOver ? 'drag-over' : ''
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <Upload className="h-16 w-16 text-white/50 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">
              Drop your documents here
            </h3>
            <p className="text-white/70 mb-6">
              Supports PDF, Word, Visio files up to 100MB
            </p>
            <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
              Choose Files
            </Button>
          </div>
        </motion.div>

        {/* Processing Options */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          {[
            {
              title: 'PDF to Word',
              description: 'Convert PDF documents to editable Word format',
              icon: <FileText className="h-8 w-8" />
            },
            {
              title: 'Visio Processing',
              description: 'Edit and convert Visio diagrams',
              icon: <Settings className="h-8 w-8" />
            },
            {
              title: 'Batch Processing',
              description: 'Process multiple documents simultaneously',
              icon: <Upload className="h-8 w-8" />
            }
          ].map((option, index) => (
            <div key={index} className="glass-card p-6 glass-card-hover">
              <div className="text-blue-400 mb-4">
                {option.icon}
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">
                {option.title}
              </h3>
              <p className="text-white/70 text-sm">
                {option.description}
              </p>
            </div>
          ))}
        </motion.div>

        {/* Documents List */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="glass-card p-6"
        >
          <h2 className="text-2xl font-bold text-white mb-6">Your Documents</h2>
          
          <div className="space-y-4">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
                <div className="flex items-center space-x-4">
                  <FileText className="h-8 w-8 text-blue-400" />
                  <div>
                    <h3 className="text-white font-medium">{doc.name}</h3>
                    <p className="text-white/60 text-sm">
                      {doc.size} • {doc.uploadedAt}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    doc.status === 'completed' 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-orange-500/20 text-orange-400'
                  }`}>
                    {doc.status}
                  </span>
                  
                  <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">
                    <Download className="h-4 w-4" />
                  </Button>
                  
                  <Button variant="ghost" size="sm" className="text-white/70 hover:text-red-400">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default DocumentProcessor

