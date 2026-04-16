from datetime import date, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ---------------------------------------------------------------------------
# Database engine
# ---------------------------------------------------------------------------
engine = create_engine(
    "postgresql://test:test@localhost/publicrepo",
    isolation_level="REPEATABLE READ",
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    title: str = Field(index=True)
    completed: bool = Field(default=False)
    priority: int = Field(default=0)
    due_date: date | None = Field(default=None)


# ---------------------------------------------------------------------------
# Dependency injection
# ---------------------------------------------------------------------------
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
app = FastAPI(title="PublicRepo", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)


@app.get("/")
def get_root() -> dict[str, str]:
    return {"message": "Hello, PublicRepo!"}


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
@app.post("/projects/", response_model=Project)
def create_project(project: Project, session: SessionDep) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, project: Project, session: SessionDep) -> Project:
    project_db = session.get(Project, project_id)
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.model_dump(exclude_unset=True)
    project_db.sqlmodel_update(project_data)
    session.add(project_db)
    session.commit()
    session.refresh(project_db)
    return project_db


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, session: SessionDep) -> dict[str, object]:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"project_id": project_id, "status": "deleted"}


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
@app.post("/projects/{project_id}/tasks/", response_model=Task)
def create_task(project_id: int, task: Task, session: SessionDep) -> Task:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task.project_id = project_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/projects/{project_id}/tasks/")
def read_tasks(project_id: int, session: SessionDep) -> list[Task]:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    return tasks


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, session: SessionDep) -> Task:
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep) -> dict[str, object]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"task_id": task_id, "status": "deleted"}
