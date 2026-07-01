# Campster

Collaborative camping/hiking trip planner. Primary feature: shared packing lists and **supply targets** (participants contribute equipment toward a shared quantity goal). Norwegian UI, English code.

## Stack

**Backend**: Flask 3.1 (Python 3.12+), SQLite + Flask-SQLAlchemy, Flask-Migrate/Alembic, Flask-Login (session auth), Werkzeug scrypt, Waitress (prod), `uv` package manager.

**Frontend**: Vue 3 (Composition API, `<script setup>`), Vite, Vue Router, Tailwind CSS 4, Headless UI/Heroicons/Flowbite, ESLint+Prettier, Node 22+.

## Structure

```
backend/
  app.py            # entry point, API routes
  auth.py           # auth decorators
  database.py       # SQLAlchemy models
  settings.py       # user admin, avatars blueprint
  migrations/        # Alembic
client/src/
  views/            # pages (Trip*, Login, SignUp, Settings, ...)
  components/       # TripCard, TripChecklist, ParticipantList, ui/, icons/
  composables/auth.js  # useAuth()
docs/               # readme.md (setup), migrations.md
```

## Models

`User`, `Trip`, `TripParticipant`, `ParticipantItem`, `SupplyTarget`, `TripAttachment` — all in `backend/database.py`.

## Features

- Trip CRUD, participants (join/leave), attachments (files/notes)
- Personal packing lists per participant: name/qty/packed/index, drag-drop order, autofill from previous trips
- Supply targets: grouped items with target qty + progress
- YR.no weather forecast on trip overview
- User admin: signup/login, avatars, admin user management, password change/reset

## Backend auth decorators (`auth.py`)

- `@admin_required`, `@participant_of_trip_required`, `@participant_self_required`, `@item_owner_required`

## Dev commands

```bash
# backend
cd backend && uv run flask run --reload
uv run flask db migrate -m "description" && uv run flask db upgrade

# frontend
cd client && npm install && npm run dev
npm run lint && npm run format

# prod
cd client && npm install && npm run build && cd ../backend && uv run flask run
cd client && npm run docker-build
```

Migration details: `docs/migrations.md`.

## API (`/api`)

- Auth: `POST /login`, `POST /signup`, `POST /logout`, `GET /profile`
- Trips: `GET|POST /trips`, `GET|PUT /trips/<id>`
- Participants: `GET /trip/<id>/participants`, `POST /trips/<id>/join`
- Supply targets: `GET|POST /trip/<id>/supply-targets`, `PUT|DELETE .../<id>`
- Items: `GET /trip/<id>/participant/<pid>/items`, `POST /participant/<pid>/items`, `PUT|DELETE .../items/<id>`, `POST /trip/<id>/participant/<pid>/autofill`, `GET /items`
- Attachments: `GET|POST /trips/<id>/attachments/`, `POST .../upload-file/`, `DELETE .../<id>`
- Settings: `POST /profile/avatar`, `GET /list-avatars`, `POST /settings/user/change-password`, `GET|POST /settings/users`, `DELETE|PUT /settings/users/<id>`, `PUT /settings/users/<id>/password-reset`, `POST /settings/server/update`

## Conventions

- No Vuex/Pinia — component refs + composables only
- Fetch API with JSON payloads, `@/` path alias for `client/src`
- Flask blueprints per feature area

## Claude Code GitHub integration

`.github/workflows/claude.yml` — triggers on `@claude` in issue/PR comments, model `claude-sonnet-4-5-20250929`, max 30 turns.

Repo: github.com/esandoe/campster
