# ParaDocs EEO Website Setup Guide

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/paradocs-eeo-website.git
cd paradocs-eeo-website
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration

#### Frontend (.env in frontend/)
```env
VITE_API_URL=http://localhost:3001
VITE_PUBLIC_URL=http://localhost:5173
```

#### Backend (.env in backend/)
```env
NODE_ENV=development
PORT=3001
DATABASE_URL=file:./data/paradocs.db
JWT_SECRET=your-secret-key-here
CORS_ORIGIN=http://localhost:5173
```

### 4. Run the Application
```bash
# Development mode (runs both frontend and backend)
npm run dev

# Frontend only
npm run dev:frontend

# Backend only
npm run dev:backend
```

### 5. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:3001
- API Health Check: http://localhost:3001/api/health

## 📁 File Structure

```
paradocs-eeo-website/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom hooks
│   │   ├── utils/        # Utilities
│   │   └── types/        # TypeScript types
│   └── public/           # Static assets
├── backend/              # Express API
│   ├── src/
│   │   ├── routes/      # API endpoints
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   └── middleware/  # Express middleware
│   └── data/            # SQLite database
├── data/                # Case data files
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

## 🔧 Configuration

### GitHub Pages Deployment

1. Update `frontend/vite.config.ts`:
```typescript
base: process.env.NODE_ENV === 'production' ? '/paradocs-eeo-website/' : '/',
```

2. Update repository settings:
   - Go to Settings > Pages
   - Set source to "GitHub Actions"

3. Push to main branch to trigger deployment

### Custom Domain (Optional)

1. Add CNAME file to `frontend/public/`:
```
your-domain.com
```

2. Configure DNS settings with your provider

## 📊 Data Management

### Index All Documents
```bash
cd scripts
node index-all-documents.js
```

This will:
- Scan all case files
- Extract timeline events
- Calculate damages
- Create searchable indexes

### Update Timeline
Edit `data/complete_timeline.json` with new events

### Add Documents
Place new documents in appropriate folders:
- PDFs: `data/documents/`
- Emails: `data/emails/`
- ROI: `data/roi/`

## 🔍 Key Features

### Dashboard
- Real-time damage counter
- Timeline overview
- Key metrics display
- Quick action buttons

### Timeline
- Complete event history
- Violation highlighting
- Document linking
- Filter by type/date

### Documents
- Full-text search
- Category filtering
- PDF viewer
- Metadata display

### Damages
- Category breakdown
- Interest calculations
- Export functionality
- Legal citations

### Email Index
- Thread tracking
- Response times
- Pattern analysis
- Violation detection

## 🛠️ Development

### Add a New Page

1. Create component in `frontend/src/pages/`:
```typescript
export default function NewPage() {
  return <div>New Page Content</div>
}
```

2. Add route in `frontend/src/App.tsx`:
```typescript
<Route path="/new-page" element={<NewPage />} />
```

3. Add navigation in `frontend/src/components/Layout.tsx`

### Add API Endpoint

1. Create route in `backend/src/routes/`:
```javascript
import { Router } from 'express'
const router = Router()

router.get('/', (req, res) => {
  res.json({ data: 'response' })
})

export default router
```

2. Import in `backend/src/server.js`

### Database Schema

SQLite tables:
- documents
- timeline_events
- emails
- damages
- violations
- users (future)

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3001
npx kill-port 3001

# Kill process on port 5173
npx kill-port 5173
```

### Build Errors
```bash
# Clear cache and rebuild
rm -rf node_modules frontend/node_modules backend/node_modules
npm install
npm run build
```

### Database Issues
```bash
# Reset database
rm backend/data/paradocs.db
npm run db:init
```

## 📝 Important Case Data

- **Case Number**: HS-FEMA-02430-2024
- **1,340-Day Violation**: September 15, 2020 - May 2024
- **Termination Date**: January 6, 2025
- **Total Damages**: $2,272,902.25

## 🔒 Security Notes

- Never commit `.env` files
- Keep JWT_SECRET secure
- Use HTTPS in production
- Sanitize all user inputs
- Regular security updates

## 📞 Support

For case-specific questions or technical support:
- Create an issue on GitHub
- Email: [your contact]

---

**Remember**: This system contains sensitive legal information. Handle with appropriate security measures. 