# Campster

Collaborative camping/hiking trip planner. Primary feature: shared packing lists and **supply targets** (participants contribute equipment toward a shared quantity goal).

## Real-world context

- **Users**: small groups of friends/family planning a shared trip together — not a scaled multi-tenant product. Favor simple, direct solutions over configurability or scale.
- **Users are Norwegian** — UI text and copy is Norwegian; code, comments, commits stay English.
- **Built evolutionarily**: features get added as real trips surface a need (e.g. the weather forecast), not designed upfront. Don't over-build for hypothetical future requirements.

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
docs/               # readme.md (setup), migrations.md, api.md
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

## API

Full route reference: `docs/api.md`. All endpoints under `/api`, defined in `backend/app.py` and `backend/settings.py`.

## Conventions

- No Vuex/Pinia — component refs + composables only
- Fetch API with JSON payloads, `@/` path alias for `client/src`
- Flask blueprints per feature area
- PRs are squash-merged — never branch off a branch that might merge before it; branch from `main`

## Claude Code GitHub integration

`.github/workflows/claude.yml` — triggers on `@claude` in issue/PR comments, model `claude-sonnet-4-5-20250929`, max 30 turns.

Repo: github.com/esandoe/campster
