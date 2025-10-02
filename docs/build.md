
# Building and Testing the OctoCAT Supply Chain Application

This guide provides instructions for building, running, and testing the OctoCAT Supply Chain Management application, which consists of a Python FastAPI backend (API) and a React Frontend.

## Prerequisites

- Python 3.12 (or later) for the API backend
- Node.js (version 18 or higher) and npm for the React frontend
- Docker/Podman (optional, for containerization)

## Installation

1. Clone the repository
2. Install dependencies for the API backend:
   ```bash
   cd api
   pip install -r requirements.txt
   ```
3. Install dependencies for the frontend:
   ```bash
   cd frontend
   npm install
   ```

## Building the Application

### API Backend (Python FastAPI)

No build step is required for the Python FastAPI backend. Ensure dependencies are installed as above.

### Frontend (React)

You can build the frontend using the following npm command:

```bash
cd frontend
npm run build
```

### Using VS Code Tasks

VS Code tasks have been configured to streamline the build process for the frontend. For the API backend, ensure dependencies are installed.

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette
2. Type `Tasks: Run Task` and select it
3. Choose from the following tasks:
   - `Build Frontend`: Builds the React frontend

Alternatively, you can press `Ctrl+Shift+B` (or `Cmd+Shift+B` on macOS) to run the default build task for the frontend.

## Running the Application

### API Backend (Python FastAPI)

To run the API backend locally:

```bash
cd api
uvicorn app.main:app --reload
```

### Frontend (React)

To run the frontend locally:

```bash
cd frontend
npm run dev
```

### Using VS Code Debugger

You can use the VS Code Debug panel to run the frontend and API backend in development mode. For the API, ensure you use the Python FastAPI configuration.

## Testing the Application

### API Backend (Python FastAPI)

To run API tests:

```bash
cd api
pytest
```

### Frontend (React)

To run frontend tests:

```bash
cd frontend
npm run test
```

### Linting

```bash
# Run linting checks on the Frontend code
cd frontend
npm run lint
```

## Additional Information

### Port Configuration

The API backend (FastAPI) runs on port 8000 by default, and the Frontend runs on port 5137. When running in a Codespace environment, ensure that the API port visibility is set to `public` to avoid CORS errors when the Frontend tries to communicate with the API.

### Docker Deployment

The project includes Dockerfiles for both API (Python FastAPI) and Frontend (React) components and a docker-compose.yml file for easy containerized deployment:

```bash
# Build and start using Docker Compose
docker-compose up --build
```