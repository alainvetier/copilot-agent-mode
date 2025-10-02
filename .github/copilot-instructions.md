# OctoCAT Supply Chain Management Application

## GitHub Repo Information

This repo is hosted in GitHub:
- owner: alainvetier
- repo: copilot-agent-mode

## Architecture

The complete architecture is described in the [Architecture Document](../docs/architecture.md).

# Build and Run Instructions

Refer to [build instructions](../docs/build.md) for detailed build instructions.

## Backend (API)

The backend is implemented in **Python 3.12+** using **FastAPI** and **Uvicorn**.

To build and run the API:

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

To run the unit tests for the API:

```bash
cd api
pytest
```

## Frontend

The frontend is implemented in **React 18+**, **TypeScript**, and **Vite**.

To build the frontend:

```bash
cd frontend
npm install
npm run build
```

To run the frontend locally:

```bash
cd frontend
npm run dev
```
