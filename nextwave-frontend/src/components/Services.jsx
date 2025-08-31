import React from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Image, 
  Workflow, 
  Brain, 
  Zap, 
  Shield,
  ArrowRight,
  CheckCircle
} from 'lucide-react'
import { Button } from '@/components/ui/button'

const Services = () => {
  const services = [
    {
      icon: <FileText className="h-12 w-12" />,
      title: "Document Processing",
      description: "Advanced PDF editing, conversion between formats (PDF ↔ Word ↔ Visio), and intelligent document analysis.",
      features: [
        "PDF to Word conversion",
        "Visio file editing",
        "Document version control",
        "Batch processing"
      ],
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Image className="h-12 w-12" />,
      title: "AI Image Analysis",
      description: "Powerful computer vision capabilities to analyze, describe, and extract characteristics from images.",
      features: [
        "Automatic image description",
        "Feature extraction",
        "Custom report generation",
        "Batch image processing"
      ],
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: <Workflow className="h-12 w-12" />,
      title: "Workflow Automation",
      description: "Create animated flow simulations and automate complex business processes with visual workflow builder.",
      features: [
        "Visual workflow designer",
        "Animated flow simulation",
        "Process automation",
        "Real-time monitoring"
      ],
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: <Brain className="h-12 w-12" />,
      title: "AI Solutions",
      description: "Intelligent systems for data-driven decisions with machine learning and natural language processing.",
      features: [
        "Smart data analysis",
        "Predictive insights",
        "Natural language processing",
        "Custom AI models"
      ],
      color: "from-orange-500 to-red-500"
    },
    {
      icon: <Zap className="h-12 w-12" />,
      title: "Automation Tools",
      description: "Streamline processes with smart automation, reducing manual work and increasing efficiency.",
      features: [
        "Process automation",
        "Task scheduling",
        "Integration APIs",
        "Custom workflows"
      ],
      color: "from-yellow-500 to-orange-500"
    },
    {
      icon: <Shield className="h-12 w-12" />,
      title: "Enterprise Security",
      description: "Robust infrastructure with enterprise-grade security, compliance, and data protection.",
      features: [
        "End-to-end encryption",
        "Compliance ready",
        "Audit trails",
        "Access controls"
      ],
      color: "from-indigo-500 to-purple-500"
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.1
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

  return (
    <section id="services" className="py-20 relative">
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
            Our Comprehensive{' '}
            <span className="gradient-text-blue">Tech Services</span>
          </h2>
          <p className="text-xl text-white/70 max-w-3xl mx-auto">
            Empower your business with cutting-edge technology solutions designed 
            to streamline operations and drive innovation.
          </p>
        </motion.div>

        {/* Services Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {services.map((service, index) => (
            <motion.div
              key={index}
              variants={itemVariants}
              className="glass-card p-8 glass-card-hover group"
              whileHover={{ scale: 1.02 }}
            >
              {/* Service Icon */}
              <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-r ${service.color} mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <div className="text-white">
                  {service.icon}
                </div>
              </div>

              {/* Service Content */}
              <h3 className="text-2xl font-bold text-white mb-4">
                {service.title}
              </h3>
              
              <p className="text-white/70 mb-6 leading-relaxed">
                {service.description}
              </p>

              {/* Features List */}
              <ul className="space-y-3 mb-8">
                {service.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center text-white/80">
                    <CheckCircle className="h-5 w-5 text-green-400 mr-3 flex-shrink-0" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* Learn More Button */}
              <Button
                variant="ghost"
                className="w-full btn-glass group-hover:bg-white/15 transition-all duration-300"
              >
                Learn More
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </motion.div>
          ))}
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-center mt-16"
        >
          <div className="glass-card p-8 max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-white mb-4">
              Ready to Transform Your Business?
            </h3>
            <p className="text-white/70 mb-8 text-lg">
              Contact us to tailor these solutions to your specific needs and discover 
              how NextWave can accelerate your digital transformation.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg"
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 px-8 py-4 text-lg font-semibold rounded-full"
              >
                Get Started Today
              </Button>
              <Button 
                variant="outline"
                size="lg"
                className="btn-glass px-8 py-4 text-lg font-semibold rounded-full"
              >
                Schedule Consultation
              </Button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default Services

