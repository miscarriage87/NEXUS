
# NEXUS System - Developer Guidelines

Comprehensive development documentation for contributing to the NEXUS Multi-Agent Platform. Guidelines for **657,453 lines of code**, 10+ specialized agents, and production-ready architecture.

## 🏗️ Development Environment Setup

### Prerequisites
```bash
# System Requirements
- Python 3.11+ (verified with 3.11.6)
- Node.js 16+ (for frontend projects)
- Git 2.30+
- Docker 20.10+ (optional, for containerized development)
- 8GB+ RAM (16GB recommended for LLM models)
- 50GB+ free disk space
```

### Development Setup
```bash
# 1. Clone & Navigate
cd /home/ubuntu/nexus

# 2. Python Environment  
python -m venv venv_dev
source venv_dev/bin/activate

# 3. Development Dependencies
pip install -e .  # Editable installation
pip install -r requirements-dev.txt

# Development tools
pip install black flake8 mypy pytest pytest-asyncio pytest-cov
pip install pre-commit isort bandit safety

# 4. Pre-commit Hooks Setup
pre-commit install

# 5. Ollama Development Models
ollama pull qwen2.5-coder:7b    # Primary development model
ollama pull qwen2:1.5b          # Lightweight testing model
```

### IDE Configuration

#### VS Code Setup
```json
// .vscode/settings.json
{
    "python.defaultInterpreter": "./venv_dev/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv*": true
    }
}
```

#### PyCharm Configuration
```python
# PyCharm Professional recommended settings:
# - Python Interpreter: ./venv_dev/bin/python  
# - Code Style: Black (88 character line length)
# - Type Checking: MyPy enabled
# - Test Runner: pytest
# - Version Control: Git with conventional commits
```

## 📋 Code Standards & Style Guide

### Python Code Style
We follow **Black** formatting with **88-character line length** and **PEP 8** compliance:

```python
# Good - NEXUS Style
class EnhancedBackendAgent(BaseAgent):
    """
    Enhanced backend agent for FastAPI application generation.
    
    Capabilities:
    - FastAPI + SQLAlchemy integration
    - Pydantic schema generation
    - JWT authentication
    - Docker containerization
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(
            agent_id="backend_enhanced",
            name="Enhanced Backend Developer", 
            config=config
        )
        self._supported_frameworks = ["fastapi", "flask", "django"]
        self._template_cache: Dict[str, str] = {}
    
    async def generate_fastapi_app(
        self, 
        specifications: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate complete FastAPI application."""
        try:
            # Validate input
            await self._validate_specifications(specifications)
            
            # Generate core components
            app_code = await self._generate_app_code(specifications)
            models_code = await self._generate_models(specifications)
            
            return {
                "status": "success",
                "app_code": app_code,
                "models_code": models_code,
                "deployment_ready": True
            }
            
        except Exception as e:
            self.logger.error(f"FastAPI generation failed: {e}")
            raise
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return [
            "fastapi_applications",
            "sqlalchemy_models",
            "pydantic_schemas",
            "jwt_authentication"
        ]
```

### Naming Conventions
```python
# Classes: PascalCase
class PerformanceMonitoringAgent(BaseAgent):
    pass

# Functions & Variables: snake_case  
async def process_project_request(request_data: Dict) -> ProjectResult:
    agent_response = await self._coordinate_agents(request_data)
    return agent_response

# Constants: UPPER_CASE
MAX_CONCURRENT_PROJECTS = 5
DEFAULT_LLM_TIMEOUT = 120

# Private Methods: _leading_underscore
def _validate_input(self, data: Dict) -> bool:
    pass

# Type Hints: Always use for public interfaces
from typing import Dict, List, Any, Optional, Union

async def generate_code(
    self, 
    template: str, 
    variables: Dict[str, Any],
    options: Optional[Dict[str, str]] = None
) -> Union[str, None]:
    pass
```

