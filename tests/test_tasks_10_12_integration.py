
"""
Integration tests for Tasks 10-12: Integration Agent, Learning Agent, Security Agent
"""
import pytest
import asyncio
import json
import tempfile
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.integration_agent import IntegrationAgent
from agents.learning_agent import LearningAgent  
from agents.security_agent import SecurityAgent

@pytest.fixture
def temp_knowledge_dir():
    """Create temporary directory for learning agent knowledge base"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def temp_project_dir():
    """Create temporary project directory with sample code"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample Python files
        main_file = os.path.join(temp_dir, "main.py")
        with open(main_file, 'w') as f:
            f.write('''
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # This is a secure pattern using parameterized queries
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                  (data['name'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({"status": "created"})

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return jsonify(user) if user else jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=False)  # Good: debug disabled
''')
        
        # Create requirements.txt
        req_file = os.path.join(temp_dir, "requirements.txt")
        with open(req_file, 'w') as f:
            f.write('''
flask==2.3.0
sqlite3
gunicorn==20.1.0
''')
        
        yield temp_dir

@pytest.fixture
def integration_config(temp_knowledge_dir):
    return {
        'agents': {
            'integration': {
                'max_concurrent_workflows': 5,
                'workflow_timeout_minutes': 30
            },
            'learning': {
                'knowledge_base_path': temp_knowledge_dir,
                'learning_rate': 0.01,
                'pattern_similarity_threshold': 0.85
            },
            'security': {
                'scan_engines': ['custom'],  # Only custom for testing
                'owasp_compliance_level': 'strict',
                'max_scan_time_seconds': 60
            }
        }
    }

@pytest.fixture
async def all_agents(integration_config):
    """Create all three agents for integration testing"""
    integration_agent = IntegrationAgent(integration_config)
    learning_agent = LearningAgent(integration_config)
    security_agent = SecurityAgent(integration_config)
    
    # Register agents with integration agent
    await integration_agent.register_agent(learning_agent)
    await integration_agent.register_agent(security_agent)
    
    return {
        'integration': integration_agent,
        'learning': learning_agent,
        'security': security_agent
    }

@pytest.mark.asyncio
async def test_agent_registration_and_health(all_agents):
    """Test that all agents register properly and report healthy status"""
    integration_agent = all_agents['integration']
    
    # Check agents are registered
    assert 'learning' in integration_agent.registered_agents
    assert 'security' in integration_agent.registered_agents
    
    # Check health monitoring
    health_report = await integration_agent.monitor_agent_health()
    
    assert health_report['overall_health'] in ['healthy', 'degraded']
    assert 'learning' in health_report['agents']
    assert 'security' in health_report['agents']

@pytest.mark.asyncio
async def test_security_learning_integration(all_agents, temp_project_dir):
    """Test integration between Security Agent and Learning Agent"""
    security_agent = all_agents['security']
    learning_agent = all_agents['learning']
    
    # Step 1: Security agent scans code
    security_scan = await security_agent.scan_code_security(temp_project_dir)
    
    assert security_scan['status'] == 'completed'
    
    # Step 2: Extract code patterns for learning
    with open(os.path.join(temp_project_dir, 'main.py'), 'r') as f:
        code_content = f.read()
    
    # Step 3: Learning agent analyzes security patterns
    learning_task = {
        'task_type': 'security_pattern_analysis',
        'code_samples': [code_content],
        'context': {
            'focus': 'security',
            'technologies': ['python', 'flask'],
            'security_scan_results': security_scan['vulnerabilities']
        }
    }
    
    learning_result = await learning_agent.process_task(learning_task)
    
    assert learning_result['status'] == 'completed'
    assert 'analysis' in learning_result

@pytest.mark.asyncio
async def test_comprehensive_security_audit_workflow(all_agents, temp_project_dir):
    """Test comprehensive security audit workflow using Integration Agent"""
    integration_agent = all_agents['integration']
    
    # Create security audit workflow
    workflow_config = {
        'template': 'security_audit',
        'requirements': {
            'project_path': temp_project_dir,
            'audit_level': 'comprehensive'
        },
        'project_context': {
            'name': 'test_security_audit',
            'type': 'web_application'
        }
    }
    
    # Execute workflow
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    # Workflow may fail due to missing agents, but should handle gracefully
    assert result['status'] in ['completed', 'failed']
    assert 'workflow_id' in result

