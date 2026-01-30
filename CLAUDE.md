# Campster - Prosjektoversikt for AI-assistenter

Dette dokumentet gir en oversikt over Campster-prosjektet for å hjelpe AI-assistenter med å raskt forstå kodebasen og bidra effektivt.

## Prosjektbeskrivelse

Campster er et samarbeidsverktøy for planlegging av camping- og fjelltursturer, med hovedfokus på å gjøre pakkelister enkle å lage og dele. Nøkkelfunksjonen er **delte forsyningsmål** (supply targets) hvor deltakere kan bidra med utstyr og holde oversikt over hva som trengs.

**Målgruppe**: Smågrupper som planlegger felles turer
**Språk**: Norsk UI med noe engelsk kode
**Utviklingsmetode**: Agil, evolusjonær utvikling basert på brukerbehov

## Teknologistabel

### Backend
- **Framework**: Flask 3.1.1+ (Python 3.12.8+)
- **Database**: SQLite med Flask-SQLAlchemy 3.1.1+
- **Migrasjoner**: Flask-Migrate 4.1.0+ (Alembic)
- **Autentisering**: Flask-Login 0.6.3+ (session-basert)
- **Passord**: Werkzeug scrypt
- **Server**: Waitress 3.0.0+ (produksjon)
- **Pakkebehandler**: `uv` (anbefalt)

### Frontend
- **Framework**: Vue 3.5.16 (Composition API med `<script setup>`)
- **Build**: Vite 6.3.5
- **Routing**: Vue Router 4.5.1
- **Styling**: Tailwind CSS 4.1.10+
- **UI-komponenter**: Headless UI, Heroicons, Flowbite
- **Linting**: ESLint 9.29.0 + Prettier 3.5.3
- **Node**: 22.0.0+, NPM 10.6.0+

### Utviklingsverktøy
- **VSCode anbefalt** med Volar, Tailwind CSS IntelliSense
- **Docker**: docker-compose støtte
- **GitHub Actions**: Claude Code integrasjon (`.github/workflows/claude.yml`)

## Prosjektstruktur

```
campster/
├── backend/                    # Flask backend
│   ├── app.py                 # Hovedinngang, Flask app og API-ruter
│   ├── auth.py                # Autentisering og autorisasjonsdekoratører
│   ├── database.py            # SQLAlchemy-modeller
│   ├── settings.py            # Settings blueprint (brukeradmin, avatarer)
│   ├── pyproject.toml         # Python-avhengigheter
│   ├── setup/                 # Database-initialisering
│   │   ├── initial_setup.py
│   │   └── sample_data.py
│   ├── migrations/            # Alembic-migrasjoner
│   └── avatars/               # Brukeravatarbilder
│
├── client/                    # Vue 3 frontend
│   ├── src/
│   │   ├── main.js           # App entry point
│   │   ├── App.vue           # Root-komponent med navbar
│   │   ├── router/index.js   # Vue Router config
│   │   ├── views/            # Sidekomponenter
│   │   │   ├── HomeView.vue
│   │   │   ├── TripView.vue
│   │   │   ├── TripHomeView.vue
│   │   │   ├── TripSupplyView.vue
│   │   │   ├── TripCheckListView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── SignUpView.vue
│   │   │   ├── SettingsView.vue
│   │   │   └── AboutView.vue
│   │   ├── components/       # Gjenbrukbare komponenter
│   │   │   ├── icons/
│   │   │   ├── ui/
│   │   │   ├── TripCard.vue
│   │   │   ├── TripChecklist.vue
│   │   │   ├── ParticipantList.vue
│   │   │   └── ...
│   │   ├── composables/      # Vue composables
│   │   │   └── auth.js       # useAuth()
│   │   └── assets/
│   ├── vite.config.js        # Vite config med API proxy
│   ├── tailwind.config.js
│   └── package.json
│
└── docs/                     # Dokumentasjon
    ├── readme.md            # Oppsett og kom-i-gang
    └── migrations.md        # Database-migrasjonsguide
```

## Kjernefunksjoner

### 1. Turbehandling (Trip Management)
- Opprett, les, oppdater turer med navn, dato, lokasjon
- Deltakerbehandling (join/leave trips)
- Trip-vedlegg (filopplasting og notater)

