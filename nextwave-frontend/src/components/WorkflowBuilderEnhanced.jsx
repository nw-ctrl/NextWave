import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Plus, 
  Save, 
  Play, 
  Settings, 
  Layers, 
  Zap,
  FileText,
  Image,
  GitBranch,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '../contexts/AuthContext'
import WorkflowCanvas from './WorkflowCanvas'

const WorkflowBuilderEnhanced = () => {
  const [workflows, setWorkflows] = useState([])
  const [selectedWorkflow, setSelectedWorkflow] = useState(null)
  const [isCreating, setIsCreating] = useState(false)
  const [newWorkflowName, setNewWorkflowName] = useState('')
  const [executions, setExecutions] = useState([])
  const [activeTab, setActiveTab] = useState('builder')
  const { user, apiCall } = useAuth()

  // Load workflows on component mount
  useEffect(() => {
    loadWorkflows()
  }, [])

  const loadWorkflows = async () => {
    try {
      const response = await apiCall('/workflows')
      if (response.ok) {
        const data = await response.json()
        setWorkflows(data.workflows || [])
        
        // Select first workflow if available
        if (data.workflows && data.workflows.length > 0) {
          setSelectedWorkflow(data.workflows[0])
        }
      }
    } catch (error) {
      console.error('Error loading workflows:', error)
    }
  }

  const createWorkflow = async () => {
    if (!newWorkflowName.trim()) return

    try {
      const response = await apiCall('/workflows', {
        method: 'POST',
        body: JSON.stringify({
          name: newWorkflowName,
          description: `Workflow created by ${user?.username || 'user'}`
        })
      })

      if (response.ok) {
        const data = await response.json()
        setWorkflows(prev => [...prev, data.workflow])
        setSelectedWorkflow(data.workflow)
        setNewWorkflowName('')
        setIsCreating(false)
      }
    } catch (error) {
      console.error('Error creating workflow:', error)
    }
  }

  const executeWorkflow = async (workflowId) => {
    try {
      const response = await apiCall(`/workflows/${workflowId}/execute`, {
        method: 'POST',
        body: JSON.stringify({
          input_data: {
            document_type: 'pdf',
            document_file: 'sample.pdf',
            image_format: 'png'
          }
        })
      })

      if (response.ok) {
        const data = await response.json()
        // Add to executions list
        setExecutions(prev => [{
          id: data.execution_id,
          workflow_id: workflowId,
          status: 'running',
          started_at: new Date().toISOString()
        }, ...prev])
      }
    } catch (error) {
      console.error('Error executing workflow:', error)
    }
  }

  // Sample workflow templates
  const workflowTemplates = [
    {
      name: 'Document Processing Pipeline',
      description: 'Upload, validate, and process documents with AI analysis',
      icon: <FileText className="h-5 w-5" />,
      color: 'from-blue-500 to-cyan-500',
      steps: ['Upload', 'Validate', 'Extract Text', 'Generate Report']
    },
    {
      name: 'Image Analysis Workflow',
      description: 'AI-powered image analysis with detailed reporting',
      icon: <Image className="h-5 w-5" />,
      color: 'from-purple-500 to-pink-500',
      steps: ['Upload Image', 'Analyze Colors', 'Detect Objects', 'Create Report']
    },
    {
      name: 'Data Transformation Flow',
      description: 'Transform and validate data through multiple stages',
      icon: <GitBranch className="h-5 w-5" />,
      color: 'from-green-500 to-emerald-500',
      steps: ['Input Data', 'Transform', 'Validate', 'Output']
    }
  ]

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running':
        return <Clock className="h-4 w-4 text-blue-400 animate-spin" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      case 'failed':
        return <AlertTriangle className="h-4 w-4 text-red-400" />
      default:
        return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">Workflow Builder</h2>
          <p className="text-white/70">Create and manage automated workflows with visual flow simulation</p>
        </div>
        
        <Button
          onClick={() => setIsCreating(true)}
          className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          New Workflow
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 glass-card p-1 w-fit">
        {[
          { id: 'builder', label: 'Builder', icon: <Layers className="h-4 w-4" /> },
          { id: 'templates', label: 'Templates', icon: <Settings className="h-4 w-4" /> },
          { id: 'executions', label: 'Executions', icon: <Zap className="h-4 w-4" /> }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all ${
              activeTab === tab.id
                ? 'bg-white/20 text-white'
                : 'text-white/70 hover:text-white hover:bg-white/10'
            }`}
          >
            {tab.icon}
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'builder' && (
          <motion.div
            key="builder"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {/* Workflow Selection */}
            <div className="glass-card p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-white">Select Workflow</h3>
                {selectedWorkflow && (
                  <Button
                    onClick={() => executeWorkflow(selectedWorkflow.id)}
                    className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Execute
                  </Button>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {workflows.map(workflow => (
                  <motion.div
                    key={workflow.id}
                    className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                      selectedWorkflow?.id === workflow.id
                        ? 'border-blue-400 bg-blue-500/20'
                        : 'border-white/20 bg-white/5 hover:border-white/40'
                    }`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setSelectedWorkflow(workflow)}
                  >
                    <h4 className="text-white font-medium mb-2">{workflow.name}</h4>
                    <p className="text-white/70 text-sm mb-3">{workflow.description}</p>
                    <div className="flex justify-between items-center text-xs text-white/50">
                      <span>Steps: {Object.keys(workflow.steps || {}).length}</span>
                      <span>v{workflow.version}</span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Workflow Canvas */}
            {selectedWorkflow && (
              <div className="glass-card p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-white">{selectedWorkflow.name}</h3>
                  <div className="flex space-x-2">
                    <Button variant="ghost" className="btn-glass">
                      <Save className="h-4 w-4 mr-2" />
                      Save
                    </Button>
                    <Button variant="ghost" className="btn-glass">
                      <Settings className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="h-96 rounded-lg overflow-hidden">
                  <WorkflowCanvas
                    workflow={selectedWorkflow}
                    onWorkflowUpdate={setSelectedWorkflow}
                    onExecute={executeWorkflow}
                  />
                </div>
              </div>
            )}
          </motion.div>
        )}

        {activeTab === 'templates' && (
          <motion.div
            key="templates"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass-card p-6"
          >
            <h3 className="text-lg font-semibold text-white mb-6">Workflow Templates</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {workflowTemplates.map((template, index) => (
                <motion.div
                  key={index}
                  className="glass-card p-6 hover:bg-white/10 transition-all cursor-pointer"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${template.color} flex items-center justify-center mb-4`}>
                    {template.icon}
                  </div>
                  
                  <h4 className="text-white font-semibold mb-2">{template.name}</h4>
                  <p className="text-white/70 text-sm mb-4">{template.description}</p>
                  
                  <div className="space-y-2 mb-4">
                    {template.steps.map((step, stepIndex) => (
                      <div key={stepIndex} className="flex items-center space-x-2 text-sm text-white/60">
                        <div className="w-2 h-2 rounded-full bg-white/40"></div>
                        <span>{step}</span>
                      </div>
                    ))}
                  </div>
                  
                  <Button className="w-full btn-glass">
                    Use Template
                  </Button>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {activeTab === 'executions' && (
          <motion.div
            key="executions"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass-card p-6"
          >
            <h3 className="text-lg font-semibold text-white mb-6">Execution History</h3>
            
            {executions.length === 0 ? (
              <div className="text-center py-12">
                <Zap className="h-12 w-12 text-white/30 mx-auto mb-4" />
                <p className="text-white/70">No executions yet</p>
                <p className="text-white/50 text-sm">Execute a workflow to see results here</p>
              </div>
            ) : (
              <div className="space-y-4">
                {executions.map(execution => (
                  <motion.div
                    key={execution.id}
                    className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                  >
                    <div className="flex items-center space-x-4">
                      {getStatusIcon(execution.status)}
                      <div>
                        <div className="text-white font-medium">
                          Execution #{execution.id.slice(0, 8)}
                        </div>
                        <div className="text-white/60 text-sm">
                          Started: {new Date(execution.started_at).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        execution.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                        execution.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {execution.status}
                      </span>
                      
                      <Button variant="ghost" size="sm" className="btn-glass">
                        View Details
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Create Workflow Modal */}
      <AnimatePresence>
        {isCreating && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={() => setIsCreating(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="glass-card p-6 w-full max-w-md mx-4"
              onClick={e => e.stopPropagation()}
            >
              <h3 className="text-lg font-semibold text-white mb-4">Create New Workflow</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-white/70 text-sm font-medium mb-2">
                    Workflow Name
                  </label>
                  <input
                    type="text"
                    value={newWorkflowName}
                    onChange={(e) => setNewWorkflowName(e.target.value)}
                    placeholder="Enter workflow name..."
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-md text-white placeholder-white/50 focus:border-blue-400 focus:outline-none"
                    autoFocus
                  />
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <Button
                    onClick={createWorkflow}
                    disabled={!newWorkflowName.trim()}
                    className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
                  >
                    Create
                  </Button>
                  <Button
                    variant="ghost"
                    onClick={() => setIsCreating(false)}
                    className="flex-1 btn-glass"
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default WorkflowBuilderEnhanced

