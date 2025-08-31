import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Menu, 
  X, 
  User, 
  LogOut, 
  Settings, 
  FileText, 
  Image, 
  Workflow,
  Shield,
  Home
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '../contexts/AuthContext'

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)
  const { user, isAuthenticated, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
    setIsProfileOpen(false)
  }

  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Services', path: '/#services', icon: Settings },
    { name: 'About', path: '/#about', icon: User },
    { name: 'Contact', path: '/#contact', icon: FileText }
  ]

  const userNavItems = [
    { name: 'Dashboard', path: '/dashboard', icon: Home },
    { name: 'Documents', path: '/documents', icon: FileText },
    { name: 'Images', path: '/images', icon: Image },
    { name: 'Workflows', path: '/workflows', icon: Workflow }
  ]

  const adminNavItems = [
    { name: 'Admin Panel', path: '/admin', icon: Shield }
  ]

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/'
    }
    return location.pathname.startsWith(path)
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50">
      <nav className="glass-morphism border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center space-x-2"
              >
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">N</span>
                </div>
                <span className="text-white font-bold text-xl">NextWave</span>
              </motion.div>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              {!isAuthenticated ? (
                <>
                  {navItems.map((item) => (
                    <Link
                      key={item.name}
                      to={item.path}
                      className={`text-sm font-medium transition-colors hover:text-blue-400 ${
                        isActive(item.path) ? 'text-blue-400' : 'text-white/80'
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                </>
              ) : (
                <>
                  {userNavItems.map((item) => (
                    <Link
                      key={item.name}
                      to={item.path}
                      className={`flex items-center space-x-1 text-sm font-medium transition-colors hover:text-blue-400 ${
                        isActive(item.path) ? 'text-blue-400' : 'text-white/80'
                      }`}
                    >
                      <item.icon size={16} />
                      <span>{item.name}</span>
                    </Link>
                  ))}
                  {user?.role === 'admin' && adminNavItems.map((item) => (
                    <Link
                      key={item.name}
                      to={item.path}
                      className={`flex items-center space-x-1 text-sm font-medium transition-colors hover:text-blue-400 ${
                        isActive(item.path) ? 'text-blue-400' : 'text-white/80'
                      }`}
                    >
                      <item.icon size={16} />
                      <span>{item.name}</span>
                    </Link>
                  ))}
                </>
              )}
            </div>

            {/* Auth Buttons / User Menu */}
            <div className="hidden md:flex items-center space-x-4">
              {!isAuthenticated ? (
                <>
                  <Link to="/login">
                    <Button variant="ghost" className="text-white hover:bg-white/10">
                      Login
                    </Button>
                  </Link>
                  <Link to="/register">
                    <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                      Get Started
                    </Button>
                  </Link>
                </>
              ) : (
                <div className="relative">
                  <Button
                    variant="ghost"
                    onClick={() => setIsProfileOpen(!isProfileOpen)}
                    className="flex items-center space-x-2 text-white hover:bg-white/10"
                  >
                    <User size={16} />
                    <span>{user?.first_name || user?.username}</span>
                  </Button>

                  <AnimatePresence>
                    {isProfileOpen && (
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="absolute right-0 mt-2 w-48 glass-morphism rounded-lg shadow-lg border border-white/10"
                      >
                        <div className="py-2">
                          <div className="px-4 py-2 border-b border-white/10">
                            <p className="text-sm text-white font-medium">{user?.username}</p>
                            <p className="text-xs text-white/60">{user?.email}</p>
                          </div>
                          <Link
                            to="/dashboard"
                            className="flex items-center space-x-2 px-4 py-2 text-sm text-white/80 hover:bg-white/10 transition-colors"
                            onClick={() => setIsProfileOpen(false)}
                          >
                            <User size={16} />
                            <span>Profile</span>
                          </Link>
                          <button
                            onClick={handleLogout}
                            className="flex items-center space-x-2 w-full px-4 py-2 text-sm text-white/80 hover:bg-white/10 transition-colors"
                          >
                            <LogOut size={16} />
                            <span>Logout</span>
                          </button>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-white hover:bg-white/10"
              >
                {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </Button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden glass-morphism border-t border-white/10"
            >
              <div className="px-4 py-4 space-y-2">
                {!isAuthenticated ? (
                  <>
                    {navItems.map((item) => (
                      <Link
                        key={item.name}
                        to={item.path}
                        className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                          isActive(item.path) 
                            ? 'text-blue-400 bg-white/10' 
                            : 'text-white/80 hover:text-white hover:bg-white/10'
                        }`}
                        onClick={() => setIsMenuOpen(false)}
                      >
                        {item.name}
                      </Link>
                    ))}
                    <div className="pt-4 space-y-2">
                      <Link to="/login" onClick={() => setIsMenuOpen(false)}>
                        <Button variant="ghost" className="w-full text-white hover:bg-white/10">
                          Login
                        </Button>
                      </Link>
                      <Link to="/register" onClick={() => setIsMenuOpen(false)}>
                        <Button className="w-full bg-gradient-to-r from-blue-500 to-purple-600">
                          Get Started
                        </Button>
                      </Link>
                    </div>
                  </>
                ) : (
                  <>
                    {userNavItems.map((item) => (
                      <Link
                        key={item.name}
                        to={item.path}
                        className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium transition-colors ${
                          isActive(item.path) 
                            ? 'text-blue-400 bg-white/10' 
                            : 'text-white/80 hover:text-white hover:bg-white/10'
                        }`}
                        onClick={() => setIsMenuOpen(false)}
                      >
                        <item.icon size={16} />
                        <span>{item.name}</span>
                      </Link>
                    ))}
                    {user?.role === 'admin' && adminNavItems.map((item) => (
                      <Link
                        key={item.name}
                        to={item.path}
                        className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium transition-colors ${
                          isActive(item.path) 
                            ? 'text-blue-400 bg-white/10' 
                            : 'text-white/80 hover:text-white hover:bg-white/10'
                        }`}
                        onClick={() => setIsMenuOpen(false)}
                      >
                        <item.icon size={16} />
                        <span>{item.name}</span>
                      </Link>
                    ))}
                    <div className="pt-4 border-t border-white/10">
                      <div className="px-3 py-2">
                        <p className="text-sm text-white font-medium">{user?.username}</p>
                        <p className="text-xs text-white/60">{user?.email}</p>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="flex items-center space-x-2 w-full px-3 py-2 rounded-md text-base font-medium text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                      >
                        <LogOut size={16} />
                        <span>Logout</span>
                      </button>
                    </div>
                  </>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </header>
  )
}

export default Header

