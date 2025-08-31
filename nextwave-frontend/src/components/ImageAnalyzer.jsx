import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, Image, Eye, Download, Trash2, Brain } from 'lucide-react'
import { Button } from '@/components/ui/button'

const ImageAnalyzer = () => {
  const [images, setImages] = useState([
    {
      id: 1,
      name: 'product_image_01.jpg',
      size: '1.8 MB',
      status: 'analyzed',
      uploadedAt: '2024-01-15',
      analysis: {
        description: 'A modern smartphone with a sleek black design, featuring a large display and multiple camera lenses on the back.',
        characteristics: {
          brightness: 142,
          edge_density: 0.08,
          dominant_colors: ['#1a1a1a', '#333333', '#666666']
        }
      }
    },
    {
      id: 2,
      name: 'landscape_photo.png',
      size: '3.2 MB',
      status: 'analyzing',
      uploadedAt: '2024-01-14'
    }
  ])

  const [selectedImage, setSelectedImage] = useState(null)

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
            AI Image Analysis
          </h1>
          <p className="text-white/70 text-lg">
            Upload images and get detailed AI-powered analysis and descriptions.
          </p>
        </motion.div>

        {/* Upload Area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="glass-card p-8 mb-8"
        >
          <div className="file-upload-area p-12 text-center rounded-lg">
            <Image className="h-16 w-16 text-white/50 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">
              Upload images for analysis
            </h3>
            <p className="text-white/70 mb-6">
              Supports JPG, PNG, GIF, WebP up to 50MB
            </p>
            <Button className="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700">
              Choose Images
            </Button>
          </div>
        </motion.div>

        {/* Analysis Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          {[
            {
              title: 'AI Description',
              description: 'Get detailed descriptions of image content',
              icon: <Brain className="h-8 w-8" />
            },
            {
              title: 'Feature Extraction',
              description: 'Analyze colors, brightness, and complexity',
              icon: <Eye className="h-8 w-8" />
            },
            {
              title: 'Report Generation',
              description: 'Generate custom PDF reports with findings',
              icon: <Download className="h-8 w-8" />
            }
          ].map((feature, index) => (
            <div key={index} className="glass-card p-6 glass-card-hover">
              <div className="text-purple-400 mb-4">
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-white/70 text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Images List */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="glass-card p-6"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Your Images</h2>
            
            <div className="space-y-4">
              {images.map((img) => (
                <div 
                  key={img.id} 
                  className={`p-4 bg-white/5 rounded-lg cursor-pointer transition-all duration-300 ${
                    selectedImage?.id === img.id ? 'bg-white/10 border border-purple-400' : 'hover:bg-white/8'
                  }`}
                  onClick={() => setSelectedImage(img)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <Image className="h-8 w-8 text-purple-400" />
                      <div>
                        <h3 className="text-white font-medium">{img.name}</h3>
                        <p className="text-white/60 text-sm">
                          {img.size} • {img.uploadedAt}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        img.status === 'analyzed' 
                          ? 'bg-green-500/20 text-green-400' 
                          : 'bg-orange-500/20 text-orange-400'
                      }`}>
                        {img.status}
                      </span>
                      
                      <Button variant="ghost" size="sm" className="text-white/70 hover:text-red-400">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Analysis Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="glass-card p-6"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Analysis Results</h2>
            
            {selectedImage ? (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {selectedImage.name}
                  </h3>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    selectedImage.status === 'analyzed' 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-orange-500/20 text-orange-400'
                  }`}>
                    {selectedImage.status}
                  </span>
                </div>

                {selectedImage.analysis ? (
                  <>
                    <div>
                      <h4 className="text-white font-medium mb-2">AI Description</h4>
                      <p className="text-white/80 text-sm leading-relaxed">
                        {selectedImage.analysis.description}
                      </p>
                    </div>

                    <div>
                      <h4 className="text-white font-medium mb-3">Image Characteristics</h4>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-white/70 text-sm">Brightness</span>
                          <span className="text-white text-sm">
                            {selectedImage.analysis.characteristics.brightness}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-white/70 text-sm">Edge Density</span>
                          <span className="text-white text-sm">
                            {selectedImage.analysis.characteristics.edge_density}
                          </span>
                        </div>
                        <div>
                          <span className="text-white/70 text-sm block mb-2">Dominant Colors</span>
                          <div className="flex space-x-2">
                            {selectedImage.analysis.characteristics.dominant_colors.map((color, index) => (
                              <div
                                key={index}
                                className="w-6 h-6 rounded-full border border-white/20"
                                style={{ backgroundColor: color }}
                              />
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>

                    <Button className="w-full bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700">
                      <Download className="h-4 w-4 mr-2" />
                      Generate Report
                    </Button>
                  </>
                ) : (
                  <div className="text-center py-8">
                    <div className="loading-spinner mx-auto mb-4"></div>
                    <p className="text-white/70">Analyzing image...</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-12">
                <Image className="h-16 w-16 text-white/30 mx-auto mb-4" />
                <p className="text-white/50">Select an image to view analysis results</p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default ImageAnalyzer

