
"""
Base Agent Class - Foundation für alle NEXUS Agents
"""
import json
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.name = name
        self.config = config
        self.status = "idle"
        self.message_queue = asyncio.Queue()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger(f"nexus.{self.agent_id}")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return result"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    async def receive_message(self, message: Dict[str, Any]):
        """Receive message from other agents"""
        await self.message_queue.put(message)
        self.logger.info(f"Received message: {message.get('type', 'unknown')}")
    
    async def send_message(self, target_agent: str, message: Dict[str, Any]):
        """Send message to another agent"""
        message.update({
            "from": self.agent_id,
            "to": target_agent,
            "timestamp": datetime.now().isoformat()
        })
        self.logger.info(f"Sending message to {target_agent}: {message.get('type', 'unknown')}")
        return message
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "capabilities": self.get_capabilities(),
            "timestamp": datetime.now().isoformat()
        }
