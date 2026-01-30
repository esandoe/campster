# Campster - Project Overview for AI Assistants

This document provides an overview of the Campster project to help AI assistants quickly understand the codebase and contribute effectively.

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

### Development Tools
- **VSCode recommended** with Volar, Tailwind CSS IntelliSense
- **Docker**: docker-compose support
- **GitHub Actions**: Claude Code integration (`.github/workflows/claude.yml`)

## Project Structure

```
campster/
├── backend/                    # Flask backend
│   ├── app.py                 # Main entry point, Flask app and API routes
│   ├── auth.py                # Authentication and authorization decorators
│   ├── database.py            # SQLAlchemy models
│   ├── settings.py            # Settings blueprint (user admin, avatars)
│   ├── pyproject.toml         # Python dependencies
│   ├── setup/                 # Database initialization
│   │   ├── initial_setup.py
│   │   └── sample_data.py
│   ├── migrations/            # Alembic migrations
│   └── avatars/               # User avatar images
│
├── client/                    # Vue 3 frontend
│   ├── src/
│   │   ├── main.js           # App entry point
│   │   ├── App.vue           # Root component with navbar
│   │   ├── router/index.js   # Vue Router config
│   │   ├── views/            # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── TripView.vue
│   │   │   ├── TripHomeView.vue
│   │   │   ├── TripSupplyView.vue
│   │   │   ├── TripCheckListView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── SignUpView.vue
│   │   │   ├── SettingsView.vue
│   │   │   └── AboutView.vue
│   │   ├── components/       # Reusable components
│   │   │   ├── icons/
│   │   │   ├── ui/
│   │   │   ├── TripCard.vue
│   │   │   ├── TripChecklist.vue
│   │   │   ├── ParticipantList.vue
│   │   │   └── ...
│   │   ├── composables/      # Vue composables
│   │   │   └── auth.js       # useAuth()
│   │   └── assets/
│   ├── vite.config.js        # Vite config with API proxy
│   ├── tailwind.config.js
│   └── package.json
│
└── docs/                     # Documentation
    ├── readme.md            # Setup and getting started
    └── migrations.md        # Database migration guide
```

## Core Features

### 1. Trip Management
- Create, read, update trips with name, date, location
- Participant management (join/leave trips)
- Trip attachments (file uploads and notes)

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

### Frontend Setup
```bash
cd client
npm install
npm run dev                    # Vite dev server (proxies to Flask)
npm run build                  # Production build
npm run lint --fix            # Fix linting errors
npm run format                # Format with Prettier
```

### Full-Stack Production Run
```bash
cd client && npm install && npm run build
cd backend && uv run flask run
```

### Docker
```bash
docker compose up --build
```

## API Overview

All endpoints are under `/api`:

### Authentication
- `POST /api/login` - Log in
- `POST /api/signup` - Register user
- `POST /api/logout` - Log out
- `GET /api/profile` - Get current user profile

### Trips
- `GET /api/trips` - List all trips
- `POST /api/trips` - Create new trip
- `GET /api/trips/<trip_id>` - Get trip details
- `PUT /api/trips/<trip_id>` - Update trip

### Participants
- `GET /api/trip/<trip_id>/participants` - List participants
- `POST /api/trips/<trip_id>/join` - Join trip

### Supply Targets
- `GET /api/trip/<trip_id>/supply-targets` - List targets
- `POST /api/trip/<trip_id>/supply-targets` - Create target
- `PUT /api/trip/<trip_id>/supply-targets/<id>` - Update target
- `DELETE /api/trip/<trip_id>/supply-targets/<id>` - Delete target

### Participant Items
- `GET /api/trip/<trip_id>/participant/<participant_id>/items` - Get items
- `POST /api/participant/<participant_id>/items` - Add item
- `PUT /api/participant/<participant_id>/items/<item_id>` - Update item
- `DELETE /api/participant/<participant_id>/items/<item_id>` - Delete item
- `POST /api/trip/<trip_id>/participant/<participant_id>/autofill` - Auto-fill from previous trips
- `GET /api/items` - Get all distinct item names

