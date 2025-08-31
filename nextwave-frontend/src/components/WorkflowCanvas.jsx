import React, { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Play, 
  Pause, 
  Square, 
  Plus, 
  Settings, 
  Trash2, 
  ArrowRight,
  Zap,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '../contexts/AuthContext'

const WorkflowCanvas = ({ workflow, onWorkflowUpdate, onExecute }) => {
  const [nodes, setNodes] = useState([])
  const [connections, setConnections] = useState([])
  const [selectedNode, setSelectedNode] = useState(null)
  const [isExecuting, setIsExecuting] = useState(false)
  const [executionStatus, setExecutionStatus] = useState({})
  const [animationQueue, setAnimationQueue] = useState([])
  const canvasRef = useRef(null)
  const { apiCall } = useAuth()

  // Node types with their configurations
  const nodeTypes = {
    input: {
      color: 'from-blue-500 to-cyan-500',
      icon: <Plus className="h-4 w-4" />,
      label: 'Input'
    },
    processing: {
      color: 'from-purple-500 to-pink-500',
      icon: <Zap className="h-4 w-4" />,
      label: 'Process'
    },
    validation: {
      color: 'from-yellow-500 to-orange-500',
      icon: <CheckCircle className="h-4 w-4" />,
      label: 'Validate'
    },
    output: {
      color: 'from-green-500 to-emerald-500',
      icon: <ArrowRight className="h-4 w-4" />,
      label: 'Output'
    },
    condition: {
      color: 'from-indigo-500 to-purple-500',
      icon: <Settings className="h-4 w-4" />,
      label: 'Condition'
    }
  }

  // Initialize workflow nodes
  useEffect(() => {
    if (workflow && workflow.steps) {
      const workflowNodes = Object.values(workflow.steps).map(step => ({
        id: step.id,
        type: step.type,
        name: step.name,
        x: Math.random() * 600 + 100,
        y: Math.random() * 400 + 100,
        status: 'idle',
        config: step.config || {}
      }))
      setNodes(workflowNodes)

      // Create connections based on next_steps
      const workflowConnections = []
      Object.values(workflow.steps).forEach(step => {
        if (step.next_steps && step.next_steps.length > 0) {
          step.next_steps.forEach(nextStepId => {
            workflowConnections.push({
              id: `${step.id}-${nextStepId}`,
              from: step.id,
              to: nextStepId,
              animated: false
            })
          })
        }
      })
      setConnections(workflowConnections)
    }
  }, [workflow])

  // Animation functions
  const animateConnection = useCallback((connectionId, duration = 1000) => {
    setConnections(prev => prev.map(conn => 
      conn.id === connectionId 
        ? { ...conn, animated: true }
        : conn
    ))

    setTimeout(() => {
      setConnections(prev => prev.map(conn => 
        conn.id === connectionId 
          ? { ...conn, animated: false }
          : conn
      ))
    }, duration)
  }, [])

  const updateNodeStatus = useCallback((nodeId, status) => {
    setNodes(prev => prev.map(node => 
      node.id === nodeId 
        ? { ...node, status }
        : node
    ))
  }, [])

  // Execute workflow with animation
  const executeWorkflow = async () => {
    if (!workflow || isExecuting) return

    setIsExecuting(true)
    setExecutionStatus({})

    try {
      // Start execution
      const response = await apiCall(`/workflows/${workflow.id}/execute`, {
        method: 'POST',
        body: JSON.stringify({
          input_data: {
            document_type: 'pdf',
            document_file: 'sample.pdf'
          }
        })
      })

      if (response.ok) {
        const data = await response.json()
        const executionId = data.execution_id

        // Poll for execution status and animate
        const pollExecution = async () => {
          try {
            const statusResponse = await apiCall(`/workflows/executions/${executionId}`)
            if (statusResponse.ok) {
              const statusData = await statusResponse.json()
              const execution = statusData.execution

              // Update execution status
              setExecutionStatus(execution)

              // Animate current step
              if (execution.current_step) {
                updateNodeStatus(execution.current_step.id, 'running')
              }

              // Animate completed steps
              execution.steps_executed.forEach(step => {
                updateNodeStatus(step.id, step.status)
                
                // Animate connections from completed steps
                const outgoingConnections = connections.filter(conn => conn.from === step.id)
                outgoingConnections.forEach(conn => {
                  setTimeout(() => animateConnection(conn.id), 500)
                })
              })

              // Continue polling if still running
              if (execution.status === 'running') {
                setTimeout(pollExecution, 1000)
              } else {
                setIsExecuting(false)
                // Reset all nodes to idle after completion
                setTimeout(() => {
                  setNodes(prev => prev.map(node => ({ ...node, status: 'idle' })))
                }, 3000)
              }
            }
          } catch (error) {
            console.error('Error polling execution:', error)
            setIsExecuting(false)
          }
        }

        // Start polling
        setTimeout(pollExecution, 500)
      }
    } catch (error) {
      console.error('Error executing workflow:', error)
      setIsExecuting(false)
    }
  }

  // Node component
  const WorkflowNode = ({ node, onSelect, onMove }) => {
    const nodeType = nodeTypes[node.type] || nodeTypes.processing
    const [isDragging, setIsDragging] = useState(false)

    const getStatusColor = (status) => {
      switch (status) {
        case 'running':
          return 'ring-2 ring-blue-400 ring-opacity-75'
        case 'completed':
          return 'ring-2 ring-green-400 ring-opacity-75'
        case 'failed':
          return 'ring-2 ring-red-400 ring-opacity-75'
        default:
          return ''
      }
    }

    const getStatusIcon = (status) => {
      switch (status) {
        case 'running':
          return <Clock className="h-3 w-3 text-blue-400 animate-spin" />
        case 'completed':
          return <CheckCircle className="h-3 w-3 text-green-400" />
        case 'failed':
          return <AlertCircle className="h-3 w-3 text-red-400" />
        default:
          return null
      }
    }

    return (
      <motion.div
        className={`absolute cursor-pointer ${getStatusColor(node.status)}`}
        style={{ left: node.x, top: node.y }}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        drag
        dragMomentum={false}
        onDragStart={() => setIsDragging(true)}
        onDragEnd={(event, info) => {
          setIsDragging(false)
          onMove(node.id, node.x + info.offset.x, node.y + info.offset.y)
        }}
        onClick={() => !isDragging && onSelect(node)}
      >
        <div className={`p-4 rounded-lg bg-gradient-to-r ${nodeType.color} text-white shadow-lg min-w-32 text-center relative`}>
          {/* Status indicator */}
          {node.status !== 'idle' && (
            <div className="absolute -top-2 -right-2 bg-white rounded-full p-1">
              {getStatusIcon(node.status)}
            </div>
          )}
          
          {/* Node icon */}
          <div className="flex justify-center mb-2">
            {nodeType.icon}
          </div>
          
          {/* Node name */}
          <div className="font-medium text-sm">{node.name}</div>
          <div className="text-xs opacity-80 mt-1">{nodeType.label}</div>
          
          {/* Pulse animation for running nodes */}
          {node.status === 'running' && (
            <motion.div
              className="absolute inset-0 rounded-lg bg-blue-400 opacity-30"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            />
          )}
        </div>
      </motion.div>
    )
  }

  // Connection component
  const Connection = ({ connection, nodes }) => {
    const fromNode = nodes.find(n => n.id === connection.from)
    const toNode = nodes.find(n => n.id === connection.to)

    if (!fromNode || !toNode) return null

    const startX = fromNode.x + 64 // Half of node width
    const startY = fromNode.y + 25 // Half of node height
    const endX = toNode.x
    const endY = toNode.y + 25

    return (
      <motion.line
        x1={startX}
        y1={startY}
        x2={endX}
        y2={endY}
        stroke={connection.animated ? "#3b82f6" : "rgba(255,255,255,0.3)"}
        strokeWidth={connection.animated ? "3" : "2"}
        strokeDasharray={connection.animated ? "0" : "5,5"}
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 0.5 }}
      >
        {connection.animated && (
          <motion.animate
            attributeName="stroke-dasharray"
            values="0 10;5 5;10 0"
            dur="1s"
            repeatCount="3"
          />
        )}
      </motion.line>
    )
  }

  // Handle node movement
  const handleNodeMove = (nodeId, newX, newY) => {
    setNodes(prev => prev.map(node => 
      node.id === nodeId 
        ? { ...node, x: newX, y: newY }
        : node
    ))
  }

  // Add new node
  const addNode = (type, x = 200, y = 200) => {
    const newNode = {
      id: `node_${Date.now()}`,
      type,
      name: `New ${nodeTypes[type].label}`,
      x,
      y,
      status: 'idle',
      config: {}
    }
    setNodes(prev => [...prev, newNode])
  }

  return (
    <div className="relative w-full h-full bg-white/5 rounded-lg overflow-hidden">
      {/* Canvas */}
      <div 
        ref={canvasRef}
        className="relative w-full h-full workflow-canvas"
        style={{ minHeight: '600px' }}
      >
        {/* SVG for connections */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none">
          {connections.map(connection => (
            <Connection 
              key={connection.id} 
              connection={connection} 
              nodes={nodes} 
            />
          ))}
        </svg>

        {/* Nodes */}
        <AnimatePresence>
          {nodes.map(node => (
            <WorkflowNode
              key={node.id}
              node={node}
              onSelect={setSelectedNode}
              onMove={handleNodeMove}
            />
          ))}
        </AnimatePresence>

        {/* Execution Controls */}
        <div className="absolute top-4 right-4 flex space-x-2">
          <Button
            onClick={executeWorkflow}
            disabled={isExecuting}
            className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
          >
            {isExecuting ? (
              <>
                <Clock className="h-4 w-4 mr-2 animate-spin" />
                Running...
              </>
            ) : (
              <>
                <Play className="h-4 w-4 mr-2" />
                Execute
              </>
            )}
          </Button>
          
          {isExecuting && (
            <Button
              variant="ghost"
              className="btn-glass"
              onClick={() => setIsExecuting(false)}
            >
              <Square className="h-4 w-4" />
            </Button>
          )}
        </div>

        {/* Node Palette */}
        <div className="absolute bottom-4 left-4 flex space-x-2">
          {Object.entries(nodeTypes).map(([type, config]) => (
            <motion.button
              key={type}
              className={`p-3 rounded-lg bg-gradient-to-r ${config.color} text-white shadow-lg`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => addNode(type)}
              title={`Add ${config.label} Node`}
            >
              {config.icon}
            </motion.button>
          ))}
        </div>

        {/* Execution Status */}
        {executionStatus && executionStatus.status && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute bottom-4 right-4 glass-card p-4 max-w-sm"
          >
            <h4 className="text-white font-medium mb-2">Execution Status</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-white/70">Status:</span>
                <span className={`font-medium ${
                  executionStatus.status === 'completed' ? 'text-green-400' :
                  executionStatus.status === 'failed' ? 'text-red-400' :
                  executionStatus.status === 'running' ? 'text-blue-400' :
                  'text-white'
                }`}>
                  {executionStatus.status}
                </span>
              </div>
              {executionStatus.current_step && (
                <div className="flex justify-between">
                  <span className="text-white/70">Current:</span>
                  <span className="text-white">{executionStatus.current_step.name}</span>
                </div>
              )}
              {executionStatus.steps_executed && (
                <div className="flex justify-between">
                  <span className="text-white/70">Progress:</span>
                  <span className="text-white">
                    {executionStatus.steps_executed.length} / {Object.keys(workflow?.steps || {}).length}
                  </span>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </div>

      {/* Node Properties Panel */}
      <AnimatePresence>
        {selectedNode && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="absolute top-0 right-0 w-80 h-full glass-card p-6 border-l border-white/10"
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-white">Node Properties</h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedNode(null)}
                className="text-white/70 hover:text-white"
              >
                ×
              </Button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-white/70 text-sm font-medium mb-2">
                  Name
                </label>
                <input
                  type="text"
                  value={selectedNode.name}
                  onChange={(e) => {
                    const updatedNode = { ...selectedNode, name: e.target.value }
                    setSelectedNode(updatedNode)
                    setNodes(prev => prev.map(node => 
                      node.id === selectedNode.id ? updatedNode : node
                    ))
                  }}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-md text-white placeholder-white/50 focus:border-blue-400 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-white/70 text-sm font-medium mb-2">
                  Type
                </label>
                <div className={`p-3 rounded-lg bg-gradient-to-r ${nodeTypes[selectedNode.type].color} text-white text-center`}>
                  {nodeTypes[selectedNode.type].label}
                </div>
              </div>

              <div>
                <label className="block text-white/70 text-sm font-medium mb-2">
                  Status
                </label>
                <div className="text-white capitalize">{selectedNode.status}</div>
              </div>

              <div className="pt-4 border-t border-white/10">
                <Button
                  variant="ghost"
                  className="w-full btn-glass text-red-400 hover:text-red-300"
                  onClick={() => {
                    setNodes(prev => prev.filter(node => node.id !== selectedNode.id))
                    setConnections(prev => prev.filter(conn => 
                      conn.from !== selectedNode.id && conn.to !== selectedNode.id
                    ))
                    setSelectedNode(null)
                  }}
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete Node
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default WorkflowCanvas

