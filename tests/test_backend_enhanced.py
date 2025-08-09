
"""
Tests for Enhanced Backend Agent (Task 5)
"""
import pytest
import asyncio
import tempfile
import os
import json
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.backend_enhanced import BackendEnhancedAgent

class TestBackendEnhancedAgent:
    """Test cases for the Enhanced Backend Agent"""
    
    @pytest.fixture
    def agent_config(self):
        return {
            'agents': {
                'backend': {
                    'model': 'test-model',
                    'technologies': ['fastapi', 'flask', 'django']
                }
            }
        }
    
    @pytest.fixture
    def backend_agent(self, agent_config):
        return BackendEnhancedAgent(agent_config)
    
    def test_initialization(self, backend_agent):
        """Test agent initialization"""
        assert backend_agent.agent_id == "backend_enhanced"
        assert backend_agent.name == "Enhanced Backend Developer"
        assert "fastapi" in backend_agent.frameworks
        assert "postgresql" in backend_agent.databases
        assert "jwt" in backend_agent.auth_methods
    
    def test_capabilities(self, backend_agent):
        """Test agent capabilities"""
        capabilities = backend_agent.get_capabilities()
        
        expected_capabilities = [
            "advanced_fastapi_development",
            "flask_development_advanced",
            "django_development_advanced",
            "graphql_api_development",
            "rest_api_advanced",
            "authentication_systems",
            "authorization_rbac",
            "api_documentation_generation",
            "microservices_architecture",
            "database_integration_advanced"
        ]
        
        for capability in expected_capabilities:
            assert capability in capabilities
    
    def test_determine_framework(self, backend_agent):
        """Test framework determination"""
        # Test FastAPI detection
        architecture = {"backend": "fastapi"}
        framework = backend_agent._determine_framework(architecture, {}, {})
        assert framework == "fastapi"
        
        # Test Flask detection from requirements
        requirements = {"framework": "flask", "lightweight": True}
        framework = backend_agent._determine_framework({}, requirements, {})
        assert framework == "flask"
        
        # Test Django detection from task title
        task = {"title": "Create Django REST API"}
        framework = backend_agent._determine_framework({}, {}, task)
        assert framework == "django"
        
        # Test default fallback
        framework = backend_agent._determine_framework({}, {}, {})
        assert framework == "fastapi"
    
    def test_determine_database(self, backend_agent):
        """Test database determination"""
        # Test PostgreSQL detection
        requirements = {"database": "postgresql", "relational": True}
        database = backend_agent._determine_database(requirements)
        assert database == "postgresql"
        
        # Test MySQL detection
        requirements = {"db": "mysql", "sql": True}
        database = backend_agent._determine_database(requirements)
        assert database == "mysql"
        
        # Test MongoDB detection
        requirements = {"database": "mongodb", "nosql": True}
        database = backend_agent._determine_database(requirements)
        assert database == "mongodb"
        
        # Test default
        database = backend_agent._determine_database({})
        assert database == "postgresql"
    
    def test_determine_auth_method(self, backend_agent):
        """Test authentication method determination"""
        # Test JWT detection
        requirements = {"auth": "jwt", "tokens": True}
        auth_method = backend_agent._determine_auth_method(requirements)
        assert auth_method == "jwt"
        
        # Test OAuth2 detection
        requirements = {"authentication": "oauth2", "google": True}
        auth_method = backend_agent._determine_auth_method(requirements)
        assert auth_method == "oauth2"
        
        # Test API key detection
        requirements = {"api-key": True, "simple": True}
        auth_method = backend_agent._determine_auth_method(requirements)
        assert auth_method == "api-key"
        
        # Test default
        auth_method = backend_agent._determine_auth_method({})
        assert auth_method == "jwt"
    
    def test_determine_features(self, backend_agent):
        """Test feature determination"""
        requirements = {
            "graphql": True,
            "websockets": True,
            "caching": "redis",
            "rate_limiting": True,
            "file_upload": True
        }
        task = {"description": "Need email notifications and background tasks"}
        
        features = backend_agent._determine_features(requirements, task)
        
        assert "graphql" in features
        assert "websockets" in features
        assert "caching" in features
        assert "rate_limiting" in features
        assert "file_upload" in features
        assert "email" in features
        assert "background_tasks" in features
    
    def test_get_fastapi_main_file(self, backend_agent):
        """Test FastAPI main file generation"""
        features = ["cors", "swagger", "monitoring", "graphql", "websockets"]
        main_file = backend_agent._get_fastapi_main_file("postgresql", "jwt", features)
        
        # Check basic FastAPI structure
        assert "from fastapi import FastAPI" in main_file
        assert "app = FastAPI(" in main_file
        
        # Check CORS middleware
        assert "CORSMiddleware" in main_file
        
        # Check GraphQL integration
        assert "graphql_router" in main_file
        
        # Check WebSocket integration
        assert "websocket_router" in main_file
        
        # Check database information in response
        assert '"database": "postgresql"' in main_file
        assert '"authentication": "jwt"' in main_file
    
    def test_get_fastapi_config_file(self, backend_agent):
        """Test FastAPI configuration file generation"""
        config_file = backend_agent._get_fastapi_config_file("postgresql", "jwt")
        
        assert "class Settings(BaseSettings):" in config_file
        assert "DATABASE_URL:" in config_file
        assert "SECRET_KEY:" in config_file
        assert "ALGORITHM:" in config_file
        assert "ACCESS_TOKEN_EXPIRE_MINUTES:" in config_file
        assert "ALLOWED_HOSTS:" in config_file
    
    def test_get_sqlalchemy_database_file(self, backend_agent):
        """Test SQLAlchemy database file generation"""
        # Test PostgreSQL
        db_file = backend_agent._get_sqlalchemy_database_file("postgresql")
        assert "postgresql://" in db_file
        assert "create_engine" in db_file
        assert "SessionLocal" in db_file
        assert "Base = declarative_base()" in db_file
        
        # Test MySQL
        db_file = backend_agent._get_sqlalchemy_database_file("mysql")
        assert "mysql+pymysql://" in db_file
        
        # Test SQLite
        db_file = backend_agent._get_sqlalchemy_database_file("sqlite")
        assert "sqlite:///" in db_file
        assert "check_same_thread" in db_file
    
    def test_get_sqlalchemy_models_file(self, backend_agent):
        """Test SQLAlchemy models file generation"""
        models_file = backend_agent._get_sqlalchemy_models_file()
        
        assert "class User(Base):" in models_file
        assert "class Todo(Base):" in models_file
        assert "class ApiKey(Base):" in models_file
        
        # Check relationships
        assert "todos = relationship" in models_file
        assert "owner = relationship" in models_file
        
        # Check fields
        assert "username = Column" in models_file
        assert "email = Column" in models_file
        assert "hashed_password = Column" in models_file
    
    def test_get_fastapi_auth_file(self, backend_agent):
        """Test FastAPI authentication file generation"""
        # Test JWT auth
        auth_file = backend_agent._get_fastapi_auth_file("jwt")
        assert "from jose import JWTError, jwt" in auth_file
        assert "create_access_token" in auth_file
        assert "verify_token" in auth_file
        assert "get_current_user" in auth_file
        
        # Test API key auth
        auth_file = backend_agent._get_fastapi_auth_file("api-key")
        assert "verify_api_key" in auth_file
        assert "api_key.key == credentials.credentials" in auth_file
    
    def test_get_users_router(self, backend_agent):
        """Test users router generation"""
        router = backend_agent._get_users_router("postgresql", "jwt")
        
        assert "router = APIRouter()" in router
        assert "@router.post(\"/register\"" in router
        assert "@router.post(\"/token\"" in router
        assert "@router.get(\"/me\"" in router
        
        # Check authentication usage
        assert "get_current_active_user" in router
        assert "authenticate_user" in router
    
    def test_get_todos_router(self, backend_agent):
        """Test todos router generation"""
        router = backend_agent._get_todos_router("postgresql", "jwt")
        
        assert "router = APIRouter()" in router
        assert "@router.get(\"/\"" in router
        assert "@router.post(\"/\"" in router
        assert "@router.get(\"/{todo_id}\"" in router
        assert "@router.put(\"/{todo_id}\"" in router
        assert "@router.delete(\"/{todo_id}\"" in router
        
        # Check filtering parameters
        assert "completed: Optional[bool]" in router
        assert "priority: Optional[str]" in router
        assert "search: Optional[str]" in router
    
    def test_get_pydantic_schemas(self, backend_agent):
        """Test Pydantic schemas generation"""
        schemas = backend_agent._get_pydantic_schemas()
        
        # User schemas
        assert "class UserBase(BaseModel):" in schemas
        assert "class UserCreate(UserBase):" in schemas
        assert "class UserResponse(UserBase):" in schemas
        
        # Todo schemas
        assert "class TodoBase(BaseModel):" in schemas
        assert "class TodoCreate(TodoBase):" in schemas
        assert "class TodoUpdate(BaseModel):" in schemas
        assert "class TodoResponse(TodoBase):" in schemas
        
        # Auth schemas
        assert "class Token(BaseModel):" in schemas
        assert "class TokenData(BaseModel):" in schemas
    
    def test_get_crud_operations(self, backend_agent):
        """Test CRUD operations generation"""
        crud = backend_agent._get_crud_operations("postgresql")
        
        assert "class TodoCRUD:" in crud
        assert "def get_todo" in crud
        assert "def get_user_todos" in crud
        assert "def create_todo" in crud
        assert "def update_todo" in crud
        assert "def delete_todo" in crud
        assert "def get_user_todo_stats" in crud
        
        # Check filtering logic
        assert "completed is not None" in crud
        assert "priority" in crud
        assert "search" in crud
    
    def test_get_fastapi_middleware(self, backend_agent):
        """Test middleware generation"""
        middleware = backend_agent._get_fastapi_middleware(["cors", "rate_limiting"])
        
        assert "class TimingMiddleware" in middleware
        assert "class LoggingMiddleware" in middleware
        assert "def setup_middleware" in middleware
        assert "X-Process-Time" in middleware
    
    def test_get_health_check_file(self, backend_agent):
        """Test health check file generation"""
        health_file = backend_agent._get_health_check_file("postgresql")
        
        assert "router = APIRouter()" in health_file
        assert "@router.get(\"/\"" in health_file
        assert "@router.get(\"/detailed\"" in health_file
        assert "HealthResponse" in health_file
        assert "SELECT 1" in health_file
    
    def test_get_graphql_schema(self, backend_agent):
        """Test GraphQL schema generation"""
        schema = backend_agent._get_graphql_schema()
        
        assert "import strawberry" in schema
        assert "@strawberry.type" in schema
        assert "class UserType:" in schema
        assert "class TodoType:" in schema
        assert "class Query:" in schema
        assert "class Mutation:" in schema
    
    def test_get_websockets_handler(self, backend_agent):
        """Test WebSocket handler generation"""
        websocket = backend_agent._get_websockets_handler()
        
        assert "class ConnectionManager:" in websocket
        assert "async def connect" in websocket
        assert "def disconnect" in websocket
        assert "async def broadcast" in websocket
        assert "@router.websocket" in websocket
    
    def test_get_docker_files(self, backend_agent):
        """Test Docker configuration generation"""
        task = {"title": "Test API"}
        files = backend_agent._get_docker_compose_file("postgresql", ["caching"])
        
        assert "version:" in files
        assert "services:" in files
        assert "app:" in files
        assert "db:" in files
        assert "redis:" in files
        assert "volumes:" in files
    
    def test_get_fastapi_dockerfile(self, backend_agent):
        """Test Dockerfile generation"""
        dockerfile = backend_agent._get_fastapi_dockerfile()
        
        assert "FROM python:" in dockerfile
        assert "WORKDIR /app" in dockerfile
        assert "COPY requirements.txt" in dockerfile
        assert "pip install" in dockerfile
        assert "EXPOSE 8000" in dockerfile
        assert "HEALTHCHECK" in dockerfile
        assert "uvicorn main:app" in dockerfile
    
    def test_get_env_example(self, backend_agent):
        """Test environment example file generation"""
        env_file = backend_agent._get_env_example("postgresql", "jwt")
        
        assert "DATABASE_URL=" in env_file
        assert "SECRET_KEY=" in env_file
        assert "DEBUG=" in env_file
        assert "ALLOWED_HOSTS=" in env_file
        
        # Check PostgreSQL URL
        assert "postgresql://" in env_file
    
    def test_get_alembic_config(self, backend_agent):
        """Test Alembic configuration generation"""
        alembic_config = backend_agent._get_alembic_config()
        
        assert "[alembic]" in alembic_config
        assert "script_location = alembic" in alembic_config
        assert "[loggers]" in alembic_config
        assert "keys = root,sqlalchemy,alembic" in alembic_config
    
    def test_get_main_tests(self, backend_agent):
        """Test main tests generation"""
        tests = backend_agent._get_main_tests()
        
        assert "import pytest" in tests
        assert "from fastapi.testclient import TestClient" in tests
        assert "def test_read_root():" in tests
        assert "def test_health_check():" in tests
        assert "def test_register_user():" in tests
        assert "def test_login_user():" in tests
        
        # Check test database setup
        assert "SQLALCHEMY_DATABASE_URL" in tests
        assert "sqlite:///./test.db" in tests
    
    def test_get_auth_tests(self, backend_agent):
        """Test authentication tests generation"""
        auth_tests = backend_agent._get_auth_tests("jwt")
        
        assert "def test_create_access_token():" in auth_tests
        assert "def test_password_hashing():" in auth_tests
        assert "def test_invalid_login():" in auth_tests
        assert "def test_protected_route_without_token():" in auth_tests
        
        # Check JWT specific tests
        assert "verify_password" in auth_tests
        assert "get_password_hash" in auth_tests
    
    def test_get_crud_tests(self, backend_agent):
        """Test CRUD tests generation"""
        crud_tests = backend_agent._get_crud_tests()
        
        assert "def test_create_todo" in crud_tests
        assert "def test_get_todo" in crud_tests
        assert "def test_get_user_todos" in crud_tests
        assert "def test_update_todo" in crud_tests
        assert "def test_delete_todo" in crud_tests
        assert "def test_get_user_todo_stats" in crud_tests
    
    def test_get_fastapi_readme(self, backend_agent):
        """Test README generation"""
        readme = backend_agent._get_fastapi_readme("postgresql", "jwt", ["cors", "swagger"])
        
        assert "# Advanced FastAPI Backend" in readme
        assert "## Features" in readme
        assert "## Quick Start" in readme
        assert "## API Documentation" in readme
        assert "Database: Postgresql" in readme
        assert "Authentication: JWT" in readme
        
        # Check feature list
        assert "- Cors" in readme
        assert "- Swagger" in readme
    
    def test_get_api_documentation(self, backend_agent):
        """Test API documentation generation"""
        api_docs = backend_agent._get_api_documentation()
        
        assert "# API Documentation" in api_docs
        assert "## Authentication" in api_docs
        assert "## Endpoints" in api_docs
        assert "### Users" in api_docs
        assert "### Todos" in api_docs
        assert "## Error Codes" in api_docs
        assert "## WebSocket Support" in api_docs
    
    @pytest.mark.asyncio
    async def test_create_advanced_fastapi_backend(self, backend_agent):
        """Test advanced FastAPI backend creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Advanced FastAPI Backend",
                "description": "Create a comprehensive FastAPI backend",
                "requirements": {
                    "graphql": True,
                    "websockets": True,
                    "authentication": "jwt"
                },
                "output_dir": temp_dir
            }
            
            result = await backend_agent._create_advanced_fastapi_backend(
                task, temp_dir, "postgresql", "jwt", ["graphql", "websockets", "cors"]
            )
            
            assert result["status"] == "completed"
            assert result["technology"] == "FastAPI"
            assert result["database"] == "postgresql"
            assert result["authentication"] == "jwt"
            assert "graphql" in result["features"]
            assert len(result["files_created"]) > 20  # Should create many files
    
    @pytest.mark.asyncio
    async def test_create_advanced_flask_backend(self, backend_agent):
        """Test Flask backend creation placeholder"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {"title": "Flask API", "output_dir": temp_dir}
            
            result = await backend_agent._create_advanced_flask_backend(
                task, temp_dir, "postgresql", "jwt", []
            )
            
            assert result["status"] == "completed"
            assert result["technology"] == "Flask"
            assert "Flask backend implementation available" in result["message"]
    
    @pytest.mark.asyncio
    async def test_create_advanced_django_backend(self, backend_agent):
        """Test Django backend creation placeholder"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {"title": "Django API", "output_dir": temp_dir}
            
            result = await backend_agent._create_advanced_django_backend(
                task, temp_dir, "postgresql", "jwt", []
            )
            
            assert result["status"] == "completed"
            assert result["technology"] == "Django"
            assert "Django backend implementation available" in result["message"]
    
    @pytest.mark.asyncio
    async def test_process_task(self, backend_agent):
        """Test task processing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Create advanced API",
                "description": "FastAPI with GraphQL and JWT auth",
                "architecture": {"backend": "fastapi"},
                "requirements": {"graphql": True, "jwt": True},
                "output_dir": temp_dir
            }
            
            result = await backend_agent.process_task(task)
            
            assert result["status"] == "completed"
            assert result["technology"] == "FastAPI"
            assert backend_agent.status == "idle"
    
    @pytest.mark.asyncio
    async def test_process_task_error_handling(self, backend_agent):
        """Test error handling in task processing"""
        task = {
            "title": "Broken task",
            "output_dir": "/invalid/path/that/does/not/exist"
        }
        
        result = await backend_agent.process_task(task)
        
        assert result["status"] == "error"
        assert "message" in result
        assert result["files_created"] == []
        assert backend_agent.status == "error"
    
    def test_mongodb_database_file(self, backend_agent):
        """Test MongoDB database configuration"""
        db_file = backend_agent._get_mongodb_database_file()
        
        assert "AsyncIOMotorClient" in db_file
        assert "MONGODB_URL" in db_file
        assert "DATABASE_NAME" in db_file
        assert "def get_database():" in db_file
        assert "def get_sync_database():" in db_file
    
    def test_mongodb_models_file(self, backend_agent):
        """Test MongoDB models generation"""
        models = backend_agent._get_mongodb_models_file()
        
        assert "class PyObjectId(ObjectId):" in models
        assert "class MongoBaseModel(BaseModel):" in models
        assert "class User(MongoBaseModel):" in models
        assert "class Todo(MongoBaseModel):" in models
        assert "json_encoders = {ObjectId: str}" in models

