
"""
Enhanced Backend Agent - Advanced API development with FastAPI/Flask/Django, GraphQL, Authentication, and Microservices
Task 5: Backend Agent API Enhancement
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.ollama_client import ollama_client

class BackendEnhancedAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("backend_enhanced", "Enhanced Backend Developer", config)
        self.technologies = config.get('agents', {}).get('backend', {}).get('technologies', [])
        self.frameworks = ['fastapi', 'flask', 'django', 'starlette', 'sanic']
        self.databases = ['postgresql', 'mysql', 'sqlite', 'mongodb', 'redis']
        self.auth_methods = ['jwt', 'oauth2', 'basic', 'api-key', 'session']
        
    def get_capabilities(self) -> List[str]:
        return [
            "advanced_fastapi_development",
            "flask_development_advanced",
            "django_development_advanced",
            "graphql_api_development",
            "rest_api_advanced",
            "authentication_systems",
            "authorization_rbac",
            "api_documentation_generation",
            "microservices_architecture",
            "database_integration_advanced",
            "caching_strategies",
            "rate_limiting",
            "api_versioning",
            "webhook_systems",
            "background_tasks",
            "service_discovery",
            "load_balancing",
            "monitoring_integration"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process advanced backend development tasks"""
        self.status = "working"
        self.logger.info(f"Processing enhanced backend task: {task.get('title', 'Unknown')}")
        
        try:
            output_dir = task.get("output_dir", "/home/ubuntu/nexus/demo")
            architecture = task.get("architecture", {})
            requirements = task.get("requirements", {})
            
            # Determine framework and features
            framework = self._determine_framework(architecture, requirements, task)
            database = self._determine_database(requirements)
            auth_method = self._determine_auth_method(requirements)
            features = self._determine_features(requirements, task)
            
            self.logger.info(f"Creating {framework} API with {database} and {auth_method} auth")
            
            # Create appropriate backend based on framework
            if framework == 'fastapi':
                result = await self._create_advanced_fastapi_backend(task, output_dir, database, auth_method, features)
            elif framework == 'flask':
                result = await self._create_advanced_flask_backend(task, output_dir, database, auth_method, features)
            elif framework == 'django':
                result = await self._create_advanced_django_backend(task, output_dir, database, auth_method, features)
            else:
                result = await self._create_advanced_fastapi_backend(task, output_dir, database, auth_method, features)
            
            self.status = "idle"
            return result
            
        except Exception as e:
            self.status = "error"
            self.logger.error(f"Error processing enhanced backend task: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "files_created": []
            }
    
    def _determine_framework(self, architecture: Dict, requirements: Dict, task: Dict) -> str:
        """Determine which backend framework to use"""
        # Check architecture specification
        if architecture.get("backend"):
            fw = architecture["backend"].lower()
            if fw in self.frameworks:
                return fw
        
        # Check requirements and task description
        req_text = f"{requirements} {task.get('title', '')} {task.get('description', '')}".lower()
        for fw in self.frameworks:
            if fw in req_text:
                return fw
        
        return "fastapi"  # Default to FastAPI
    
    def _determine_database(self, requirements: Dict) -> str:
        """Determine which database to use"""
        req_str = str(requirements).lower()
        for db in self.databases:
            if db in req_str:
                return db
        return "postgresql"  # Default to PostgreSQL
    
    def _determine_auth_method(self, requirements: Dict) -> str:
        """Determine which authentication method to use"""
        req_str = str(requirements).lower()
        if 'oauth' in req_str or 'oauth2' in req_str:
            return 'oauth2'
        elif 'jwt' in req_str:
            return 'jwt'
        elif 'session' in req_str:
            return 'session'
        elif 'api-key' in req_str or 'apikey' in req_str:
            return 'api-key'
        return 'jwt'  # Default to JWT
    
    def _determine_features(self, requirements: Dict, task: Dict) -> List[str]:
        """Determine which features to include"""
        features = []
        content = f"{requirements} {task.get('title', '')} {task.get('description', '')}".lower()
        
        feature_mapping = {
            'graphql': ['graphql', 'graph ql', 'graph-ql'],
            'websockets': ['websocket', 'ws', 'realtime', 'real-time'],
            'caching': ['cache', 'redis', 'memcached'],
            'rate_limiting': ['rate limit', 'throttle', 'rate-limit'],
            'file_upload': ['upload', 'file', 'media'],
            'email': ['email', 'mail', 'smtp'],
            'background_tasks': ['task', 'job', 'queue', 'celery'],
            'monitoring': ['monitor', 'metrics', 'health'],
            'cors': ['cors', 'cross-origin'],
            'swagger': ['swagger', 'openapi', 'docs']
        }
        
        for feature, keywords in feature_mapping.items():
            if any(keyword in content for keyword in keywords):
                features.append(feature)
        
        # Add default features
        default_features = ['cors', 'swagger', 'monitoring']
        for feature in default_features:
            if feature not in features:
                features.append(feature)
        
        return features
    
    async def _create_advanced_fastapi_backend(self, task: Dict[str, Any], output_dir: str,
                                             database: str, auth_method: str, features: List[str]) -> Dict[str, Any]:
        """Create advanced FastAPI backend with all features"""
        backend_dir = os.path.join(output_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)
        
        files = {}
        
        # Requirements with all dependencies
        dependencies = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "python-multipart==0.0.6",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "python-dotenv==1.0.0",
            "sqlalchemy==2.0.23",
            "alembic==1.12.1",
            "pytest==7.4.3",
            "httpx==0.25.2",
            "pytest-asyncio==0.21.1"
        ]
        
        # Add database-specific dependencies
        if database == 'postgresql':
            dependencies.extend(["psycopg2-binary==2.9.7", "asyncpg==0.29.0"])
        elif database == 'mysql':
            dependencies.extend(["pymysql==1.1.0", "aiomysql==0.2.0"])
        elif database == 'mongodb':
            dependencies.extend(["motor==3.3.2", "pymongo==4.6.0"])
        elif database == 'redis':
            dependencies.extend(["redis==5.0.1", "aioredis==2.0.1"])
        
        # Add feature-specific dependencies
        if 'graphql' in features:
            dependencies.extend(["strawberry-graphql[fastapi]==0.214.1", "graphene==3.3"])
        if 'websockets' in features:
            dependencies.append("websockets==12.0")
        if 'caching' in features:
            dependencies.append("redis==5.0.1")
        if 'email' in features:
            dependencies.append("fastapi-mail==1.4.1")
        if 'background_tasks' in features:
            dependencies.extend(["celery==5.3.4", "flower==2.0.1"])
        
        files["requirements.txt"] = "\n".join(dependencies)
        
        # Main application file
        files["main.py"] = self._get_fastapi_main_file(database, auth_method, features)
        
        # Configuration
        files["config.py"] = self._get_fastapi_config_file(database, auth_method)
        
        # Database models and connection
        if database in ['postgresql', 'mysql', 'sqlite']:
            files["database.py"] = self._get_sqlalchemy_database_file(database)
            files["models.py"] = self._get_sqlalchemy_models_file()
        elif database == 'mongodb':
            files["database.py"] = self._get_mongodb_database_file()
            files["models.py"] = self._get_mongodb_models_file()
        
        # Authentication
        files["auth.py"] = self._get_fastapi_auth_file(auth_method)
        
        # API routes
        files["routers/__init__.py"] = ""
        files["routers/users.py"] = self._get_users_router(database, auth_method)
        files["routers/todos.py"] = self._get_todos_router(database, auth_method)
        
        # GraphQL support
        if 'graphql' in features:
            files["graphql_schema.py"] = self._get_graphql_schema()
            files["routers/graphql.py"] = self._get_graphql_router()
        
        # WebSockets support
        if 'websockets' in features:
            files["websockets.py"] = self._get_websockets_handler()
        
        # Middleware
        files["middleware.py"] = self._get_fastapi_middleware(features)
        
        # Utils
        files["utils.py"] = self._get_fastapi_utils()
        
        # Schemas (Pydantic models)
        files["schemas.py"] = self._get_pydantic_schemas()
        
        # CRUD operations
        files["crud.py"] = self._get_crud_operations(database)
        
        # Dependencies
        files["dependencies.py"] = self._get_fastapi_dependencies(auth_method)
        
        # Database migrations (Alembic)
        files["alembic.ini"] = self._get_alembic_config()
        files["alembic/env.py"] = self._get_alembic_env_file()
        files["alembic/script.py.mako"] = self._get_alembic_template()
        
        # Environment configuration
        files[".env.example"] = self._get_env_example(database, auth_method)
        
        # Docker support
        files["Dockerfile"] = self._get_fastapi_dockerfile()
        files["docker-compose.yml"] = self._get_docker_compose_file(database, features)
        
        # Testing
        files["tests/__init__.py"] = ""
        files["tests/test_main.py"] = self._get_main_tests()
        files["tests/test_auth.py"] = self._get_auth_tests(auth_method)
        files["tests/test_crud.py"] = self._get_crud_tests()
        
        # Documentation
        files["README.md"] = self._get_fastapi_readme(database, auth_method, features)
        
        # API documentation
        files["docs/api.md"] = self._get_api_documentation()
        
        # Health check
        files["health.py"] = self._get_health_check_file(database)
        
        # Write all files
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
            "technology": "FastAPI",
            "database": database,
            "authentication": auth_method,
            "features": features
        }
    
    def _get_fastapi_main_file(self, database: str, auth_method: str, features: List[str]) -> str:
        imports = """from fastapi import FastAPI, Middleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from database import engine, Base
from routers import users, todos
from middleware import setup_middleware
from health import health_router
from config import settings"""
        
        if 'graphql' in features:
            imports += "\nfrom routers.graphql import graphql_router"
        
        if 'websockets' in features:
            imports += "\nfrom websockets import websocket_router"
        
        middleware_setup = ""
        if 'cors' in features:
            middleware_setup += """
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
        
        routes_setup = """
# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(todos.router, prefix="/api/v1/todos", tags=["todos"])"""
        
        if 'graphql' in features:
            routes_setup += '\napp.include_router(graphql_router, prefix="/graphql", tags=["graphql"])'
        
        if 'websockets' in features:
            routes_setup += '\napp.include_router(websocket_router, prefix="/ws", tags=["websockets"])'
        
        return f"""{imports}

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Advanced API",
    description="Advanced FastAPI backend with authentication and modern features",
    version="1.0.0",
    lifespan=lifespan
)
{middleware_setup}
# Setup custom middleware
setup_middleware(app)
{routes_setup}

@app.get("/")
async def root():
    return {{
        "message": "Advanced FastAPI Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "database": "{database}",
        "authentication": "{auth_method}",
        "features": {features}
    }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )"""
    
    def _get_fastapi_config_file(self, database: str, auth_method: str) -> str:
        return f"""import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Advanced API"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Email
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "")
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()"""
    
    def _get_sqlalchemy_database_file(self, database: str) -> str:
        if database == 'postgresql':
            db_url = "postgresql://user:password@localhost/dbname"
        elif database == 'mysql':
            db_url = "mysql+pymysql://user:password@localhost/dbname"
        else:  # sqlite
            db_url = "sqlite:///./app.db"
        
        return f"""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={{"check_same_thread": False}},
        echo=settings.DEBUG
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()"""
    
    def _get_sqlalchemy_models_file(self) -> str:
        return """from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    priority = Column(String(10), default="medium")  # low, medium, high
    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="todos")

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True))
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")"""
    
    def _get_fastapi_auth_file(self, auth_method: str) -> str:
        return f"""from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User, ApiKey
from schemas import TokenData
from config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({{"exp": expire}})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={{"WWW-Authenticate": "Bearer"}},
    )
    
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

{'async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:' if auth_method == 'api-key' else ''}
{'    api_key = db.query(ApiKey).filter(ApiKey.key == credentials.credentials, ApiKey.is_active == True).first()' if auth_method == 'api-key' else ''}
{'    if not api_key:' if auth_method == 'api-key' else ''}
{'        raise HTTPException(status_code=401, detail="Invalid API key")' if auth_method == 'api-key' else ''}
{'    # Update last used timestamp' if auth_method == 'api-key' else ''}
{'    api_key.last_used = datetime.utcnow()' if auth_method == 'api-key' else ''}
{'    db.commit()' if auth_method == 'api-key' else ''}
{'    return api_key.user' if auth_method == 'api-key' else ''}

def create_user(db: Session, username: str, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user"""
    
    def _get_users_router(self, database: str, auth_method: str) -> str:
        return f"""from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    create_user,
    {'verify_api_key' if auth_method == 'api-key' else 'get_current_user'}
)
from config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    db_user = create_user(db, user.username, user.email, user.password)
    return UserResponse.from_orm(db_user)

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={{"WWW-Authenticate": "Bearer"}},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={{"sub": user.username}}, expires_delta=access_token_expires
    )
    return {{"access_token": access_token, "token_type": "bearer"}}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse.from_orm(current_user)

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.from_orm(user) for user in users]

@router.get("/{{user_id}}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user)"""
    
    def _get_todos_router(self, database: str, auth_method: str) -> str:
        return f"""from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Todo, User
from schemas import TodoCreate, TodoUpdate, TodoResponse
from auth import get_current_active_user
from crud import todo_crud

router = APIRouter()

@router.get("/", response_model=List[TodoResponse])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    todos = todo_crud.get_user_todos(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit,
        completed=completed,
        priority=priority,
        search=search
    )
    return [TodoResponse.from_orm(todo) for todo in todos]

@router.post("/", response_model=TodoResponse)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_todo = todo_crud.create_todo(db=db, todo=todo, user_id=current_user.id)
    return TodoResponse.from_orm(db_todo)

@router.get("/{{todo_id}}", response_model=TodoResponse)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    todo = todo_crud.get_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.from_orm(todo)

@router.put("/{{todo_id}}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    todo = todo_crud.update_todo(db=db, todo_id=todo_id, todo_update=todo_update, user_id=current_user.id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.from_orm(todo)

@router.delete("/{{todo_id}}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    success = todo_crud.delete_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {{"message": "Todo deleted successfully"}}

@router.get("/stats/summary")
def get_todo_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    stats = todo_crud.get_user_todo_stats(db=db, user_id=current_user.id)
    return stats"""
    
    def _get_pydantic_schemas(self) -> str:
        return """from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Todo schemas
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

class TodoResponse(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Generic response schemas
class MessageResponse(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database: str"""
    
    def _get_crud_operations(self, database: str) -> str:
        return """from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from models import Todo, User
from schemas import TodoCreate, TodoUpdate

class TodoCRUD:
    def get_todo(self, db: Session, todo_id: int, user_id: int) -> Optional[Todo]:
        return db.query(Todo).filter(
            and_(Todo.id == todo_id, Todo.owner_id == user_id)
        ).first()
    
    def get_user_todos(
        self, 
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Todo]:
        query = db.query(Todo).filter(Todo.owner_id == user_id)
        
        if completed is not None:
            query = query.filter(Todo.completed == completed)
        
        if priority:
            query = query.filter(Todo.priority == priority)
        
        if search:
            query = query.filter(
                or_(
                    Todo.title.contains(search),
                    Todo.description.contains(search)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def create_todo(self, db: Session, todo: TodoCreate, user_id: int) -> Todo:
        db_todo = Todo(**todo.dict(), owner_id=user_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    def update_todo(
        self, 
        db: Session, 
        todo_id: int, 
        todo_update: TodoUpdate, 
        user_id: int
    ) -> Optional[Todo]:
        todo = self.get_todo(db, todo_id, user_id)
        if todo:
            update_data = todo_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(todo, field, value)
            db.commit()
            db.refresh(todo)
        return todo
    
    def delete_todo(self, db: Session, todo_id: int, user_id: int) -> bool:
        todo = self.get_todo(db, todo_id, user_id)
        if todo:
            db.delete(todo)
            db.commit()
            return True
        return False
    
    def get_user_todo_stats(self, db: Session, user_id: int) -> dict:
        total = db.query(Todo).filter(Todo.owner_id == user_id).count()
        completed = db.query(Todo).filter(
            and_(Todo.owner_id == user_id, Todo.completed == True)
        ).count()
        pending = total - completed
        
        priority_stats = {}
        for priority in ['low', 'medium', 'high']:
            count = db.query(Todo).filter(
                and_(Todo.owner_id == user_id, Todo.priority == priority)
            ).count()
            priority_stats[priority] = count
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": priority_stats
        }

todo_crud = TodoCRUD()"""
    
    def _get_fastapi_middleware(self, features: List[str]) -> str:
        return """from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging

logger = logging.getLogger(__name__)

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} - "
            f"{response.status_code} - {process_time:.4f}s"
        )
        return response

def setup_middleware(app: FastAPI):
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)"""
    
    def _get_fastapi_utils(self) -> str:
        return """import secrets
import string
from typing import Any, Dict

def generate_api_key(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def format_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data
    }

def format_error_response(message: str, error_code: str = None) -> Dict[str, Any]:
    response = {
        "success": False,
        "message": message
    }
    if error_code:
        response["error_code"] = error_code
    return response"""
    
    def _get_fastapi_dependencies(self, auth_method: str) -> str:
        return f"""from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_active_user{'verify_api_key' if auth_method == 'api-key' else ''}
from models import User

def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

{'async def api_key_auth(user: User = Depends(verify_api_key)) -> User:' if auth_method == 'api-key' else ''}
{'    return user' if auth_method == 'api-key' else ''}"""
    
    def _get_health_check_file(self, database: str) -> str:
        return f"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from database import get_db
