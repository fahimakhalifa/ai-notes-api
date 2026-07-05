# AI Notes API – Smart Summaries & Sentiment

![CI](https://github.com/fahimakhalifa/ai-notes-api/actions/workflows/ci.yml/badge.svg)

An authenticated notes API with **text summarization** and **sentiment analysis** powered by Hugging Face, plus **background job processing** for long-running ML. Built with **FastAPI + SQLAlchemy + Pydantic v2 + Postgres**.

<p align="center">
  <img src="docs/screenshot-docs.png" alt="FastAPI Docs" width="650">
</p>

## Features

- **JWT auth** (register/login, `/me`)
- **Notes CRUD** with ownership enforcement
- **Summarization** (`sshleifer/distilbart-cnn-12-6`) – sync & async
- **Sentiment analysis** (`distilbert-base-uncased-finetuned-sst-2-english`) – sync & async
- **Background jobs** with status tracking (`PENDING → RUNNING → SUCCEEDED/FAILED`)
- **Caching**: skip recompute if note unchanged since last analysis
- **Typed schemas** (Pydantic v2), clean separation of models/schemas/utils

## API Endpoints

### Health Check

| Method | Endpoint | Description                    |
| ------ | -------- | ------------------------------ |
| `GET`  | `/`      | Checks that the API is running |

### Authentication

| Method | Endpoint    | Description                                   |
| ------ | ----------- | --------------------------------------------- |
| `POST` | `/register` | Create a new user account                     |
| `POST` | `/login`    | Authenticate user and return JWT access token |
| `GET`  | `/me`       | Return the currently authenticated user       |

### Notes

| Method   | Endpoint       | Description                                |
| -------- | -------------- | ------------------------------------------ |
| `POST`   | `/notes`       | Create a note for the authenticated user   |
| `GET`    | `/notes`       | List notes owned by the authenticated user |
| `GET`    | `/notes/{id}`  | Get a specific note by ID                  |
| `PUT`    | `/notes/{id}`  | Update a note                              |
| `DELETE` | `/delete/{id}` | Delete a note                              |

### AI Features

| Method | Endpoint                      | Description                           |
| ------ | ----------------------------- | ------------------------------------- |
| `POST` | `/notes/{id}/summarize`       | Generate a summary for a note         |
| `POST` | `/notes/{id}/sentiment`       | Analyze note sentiment                |
| `POST` | `/notes/{id}/summarize-async` | Start an async summarization job      |
| `POST` | `/notes/{id}/sentiment-async` | Start an async sentiment analysis job |
| `GET`  | `/jobs/{job_id}`              | Check background job status           |

## Example Workflow

```text
1. Register a user
2. Login and receive a JWT token
3. Create a note
4. Summarize the note
5. Analyze sentiment
6. For long text, start an async job
7. Poll /jobs/{job_id} until the job finishes
```

## Production Notes

* JWT authentication protects user-specific routes.
* Notes are linked to users through ownership checks.
* Summarization and sentiment analysis use Hugging Face transformer models.
* Async endpoints use background jobs for longer-running AI tasks.
* Environment variables are loaded from `.env`.
* Alembic is used for database migrations.
* CI runs syntax checks and lightweight tests on each push and pull request.


## Tech Stack

- FastAPI, SQLAlchemy, Pydantic v2
- PostgreSQL
- Hugging Face `transformers` pipelines
- Uvicorn

## Quickstart (local)

> Prereqs: Python 3.11, Postgres running locally

```bash
git clone <https://github.com/fahimakhalifa/ai-notes-api.git>
cd ai-notes-api
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt

# Copy env and fill with your DB creds
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

# Create database in Postgres matching .env (DATABASE_NAME)
alembic upgrade head
# Then run the server:
uvicorn app.main:app --reload
