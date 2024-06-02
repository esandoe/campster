# Campster

Campster is a camping/hike planning tool, currently focused on making packing lists easy, including shared supply targets!

![Nadeshiko eating cup ramen](https://github.com/Lian-D/Lian-d/raw/master/nadeshiko.gif)

## Getting started

This is an agile project which means the project will iterate and evolve along with the users needs. Hence, it has a `backend/` and a `client/`. Anyways, here's how to get the project running locally!

### Prerequisites

Required:

- node (currently 22.0.0)
- npm (currently 10.6.0)
- python (currently 3.11.6)

Recommended:

- [VSCode](https://code.visualstudio.com/)
  - [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (disable Vetur)
  - [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
  - [SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)

### Running the backend 🐍🖥

Navigate to the backend,
create a python venv,
activate the venv,
install dependencies in said venv

Windows
```powershell
cd backend &&
python -m venv .campsterenv &&
.campsterenv/Scripts/Activate.ps1 &&
pip install -r requirements.txt
```

Mac/Linux
```bash
cd backend &&
python3.12 -m venv .campsterenv &&
source .campsterenv/bin/activate &&
pip install -r requirements.txt
```

If it completes successfully, you can now run the server!

```powershell
flask run --reload
```

See also [Migrations](./migrations.md) for how to perform database migrations.

### Running the client 🌐📱

You might want to open a new terminal for this? idk.

Anyway, assuming you're at the project root again,
navigate to the frontend
and install the project dependencies

```sh
npm install
```

If it completes successfully, you can now run the client!

```sh
npm run dev
```
