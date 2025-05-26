import { Router } from 'express'
import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const router = Router()
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Get timeline data from the JSON files
const timelineData = JSON.parse(
  readFileSync(join(__dirname, '../../../../comprehensive_timeline_HS-FEMA-02430-2024.json'), 'utf8')
)

// GET /api/timeline - Get all timeline events
router.get('/', (req, res) => {
  const { type, violation, startDate, endDate } = req.query
  
  let events = timelineData.events || []
  
  // Filter by type
  if (type) {
    events = events.filter(event => event.type === type)
  }
  
  // Filter by violation status
  if (violation !== undefined) {
    events = events.filter(event => event.violation === (violation === 'true'))
  }
  
  // Filter by date range
  if (startDate || endDate) {
    events = events.filter(event => {
      const eventDate = new Date(event.date)
      if (startDate && eventDate < new Date(startDate)) return false
      if (endDate && eventDate > new Date(endDate)) return false
      return true
    })
  }
  
  res.json({
    case_number: timelineData.case_number,
    total_events: events.length,
    events,
    key_dates: timelineData.key_dates,
    violations: timelineData.violations
  })
})

// GET /api/timeline/stats - Get timeline statistics
router.get('/stats', (req, res) => {
  const events = timelineData.events || []
  const violations = events.filter(e => e.violation)
  
  // Calculate the 1340-day violation
  const firstAccommodation = events.find(e => e.id === 1)
  const accommodationViolationDays = firstAccommodation?.responseTime || 0
  
  res.json({
    total_events: events.length,
    total_violations: violations.length,
    longest_delay: accommodationViolationDays,
    violation_types: {
      accommodation: events.filter(e => e.type === 'accommodation' && e.violation).length,
      retaliation: events.filter(e => e.type === 'retaliation').length,
      termination: events.filter(e => e.type === 'termination' && e.violation).length,
    },
    case_duration: {
      start_date: events[0]?.date,
      current_date: new Date().toISOString().split('T')[0],
      days: Math.floor((new Date() - new Date(events[0]?.date)) / (1000 * 60 * 60 * 24))
    }
  })
})

// GET /api/timeline/:id - Get specific event
router.get('/:id', (req, res) => {
  const event = timelineData.events.find(e => e.id === parseInt(req.params.id))
  
  if (!event) {
    return res.status(404).json({ error: 'Event not found' })
  }
  
  res.json(event)
})

export default router 