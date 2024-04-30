# Campster

![Nadeshiko eating cup ramen](https://github.com/Lian-D/Lian-d/raw/master/nadeshiko.gif)

## Getting started

This is an agile project which means the project will iterate and evolve along with the users needs. Hence, it has a `backend/` and a `client/`. Anyways, here's how to get the project running locally!

### Prerequisites

- node (currently 22.0.0)
- npm (currently 10.6.0)
- python (currently 3.11.6)

### Running the backend

Navigate to the backend,
create a python venv,
activate the venv,
install dependencies in said venv

```powershell
cd backend &&
python -m venv .campsterenv &&
.campsterenv/Scripts/Activate.ps1 &&
pip install -r requirements.txt
```

If it completes successfully, you can now run the server!

```powershell
flask run --reload
```
