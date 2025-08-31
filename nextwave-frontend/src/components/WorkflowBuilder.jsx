import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Plus, Play, Pause, Settings, Trash2, Workflow, Save } from 'lucide-react'
import { Button } from '@/components/ui/button'

const WorkflowBuilder = () => {
  const [workflows, setWorkflows] = useState([
    {
      id: 1,
      name: 'Document Processing Flow',
      description: 'Automated document upload, validation, and processing',
      status: 'active',
      lastRun: '2024-01-15',
      steps: 4
    },
    {
      id: 2,
      name: 'Image Analysis Pipeline',
      description: 'Batch image analysis with report generation',
      status: 'draft',
      lastRun: null,
      steps: 3
    }
  ])

  const [selectedWorkflow, setSelectedWorkflow] = useState(null)

  const workflowSteps = [
    { id: 'upload', name: 'Upload Document', type: 'input', x: 100, y: 100 },
    { id: 'validate', name: 'Validate Format', type: 'validation', x: 300, y: 100 },
    { id: 'process', name: 'Process Content', type: 'processing', x: 500, y: 100 },
    { id: 'output', name: 'Generate Output', type: 'output', x: 700, y: 100 }
  ]

  const getStepColor = (type) => {
    switch (type) {
      case 'input':
        return 'from-blue-500 to-cyan-500'
      case 'validation':
        return 'from-yellow-500 to-orange-500'
      case 'processing':
        return 'from-purple-500 to-pink-500'
      case 'output':
        return 'from-green-500 to-emerald-500'
      default:
        return 'from-gray-500 to-gray-600'
    }
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
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                Workflow Builder
              </h1>
              <p className="text-white/70 text-lg">
                Create and manage automated workflows with visual drag-and-drop interface.
              </p>
            </div>
            <Button className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700">
              <Plus className="h-4 w-4 mr-2" />
              New Workflow
            </Button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Workflows List */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="glass-card p-6"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Your Workflows</h2>
            
            <div className="space-y-4">
              {workflows.map((workflow) => (
                <div 
                  key={workflow.id}
                  className={`p-4 bg-white/5 rounded-lg cursor-pointer transition-all duration-300 ${
                    selectedWorkflow?.id === workflow.id ? 'bg-white/10 border border-green-400' : 'hover:bg-white/8'
                  }`}
                  onClick={() => setSelectedWorkflow(workflow)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-white font-medium">{workflow.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      workflow.status === 'active' 
                        ? 'bg-green-500/20 text-green-400' 
                        : 'bg-gray-500/20 text-gray-400'
                    }`}>
                      {workflow.status}
                    </span>
                  </div>
                  
                  <p className="text-white/60 text-sm mb-3">
                    {workflow.description}
                  </p>
                  
                  <div className="flex items-center justify-between text-xs text-white/50">
                    <span>{workflow.steps} steps</span>
                    <span>
                      {workflow.lastRun ? `Last run: ${workflow.lastRun}` : 'Never run'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Workflow Canvas */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="lg:col-span-2 glass-card p-6"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">
                {selectedWorkflow ? selectedWorkflow.name : 'Workflow Canvas'}
              </h2>
              
              {selectedWorkflow && (
                <div className="flex space-x-2">
                  <Button variant="ghost" size="sm" className="btn-glass">
                    <Save className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="btn-glass">
                    <Settings className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="btn-glass">
                    <Play className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>

            {selectedWorkflow ? (
              <div className="workflow-canvas bg-white/5 rounded-lg p-8 min-h-96 relative overflow-hidden">
                {/* Workflow Steps */}
                {workflowSteps.map((step, index) => (
                  <motion.div
                    key={step.id}
                    className="absolute"
                    style={{ left: step.x, top: step.y }}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className={`p-4 rounded-lg bg-gradient-to-r ${getStepColor(step.type)} text-white text-center min-w-32 shadow-lg`}>
                      <div className="font-medium text-sm">{step.name}</div>
                      <div className="text-xs opacity-80 mt-1">{step.type}</div>
                    </div>
                  </motion.div>
                ))}

                {/* Connection Lines */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none">
                  {workflowSteps.slice(0, -1).map((step, index) => {
                    const nextStep = workflowSteps[index + 1]
                    return (
                      <motion.line
                        key={`line-${index}`}
                        x1={step.x + 64}
                        y1={step.y + 25}
                        x2={nextStep.x}
                        y2={nextStep.y + 25}
                        stroke="rgba(255,255,255,0.3)"
                        strokeWidth="2"
                        strokeDasharray="5,5"
                        initial={{ pathLength: 0 }}
                        animate={{ pathLength: 1 }}
                        transition={{ delay: 0.5 + index * 0.2, duration: 0.5 }}
                      />
                    )
                  })}
                </svg>

                {/* Floating Action Button */}
                <motion.div
                  className="absolute bottom-4 right-4"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <Button className="rounded-full w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600">
                    <Plus className="h-5 w-5" />
                  </Button>
                </motion.div>
              </div>
            ) : (
              <div className="bg-white/5 rounded-lg p-12 text-center min-h-96 flex items-center justify-center">
                <div>
                  <Workflow className="h-16 w-16 text-white/30 mx-auto mb-4" />
                  <p className="text-white/50 text-lg mb-4">Select a workflow to edit</p>
                  <p className="text-white/30 text-sm">
                    Choose from your existing workflows or create a new one
                  </p>
                </div>
              </div>
            )}
          </motion.div>
        </div>

        {/* Workflow Templates */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-8"
        >
          <h2 className="text-2xl font-bold text-white mb-6">Workflow Templates</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                name: 'Document Processing',
                description: 'Upload → Validate → Process → Output',
                steps: 4,
                color: 'from-blue-500 to-cyan-500'
              },
              {
                name: 'Image Analysis',
                description: 'Upload → Analyze → Extract → Report',
                steps: 4,
                color: 'from-purple-500 to-pink-500'
              },
              {
                name: 'Data Pipeline',
                description: 'Import → Clean → Transform → Export',
                steps: 4,
                color: 'from-green-500 to-emerald-500'
              }
            ].map((template, index) => (
              <motion.div
                key={index}
                className="glass-card p-6 glass-card-hover"
                whileHover={{ scale: 1.02 }}
                transition={{ duration: 0.3 }}
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${template.color} flex items-center justify-center mb-4`}>
                  <Workflow className="h-6 w-6 text-white" />
                </div>
                
                <h3 className="text-lg font-semibold text-white mb-2">
                  {template.name}
                </h3>
                
                <p className="text-white/70 text-sm mb-4">
                  {template.description}
                </p>
                
                <div className="flex justify-between items-center">
                  <span className="text-white/50 text-xs">
                    {template.steps} steps
                  </span>
                  <Button variant="ghost" size="sm" className="btn-glass">
                    Use Template
                  </Button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default WorkflowBuilder