### Documentation Standards
```python
# Module Docstrings
"""
NEXUS Performance Agent - System Monitoring & Optimization

This module implements real-time performance monitoring for the NEXUS
multi-agent system, including:
- System resource monitoring (CPU, Memory, Disk)
- Agent performance metrics
- Bottleneck detection
- Automatic scaling recommendations

Example:
    Basic usage of the performance agent:
    
    >>> agent = PerformanceAgent(config)
    >>> await agent.initialize()
    >>> metrics = await agent.get_current_metrics()
    >>> print(f"CPU usage: {metrics['cpu_usage']}%")

TODO:
    - Implement continuous monitoring loop (Line 45)
    - Add alerting system integration
    - Performance regression detection
"""

# Class Docstrings - Google Style
class ContextAgent(BaseAgent):
    """
    Context and memory management agent for NEXUS system.
    
    Manages conversation history, semantic search, and knowledge extraction
    across agent interactions. Provides persistent memory and context
    retrieval for enhanced agent coordination.
    
    Attributes:
        memory_db_path (str): Path to SQLite knowledge database
        context_window_size (int): Maximum context tokens to maintain
        semantic_search_enabled (bool): Whether semantic search is available
        
    Example:
        Initialize and store conversation context:
        
        >>> context_agent = ContextAgent(config)
        >>> await context_agent.initialize()
        >>> await context_agent.store_conversation({
        ...     "conversation_id": "proj_123",
        ...     "participants": ["orchestrator", "backend"],
        ...     "messages": [...]
        ... })
    """

# Method Docstrings
async def analyze_code_quality(self, code_path: str) -> Dict[str, Any]:
    """
    Perform comprehensive code quality analysis.
    
    Analyzes Python code for complexity, test coverage, security issues,
    and adherence to best practices. Generates actionable recommendations
    for code improvement.
    
    Args:
        code_path (str): Absolute path to code directory or file
        
    Returns:
        Dict[str, Any]: Analysis results containing:
            - overall_score (float): Quality score 0-100
            - metrics (Dict): Detailed metrics breakdown
            - recommendations (List[Dict]): Improvement suggestions
            - file_analysis (List[Dict]): Per-file analysis
            
    Raises:
        FileNotFoundError: If code_path doesn't exist
        PermissionError: If insufficient permissions to read files
        QualityAnalysisError: If analysis tools fail
        
    Example:
        >>> qa_agent = QAAgent(config)
        >>> result = await qa_agent.analyze_code_quality("/path/to/project")
        >>> print(f"Quality Score: {result['overall_score']}")
        >>> for rec in result['recommendations']:
        ...     print(f"- {rec['description']}")
    """
```

## 🏗️ Architecture Guidelines

### Agent Development Pattern
Every NEXUS agent follows a standardized architecture:

