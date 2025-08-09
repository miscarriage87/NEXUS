
"""
Tests for Enhanced Orchestrator Agent
"""
import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from agents.orchestrator_enhanced import EnhancedOrchestratorAgent, TaskPriority, ResourceType

class TestEnhancedOrchestrator:
    @pytest.fixture
    def config(self):
        return {
            'agents': {
                'orchestrator': {
                    'model': 'test-model'
                }
            },
            'nexus': {
                'demo_output': '/tmp/test_nexus'
            }
        }
    
    @pytest.fixture
    def orchestrator(self, config):
        return EnhancedOrchestratorAgent(config)
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator.agent_id == "enhanced_orchestrator"
        assert orchestrator.name == "Enhanced Project Orchestrator"
        assert len(orchestrator.project_templates) > 0
        assert ResourceType.CPU in orchestrator.available_resources
        assert len(orchestrator.coordination_protocols) >= 0
    
    def test_capabilities(self, orchestrator):
        """Test orchestrator capabilities"""
        capabilities = orchestrator.get_capabilities()
        assert "advanced_project_planning" in capabilities
        assert "intelligent_task_coordination" in capabilities
        assert "resource_allocation_optimization" in capabilities
        assert "multi_agent_protocol_coordination" in capabilities
    
    @pytest.mark.asyncio
    async def test_advanced_project_planning(self, orchestrator):
        """Test advanced project planning"""
        project_request = {
            "type": "web_application",
            "description": "A todo application with user authentication",
            "technologies": {"frontend": "react", "backend": "fastapi"},
            "requirements": {"users": 1000}
        }
        
        with patch('agents.orchestrator_enhanced.ollama_client') as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.generate = AsyncMock(return_value={
                'response': json.dumps({
                    "project_name": "Enhanced Todo App",
                    "description": "Advanced todo application",
                    "complexity_score": 6,
                    "phases": [
                        {
                            "id": "analysis",
                            "name": "Analysis",
                            "tasks": [{"id": "req_analysis", "title": "Requirements Analysis"}]
                        }
                    ]
                })
            })
            
            result = await orchestrator.advanced_project_planning(project_request)
            
            assert result["project_name"] == "Enhanced Todo App"
            assert "phases" in result
            assert result["complexity_score"] == 6
    
    @pytest.mark.asyncio
    async def test_resource_allocation(self, orchestrator):
        """Test intelligent resource allocation"""
        # Add mock agents
        mock_agent = Mock()
        mock_agent.get_capabilities.return_value = ["backend", "database"]
        mock_agent.get_status.return_value = {"status": "idle"}
        orchestrator.agents = {"backend": mock_agent}
        
        project_plan = {
            "phases": [
                {
                    "id": "backend",
                    "tasks": [
                        {
                            "id": "api_dev",
                            "type": "backend",
                            "priority": 1,
                            "estimated_hours": 8
                        }
                    ]
                }
            ],
            "resource_requirements": {
                "peak_cpu": 30,
                "peak_memory": 40
            }
        }
        
        allocations = await orchestrator.intelligent_resource_allocation(project_plan)
        
        assert "api_dev" in allocations
        allocation = allocations["api_dev"]
        assert allocation.agent_id == "backend"
        assert ResourceType.CPU in allocation.resources
    
    @pytest.mark.asyncio
    async def test_coordination_protocol(self, orchestrator):
        """Test coordination protocol creation"""
        protocol_config = {
            "agents": ["frontend", "backend"],
            "type": "synchronous",
            "sync_points": ["phase_completion"],
            "timeout_minutes": 30
        }
        
        protocol_id = await orchestrator.create_coordination_protocol(protocol_config)
        
        assert protocol_id in orchestrator.coordination_protocols
        protocol = orchestrator.coordination_protocols[protocol_id]
        assert protocol.agents == ["frontend", "backend"]
        assert protocol.coordination_type == "synchronous"
    
    @pytest.mark.asyncio
    async def test_performance_metrics(self, orchestrator):
        """Test performance metrics calculation"""
        # Add some mock project data
        orchestrator.active_projects = {
            "proj1": {
                "status": "completed",
                "tasks": {
                    "task1": {"status": "completed"},
                    "task2": {"status": "completed"}
                }
            },
            "proj2": {
                "status": "executing", 
                "tasks": {
                    "task3": {"status": "in_progress"}
                }
            }
        }
        
        metrics = await orchestrator.get_performance_metrics()
        
        assert "projects" in metrics
        assert "tasks" in metrics
        assert "resources" in metrics
        assert metrics["projects"]["total"] == 2
        assert metrics["projects"]["completed"] == 1

class TestResourceAllocation:
    def test_resource_allocation_creation(self):
        """Test ResourceAllocation dataclass"""
        from agents.orchestrator_enhanced import ResourceAllocation
        from datetime import timedelta
        
        allocation = ResourceAllocation(
            agent_id="test_agent",
            resources={ResourceType.CPU: 50.0, ResourceType.MEMORY: 60.0},
            priority=TaskPriority.HIGH
        )
        
        assert allocation.agent_id == "test_agent"
        assert allocation.resources[ResourceType.CPU] == 50.0
        assert allocation.priority == TaskPriority.HIGH

class TestCoordinationProtocol:
    def test_coordination_protocol_creation(self):
        """Test CoordinationProtocol dataclass"""
        from agents.orchestrator_enhanced import CoordinationProtocol
        from datetime import timedelta
        
        protocol = CoordinationProtocol(
            protocol_id="test_protocol",
            agents=["agent1", "agent2"],
            coordination_type="asynchronous",
            sync_points=["phase_end"],
            timeout=timedelta(minutes=45)
        )
        
        assert protocol.protocol_id == "test_protocol"
        assert len(protocol.agents) == 2
        assert protocol.coordination_type == "asynchronous"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

