
"""Specialized agents for different development tasks"""

# Import all agents for easy access
from .integration_agent import IntegrationAgent
from .learning_agent import LearningAgent
from .security_agent import SecurityAgent

# Import existing agents if they exist
try:
    from .backend_enhanced import BackendEnhancedAgent
    from .frontend_enhanced import FrontendEnhancedAgent
    from .orchestrator_enhanced import EnhancedOrchestratorAgent
except ImportError:
    pass

# Agent registry for easy instantiation
AGENT_REGISTRY = {
    'integration': IntegrationAgent,
    'learning': LearningAgent,
    'security': SecurityAgent,
}

# Try to add existing agents to registry
try:
    AGENT_REGISTRY.update({
        'backend_enhanced': BackendEnhancedAgent,
        'frontend_enhanced': FrontendEnhancedAgent,
        'orchestrator_enhanced': EnhancedOrchestratorAgent,
    })
except NameError:
    pass

def get_agent(agent_type: str, config: dict):
    """Get an agent instance by type"""
    if agent_type in AGENT_REGISTRY:
        return AGENT_REGISTRY[agent_type](config)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

def list_available_agents():
    """List all available agent types"""
    return list(AGENT_REGISTRY.keys())

__all__ = [
    'IntegrationAgent',
    'LearningAgent', 
    'SecurityAgent',
    'AGENT_REGISTRY',
    'get_agent',
    'list_available_agents'
]
