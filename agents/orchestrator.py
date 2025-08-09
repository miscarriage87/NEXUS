
"""
Orchestrator Agent - Koordiniert alle anderen Agents und plant Projekte
"""
import asyncio
import json
import yaml
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = Path(__file__).resolve().parent.parent

from core.base_agent import BaseAgent
from core.messaging import MessageBus, Message, MessageType, TaskRequest, ProjectPlan
from core.ollama_client import ollama_client

class OrchestratorAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("orchestrator", "Project Orchestrator", config)
        self.message_bus = MessageBus()
        self.active_projects = {}
        self.task_queue = asyncio.Queue()
        self.agents = {}
        
    def get_capabilities(self) -> List[str]:
        return [
            "project_planning",
            "task_coordination",
            "agent_management",
            "requirement_analysis",
            "architecture_design"
        ]
    
    async def register_agent(self, agent_id: str, agent):
        """Register an agent with the orchestrator"""
        self.agents[agent_id] = agent
        self.message_bus.register_agent(agent_id, agent)
        self.logger.info(f"Registered agent: {agent_id}")
    
    async def create_project(self, project_request: Dict[str, Any]) -> str:
        """Create a new project and generate tasks"""
        project_id = str(uuid.uuid4())
        
        # Use LLM to analyze requirements and create project plan
        system_prompt = """Du bist ein erfahrener Software-Architekt und Projektmanager. 
        Analysiere die Projektanforderungen und erstelle einen detaillierten Projektplan mit Tasks für Frontend- und Backend-Entwicklung.
        
        Antworte im JSON-Format mit folgender Struktur:
        {
            "project_name": "Name des Projekts",
            "description": "Detaillierte Beschreibung",
            "architecture": {
                "frontend": "Technologie-Stack",
                "backend": "Technologie-Stack",
                "database": "Datenbank-Typ"
            },
            "tasks": [
                {
                    "id": "unique_id",
                    "type": "frontend|backend",
                    "title": "Task Titel",
                    "description": "Detaillierte Beschreibung",
                    "requirements": {},
                    "priority": 1-5,
                    "estimated_hours": 1-8
                }
            ]
        }"""
        
        user_prompt = f"""Erstelle einen Projektplan für folgende Anforderung:
        
        Projekttyp: {project_request.get('type', 'web_application')}
        Beschreibung: {project_request.get('description', 'Keine Beschreibung')}
        Technologien: {project_request.get('technologies', {})}
        Besondere Anforderungen: {project_request.get('requirements', {})}
        
        Erstelle konkrete, umsetzbare Tasks für Frontend- und Backend-Entwicklung."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('orchestrator', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                # Parse LLM response
                plan_text = response.get('response', '{}')
                try:
                    project_plan = json.loads(plan_text)
                except json.JSONDecodeError:
                    # Fallback plan if JSON parsing fails
                    project_plan = self._create_fallback_plan(project_request)
                
                # Store project
                self.active_projects[project_id] = {
                    "id": project_id,
                    "plan": project_plan,
                    "status": "planning",
                    "created_at": datetime.now().isoformat(),
                    "tasks": {}
                }
                
                self.logger.info(f"Created project: {project_id} - {project_plan.get('project_name', 'Unnamed')}")
                return project_id
                
        except Exception as e:
            self.logger.error(f"Error creating project: {str(e)}")
            # Create fallback project
            project_plan = self._create_fallback_plan(project_request)
            self.active_projects[project_id] = {
                "id": project_id,
                "plan": project_plan,
                "status": "planning",
                "created_at": datetime.now().isoformat(),
                "tasks": {}
            }
            return project_id
    
    def _create_fallback_plan(self, project_request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fallback project plan if LLM fails"""
        project_type = project_request.get('type', 'todo_app')
        
        if project_type == 'todo_app':
            return {
                "project_name": "Todo List Application",
                "description": "Simple todo list with CRUD operations",
                "architecture": {
                    "frontend": "React with Tailwind CSS",
                    "backend": "FastAPI with SQLite",
                    "database": "SQLite"
                },
                "tasks": [
                    {
                        "id": "frontend_setup",
                        "type": "frontend",
                        "title": "Setup React Application",
                        "description": "Create React app with Tailwind CSS and basic structure",
                        "requirements": {"framework": "react", "styling": "tailwind"},
                        "priority": 1,
                        "estimated_hours": 2
                    },
                    {
                        "id": "frontend_components",
                        "type": "frontend",
                        "title": "Create Todo Components",
                        "description": "Build TodoList, TodoItem, and AddTodo components",
                        "requirements": {"components": ["TodoList", "TodoItem", "AddTodo"]},
                        "priority": 2,
                        "estimated_hours": 3
                    },
                    {
                        "id": "backend_api",
                        "type": "backend",
                        "title": "Create FastAPI Backend",
                        "description": "Setup FastAPI with CRUD endpoints for todos",
                        "requirements": {"framework": "fastapi", "endpoints": ["GET", "POST", "PUT", "DELETE"]},
                        "priority": 1,
                        "estimated_hours": 3
                    },
                    {
                        "id": "backend_database",
                        "type": "backend",
                        "title": "Setup Database",
                        "description": "Create SQLite database with todo table",
                        "requirements": {"database": "sqlite", "tables": ["todos"]},
                        "priority": 1,
                        "estimated_hours": 1
                    }
                ]
            }
        else:
            return {
                "project_name": "Simple Web Application",
                "description": "Basic web application",
                "architecture": {
                    "frontend": "HTML/CSS/JavaScript",
                    "backend": "Python Flask",
                    "database": "SQLite"
                },
                "tasks": [
                    {
                        "id": "frontend_basic",
                        "type": "frontend",
                        "title": "Create Basic Frontend",
                        "description": "HTML, CSS, and JavaScript files",
                        "requirements": {},
                        "priority": 1,
                        "estimated_hours": 2
                    },
                    {
                        "id": "backend_basic",
                        "type": "backend",
                        "title": "Create Basic Backend",
                        "description": "Flask application with basic routes",
                        "requirements": {},
                        "priority": 1,
                        "estimated_hours": 2
                    }
                ]
            }
    
    async def execute_project(self, project_id: str):
        """Execute a project by distributing tasks to agents"""
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.active_projects[project_id]
        project["status"] = "executing"
        
        self.logger.info(f"Starting execution of project: {project_id}")
        
        # Create output directory
        demo_output = self.config.get('nexus', {}).get('demo_output', str(BASE_DIR / 'demo'))
        output_dir = f"{demo_output}/{project_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Execute tasks
        tasks = project["plan"].get("tasks", [])
        for task in tasks:
            await self._execute_task(project_id, task, output_dir)
        
        project["status"] = "completed"
        self.logger.info(f"Completed project: {project_id}")
    
    async def _execute_task(self, project_id: str, task: Dict[str, Any], output_dir: str):
        """Execute a single task"""
        task_type = task.get("type", "frontend")
        agent_id = "frontend" if task_type == "frontend" else "backend"
        
        if agent_id not in self.agents:
            self.logger.error(f"Agent {agent_id} not available")
            return
        
        self.logger.info(f"Executing task: {task['id']} with agent: {agent_id}")
        
        # Create task message
        task_message = {
            "task_id": task["id"],
            "project_id": project_id,
            "title": task["title"],
            "description": task["description"],
            "requirements": task.get("requirements", {}),
            "output_dir": output_dir,
            "architecture": self.active_projects[project_id]["plan"].get("architecture", {})
        }
        
        # Send task to agent
        agent = self.agents[agent_id]
        result = await agent.process_task(task_message)
        
        # Store task result
        self.active_projects[project_id]["tasks"][task["id"]] = result
        
        self.logger.info(f"Task {task['id']} completed: {result.get('status', 'unknown')}")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process orchestrator-specific tasks"""
        # Check if this is a project creation request
        if "type" in task and task["type"] in ["todo_app", "blog", "web_app"] or "create_project" in str(task):
            try:
                project_id = await self.create_project(task)
                await self.execute_project(project_id)
                return {
                    "status": "completed",
                    "project_id": project_id,
                    "result": "Project created and executed successfully"
                }
            except Exception as e:
                self.logger.error(f"Error in process_task: {str(e)}")
                return {"status": "error", "message": str(e)}
        
        # Handle explicit create_project task type
        task_type = task.get("task_type", task.get("type", "unknown"))
        if task_type == "create_project":
            try:
                project_id = await self.create_project(task)
                await self.execute_project(project_id)
                return {
                    "status": "completed",
                    "project_id": project_id,
                    "result": "Project created and executed successfully"
                }
            except Exception as e:
                self.logger.error(f"Error in process_task: {str(e)}")
                return {"status": "error", "message": str(e)}
        
        return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """Get status of a project"""
        if project_id in self.active_projects:
            return self.active_projects[project_id]
        return {"error": "Project not found"}

async def main():
    """Main function for testing orchestrator"""
    # Load config
    with open(BASE_DIR / 'nexus_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create orchestrator
    orchestrator = OrchestratorAgent(config)
    
    # Import and create other agents
    from frontend import FrontendAgent
    from backend import BackendAgent
    
    frontend_agent = FrontendAgent(config)
    backend_agent = BackendAgent(config)
    
    # Register agents
    await orchestrator.register_agent("frontend", frontend_agent)
    await orchestrator.register_agent("backend", backend_agent)
    
    # Create and execute a demo project
    project_request = {
        "type": "todo_app",
        "description": "Simple todo list application with React frontend and FastAPI backend",
        "technologies": {
            "frontend": "react",
            "backend": "fastapi",
            "database": "sqlite"
        }
    }
    
    result = await orchestrator.process_task({
        "type": "create_project",
        **project_request
    })
    
    print(f"Project execution result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
