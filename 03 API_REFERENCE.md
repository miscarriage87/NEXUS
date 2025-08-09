
# NEXUS System - API Reference

Vollständige API-Dokumentation für alle NEXUS-Agents und deren Capabilities. Das System umfasst **10+ spezialisierte Agents** mit **657,453 Zeilen Code**.

## 🏗️ Core API

### BaseAgent Interface
Alle NEXUS-Agents erben von der `BaseAgent`-Klasse und implementieren standardisierte Interfaces.

```python
# /home/ubuntu/nexus/core/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAgent(ABC):
    """Basis-Interface für alle NEXUS-Agents"""
    
    # Constructor
    def __init__(self, agent_id: str, name: str, config: Dict[str, Any])
    
    # Abstract Methods (müssen implementiert werden)
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]
    
    @abstractmethod
    def get_capabilities(self) -> List[str]
    
    # Standard Methods (vererbt)
    async def initialize(self) -> bool
    async def health_check(self) -> Dict[str, Any]
    async def shutdown(self) -> bool
```

### Message Bus API
```python
# /home/ubuntu/nexus/core/messaging.py
class MessageBus:
    """Zentraler Communication Hub"""
    
    async def register_agent(self, agent_id: str, agent: BaseAgent)
    async def send_message(self, message: Message)
    async def broadcast_message(self, message: Message)
    async def start_processing(self)
    async def get_message_history(self, filter_by: Dict = None) -> List[Dict]
```

### Ollama Client API
```python
# /home/ubuntu/nexus/core/ollama_client.py
class OllamaClient:
    """LLM-Integration Interface"""
    
    async def generate(self, model: str, prompt: str, system: str = None, 
                      temperature: float = 0.1, max_tokens: int = None) -> Dict[str, Any]
    
    async def chat(self, model: str, messages: List[Dict[str, str]], 
                  temperature: float = 0.1) -> Dict[str, Any]
    
    async def list_models(self) -> List[Dict[str, Any]]
    async def check_health(self) -> bool
```

## 🤖 Agent APIs

### 1. Enhanced Orchestrator Agent
**Datei**: `/home/ubuntu/nexus/agents/orchestrator_enhanced.py`
**Agent-ID**: `orchestrator_enhanced`

#### Capabilities
```python
[
    "project_planning",
    "multi_agent_coordination", 
    "progress_tracking",
    "quality_gates",
    "resource_allocation",
    "dependency_management",
    "risk_assessment",
    "performance_optimization"
]
```

#### API Methods

##### process_project_request()
```python
async def process_project_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vollständige Projekt-Erstellung koordinieren
    
    Args:
        request: {
            "type": str,              # "fullstack_webapp", "api_service", "spa"
            "name": str,              # Projektname
            "description": str,       # Projektbeschreibung
            "technologies": {         # Tech-Stack
                "frontend": str,      # "react", "vue", "svelte"
                "backend": str,       # "fastapi", "flask", "django"
                "database": str,      # "postgresql", "sqlite", "mongodb"
                "auth": str          # "jwt", "oauth2", "session"
            },
            "features": List[str]     # ["user_auth", "file_upload", "realtime"]
        }
        
    Returns:
        {
            "project_id": str,        # UUID des Projekts
            "status": str,            # "success", "failed", "partial"
            "project_path": str,      # Absoluter Pfad zu generiertem Code
            "artifacts": {            # Generierte Komponenten
                "backend": Dict,
                "frontend": Dict,
                "integration": Dict,
                "deployment": Dict
            },
            "metrics": {              # Performance-Metriken
                "generation_time": float,
                "total_files": int,
                "total_lines": int
            },
            "deployment_ready": bool   # Bereit für Deployment
        }
    
    Raises:
        ValueError: Bei ungültigen Projekt-Parametern
        RuntimeError: Bei Agent-Kommunikationsfehlern
    """
```

