# PDRL

A Python project using LangChain and LangGraph with Ollama for AI-powered recipe generation.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Ensure Ollama is running locally:
   ```bash
   ollama serve
   ```
   Pull a model if needed: `ollama pull llama3.2`

## Run Locally

Run the main application:
```bash
python src/main.py
```

Override configs via CLI:
```bash
python src/main.py app.debug=false models.temperature=0.5
```

## Development with Docker Compose

Build and run in development mode:
```bash
cd deployment
docker compose up --build
```

## Production Deployment with Dokploy

1. Build the Docker image using the `deployment/Dockerfile`.
2. Deploy to Dokploy, ensuring Ollama is accessible (run separately or integrate as multi-container).

## Future Migration to Django

To migrate to Django:
- Install Django: `uv add django`
- Create Django project: `django-admin startproject pdrl_django .`
- Move LangChain/LangGraph logic into Django views or management commands.
- Use Django's settings for configs instead of Hydra.