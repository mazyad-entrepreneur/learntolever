# LearnToLever

A structured programming learning platform built with **Django** + **React** + **PostgreSQL**.

🌐 **Live:** [learntolever.vercel.app](https://learntolever.vercel.app)

## Architecture

```
learntolever/
├── backend/            # Django + DRF (hosted on Render)
│   ├── core/           # Models, views, serializers, admin
│   ├── learntolever/   # Settings, URLs, WSGI
│   └── seed/           # Initial seed data
└── frontend/           # React + Vite + Tailwind (hosted on Vercel)
    └── src/
        ├── api/        # API clients (public + studio)
        ├── components/ # Reusable UI components
        ├── pages/      # Public route pages
        └── studio/     # Creator Studio (admin CMS)
```

## Quick Start (Local Development)

### 1. Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

- **App:** http://localhost:5173/
- **Creator Studio:** http://localhost:5173/studio
- **Django Admin:** http://localhost:8000/admin/

## API Endpoints

### Public (read-only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/series/` | List all published series |
| GET | `/api/series/<slug>/` | Series detail + modules |
| GET | `/api/modules/` | List all published modules |
| GET | `/api/modules/<slug>/` | Module detail + topics |
| GET | `/api/topics/<slug>/` | Full topic content |
| GET | `/api/topics/<slug>/problems/` | Problems for a topic |
| GET | `/api/modules/<slug>/revision/` | Revision notes |

### Auth (JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Obtain JWT token pair |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Current user info |

### Studio (authenticated, staff only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| CRUD | `/api/studio/series/` | Manage series |
| CRUD | `/api/studio/modules/` | Manage modules |
| CRUD | `/api/studio/topics/` | Manage topics |
| CRUD | `/api/studio/blocks/` | Manage content blocks |
| CRUD | `/api/studio/problems/` | Manage problems |

## Deployment

### Backend → Render (Free Tier)

**Environment Variables:**
| Variable | Value |
|----------|-------|
| `DATABASE_URL` | *(auto-set by Render PostgreSQL)* |
| `DJANGO_SECRET_KEY` | *(your secret key)* |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `*` |
| `FRONTEND_URL` | `https://learntolever.vercel.app` |

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn learntolever.wsgi:application
```

### Frontend → Vercel

**Environment Variables:**
| Variable | Value |
|----------|-------|
| `VITE_API_BASE` | `https://learntolever-api.onrender.com/api` |

**Build Command:** `npm run build`
**Output Directory:** `dist`
**Root Directory:** `frontend`

## Features

- ✅ Series → Module → Topic → ContentBlock hierarchy
- ✅ Creator Studio (admin CMS with live preview)
- ✅ Block-based content editor (heading, code, callout, etc.)
- ✅ JWT authentication for staff users
- ✅ REST API with DRF
- ✅ Dark/Light mode with persistence
- ✅ Responsive documentation-style UI
- ✅ Code blocks with copy button
- ✅ Expandable problem solutions
- ✅ Revision notes
- ✅ Ad placeholder components (AdSense ready)
- ✅ SEO-friendly slug-based URLs
- ✅ 404 catch-all page

## Future Roadmap

- [ ] User accounts & progress tracking
- [ ] AI-generated quizzes
- [ ] Coding playground (embedded editor)
- [ ] Subscriptions & payments
- [ ] Google AdSense integration
- [ ] Search functionality
