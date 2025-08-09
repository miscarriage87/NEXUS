
"""
Database Agent - Comprehensive database management, schema generation and optimization
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.base_agent import BaseAgent
from core.ollama_client import ollama_client

class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"

class IndexType(Enum):
    BTREE = "btree"
    HASH = "hash"
    GIN = "gin"
    GIST = "gist"
    UNIQUE = "unique"

@dataclass
class TableSchema:
    name: str
    columns: List[Dict[str, Any]]
    primary_key: List[str]
    foreign_keys: List[Dict[str, Any]]
    indexes: List[Dict[str, Any]]
    constraints: List[Dict[str, Any]]

@dataclass
class DatabaseOptimization:
    optimization_type: str
    target_table: str
    recommendation: str
    impact_score: float
    implementation: str

class DatabaseAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("database", "Database Management Agent", config)
        self.supported_databases = [db.value for db in DatabaseType]
        self.schema_templates = self._initialize_schema_templates()
        self.optimization_rules = self._initialize_optimization_rules()
        
    def get_capabilities(self) -> List[str]:
        return [
            "schema_generation",
            "database_design",
            "migration_management", 
            "query_optimization",
            "performance_analysis",
            "data_modeling",
            "index_optimization",
            "database_security",
            "backup_strategies",
            "scaling_recommendations"
        ]
    
    def _initialize_schema_templates(self) -> Dict[str, Any]:
        """Initialize common database schema templates"""
        return {
            "user_management": {
                "tables": {
                    "users": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                            {"name": "username", "type": "VARCHAR(50)", "unique": True, "not_null": True},
                            {"name": "email", "type": "VARCHAR(255)", "unique": True, "not_null": True},
                            {"name": "password_hash", "type": "VARCHAR(255)", "not_null": True},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
                            {"name": "updated_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
                            {"name": "is_active", "type": "BOOLEAN", "default": True}
                        ],
                        "indexes": [
                            {"name": "idx_users_email", "columns": ["email"], "type": "unique"},
                            {"name": "idx_users_username", "columns": ["username"], "type": "unique"},
                            {"name": "idx_users_created_at", "columns": ["created_at"], "type": "btree"}
                        ]
                    },
                    "user_profiles": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                            {"name": "user_id", "type": "INTEGER", "not_null": True},
                            {"name": "first_name", "type": "VARCHAR(100)"},
                            {"name": "last_name", "type": "VARCHAR(100)"},
                            {"name": "avatar_url", "type": "VARCHAR(500)"},
                            {"name": "bio", "type": "TEXT"},
                            {"name": "location", "type": "VARCHAR(255)"},
                            {"name": "website", "type": "VARCHAR(255)"},
                            {"name": "updated_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                        ],
                        "foreign_keys": [
                            {"column": "user_id", "references": "users(id)", "on_delete": "CASCADE"}
                        ]
                    }
                }
            },
            "todo_application": {
                "tables": {
                    "todos": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                            {"name": "title", "type": "VARCHAR(200)", "not_null": True},
                            {"name": "description", "type": "TEXT"},
                            {"name": "completed", "type": "BOOLEAN", "default": False},
                            {"name": "priority", "type": "INTEGER", "default": 1},
                            {"name": "due_date", "type": "TIMESTAMP"},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
                            {"name": "updated_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
                            {"name": "user_id", "type": "INTEGER"}
                        ],
                        "indexes": [
                            {"name": "idx_todos_completed", "columns": ["completed"], "type": "btree"},
                            {"name": "idx_todos_due_date", "columns": ["due_date"], "type": "btree"},
                            {"name": "idx_todos_user_id", "columns": ["user_id"], "type": "btree"}
                        ],
                        "foreign_keys": [
                            {"column": "user_id", "references": "users(id)", "on_delete": "CASCADE"}
                        ]
                    },
                    "categories": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                            {"name": "name", "type": "VARCHAR(100)", "not_null": True, "unique": True},
                            {"name": "color", "type": "VARCHAR(7)", "default": "#000000"},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                        ]
                    },
                    "todo_categories": {
                        "columns": [
                            {"name": "todo_id", "type": "INTEGER", "not_null": True},
                            {"name": "category_id", "type": "INTEGER", "not_null": True}
                        ],
                        "primary_key": ["todo_id", "category_id"],
                        "foreign_keys": [
                            {"column": "todo_id", "references": "todos(id)", "on_delete": "CASCADE"},
                            {"column": "category_id", "references": "categories(id)", "on_delete": "CASCADE"}
                        ]
                    }
                }
            },
            "blog_system": {
                "tables": {
                    "posts": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                            {"name": "title", "type": "VARCHAR(255)", "not_null": True},
                            {"name": "slug", "type": "VARCHAR(255)", "unique": True, "not_null": True},
                            {"name": "content", "type": "TEXT", "not_null": True},
                            {"name": "excerpt", "type": "VARCHAR(500)"},
                            {"name": "status", "type": "VARCHAR(20)", "default": "draft"},
                            {"name": "author_id", "type": "INTEGER", "not_null": True},
                            {"name": "published_at", "type": "TIMESTAMP"},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
                            {"name": "updated_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                        ],
                        "indexes": [
                            {"name": "idx_posts_slug", "columns": ["slug"], "type": "unique"},
                            {"name": "idx_posts_status", "columns": ["status"], "type": "btree"},
                            {"name": "idx_posts_published_at", "columns": ["published_at"], "type": "btree"},
                            {"name": "idx_posts_author_id", "columns": ["author_id"], "type": "btree"}
                        ],
                        "foreign_keys": [
                            {"column": "author_id", "references": "users(id)", "on_delete": "CASCADE"}
                        ]
                    },
                    "comments": {
                        "columns": [
                            {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                            {"name": "post_id", "type": "INTEGER", "not_null": True},
                            {"name": "author_id", "type": "INTEGER"},
                            {"name": "author_name", "type": "VARCHAR(100)"},
                            {"name": "author_email", "type": "VARCHAR(255)"},
                            {"name": "content", "type": "TEXT", "not_null": True},
                            {"name": "status", "type": "VARCHAR(20)", "default": "pending"},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                        ],
                        "indexes": [
                            {"name": "idx_comments_post_id", "columns": ["post_id"], "type": "btree"},
                            {"name": "idx_comments_status", "columns": ["status"], "type": "btree"}
                        ],
                        "foreign_keys": [
                            {"column": "post_id", "references": "posts(id)", "on_delete": "CASCADE"},
                            {"column": "author_id", "references": "users(id)", "on_delete": "SET NULL"}
                        ]
                    }
                }
            }
        }
    
    def _initialize_optimization_rules(self) -> List[Dict[str, Any]]:
        """Initialize database optimization rules"""
        return [
            {
                "name": "missing_index_on_foreign_key",
                "description": "Foreign key columns should have indexes for join performance",
                "severity": "high",
                "check": "foreign_key_without_index",
                "recommendation": "Add index on foreign key column"
            },
            {
                "name": "large_table_without_partitioning",
                "description": "Large tables benefit from partitioning",
                "severity": "medium",
                "check": "table_size_over_threshold",
                "recommendation": "Consider table partitioning"
            },
            {
                "name": "unused_indexes",
                "description": "Unused indexes consume space and slow down writes",
                "severity": "medium",
                "check": "index_usage_statistics",
                "recommendation": "Remove unused indexes"
            },
            {
                "name": "missing_primary_key",
                "description": "Tables should have primary keys for replication and performance",
                "severity": "high",
                "check": "table_without_primary_key",
                "recommendation": "Add primary key to table"
            }
        ]
    
    async def generate_schema(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate database schema based on requirements"""
        project_type = requirements.get('project_type', 'web_application')
        entities = requirements.get('entities', [])
        relationships = requirements.get('relationships', [])
        
        self.logger.info(f"Generating schema for project type: {project_type}")
        
        # Check if we have a template for this project type
        if project_type in self.schema_templates:
            base_schema = self.schema_templates[project_type]
        else:
            # Use AI to generate schema
            base_schema = await self._generate_ai_schema(requirements)
        
        # Enhance schema based on specific requirements
        enhanced_schema = await self._enhance_schema_with_ai(base_schema, requirements)
        
        # Add optimizations and best practices
        optimized_schema = self._apply_optimization_rules(enhanced_schema)
        
        return {
            "schema": optimized_schema,
            "database_type": requirements.get('database_type', 'postgresql'),
            "migration_scripts": await self._generate_migration_scripts(optimized_schema, requirements),
            "indexes": self._generate_recommended_indexes(optimized_schema),
            "constraints": self._generate_constraints(optimized_schema),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "project_type": project_type,
                "optimization_score": self._calculate_optimization_score(optimized_schema)
            }
        }
    
    async def _generate_ai_schema(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to generate database schema from requirements"""
        system_prompt = """Du bist ein Senior-Datenbankarchitekt mit 15+ Jahren Erfahrung. 
        Erstelle ein optimales Datenbankschema basierend auf den Projektanforderungen.
        
        Berücksichtige:
        1. Normalisierung (3NF minimum)
        2. Performance-optimierte Indizierung
        3. Referentielle Integrität
        4. Skalierbarkeit
        5. Sicherheit
        
        Antworte im JSON-Format:
        {
            "tables": {
                "table_name": {
                    "columns": [
                        {"name": "column", "type": "TYPE", "constraints": [...]}
                    ],
                    "primary_key": ["columns"],
                    "foreign_keys": [{"column": "col", "references": "table(col)"}],
                    "indexes": [{"name": "idx_name", "columns": ["col"], "type": "btree"}],
                    "constraints": [{"type": "check", "definition": "condition"}]
                }
            }
        }"""
        
        entities_str = json.dumps(requirements.get('entities', []), indent=2)
        relationships_str = json.dumps(requirements.get('relationships', []), indent=2)
        
        user_prompt = f"""Erstelle ein Datenbankschema für:
        
        Projekttyp: {requirements.get('project_type', 'web_application')}
        Beschreibung: {requirements.get('description', 'Keine Beschreibung')}
        
        Entitäten: {entities_str}
        
        Beziehungen: {relationships_str}
        
        Besondere Anforderungen:
        - Datenbank-Typ: {requirements.get('database_type', 'postgresql')}
        - Erwartete Datenmenge: {requirements.get('expected_data_volume', 'medium')}
        - Performance-Anforderungen: {requirements.get('performance_requirements', 'standard')}
        - Compliance: {requirements.get('compliance_requirements', [])}
        
        Erstelle ein vollständiges, optimiertes Schema."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('database', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                schema_text = response.get('response', '{}')
                try:
                    schema = json.loads(schema_text)
                    return schema
                except json.JSONDecodeError:
                    self.logger.warning("AI returned invalid JSON, using fallback schema")
                    return self._create_fallback_schema(requirements)
                    
        except Exception as e:
            self.logger.error(f"Error generating AI schema: {str(e)}")
            return self._create_fallback_schema(requirements)
    
    def _create_fallback_schema(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create a simple fallback schema"""
        return {
            "tables": {
                "items": {
                    "columns": [
                        {"name": "id", "type": "INTEGER", "primary_key": True, "auto_increment": True},
                        {"name": "name", "type": "VARCHAR(255)", "not_null": True},
                        {"name": "description", "type": "TEXT"},
                        {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                    ],
                    "indexes": [
                        {"name": "idx_items_name", "columns": ["name"], "type": "btree"}
                    ]
                }
            }
        }
    
    async def _enhance_schema_with_ai(self, base_schema: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance base schema with AI suggestions"""
        # Add audit fields, optimize data types, add missing relationships
        enhanced_schema = base_schema.copy()
        
        # Add common audit fields to all tables
        for table_name, table_def in enhanced_schema.get('tables', {}).items():
            columns = table_def.get('columns', [])
            
            # Add audit columns if not present
            audit_columns = ['created_at', 'updated_at', 'created_by', 'updated_by']
            existing_columns = [col.get('name') for col in columns]
            
            for audit_col in audit_columns:
                if audit_col not in existing_columns:
                    if audit_col in ['created_at', 'updated_at']:
                        columns.append({
                            "name": audit_col,
                            "type": "TIMESTAMP",
                            "default": "CURRENT_TIMESTAMP"
                        })
                    elif audit_col in ['created_by', 'updated_by']:
                        columns.append({
                            "name": audit_col,
                            "type": "INTEGER",
                            "references": "users(id)"
                        })
        
        return enhanced_schema
    
    def _apply_optimization_rules(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization rules to schema"""
        optimized_schema = schema.copy()
        
        # Apply each optimization rule
        for table_name, table_def in optimized_schema.get('tables', {}).items():
            # Ensure primary key exists
            if not table_def.get('primary_key') and not any(
                col.get('primary_key') for col in table_def.get('columns', [])
            ):
                # Add surrogate primary key
                columns = table_def.setdefault('columns', [])
                columns.insert(0, {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "auto_increment": True
                })
            
            # Add indexes for foreign keys
            foreign_keys = table_def.get('foreign_keys', [])
            indexes = table_def.setdefault('indexes', [])
            
            for fk in foreign_keys:
                fk_column = fk.get('column')
                if fk_column:
                    # Check if index already exists
                    existing_indexes = [idx.get('columns', []) for idx in indexes]
                    if [fk_column] not in existing_indexes:
                        indexes.append({
                            "name": f"idx_{table_name}_{fk_column}",
                            "columns": [fk_column],
                            "type": "btree"
                        })
        
        return optimized_schema
    
    async def _generate_migration_scripts(self, schema: Dict[str, Any], requirements: Dict[str, Any]) -> List[str]:
        """Generate database migration scripts"""
        db_type = requirements.get('database_type', 'postgresql')
        migrations = []
        
        # Generate CREATE TABLE statements
        for table_name, table_def in schema.get('tables', {}).items():
            migration = self._generate_create_table_sql(table_name, table_def, db_type)
            migrations.append(migration)
        
        # Generate INDEX statements
        for table_name, table_def in schema.get('tables', {}).items():
            for index in table_def.get('indexes', []):
                index_sql = self._generate_create_index_sql(table_name, index, db_type)
                migrations.append(index_sql)
        
        return migrations
    
    def _generate_create_table_sql(self, table_name: str, table_def: Dict[str, Any], db_type: str) -> str:
        """Generate CREATE TABLE SQL statement"""
        columns = table_def.get('columns', [])
        
        column_definitions = []
        for col in columns:
            col_def = f"{col['name']} {col['type']}"
            
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if col.get('auto_increment') and db_type in ['mysql', 'sqlite']:
                col_def += " AUTOINCREMENT" if db_type == 'sqlite' else " AUTO_INCREMENT"
            elif col.get('auto_increment') and db_type == 'postgresql':
                col_def = f"{col['name']} SERIAL PRIMARY KEY"
            if col.get('not_null'):
                col_def += " NOT NULL"
            if col.get('unique'):
                col_def += " UNIQUE"
            if col.get('default') is not None:
                col_def += f" DEFAULT {col['default']}"
            
            column_definitions.append(col_def)
        
        # Add foreign key constraints
        foreign_keys = table_def.get('foreign_keys', [])
        for fk in foreign_keys:
            fk_def = f"FOREIGN KEY ({fk['column']}) REFERENCES {fk['references']}"
            if fk.get('on_delete'):
                fk_def += f" ON DELETE {fk['on_delete']}"
            column_definitions.append(fk_def)
        
        column_separator = ',\n    '
        sql = f"""CREATE TABLE {table_name} (
    {column_separator.join(column_definitions)}
);"""
        
        return sql
    
    def _generate_create_index_sql(self, table_name: str, index: Dict[str, Any], db_type: str) -> str:
        """Generate CREATE INDEX SQL statement"""
        index_name = index.get('name', f"idx_{table_name}_{'_'.join(index['columns'])}")
        columns = ', '.join(index['columns'])
        index_type = index.get('type', 'btree')
        
        unique = "UNIQUE " if index_type == 'unique' else ""
        
        if db_type == 'postgresql' and index_type not in ['unique', 'btree']:
            sql = f"CREATE {unique}INDEX {index_name} ON {table_name} USING {index_type} ({columns});"
        else:
            sql = f"CREATE {unique}INDEX {index_name} ON {table_name} ({columns});"
        
        return sql
    
    def _generate_recommended_indexes(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommended indexes for performance"""
        recommendations = []
        
        for table_name, table_def in schema.get('tables', {}).items():
            columns = table_def.get('columns', [])
            
            # Recommend indexes for commonly queried columns
            for col in columns:
                col_name = col.get('name')
                col_type = col.get('type', '').upper()
                
                # Date/timestamp columns often used in WHERE clauses
                if 'TIMESTAMP' in col_type or 'DATE' in col_type:
                    if col_name not in ['created_at', 'updated_at']:  # Skip audit fields
                        recommendations.append({
                            "table": table_name,
                            "index_name": f"idx_{table_name}_{col_name}",
                            "columns": [col_name],
                            "type": "btree",
                            "reason": "Date/timestamp column for range queries"
                        })
                
                # Status/enum columns
                if col_name in ['status', 'type', 'category', 'state']:
                    recommendations.append({
                        "table": table_name,
                        "index_name": f"idx_{table_name}_{col_name}",
                        "columns": [col_name],
                        "type": "btree",
                        "reason": "Status/categorical column for filtering"
                    })
        
        return recommendations
    
    def _generate_constraints(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate database constraints"""
        constraints = []
        
        for table_name, table_def in schema.get('tables', {}).items():
            # Add common constraints
            constraints.extend([
                {
                    "table": table_name,
                    "type": "check",
                    "name": f"chk_{table_name}_created_at",
                    "definition": "created_at <= CURRENT_TIMESTAMP",
                    "reason": "Ensure created_at is not in future"
                }
            ])
            
            # Add specific constraints based on column names
            for col in table_def.get('columns', []):
                col_name = col.get('name')
                col_type = col.get('type', '')
                
                if col_name == 'email':
                    email_regex = r"email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'"
                    constraints.append({
                        "table": table_name,
                        "type": "check",
                        "name": f"chk_{table_name}_email_format",
                        "definition": email_regex,
                        "reason": "Validate email format"
                    })
                
                if col_name in ['priority', 'rating', 'score']:
                    constraints.append({
                        "table": table_name,
                        "type": "check",
                        "name": f"chk_{table_name}_{col_name}_range",
                        "definition": f"{col_name} >= 0 AND {col_name} <= 10",
                        "reason": f"Ensure {col_name} is in valid range"
                    })
        
        return constraints
    
    def _calculate_optimization_score(self, schema: Dict[str, Any]) -> float:
        """Calculate optimization score for schema"""
        score = 0.0
        max_score = 0.0
        
        for table_name, table_def in schema.get('tables', {}).items():
            table_score = 0.0
            table_max = 0.0
            
            # Check for primary key
            has_pk = (table_def.get('primary_key') or 
                     any(col.get('primary_key') for col in table_def.get('columns', [])))
            table_score += 20 if has_pk else 0
            table_max += 20
            
            # Check for appropriate indexes
            fk_count = len(table_def.get('foreign_keys', []))
            index_count = len(table_def.get('indexes', []))
            
            if fk_count > 0:
                # Should have at least as many indexes as foreign keys
                index_ratio = min(index_count / fk_count, 1.0)
                table_score += index_ratio * 30
            else:
                table_score += 30  # No FKs needed
            table_max += 30
            
            # Check for audit fields
            columns = [col.get('name') for col in table_def.get('columns', [])]
            audit_fields = ['created_at', 'updated_at']
            audit_score = sum(10 for field in audit_fields if field in columns)
            table_score += audit_score
            table_max += 20
            
            # Check for constraints
            constraints = table_def.get('constraints', [])
            constraint_score = min(len(constraints) * 5, 30)
            table_score += constraint_score
            table_max += 30
            
            score += table_score
            max_score += table_max
        
        return (score / max_score * 100) if max_score > 0 else 0.0
    
    async def analyze_performance(self, database_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze database performance and provide recommendations"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "database_type": database_config.get('type', 'unknown'),
            "analysis_type": "static_analysis",  # Could be extended to dynamic analysis
            "findings": [],
            "recommendations": [],
            "optimization_score": 0.0
        }
        
        # Apply optimization rules
        schema = database_config.get('schema', {})
        
        for rule in self.optimization_rules:
            findings = self._apply_optimization_rule(rule, schema)
            analysis["findings"].extend(findings)
        
        # Generate recommendations
        for finding in analysis["findings"]:
            if finding["severity"] == "high":
                analysis["recommendations"].append({
                    "priority": "immediate",
                    "recommendation": finding["recommendation"],
                    "impact": "high",
                    "effort": "medium"
                })
        
        # Calculate overall optimization score
        analysis["optimization_score"] = self._calculate_optimization_score(schema)
        
        return analysis
    
    def _apply_optimization_rule(self, rule: Dict[str, Any], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply a specific optimization rule"""
        findings = []
        
        if rule["check"] == "foreign_key_without_index":
            for table_name, table_def in schema.get('tables', {}).items():
                foreign_keys = table_def.get('foreign_keys', [])
                indexes = table_def.get('indexes', [])
                indexed_columns = set()
                
                for index in indexes:
                    indexed_columns.update(index.get('columns', []))
                
                for fk in foreign_keys:
                    fk_column = fk.get('column')
                    if fk_column and fk_column not in indexed_columns:
                        findings.append({
                            "rule": rule["name"],
                            "severity": rule["severity"],
                            "table": table_name,
                            "column": fk_column,
                            "description": f"Foreign key column '{fk_column}' lacks index",
                            "recommendation": f"Add index on {table_name}.{fk_column}"
                        })
        
        elif rule["check"] == "table_without_primary_key":
            for table_name, table_def in schema.get('tables', {}).items():
                has_pk = (table_def.get('primary_key') or 
                         any(col.get('primary_key') for col in table_def.get('columns', [])))
                
                if not has_pk:
                    findings.append({
                        "rule": rule["name"],
                        "severity": rule["severity"],
                        "table": table_name,
                        "description": f"Table '{table_name}' lacks primary key",
                        "recommendation": f"Add primary key to {table_name}"
                    })
        
        return findings
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process database-related tasks"""
        try:
            task_type = task.get("title", "").lower()
            requirements = task.get("requirements", {})
            output_dir = task.get("output_dir", "/tmp")
            
            if "schema" in task_type or "database" in task_type:
                # Generate database schema
                project_type = self._infer_project_type(task)
                
                schema_requirements = {
                    "project_type": project_type,
                    "database_type": requirements.get("database", "sqlite"),
                    "description": task.get("description", ""),
                    "entities": self._extract_entities_from_task(task),
                    "relationships": [],
                    "expected_data_volume": "medium",
                    "performance_requirements": "standard"
                }
                
                schema_result = await self.generate_schema(schema_requirements)
                
                # Write database files
                db_files = await self._write_database_files(schema_result, output_dir, project_type)
                
                return {
                    "status": "completed",
                    "result": "Database schema generated successfully",
                    "files_created": db_files,
                    "schema": schema_result,
                    "agent_id": self.agent_id
                }
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown database task type: {task_type}",
                    "agent_id": self.agent_id
                }
                
        except Exception as e:
            self.logger.error(f"Error processing database task: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "agent_id": self.agent_id
            }
    
    def _infer_project_type(self, task: Dict[str, Any]) -> str:
        """Infer project type from task description"""
        description = (task.get("description", "") + " " + 
                      task.get("title", "")).lower()
        
        if "todo" in description or "task" in description:
            return "todo_application"
        elif "blog" in description or "post" in description:
            return "blog_system"
        elif "user" in description or "auth" in description:
            return "user_management"
        else:
            return "web_application"
    
    def _extract_entities_from_task(self, task: Dict[str, Any]) -> List[str]:
        """Extract entities from task description"""
        description = task.get("description", "").lower()
        title = task.get("title", "").lower()
        
        # Common entities based on keywords
        entities = []
        
        entity_keywords = {
            "users": ["user", "account", "login", "auth"],
            "todos": ["todo", "task", "item"],
            "posts": ["post", "blog", "article"],
            "comments": ["comment", "reply"],
            "categories": ["category", "tag", "label"],
            "orders": ["order", "purchase", "buy"],
            "products": ["product", "item", "catalog"]
        }
        
        full_text = f"{description} {title}"
        
        for entity, keywords in entity_keywords.items():
            if any(keyword in full_text for keyword in keywords):
                entities.append(entity)
        
        return entities if entities else ["items"]  # Default entity
    
    async def _write_database_files(self, schema_result: Dict[str, Any], output_dir: str, project_type: str) -> List[str]:
        """Write database-related files to output directory"""
        files_created = []
        
        # Create backend directory
        backend_dir = f"{output_dir}/backend"
        os.makedirs(backend_dir, exist_ok=True)
        
        # Write database.py
        database_py = self._generate_database_py(schema_result, project_type)
        db_file = f"{backend_dir}/database.py"
        with open(db_file, 'w') as f:
            f.write(database_py)
        files_created.append(db_file)
        
        # Write models.py
        models_py = self._generate_models_py(schema_result, project_type)
        models_file = f"{backend_dir}/models.py"
        with open(models_file, 'w') as f:
            f.write(models_py)
        files_created.append(models_file)
        
        # Write migration script
        migration_sql = '\n\n'.join(schema_result.get('migration_scripts', []))
        migration_file = f"{backend_dir}/init_db.sql"
        with open(migration_file, 'w') as f:
            f.write(migration_sql)
        files_created.append(migration_file)
        
        return files_created
    
    def _generate_database_py(self, schema_result: Dict[str, Any], project_type: str) -> str:
        """Generate database.py file"""
        db_type = schema_result.get('database_type', 'sqlite')
        
        if db_type == 'sqlite':
            return '''import sqlite3
from typing import Dict, List, Any
import os

class Database:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with schema"""
        if not os.path.exists(self.db_path):
            with open('init_db.sql', 'r') as f:
                schema = f.read()
            
            conn = sqlite3.connect(self.db_path)
            conn.executescript(schema)
            conn.close()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected_rows

# Global database instance
db = Database()
'''
        else:
            # PostgreSQL/MySQL version
            return f'''import asyncpg  # or pymysql for MySQL
from typing import Dict, List, Any
import os
import asyncio

class Database:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv(
            'DATABASE_URL', 
            'postgresql://user:password@localhost/dbname'
        )
        self.pool = None
    
    async def init_pool(self):
        """Initialize connection pool"""
        self.pool = await asyncpg.create_pool(self.connection_string)
        await self.init_db()
    
    async def init_db(self):
        """Initialize database with schema"""
        with open('init_db.sql', 'r') as f:
            schema = f.read()
        
        async with self.pool.acquire() as conn:
            await conn.execute(schema)
    
    async def execute_query(self, query: str, *params) -> List[Dict]:
        """Execute SELECT query"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(row) for row in rows]
    
    async def execute_update(self, query: str, *params) -> str:
        """Execute INSERT/UPDATE/DELETE query"""
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, *params)
            return result

# Global database instance
db = Database()
'''
    
    def _generate_models_py(self, schema_result: Dict[str, Any], project_type: str) -> str:
        """Generate SQLAlchemy models.py file"""
        schema = schema_result.get('schema', {})
        tables = schema.get('tables', {})
        
        imports = '''from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

'''
        
        models = []
        for table_name, table_def in tables.items():
            model_class = ''.join(word.capitalize() for word in table_name.split('_'))
            
            model_code = f'''class {model_class}(Base):
    __tablename__ = '{table_name}'
    
'''
            
            # Add columns
            for col in table_def.get('columns', []):
                col_name = col['name']
                col_type = col['type']
                
                # Map SQL types to SQLAlchemy types
                if 'INTEGER' in col_type.upper():
                    sa_type = 'Integer'
                elif 'VARCHAR' in col_type.upper() or 'CHAR' in col_type.upper():
                    sa_type = 'String'
                elif 'TEXT' in col_type.upper():
                    sa_type = 'Text'
                elif 'BOOLEAN' in col_type.upper():
                    sa_type = 'Boolean'
                elif 'TIMESTAMP' in col_type.upper() or 'DATETIME' in col_type.upper():
                    sa_type = 'DateTime'
                else:
                    sa_type = 'String'
                
                # Add column definition
                column_def = f"    {col_name} = Column({sa_type}"
                
                if col.get('primary_key'):
                    column_def += ", primary_key=True"
                if col.get('unique'):
                    column_def += ", unique=True"
                if col.get('not_null'):
                    column_def += ", nullable=False"
                if col.get('default') and sa_type == 'DateTime':
                    column_def += ", default=datetime.utcnow"
                elif col.get('default'):
                    column_def += f", default={repr(col['default'])}"
                
                column_def += ")\n"
                model_code += column_def
            
            # Add foreign key relationships
            for fk in table_def.get('foreign_keys', []):
                ref_table = fk['references'].split('(')[0]
                ref_class = ''.join(word.capitalize() for word in ref_table.split('_'))
                rel_name = ref_table.rstrip('s')  # Simple pluralization removal
                
                model_code += f"    {rel_name} = relationship('{ref_class}')\n"
            
            models.append(model_code)
        
        return imports + '\n\n'.join(models)

