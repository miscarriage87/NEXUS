
"""
Test cases for NEXUS Agent System
"""
import pytest
import asyncio
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import OrchestratorAgent
from agents.frontend import FrontendAgent
from agents.backend import BackendAgent
from core.messaging import MessageBus, Message, MessageType
import yaml

@pytest.fixture
def config():
    """Test configuration"""
    return {
        'nexus': {
            'version': '1.0.0',
            'project_root': '/tmp/nexus_test'
        },
        'ollama': {
            'base_url': 'http://localhost:11434',
            'timeout': 30
        },
        'agents': {
            'orchestrator': {
                'id': 'orchestrator',
                'model': 'qwen2.5-coder:7b'
            },
            'frontend': {
                'id': 'frontend',
                'model': 'qwen2.5-coder:7b',
                'technologies': ['react', 'html', 'css', 'javascript']
            },
            'backend': {
                'id': 'backend',
                'model': 'codellama:7b',
                'technologies': ['python', 'fastapi', 'flask']
            }
        }
    }

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

class TestMessageBus:
    """Test message bus functionality"""
    
    def test_message_bus_creation(self):
        bus = MessageBus()
        assert bus.agents == {}
        assert bus.message_history == []
    
    def test_agent_registration(self):
        bus = MessageBus()
        mock_agent = Mock()
        bus.register_agent("test_agent", mock_agent)
        assert "test_agent" in bus.agents
        assert bus.agents["test_agent"] == mock_agent

class TestOrchestratorAgent:
    """Test orchestrator agent functionality"""
    
    def test_orchestrator_creation(self, config):
        orchestrator = OrchestratorAgent(config)
        assert orchestrator.agent_id == "orchestrator"
        assert orchestrator.name == "Project Orchestrator"
        assert "project_planning" in orchestrator.get_capabilities()
    
    @pytest.mark.asyncio
    async def test_agent_registration(self, config):
        orchestrator = OrchestratorAgent(config)
        mock_agent = Mock()
        await orchestrator.register_agent("test_agent", mock_agent)
        assert "test_agent" in orchestrator.agents
    
    def test_fallback_plan_creation(self, config):
        orchestrator = OrchestratorAgent(config)
        project_request = {"type": "todo_app"}
        plan = orchestrator._create_fallback_plan(project_request)
        
        assert "project_name" in plan
        assert "tasks" in plan
        assert len(plan["tasks"]) > 0
        assert plan["architecture"]["frontend"] == "React with Tailwind CSS"

class TestFrontendAgent:
    """Test frontend agent functionality"""
    
    def test_frontend_creation(self, config):
        frontend = FrontendAgent(config)
        assert frontend.agent_id == "frontend"
        assert frontend.name == "Frontend Developer"
        assert "react_development" in frontend.get_capabilities()
    
    def test_default_react_files(self, config):
        frontend = FrontendAgent(config)
        task = {"title": "Test React App"}
        files = frontend._get_default_react_files(task)
        
        assert "package.json" in files
        assert "src/App.js" in files
        assert "src/index.js" in files
        assert "public/index.html" in files
        
        # Check if package.json is valid JSON
        import json
        package_data = json.loads(files["package.json"])
        assert "react" in package_data["dependencies"]
    
    @pytest.mark.asyncio
    async def test_process_task(self, config, temp_dir):
        frontend = FrontendAgent(config)
        task = {
            "title": "Create React App",
            "description": "Test React application",
            "output_dir": temp_dir,
            "architecture": {"frontend": "react"}
        }
        
        result = await frontend.process_task(task)
        assert result["status"] == "completed"
        assert "files_created" in result
        assert len(result["files_created"]) > 0

class TestBackendAgent:
    """Test backend agent functionality"""
    
    def test_backend_creation(self, config):
        backend = BackendAgent(config)
        assert backend.agent_id == "backend"
        assert backend.name == "Backend Developer"
        assert "api_development" in backend.get_capabilities()
    
    def test_default_fastapi_files(self, config):
        backend = BackendAgent(config)
        task = {"title": "Test FastAPI Backend"}
        files = backend._get_default_fastapi_files(task)
        
        assert "main.py" in files
        assert "models.py" in files
        assert "database.py" in files
        assert "requirements.txt" in files
        
        # Check if main.py contains FastAPI imports
        assert "from fastapi import FastAPI" in files["main.py"]
    
    @pytest.mark.asyncio
    async def test_process_task(self, config, temp_dir):
        backend = BackendAgent(config)
        task = {
            "title": "Create FastAPI Backend",
            "description": "Test FastAPI application",
            "output_dir": temp_dir,
            "architecture": {"backend": "fastapi"}
        }
        
        result = await backend.process_task(task)
        assert result["status"] == "completed"
        assert "files_created" in result
        assert len(result["files_created"]) > 0

class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.mark.asyncio
    async def test_full_project_creation(self, config, temp_dir):
        """Test complete project creation workflow"""
        # Override demo output directory
        config['nexus']['demo_output'] = temp_dir
        
        # Create agents
        orchestrator = OrchestratorAgent(config)
        frontend = FrontendAgent(config)
        backend = BackendAgent(config)
        
        # Register agents
        await orchestrator.register_agent("frontend", frontend)
        await orchestrator.register_agent("backend", backend)
        
        # Create project
        project_request = {
            "type": "todo_app",
            "description": "Test todo application",
            "technologies": {
                "frontend": "react",
                "backend": "fastapi"
            }
        }
        
        result = await orchestrator.process_task(project_request)
        
        # Verify result
        assert result["status"] == "completed"
        assert "project_id" in result
        
        # Check if files were created
        project_id = result["project_id"]
        project_dir = os.path.join(temp_dir, project_id)
        assert os.path.exists(project_dir)
        assert os.path.exists(os.path.join(project_dir, "frontend"))
        assert os.path.exists(os.path.join(project_dir, "backend"))
        
        # Check specific files
        frontend_files = os.listdir(os.path.join(project_dir, "frontend"))
        backend_files = os.listdir(os.path.join(project_dir, "backend"))
        
        assert any("package.json" in f for f in frontend_files)
        assert any("main.py" in f for f in backend_files)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