```python
# Template for new agent development
from core.base_agent import BaseAgent
from core.messaging import Message
from typing import Dict, Any, List, Optional
import logging
import asyncio

class NewSpecializedAgent(BaseAgent):
    """
    Template for implementing new NEXUS agents.
    
    Required Implementation:
    - get_capabilities(): Return list of agent capabilities
    - process_task(): Handle incoming tasks
    - Optional: Custom initialization, health checks, cleanup
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            agent_id="new_specialized",          # Unique agent identifier
            name="New Specialized Agent",       # Human-readable name
            config=config
        )
        
        # Agent-specific initialization
        self.specialized_config = config.get('new_specialized', {})
        self.max_concurrent_tasks = self.specialized_config.get('max_tasks', 3)
        self.task_queue: asyncio.Queue = asyncio.Queue()
        
        # Performance tracking
        self.task_metrics = {
            "completed_tasks": 0,
            "failed_tasks": 0,
            "avg_processing_time": 0.0
        }
    
    def get_capabilities(self) -> List[str]:
        """
        Define agent capabilities - REQUIRED IMPLEMENTATION.
        
        Returns comprehensive list of what this agent can do.
        Used by orchestrator for task assignment.
        """
        return [
            "specialized_task_type_1",
            "specialized_task_type_2", 
            "data_processing",
            "custom_analysis",
            "report_generation"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core task processing - REQUIRED IMPLEMENTATION.
        
        All agents must implement this method to handle task requests
        from the orchestrator or other agents.
        """
        task_type = task.get("type")
        task_id = task.get("task_id", "unknown")
        
        self.logger.info(f"Processing task {task_id} of type {task_type}")
        
        try:
            # Route to specific handler based on task type
            if task_type == "specialized_task_type_1":
                return await self._handle_specialized_task_1(task)
            elif task_type == "data_processing":
                return await self._handle_data_processing(task)
            else:
                raise ValueError(f"Unsupported task type: {task_type}")
                
        except Exception as e:
            self.logger.error(f"Task {task_id} failed: {e}")
            self.task_metrics["failed_tasks"] += 1
            
            return {
                "status": "failed",
                "task_id": task_id,
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def _handle_specialized_task_1(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle specialized task type 1."""
        # Implementation specific to this task type
        
        # LLM integration example
        if hasattr(self, 'ollama_client') and self.ollama_client:
            llm_response = await self._use_llm_for_task(task)
        else:
            # Fallback to template-based approach
            llm_response = self._template_based_processing(task)
        
        result = {
            "status": "success",
            "task_id": task.get("task_id"),
            "result": llm_response,
            "processing_time": "calculated",
            "agent_id": self.agent_id
        }
        
        self.task_metrics["completed_tasks"] += 1
        return result
    
    async def _use_llm_for_task(self, task: Dict[str, Any]) -> str:
        """Use LLM for task processing with proper error handling."""
        system_prompt = """
        You are a specialized AI agent in the NEXUS system.
        Process the given task according to your capabilities.
        Provide structured, actionable output.
        """
        
        user_prompt = f"""
        Task Type: {task.get('type')}
        Task Data: {task.get('data', {})}
        Requirements: {task.get('requirements', [])}
        
        Process this task and provide detailed results.
        """
        
        try:
            response = await self.ollama_client.generate(
                model=self.config['ollama']['models'].get(
                    'new_specialized', 
                    'qwen2.5-coder:7b'
                ),
                system=system_prompt,
                prompt=user_prompt,
                temperature=0.1
            )
            
            return response['response']
            
        except Exception as e:
            self.logger.warning(f"LLM processing failed: {e}, using fallback")
            return self._template_based_processing(task)
    
    def _template_based_processing(self, task: Dict[str, Any]) -> str:
        """Fallback processing without LLM."""
        return f"Template-based result for task {task.get('task_id')}"
    
    # Override initialization if needed
    async def initialize(self) -> bool:
        """Custom agent initialization."""
        # Call parent initialization first
        if not await super().initialize():
            return False
        
        # Agent-specific initialization
        try:
            await self._setup_specialized_resources()
            self.logger.info(f"Agent {self.agent_id} specialized setup complete")
            return True
        except Exception as e:
            self.logger.error(f"Specialized initialization failed: {e}")
            return False
    
    async def _setup_specialized_resources(self):
        """Setup agent-specific resources."""
        # Database connections, API clients, etc.
        pass
    
    # Override health check if needed
    async def health_check(self) -> Dict[str, Any]:
        """Extended health check with agent-specific metrics."""
        base_health = await super().health_check()
        
        # Add specialized health information
        specialized_health = {
            "task_metrics": self.task_metrics,
            "queue_size": self.task_queue.qsize(),
            "specialized_status": "healthy",  # Custom logic here
            "resource_usage": await self._check_resource_usage()
        }
        
        return {**base_health, **specialized_health}
    
    async def _check_resource_usage(self) -> Dict[str, Any]:
        """Check agent-specific resource usage."""
        return {
            "memory_mb": "calculated", 
            "active_connections": 0,
            "cache_size": 0
        }
```

### Message Bus Integration
```python
# Message-based agent communication
class MessageIntegratedAgent(BaseAgent):
    """Example of proper message bus integration."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("message_agent", "Message Integrated Agent", config)
        self.message_subscriptions = [
            "project_created",
            "quality_check_required",
            "deployment_requested"
        ]
    
    async def initialize(self) -> bool:
        """Initialize with message subscriptions."""
        if not await super().initialize():
            return False
        
        # Subscribe to relevant message types
        for message_type in self.message_subscriptions:
            await self.message_bus.subscribe(message_type, self._handle_message)
        
        return True
    
    async def _handle_message(self, message: Message):
        """Handle incoming messages from message bus."""
        message_type = message.type
        content = message.content
        
        self.logger.info(f"Received message: {message_type} from {message.from_agent}")
        
        if message_type == "project_created":
            await self._handle_project_created(content)
        elif message_type == "quality_check_required":
            await self._handle_quality_check(content, message.correlation_id)
        # ... handle other message types
    
    async def _send_response_message(self, response_data: Dict, original_message: Message):
        """Send response message back to requesting agent."""
        response_message = Message(
            type="task_response",
            from_agent=self.agent_id,
            to_agent=original_message.from_agent,
            content=response_data,
            correlation_id=original_message.correlation_id
        )
        
        await self.message_bus.send_message(response_message)
```

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_base_agent.py
│   ├── test_messaging.py
│   └── agents/
│       ├── test_orchestrator.py
│       ├── test_backend.py
│       └── test_frontend.py
├── integration/             # Integration tests
│   ├── test_agent_communication.py
│   ├── test_project_generation.py
│   └── test_llm_integration.py  
├── e2e/                    # End-to-end tests
│   ├── test_full_project_creation.py
│   └── test_system_startup.py
├── fixtures/               # Test data and fixtures
│   ├── sample_configs.yaml
│   ├── mock_llm_responses.json
│   └── test_projects/
└── conftest.py            # Pytest configuration
```

### Unit Test Example
```python
# tests/unit/agents/test_backend_enhanced.py
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from agents.backend_enhanced import BackendEnhancedAgent

class TestBackendEnhancedAgent:
    """Test suite for BackendEnhancedAgent."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            'ollama': {
                'models': {'backend': 'test-model'},
                'base_url': 'http://localhost:11434'
            },
            'backend': {
                'supported_frameworks': ['fastapi', 'flask']
            }
        }
    
    @pytest.fixture
    def backend_agent(self, mock_config):
        """Create backend agent instance for testing."""
        agent = BackendEnhancedAgent(mock_config)
        agent.ollama_client = AsyncMock()
        return agent
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, backend_agent):
        """Test agent initialization."""
        # Mock the ollama client setup
        backend_agent.ollama_client.check_health = AsyncMock(return_value=True)
        
        result = await backend_agent.initialize()
        
        assert result is True
        assert backend_agent.is_initialized is True
        assert backend_agent.agent_id == "backend_enhanced"
    
    @pytest.mark.asyncio
    async def test_get_capabilities(self, backend_agent):
        """Test capabilities retrieval."""
        capabilities = backend_agent.get_capabilities()
        
        assert isinstance(capabilities, list)
        assert "fastapi_applications" in capabilities
        assert "sqlalchemy_models" in capabilities
        assert len(capabilities) > 0
    
    @pytest.mark.asyncio
    async def test_fastapi_generation(self, backend_agent):
        """Test FastAPI application generation."""
        # Mock LLM response
        mock_llm_response = {
            'response': 'from fastapi import FastAPI\napp = FastAPI()'
        }
        backend_agent.ollama_client.generate = AsyncMock(return_value=mock_llm_response)
        
        # Mock file writing
        with patch('builtins.open', create=True) as mock_open:
            with patch('os.makedirs') as mock_makedirs:
                task = {
                    "type": "generate_backend",
                    "project_id": "test-123",
                    "specifications": {
                        "framework": "fastapi",
                        "database": "sqlite"
                    }
                }
                
                result = await backend_agent.process_task(task)
                
                assert result["status"] == "success"
                assert "backend_path" in result
                assert result["framework"] == "fastapi"
                
                # Verify LLM was called
                backend_agent.ollama_client.generate.assert_called_once()
                
                # Verify file operations
                mock_makedirs.assert_called()
                mock_open.assert_called()
    
    @pytest.mark.asyncio
    async def test_error_handling(self, backend_agent):
        """Test error handling in task processing."""
        # Mock LLM failure
        backend_agent.ollama_client.generate = AsyncMock(
            side_effect=Exception("LLM connection failed")
        )
        
        task = {
            "type": "generate_backend", 
            "project_id": "test-error",
            "specifications": {}
        }
        
        # Should fall back to template-based generation
        with patch.object(backend_agent, '_template_based_backend') as mock_template:
            mock_template.return_value = {"status": "success", "method": "template"}
            
            result = await backend_agent.process_task(task)
            
            # Should succeed with template fallback
            mock_template.assert_called_once()
            assert result["method"] == "template"
    
    def test_unsupported_task_type(self, backend_agent):
        """Test handling of unsupported task types."""
        task = {"type": "unsupported_task"}
        
        with pytest.raises(ValueError, match="Unsupported task type"):
            asyncio.run(backend_agent.process_task(task))
    
    @pytest.mark.parametrize("framework,expected", [
        ("fastapi", True),
        ("flask", True), 
        ("django", True),
        ("unsupported", False)
    ])
    def test_framework_support(self, backend_agent, framework, expected):
        """Test framework support validation."""
        is_supported = framework in backend_agent._supported_frameworks
        assert is_supported == expected
```

### Integration Test Example
```python
# tests/integration/test_agent_communication.py
import pytest
import asyncio
from core.messaging import MessageBus, Message
from agents.orchestrator_enhanced import EnhancedOrchestratorAgent
from agents.backend_enhanced import BackendEnhancedAgent

class TestAgentCommunication:
    """Test inter-agent communication via message bus."""
    
    @pytest.fixture
    async def message_bus(self):
        """Create and start message bus for testing."""
        bus = MessageBus()
        await bus.start_processing()
        yield bus
        await bus.stop_processing()
    
    @pytest.fixture
    async def orchestrator_agent(self, mock_config, message_bus):
        """Create orchestrator agent."""
        agent = EnhancedOrchestratorAgent(mock_config, message_bus)
        agent.ollama_client = AsyncMock()
        await agent.initialize()
        await message_bus.register_agent("orchestrator", agent)
        return agent
    
    @pytest.fixture  
    async def backend_agent(self, mock_config, message_bus):
        """Create backend agent.""" 
        agent = BackendEnhancedAgent(mock_config)
        agent.ollama_client = AsyncMock()
        await agent.initialize()
        await message_bus.register_agent("backend", agent)
        return agent
    
    @pytest.mark.asyncio
    async def test_orchestrator_to_backend_communication(
        self, message_bus, orchestrator_agent, backend_agent
    ):
        """Test message flow from orchestrator to backend agent."""
        
        # Mock backend response
        backend_agent.process_task = AsyncMock(return_value={
            "status": "success",
            "backend_path": "/test/path"
        })
        
        # Send task from orchestrator to backend
        task_message = Message(
            type="task_request",
            from_agent="orchestrator",
            to_agent="backend",
            content={
                "type": "generate_backend",
                "project_id": "test-comm-123"
            }
        )
        
        await message_bus.send_message(task_message)
        
        # Wait for processing
        await asyncio.sleep(0.1)
        
        # Verify backend received and processed the task
        backend_agent.process_task.assert_called_once()
        call_args = backend_agent.process_task.call_args[0][0]
        assert call_args["type"] == "generate_backend"
        assert call_args["project_id"] == "test-comm-123"
```

### End-to-End Test Example
```python
# tests/e2e/test_full_project_creation.py
import pytest
import asyncio
import os
import tempfile
from pathlib import Path

@pytest.mark.e2e
@pytest.mark.slow 
class TestFullProjectCreation:
    """End-to-end tests for complete project creation."""
    
    @pytest.mark.asyncio
    async def test_todo_app_generation(self, system_initializer):
        """Test complete todo application generation."""
        
        project_request = {
            "type": "fullstack_webapp",
            "name": "Test Todo App",
            "description": "Simple todo application for testing",
            "technologies": {
                "frontend": "react",
                "backend": "fastapi",
                "database": "sqlite"
            },
            "features": [
                "user_authentication",
                "crud_operations",
                "responsive_design"
            ]
        }
        
        # Generate project
        result = await system_initializer.orchestrator.process_project_request(
            project_request
        )
        
        # Verify result structure
        assert result["status"] == "success"
        assert "project_id" in result
        assert "project_path" in result
        
        project_path = Path(result["project_path"])
        assert project_path.exists()
        
        # Verify backend structure
        backend_path = project_path / "backend"
        assert (backend_path / "main.py").exists()
        assert (backend_path / "models.py").exists()
        assert (backend_path / "requirements.txt").exists()
        
        # Verify frontend structure  
        frontend_path = project_path / "frontend"
        assert (frontend_path / "package.json").exists()
        assert (frontend_path / "src" / "App.js").exists()
        
        # Verify code quality
        backend_main = (backend_path / "main.py").read_text()
        assert "FastAPI" in backend_main
        assert "app = FastAPI" in backend_main
        
        frontend_package = (frontend_path / "package.json").read_text()
        assert "react" in frontend_package.lower()
        
        # Verify deployment readiness
        assert result.get("deployment_ready") is True
        assert (backend_path / "Dockerfile").exists()
```

### Test Configuration
```python
# tests/conftest.py
import pytest
import asyncio
import yaml
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_config():
    """Standard mock configuration for tests."""
    return {
        'nexus': {
            'version': '2.0.0',
            'environment': 'test'
        },
        'ollama': {
            'base_url': 'http://localhost:11434',
            'timeout': 30,
            'models': {
                'orchestrator': 'qwen2:1.5b',
                'backend': 'qwen2:1.5b', 
                'frontend': 'qwen2:1.5b'
            }
        },
        'agents': {
            'orchestrator': {
                'max_concurrent_projects': 2
            }
        }
    }

@pytest.fixture
def temp_project_dir():
    """Temporary directory for test projects."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client for testing.""" 
    client = AsyncMock()
    client.check_health.return_value = True
    client.list_models.return_value = [
        {"name": "qwen2:1.5b", "size": 1000000000}
    ]
    client.generate.return_value = {
        "response": "# Generated code",
        "model": "qwen2:1.5b"
    }
    return client

