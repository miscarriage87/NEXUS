
"""
Message Protocol für Inter-Agent-Kommunikation
"""
import json
from typing import Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class MessageType(str, Enum):
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    PROJECT_PLAN = "project_plan"
    CODE_GENERATION = "code_generation"
    FILE_OPERATION = "file_operation"
    ERROR = "error"

class Message(BaseModel):
    type: MessageType
    from_agent: str
    to_agent: str
    content: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: str = None

class TaskRequest(BaseModel):
    task_id: str
    task_type: str
    description: str
    requirements: Dict[str, Any]
    priority: int = 1
    deadline: str = None

class TaskResponse(BaseModel):
    task_id: str
    status: str  # "completed", "failed", "in_progress"
    result: Dict[str, Any]
    files_created: List[str] = []
    errors: List[str] = []

class ProjectPlan(BaseModel):
    project_id: str
    name: str
    description: str
    tasks: List[TaskRequest]
    dependencies: Dict[str, List[str]] = {}
    estimated_duration: str = None

class MessageBus:
    def __init__(self):
        self.agents = {}
        self.message_history = []
    
    def register_agent(self, agent_id: str, agent):
        """Register an agent with the message bus"""
        self.agents[agent_id] = agent
    
    async def send_message(self, message: Message):
        """Send message to target agent"""
        self.message_history.append(message)
        
        if message.to_agent in self.agents:
            target_agent = self.agents[message.to_agent]
            await target_agent.receive_message(message.dict())
        else:
            raise ValueError(f"Agent {message.to_agent} not found")
    
    def get_message_history(self, agent_id: str = None) -> List[Message]:
        """Get message history for specific agent or all"""
        if agent_id:
            return [msg for msg in self.message_history 
                   if msg.from_agent == agent_id or msg.to_agent == agent_id]
        return self.message_history

def create_task_request(task_id: str, task_type: str, description: str, 
                       requirements: Dict[str, Any]) -> Message:
    """Helper function to create task request message"""
    return Message(
        type=MessageType.TASK_REQUEST,
        from_agent="orchestrator",
        to_agent="",  # Will be set by orchestrator
        content=TaskRequest(
            task_id=task_id,
            task_type=task_type,
            description=description,
            requirements=requirements
        ).dict()
    )