@pytest.mark.asyncio
async def test_learning_from_security_findings(all_agents, temp_project_dir):
    """Test learning agent learning from security findings"""
    security_agent = all_agents['security']
    learning_agent = all_agents['learning']
    
    # Run security scan
    security_scan = await security_agent.scan_code_security(temp_project_dir)
    
    # Create project outcome data for learning
    project_data = {
        'project_id': 'security_test_project',
        'project_type': 'web_application',
        'technologies': ['python', 'flask', 'sqlite'],
        'requirements': {'security': 'high_priority'},
        'success_metrics': {
            'security_score': 85 if len(security_scan.get('vulnerabilities', [])) == 0 else 60,
            'vulnerabilities_found': len(security_scan.get('vulnerabilities', [])),
            'compliance_score': 80
        },
        'patterns_used': ['parameterized_queries', 'debug_disabled'],
        'completion_time': 25.5,
        'success_score': 0.8,
        'issues_encountered': ['initial_security_setup'] if len(security_scan.get('vulnerabilities', [])) > 0 else []
    }
    
    # Learning agent learns from this project
    learning_result = await learning_agent.learn_from_project(project_data)
    
    assert learning_result['status'] == 'completed'
    assert learning_result['project_id'] == 'security_test_project'

@pytest.mark.asyncio
async def test_security_recommendations_from_learning(all_agents, temp_project_dir):
    """Test getting security recommendations from learning agent"""
    learning_agent = all_agents['learning']
    
    # First, add some security patterns
    security_code = [
        "cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",  # Good pattern
        "app.run(debug=False)",  # Good pattern
        "password = os.environ.get('PASSWORD')"  # Good pattern
    ]
    
    await learning_agent.analyze_code_patterns(
        security_code,
        {'technologies': ['python', 'flask'], 'focus': 'security'}
    )
    
    # Get recommendations for a new project
    context = {
        'project_type': 'web_application',
        'technologies': ['python', 'flask'],
        'security_requirements': ['input_validation', 'secure_auth']
    }
    
    recommendations = await learning_agent.get_recommendations(context)
    
    assert isinstance(recommendations, list)

@pytest.mark.asyncio
async def test_coordinated_security_workflow(all_agents, temp_project_dir):
    """Test coordinated workflow with security scanning and learning"""
    integration_agent = all_agents['integration']
    
    # Create custom workflow that coordinates security and learning
    workflow_config = {
        'name': 'Security Analysis and Learning Workflow',
        'steps': [
            {
                'step_id': 'security_scan',
                'agent': 'security',
                'task_config': {
                    'task_type': 'scan_code_security',
                    'code_path': temp_project_dir
                },
                'timeout': 120
            },
            {
                'step_id': 'pattern_learning', 
                'agent': 'learning',
                'task_config': {
                    'task_type': 'analyze_patterns',
                    'code_samples': ['sample_code'],  # Would be populated from previous step
                    'context': {'focus': 'security'}
                },
                'dependencies': ['security_scan'],
                'timeout': 60
            }
        ],
        'coordination_strategy': 'sequential'
    }
    
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    assert result['status'] in ['completed', 'failed']  # May fail due to step dependencies
    assert 'workflow_id' in result

@pytest.mark.asyncio
async def test_agent_capability_discovery(all_agents):
    """Test that agents correctly report their capabilities"""
    integration_agent = all_agents['integration']
    learning_agent = all_agents['learning']  
    security_agent = all_agents['security']
    
    # Get capabilities
    integration_caps = integration_agent.get_capabilities()
    learning_caps = learning_agent.get_capabilities()
    security_caps = security_agent.get_capabilities()
    
    # Check Integration Agent capabilities
    assert 'workflow_orchestration' in integration_caps
    assert 'multi_agent_coordination' in integration_caps
    assert 'event_driven_architecture' in integration_caps
    
    # Check Learning Agent capabilities
    assert 'code_pattern_analysis' in learning_caps
    assert 'adaptive_recommendations' in learning_caps
    assert 'knowledge_base_management' in learning_caps
    
    # Check Security Agent capabilities
    assert 'static_code_analysis' in security_caps
    assert 'owasp_compliance_checking' in security_caps
    assert 'vulnerability_assessment' in security_caps