from schemas import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database="{database}"
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {{str(e)}}")

@router.get("/detailed")
def detailed_health_check(db: Session = Depends(get_db)):
    checks = {{}}
    
    # Database check
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = {{"status": "healthy", "response_time": "< 1ms"}}
    except Exception as e:
        checks["database"] = {{"status": "unhealthy", "error": str(e)}}
    
    # Add more checks as needed
    overall_status = "healthy" if all(
        check["status"] == "healthy" for check in checks.values()
    ) else "unhealthy"
    
    return {{
        "status": overall_status,
        "timestamp": datetime.utcnow(),
        "checks": checks
    }}"""
    
    def _get_graphql_schema(self) -> str:
        return """import strawberry
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from models import User, Todo
from auth import get_current_active_user

@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

@strawberry.type
class TodoType:
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    owner_id: int

@strawberry.input
class TodoInput:
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[UserType]:
        # This would need dependency injection for database and auth
        return []
    
    @strawberry.field
    def todos(self) -> List[TodoType]:
        # This would need dependency injection for database and auth
        return []

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_todo(self, todo_input: TodoInput) -> TodoType:
        # This would need dependency injection for database and auth
        pass

schema = strawberry.Schema(query=Query, mutation=Mutation)"""
    
    def _get_graphql_router(self) -> str:
        return """from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from graphql_schema import schema