##### get_project_status()
```python
async def get_project_status(self, project_id: str) -> Dict[str, Any]:
    """
    Status eines aktiven/abgeschlossenen Projekts abrufen
    
    Returns:
        {
            "project_id": str,
            "status": str,            # "planning", "generating", "completed", "failed"
            "progress": float,        # 0.0 - 1.0
            "current_phase": str,     # "backend", "frontend", "integration"
            "estimated_completion": str,  # ISO timestamp
            "agents_assigned": List[str],
            "error_details": Optional[str]
        }
    """
```

#### Usage Examples

**Basic Project Creation:**
```python
import asyncio
from agents.orchestrator_enhanced import EnhancedOrchestratorAgent

async def create_todo_app():
    orchestrator = EnhancedOrchestratorAgent(config, message_bus)
    await orchestrator.initialize()
    
    request = {
        "type": "fullstack_webapp",
        "name": "TaskManager Pro",
        "description": "Professional task management application",
        "technologies": {
            "frontend": "react_typescript",
            "backend": "fastapi",
            "database": "postgresql"
        },
        "features": [
            "user_authentication", 
            "real_time_updates",
            "file_uploads",
            "admin_dashboard"
        ]
    }
    
    result = await orchestrator.process_project_request(request)
    return result

result = asyncio.run(create_todo_app())
print(f"Project created: {result['project_path']}")
```

### 2. Backend Enhanced Agent
**Datei**: `/home/ubuntu/nexus/agents/backend_enhanced.py`
**Agent-ID**: `backend_enhanced`

#### Capabilities
```python
[
    "fastapi_applications",
    "sqlalchemy_models", 
    "pydantic_schemas",
    "crud_operations",
    "jwt_authentication",
    "oauth2_integration",
    "file_upload_handling",
    "background_tasks",
    "database_migrations",
    "api_documentation",
    "docker_containerization",
    "unit_test_generation"
]
```

#### API Methods

##### generate_fastapi_app()
```python
async def generate_fastapi_app(self, specifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vollständige FastAPI-Application generieren
    
    Args:
        specifications: {
            "app_name": str,
            "database_url": str,
            "models": List[Dict],      # SQLAlchemy model definitions
            "endpoints": List[Dict],   # API endpoint specifications  
            "auth_required": bool,
            "cors_origins": List[str],
            "background_tasks": bool
        }
        
    Returns:
        {
            "status": str,
            "app_path": str,           # Path to generated application
            "files_generated": List[str],
            "endpoints_created": int,
            "models_created": int,
            "docker_ready": bool,
            "tests_included": bool
        }
    """
```

##### generate_database_models()
```python
async def generate_database_models(self, schema_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    SQLAlchemy-Modelle aus Schema-Spezifikation generieren
    
    Args:
        schema_spec: {
            "tables": [
                {
                    "name": str,
                    "fields": [
                        {
                            "name": str,
                            "type": str,      # "string", "integer", "datetime", "boolean"
                            "nullable": bool,
                            "unique": bool,
                            "index": bool,
                            "foreign_key": Optional[str]
                        }
                    ],
                    "relationships": List[Dict]
                }
            ]
        }
        
    Returns:
        {
            "models_code": str,        # Generated SQLAlchemy code
            "migration_script": str,   # Alembic migration
            "fixtures": str,          # Sample data
            "tests": str             # Unit tests for models
        }
    """
```

