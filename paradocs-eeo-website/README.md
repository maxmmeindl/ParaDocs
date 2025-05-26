# ParaDocs EEO Case Management System

## 🎯 Case HS-FEMA-02430-2024 Interactive Website

A comprehensive web application for managing and presenting evidence in the EEOC discrimination case against FEMA, featuring the critical **1,340-day accommodation violation** and **wrongful termination**.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/paradocs-eeo-website.git
cd paradocs-eeo-website

# Install dependencies
npm install

# Start development servers
npm run dev

# Build for production
npm run build

# Deploy to GitHub Pages
npm run deploy
```

## 📊 Key Features

### 1. **Document Management**
- Full-text searchable PDF viewer
- Document categorization and tagging
- Evidence correlation system
- Automated OCR for scanned documents

### 2. **Timeline Visualization**
- Interactive chronological display
- Violation highlighting
- Event correlation with documents
- Response time tracking

### 3. **Damage Calculator**
- Real-time interest calculations
- Category breakdowns
- Legal citation support
- Export to court-ready format

### 4. **Email Indexing**
- Comprehensive email tracking
- Response time analysis
- Thread reconstruction
- Violation pattern detection

### 5. **Legal Research**
- Federal citation database
- Case law integration
- Regulation compliance checker
- Precedent analyzer

## 🏗️ Architecture

```
paradocs-eeo-website/
├── frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/       # Main application pages
│   │   ├── services/    # API and data services
│   │   ├── hooks/       # Custom React hooks
│   │   ├── utils/       # Helper functions
│   │   └── types/       # TypeScript definitions
│   └── public/          # Static assets
│
├── backend/             # Node.js + Express API
│   ├── src/
│   │   ├── routes/     # API endpoints
│   │   ├── models/     # Data models
│   │   ├── services/   # Business logic
│   │   ├── middleware/ # Express middleware
│   │   └── utils/      # Backend utilities
│   └── data/           # Database files
│
├── docs/               # Documentation
│   ├── evidence/       # Categorized evidence
│   ├── timeline/       # Timeline data
│   └── legal/         # Legal research
│
├── data/              # Raw data files
│   ├── emails/        # Email archives
│   ├── documents/     # PDF documents
│   └── roi/          # Report of Investigation
│
└── scripts/          # Utility scripts
    ├── analyze/      # Data analysis
    ├── import/       # Data importers
    └── export/       # Report generators
```

## 💻 Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Chart.js** - Data visualization
- **PDF.js** - PDF rendering
- **React Query** - Data fetching
- **React Router** - Navigation
- **Zustand** - State management

### Backend
- **Node.js** - Runtime
- **Express** - Web framework
- **SQLite** - Database
- **Prisma** - ORM
- **JWT** - Authentication
- **Multer** - File uploads
- **Sharp** - Image processing
- **Tesseract.js** - OCR

### DevOps
- **GitHub Actions** - CI/CD
- **GitHub Pages** - Frontend hosting
- **Docker** - Containerization
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Jest** - Testing

## 📱 Key Pages

### 1. **Dashboard**
- Case overview with key metrics
- $2.27M damage tracker
- Timeline summary
- Recent activity feed

### 2. **Timeline**
- Interactive event display
- Violation highlighting
- Document linking
- Filter by type/date

### 3. **Documents**
- Searchable document library
- Category filtering
- Full-text search
- Evidence tagging

### 4. **Damages**
- Category breakdowns
- Running calculations
- Interest accrual
- Export functionality

### 5. **Emails**
- Thread visualization
- Response tracking
- Pattern analysis
- Violation flagging

### 6. **Legal Research**
- Citation database
- Case law search
- Regulation lookup
- Precedent analysis

### 7. **Reports**
- Generate court filings
- Export evidence packages
- Create presentations
- Settlement calculators

## 🔐 Security Features

- Role-based access control
- Encrypted data storage
- Audit logging
- Session management
- File upload validation
- XSS/CSRF protection

## 📈 Case Statistics

- **Accommodation Delay**: 1,340 days (44.7x legal limit)
- **Total Damages**: $2,272,902.25
- **Violations**: 3 major (ADA, Retaliation, Termination)
- **Evidence Items**: 76+ documents
- **Timeline Events**: 15+ critical dates

## 🚦 Development Workflow

1. **Local Development**
   ```bash
   npm run dev
   ```

2. **Run Tests**
   ```bash
   npm test
   ```

3. **Build Production**
   ```bash
   npm run build
   ```

4. **Deploy to GitHub Pages**
   ```bash
   npm run deploy
   ```

## 📝 Environment Variables

Create `.env` files in both frontend and backend:

### Frontend (.env)
```
VITE_API_URL=http://localhost:3001
VITE_PUBLIC_URL=https://yourusername.github.io/paradocs-eeo-website
```

### Backend (.env)
```
NODE_ENV=development
PORT=3001
DATABASE_URL=file:./data/paradocs.db
JWT_SECRET=your-secret-key
CORS_ORIGIN=http://localhost:5173
```

## 🤝 Contributing

This is a private case management system. Access restricted to authorized personnel only.

## 📄 License

Private and confidential. All rights reserved.

## 🆘 Support

For technical support or questions about the case:
- Email: [your contact]
- Case Number: HS-FEMA-02430-2024

---

**⚖️ Justice Delayed is Justice Denied - 1,340 Days is Inexcusable** 