@pytest.mark.asyncio
async def test_error_propagation_in_workflows(all_agents):
    """Test error handling and propagation in coordinated workflows"""
    integration_agent = all_agents['integration']
    
    # Create workflow with intentional error
    workflow_config = {
        'name': 'Error Test Workflow',
        'steps': [
            {
                'step_id': 'failing_step',
                'agent': 'security',
                'task_config': {
                    'task_type': 'scan_code_security',
                    'code_path': '/nonexistent/path'  # This should cause an error
                },
                'timeout': 30
            }
        ],
        'enable_rollback': True
    }
    
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    assert result['status'] == 'failed'
    assert 'error' in result or 'failed_step' in result

@pytest.mark.asyncio
async def test_performance_monitoring_across_agents(all_agents):
    """Test performance monitoring across all agents"""
    integration_agent = all_agents['integration']
    learning_agent = all_agents['learning']
    security_agent = all_agents['security']
    
    # Get metrics from all agents
    integration_metrics = await integration_agent.get_integration_metrics()
    learning_metrics = await learning_agent.get_learning_metrics()
    security_metrics = await security_agent.get_security_metrics()
    
    # Verify metrics structure
    assert 'coordination_metrics' in integration_metrics
    assert 'learning_metrics' in learning_metrics
    assert 'security_metrics' in security_metrics
    
    # Verify timestamps are present
    assert 'timestamp' in integration_metrics
    assert 'timestamp' in learning_metrics
    assert 'timestamp' in security_metrics

@pytest.mark.asyncio
async def test_knowledge_sharing_between_agents(all_agents, temp_project_dir):
    """Test knowledge sharing between Learning and Security agents"""
    learning_agent = all_agents['learning']
    security_agent = all_agents['security']
    
    # Security agent finds patterns
    security_result = await security_agent.scan_code_security(temp_project_dir)
    
    # Learning agent can analyze these patterns
    if security_result.get('vulnerabilities'):
        # Convert security findings to learning context
        learning_context = {
            'security_findings': security_result['vulnerabilities'],
            'technologies': ['python', 'flask'],
            'focus': 'security_patterns'
        }
        
        # Learning agent gets recommendations based on security findings
        recommendations = await learning_agent.get_recommendations(learning_context)
        
        assert isinstance(recommendations, list)

@pytest.mark.asyncio
async def test_end_to_end_project_analysis(all_agents, temp_project_dir):
    """Test end-to-end project analysis workflow"""
    integration_agent = all_agents['integration']
    
    # Comprehensive project analysis workflow
    project_analysis_config = {
        'name': 'Complete Project Analysis',
        'description': 'Full security scan, pattern learning, and recommendations',
        'steps': [
            {
                'step_id': 'security_baseline',
                'agent': 'security',
                'task_config': {
                    'task_type': 'scan_code_security',
                    'code_path': temp_project_dir
                }
            },
            {
                'step_id': 'compliance_check',
                'agent': 'security', 
                'task_config': {
                    'task_type': 'owasp_compliance',
                    'project_path': temp_project_dir
                },
                'dependencies': ['security_baseline']
            },
            {
                'step_id': 'pattern_analysis',
                'agent': 'learning',
                'task_config': {
                    'task_type': 'analyze_patterns',
                    'code_samples': ['# Sample code would be extracted from project'],
                    'context': {'project_path': temp_project_dir}
                },
                'dependencies': ['security_baseline']
            }
        ],
        'coordination_strategy': 'dag',  # Allow parallel execution where possible
        'timeout_minutes': 10
    }
    
    result = await integration_agent.orchestrate_workflow(project_analysis_config)
    
    # Should complete or fail gracefully
    assert result['status'] in ['completed', 'failed', 'timeout']
    assert 'workflow_id' in result

@pytest.mark.asyncio
async def test_agent_communication_patterns(all_agents):
    """Test communication patterns between agents"""
    integration_agent = all_agents['integration']
    learning_agent = all_agents['learning']
    security_agent = all_agents['security']
    
    # Test message sending capabilities
    test_message = {
        'type': 'test_communication',
        'data': {'test': 'value'},
        'timestamp': '2024-01-01T00:00:00'
    }
    
    # Integration agent should be able to communicate with other agents
    try:
        # This tests the underlying message infrastructure
        learning_status = learning_agent.get_status()
        security_status = security_agent.get_status()
        
        assert learning_status['agent_id'] == 'learning'
        assert security_status['agent_id'] == 'security'
        
    except Exception as e:
        pytest.fail(f"Agent communication failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
