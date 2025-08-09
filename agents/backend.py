
"""
Backend Agent - Entwickelt APIs, Datenbank-Schemas und Server-Logic
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, List
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = Path(__file__).resolve().parent.parent

from core.base_agent import BaseAgent
from core.ollama_client import ollama_client

class BackendAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("backend", "Backend Developer", config)
        self.technologies = config.get('agents', {}).get('backend', {}).get('technologies', [])
        
    def get_capabilities(self) -> List[str]:
        return [
            "api_development",
            "database_design",
            "server_logic",
            "fastapi_development",
            "flask_development",
            "sqlite_management"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process backend development tasks"""
        self.status = "working"
        self.logger.info(f"Processing backend task: {task.get('title', 'Unknown')}")
        
        try:
            architecture = task.get("architecture", {})
            output_dir = task.get("output_dir", str(BASE_DIR / "demo"))
            
            backend_tech = architecture.get("backend", "fastapi").lower()
            
            if "fastapi" in backend_tech:
                result = await self._create_fastapi_backend(task, output_dir)
            elif "flask" in backend_tech:
                result = await self._create_flask_backend(task, output_dir)
            else:
                result = await self._create_fastapi_backend(task, output_dir)  # Default
            
            self.status = "idle"
            return result
            
        except Exception as e:
            self.status = "error"
            self.logger.error(f"Error processing task: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "files_created": []
            }
    
    async def _create_fastapi_backend(self, task: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Create FastAPI backend"""
        backend_dir = os.path.join(output_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)
        
        # Generate FastAPI code using LLM
        system_prompt = """Du bist ein erfahrener Python-Backend-Entwickler. Erstelle vollständigen, funktionsfähigen FastAPI-Code.
        
        Antworte im JSON-Format:
        {
            "files": {
                "filename.py": "file_content",
                "requirements.txt": "dependencies"
            }
        }
        
        Erstelle immer:
        - main.py als FastAPI Hauptdatei
        - models.py für Datenmodelle
        - database.py für Datenbankverbindung
        - requirements.txt mit Dependencies
        - README.md mit Anweisungen
        
        Verwende SQLite als Datenbank und Pydantic für Modelle."""
        
        user_prompt = f"""Erstelle ein FastAPI-Backend für:
        
        Task: {task.get('title', 'FastAPI Backend')}
        Beschreibung: {task.get('description', 'Keine Beschreibung')}
        Anforderungen: {json.dumps(task.get('requirements', {}), indent=2)}
        
        Das Backend soll vollständige CRUD-Operationen unterstützen."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('backend', {}).get('model', 'codellama:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                # Parse LLM response
                code_text = response.get('response', '{}')
                try:
                    code_data = json.loads(code_text)
                    files = code_data.get('files', {})
                except json.JSONDecodeError:
                    # Fallback to default FastAPI app
                    files = self._get_default_fastapi_files(task)
                
        except Exception as e:
            self.logger.error(f"LLM error: {str(e)}")
            files = self._get_default_fastapi_files(task)
        
        # Write files
        created_files = []
        for filename, content in files.items():
            file_path = os.path.join(backend_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(file_path)
        
        return {
            "status": "completed",
            "files_created": created_files,
            "output_directory": backend_dir,
            "technology": "FastAPI"
        }
    
    def _get_default_fastapi_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Get default FastAPI application files"""
        return {
            "main.py": """from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import database
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TodoCreate(BaseModel):
    text: str
    completed: bool = False

class TodoUpdate(BaseModel):
    text: str = None
    completed: bool = None

class TodoResponse(BaseModel):
    id: int
    text: str
    completed: bool
    
    class Config:
        from_attributes = True

# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(text=todo.text, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.text is not None:
        todo.text = todo_update.text
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)""",
            
            "models.py": """from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    completed = Column(Boolean, default=False)""",
            
            "database.py": """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()""",
            
            "requirements.txt": """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6""",
            
            "README.md": """# Todo API Backend

FastAPI backend for Todo application.

## Installation

```bash
pip install -r requirements.txt
```

## Running the server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- GET `/` - Health check
- GET `/todos` - Get all todos
- POST `/todos` - Create new todo
- GET `/todos/{id}` - Get specific todo
- PUT `/todos/{id}` - Update todo
- DELETE `/todos/{id}` - Delete todo

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.
"""
        }
    
    async def _create_flask_backend(self, task: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Create Flask backend"""
        backend_dir = os.path.join(output_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)
        
        files = {
            "app.py": """from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'todos.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return jsonify({"message": "Todo API is running!"})

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return jsonify([dict(todo) for todo in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    text = data.get('text')
    completed = data.get('completed', False)
    
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO todos (text, completed) VALUES (?, ?)',
        (text, completed)
    )
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"id": todo_id, "text": text, "completed": completed}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    conn.close()
    
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    return jsonify(dict(todo))

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    text = data.get('text')
    completed = data.get('completed')
    
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    
    if todo is None:
        conn.close()
        return jsonify({"error": "Todo not found"}), 404
    
    if text is not None:
        conn.execute('UPDATE todos SET text = ? WHERE id = ?', (text, todo_id))
    if completed is not None:
        conn.execute('UPDATE todos SET completed = ? WHERE id = ?', (completed, todo_id))
    
    conn.commit()
    updated_todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(updated_todo))

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    
    if todo is None:
        conn.close()
        return jsonify({"error": "Todo not found"}), 404
    
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Todo deleted successfully"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)""",
            
            "requirements.txt": """Flask==2.3.3
Flask-CORS==4.0.0""",
            
            "README.md": """# Todo API Backend (Flask)

Flask backend for Todo application.

## Installation

```bash
pip install -r requirements.txt
```

## Running the server

```bash
python app.py
```

## API Endpoints

- GET `/` - Health check
- GET `/todos` - Get all todos
- POST `/todos` - Create new todo
- GET `/todos/{id}` - Get specific todo
- PUT `/todos/{id}` - Update todo
- DELETE `/todos/{id}` - Delete todo
"""
        }
        
        # Write files
        created_files = []
        for filename, content in files.items():
            file_path = os.path.join(backend_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(file_path)
        
        return {
            "status": "completed",
            "files_created": created_files,
            "output_directory": backend_dir,
            "technology": "Flask"
        }
