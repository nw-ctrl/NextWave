import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Components
import Header from './components/Header'
import Hero from './components/Hero'
import Services from './components/Services'
import About from './components/About'
import Contact from './components/Contact'
import Dashboard from './components/Dashboard'
import Login from './components/Login'
import Register from './components/Register'
import DocumentProcessor from './components/DocumentProcessor'
import ImageAnalyzer from './components/ImageAnalyzer'
import WorkflowBuilder from './components/WorkflowBuilder'
import AdminPanel from './components/AdminPanel'

// Context
import { AuthProvider, useAuth } from './contexts/AuthContext'

// Particles background component
const ParticlesBackground = () => {
  const [particles, setParticles] = useState([])

  useEffect(() => {
    const generateParticles = () => {
      const newParticles = []
      for (let i = 0; i < 50; i++) {
        newParticles.push({
          id: i,
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          size: Math.random() * 3 + 1,
          speedX: (Math.random() - 0.5) * 0.5,
          speedY: (Math.random() - 0.5) * 0.5,
          opacity: Math.random() * 0.5 + 0.2
        })
      }
      setParticles(newParticles)
    }

    generateParticles()

    const animateParticles = () => {
      setParticles(prev => prev.map(particle => ({
        ...particle,
        x: (particle.x + particle.speedX + window.innerWidth) % window.innerWidth,
        y: (particle.y + particle.speedY + window.innerHeight) % window.innerHeight
      })))
    }

    const interval = setInterval(animateParticles, 50)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="fixed inset-0 pointer-events-none z-0">
      {particles.map(particle => (
        <div
          key={particle.id}
          className="absolute rounded-full bg-blue-400"
          style={{
            left: particle.x,
            top: particle.y,
            width: particle.size,
            height: particle.size,
            opacity: particle.opacity
          }}
        />
      ))}
    </div>
  )
}

// Protected Route component
const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (adminOnly && user?.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  return children
}

// Main App Layout
const AppLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      <ParticlesBackground />
      <div className="relative z-10">
        <Header />
        <main className="pt-16">
          {children}
        </main>
      </div>
    </div>
  )
}

// Home Page Component
const HomePage = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Hero />
      <Services />
      <About />
      <Contact />
    </motion.div>
  )
}

// Main App Component
function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={
              <AppLayout>
                <HomePage />
              </AppLayout>
            } />
            
            <Route path="/login" element={
              <AppLayout>
                <Login />
              </AppLayout>
            } />
            
            <Route path="/register" element={
              <AppLayout>
                <Register />
              </AppLayout>
            } />

            {/* Protected Routes */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <AppLayout>
                  <Dashboard />
                </AppLayout>
              </ProtectedRoute>
            } />

            <Route path="/documents" element={
              <ProtectedRoute>
                <AppLayout>
                  <DocumentProcessor />
                </AppLayout>
              </ProtectedRoute>
            } />

            <Route path="/images" element={
              <ProtectedRoute>
                <AppLayout>
                  <ImageAnalyzer />
                </AppLayout>
              </ProtectedRoute>
            } />

            <Route path="/workflows" element={
              <ProtectedRoute>
                <AppLayout>
                  <WorkflowBuilder />
                </AppLayout>
              </ProtectedRoute>
            } />

            {/* Admin Routes */}
            <Route path="/admin" element={
              <ProtectedRoute adminOnly={true}>
                <AppLayout>
                  <AdminPanel />
                </AppLayout>
              </ProtectedRoute>
            } />

            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App