### Attachments
- `GET /api/trips/<trip_id>/attachments/` - List attachments
- `POST /api/trips/<trip_id>/attachments/` - Add attachment (text)
- `POST /api/trips/<trip_id>/attachments/upload-file/` - Upload file
- `DELETE /api/trips/<trip_id>/attachments/<attachment_id>` - Delete attachment

### Settings
- `POST /api/profile/avatar` - Update avatar
- `GET /api/list-avatars` - List available avatars
- `POST /api/settings/user/change-password` - Change password
- `GET /api/settings/users` - List users (admin)
- `POST /api/settings/users` - Create user (admin)
- `DELETE /api/settings/users/<user_id>` - Delete user (admin)
- `PUT /api/settings/users/<user_id>` - Update user (admin)
- `PUT /api/settings/users/<user_id>/password-reset` - Reset password (admin)
- `POST /api/settings/server/update` - Update server (admin)

## Code Conventions and Patterns

### Backend
1. **Authorization Decorators** (defined in `auth.py`):
   - `@admin_required` - Admin only
   - `@participant_of_trip_required` - Must be participant in trip
   - `@participant_self_required` - Must be own participant
   - `@item_owner_required` - Must own the item

2. **Database**: SQLAlchemy with dataclass decorators and type hints
3. **Routing**: Flask blueprints for organized endpoints
4. **Error Handling**: JSON responses with standardized error messages

### Frontend
1. **Vue 3 Composition API** with `<script setup>`
2. **State Management**: Component-level refs and composables (no Vuex/Pinia)
3. **Styling**: Utility-first with Tailwind CSS
4. **API Calls**: Fetch API with JSON payloads
5. **Path Aliases**: `@/` for `src/` directory

## Testing and Quality

- **Linting**: `npm run lint` in client directory
- **Formatting**: `npm run format` (Prettier)
- **Type Checking**: jsconfig.json for path resolution

## Important Technical Decisions

1. **SQLite for simplicity** - Good for small team collaboration tools
2. **Session-based authentication** - Via Flask-Login
3. **No dedicated state management** - Composables and component state are sufficient
4. **Built-in admin functions** - User management, server updates
5. **File upload support** - For trip attachments and avatars

## Common Tasks

### Adding a New Database Model
1. Define the model in `backend/database.py`
2. Run `uv run flask db migrate -m "description"`
3. Review the migration in `backend/migrations/versions/`
4. Run `uv run flask db upgrade`

### Adding a New API Endpoint
1. Add route in `backend/app.py` (or relevant blueprint)
2. Add authorization decorator if necessary
3. Test with curl or Postman

### Adding a New Vue Page
1. Create component in `client/src/views/`
2. Add route in `client/src/router/index.js`
3. Add navigation link in `Navbar.vue` if necessary

### Running Database Migrations
See `docs/migrations.md` for detailed guide.

## Troubleshooting

### Backend Won't Start
- Check that `uv` is installed
- Check that Python 3.12.8+ is installed
- Check that `instance/campster.db` exists (run `uv run flask run` first time)

### Frontend Won't Build
- Run `npm install` in `client/`
- Check Node version (22.0.0+)
- Check that Tailwind CSS is configured correctly

### API Calls Fail
- Check that backend is running on correct port (default: 5000)
- Check CORS configuration in `backend/app.py`
- Check that Vite proxy is configured correctly in `client/vite.config.js`

## Additional Documentation

- `docs/readme.md` - Detailed setup and getting started guide
- `docs/migrations.md` - Database migration guide
- GitHub Issues - For ongoing development tasks

## Contact and Contributions

- **Repository**: github.com/esandoe/campster
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Pull Requests**: Welcome! Follow existing code style

## Claude Code Integration

The project has GitHub Actions integration for Claude Code:
- Trigger: `@claude` in issue comments
- Workflow: `.github/workflows/claude.yml`
- Model: claude-sonnet-4-5-20250929
- Max turns: 30

AI assistants can be tagged in issues and PRs for automatic help with coding tasks.
