# LearnToLever

A structured programming learning platform built with **Django** + **React** + **PostgreSQL**.

## Quick Start

### 1. Backend (Django)

```bash
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

**Admin Panel:** http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

### 2. Frontend (React + Vite)

```bash
cd frontend
npm run dev
```

**App:** http://localhost:5173/

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/modules/` | List all modules |
| GET | `/api/modules/<slug>/` | Module detail + topics |
| GET | `/api/topics/<slug>/` | Full topic content |
| GET | `/api/topics/<slug>/problems/` | Problems for a topic |
| GET | `/api/modules/<slug>/revision/` | Revision notes |

### PostgreSQL Setup (Optional)

The app runs on SQLite by default. To switch to PostgreSQL:

```bash
export USE_POSTGRES=true
export DB_NAME=learntolever
export DB_USER=your_user
export DB_PASSWORD=your_password
```

### Seed Data

```bash
cd backend
source venv/bin/activate
python manage.py shell < seed/seed_data.py
```

## Architecture

```
learntolever/
├── backend/          # Django + DRF
│   ├── core/         # Models, views, serializers, admin
│   ├── learntolever/ # Settings, URLs
│   └── seed/         # Initial data
└── frontend/         # React + Vite + Tailwind
    └── src/
        ├── api/       # API client
        ├── components/ # Reusable UI components
        └── pages/     # Route pages
```

## Features

- ✅ Module/Topic/Concept/Problem system
- ✅ Django Admin CMS
- ✅ REST API with DRF
- ✅ Dark/Light mode
- ✅ Responsive documentation-style UI
- ✅ Code blocks with copy button
- ✅ Expandable problem solutions
- ✅ Revision notes
- ✅ Ad placeholder components (AdSense ready)
- ✅ SEO-friendly slug-based URLs

## Future Ready

- [ ] User accounts & auth
- [ ] Progress tracking
- [ ] AI-generated quizzes
- [ ] Coding playground
- [ ] Subscriptions
- [ ] Google AdSense integration
