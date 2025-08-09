
"""
Comprehensive tests for Integration Agent
"""
import pytest
import asyncio
import json
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.integration_agent import IntegrationAgent, WorkflowStatus, EventType, WorkflowStep, WorkflowDefinition
from core.base_agent import BaseAgent

class MockAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, f"Mock {agent_id}", {})
        self.process_task_calls = []
    
    async def process_task(self, task):
        self.process_task_calls.append(task)
        return {"status": "completed", "result": f"Mock result from {self.agent_id}"}
    
    def get_capabilities(self):
        return ["mock_capability"]

@pytest.fixture
def integration_config():
    return {
        'agents': {
            'integration': {
                'max_concurrent_workflows': 5,
                'workflow_timeout_minutes': 30,
                'health_check_interval_seconds': 10
            }
        }
    }

@pytest.fixture
def integration_agent(integration_config):
    return IntegrationAgent(integration_config)

@pytest.fixture
def mock_agents():
    agents = {
        'backend': MockAgent('backend'),
        'frontend': MockAgent('frontend'),
        'database': MockAgent('database')
    }
    return agents

@pytest.mark.asyncio
async def test_integration_agent_initialization(integration_agent):
    """Test Integration Agent initialization"""
    assert integration_agent.agent_id == "integration"
    assert integration_agent.name == "Integration Coordinator"
    assert len(integration_agent.workflow_templates) > 0
    assert "full_stack_development" in integration_agent.workflow_templates
    assert len(integration_agent.get_capabilities()) > 10

@pytest.mark.asyncio
async def test_register_agent(integration_agent, mock_agents):
    """Test agent registration"""
    backend_agent = mock_agents['backend']
    
    await integration_agent.register_agent(backend_agent)
    
    assert 'backend' in integration_agent.registered_agents
    assert integration_agent.registered_agents['backend'] == backend_agent
    assert 'backend' in integration_agent.agent_health
    assert integration_agent.agent_health['backend'].status == "healthy"

@pytest.mark.asyncio
async def test_monitor_agent_health(integration_agent, mock_agents):
    """Test agent health monitoring"""
    # Register mock agents
    for agent in mock_agents.values():
        await integration_agent.register_agent(agent)
    
    health_report = await integration_agent.monitor_agent_health()
    
    assert "overall_health" in health_report
    assert "agents" in health_report
    assert len(health_report["agents"]) == len(mock_agents)
    
    for agent_id in mock_agents.keys():
        assert agent_id in health_report["agents"]
        assert "status" in health_report["agents"][agent_id]

@pytest.mark.asyncio
async def test_workflow_from_template(integration_agent, mock_agents):
    """Test creating workflow from template"""
    # Register mock agents
    for agent in mock_agents.values():
        await integration_agent.register_agent(agent)
    
    workflow_config = {
        "template": "full_stack_development",
        "requirements": {"type": "web_app"},
        "project_context": {"name": "test_project"}
    }
    
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    assert result["status"] in ["completed", "failed"]  # May fail due to missing agents
    assert "workflow_id" in result

@pytest.mark.asyncio 
async def test_custom_workflow(integration_agent, mock_agents):
    """Test creating custom workflow"""
    # Register mock agents
    for agent in mock_agents.values():
        await integration_agent.register_agent(agent)
    
    workflow_config = {
        "name": "Custom Test Workflow",
        "steps": [
            {
                "agent": "backend",
                "task_config": {"task_type": "test_task"},
                "timeout": 60
            }
        ],
        "coordination_strategy": "sequential"
    }
    
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    assert result["status"] == "completed"
    assert "workflow_id" in result
    assert "step_results" in result

@pytest.mark.asyncio
async def test_workflow_validation(integration_agent):
    """Test workflow validation"""
    # Test invalid workflow (missing agents)
    steps = [
        WorkflowStep(
            step_id="test_step",
            agent_id="nonexistent_agent",
            task_config={"task": "test"}
        )
    ]
    
    workflow_def = WorkflowDefinition(
        workflow_id="test_workflow",
        name="Test Workflow",
        description="Test",
        steps=steps
    )
    
    validation_result = await integration_agent._validate_workflow(workflow_def)
    
    assert not validation_result["valid"]
    assert len(validation_result["errors"]) > 0

@pytest.mark.asyncio
async def test_circular_dependency_detection(integration_agent):
    """Test circular dependency detection"""
    steps = [
        WorkflowStep("step1", "agent1", {}, dependencies=["step2"]),
        WorkflowStep("step2", "agent2", {}, dependencies=["step1"])
    ]
    
    has_circular = integration_agent._has_circular_dependencies(steps)
    
    assert has_circular == True

