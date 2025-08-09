
# Database Agent

The Database Agent is a comprehensive database management component that handles schema generation, optimization, migrations, and performance analysis for NEXUS projects.

## Overview

The Database Agent provides:

- **Intelligent Schema Generation**: AI-powered database schema creation from requirements
- **Migration Management**: Automated migration script generation and execution
- **Performance Optimization**: Database tuning and optimization recommendations
- **Multi-Database Support**: SQLite, PostgreSQL, MySQL, MongoDB, and Redis support

## Key Features

### 1. Schema Generation

#### Template-Based Schemas
Pre-built schema templates for common application patterns:

- **User Management**: Complete user authentication and profile system
- **Todo Application**: Task management with categories and priorities
- **Blog System**: Content management with posts, comments, and categories
- **E-commerce**: Product catalog, orders, and customer management

#### AI-Enhanced Design
- LLM-powered schema analysis and optimization
- Automatic relationship inference and constraint generation
- Best practices implementation and normalization

### 2. Database Types Supported

```python
class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql" 
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"
```

### 3. Optimization Features

#### Performance Rules
- Missing index detection on foreign keys
- Primary key validation
- Query optimization recommendations
- Table partitioning strategies

#### Security Enhancements
- Data validation constraints
- Audit field implementation
- Access control recommendations
- Encryption guidance

## Architecture

### Core Components

```python
class DatabaseAgent(BaseAgent):
    def __init__(self, config):
        self.supported_databases = [...]
        self.schema_templates = self._initialize_schema_templates()
        self.optimization_rules = self._initialize_optimization_rules()
```

### Schema Templates Structure

```python
"user_management": {
    "tables": {
        "users": {
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "username", "type": "VARCHAR(50)", "unique": True},
                {"name": "email", "type": "VARCHAR(255)", "unique": True},
                # ... more columns
            ],
            "indexes": [
                {"name": "idx_users_email", "columns": ["email"], "type": "unique"}
            ]
        }
    }
}
```

### Optimization Rules

1. **Foreign Key Index Rule**
   - Detects foreign keys without corresponding indexes
   - Recommends index creation for join performance

2. **Primary Key Validation**
   - Ensures all tables have primary keys
   - Suggests surrogate keys when needed

3. **Large Table Partitioning**
   - Identifies tables that could benefit from partitioning
   - Provides partitioning strategy recommendations

4. **Unused Index Detection**
   - Analyzes index usage patterns
   - Recommends removal of unused indexes

## Usage Examples

### Basic Schema Generation

```python
database_agent = DatabaseAgent(config)

requirements = {
    "project_type": "todo_application",
    "database_type": "postgresql",
    "description": "Task management system",
    "entities": ["todos", "users", "categories"],
    "expected_data_volume": "medium"
}

schema_result = await database_agent.generate_schema(requirements)
```

### Custom Schema with AI

```python
requirements = {
    "project_type": "custom_app",
    "database_type": "mysql",
    "description": "Inventory management system",
    "entities": ["products", "suppliers", "orders", "customers"],
    "relationships": [
        {"from": "orders", "to": "customers", "type": "many_to_one"},
        {"from": "orders", "to": "products", "type": "many_to_many"}
    ]
}

schema_result = await database_agent.generate_schema(requirements)
```

### Performance Analysis

```python
database_config = {
    "type": "postgresql",
    "schema": existing_schema
}

analysis = await database_agent.analyze_performance(database_config)

print(f"Optimization score: {analysis['optimization_score']}")
for finding in analysis['findings']:
    print(f"Issue: {finding['description']}")
    print(f"Recommendation: {finding['recommendation']}")
```

## Generated Files

The Database Agent generates several files for each project:

### 1. database.py
Database connection and query execution utilities:

```python
# SQLite version
class Database:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self.init_db()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        # Query execution implementation
        pass
```

### 2. models.py
SQLAlchemy ORM models:

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3. init_db.sql
Migration scripts for database initialization:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users (email);
```

## Schema Templates

### User Management Template

Complete user authentication system with:
- User accounts with secure authentication
- User profiles with extended information
- Role-based access control
- Audit trails and session management

### Todo Application Template

Task management system featuring:
- Todo items with priorities and due dates
- Categories and tags for organization
- User ownership and sharing capabilities
- Progress tracking and completion status

### Blog System Template

Content management system with:
- Posts with rich content and metadata
- Comment system with moderation
- Category and tag management
- Author management and permissions

## Optimization Features

### Index Recommendations

```python
recommendations = [
    {
        "table": "posts",
        "index_name": "idx_posts_published_at",
        "columns": ["published_at"],
        "type": "btree",
        "reason": "Date/timestamp column for range queries"
    }
]
```

### Constraint Generation

```python
constraints = [
    {
        "table": "users",
        "type": "check",
        "name": "chk_users_email_format", 
        "definition": "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
        "reason": "Validate email format"
    }
]
```

### Performance Scoring

The optimization score (0-100) considers:
- Presence of primary keys
- Foreign key indexing
- Audit field implementation
- Constraint coverage
- Normalization level

## Integration with Other Agents

### Orchestrator Integration
The Database Agent integrates seamlessly with the Enhanced Orchestrator:

```python
# Task processing
task = {
    "title": "Setup Database Schema",
    "description": "Create database for todo application",
    "requirements": {"database": "postgresql"}
}

result = await database_agent.process_task(task)
```

### Analyst Agent Collaboration
Works with the Analyst Agent to:
- Extract entities from requirements analysis
- Validate data modeling decisions
- Ensure compliance with business rules
- Optimize for identified usage patterns

## Configuration

### Basic Configuration

```yaml
agents:
  database:
    model: "qwen2.5-coder:7b"
    default_database: "postgresql"
    optimization_enabled: true
    migration_strategy: "incremental"
```

### Advanced Configuration

```yaml
database:
  templates:
    enable_custom_templates: true
    template_directory: "/custom/templates"
  
  optimization:
    index_threshold: 1000  # rows
    performance_monitoring: true
    auto_optimization: false
  
  migration:
    backup_before_migration: true
    rollback_on_error: true
    migration_history: true
```

## Error Handling

### Schema Validation
- Validates generated schemas against database constraints
- Checks for circular dependencies
- Ensures referential integrity

### Migration Safety
- Dry-run capabilities for testing migrations
- Automatic backup creation before schema changes
- Rollback procedures for failed migrations

## Performance Considerations

### Large Scale Optimization
- Table partitioning strategies for large datasets
- Index optimization for query performance
- Connection pooling and resource management
- Caching strategies and implementation

### Monitoring Integration
- Performance metrics collection
- Query performance analysis
- Resource utilization tracking
- Automated alerting for performance issues

## Future Enhancements

### Planned Features
- Real-time schema evolution and migration
- Advanced query optimization with machine learning
- Multi-database federation and synchronization
- Automated performance tuning and optimization

### Extensibility
- Custom optimization rule plugins
- Template marketplace for specialized schemas
- Integration with database monitoring tools
- Support for NoSQL and graph databases