# Markers for test categories
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests") 
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow-running tests")
    config.addinivalue_line("markers", "llm: Tests requiring LLM service")

# Test running configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers."""
    if config.getoption("--no-slow"):
        skip_slow = pytest.mark.skip(reason="--no-slow option given")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
```

### Running Tests
```bash
# All tests
python -m pytest tests/ -v

# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests
python -m pytest tests/integration/ -v

# End-to-end tests (slow)
python -m pytest tests/e2e/ -v -m e2e

# Skip slow tests
python -m pytest tests/ -v --no-slow

# With coverage
python -m pytest tests/ --cov=agents --cov=core --cov-report=html

# Specific test file
python -m pytest tests/unit/agents/test_backend_enhanced.py -v

# Test with specific marker
python -m pytest -m "not slow" -v

# Parallel test execution
python -m pytest tests/ -v -n auto  # requires pytest-xdist
```

## 🚀 Development Workflow

### Git Workflow
We follow **Git Flow** with conventional commits:

```bash
# Feature Development Workflow
git checkout develop
git pull origin develop
git checkout -b feature/new-agent-implementation

# Make changes...
git add .
git commit -m "feat(agent): implement specialized analysis agent

- Add AnalysisAgent with natural language processing capabilities
- Integrate with LLM for document analysis
- Add comprehensive test suite
- Update documentation

