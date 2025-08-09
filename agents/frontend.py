
"""
Frontend Agent - Erstellt React/HTML/CSS/JavaScript Code und UI/UX Design
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

class FrontendAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("frontend", "Frontend Developer", config)
        self.technologies = config.get('agents', {}).get('frontend', {}).get('technologies', [])
        
    def get_capabilities(self) -> List[str]:
        return [
            "react_development",
            "html_css_javascript",
            "ui_ux_design",
            "responsive_design",
            "component_creation",
            "state_management"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process frontend development tasks"""
        self.status = "working"
        self.logger.info(f"Processing frontend task: {task.get('title', 'Unknown')}")
        
        try:
            task_type = task.get("title", "").lower()
            output_dir = task.get("output_dir", str(BASE_DIR / "demo"))
            architecture = task.get("architecture", {})
            
            if "react" in task_type or architecture.get("frontend", "").lower() == "react":
                result = await self._create_react_app(task, output_dir)
            else:
                result = await self._create_html_app(task, output_dir)
            
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
    
    async def _create_react_app(self, task: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Create React application"""
        frontend_dir = os.path.join(output_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)
        
        # Generate React code using LLM
        system_prompt = """Du bist ein erfahrener React-Entwickler. Erstelle vollständigen, funktionsfähigen React-Code.
        
        Antworte im JSON-Format:
        {
            "files": {
                "filename.ext": "file_content",
                "another_file.ext": "content"
            }
        }
        
        Erstelle immer:
        - package.json mit allen Dependencies
        - src/App.js als Hauptkomponente
        - src/index.js als Entry Point
        - public/index.html
        - src/App.css für Styling
        
        Verwende moderne React mit Hooks und funktionale Komponenten."""
        
        user_prompt = f"""Erstelle eine React-Anwendung für:
        
        Task: {task.get('title', 'React App')}
        Beschreibung: {task.get('description', 'Keine Beschreibung')}
        Anforderungen: {json.dumps(task.get('requirements', {}), indent=2)}
        
        Die App soll vollständig funktionsfähig sein mit allen notwendigen Dateien."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('frontend', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                # Parse LLM response
                code_text = response.get('response', '{}')
                try:
                    code_data = json.loads(code_text)
                    files = code_data.get('files', {})
                except json.JSONDecodeError:
                    # Fallback to default React app
                    files = self._get_default_react_files(task)
                
        except Exception as e:
            self.logger.error(f"LLM error: {str(e)}")
            files = self._get_default_react_files(task)
        
        # Write files
        created_files = []
        for filename, content in files.items():
            file_path = os.path.join(frontend_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(file_path)
        
        return {
            "status": "completed",
            "files_created": created_files,
            "output_directory": frontend_dir,
            "technology": "React"
        }
    
    def _get_default_react_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Get default React application files"""
        app_name = task.get('title', 'Todo App').replace(' ', '')
        
        return {
            "package.json": json.dumps({
                "name": app_name.lower().replace(' ', '-'),
                "version": "0.1.0",
                "private": True,
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "react-scripts": "5.0.1"
                },
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                },
                "eslintConfig": {
                    "extends": ["react-app", "react-app/jest"]
                },
                "browserslist": {
                    "production": [">0.2%", "not dead", "not op_mini all"],
                    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
                }
            }, indent=2),
            
            "public/index.html": """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Todo App created with React" />
    <title>Todo App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>""",
            
            "src/index.js": """import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""",
            
            "src/App.js": """import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const addTodo = () => {
    if (inputValue.trim() !== '') {
      const newTodo = {
        id: Date.now(),
        text: inputValue,
        completed: false
      };
      setTodos([...todos, newTodo]);
      setInputValue('');
    }
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Todo List</h1>
        <div className="todo-input">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Add a new todo..."
            onKeyPress={(e) => e.key === 'Enter' && addTodo()}
          />
          <button onClick={addTodo}>Add</button>
        </div>
        <div className="todo-list">
          {todos.map(todo => (
            <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
              <span onClick={() => toggleTodo(todo.id)}>{todo.text}</span>
              <button onClick={() => deleteTodo(todo.id)}>Delete</button>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;""",
            
            "src/App.css": """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 100vh;
}

.todo-input {
  margin: 20px 0;
}

.todo-input input {
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  margin-right: 10px;
  width: 300px;
}

.todo-input button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #61dafb;
  color: #282c34;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.todo-input button:hover {
  background-color: #21a9c7;
}

.todo-list {
  max-width: 500px;
  margin: 0 auto;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  background-color: #f0f0f0;
  color: #282c34;
  border-radius: 4px;
}

.todo-item.completed span {
  text-decoration: line-through;
  opacity: 0.6;
}

.todo-item span {
  cursor: pointer;
  flex-grow: 1;
  text-align: left;
}

.todo-item button {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.todo-item button:hover {
  background-color: #ff5252;
}"""
        }
    
    async def _create_html_app(self, task: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Create HTML/CSS/JS application"""
        frontend_dir = os.path.join(output_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)
        
        # Create simple HTML app
        files = {
            "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Web App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Simple Web Application</h1>
        <p>This is a basic web application created by the NEXUS Frontend Agent.</p>
        <div id="content">
            <button onclick="addContent()">Click Me!</button>
            <div id="dynamic-content"></div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
            
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #333;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    margin-top: 50px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
}

button {
    background-color: #3498db;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background-color: #2980b9;
}

#dynamic-content {
    margin-top: 20px;
    padding: 10px;
    background-color: #ecf0f1;
    border-radius: 4px;
}""",
            
            "script.js": """let clickCount = 0;

function addContent() {
    clickCount++;
    const contentDiv = document.getElementById('dynamic-content');
    contentDiv.innerHTML = `
        <h3>Dynamic Content</h3>
        <p>Button clicked ${clickCount} times!</p>
        <p>This content was generated dynamically using JavaScript.</p>
    `;
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Simple Web App loaded successfully!');
});"""
        }
        
        # Write files
        created_files = []
        for filename, content in files.items():
            file_path = os.path.join(frontend_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(file_path)
        
        return {
            "status": "completed",
            "files_created": created_files,
            "output_directory": frontend_dir,
            "technology": "HTML/CSS/JS"
        }
