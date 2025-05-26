import { Router } from 'express'

const router = Router()

router.get('/', (req, res) => {
  res.json({ message: 'Damages API - Coming soon' })
})

export default router 