### 2. Pakkelister (Primary Feature)
- Personlige sjekklister per deltaker
- Items har navn, antall, packed-status, og index (for rekkefølge)
- Drag-and-drop omorganisering
- Autoutfylling fra tidligere turer

### 3. Forsyningsmål (Supply Targets)
- Grupperte pakkegjenstander etter kategori/mål
- Target quantity goal med fremgangsindikator
- Viser totalt antall items og progressprosent

### 4. Brukeradministrasjon
- Registrering og innlogging
- Avatarvalg (20+ forhåndsdefinerte)
- Admin-brukere kan administrere andre brukere
- Passordbytte og reset-funksjonalitet

## Database-modeller

```python
User              # Brukere (autentisering, profiler)
Trip              # Turer (camping/hiking trips)
TripParticipant   # Forhold mellom brukere og turer
ParticipantItem   # Individuelle pakkegjenstander
SupplyTarget      # Delte forsyningsmål
TripAttachment    # Filer/notater for turer
```

## Utviklingsarbeidsflyt

### Backend-oppsett
```bash
cd backend
uv run                          # Installer avhengigheter
uv run flask run --reload       # Kjør med hot reload
uv run flask db migrate -m "beskrivelse"  # Opprett migrasjon
uv run flask db upgrade         # Kjør migrasjoner
```

### Frontend-oppsett
```bash
cd client
npm install
npm run dev                    # Vite dev server (proxier til Flask)
npm run build                  # Produksjonsbygg
npm run lint --fix            # Rett linting-feil
npm run format                # Formater med Prettier
```

### Full-stack produksjonskjøring
```bash
cd client && npm install && npm run build
cd backend && uv run flask run
```

### Docker
```bash
docker compose up --build
```

## API-oversikt

Alle endepunkter er under `/api`:

### Autentisering
- `POST /api/login` - Logg inn
- `POST /api/signup` - Registrer bruker
- `POST /api/logout` - Logg ut
- `GET /api/profile` - Hent nåværende brukerprofil

### Turer
- `GET /api/trips` - List alle turer
- `POST /api/trips` - Opprett ny tur
- `GET /api/trips/<trip_id>` - Hent turdetaljer
- `PUT /api/trips/<trip_id>` - Oppdater tur

### Deltakere
- `GET /api/trip/<trip_id>/participants` - List deltakere
- `POST /api/trips/<trip_id>/join` - Bli med på tur

### Forsyningsmål (Supply Targets)
- `GET /api/trip/<trip_id>/supply-targets` - List mål
- `POST /api/trip/<trip_id>/supply-targets` - Opprett mål
- `PUT /api/trip/<trip_id>/supply-targets/<id>` - Oppdater mål
- `DELETE /api/trip/<trip_id>/supply-targets/<id>` - Slett mål

### Pakkegjenstander (Participant Items)
- `GET /api/trip/<trip_id>/participant/<participant_id>/items` - Hent items
- `POST /api/participant/<participant_id>/items` - Legg til item
- `PUT /api/participant/<participant_id>/items/<item_id>` - Oppdater item
- `DELETE /api/participant/<participant_id>/items/<item_id>` - Slett item
- `POST /api/trip/<trip_id>/participant/<participant_id>/autofill` - Autoutfyll fra tidligere turer
- `GET /api/items` - Hent alle distinkte item-navn

### Vedlegg
- `GET /api/trips/<trip_id>/attachments/` - List vedlegg
- `POST /api/trips/<trip_id>/attachments/` - Legg til vedlegg (tekst)
- `POST /api/trips/<trip_id>/attachments/upload-file/` - Last opp fil
- `DELETE /api/trips/<trip_id>/attachments/<attachment_id>` - Slett vedlegg

### Innstillinger
- `POST /api/profile/avatar` - Oppdater avatar
- `GET /api/list-avatars` - List tilgjengelige avatarer
- `POST /api/settings/user/change-password` - Bytt passord
- `GET /api/settings/users` - List brukere (admin)
- `POST /api/settings/users` - Opprett bruker (admin)
- `DELETE /api/settings/users/<user_id>` - Slett bruker (admin)
- `PUT /api/settings/users/<user_id>` - Oppdater bruker (admin)
- `PUT /api/settings/users/<user_id>/password-reset` - Reset passord (admin)
- `POST /api/settings/server/update` - Oppdater server (admin)

