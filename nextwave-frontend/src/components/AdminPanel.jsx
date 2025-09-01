import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  FileText, 
  Image, 
  Activity, 
  Settings, 
  Shield,
  BarChart3,
  AlertTriangle,
  CheckCircle,
  Clock,
  Mail
} from 'lucide-react'
import { Button } from "@/components/ui/button"
import { useAuth } from "@/contexts/AuthContext"

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('overview')

  const adminStats = {
    totalUsers: 1247,
    activeUsers: 892,
    documentsProcessed: 15420,
    imagesAnalyzed: 8934,
    systemUptime: '99.9%',
    storageUsed: '2.4 TB'
  }

  const recentUsers = [
    { id: 1, name: 'John Smith', email: 'john@example.com', role: 'user', status: 'active', joinedAt: '2024-01-15' },
    { id: 2, name: 'Sarah Johnson', email: 'sarah@example.com', role: 'user', status: 'active', joinedAt: '2024-01-14' },
    { id: 3, name: 'Mike Wilson', email: 'mike@example.com', role: 'admin', status: 'active', joinedAt: '2024-01-13' }
  ]

  const systemLogs = [
    { id: 1, type: 'info', message: 'System backup completed successfully', timestamp: '2024-01-15 10:30:00' },
    { id: 2, type: 'warning', message: 'High CPU usage detected on server-02', timestamp: '2024-01-15 09:15:00' },
    { id: 3, type: 'error', message: 'Failed to process document: timeout error', timestamp: '2024-01-15 08:45:00' },
    { id: 4, type: 'info', message: 'New user registration: john@example.com', timestamp: '2024-01-15 08:20:00' }
  ]

  const tabs = [
    { id: 'overview', name: 'Overview', icon: <BarChart3 className="h-4 w-4" /> },
    { id: 'users', name: 'Users', icon: <Users className="h-4 w-4" /> },
    { id: 'contacts', name: 'Contact Submissions', icon: <Mail className="h-4 w-4" /> },
    { id: 'system', name: 'System', icon: <Settings className="h-4 w-4" /> },
    { id: 'logs', name: 'Logs', icon: <Activity className="h-4 w-4" /> }
  ]

  const getLogIcon = (type) => {
    switch (type) {
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-400" />
      case 'warning':
        return <Clock className="h-4 w-4 text-yellow-400" />
      case 'info':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      default:
        return <Activity className="h-4 w-4 text-blue-400" />
    }
  }

  const renderOverview = () => (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          { title: 'Total Users', value: adminStats.totalUsers, icon: <Users className="h-6 w-6" />, color: 'text-blue-400' },
          { title: 'Active Users', value: adminStats.activeUsers, icon: <Users className="h-6 w-6" />, color: 'text-green-400' },
          { title: 'Documents Processed', value: adminStats.documentsProcessed, icon: <FileText className="h-6 w-6" />, color: 'text-purple-400' },
          { title: 'Images Analyzed', value: adminStats.imagesAnalyzed, icon: <Image className="h-6 w-6" />, color: 'text-pink-400' },
          { title: 'System Uptime', value: adminStats.systemUptime, icon: <Activity className="h-6 w-6" />, color: 'text-green-400' },
          { title: 'Storage Used', value: adminStats.storageUsed, icon: <BarChart3 className="h-6 w-6" />, color: 'text-orange-400' }
        ].map((stat, index) => (
          <motion.div
            key={index}
            className="admin-card p-6"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/70 text-sm font-medium mb-1">{stat.title}</p>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
              </div>
              <div className={stat.color}>
                {stat.icon}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="admin-card p-6">
        <h3 className="text-xl font-bold text-white mb-6">Recent Activity</h3>
        <div className="space-y-4">
          {systemLogs.slice(0, 5).map((log) => (
            <div key={log.id} className="flex items-start space-x-3 p-3 bg-white/5 rounded-lg">
              {getLogIcon(log.type)}
              <div className="flex-1">
                <p className="text-white text-sm">{log.message}</p>
                <p className="text-white/50 text-xs mt-1">{log.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  const renderUsers = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-bold text-white">User Management</h3>
        <Button className="bg-gradient-to-r from-blue-500 to-purple-600">
          Add User
        </Button>
      </div>

      <div className="admin-card p-6">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left text-white/70 font-medium py-3">Name</th>
                <th className="text-left text-white/70 font-medium py-3">Email</th>
                <th className="text-left text-white/70 font-medium py-3">Role</th>
                <th className="text-left text-white/70 font-medium py-3">Status</th>
                <th className="text-left text-white/70 font-medium py-3">Joined</th>
                <th className="text-left text-white/70 font-medium py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {recentUsers.map((user) => (
                <tr key={user.id} className="border-b border-white/5">
                  <td className="py-4 text-white">{user.name}</td>
                  <td className="py-4 text-white/80">{user.email}</td>
                  <td className="py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      user.role === 'admin' 
                        ? 'bg-purple-500/20 text-purple-400' 
                        : 'bg-blue-500/20 text-blue-400'
                    }`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="py-4">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-400">
                      {user.status}
                    </span>
                  </td>
                  <td className="py-4 text-white/60">{user.joinedAt}</td>
                  <td className="py-4">
                    <div className="flex space-x-2">
                      <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">
                        Edit
                      </Button>
                      <Button variant="ghost" size="sm" className="text-white/70 hover:text-red-400">
                        Delete
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )

  const renderSystem = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-bold text-white">System Configuration</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="admin-card p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Server Status</h4>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-white/70">CPU Usage</span>
              <span className="text-white">45%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/70">Memory Usage</span>
              <span className="text-white">62%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/70">Disk Usage</span>
              <span className="text-white">78%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/70">Network I/O</span>
              <span className="text-green-400">Normal</span>
            </div>
          </div>
        </div>

        <div className="admin-card p-6">
          <h4 className="text-lg font-semibold text-white mb-4">System Settings</h4>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-white/70">Maintenance Mode</span>
              <Button variant="ghost" size="sm" className="btn-glass">
                Disabled
              </Button>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/70">Auto Backup</span>
              <Button variant="ghost" size="sm" className="btn-glass">
                Enabled
              </Button>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/70">Debug Mode</span>
              <Button variant="ghost" size="sm" className="btn-glass">
                Disabled
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  const renderLogs = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-bold text-white">System Logs</h3>
        <div className="flex space-x-2">
          <Button variant="ghost" size="sm" className="btn-glass">
            Filter
          </Button>
          <Button variant="ghost" size="sm" className="btn-glass">
            Export
          </Button>
        </div>
      </div>

      <div className="admin-card p-6">
        <div className="space-y-3">
          {systemLogs.map((log) => (
            <div key={log.id} className="flex items-start space-x-3 p-3 bg-white/5 rounded-lg">
              {getLogIcon(log.type)}
              <div className="flex-1">
                <div className="flex justify-between items-start">
                  <p className="text-white text-sm">{log.message}</p>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    log.type === 'error' ? 'bg-red-500/20 text-red-400' :
                    log.type === 'warning' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-green-500/20 text-green-400'
                  }`}>
                    {log.type}
                  </span>
                </div>
                <p className="text-white/50 text-xs mt-1">{log.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  const renderContacts = () => {
    const { apiCall } = useAuth();
    const [contacts, setContacts] = useState([]);
    const [loadingContacts, setLoadingContacts] = useState(true);
    const [errorContacts, setErrorContacts] = useState(null);

    useEffect(() => {
      const fetchContacts = async () => {
        try {
          setLoadingContacts(true);
          const response = await apiCall('/admin/contacts');
          if (response.ok) {
            const data = await response.json();
            setContacts(data.contacts);
          } else {
            setErrorContacts('Failed to fetch contact submissions.');
          }
        } catch (error) {
          setErrorContacts('Network error: ' + error.message);
        } finally {
          setLoadingContacts(false);
        }
      };
      fetchContacts();
    }, [apiCall]);

    if (loadingContacts) {
      return <div className="text-white">Loading contact submissions...</div>;
    }

    if (errorContacts) {
      return <div className="text-red-400">Error: {errorContacts}</div>;
    }

    return (
      <div className="space-y-6">
        <h3 className="text-xl font-bold text-white">Contact Submissions</h3>
        <div className="admin-card p-6">
          {contacts.length === 0 ? (
            <p className="text-white/70">No contact submissions found.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="text-left text-white/70 font-medium py-3">Name</th>
                    <th className="text-left text-white/70 font-medium py-3">Email</th>
                    <th className="text-left text-white/70 font-medium py-3">Subject</th>
                    <th className="text-left text-white/70 font-medium py-3">Status</th>
                    <th className="text-left text-white/70 font-medium py-3">Created At</th>
                  </tr>
                </thead>
                <tbody>
                  {contacts.map((contact) => (
                    <tr key={contact.id} className="border-b border-white/5">
                      <td className="py-4 text-white">{contact.name}</td>
                      <td className="py-4 text-white/80">{contact.email}</td>
                      <td className="py-4 text-white/80">{contact.subject}</td>
                      <td className="py-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          contact.status === 'new' ? 'bg-blue-500/20 text-blue-400' :
                          contact.status === 'in_progress' ? 'bg-yellow-500/20 text-yellow-400' :
                          contact.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          {contact.status}
                        </span>
                      </td>
                      <td className="py-4 text-white/60">{new Date(contact.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    );
  };

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
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="h-8 w-8 text-purple-400" />
            <h1 className="text-3xl md:text-4xl font-bold text-white">
              Admin Panel
            </h1>
          </div>
          <p className="text-white/70 text-lg">
            Manage users, monitor system performance, and configure settings.
          </p>
        </motion.div>

        {/* Navigation Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="glass-card p-2 mb-8"
        >
          <div className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                    : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                {tab.icon}
                <span>{tab.name}</span>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'users' && renderUsers()}
          {activeTab === 'contacts' && renderContacts()}
          {activeTab === 'system' && renderSystem()}
          {activeTab === 'logs' && renderLogs()}
        </motion.div>
      </div>
    </div>
  )
}

export default AdminPanel

