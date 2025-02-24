from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Add CORS middleware (already in your code, but ensure it’s there)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:19006"],  # Expo web origin (adjust if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        dbname="agentgtd",
        user="postgres",  # Replace with your username
        password="your_password",  # Replace with your password
        host="localhost",
        port="5432"
    )

# Pydantic model for task input
class Task(BaseModel):
    text: str
    category: str

# Get all tasks
@app.get("/tasks")
async def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks

# Add a new task
@app.post("/tasks")
async def add_task(task: Task):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO tasks (text, category) VALUES (%s, %s) RETURNING *",
        (task.text, task.category)
    )
    new_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_task

# Delete a task by ID
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING *", (task_id,))
    deleted_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# Run with: uvicorn main:app --reload