## Kode-konvensjoner og mønstre

### Backend
1. **Autorisasjonsdekoratører** (definert i `auth.py`):
   - `@admin_required` - Kun admin
   - `@participant_of_trip_required` - Må være deltaker i turen
   - `@participant_self_required` - Må være egen deltaker
   - `@item_owner_required` - Må eie gjenstanden

2. **Database**: SQLAlchemy med dataclass-dekoratører og type hints
3. **Routing**: Flask blueprints for organiserte endepunkter
4. **Feilhåndtering**: JSON-responser med standardiserte feilmeldinger

### Frontend
1. **Vue 3 Composition API** med `<script setup>`
2. **State management**: Component-level refs og composables (ingen Vuex/Pinia)
3. **Styling**: Utility-first med Tailwind CSS
4. **API-kall**: Fetch API med JSON payloads
5. **Path aliases**: `@/` for `src/`-katalogen

## Testing og kvalitet

- **Linting**: `npm run lint` i client-katalogen
- **Formatting**: `npm run format` (Prettier)
- **Type checking**: jsconfig.json for path resolution

## Viktige tekniske beslutninger

1. **SQLite for enkelhet** - Godt for små team-samarbeidsverktøy
2. **Session-basert autentisering** - Via Flask-Login
3. **Ingen dedikert state management** - Composables og komponent-state er tilstrekkelig
4. **Admin-funksjoner innebygd** - Brukerbehandling, server-oppdateringer
5. **Filopplastingsstøtte** - For tur-vedlegg og avatarer

## Vanlige oppgaver

### Legge til ny databasemodell
1. Definer modellen i `backend/database.py`
2. Kjør `uv run flask db migrate -m "beskrivelse"`
3. Gjennomgå migrasjonen i `backend/migrations/versions/`
4. Kjør `uv run flask db upgrade`

### Legge til ny API-endepunkt
1. Legg til rute i `backend/app.py` (eller relevant blueprint)
2. Legg til autorisasjonsdekoratør hvis nødvendig
3. Test med curl eller Postman

### Legge til ny Vue-side
1. Opprett komponent i `client/src/views/`
2. Legg til rute i `client/src/router/index.js`
3. Legg til navigasjonslenke i `Navbar.vue` hvis nødvendig

### Kjøre databasemigrasjoner
Se `docs/migrations.md` for detaljert guide.

## Feilsøking

### Backend starter ikke
- Sjekk at `uv` er installert
- Sjekk at Python 3.12.8+ er installert
- Sjekk at `instance/campster.db` eksisterer (kjør `uv run flask run` første gang)

### Frontend bygger ikke
- Kjør `npm install` i `client/`
- Sjekk Node-versjonen (22.0.0+)
- Sjekk at Tailwind CSS er konfigurert riktig

### API-kall feiler
- Sjekk at backend kjører på riktig port (standard: 5000)
- Sjekk CORS-konfigurasjonen i `backend/app.py`
- Sjekk at Vite proxy er konfigurert riktig i `client/vite.config.js`

## Ytterligere dokumentasjon

- `docs/readme.md` - Detaljert oppsett og kom-i-gang-guide
- `docs/migrations.md` - Database-migrasjonsguide
- GitHub Issues - For pågående utviklingsoppgaver

## Kontakt og bidrag

- **Repository**: github.com/esandoe/campster
- **Issues**: Bruk GitHub Issues for bug-rapporter og feature-forespørsler
- **Pull Requests**: Velkomne! Følg eksisterende kode-stil

## Claude Code-integrasjon

Prosjektet har GitHub Actions-integrasjon for Claude Code:
- Trigger: `@claude` i issue-kommentarer
- Workflow: `.github/workflows/claude.yml`
- Modell: claude-sonnet-4-5-20250929
- Max turns: 30

AI-assistenter kan tagges i issues og PRs for automatisk hjelp med kodingsoppgaver.
