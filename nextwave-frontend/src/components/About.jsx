import React from 'react'
import { motion } from 'framer-motion'
import { 
  MapPin, 
  Users, 
  Award, 
  Target,
  Heart,
  Lightbulb,
  Shield,
  Zap
} from 'lucide-react'

const About = () => {
  const values = [
    {
      icon: <Lightbulb className="h-8 w-8" />,
      title: "Innovation",
      description: "Constantly pushing boundaries with cutting-edge technology solutions"
    },
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Reliability",
      description: "Dependable services with 99.9% uptime and enterprise-grade security"
    },
    {
      icon: <Heart className="h-8 w-8" />,
      title: "Client-Focused",
      description: "Your success is our priority, with personalized support and solutions"
    },
    {
      icon: <Zap className="h-8 w-8" />,
      title: "Efficiency",
      description: "Streamlined processes that save time and maximize productivity"
    }
  ]

  const stats = [
    {
      icon: <Users className="h-8 w-8 text-blue-400" />,
      number: "500+",
      label: "Happy Clients",
      description: "Businesses transformed"
    },
    {
      icon: <Award className="h-8 w-8 text-green-400" />,
      number: "5+",
      label: "Years Experience",
      description: "In tech innovation"
    },
    {
      icon: <Target className="h-8 w-8 text-purple-400" />,
      number: "99.9%",
      label: "Success Rate",
      description: "Project completion"
    },
    {
      icon: <MapPin className="h-8 w-8 text-orange-400" />,
      number: "100%",
      label: "Australian",
      description: "Owned & operated"
    }
  ]

  return (
    <section id="about" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            About{' '}
            <span className="gradient-text-blue">NextWave</span>
          </h2>
          <p className="text-xl text-white/70 max-w-3xl mx-auto">
            An Australian-based high-tech company dedicated to helping clients 
            embrace technology and find efficient solutions.
          </p>
        </motion.div>

        {/* Company Story */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="glass-card p-8 md:p-12 mb-16"
        >
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-3xl font-bold text-white mb-6">
                Our Story
              </h3>
              <p className="text-white/80 text-lg leading-relaxed mb-6">
                NextWave was founded with a vision to bridge the gap between traditional 
                business processes and modern technology. We believe that every organization, 
                regardless of size, should have access to powerful AI-driven tools and 
                automation solutions.
              </p>
              <p className="text-white/80 text-lg leading-relaxed mb-6">
                Based in Australia, we understand the unique challenges faced by local 
                businesses and provide tailored solutions that drive real results. Our 
                team of experts combines deep technical knowledge with practical business 
                experience to deliver solutions that work.
              </p>
              <p className="text-white/80 text-lg leading-relaxed">
                From document processing to AI-powered image analysis, we're committed 
                to helping you embrace the future of technology while maintaining the 
                reliability and security your business demands.
              </p>
            </div>
            
            <div className="relative">
              <motion.div
                className="glass-card p-8 text-center"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3 }}
              >
                <MapPin className="h-16 w-16 text-blue-400 mx-auto mb-4" />
                <h4 className="text-2xl font-bold text-white mb-2">
                  Proudly Australian
                </h4>
                <p className="text-white/70 mb-4">
                  Based in Sydney, NSW
                </p>
                <p className="text-white/60 text-sm">
                  Supporting local businesses with world-class technology solutions
                </p>
              </motion.div>
            </div>
          </div>
        </motion.div>

        {/* Values Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-16"
        >
          <h3 className="text-3xl font-bold text-white text-center mb-12">
            Our Core Values
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map((value, index) => (
              <motion.div
                key={index}
                className="glass-card p-6 text-center glass-card-hover"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3 }}
              >
                <div className="inline-flex p-3 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 mb-4">
                  <div className="text-white">
                    {value.icon}
                  </div>
                </div>
                <h4 className="text-xl font-bold text-white mb-3">
                  {value.title}
                </h4>
                <p className="text-white/70 text-sm">
                  {value.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="glass-card p-8 md:p-12"
        >
          <h3 className="text-3xl font-bold text-white text-center mb-12">
            Our Impact
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                className="text-center"
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex justify-center mb-4">
                  {stat.icon}
                </div>
                <div className="text-4xl font-bold gradient-text-blue mb-2">
                  {stat.number}
                </div>
                <div className="text-white font-semibold mb-1">
                  {stat.label}
                </div>
                <div className="text-white/60 text-sm">
                  {stat.description}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Mission Statement */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="text-center mt-16"
        >
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-white mb-6">
              Our Mission
            </h3>
            <p className="text-xl text-white/80 leading-relaxed">
              "To empower businesses with innovative technology solutions that simplify 
              complex processes, enhance productivity, and drive sustainable growth in 
              the digital age."
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default About

