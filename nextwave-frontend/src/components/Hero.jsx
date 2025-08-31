import React from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowRight, Zap, Shield, Cpu, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'

const Hero = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  }

  const floatingIcons = [
    { Icon: Zap, delay: 0, x: 100, y: 50 },
    { Icon: Shield, delay: 1, x: -80, y: 80 },
    { Icon: Cpu, delay: 2, x: 120, y: -60 },
    { Icon: Sparkles, delay: 0.5, x: -100, y: -40 }
  ]

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Floating Background Icons */}
      {floatingIcons.map(({ Icon, delay, x, y }, index) => (
        <motion.div
          key={index}
          className="absolute text-white/10"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ 
            opacity: 1, 
            scale: 1,
            x: [0, x, 0],
            y: [0, y, 0]
          }}
          transition={{
            duration: 8,
            delay,
            repeat: Infinity,
            repeatType: "reverse",
            ease: "easeInOut"
          }}
          style={{
            left: `${50 + (index - 1.5) * 20}%`,
            top: `${50 + (index % 2 === 0 ? -10 : 10)}%`
          }}
        >
          <Icon size={80} />
        </motion.div>
      ))}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-8"
        >
          {/* Main Heading */}
          <motion.div variants={itemVariants} className="space-y-4">
            <motion.h1 
              className="text-4xl md:text-6xl lg:text-7xl font-bold text-white leading-tight"
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              Embrace the Future with{' '}
              <span className="gradient-text-blue">NextWave</span>
            </motion.h1>
            
            <motion.p 
              className="text-xl md:text-2xl text-white/80 max-w-3xl mx-auto"
              variants={itemVariants}
            >
              Your Partner in Cutting-Edge Tech Solutions
            </motion.p>
          </motion.div>

          {/* Subtitle */}
          <motion.p 
            variants={itemVariants}
            className="text-lg md:text-xl text-white/70 max-w-4xl mx-auto leading-relaxed"
          >
            Advanced document processing, AI-powered image analysis, and automated workflow solutions 
            for Australian businesses ready to innovate.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div 
            variants={itemVariants}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Link to="/register">
              <Button 
                size="lg"
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 group"
              >
                Get Started
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            
            <Link to="#services">
              <Button 
                variant="outline"
                size="lg"
                className="btn-glass px-8 py-4 text-lg font-semibold rounded-full hover:scale-105 transition-all duration-300"
              >
                Explore Services
              </Button>
            </Link>
          </motion.div>

          {/* Feature Cards */}
          <motion.div 
            variants={itemVariants}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 max-w-5xl mx-auto"
          >
            {[
              {
                icon: <Zap className="h-8 w-8 text-blue-400" />,
                title: "Lightning Fast",
                description: "Process documents and images in seconds with our optimized AI algorithms"
              },
              {
                icon: <Shield className="h-8 w-8 text-green-400" />,
                title: "Secure & Private",
                description: "Enterprise-grade security with end-to-end encryption for all your data"
              },
              {
                icon: <Cpu className="h-8 w-8 text-purple-400" />,
                title: "AI-Powered",
                description: "Advanced machine learning models for intelligent document and image analysis"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="glass-card p-6 text-center glass-card-hover"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-white/70">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </motion.div>

          {/* Stats Section */}
          <motion.div 
            variants={itemVariants}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 max-w-4xl mx-auto"
          >
            {[
              { number: "99.9%", label: "Uptime" },
              { number: "10k+", label: "Documents Processed" },
              { number: "5k+", label: "Images Analyzed" },
              { number: "24/7", label: "Support" }
            ].map((stat, index) => (
              <motion.div
                key={index}
                className="text-center"
                whileHover={{ scale: 1.1 }}
              >
                <div className="text-3xl md:text-4xl font-bold gradient-text-blue mb-2">
                  {stat.number}
                </div>
                <div className="text-white/70 text-sm md:text-base">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </motion.div>

          {/* Scroll Indicator */}
          <motion.div
            className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
              <div className="w-1 h-3 bg-white/50 rounded-full mt-2"></div>
            </div>
          </motion.div>
        </motion.div>
      </div>

      {/* Background Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-900/50 pointer-events-none" />
    </section>
  )
}

export default Hero