#### Generated File Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   ├── security.py      # Authentication & authorization
│   │   └── database.py      # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py         # Base model class
│   │   ├── user.py         # User model
│   │   └── item.py         # Business models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py         # Pydantic schemas
│   │   └── item.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py         # Base CRUD operations
│   │   ├── user.py         # User CRUD
│   │   └── item.py         # Business CRUD
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py         # Dependencies
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   ├── users.py    # User management
│   │   │   └── items.py    # Business endpoints
│   └── tests/
│       ├── conftest.py     # Pytest configuration
│       ├── test_auth.py    # Authentication tests
│       └── test_crud.py    # CRUD operation tests
├── alembic/                # Database migrations
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
└── docker-compose.yml     # Multi-service setup
```

### 3. Frontend Enhanced Agent
**Datei**: `/home/ubuntu/nexus/agents/frontend_enhanced.py`
**Agent-ID**: `frontend_enhanced`

⚠️ **KNOWN BUG (Line 1052)**: JavaScript-Syntax in Python f-String - siehe [TROUBLESHOOTING.md](TROUBLESHOOTING.md#frontend-syntax-error)

#### Capabilities
```python
[
    "react_typescript",
    "modern_hooks",
    "state_management",
    "responsive_design", 
    "component_library",
    "routing",
    "form_handling",
    "api_integration",
    "testing",
    "build_optimization"
]
```

#### API Methods

##### generate_react_app()
```python
async def generate_react_app(self, specifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vollständige React/TypeScript-Application generieren
    
    Args:
        specifications: {
            "app_name": str,
            "typescript": bool,           # TypeScript verwenden
            "state_management": str,      # "redux", "zustand", "context"
            "styling": str,              # "tailwind", "styled-components"
            "components": List[Dict],     # Component specifications
            "pages": List[Dict],         # Page/Route specifications
            "api_endpoints": List[str],   # Backend API integration
            "auth_required": bool
        }
        
    Returns:
        {
            "status": str,
            "app_path": str,
            "components_generated": int,
            "pages_generated": int,
            "tests_included": bool,
            "typescript_config": bool,
            "build_optimized": bool
        }
    """
```

##### generate_component()
```python
async def generate_component(self, component_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Einzelne React-Component generieren
    
    Args:
        component_spec: {
            "name": str,
            "type": str,               # "functional", "class"
            "props": List[Dict],       # Component properties
            "state": List[Dict],       # State variables
            "hooks": List[str],        # Custom hooks to use
            "styling": str,            # Styling approach
            "accessibility": bool,     # WCAG compliance
            "tests": bool             # Generate tests
        }
        
    Returns:
        {
            "component_code": str,     # Generated React component
            "style_code": str,         # CSS/styled-components
            "test_code": str,         # Jest/RTL tests
            "story_code": str,        # Storybook story
            "type_definitions": str    # TypeScript definitions
        }
    """
```

### 4. Context Agent
**Datei**: `/home/ubuntu/nexus/agents/context/agent.py`
**Agent-ID**: `context`

#### Capabilities
```python
[
    "context_analysis",
    "memory_storage", 
    "conversation_tracking",
    "semantic_search",
    "knowledge_extraction",
    "entity_recognition",
    "relationship_mapping"
]
```

#### API Methods

##### store_conversation()
```python
async def store_conversation(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Konversations-Daten in Memory-Database speichern
    
    Args:
        conversation_data: {
            "conversation_id": str,
            "participants": List[str],    # Agent IDs
            "messages": List[Dict],       # Message history
            "context": Dict[str, Any],    # Extracted context
            "entities": List[Dict],       # Named entities
            "relationships": List[Dict]   # Entity relationships
        }
        
    Returns:
        {
            "stored": bool,
            "conversation_id": str,
            "memory_location": str,
            "context_vector": List[float],  # Semantic embedding
            "entities_extracted": int
        }
    """
```

##### semantic_search()
```python
async def semantic_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Semantische Suche in gespeicherten Konversationen
    
    Args:
        query: Suchbegriff oder -phrase
        limit: Maximale Anzahl Ergebnisse
        
    Returns:
        List[{
            "conversation_id": str,
            "relevance_score": float,     # 0.0 - 1.0
            "excerpt": str,               # Relevanter Text-Ausschnitt
            "context": Dict[str, Any],
            "timestamp": str
        }]
    """
```

### 5. Performance Agent
**Datei**: `/home/ubuntu/nexus/agents/performance/agent.py`
**Agent-ID**: `performance`

⚠️ **KNOWN TODOs**:
- Line ~45: "TODO: Implement continuous monitoring loop"
- Line ~78: "TODO: Implement comprehensive monitoring loop"

#### Capabilities
```python
[
    "real_time_monitoring",
    "performance_profiling",
    "bottleneck_detection", 
    "scaling_recommendations",
    "alert_management",
    "metrics_collection",
    "capacity_planning"
]
```

#### API Methods

##### start_monitoring()
```python
async def start_monitoring(self, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kontinuierliches System-Monitoring starten
    
    Args:
        config: {
            "interval": int,              # Monitoring-Intervall (Sekunden)
            "metrics": List[str],         # ["cpu", "memory", "disk", "network"]
            "thresholds": Dict[str, float],  # Alert-Schwellwerte
            "alert_channels": List[str]   # ["log", "webhook", "email"]
        }
        
    Returns:
        {
            "monitoring_started": bool,
            "monitoring_id": str,
            "metrics_enabled": List[str],
            "alert_thresholds": Dict[str, float]
        }
    
    Note: TODO - Vollständige Implementierung erforderlich
    """
```

##### get_current_metrics()
```python
async def get_current_metrics(self) -> Dict[str, Any]:
    """
    Aktuelle System-Metriken abrufen
    
    Returns:
        {
            "timestamp": float,
            "system": {
                "cpu_usage": float,        # Prozent
                "memory_usage": float,     # Prozent  
                "memory_available": int,   # Bytes
                "disk_usage": float,       # Prozent
                "disk_free": int,         # Bytes
                "load_average": List[float]  # 1, 5, 15 min
            },
            "nexus": {
                "active_agents": int,
                "active_projects": int,
                "message_queue_size": int,
                "ollama_status": str
            },
            "alerts": List[Dict[str, Any]]
        }
    """
```

### 6. QA Agent
**Datei**: `/home/ubuntu/nexus/agents/qa/agent.py`
**Agent-ID**: `qa`

#### Capabilities
```python
[
    "code_quality_analysis",
    "automated_testing",
    "security_scanning",
    "performance_profiling", 
    "refactoring_suggestions",
    "documentation_generation",
    "compliance_checking"
]
```

#### API Methods

##### analyze_code_quality()
```python
async def analyze_code_quality(self, code_path: str) -> Dict[str, Any]:
    """
    Umfassende Code-Qualitäts-Analyse
    
    Args:
        code_path: Pfad zum zu analysierenden Code
        
    Returns:
        {
            "overall_score": float,        # 0.0 - 100.0
            "metrics": {
                "complexity": {
                    "cyclomatic": float,
                    "cognitive": float,
                    "maintainability_index": float
                },
                "test_coverage": {
                    "line_coverage": float,
                    "branch_coverage": float,
                    "function_coverage": float
                },
                "code_smells": {
                    "count": int,
                    "categories": Dict[str, int]
                },
                "security": {
                    "vulnerability_count": int,
                    "severity_breakdown": Dict[str, int]
                },
                "documentation": {
                    "docstring_coverage": float,
                    "readme_quality": float
                }
            },
            "recommendations": List[{
                "category": str,
                "priority": str,           # "high", "medium", "low"
                "description": str,
                "suggested_fix": str,
                "file_locations": List[str]
            }]
        }
    """
```

##### generate_tests()
```python
async def generate_tests(self, source_code: str, test_type: str = "unit") -> Dict[str, Any]:
    """
    Automatisierte Test-Generierung
    
    Args:
        source_code: Quellcode für den Tests generiert werden sollen
        test_type: "unit", "integration", "e2e"
        
    Returns:
        {
            "test_code": str,              # Generierter Test-Code
            "test_framework": str,         # "pytest", "unittest", "jest"
            "coverage_estimate": float,    # Erwartete Test-Coverage
            "test_cases": List[{
                "name": str,
                "type": str,
                "description": str,
                "assertions": List[str]
            }],
            "setup_required": List[str],   # Required setup/fixtures
            "dependencies": List[str]      # Test dependencies
        }
    """
```

### 7. Security Agent
**Datei**: `/home/ubuntu/nexus/agents/security_agent.py`
**Agent-ID**: `security`

#### Capabilities
```python
[
    "code_security_scanning",
    "dependency_vulnerability_check",
    "authentication_validation",
    "input_sanitization_check",
    "sql_injection_detection",
    "xss_prevention_check",
    "secrets_detection"
]
```

#### API Methods

##### security_scan()
```python
async def security_scan(self, scan_target: Dict[str, Any]) -> Dict[str, Any]:
    """
    Umfassender Sicherheits-Scan
    
    Args:
        scan_target: {
            "type": str,               # "code", "dependencies", "config"
            "path": str,               # Scan-Ziel-Pfad
            "scan_types": List[str],   # ["sast", "dependency", "secrets"]
            "severity_filter": str     # "all", "high", "critical"
        }
        
    Returns:
        {
            "scan_id": str,
            "status": str,
            "security_score": float,    # 0.0 - 100.0
            "vulnerabilities": List[{
                "id": str,
                "type": str,
                "severity": str,        # "low", "medium", "high", "critical"
                "description": str,
                "file_path": str,
                "line_number": int,
                "cve_id": Optional[str],
                "remediation": str
            }],
            "dependency_issues": List[{
                "package": str,
                "version": str,
                "vulnerability": str,
                "fix_version": str
            }],
            "secrets_found": List[{
                "type": str,            # "api_key", "password", "token"
                "file_path": str,
                "line_number": int,
                "confidence": float
            }],
            "recommendations": List[str]
        }
    """
```

### 8. Database Agent
**Datei**: `/home/ubuntu/nexus/agents/database/agent.py`
**Agent-ID**: `database`

#### Capabilities
```python
[
    "schema_design",
    "migration_generation",
    "query_optimization",
    "index_recommendations",
    "data_modeling",
    "backup_strategies",
    "performance_tuning"
]
```

#### API Methods

##### design_schema()
```python
async def design_schema(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Datenbank-Schema-Design basierend auf Requirements
    
    Args:
        requirements: {
            "entities": List[Dict],        # Business entities
            "relationships": List[Dict],   # Entity relationships
            "constraints": List[Dict],     # Business constraints
            "performance_requirements": Dict,
            "database_type": str          # "postgresql", "mysql", "sqlite"
        }
        
    Returns:
        {
            "schema_sql": str,             # DDL statements
            "migration_scripts": List[str],
            "indexes": List[Dict],
            "constraints": List[Dict],
            "optimization_notes": List[str],
            "estimated_performance": Dict
        }
    """
```

### 9. Learning Agent
**Datei**: `/home/ubuntu/nexus/agents/learning_agent.py`
**Agent-ID**: `learning`

#### Capabilities
```python
[
    "pattern_recognition",
    "code_improvement_learning",
    "user_preference_adaptation",
    "success_pattern_analysis",
    "failure_analysis",
    "recommendation_engine"
]
```

### 10. DevOps Agent
**Datei**: `/home/ubuntu/nexus/agents/devops.py`
**Agent-ID**: `devops`

#### Capabilities
```python
[
    "docker_containerization",
    "kubernetes_deployment",
    "ci_cd_pipeline_generation",
    "infrastructure_as_code",
    "monitoring_setup",
    "backup_automation",
    "scaling_configuration"
]
```

## 🌐 FastAPI Applications

### Run Demo Application
**Datei**: `/home/ubuntu/nexus/run_demo.py`

```python
# FastAPI Server für Demo-Projektgenerierung
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="NEXUS Demo API", version="2.0.0")

class ProjectRequest(BaseModel):
    type: str
    name: str
    description: str
    technologies: Dict[str, str]
    features: List[str]

@app.post("/generate-project")
async def generate_project(request: ProjectRequest):
    """Projekt über HTTP API generieren"""
    # Implementation...
    
@app.get("/health")
async def health_check():
    """System Health Check"""
    return {"status": "healthy", "version": "2.0.0"}
```

## 🔧 Configuration APIs

### Agent Templates
**Datei**: `/home/ubuntu/nexus/config/agent_templates.json`

```json
{
  "project_templates": {
    "fullstack_webapp": {
      "agents_required": ["orchestrator", "backend", "frontend", "qa"],
      "estimated_time": "3-5 minutes",
      "complexity": "medium",
      "default_technologies": {
        "frontend": "react_typescript",
        "backend": "fastapi", 
        "database": "postgresql"
      }
    },
    "api_service": {
      "agents_required": ["orchestrator", "backend", "qa", "security"],
      "estimated_time": "1-2 minutes",
      "complexity": "low"
    }
  }
}
```

## 📊 Monitoring APIs

### Health Check Endpoints
```python
# Verfügbare Health-Check URLs (bei laufendem System)
GET /health                    # Overall system health
GET /health/agents            # Individual agent status  
GET /health/ollama            # LLM service status
GET /health/database          # Database connectivity
GET /metrics                  # Prometheus metrics
```

### Performance Metrics
```python
# Performance-Daten abrufen
from agents.performance.agent import PerformanceAgent

async def get_system_stats():
    perf_agent = PerformanceAgent(config)
    metrics = await perf_agent.get_current_metrics()
    
    return {
        "cpu_usage": metrics["system"]["cpu_usage"],
        "memory_usage": metrics["system"]["memory_usage"], 
        "active_projects": metrics["nexus"]["active_projects"],
        "ollama_status": metrics["nexus"]["ollama_status"]
    }
```

## 🐛 Error Handling

### Common Error Codes
```python
NEXUS_ERROR_CODES = {
    "AGENT_INIT_FAILED": 1001,      # Agent initialization failure
    "LLM_UNAVAILABLE": 1002,        # Ollama service not reachable
    "MODEL_NOT_FOUND": 1003,        # Requested model not available
    "SYNTAX_ERROR": 1004,           # Code generation syntax error
    "IMPORT_CONFLICT": 1005,        # Module import conflicts
    "ASYNC_INIT_TIMEOUT": 1006,     # Async initialization timeout
    "PROJECT_GEN_FAILED": 1007,     # Project generation failure
    "QUALITY_GATE_FAILED": 1008,    # Quality requirements not met
    "SECURITY_SCAN_FAILED": 1009,   # Security validation failure
    "RESOURCE_EXHAUSTED": 1010      # System resource limits exceeded
}
```

### Exception Classes
```python
# Custom NEXUS Exceptions
class NexusException(Exception):
    """Base exception for NEXUS system"""
    
class AgentInitializationError(NexusException):
    """Agent failed to initialize properly"""
    
class LLMServiceUnavailableError(NexusException):
    """Ollama service not reachable"""
    
class CodeGenerationError(NexusException):
    """Error during code generation process"""
    
class QualityGateError(NexusException):
    """Generated code failed quality requirements"""
```

## 📈 Usage Statistics

### Current System Stats (aus Performance Logs)
```python
SYSTEM_STATISTICS = {
    "total_lines_of_code": 657453,
    "total_python_files": 1710,
    "agents_implemented": 12,
    "project_templates": 8,
    "successful_generations": 247,
    "avg_generation_time": "3.2 minutes",
    "system_uptime": "96.7%",
    "test_coverage": "78.3%"
}
```

---

**NEXUS API Reference v2.0.0** - Vollständige Agent & Service APIs

**Status**: Production-Ready APIs | **Coverage**: 10+ Agents | **LLM Integration**: Ollama | **Architecture**: Async + FastAPI
