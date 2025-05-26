import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import compression from 'compression'
import dotenv from 'dotenv'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

// Import routes
import timelineRoutes from './routes/timeline.js'
import documentsRoutes from './routes/documents.js'
import damagesRoutes from './routes/damages.js'
import emailsRoutes from './routes/emails.js'
import legalRoutes from './routes/legal.js'

// Load environment variables
dotenv.config()

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const app = express()
const PORT = process.env.PORT || 3001

// Middleware
app.use(helmet())
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true
}))
app.use(compression())
app.use(morgan('dev'))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Static files
app.use('/uploads', express.static(join(__dirname, '../uploads')))

// API Routes
app.use('/api/timeline', timelineRoutes)
app.use('/api/documents', documentsRoutes)
app.use('/api/damages', damagesRoutes)
app.use('/api/emails', emailsRoutes)
app.use('/api/legal', legalRoutes)

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    case: 'HS-FEMA-02430-2024'
  })
})

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  })
})

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' })
})

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`)
  console.log(`📁 Case: HS-FEMA-02430-2024`)
  console.log(`💰 Total Damages: $2,272,902.25`)
}) 