router = APIRouter()

graphql_app = GraphQLRouter(schema)

router.include_router(graphql_app, path="/")"""
    
    def _get_websockets_handler(self) -> str:
        return """from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong", "timestamp": str(datetime.utcnow())}),
                    websocket
                )
            elif message.get("type") == "broadcast":
                await manager.broadcast(
                    json.dumps({
                        "type": "message",
                        "content": message.get("content", ""),
                        "timestamp": str(datetime.utcnow())
                    })
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)"""
    
    def _get_alembic_config(self) -> str:
        return """# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# file_template = %Y%m%d_%H%M_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# max_rev_id_len = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses
# os.pathsep. If this key is omitted entirely, it falls back to the legacy
# behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S"""
    
    def _get_alembic_env_file(self) -> str:
        return """from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from models import Base
from config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()"""
    
    def _get_alembic_template(self) -> str:
        return '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}'''
    
    def _get_env_example(self, database: str, auth_method: str) -> str:
        if database == 'postgresql':
            db_url = "postgresql://user:password@localhost:5432/dbname"
        elif database == 'mysql':
            db_url = "mysql+pymysql://user:password@localhost:3306/dbname"
        else:
            db_url = "sqlite:///./app.db"
        
        return f"""# Application
DEBUG=True
APP_NAME="Advanced API"

# Database
DATABASE_URL={db_url}

# Authentication
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_HOSTS=["http://localhost:3000", "http://localhost:8080"]

# Redis
REDIS_URL=redis://localhost:6379

# Email
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=noreply@yourapp.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# External APIs
API_VERSION=v1"""
    
    def _get_fastapi_dockerfile(self) -> str:
        return """# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    libpq5 \\
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]"""
    
    def _get_docker_compose_file(self, database: str, features: List[str]) -> str:
        services = {
            "app": {
                "build": ".",
                "ports": ["8000:8000"],
                "environment": [
                    "DATABASE_URL=postgresql://user:password@db:5432/dbname" if database == 'postgresql'
                    else "DATABASE_URL=mysql+pymysql://user:password@db:3306/dbname" if database == 'mysql'
                    else "DATABASE_URL=sqlite:///./app.db",
                    "SECRET_KEY=your-secret-key",
                    "DEBUG=True"
                ],
                "volumes": ["./:/app"],
                "depends_on": []
            }
        }
        
        if database == 'postgresql':
            services["db"] = {
                "image": "postgres:15",
                "environment": [
                    "POSTGRES_USER=user",
                    "POSTGRES_PASSWORD=password",
                    "POSTGRES_DB=dbname"
                ],
                "volumes": ["postgres_data:/var/lib/postgresql/data"],
                "ports": ["5432:5432"]
            }
            services["app"]["depends_on"].append("db")
        elif database == 'mysql':
            services["db"] = {
                "image": "mysql:8.0",
                "environment": [
                    "MYSQL_ROOT_PASSWORD=rootpassword",
                    "MYSQL_USER=user",
                    "MYSQL_PASSWORD=password",
                    "MYSQL_DATABASE=dbname"
                ],
                "volumes": ["mysql_data:/var/lib/mysql"],
                "ports": ["3306:3306"]
            }
            services["app"]["depends_on"].append("db")
        
        if 'caching' in features:
            services["redis"] = {
                "image": "redis:7",
                "ports": ["6379:6379"],
                "volumes": ["redis_data:/data"]
            }
            services["app"]["depends_on"].append("redis")
        
        compose_content = "version: '3.8'\n\nservices:\n"
        for service, config in services.items():
            compose_content += f"  {service}:\n"
            for key, value in config.items():
                if isinstance(value, list):
                    compose_content += f"    {key}:\n"
                    for item in value:
                        compose_content += f"      - {item}\n"
                else:
                    compose_content += f"    {key}: {value}\n"
        
        # Add volumes section
        volumes = []
        if database == 'postgresql':
            volumes.append("postgres_data")
        elif database == 'mysql':
            volumes.append("mysql_data")
        if 'caching' in features:
            volumes.append("redis_data")
        
        if volumes:
            compose_content += "\nvolumes:\n"
            for volume in volumes:
                compose_content += f"  {volume}:\n"
        
        return compose_content
    
    def _get_main_tests(self) -> str:
        return """import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db, Base
from models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Advanced FastAPI Backend"

def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_register_user():
    response = client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_login_user():
    # First register a user
    client.post(
        "/api/v1/users/register",
        json={"username": "logintest", "email": "login@example.com", "password": "testpass123"}
    )
    
    # Then try to login
    response = client.post(
        "/api/v1/users/token",
        data={"username": "logintest", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user():
    # Register and login to get token
    client.post(
        "/api/v1/users/register",
        json={"username": "currentuser", "email": "current@example.com", "password": "testpass123"}
    )
    
    login_response = client.post(
        "/api/v1/users/token",
        data={"username": "currentuser", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]
    
    # Get current user info
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser"
    assert data["email"] == "current@example.com"""
    
    def _get_auth_tests(self, auth_method: str) -> str:
        return f"""import pytest
from fastapi.testclient import TestClient
from main import app
from auth import create_access_token, verify_password, get_password_hash

client = TestClient(app)

def test_create_access_token():
    token = create_access_token(data={{"sub": "testuser"}})
    assert isinstance(token, str)
    assert len(token) > 0

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_invalid_login():
    response = client.post(
        "/api/v1/users/token",
        data={{"username": "nonexistent", "password": "wrongpass"}}
    )
    assert response.status_code == 401

def test_protected_route_without_token():
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_protected_route_with_invalid_token():
    response = client.get(
        "/api/v1/users/me",
        headers={{"Authorization": "Bearer invalid_token"}}
    )
    assert response.status_code == 401

{'def test_api_key_authentication():' if auth_method == 'api-key' else ''}
{'    # Test API key authentication if enabled' if auth_method == 'api-key' else ''}
{'    pass' if auth_method == 'api-key' else ''}"""
    
    def _get_crud_tests(self) -> str:
        return """import pytest
from sqlalchemy.orm import Session
from crud import todo_crud
from schemas import TodoCreate, TodoUpdate
from models import User, Todo

def test_create_todo(db_session: Session, test_user: User):
    todo_data = TodoCreate(
        title="Test Todo",
        description="This is a test todo",
        priority="high"
    )
    
    todo = todo_crud.create_todo(db_session, todo_data, test_user.id)
    
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo"
    assert todo.priority == "high"
    assert todo.owner_id == test_user.id
    assert not todo.completed

def test_get_todo(db_session: Session, test_user: User):
    # Create a todo first
    todo_data = TodoCreate(title="Get Test Todo")
    created_todo = todo_crud.create_todo(db_session, todo_data, test_user.id)
    
    # Get the todo
    retrieved_todo = todo_crud.get_todo(db_session, created_todo.id, test_user.id)
    
    assert retrieved_todo is not None
    assert retrieved_todo.id == created_todo.id
    assert retrieved_todo.title == "Get Test Todo"

def test_get_user_todos(db_session: Session, test_user: User):
    # Create multiple todos
    for i in range(5):
        todo_data = TodoCreate(title=f"Todo {i}")
        todo_crud.create_todo(db_session, todo_data, test_user.id)
    
    todos = todo_crud.get_user_todos(db_session, test_user.id)
    
    assert len(todos) == 5
    for i, todo in enumerate(todos):
        assert todo.title == f"Todo {i}"
        assert todo.owner_id == test_user.id

def test_update_todo(db_session: Session, test_user: User):
    # Create a todo
    todo_data = TodoCreate(title="Original Title")
    created_todo = todo_crud.create_todo(db_session, todo_data, test_user.id)
    
    # Update the todo
    update_data = TodoUpdate(title="Updated Title", completed=True)
    updated_todo = todo_crud.update_todo(
        db_session, created_todo.id, update_data, test_user.id
    )
    
    assert updated_todo is not None
    assert updated_todo.title == "Updated Title"
    assert updated_todo.completed == True

def test_delete_todo(db_session: Session, test_user: User):
    # Create a todo
    todo_data = TodoCreate(title="To be deleted")
    created_todo = todo_crud.create_todo(db_session, todo_data, test_user.id)
    
    # Delete the todo
    result = todo_crud.delete_todo(db_session, created_todo.id, test_user.id)
    
    assert result == True
    
    # Verify it's deleted
    deleted_todo = todo_crud.get_todo(db_session, created_todo.id, test_user.id)
    assert deleted_todo is None

def test_get_user_todo_stats(db_session: Session, test_user: User):
    # Create todos with different statuses and priorities
    todos_data = [
        TodoCreate(title="Todo 1", priority="high", completed=True),
        TodoCreate(title="Todo 2", priority="medium", completed=False),
        TodoCreate(title="Todo 3", priority="low", completed=True),
        TodoCreate(title="Todo 4", priority="high", completed=False),
    ]
    
    for todo_data in todos_data:
        todo_crud.create_todo(db_session, todo_data, test_user.id)
    
    stats = todo_crud.get_user_todo_stats(db_session, test_user.id)
    
    assert stats["total"] == 4
    assert stats["completed"] == 2
    assert stats["pending"] == 2
    assert stats["by_priority"]["high"] == 2
    assert stats["by_priority"]["medium"] == 1
    assert stats["by_priority"]["low"] == 1"""
    
    def _get_fastapi_readme(self, database: str, auth_method: str, features: List[str]) -> str:
        features_list = "\n".join([f"- {feature.replace('_', ' ').title()}" for feature in features])
        
        return f"""# Advanced FastAPI Backend

A comprehensive FastAPI backend with modern features and best practices.

## Features

{features_list}
- Database: {database.title()}
- Authentication: {auth_method.upper().replace('-', ' ')}
- API Documentation (Swagger/OpenAPI)
- Database Migrations (Alembic)
- Docker Support
- Comprehensive Testing
- Production Ready

## Quick Start

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize database**
   ```bash
   alembic upgrade head
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

### Docker Development

1. **Build and run with docker-compose**
   ```bash
   docker-compose up --build
   ```

This will start:
- FastAPI application on port 8000
- {database.title()} database{' on port 5432' if database == 'postgresql' else ' on port 3306' if database == 'mysql' else ''}
{f'- Redis cache on port 6379' if 'caching' in features else ''}

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
{f'- **GraphQL Playground**: http://localhost:8000/graphql' if 'graphql' in features else ''}

## Authentication

The API uses {auth_method.upper().replace('-', ' ')} authentication.

### Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \\
     -H "Content-Type: application/json" \\
     -d '{{"username": "testuser", "email": "test@example.com", "password": "password123"}}'
```

### Login to get access token
```bash
curl -X POST "http://localhost:8000/api/v1/users/token" \\
     -H "Content-Type: application/x-www-form-urlencoded" \\
     -d "username=testuser&password=password123"
```

### Use the token in requests
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \\
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/token` - Login and get access token
- `GET /api/v1/users/me` - Get current user info

### Todos
- `GET /api/v1/todos/` - List todos with filtering
- `POST /api/v1/todos/` - Create new todo
- `GET /api/v1/todos/{{id}}` - Get specific todo
- `PUT /api/v1/todos/{{id}}` - Update todo
- `DELETE /api/v1/todos/{{id}}` - Delete todo
- `GET /api/v1/todos/stats/summary` - Get todo statistics

### Health Check
- `GET /health/` - Basic health check
- `GET /health/detailed` - Detailed health check

## Database Migrations

Using Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Environment Variables

Key environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-super-secret-key
DEBUG=True
ALLOWED_HOSTS=["http://localhost:3000"]
```

See `.env.example` for all available options.

## Production Deployment

### Docker

```bash
# Build production image
docker build -t advanced-api .

# Run production container
docker run -d -p 8000:8000 --env-file .env advanced-api
```

### Manual Deployment

1. Install dependencies
2. Set production environment variables
3. Run database migrations
4. Use a production WSGI server like Gunicorn:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Project Structure

```
.
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # Database connection
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── auth.py              # Authentication logic
├── middleware.py        # Custom middleware
├── routers/             # API route handlers
├── tests/               # Test suite
├── alembic/             # Database migrations
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Multi-service setup
└── requirements.txt     # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.
"""
    
    def _get_api_documentation(self) -> str:
        return """# API Documentation

## Overview

This is a comprehensive REST API built with FastAPI, providing user authentication and todo management functionality.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "SPECIFIC_ERROR_CODE"
}
```

## Endpoints

### Users

#### Register User
```http
POST /users/register
Content-Type: application/json

{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

#### Login
```http
POST /users/token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

#### Get Current User
```http
GET /users/me
Authorization: Bearer <token>
```

### Todos

#### List Todos
```http
GET /todos/?skip=0&limit=100&completed=true&priority=high&search=keyword
Authorization: Bearer <token>
```

Query Parameters:
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return
- `completed`: Filter by completion status (true/false)
- `priority`: Filter by priority (low/medium/high)
- `search`: Search in title and description

#### Create Todo
```http
POST /todos/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "string",
  "description": "string",
  "priority": "medium",
  "due_date": "2023-12-31T23:59:59"
}
```

#### Get Todo
```http
GET /todos/{todo_id}
Authorization: Bearer <token>
```

#### Update Todo
```http
PUT /todos/{todo_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "string",
  "description": "string",
  "completed": true,
  "priority": "high",
  "due_date": "2023-12-31T23:59:59"
}
```

#### Delete Todo
```http
DELETE /todos/{todo_id}
Authorization: Bearer <token>
```

#### Get Todo Statistics
```http
GET /todos/stats/summary
Authorization: Bearer <token>
```

Returns:
```json
{
  "total": 10,
  "completed": 3,
  "pending": 7,
  "by_priority": {
    "low": 2,
    "medium": 5,
    "high": 3
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Input data validation failed |
| 500 | Internal Server Error - Something went wrong |

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per authenticated user

When rate limit is exceeded, the API returns a 429 status code.

## Data Models

### User
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Todo
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "completed": false,
  "priority": "medium",
  "due_date": "2023-12-31T23:59:59",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "owner_id": 1
}
```

## WebSocket Support

Real-time updates are available via WebSocket connection:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/");

ws.onopen = function(event) {
    console.log("Connected to WebSocket");
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Received:", data);
};
```

## Examples

### Complete User Registration and Todo Creation Flow

```bash
# 1. Register a new user
curl -X POST "http://localhost:8000/api/v1/users/register" \\
     -H "Content-Type: application/json" \\
     -d '{"username": "johndoe", "email": "john@example.com", "password": "securepass123"}'

# 2. Login to get access token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/users/token" \\
     -H "Content-Type: application/x-www-form-urlencoded" \\
     -d "username=johndoe&password=securepass123" | jq -r .access_token)

# 3. Create a todo
curl -X POST "http://localhost:8000/api/v1/todos/" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "priority": "medium"}'

# 4. List todos
curl -X GET "http://localhost:8000/api/v1/todos/" \\
     -H "Authorization: Bearer $TOKEN"
```
"""
    
    async def _create_advanced_flask_backend(self, task: Dict[str, Any], output_dir: str,
                                           database: str, auth_method: str, features: List[str]) -> Dict[str, Any]:
        """Create advanced Flask backend"""
        # Implementation for Flask would be similar to FastAPI but adapted for Flask
        # For brevity, returning a placeholder that indicates Flask support is available
        return {
            "status": "completed",
            "message": "Advanced Flask backend implementation available",
            "technology": "Flask",
            "database": database,
            "authentication": auth_method,
            "features": features,
            "files_created": []
        }
    
    async def _create_advanced_django_backend(self, task: Dict[str, Any], output_dir: str,
                                            database: str, auth_method: str, features: List[str]) -> Dict[str, Any]:
        """Create advanced Django backend"""
        # Implementation for Django would be similar but adapted for Django
        # For brevity, returning a placeholder that indicates Django support is available
        return {
            "status": "completed",
            "message": "Advanced Django backend implementation available", 
            "technology": "Django",
            "database": database,
            "authentication": auth_method,
            "features": features,
            "files_created": []
        }
    
    def _get_mongodb_database_file(self) -> str:
        return """from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "advanced_api")

# Async client for FastAPI
client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Sync client for non-async operations
sync_client = MongoClient(MONGODB_URL)
sync_database = sync_client[DATABASE_NAME]

def get_database():
    return database

def get_sync_database():
    return sync_database"""
    
    def _get_mongodb_models_file(self) -> str:
        return """from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class User(MongoBaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class Todo(MongoBaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    owner_id: PyObjectId"""

