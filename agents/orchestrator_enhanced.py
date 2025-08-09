
"""
Enhanced Orchestrator Agent - Advanced task planning, coordination and resource allocation
"""
import asyncio
import json
import yaml
import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import os
import sys
import heapq
from dataclasses import dataclass, field
from enum import Enum

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.messaging import MessageBus, Message, MessageType, TaskRequest, ProjectPlan
from core.ollama_client import ollama_client

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    DEFERRED = 5

class ResourceType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    AGENT_SLOTS = "agent_slots"

@dataclass
class ResourceAllocation:
    agent_id: str
    resources: Dict[ResourceType, float] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM
    allocated_at: datetime = field(default_factory=datetime.now)
    estimated_duration: timedelta = field(default_factory=lambda: timedelta(hours=1))

@dataclass
class TaskDependency:
    task_id: str
    depends_on: List[str] = field(default_factory=list)
    dependency_type: str = "sequential"  # sequential, parallel, conditional

@dataclass
class CoordinationProtocol:
    protocol_id: str
    agents: List[str]
    coordination_type: str  # synchronous, asynchronous, event_driven
    sync_points: List[str] = field(default_factory=list)
    timeout: timedelta = field(default_factory=lambda: timedelta(minutes=30))

class EnhancedOrchestratorAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("enhanced_orchestrator", "Enhanced Project Orchestrator", config)
        self.message_bus = MessageBus()
        
        # Advanced Project Management
        self.active_projects = {}
        self.project_templates = {}
        self.task_queue = asyncio.PriorityQueue()
        self.dependency_graph = {}
        
        # Agent Management
        self.agents = {}
        self.agent_capabilities = {}
        self.agent_load = {}
        
        # Resource Management
        self.available_resources = {
            ResourceType.CPU: 100.0,
            ResourceType.MEMORY: 100.0,
            ResourceType.DISK: 100.0,
            ResourceType.NETWORK: 100.0,
            ResourceType.AGENT_SLOTS: 10.0
        }
        self.resource_allocations = {}
        
        # Coordination Protocols
        self.coordination_protocols = {}
        self.active_coordinations = {}
        
        # Enhanced Logging
        self.performance_metrics = {}
        self.task_history = []
        
        # Initialize advanced components
        self._initialize_templates()
        self._initialize_metrics()
        
    def get_capabilities(self) -> List[str]:
        return [
            "advanced_project_planning",
            "intelligent_task_coordination",
            "resource_allocation_optimization",
            "multi_agent_protocol_coordination",
            "performance_monitoring",
            "dependency_management",
            "template_based_planning",
            "predictive_scheduling"
        ]
    
    def _initialize_templates(self):
        """Initialize project templates for common patterns"""
        self.project_templates = {
            "web_application": {
                "name": "Full-Stack Web Application",
                "phases": ["analysis", "design", "frontend", "backend", "database", "integration", "testing"],
                "default_dependencies": {
                    "design": ["analysis"],
                    "frontend": ["design"],
                    "backend": ["design", "database"],
                    "integration": ["frontend", "backend"],
                    "testing": ["integration"]
                },
                "resource_estimates": {
                    "analysis": {"cpu": 5, "memory": 10, "duration": 2},
                    "design": {"cpu": 10, "memory": 15, "duration": 4},
                    "frontend": {"cpu": 20, "memory": 25, "duration": 8},
                    "backend": {"cpu": 25, "memory": 30, "duration": 10},
                    "database": {"cpu": 15, "memory": 20, "duration": 4},
                    "integration": {"cpu": 15, "memory": 20, "duration": 6},
                    "testing": {"cpu": 10, "memory": 15, "duration": 4}
                }
            },
            "api_service": {
                "name": "REST API Service",
                "phases": ["analysis", "design", "backend", "database", "testing", "documentation"],
                "default_dependencies": {
                    "design": ["analysis"],
                    "backend": ["design"],
                    "database": ["design"],
                    "testing": ["backend", "database"],
                    "documentation": ["backend", "testing"]
                },
                "resource_estimates": {
                    "analysis": {"cpu": 5, "memory": 10, "duration": 1},
                    "design": {"cpu": 10, "memory": 15, "duration": 3},
                    "backend": {"cpu": 30, "memory": 35, "duration": 12},
                    "database": {"cpu": 20, "memory": 25, "duration": 6},
                    "testing": {"cpu": 15, "memory": 20, "duration": 8},
                    "documentation": {"cpu": 5, "memory": 10, "duration": 2}
                }
            }
        }
    
    def _initialize_metrics(self):
        """Initialize performance metrics tracking"""
        self.performance_metrics = {
            "projects_completed": 0,
            "tasks_completed": 0,
            "average_task_duration": 0,
            "resource_utilization": 0,
            "coordination_efficiency": 0,
            "error_rate": 0,
            "agent_performance": {}
        }
    
    async def advanced_project_planning(self, project_request: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced project planning with templates and AI analysis"""
        project_type = project_request.get('type', 'web_application')
        
        # Use template as base if available
        template = self.project_templates.get(project_type, self.project_templates['web_application'])
        
        # Enhanced LLM analysis with context
        system_prompt = f"""Du bist ein Senior Software-Architekt mit 15+ Jahren Erfahrung. 
        Du verwendest bewährte Projektvorlagen und passt sie intelligent an spezifische Anforderungen an.
        
        Verfügbare Template: {template['name']}
        Standard-Phasen: {', '.join(template['phases'])}
        
        Erweitere und verfeinere den Projektplan basierend auf:
        1. Template-Struktur als Grundlage
        2. Spezifische Projektanforderungen
        3. Ressourcenschätzungen
        4. Abhängigkeiten zwischen Tasks
        5. Kritische Pfade
        6. Risikobewertung
        
        Antworte im JSON-Format mit erweiterter Struktur:
        {{
            "project_name": "Name",
            "description": "Detaillierte Beschreibung",
            "complexity_score": 1-10,
            "estimated_duration_hours": 0,
            "risk_level": "low|medium|high",
            "architecture": {{
                "frontend": "Stack mit Begründung",
                "backend": "Stack mit Begründung", 
                "database": "DB mit Begründung",
                "infrastructure": "Deployment-Strategie"
            }},
            "phases": [
                {{
                    "id": "phase_id",
                    "name": "Phase Name",
                    "description": "Beschreibung",
                    "tasks": [...tasks...],
                    "estimated_hours": 0,
                    "dependencies": ["phase_ids"],
                    "critical_path": true/false
                }}
            ],
            "resource_requirements": {{
                "peak_cpu": 0-100,
                "peak_memory": 0-100,
                "storage_gb": 0,
                "agents_needed": ["agent_types"]
            }},
            "success_criteria": ["Kriterium 1", "Kriterium 2"]
        }}"""
        
        user_prompt = f"""Erstelle einen detaillierten Projektplan:
        
        Projektanforderungen:
        - Typ: {project_request.get('type', 'web_application')}
        - Beschreibung: {project_request.get('description', 'Keine Details')}
        - Technologien: {json.dumps(project_request.get('technologies', {}), indent=2)}
        - Besondere Anforderungen: {json.dumps(project_request.get('requirements', {}), indent=2)}
        - Deadline: {project_request.get('deadline', 'Keine Deadline')}
        - Budget/Zeitrahmen: {project_request.get('timeframe', 'Standard')}
        
        Template-Basis: {json.dumps(template, indent=2)}
        
        Optimiere für maximale Effizienz und Parallelisierung."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('orchestrator', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                plan_text = response.get('response', '{}')
                try:
                    project_plan = json.loads(plan_text)
                    
                    # Validate and enhance plan
                    project_plan = self._validate_and_enhance_plan(project_plan, template)
                    
                except json.JSONDecodeError:
                    self.logger.warning("LLM returned invalid JSON, using enhanced template")
                    project_plan = self._create_enhanced_template_plan(project_request, template)
                
        except Exception as e:
            self.logger.error(f"Error in advanced planning: {str(e)}")
            project_plan = self._create_enhanced_template_plan(project_request, template)
        
        return project_plan
    
    def _validate_and_enhance_plan(self, plan: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enhance AI-generated plan"""
        # Ensure required fields
        if 'phases' not in plan:
            plan['phases'] = []
        if 'resource_requirements' not in plan:
            plan['resource_requirements'] = template['resource_estimates']
        
        # Add task IDs and dependencies if missing
        for phase in plan.get('phases', []):
            if 'id' not in phase:
                phase['id'] = phase.get('name', 'unknown').lower().replace(' ', '_')
            
            for task in phase.get('tasks', []):
                if 'id' not in task:
                    task['id'] = f"{phase['id']}_{task.get('title', 'task').lower().replace(' ', '_')}"
                if 'priority' not in task:
                    task['priority'] = TaskPriority.MEDIUM.value
                if 'estimated_hours' not in task:
                    task['estimated_hours'] = 4  # Default estimate
        
        return plan
    
    def _create_enhanced_template_plan(self, project_request: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced plan from template"""
        project_type = project_request.get('type', 'web_application')
        
        phases = []
        total_duration = 0
        
        for phase_name in template['phases']:
            phase_resources = template['resource_estimates'].get(phase_name, {})
            duration = phase_resources.get('duration', 4)
            total_duration += duration
            
            # Create tasks for this phase
            tasks = self._generate_phase_tasks(phase_name, project_request, phase_resources)
            
            phases.append({
                "id": phase_name,
                "name": phase_name.title(),
                "description": f"{phase_name.title()} phase for {project_type}",
                "tasks": tasks,
                "estimated_hours": duration,
                "dependencies": template['default_dependencies'].get(phase_name, []),
                "critical_path": phase_name in ['backend', 'integration']
            })
        
        return {
            "project_name": f"Enhanced {project_type.title()}",
            "description": project_request.get('description', f"Advanced {project_type} project"),
            "complexity_score": 6,
            "estimated_duration_hours": total_duration,
            "risk_level": "medium",
            "architecture": {
                "frontend": "React with TypeScript",
                "backend": "FastAPI with async support",
                "database": "PostgreSQL with SQLAlchemy",
                "infrastructure": "Docker containerization"
            },
            "phases": phases,
            "resource_requirements": {
                "peak_cpu": 60,
                "peak_memory": 70,
                "storage_gb": 10,
                "agents_needed": ["analyst", "database", "frontend", "backend"]
            },
            "success_criteria": ["All tests pass", "Performance benchmarks met", "Documentation complete"]
        }
    
    def _generate_phase_tasks(self, phase_name: str, project_request: Dict[str, Any], resources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate tasks for a specific phase"""
        phase_task_templates = {
            "analysis": [
                {"title": "Requirements Analysis", "type": "analyst", "description": "Analyze and document requirements"},
                {"title": "Stakeholder Interview", "type": "analyst", "description": "Interview stakeholders for detailed requirements"},
                {"title": "Technical Feasibility", "type": "analyst", "description": "Assess technical feasibility"}
            ],
            "design": [
                {"title": "System Architecture", "type": "analyst", "description": "Design overall system architecture"},
                {"title": "Database Schema", "type": "database", "description": "Design database schema"},
                {"title": "API Specification", "type": "backend", "description": "Define API endpoints and contracts"}
            ],
            "frontend": [
                {"title": "UI/UX Design", "type": "frontend", "description": "Create user interface designs"},
                {"title": "Component Development", "type": "frontend", "description": "Develop reusable components"},
                {"title": "State Management", "type": "frontend", "description": "Implement state management"}
            ],
            "backend": [
                {"title": "API Development", "type": "backend", "description": "Develop REST API endpoints"},
                {"title": "Business Logic", "type": "backend", "description": "Implement core business logic"},
                {"title": "Authentication", "type": "backend", "description": "Implement authentication system"}
            ],
            "database": [
                {"title": "Schema Creation", "type": "database", "description": "Create database schema"},
                {"title": "Migration Scripts", "type": "database", "description": "Create migration scripts"},
                {"title": "Optimization", "type": "database", "description": "Optimize database performance"}
            ]
        }
        
        tasks = []
        task_templates = phase_task_templates.get(phase_name, [{"title": f"{phase_name.title()} Task", "type": "backend", "description": f"Complete {phase_name} phase"}])
        
        for i, template in enumerate(task_templates):
            task_id = f"{phase_name}_{i+1}_{template['title'].lower().replace(' ', '_')}"
            tasks.append({
                "id": task_id,
                "title": template["title"],
                "description": template["description"],
                "type": template["type"],
                "priority": TaskPriority.MEDIUM.value,
                "estimated_hours": resources.get('duration', 4) // len(task_templates),
                "requirements": project_request.get('requirements', {})
            })
        
        return tasks
    
    async def intelligent_resource_allocation(self, project_plan: Dict[str, Any]) -> Dict[str, ResourceAllocation]:
        """Intelligently allocate resources based on project needs and agent capacity"""
        allocations = {}
        
        # Calculate resource needs from project plan
        resource_needs = project_plan.get('resource_requirements', {})
        
        # Get current agent loads
        agent_loads = await self._calculate_agent_loads()
        
        # Allocate resources using optimization algorithm
        for phase in project_plan.get('phases', []):
            for task in phase.get('tasks', []):
                agent_type = task.get('type', 'backend')
                
                # Find best agent for task
                best_agent = await self._find_optimal_agent(agent_type, agent_loads)
                
                if best_agent:
                    # Calculate resource allocation
                    cpu_needed = min(resource_needs.get('peak_cpu', 20), 
                                   self.available_resources[ResourceType.CPU])
                    memory_needed = min(resource_needs.get('peak_memory', 25),
                                      self.available_resources[ResourceType.MEMORY])
                    
                    allocation = ResourceAllocation(
                        agent_id=best_agent,
                        resources={
                            ResourceType.CPU: cpu_needed,
                            ResourceType.MEMORY: memory_needed,
                            ResourceType.AGENT_SLOTS: 1
                        },
                        priority=TaskPriority(task.get('priority', TaskPriority.MEDIUM.value)),
                        estimated_duration=timedelta(hours=task.get('estimated_hours', 4))
                    )
                    
                    allocations[task['id']] = allocation
                    
                    # Update available resources
                    self.available_resources[ResourceType.CPU] -= cpu_needed
                    self.available_resources[ResourceType.MEMORY] -= memory_needed
                    self.available_resources[ResourceType.AGENT_SLOTS] -= 1
                    
                    # Update agent load
                    agent_loads[best_agent] = agent_loads.get(best_agent, 0) + task.get('estimated_hours', 4)
        
        return allocations
    
    async def _calculate_agent_loads(self) -> Dict[str, float]:
        """Calculate current load for each agent"""
        loads = {}
        
        for agent_id, agent in self.agents.items():
            # Get agent status
            status = agent.get_status()
            
            # Calculate load based on active tasks
            current_load = 0
            for project_id, project in self.active_projects.items():
                if project.get('status') == 'executing':
                    for task_id, task_result in project.get('tasks', {}).items():
                        if (task_result.get('agent_id') == agent_id and 
                            task_result.get('status') == 'in_progress'):
                            current_load += task_result.get('estimated_hours', 2)
            
            loads[agent_id] = current_load
            
        return loads
    
    async def _find_optimal_agent(self, agent_type: str, agent_loads: Dict[str, float]) -> Optional[str]:
        """Find the optimal agent for a task based on type and current load"""
        suitable_agents = []
        
        for agent_id, agent in self.agents.items():
            capabilities = agent.get_capabilities()
            
            # Check if agent can handle this task type
            if (agent_type in capabilities or 
                agent_id == agent_type or
                any(capability.startswith(agent_type) for capability in capabilities)):
                
                current_load = agent_loads.get(agent_id, 0)
                suitable_agents.append((agent_id, current_load))
        
        if not suitable_agents:
            return None
        
        # Return agent with lowest current load
        return min(suitable_agents, key=lambda x: x[1])[0]
    
    async def create_coordination_protocol(self, protocol_config: Dict[str, Any]) -> str:
        """Create a multi-agent coordination protocol"""
        protocol_id = str(uuid.uuid4())
        
        protocol = CoordinationProtocol(
            protocol_id=protocol_id,
            agents=protocol_config.get('agents', []),
            coordination_type=protocol_config.get('type', 'asynchronous'),
            sync_points=protocol_config.get('sync_points', []),
            timeout=timedelta(minutes=protocol_config.get('timeout_minutes', 30))
        )
        
        self.coordination_protocols[protocol_id] = protocol
        
        self.logger.info(f"Created coordination protocol: {protocol_id} with {len(protocol.agents)} agents")
        
        return protocol_id
    
    async def execute_with_coordination(self, project_id: str, protocol_id: Optional[str] = None):
        """Execute project with advanced coordination"""
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.active_projects[project_id]
        project["status"] = "coordinating"
        
        # Create coordination protocol if not provided
        if not protocol_id:
            protocol_config = {
                "agents": list(self.agents.keys()),
                "type": "event_driven",
                "sync_points": ["phase_completion", "error_handling"],
                "timeout_minutes": 60
            }
            protocol_id = await self.create_coordination_protocol(protocol_config)
        
        protocol = self.coordination_protocols[protocol_id]
        
        # Start coordinated execution
        self.active_coordinations[project_id] = {
            "protocol_id": protocol_id,
            "started_at": datetime.now(),
            "sync_status": {},
            "event_log": []
        }
        
        project["status"] = "executing"
        
        try:
            # Execute phases with coordination
            plan = project["plan"]
            phases = plan.get('phases', [])
            
            for phase in phases:
                await self._execute_phase_with_coordination(project_id, phase, protocol)
                
                # Wait for sync point if required
                if "phase_completion" in protocol.sync_points:
                    await self._wait_for_sync_point(project_id, f"phase_{phase['id']}_completed")
            
            project["status"] = "completed"
            self.logger.info(f"Project {project_id} completed with coordination")
            
        except Exception as e:
            project["status"] = "failed"
            self.logger.error(f"Project {project_id} failed during coordination: {str(e)}")
            raise
        
        finally:
            # Cleanup coordination
            if project_id in self.active_coordinations:
                del self.active_coordinations[project_id]
    
    async def _execute_phase_with_coordination(self, project_id: str, phase: Dict[str, Any], protocol: CoordinationProtocol):
        """Execute a project phase with coordination"""
        phase_id = phase['id']
        self.logger.info(f"Starting coordinated execution of phase: {phase_id}")
        
        # Check dependencies
        dependencies = phase.get('dependencies', [])
        if dependencies:
            await self._wait_for_dependencies(project_id, dependencies)
        
        # Execute tasks in phase
        tasks = phase.get('tasks', [])
        
        if protocol.coordination_type == "synchronous":
            # Execute tasks sequentially
            for task in tasks:
                await self._execute_task_with_coordination(project_id, task, protocol)
        
        elif protocol.coordination_type == "asynchronous":
            # Execute tasks in parallel
            task_futures = []
            for task in tasks:
                future = asyncio.create_task(
                    self._execute_task_with_coordination(project_id, task, protocol)
                )
                task_futures.append(future)
            
            await asyncio.gather(*task_futures, return_exceptions=True)
        
        # Log phase completion
        coordination = self.active_coordinations[project_id]
        coordination["event_log"].append({
            "event": "phase_completed",
            "phase_id": phase_id,
            "timestamp": datetime.now().isoformat()
        })
    
    async def _execute_task_with_coordination(self, project_id: str, task: Dict[str, Any], protocol: CoordinationProtocol):
        """Execute a single task with coordination"""
        task_id = task["id"]
        agent_type = task.get("type", "backend")
        
        # Find appropriate agent
        agent_id = None
        for aid, agent in self.agents.items():
            if aid == agent_type or agent_type in agent.get_capabilities():
                agent_id = aid
                break
        
        if not agent_id:
            self.logger.error(f"No suitable agent found for task: {task_id}")
            return {"status": "failed", "error": "No suitable agent"}
        
        # Log task start
        coordination = self.active_coordinations[project_id]
        coordination["event_log"].append({
            "event": "task_started",
            "task_id": task_id,
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        })
        
        try:
            # Execute task
            agent = self.agents[agent_id]
            
            demo_output = self.config.get('nexus', {}).get('demo_output', '/home/ubuntu/nexus/demo')
            output_dir = f"{demo_output}/{project_id}"
            os.makedirs(output_dir, exist_ok=True)
            
            task_message = {
                "task_id": task_id,
                "project_id": project_id,
                "title": task["title"],
                "description": task["description"],
                "requirements": task.get("requirements", {}),
                "output_dir": output_dir,
                "architecture": self.active_projects[project_id]["plan"].get("architecture", {}),
                "coordination_context": {
                    "protocol_id": protocol.protocol_id,
                    "sync_points": protocol.sync_points
                }
            }
            
            result = await agent.process_task(task_message)
            
            # Store result
            self.active_projects[project_id]["tasks"][task_id] = result
            
            # Log task completion
            coordination["event_log"].append({
                "event": "task_completed",
                "task_id": task_id,
                "agent_id": agent_id,
                "status": result.get("status", "unknown"),
                "timestamp": datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            # Log task error
            coordination["event_log"].append({
                "event": "task_error",
                "task_id": task_id,
                "agent_id": agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            
            raise
    
    async def _wait_for_sync_point(self, project_id: str, sync_point: str):
        """Wait for a synchronization point"""
        coordination = self.active_coordinations[project_id]
        protocol = self.coordination_protocols[coordination["protocol_id"]]
        
        self.logger.info(f"Waiting for sync point: {sync_point}")
        
        # Wait for all agents to reach sync point (simplified implementation)
        start_time = datetime.now()
        timeout = protocol.timeout
        
        while datetime.now() - start_time < timeout:
            # Check if sync point reached
            recent_events = [
                event for event in coordination["event_log"]
                if sync_point in event.get("event", "")
            ]
            
            if len(recent_events) >= len(protocol.agents):
                self.logger.info(f"Sync point reached: {sync_point}")
                return
            
            await asyncio.sleep(1)
        
        raise TimeoutError(f"Sync point {sync_point} timed out after {timeout}")
    
    async def _wait_for_dependencies(self, project_id: str, dependencies: List[str]):
        """Wait for phase dependencies to complete"""
        self.logger.info(f"Waiting for dependencies: {dependencies}")
        
        project = self.active_projects[project_id]
        
        # Simple dependency check (could be enhanced with more sophisticated logic)
        max_wait = 300  # 5 minutes
        wait_time = 0
        
        while wait_time < max_wait:
            all_ready = True
            
            for dep in dependencies:
                # Check if dependency phase is completed
                dep_completed = any(
                    event.get("event") == "phase_completed" and 
                    event.get("phase_id") == dep
                    for event in self.active_coordinations.get(project_id, {}).get("event_log", [])
                )
                
                if not dep_completed:
                    all_ready = False
                    break
            
            if all_ready:
                return
            
            await asyncio.sleep(5)
            wait_time += 5
        
        raise TimeoutError(f"Dependencies {dependencies} not satisfied within timeout")
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        # Calculate real-time metrics
        total_projects = len(self.active_projects)
        completed_projects = len([p for p in self.active_projects.values() if p.get('status') == 'completed'])
        
        # Resource utilization
        cpu_used = 100 - self.available_resources[ResourceType.CPU]
        memory_used = 100 - self.available_resources[ResourceType.MEMORY]
        
        # Task metrics
        total_tasks = sum(len(p.get('tasks', {})) for p in self.active_projects.values())
        completed_tasks = sum(
            len([t for t in p.get('tasks', {}).values() if t.get('status') == 'completed'])
            for p in self.active_projects.values()
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "projects": {
                "total": total_projects,
                "completed": completed_projects,
                "success_rate": completed_projects / max(total_projects, 1) * 100
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "completion_rate": completed_tasks / max(total_tasks, 1) * 100
            },
            "resources": {
                "cpu_utilization": cpu_used,
                "memory_utilization": memory_used,
                "agent_utilization": (10 - self.available_resources[ResourceType.AGENT_SLOTS]) / 10 * 100
            },
            "coordination": {
                "active_protocols": len(self.active_coordinations),
                "total_protocols_created": len(self.coordination_protocols)
            },
            "agents": {
                "registered": len(self.agents),
                "capabilities": {aid: agent.get_capabilities() for aid, agent in self.agents.items()}
            }
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced task processing with advanced features"""
        try:
            task_type = task.get("task_type", task.get("type", "unknown"))
            
            if task_type in ["create_project", "web_application", "api_service"]:
                # Use advanced planning
                project_plan = await self.advanced_project_planning(task)
                project_id = str(uuid.uuid4())
                
                # Allocate resources
                resource_allocations = await self.intelligent_resource_allocation(project_plan)
                
                # Store project with enhancements
                self.active_projects[project_id] = {
                    "id": project_id,
                    "plan": project_plan,
                    "status": "planned",
                    "created_at": datetime.now().isoformat(),
                    "tasks": {},
                    "resource_allocations": resource_allocations,
                    "metrics": {
                        "planning_time": datetime.now().isoformat(),
                        "complexity_score": project_plan.get('complexity_score', 5)
                    }
                }
                
                # Execute with coordination
                await self.execute_with_coordination(project_id)
                
                # Update metrics
                self.performance_metrics["projects_completed"] += 1
                
                return {
                    "status": "completed",
                    "project_id": project_id,
                    "result": "Enhanced project created and executed successfully",
                    "metrics": await self.get_performance_metrics()
                }
            
            elif task_type == "get_metrics":
                return await self.get_performance_metrics()
            
            elif task_type == "optimize_resources":
                # Trigger resource optimization
                await self._optimize_resources()
                return {"status": "completed", "result": "Resource optimization completed"}
            
            else:
                return {"status": "error", "message": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"Error in enhanced process_task: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _optimize_resources(self):
        """Optimize resource allocation across all active projects"""
        self.logger.info("Starting resource optimization...")
        
        # Collect all active tasks
        all_tasks = []
        for project_id, project in self.active_projects.items():
            if project.get('status') in ['executing', 'planned']:
                for task_id, task_data in project.get('tasks', {}).items():
                    if task_data.get('status') in ['pending', 'in_progress']:
                        all_tasks.append({
                            'project_id': project_id,
                            'task_id': task_id,
                            'task_data': task_data
                        })
        
        # Re-allocate resources based on priority and efficiency
        for task_info in all_tasks:
            project_id = task_info['project_id']
            task_id = task_info['task_id']
            
            # Update resource allocation
            if project_id in self.active_projects:
                allocations = self.active_projects[project_id].get('resource_allocations', {})
                if task_id in allocations:
                    # Adjust allocation based on current system load
                    current_allocation = allocations[task_id]
                    
                    # Optimize CPU allocation
                    if self.available_resources[ResourceType.CPU] < 20:
                        current_allocation.resources[ResourceType.CPU] *= 0.8
                    elif self.available_resources[ResourceType.CPU] > 70:
                        current_allocation.resources[ResourceType.CPU] *= 1.2
                    
                    # Similar optimization for memory
                    if self.available_resources[ResourceType.MEMORY] < 20:
                        current_allocation.resources[ResourceType.MEMORY] *= 0.8
        
        self.logger.info("Resource optimization completed")

