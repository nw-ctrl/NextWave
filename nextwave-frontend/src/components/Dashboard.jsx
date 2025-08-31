import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  FileText, 
  Image, 
  Workflow, 
  BarChart3,
  Plus,
  Clock,
  CheckCircle,
  AlertCircle,
  TrendingUp
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '../contexts/AuthContext'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    documents: 0,
    images: 0,
    workflows: 0,
    processing: 0
  })
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate loading dashboard data
    const loadDashboardData = async () => {
      try {
        // In a real app, you would fetch this data from your API
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        setStats({
          documents: 12,
          images: 8,
          workflows: 3,
          processing: 2
        })

        setRecentActivity([
          {
            id: 1,
            type: 'document',
            action: 'uploaded',
            name: 'Annual Report 2024.pdf',
            time: '2 hours ago',
            status: 'completed'
          },
          {
            id: 2,
            type: 'image',
            action: 'analyzed',
            name: 'product_image_01.jpg',
            time: '4 hours ago',
            status: 'completed'
          },
          {
            id: 3,
            type: 'workflow',
            action: 'executed',
            name: 'Document Processing Flow',
            time: '1 day ago',
            status: 'completed'
          },
          {
            id: 4,
            type: 'document',
            action: 'processing',
            name: 'Contract_v2.docx',
            time: '2 days ago',
            status: 'processing'
          }
        ])
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadDashboardData()
  }, [])

  const quickActions = [
    {
      title: 'Upload Document',
      description: 'Process PDF, Word, or Visio files',
      icon: <FileText className="h-8 w-8" />,
      link: '/documents',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Analyze Image',
      description: 'AI-powered image analysis',
      icon: <Image className="h-8 w-8" />,
      link: '/images',
      color: 'from-purple-500 to-pink-500'
    },
    {
      title: 'Create Workflow',
      description: 'Build automated processes',
      icon: <Workflow className="h-8 w-8" />,
      link: '/workflows',
      color: 'from-green-500 to-emerald-500'
    }
  ]

  const statCards = [
    {
      title: 'Documents',
      value: stats.documents,
      icon: <FileText className="h-6 w-6" />,
      color: 'text-blue-400',
      bgColor: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      title: 'Images',
      value: stats.images,
      icon: <Image className="h-6 w-6" />,
      color: 'text-purple-400',
      bgColor: 'from-purple-500/20 to-pink-500/20'
    },
    {
      title: 'Workflows',
      value: stats.workflows,
      icon: <Workflow className="h-6 w-6" />,
      color: 'text-green-400',
      bgColor: 'from-green-500/20 to-emerald-500/20'
    },
    {
      title: 'Processing',
      value: stats.processing,
      icon: <Clock className="h-6 w-6" />,
      color: 'text-orange-400',
      bgColor: 'from-orange-500/20 to-red-500/20'
    }
  ]

  const getActivityIcon = (type) => {
    switch (type) {
      case 'document':
        return <FileText className="h-5 w-5" />
      case 'image':
        return <Image className="h-5 w-5" />
      case 'workflow':
        return <Workflow className="h-5 w-5" />
      default:
        return <BarChart3 className="h-5 w-5" />
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      case 'processing':
        return <Clock className="h-4 w-4 text-orange-400" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-400" />
      default:
        return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-white/70">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            Welcome back, {user?.first_name || user?.username}!
          </h1>
          <p className="text-white/70 text-lg">
            Here's what's happening with your NextWave account today.
          </p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {statCards.map((stat, index) => (
            <motion.div
              key={index}
              className="glass-card p-6 glass-card-hover"
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.3 }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/70 text-sm font-medium mb-1">
                    {stat.title}
                  </p>
                  <p className="text-3xl font-bold text-white">
                    {stat.value}
                  </p>
                </div>
                <div className={`p-3 rounded-full bg-gradient-to-r ${stat.bgColor}`}>
                  <div className={stat.color}>
                    {stat.icon}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="lg:col-span-2"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {quickActions.map((action, index) => (
                <Link key={index} to={action.link}>
                  <motion.div
                    className="glass-card p-6 glass-card-hover text-center"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-r ${action.color} mb-4`}>
                      <div className="text-white">
                        {action.icon}
                      </div>
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {action.title}
                    </h3>
                    <p className="text-white/70 text-sm mb-4">
                      {action.description}
                    </p>
                    <Button
                      variant="ghost"
                      className="btn-glass w-full"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Get Started
                    </Button>
                  </motion.div>
                </Link>
              ))}
            </div>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <h2 className="text-2xl font-bold text-white mb-6">Recent Activity</h2>
            <div className="glass-card p-6">
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 p-2 rounded-full bg-white/10">
                      <div className="text-white/70">
                        {getActivityIcon(activity.type)}
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm font-medium">
                        {activity.name}
                      </p>
                      <p className="text-white/60 text-xs">
                        {activity.action} • {activity.time}
                      </p>
                    </div>
                    <div className="flex-shrink-0">
                      {getStatusIcon(activity.status)}
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 pt-4 border-t border-white/10">
                <Button
                  variant="ghost"
                  className="w-full btn-glass text-sm"
                >
                  View All Activity
                </Button>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Performance Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-8"
        >
          <div className="glass-card p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Performance Overview</h2>
              <TrendingUp className="h-6 w-6 text-green-400" />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold gradient-text-blue mb-2">
                  98.5%
                </div>
                <p className="text-white/70 text-sm">Success Rate</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold gradient-text-blue mb-2">
                  2.3s
                </div>
                <p className="text-white/70 text-sm">Avg Processing Time</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold gradient-text-blue mb-2">
                  23
                </div>
                <p className="text-white/70 text-sm">Total Tasks This Month</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard

