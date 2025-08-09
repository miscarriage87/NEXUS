# Todo API Backend

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