@pytest.mark.asyncio
async def test_event_system(integration_agent):
    """Test event emission and handling"""
    # Test event emission
    await integration_agent._emit_event(EventType.WORKFLOW_STARTED, {"test": "data"})
    
    # Check event was stored
    assert len(integration_agent.event_store) > 0
    assert integration_agent.event_store[-1]["event_type"] == EventType.WORKFLOW_STARTED.value

@pytest.mark.asyncio
async def test_integration_testing(integration_agent, mock_agents):
    """Test integration testing functionality"""
    # Register mock agents
    for agent in mock_agents.values():
        await integration_agent.register_agent(agent)
    
    task = {
        "task_type": "integration_testing",
        "test_config": {"comprehensive": True}
    }
    
    result = await integration_agent.process_task(task)
    
    assert result["status"] == "completed"
    assert "test_results" in result
    assert "success_rate" in result["test_results"]

@pytest.mark.asyncio
async def test_get_integration_metrics(integration_agent):
    """Test integration metrics collection"""
    metrics = await integration_agent.get_integration_metrics()
    
    assert "coordination_metrics" in metrics
    assert "active_workflows" in metrics
    assert "registered_agents" in metrics
    assert "timestamp" in metrics

@pytest.mark.asyncio
async def test_workflow_rollback(integration_agent, mock_agents):
    """Test workflow rollback functionality"""
    # This test would require more complex setup to test actual rollback
    # For now, test the rollback method exists and handles empty cases
    
    workflow_def = WorkflowDefinition(
        workflow_id="test_rollback",
        name="Rollback Test",
        description="Test rollback",
        steps=[]
    )
    
    await integration_agent._execute_rollback(workflow_def, {})
    # Should complete without error

@pytest.mark.asyncio
async def test_dependency_graph_building(integration_agent):
    """Test dependency graph construction"""
    steps = [
        WorkflowStep("step1", "agent1", {}, dependencies=[]),
        WorkflowStep("step2", "agent2", {}, dependencies=["step1"]),
        WorkflowStep("step3", "agent3", {}, dependencies=["step1", "step2"])
    ]
    
    graph = integration_agent._build_dependency_graph(steps)
    
    assert "step1" in graph
    assert len(graph["step1"]) == 0  # No dependencies
    assert len(graph["step2"]) == 1  # Depends on step1
    assert len(graph["step3"]) == 2  # Depends on step1 and step2

@pytest.mark.asyncio
async def test_workflow_templates(integration_agent):
    """Test workflow template system"""
    templates = integration_agent.workflow_templates
    
    # Check required templates exist
    assert "full_stack_development" in templates
    assert "api_development" in templates
    assert "security_audit" in templates
    
    # Check template structure
    full_stack = templates["full_stack_development"]
    assert "steps" in full_stack
    assert len(full_stack["steps"]) > 0
    assert all("agent" in step for step in full_stack["steps"])

@pytest.mark.asyncio
async def test_parallel_workflow_execution(integration_agent, mock_agents):
    """Test parallel workflow execution"""
    # Register mock agents
    for agent in mock_agents.values():
        await integration_agent.register_agent(agent)
    
    workflow_config = {
        "name": "Parallel Test Workflow",
        "coordination_strategy": "parallel",
        "steps": [
            {
                "agent": "backend",
                "task_config": {"task_type": "task1"}
            },
            {
                "agent": "frontend", 
                "task_config": {"task_type": "task2"}
            }
        ]
    }
    
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    assert result["status"] == "completed"
    assert "execution_time" in result

@pytest.mark.asyncio
async def test_error_handling(integration_agent):
    """Test error handling in workflows"""
    workflow_config = {
        "name": "Error Test Workflow",
        "steps": [
            {
                "agent": "nonexistent_agent",
                "task_config": {"task_type": "test"}
            }
        ]
    }
    
    result = await integration_agent.orchestrate_workflow(workflow_config)
    
    assert result["status"] == "failed"
    assert "error" in result

@pytest.mark.asyncio
async def test_process_unknown_task(integration_agent):
    """Test handling of unknown task types"""
    task = {"task_type": "unknown_task"}
    
    result = await integration_agent.process_task(task)
    
    assert result["status"] == "error"
    assert "Unknown task type" in result["message"]

if __name__ == "__main__":
    pytest.main([__file__])