Closes #123"

# Push feature branch
git push origin feature/new-agent-implementation

# Create Pull Request to develop branch
# After review and approval, merge via GitHub/GitLab
```

### Conventional Commit Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix  
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Scopes:**
- `agent`: Agent-related changes
- `core`: Core system changes
- `config`: Configuration changes
- `test`: Test-related changes
- `docs`: Documentation changes

**Examples:**
```bash
git commit -m "feat(agent): add performance monitoring capabilities"
git commit -m "fix(core): resolve async initialization race condition"
git commit -m "docs(api): update agent capability documentation" 
git commit -m "test(integration): add message bus communication tests"
git commit -m "refactor(backend): extract common FastAPI generation logic"
```

### Pull Request Process

#### PR Template
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass  
- [ ] End-to-end tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented appropriately
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new security vulnerabilities introduced

## Related Issues
Closes #123
```

#### Review Process
1. **Automated Checks**: CI/CD pipeline runs tests, linting, security scans
2. **Code Review**: At least 1 reviewer required, 2 for core changes
3. **Testing**: All tests must pass, coverage maintained
4. **Documentation**: Updates required for new features
5. **Merge**: Squash and merge to develop branch

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, -x, tests/]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-yaml
```

## 📦 Deployment & Release

### Version Management
We use **Semantic Versioning** (SemVer):

```
MAJOR.MINOR.PATCH

Examples:
2.0.0 - Major release with breaking changes
2.1.0 - Minor release with new features  
2.1.1 - Patch release with bug fixes
```

### Release Process
```bash
# 1. Prepare Release Branch
git checkout develop
git pull origin develop
git checkout -b release/2.1.0

# 2. Update Version Numbers
# Update version in:
# - setup.py
# - __init__.py files
# - documentation
# - CHANGELOG.md

# 3. Final Testing
python -m pytest tests/ -v --cov=agents --cov=core

# 4. Build & Package
python setup.py sdist bdist_wheel

# 5. Tag Release
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

# 6. Merge to Main
git checkout main
git merge release/2.1.0
git push origin main

# 7. Merge back to Develop
git checkout develop  
git merge release/2.1.0
git push origin develop
```

### Docker Development
```dockerfile
# Dockerfile.dev - Development container
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install development dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Install pre-commit hooks
RUN pip install pre-commit

# Copy source code
COPY . .

# Install in development mode
RUN pip install -e .

# Expose ports
EXPOSE 8000 8080

CMD ["python", "start_nexus.py"]
```

```yaml
# docker-compose.dev.yml - Development environment
version: '3.8'

services:
  nexus-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
      - "8080:8080"
    volumes:
      - .:/app
      - /app/venv_dev  # Exclude venv from mount
    environment:
      - NEXUS_ENV=development
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
      - redis

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    environment:
      - OLLAMA_ORIGINS=*

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  ollama_models:
  redis_data:
```

## 🔍 Debugging & Profiling

### Logging Best Practices
```python
# Structured logging for development
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logger for NEXUS development."""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Console handler for development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Custom formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log info with structured data."""
        self._log_structured(logging.INFO, message, **kwargs)
    
    def error(self, message: str, error: Exception = None, **kwargs):
        """Log error with exception details."""
        error_data = {}
        if error:
            error_data = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "traceback": format_exc() if hasattr(error, '__traceback__') else None
            }
        
        self._log_structured(logging.ERROR, message, error=error_data, **kwargs)
    
    def _log_structured(self, level: int, message: str, **kwargs):
        """Log with structured data."""
        log_data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs
        }
        
        if kwargs:
            self.logger.log(level, f"{message} | Data: {json.dumps(log_data)}")
        else:
            self.logger.log(level, message)

