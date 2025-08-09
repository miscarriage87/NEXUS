
"""
Comprehensive tests for Learning Agent
"""
import pytest
import asyncio
import json
import tempfile
import sqlite3
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.learning_agent import LearningAgent, CodePattern, ProjectOutcome, Recommendation

@pytest.fixture
def temp_knowledge_dir():
    """Create temporary directory for knowledge base"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def learning_config(temp_knowledge_dir):
    return {
        'agents': {
            'learning': {
                'knowledge_base_path': temp_knowledge_dir,
                'learning_rate': 0.01,
                'pattern_similarity_threshold': 0.85,
                'model': 'qwen2.5-coder:7b'
            }
        }
    }

@pytest.fixture
def learning_agent(learning_config):
    return LearningAgent(learning_config)

@pytest.fixture
def sample_code_patterns():
    return [
        """
        async def get_user(user_id: int):
            query = "SELECT * FROM users WHERE id = ?"
            return await db.execute(query, (user_id,))
        """,
        """
        class UserService:
            def __init__(self, db):
                self.db = db
            
            async def create_user(self, user_data):
                return await self.db.create(user_data)
        """,
        """
        @app.route('/api/users', methods=['POST'])
        @jwt_required()
        def create_user():
            data = request.get_json()
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict())
        """
    ]

@pytest.fixture
def sample_project_outcome():
    return {
        "project_id": "test_project_123",
        "project_type": "web_application",
        "technologies": ["python", "fastapi", "postgresql"],
        "requirements": {"features": ["auth", "api", "database"]},
        "success_metrics": {"overall_score": 0.85, "performance": 0.9, "security": 0.8},
        "patterns_used": ["async_function", "class_definition", "api_route"],
        "completion_time": 45.5,
        "success_score": 0.85,
        "issues_encountered": ["initial_db_setup", "auth_integration"]
    }

@pytest.mark.asyncio
async def test_learning_agent_initialization(learning_agent):
    """Test Learning Agent initialization"""
    assert learning_agent.agent_id == "learning"
    assert learning_agent.name == "Adaptive Learning Agent"
    assert len(learning_agent.get_capabilities()) > 10
    assert os.path.exists(learning_agent.db_path)

@pytest.mark.asyncio
async def test_knowledge_base_setup(learning_agent):
    """Test knowledge base database setup"""
    # Check if database was created with correct tables
    with sqlite3.connect(learning_agent.db_path) as conn:
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['code_patterns', 'project_outcomes', 'recommendations', 'feedback']
        for table in expected_tables:
            assert table in tables

@pytest.mark.asyncio
async def test_code_pattern_analysis(learning_agent, sample_code_patterns):
    """Test code pattern analysis functionality"""
    context = {
        "project_type": "web_application",
        "technologies": ["python", "fastapi"],
        "success_metrics": {"overall_score": 0.8}
    }
    
    result = await learning_agent.analyze_code_patterns(sample_code_patterns, context)
    
    assert result["status"] == "completed"
    assert "analysis" in result
    assert result["analysis"]["samples_analyzed"] == len(sample_code_patterns)
    assert isinstance(result["analysis"]["patterns_found"], list)

@pytest.mark.asyncio
async def test_pattern_extraction(learning_agent):
    """Test pattern extraction from code"""
    code = """
    async def process_data(data: List[Dict]) -> Dict:
        results = []
        for item in data:
            processed = await transform_item(item)
            results.append(processed)
        return {"results": results, "count": len(results)}
    """
    
    patterns = await learning_agent._extract_patterns_from_code(code, {"technologies": ["python"]})
    
    assert len(patterns) > 0
    assert any(pattern["type"] == "function" for pattern in patterns)

@pytest.mark.asyncio
async def test_pattern_id_generation(learning_agent):
    """Test pattern ID generation"""
    code1 = "def hello(): pass"
    code2 = "def hello(): pass"  # Same code
    code3 = "def world(): pass"  # Different code
    
    id1 = learning_agent._generate_pattern_id(code1)
    id2 = learning_agent._generate_pattern_id(code2)
    id3 = learning_agent._generate_pattern_id(code3)
    
    assert id1 == id2  # Same code should have same ID
    assert id1 != id3  # Different code should have different ID

@pytest.mark.asyncio
async def test_learn_from_project(learning_agent, sample_project_outcome):
    """Test learning from project outcomes"""
    result = await learning_agent.learn_from_project(sample_project_outcome)
    
    assert result["status"] == "completed"
    assert result["project_id"] == sample_project_outcome["project_id"]
    assert sample_project_outcome["project_id"] in learning_agent.project_outcomes

@pytest.mark.asyncio
async def test_project_outcome_storage(learning_agent, sample_project_outcome):
    """Test project outcome database storage"""
    await learning_agent.learn_from_project(sample_project_outcome)
    
    # Check if stored in database
    with sqlite3.connect(learning_agent.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project_outcomes WHERE project_id = ?", 
                      (sample_project_outcome["project_id"],))
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] == sample_project_outcome["project_id"]  # project_id

@pytest.mark.asyncio
async def test_get_recommendations(learning_agent):
    """Test recommendation generation"""
    # Add some patterns first
    await learning_agent.analyze_code_patterns([
        "async def get_data(): return await db.fetch()",
        "class DataService: pass"
    ], {"technologies": ["python", "fastapi"]})
    
    context = {
        "project_type": "web_application",
        "technologies": ["python", "fastapi", "postgresql"],
        "current_patterns": ["async_function"]
    }
    
    recommendations = await learning_agent.get_recommendations(context)
    
    assert isinstance(recommendations, list)
    # May be empty initially, but should be a valid list

@pytest.mark.asyncio
async def test_project_outcome_prediction(learning_agent, sample_project_outcome):
    """Test project outcome prediction"""
    # First, learn from a sample project
    await learning_agent.learn_from_project(sample_project_outcome)
    
    project_config = {
        "project_type": "web_application",
        "technologies": ["python", "fastapi", "postgresql"],
        "requirements": {"features": ["auth", "api"]}
    }
    
    prediction = await learning_agent.predict_project_outcome(project_config)
    
    assert prediction["status"] == "completed"
    assert "prediction" in prediction
    assert "predicted_success_score" in prediction["prediction"]
    assert "confidence" in prediction["prediction"]

@pytest.mark.asyncio
async def test_similar_project_finding(learning_agent, sample_project_outcome):
    """Test finding similar projects"""
    await learning_agent.learn_from_project(sample_project_outcome)
    
    config = {
        "project_type": "web_application",
        "technologies": ["python", "fastapi"]  # Similar to sample
    }
    
    similar_projects = learning_agent._find_similar_projects(config)
    
    assert isinstance(similar_projects, list)
    if similar_projects:  # If we found similar projects
        assert "similarity_score" in similar_projects[0]
        assert "success_score" in similar_projects[0]

@pytest.mark.asyncio
async def test_completion_time_estimation(learning_agent, sample_project_outcome):
    """Test project completion time estimation"""
    await learning_agent.learn_from_project(sample_project_outcome)
    
    config = {
        "project_type": "web_application",
        "technologies": ["python", "fastapi", "postgresql"]
    }
    
    estimated_time = learning_agent._estimate_completion_time(config)
    
    assert isinstance(estimated_time, (int, float))
    assert estimated_time > 0

@pytest.mark.asyncio
async def test_learning_metrics(learning_agent):
    """Test learning metrics collection"""
    metrics = await learning_agent.get_learning_metrics()
    
    assert "learning_metrics" in metrics
    assert "knowledge_base_stats" in metrics
    assert "timestamp" in metrics
    assert "patterns" in metrics["knowledge_base_stats"]

@pytest.mark.asyncio
async def test_pattern_similarity_search(learning_agent):
    """Test finding similar patterns"""
    # Add some test patterns
    await learning_agent.analyze_code_patterns([
        "def calculate_total(items): return sum(item.price for item in items)",
        "async def fetch_user(id): return await db.get_user(id)"
    ], {"technologies": ["python"]})
    
    current_patterns = [{"type": "function", "description": "calculation function"}]
    context = {"technologies": ["python"]}
    
    similar_patterns = learning_agent._find_similar_patterns(current_patterns, context)
    
    assert isinstance(similar_patterns, list)

@pytest.mark.asyncio
async def test_model_persistence(learning_agent):
    """Test learning model persistence"""
    # Add some data to models
    learning_agent.pattern_frequencies["test_pattern"] = 5
    learning_agent.technology_correlations["python"]["fastapi"] = 0.8
    learning_agent.success_predictors["uses_python"] = 0.9
    
    # Save models
    learning_agent.save_learning_models()
    
    # Create new agent instance
    new_agent = LearningAgent(learning_agent.config)
    
    # Check if data was loaded
    assert new_agent.pattern_frequencies.get("test_pattern", 0) == 5
    assert new_agent.technology_correlations.get("python", {}).get("fastapi", 0) == 0.8

@pytest.mark.asyncio
async def test_false_positive_reduction(learning_agent):
    """Test false positive pattern detection"""
    # Test FP detection logic
    test_pattern_fp = "test:pattern:/test/example.py"
    learning_agent.false_positive_patterns.add(test_pattern_fp)
    
    # This would be used in actual pattern analysis
    assert test_pattern_fp in learning_agent.false_positive_patterns

@pytest.mark.asyncio
async def test_pattern_distribution(learning_agent):
    """Test pattern distribution analysis"""
    # Add some test patterns
    pattern1 = CodePattern("p1", "function", "def test1(): pass", "Test function 1")
    pattern2 = CodePattern("p2", "class", "class Test2: pass", "Test class 1")
    pattern3 = CodePattern("p3", "function", "def test3(): pass", "Test function 2")
    
    learning_agent.code_patterns["p1"] = pattern1
    learning_agent.code_patterns["p2"] = pattern2
    learning_agent.code_patterns["p3"] = pattern3
    
    distribution = learning_agent._get_pattern_distribution()
    
    assert distribution["function"] == 2
    assert distribution["class"] == 1

@pytest.mark.asyncio
async def test_technology_success_rates(learning_agent):
    """Test technology success rate calculation"""
    # Add test project outcomes
    outcome1 = ProjectOutcome("p1", "web_app", ["python", "fastapi"], {}, {}, [], 10, 0.8)
    outcome2 = ProjectOutcome("p2", "api", ["python", "django"], {}, {}, [], 15, 0.9)
    outcome3 = ProjectOutcome("p3", "web_app", ["python", "fastapi"], {}, {}, [], 12, 0.7)
    
    learning_agent.project_outcomes["p1"] = outcome1
    learning_agent.project_outcomes["p2"] = outcome2
    learning_agent.project_outcomes["p3"] = outcome3
    
    success_rates = learning_agent._get_technology_success_rates()
    
    assert "python" in success_rates
    assert "fastapi" in success_rates
    assert success_rates["python"] > 0  # Should have positive success rate

@pytest.mark.asyncio
@patch('agents.learning_agent.ollama_client')
async def test_llm_integration(mock_ollama, learning_agent):
    """Test LLM integration for pattern enhancement"""
    # Mock LLM response
    mock_ollama.__aenter__.return_value = mock_ollama
    mock_ollama.generate.return_value = {
        "response": json.dumps([{
            "type": "function",
            "code": "def test(): pass",
            "description": "Enhanced description",
            "quality_score": 8
        }])
    }
    
    patterns = [{"type": "function", "code": "def test(): pass", "description": "Basic function"}]
    enhanced = await learning_agent._enhance_patterns_with_llm(patterns, {"technologies": ["python"]})
    
    assert isinstance(enhanced, list)

@pytest.mark.asyncio
async def test_process_task_types(learning_agent, sample_code_patterns, sample_project_outcome):
    """Test different task types processing"""
    # Test analyze_patterns task
    task1 = {
        "task_type": "analyze_patterns",
        "code_samples": sample_code_patterns,
        "context": {"technologies": ["python"]}
    }
    result1 = await learning_agent.process_task(task1)
    assert result1["status"] == "completed"
    
    # Test learn_from_project task
    task2 = {
        "task_type": "learn_from_project",
        "project_data": sample_project_outcome
    }
    result2 = await learning_agent.process_task(task2)
    assert result2["status"] == "completed"
    
    # Test get_recommendations task
    task3 = {
        "task_type": "get_recommendations",
        "context": {"technologies": ["python", "fastapi"]}
    }
    result3 = await learning_agent.process_task(task3)
    assert result3["status"] == "completed"
    
    # Test predict_outcome task
    task4 = {
        "task_type": "predict_outcome",
        "project_config": {"technologies": ["python"], "project_type": "web_app"}
    }
    result4 = await learning_agent.process_task(task4)
    assert result4["status"] == "completed"
    
    # Test get_metrics task
    task5 = {"task_type": "get_metrics"}
    result5 = await learning_agent.process_task(task5)
    assert "learning_metrics" in result5

@pytest.mark.asyncio
async def test_unknown_task_handling(learning_agent):
    """Test handling of unknown task types"""
    task = {"task_type": "unknown_task"}
    result = await learning_agent.process_task(task)
    
    assert result["status"] == "error"
    assert "Unknown task type" in result["message"]
    assert "available_tasks" in result

@pytest.mark.asyncio 
async def test_security_pattern_analysis(learning_agent):
    """Test security-specific pattern analysis"""
    security_code = [
        "password = 'hardcoded123'",  # Security issue
        "user_input = request.args.get('input')",  # Input handling
        "query = f'SELECT * FROM users WHERE id = {user_id}'"  # SQL injection risk
    ]
    
    task = {
        "task_type": "security_pattern_analysis",
        "code_samples": security_code,
        "context": {"focus": "security", "technologies": ["python"]}
    }
    
    result = await learning_agent.process_task(task)
    
    assert result["status"] == "completed"
    assert "analysis" in result

if __name__ == "__main__":
    pytest.main([__file__])
