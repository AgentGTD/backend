from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        dbname="agentgtd",
        user="postgres",  # Replace with your username
        password="postgres",  # Replace with your password
        host="localhost",
        port="5432"
    )

# Pydantic model for task input
class Task(BaseModel):
    text: str

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
    cur.execute("INSERT INTO tasks (text) VALUES (%s) RETURNING *", (task.text,))
    new_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_task

# Run with: uvicorn main:app --reload