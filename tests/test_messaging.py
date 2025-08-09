
"""
Test cases for NEXUS messaging system
"""
import pytest
import asyncio
from datetime import datetime
from core.messaging import MessageBus, Message, MessageType, TaskRequest, ProjectPlan

class TestMessage:
    """Test message creation and validation"""
    
    def test_message_creation(self):
        message = Message(
            type=MessageType.TASK_REQUEST,
            from_agent="orchestrator",
            to_agent="frontend",
            content={"test": "data"}
        )
        
        assert message.type == MessageType.TASK_REQUEST
        assert message.from_agent == "orchestrator"
        assert message.to_agent == "frontend"
        assert message.content == {"test": "data"}
        assert message.timestamp is not None

class TestTaskRequest:
    """Test task request model"""
    
    def test_task_request_creation(self):
        task = TaskRequest(
            task_id="test_task",
            task_type="frontend",
            description="Test task",
            requirements={"framework": "react"}
        )
        
        assert task.task_id == "test_task"
        assert task.task_type == "frontend"
        assert task.priority == 1  # default value
        assert task.requirements["framework"] == "react"

class TestProjectPlan:
    """Test project plan model"""
    
    def test_project_plan_creation(self):
        tasks = [
            TaskRequest(
                task_id="task1",
                task_type="frontend",
                description="Frontend task",
                requirements={}
            )
        ]
        
        plan = ProjectPlan(
            project_id="test_project",
            name="Test Project",
            description="Test project description",
            tasks=tasks
        )
        
        assert plan.project_id == "test_project"
        assert plan.name == "Test Project"
        assert len(plan.tasks) == 1
        assert plan.dependencies == {}  # default value

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
