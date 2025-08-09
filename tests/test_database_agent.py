
"""
Tests for Database Agent
"""
import pytest
import asyncio
import json
import os
import tempfile
from unittest.mock import Mock, AsyncMock, patch
from agents.database.agent import DatabaseAgent, DatabaseType, IndexType

class TestDatabaseAgent:
    @pytest.fixture
    def config(self):
        return {
            'agents': {
                'database': {
                    'model': 'test-model'
                }
            }
        }
    
    @pytest.fixture
    def database_agent(self, config):
        return DatabaseAgent(config)
    
    def test_initialization(self, database_agent):
        """Test database agent initialization"""
        assert database_agent.agent_id == "database"
        assert database_agent.name == "Database Management Agent"
        assert len(database_agent.supported_databases) > 0
        assert "schema_generation" in database_agent.get_capabilities()
    
    def test_capabilities(self, database_agent):
        """Test database agent capabilities"""
        capabilities = database_agent.get_capabilities()
        expected_capabilities = [
            "schema_generation",
            "database_design",
            "migration_management",
            "query_optimization",
            "performance_analysis",
            "data_modeling"
        ]
        
        for capability in expected_capabilities:
            assert capability in capabilities
    
    def test_schema_templates(self, database_agent):
        """Test schema templates initialization"""
        templates = database_agent.schema_templates
        
        assert "user_management" in templates
        assert "todo_application" in templates
        assert "blog_system" in templates
        
        # Test user_management template structure
        user_mgmt = templates["user_management"]
        assert "tables" in user_mgmt
        assert "users" in user_mgmt["tables"]
        
        users_table = user_mgmt["tables"]["users"]
        assert "columns" in users_table
        assert "indexes" in users_table
    
    def test_optimization_rules(self, database_agent):
        """Test optimization rules initialization"""
        rules = database_agent.optimization_rules
        
        assert len(rules) > 0
        
        # Check rule structure
        for rule in rules:
            assert "name" in rule
            assert "description" in rule
            assert "severity" in rule
            assert "check" in rule
            assert "recommendation" in rule
    
    @pytest.mark.asyncio
    async def test_generate_schema_with_template(self, database_agent):
        """Test schema generation using templates"""
        requirements = {
            "project_type": "todo_application",
            "database_type": "postgresql",
            "description": "Simple todo app",
            "entities": ["todos", "users"],
            "relationships": []
        }
        
        result = await database_agent.generate_schema(requirements)
        
        assert "schema" in result
        assert "migration_scripts" in result
        assert "indexes" in result
        assert result["database_type"] == "postgresql"
        
        # Check schema structure
        schema = result["schema"]
        assert "tables" in schema
        
        # Should include template tables
        tables = schema["tables"]
        assert any("todo" in table_name.lower() for table_name in tables.keys())
    
    @pytest.mark.asyncio
    async def test_generate_schema_with_ai(self, database_agent):
        """Test schema generation with AI fallback"""
        requirements = {
            "project_type": "custom_app",  # Not in templates
            "database_type": "mysql",
            "description": "Custom application",
            "entities": ["products", "orders"],
            "relationships": [{"from": "orders", "to": "products", "type": "many_to_one"}]
        }
        
        mock_ai_response = {
            "tables": {
                "products": {
                    "columns": [
                        {"name": "id", "type": "INTEGER", "primary_key": True},
                        {"name": "name", "type": "VARCHAR(255)", "not_null": True}
                    ],
                    "indexes": [
                        {"name": "idx_products_name", "columns": ["name"], "type": "btree"}
                    ]
                }
            }
        }
        
        with patch('agents.database.agent.ollama_client') as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.generate = AsyncMock(return_value={
                'response': json.dumps(mock_ai_response)
            })
            
            result = await database_agent.generate_schema(requirements)
            
            assert result["database_type"] == "mysql"
            schema = result["schema"]
            assert "products" in schema["tables"]
    
    def test_create_table_sql_generation(self, database_agent):
        """Test CREATE TABLE SQL generation"""
        table_def = {
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                {"name": "name", "type": "VARCHAR(100)", "not_null": True, "unique": True},
                {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
            ],
            "foreign_keys": [
                {"column": "user_id", "references": "users(id)", "on_delete": "CASCADE"}
            ]
        }
        
        sql = database_agent._generate_create_table_sql("test_table", table_def, "postgresql")
        
        assert "CREATE TABLE test_table" in sql
        assert "id SERIAL PRIMARY KEY" in sql
        assert "name VARCHAR(100) NOT NULL UNIQUE" in sql
        assert "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" in sql
        assert "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE" in sql
    
    def test_create_index_sql_generation(self, database_agent):
        """Test CREATE INDEX SQL generation"""
        index_def = {
            "name": "idx_test_name",
            "columns": ["name", "created_at"],
            "type": "btree"
        }
        
        sql = database_agent._generate_create_index_sql("test_table", index_def, "postgresql")
        
        assert "CREATE INDEX idx_test_name ON test_table (name, created_at)" in sql
        
        # Test unique index
        unique_index = {
            "name": "idx_test_unique",
            "columns": ["email"],
            "type": "unique"
        }
        
        unique_sql = database_agent._generate_create_index_sql("test_table", unique_index, "postgresql")
        assert "CREATE UNIQUE INDEX" in unique_sql
    
    def test_optimization_score_calculation(self, database_agent):
        """Test optimization score calculation"""
        good_schema = {
            "tables": {
                "users": {
                    "columns": [
                        {"name": "id", "type": "INTEGER", "primary_key": True},
                        {"name": "created_at", "type": "TIMESTAMP"},
                        {"name": "updated_at", "type": "TIMESTAMP"}
                    ],
                    "indexes": [
                        {"name": "idx_users_created_at", "columns": ["created_at"]}
                    ],
                    "foreign_keys": [
                        {"column": "role_id", "references": "roles(id)"}
                    ],
                    "constraints": [
                        {"type": "check", "definition": "created_at <= CURRENT_TIMESTAMP"}
                    ]
                }
            }
        }
        
        score = database_agent._calculate_optimization_score(good_schema)
        assert 0 <= score <= 100
        assert score > 50  # Should be reasonably good
        
        # Test empty schema
        empty_score = database_agent._calculate_optimization_score({})
        assert empty_score == 0.0
    
    @pytest.mark.asyncio
    async def test_performance_analysis(self, database_agent):
        """Test database performance analysis"""
        database_config = {
            "type": "postgresql",
            "schema": {
                "tables": {
                    "users": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True}
                        ],
                        "foreign_keys": [
                            {"column": "role_id", "references": "roles(id)"}
                        ],
                        "indexes": []  # Missing index for foreign key
                    }
                }
            }
        }
        
        analysis = await database_agent.analyze_performance(database_config)
        
        assert "findings" in analysis
        assert "recommendations" in analysis
        assert "optimization_score" in analysis
        
        # Should find missing index issue
        findings = analysis["findings"]
        assert any("foreign key" in finding.get("description", "").lower() for finding in findings)
    
    def test_apply_optimization_rule_foreign_key_without_index(self, database_agent):
        """Test foreign key without index rule"""
        rule = {
            "name": "missing_index_on_foreign_key",
            "severity": "high", 
            "check": "foreign_key_without_index"
        }
        
        schema = {
            "tables": {
                "orders": {
                    "foreign_keys": [
                        {"column": "user_id", "references": "users(id)"}
                    ],
                    "indexes": []  # No indexes
                }
            }
        }
        
        findings = database_agent._apply_optimization_rule(rule, schema)
        
        assert len(findings) == 1
        finding = findings[0]
        assert finding["severity"] == "high"
        assert finding["table"] == "orders"
        assert finding["column"] == "user_id"
    
    def test_apply_optimization_rule_missing_primary_key(self, database_agent):
        """Test missing primary key rule"""
        rule = {
            "name": "missing_primary_key",
            "severity": "high",
            "check": "table_without_primary_key"
        }
        
        schema = {
            "tables": {
                "logs": {
                    "columns": [
                        {"name": "message", "type": "TEXT"},
                        {"name": "created_at", "type": "TIMESTAMP"}
                    ]
                    # No primary key defined
                }
            }
        }
        
        findings = database_agent._apply_optimization_rule(rule, schema)
        
        assert len(findings) == 1
        finding = findings[0]
        assert finding["table"] == "logs"
        assert "primary key" in finding["description"].lower()
    
    @pytest.mark.asyncio
    async def test_process_task_schema_creation(self, database_agent):
        """Test processing schema creation task"""
        task = {
            "title": "Setup Database Schema",
            "description": "Create database schema for todo application",
            "requirements": {"database": "sqlite"},
            "output_dir": "/tmp/test_output"
        }
        
        with patch('agents.database.agent.ollama_client'):
            with patch('os.makedirs'):
                with patch('builtins.open', create=True) as mock_open:
                    mock_file = Mock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    
                    result = await database_agent.process_task(task)
                    
                    assert result["status"] == "completed"
                    assert "files_created" in result
                    assert "schema" in result
                    assert result["agent_id"] == "database"
    
    def test_infer_project_type(self, database_agent):
        """Test project type inference"""
        todo_task = {
            "description": "Create a todo list application",
            "title": "Todo App Database"
        }
        assert database_agent._infer_project_type(todo_task) == "todo_application"
        
        blog_task = {
            "description": "Setup blog database",
            "title": "Blog System"
        }
        assert database_agent._infer_project_type(blog_task) == "blog_system"
        
        user_task = {
            "description": "User authentication system",
            "title": "User Management"
        }
        assert database_agent._infer_project_type(user_task) == "user_management"
        
        generic_task = {
            "description": "Generic web application",
            "title": "Web App"
        }
        assert database_agent._infer_project_type(generic_task) == "web_application"
    
    def test_extract_entities_from_task(self, database_agent):
        """Test entity extraction from task description"""
        task = {
            "description": "Create a blog system with users, posts, and comments",
            "title": "Blog Application Database"
        }
        
        entities = database_agent._extract_entities_from_task(task)
        
        assert "users" in entities
        assert "posts" in entities
        assert "comments" in entities
    
    def test_generate_database_py_sqlite(self, database_agent):
        """Test database.py generation for SQLite"""
        schema_result = {
            "database_type": "sqlite",
            "migration_scripts": ["CREATE TABLE test..."]
        }
        
        db_py = database_agent._generate_database_py(schema_result, "todo_application")
        
        assert "import sqlite3" in db_py
        assert "class Database:" in db_py
        assert "get_connection" in db_py
        assert "execute_query" in db_py
    
    def test_generate_database_py_postgresql(self, database_agent):
        """Test database.py generation for PostgreSQL"""
        schema_result = {
            "database_type": "postgresql",
            "migration_scripts": ["CREATE TABLE test..."]
        }
        
        db_py = database_agent._generate_database_py(schema_result, "web_application")
        
        assert "asyncpg" in db_py
        assert "create_pool" in db_py
        assert "async def" in db_py
    
    def test_generate_models_py(self, database_agent):
        """Test models.py generation"""
        schema_result = {
            "schema": {
                "tables": {
                    "users": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True},
                            {"name": "username", "type": "VARCHAR(50)", "not_null": True, "unique": True},
                            {"name": "email", "type": "VARCHAR(255)", "not_null": True},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                        ],
                        "foreign_keys": []
                    },
                    "posts": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True},
                            {"name": "title", "type": "VARCHAR(255)", "not_null": True},
                            {"name": "content", "type": "TEXT"},
                            {"name": "user_id", "type": "INTEGER", "not_null": True}
                        ],
                        "foreign_keys": [
                            {"references": "users(id)"}
                        ]
                    }
                }
            }
        }
        
        models_py = database_agent._generate_models_py(schema_result, "blog_system")
        
        assert "from sqlalchemy import" in models_py
        assert "class Users(Base):" in models_py
        assert "class Posts(Base):" in models_py
        assert "__tablename__ = 'users'" in models_py
        assert "relationship(" in models_py

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

