# PublicRepo

A simple, scalable FastAPI backend service for managing **Projects** and their associated **Tasks** with PostgreSQL integration.

---

## Overview

Each Project can have multiple Tasks. The service exposes RESTful APIs to create, read, update, and delete both Projects and Tasks, including an endpoint to retrieve all Tasks for a given Project sorted by priority.

## API Endpoints

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/projects/` | Create a new project |
| `GET` | `/projects/{project_id}` | Retrieve project details |
| `PUT` | `/projects/{project_id}` | Update project details |
| `DELETE` | `/projects/{project_id}` | Delete a project |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/projects/{project_id}/tasks/` | Add a new task to a project |
| `GET` | `/projects/{project_id}/tasks/` | List all tasks for a project |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Data Model

### Project

| Field | Type | Notes |
|-------|------|-------|
| `id` | `int` | Primary key |
| `name` | `str` | Required |
| `description` | `str \| None` | Optional |
| `created_at` | `datetime` | Auto-generated timestamp |

### Task

| Field | Type | Notes |
|-------|------|-------|
| `id` | `int` | Primary key |
| `project_id` | `int` | Foreign key → `project.id` |
| `title` | `str` | Required |
| `priority` | `int` | Higher number = higher priority |
| `completed` | `bool` | Default: `False` |
| `due_date` | `date \| None` | Optional |

## Database

- **PostgreSQL** is used for data persistence.
- Schema includes indexes on `project_id` and `priority`.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- PostgreSQL
- Python 3.10+

## Running the App

```bash
# Install dependencies
pip install fastapi sqlmodel psycopg2-binary uvicorn

# Start the server
uvicorn main:app --reload
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.
