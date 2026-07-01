# Campster

## Project Description

Campster is a collaborative tool for planning camping and hiking trips, with a primary focus on making packing lists easy to create and share. The key feature is **shared supply targets** where participants can contribute equipment and keep track of what's needed.

**Target Audience**: Small groups planning shared trips
**Language**: Norwegian UI with some English code
**Development Method**: Agile, evolutionary development based on user needs

## Technology Stack

### Backend
- **Framework**: Flask 3.1.1+ (Python 3.12.8+)
- **Database**: SQLite with Flask-SQLAlchemy 3.1.1+
- **Migrations**: Flask-Migrate 4.1.0+ (Alembic)
- **Authentication**: Flask-Login 0.6.3+ (session-based)
- **Password**: Werkzeug scrypt
- **Server**: Waitress 3.0.0+ (production)
- **Package Manager**: `uv` (recommended)

### Frontend
- **Framework**: Vue 3.5.16 (Composition API with `<script setup>`)
- **Build**: Vite 6.3.5
- **Routing**: Vue Router 4.5.1
- **Styling**: Tailwind CSS 4.1.10+
- **UI Components**: Headless UI, Heroicons, Flowbite
- **Linting**: ESLint 9.29.0 + Prettier 3.5.3
- **Node**: 22.0.0+, NPM 10.6.0+

## Project Structure

```
campster/
├── backend/                    # Flask backend
│   ├── app.py                 # Main entry point, Flask app and API routes
│   ├── auth.py                # Authentication and authorization decorators
│   ├── database.py            # SQLAlchemy models
│   ├── settings.py            # Settings blueprint (user admin, avatars)
│   ├── migrations/            # Alembic migrations
│   └── avatars/               # User avatar images
│
├── client/                    # Vue 3 frontend
│   ├── src/
│   │   ├── views/            # Page components (TripHomeView, TripSupplyView, ...)
│   │   ├── components/       # Reusable components (TripCard, TripChecklist, ui/, icons/)
│   │   └── composables/      # Vue composables (useAuth() in auth.js)
│   └── vite.config.js        # Vite config with API proxy
│
└── docs/                     # Documentation
    ├── readme.md            # Setup and getting started
    ├── migrations.md        # Database migration guide
    └── api.md               # Full API route reference
```

## Core Features

### 1. Trip Management
- Create, read, update trips with name, date, location
- Participant management (join/leave trips)
- Trip attachments (file uploads and notes)
- YR.no weather forecast on trip overview

### 2. Packing Lists (Primary Feature)
- Personal checklists per participant
- Items have name, quantity, packed status, and index (for ordering)
- Drag-and-drop reorganization
- Auto-fill from previous trips

### 3. Supply Targets
- Grouped packing items by category/goal
- Target quantity goal with progress indicator
- Shows total item count and progress percentage

### 4. User Administration
- Registration and login
- Avatar selection (20+ predefined)
- Admin users can manage other users
- Password change and reset functionality

## Database Models

```python
User              # Users (authentication, profiles)
Trip              # Trips (camping/hiking trips)
TripParticipant   # Relationship between users and trips
ParticipantItem   # Individual packing items
SupplyTarget      # Shared supply targets
TripAttachment    # Files/notes for trips
```

## Development Workflow

### Backend Setup
```bash
cd backend
uv run                          # Install dependencies
uv run flask run --reload       # Run with hot reload
uv run flask db migrate -m "description"  # Create migration
uv run flask db upgrade         # Run migrations
```
Details: `docs/migrations.md`.

### Frontend Setup
```bash
cd client
npm install
npm run dev                    # Vite dev server (proxies to Flask)
npm run build                  # Production build
npm run lint                   # Lint (also fixes)
npm run format                # Format with Prettier
```

### Full-Stack Production Run
```bash
cd client && npm install && npm run build
cd backend && uv run flask run
```

### Docker
```bash
npm run docker-build          # from client/, runs docker compose up --build
```

## API Overview

Full route reference: `docs/api.md`. All endpoints are under `/api`, defined in `backend/app.py` and `backend/settings.py`.

## Code Conventions and Patterns

### Backend
1. **Authorization Decorators** (defined in `auth.py`):
   - `@admin_required` - Admin only
   - `@participant_of_trip_required` - Must be participant in trip
   - `@participant_self_required` - Must be own participant
   - `@item_owner_required` - Must own the item
   - **Order matters**: `@<blueprint>.route(...)` must be the topmost/outermost decorator, auth decorators below it. If `route()` sits below an auth decorator, Flask registers the undecorated view and auth silently never runs (see PR #54).

2. **Database**: SQLAlchemy with dataclass decorators and type hints
3. **Routing**: Flask blueprints for organized endpoints
4. **Error Handling**: JSON responses with standardized error messages

### Frontend
1. **Vue 3 Composition API** with `<script setup>`
2. **State Management**: Component-level refs and composables (no Vuex/Pinia)
3. **Styling**: Utility-first with Tailwind CSS
4. **API Calls**: Fetch API with JSON payloads
5. **Path Aliases**: `@/` for `src/` directory

### Git
- PRs are squash-merged — branch off `main`, not off another branch that might merge first

## Claude Code Integration

The project has GitHub Actions integration for Claude Code:
- Trigger: `@claude` in issue comments
- Workflow: `.github/workflows/claude.yml`
- Model: claude-sonnet-4-5-20250929
- Max turns: 30

Repository: github.com/esandoe/campster