# Usage in agents
logger = StructuredLogger("nexus.backend_agent")

logger.info(
    "Processing backend generation task",
    project_id="proj_123",
    framework="fastapi",
    estimated_duration=120
)

logger.error(
    "LLM generation failed", 
    error=e,
    task_id="task_456",
    retry_count=3
)
```

### Performance Profiling
```python
# Performance profiling for development
import cProfile
import pstats
import time
from functools import wraps
from typing import Callable

def profile_performance(func: Callable):
    """Decorator for profiling function performance."""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        if hasattr(func, '_is_coroutine'):
            # Async function profiling
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            
            duration = end_time - start_time
            print(f"🔍 {func.__name__} took {duration:.4f} seconds")
            
            return result
        else:
            # Sync function profiling
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            duration = end_time - start_time
            print(f"🔍 {func.__name__} took {duration:.4f} seconds")
            
            return result
    
    return async_wrapper

# Usage
@profile_performance
async def generate_backend_code(self, specifications):
    """Generate backend code with performance profiling."""
    # Implementation...
    pass

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function with memory profiling."""
    # Implementation that might have memory issues
    pass

# Line-by-line profiling
def profile_agent_method(agent_instance, method_name: str):
    """Profile specific agent method line by line."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Execute method
    method = getattr(agent_instance, method_name)
    result = method()
    
    profiler.disable()
    
    # Generate report
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
    
    return result
```

## 📚 Contributing Guidelines

### New Agent Development
To contribute a new agent to NEXUS:

1. **Create Agent Class**:
   ```python
   # agents/my_new_agent.py
   from core.base_agent import BaseAgent
   
   class MyNewAgent(BaseAgent):
       def __init__(self, config):
           super().__init__("my_new", "My New Agent", config)
       
       def get_capabilities(self):
           return ["my_capability_1", "my_capability_2"]
       
       async def process_task(self, task):
           # Implementation
           pass
   ```

2. **Add Configuration**:
   ```yaml
   # nexus_config.yaml
   agents:
     my_new:
       max_concurrent_tasks: 3
       custom_setting: "value"
   ```

3. **Write Tests**:
   ```python
   # tests/unit/agents/test_my_new_agent.py
   import pytest
   from agents.my_new_agent import MyNewAgent
   
   class TestMyNewAgent:
       # Comprehensive test suite
       pass
   ```

4. **Update Documentation**:
   - Add to API_REFERENCE.md
   - Update ARCHITECTURE.md
   - Add usage examples

### Bug Reports
When reporting bugs, include:

1. **Environment Information**:
   ```
   - Python version
   - NEXUS version
   - Operating System
   - Ollama version
   - Available models
   ```

2. **Reproduction Steps**:
   ```
   1. Configure system with...
   2. Execute command...
   3. Expected vs actual behavior
   ```

3. **Log Output**:
   ```
   Relevant log entries with timestamps
   Error tracebacks
   System resource usage
   ```

4. **Minimal Example**:
   ```python
   # Minimal code that reproduces the issue
   ```

### Feature Requests
Structure feature requests with:

1. **Problem Statement**: What problem does this solve?
2. **Proposed Solution**: How should it work?
3. **Alternatives Considered**: What other options were considered?
4. **Impact Assessment**: How does this affect existing functionality?
5. **Implementation Notes**: Technical considerations

---

**NEXUS Development Guide v2.0.0** - Complete Developer Documentation

**Standards**: Python 3.11+ | Black Formatting | Async-First | Comprehensive Testing | Production-Ready Code

