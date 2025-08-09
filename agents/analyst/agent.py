
"""
Analyst Agent - Requirements analysis, feasibility assessment and architecture recommendations
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.base_agent import BaseAgent
from core.ollama_client import ollama_client

class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    USER_STORY = "user_story"

class FeasibilityLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NOT_FEASIBLE = "not_feasible"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Requirement:
    id: str
    type: RequirementType
    title: str
    description: str
    priority: int
    acceptance_criteria: List[str]
    dependencies: List[str]
    estimated_effort: str
    business_value: str

@dataclass
class FeasibilityAssessment:
    requirement_id: str
    feasibility_level: FeasibilityLevel
    technical_challenges: List[str]
    resource_requirements: Dict[str, Any]
    time_estimate: str
    risk_factors: List[str]
    recommendations: List[str]

@dataclass
class ArchitectureRecommendation:
    component: str
    recommendation: str
    rationale: str
    alternatives: List[str]
    trade_offs: Dict[str, Any]
    implementation_guidance: str

class AnalystAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("analyst", "Requirements & Architecture Analysis Agent", config)
        self.requirement_templates = self._initialize_requirement_templates()
        self.feasibility_criteria = self._initialize_feasibility_criteria()
        self.architecture_patterns = self._initialize_architecture_patterns()
        
    def get_capabilities(self) -> List[str]:
        return [
            "requirements_analysis",
            "stakeholder_analysis", 
            "business_process_analysis",
            "technical_feasibility_assessment",
            "risk_analysis",
            "architecture_recommendations",
            "technology_stack_selection",
            "scalability_assessment",
            "performance_analysis",
            "security_assessment",
            "cost_estimation",
            "timeline_planning"
        ]
    
    def _initialize_requirement_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize templates for common requirement types"""
        return {
            "web_application": [
                {
                    "type": RequirementType.FUNCTIONAL,
                    "category": "user_management",
                    "requirements": [
                        "User registration and authentication",
                        "User profile management",
                        "Password reset functionality",
                        "Role-based access control"
                    ]
                },
                {
                    "type": RequirementType.FUNCTIONAL,
                    "category": "core_functionality",
                    "requirements": [
                        "CRUD operations for main entities",
                        "Search and filtering capabilities",
                        "Data validation and error handling",
                        "Responsive user interface"
                    ]
                },
                {
                    "type": RequirementType.NON_FUNCTIONAL,
                    "category": "performance",
                    "requirements": [
                        "Page load time < 3 seconds",
                        "Support 1000+ concurrent users",
                        "99.9% uptime availability",
                        "Mobile responsiveness"
                    ]
                }
            ],
            "todo_application": [
                {
                    "type": RequirementType.FUNCTIONAL,
                    "category": "task_management",
                    "requirements": [
                        "Create, read, update, delete tasks",
                        "Mark tasks as complete/incomplete",
                        "Set task priorities and due dates",
                        "Organize tasks by categories"
                    ]
                },
                {
                    "type": RequirementType.FUNCTIONAL,
                    "category": "user_experience",
                    "requirements": [
                        "Intuitive drag-and-drop interface",
                        "Real-time updates",
                        "Search and filter tasks",
                        "Export task lists"
                    ]
                }
            ],
            "api_service": [
                {
                    "type": RequirementType.FUNCTIONAL,
                    "category": "api_endpoints",
                    "requirements": [
                        "RESTful API design",
                        "CRUD endpoints for resources",
                        "API authentication and authorization",
                        "Request/response validation"
                    ]
                },
                {
                    "type": RequirementType.NON_FUNCTIONAL,
                    "category": "api_quality",
                    "requirements": [
                        "Response time < 200ms",
                        "Rate limiting and throttling",
                        "API versioning strategy",
                        "Comprehensive error handling"
                    ]
                }
            ]
        }
    
    def _initialize_feasibility_criteria(self) -> Dict[str, Dict[str, Any]]:
        """Initialize criteria for feasibility assessment"""
        return {
            "technical_complexity": {
                "simple": {"score": 1, "description": "Standard implementation with well-known patterns"},
                "moderate": {"score": 2, "description": "Some complexity but manageable with experienced team"},
                "complex": {"score": 3, "description": "High complexity requiring specialized expertise"},
                "very_complex": {"score": 4, "description": "Cutting-edge technology or novel approaches"}
            },
            "resource_availability": {
                "readily_available": {"score": 1, "description": "Resources and skills readily available"},
                "available": {"score": 2, "description": "Resources available with some effort"},
                "limited": {"score": 3, "description": "Limited availability, may need external help"},
                "scarce": {"score": 4, "description": "Very limited or expensive to acquire"}
            },
            "time_constraints": {
                "flexible": {"score": 1, "description": "Flexible timeline allows for proper implementation"},
                "reasonable": {"score": 2, "description": "Reasonable timeline with some pressure"},
                "tight": {"score": 3, "description": "Tight timeline requiring careful prioritization"},
                "unrealistic": {"score": 4, "description": "Timeline may be unrealistic for quality delivery"}
            }
        }
    
    def _initialize_architecture_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize architecture patterns and recommendations"""
        return {
            "web_application": {
                "frontend": {
                    "spa": {
                        "technologies": ["React", "Vue.js", "Angular"],
                        "pros": ["Rich user experience", "Fast navigation", "Offline capabilities"],
                        "cons": ["SEO challenges", "Initial load time", "JavaScript dependency"],
                        "use_cases": ["Interactive applications", "Admin dashboards", "Real-time updates"]
                    },
                    "mpa": {
                        "technologies": ["Next.js", "Nuxt.js", "Django templates"],
                        "pros": ["SEO friendly", "Fast initial load", "Progressive enhancement"],
                        "cons": ["More server requests", "Less interactivity", "Complex state management"],
                        "use_cases": ["Content-heavy sites", "E-commerce", "Marketing pages"]
                    }
                },
                "backend": {
                    "monolithic": {
                        "technologies": ["Django", "Rails", "Express.js"],
                        "pros": ["Simple deployment", "ACID transactions", "Easy development"],
                        "cons": ["Scaling challenges", "Technology lock-in", "Single point of failure"],
                        "use_cases": ["Small to medium applications", "Rapid prototyping", "Limited team"]
                    },
                    "microservices": {
                        "technologies": ["FastAPI", "Spring Boot", "Node.js"],
                        "pros": ["Independent scaling", "Technology diversity", "Team autonomy"],
                        "cons": ["Complexity", "Network overhead", "Data consistency"],
                        "use_cases": ["Large applications", "Multiple teams", "Different scaling needs"]
                    }
                },
                "database": {
                    "relational": {
                        "technologies": ["PostgreSQL", "MySQL", "SQLite"],
                        "pros": ["ACID compliance", "Complex queries", "Mature ecosystem"],
                        "cons": ["Scaling limitations", "Schema rigidity", "Performance bottlenecks"],
                        "use_cases": ["Structured data", "Complex relationships", "Transactions"]
                    },
                    "nosql": {
                        "technologies": ["MongoDB", "Redis", "DynamoDB"],
                        "pros": ["Flexible schema", "Horizontal scaling", "High performance"],
                        "cons": ["Limited queries", "Consistency models", "Learning curve"],
                        "use_cases": ["Unstructured data", "High scale", "Rapid development"]
                    }
                }
            }
        }
    
    async def analyze_requirements(self, project_description: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive requirements analysis"""
        self.logger.info("Starting comprehensive requirements analysis")
        
        project_type = project_description.get('type', 'web_application')
        description = project_description.get('description', '')
        stakeholders = project_description.get('stakeholders', [])
        
        # Use AI to extract detailed requirements
        ai_requirements = await self._extract_requirements_with_ai(project_description)
        
        # Apply template-based requirements
        template_requirements = self._apply_requirement_templates(project_type, description)
        
        # Merge and prioritize requirements
        all_requirements = self._merge_requirements(ai_requirements, template_requirements)
        
        # Analyze stakeholder needs
        stakeholder_analysis = await self._analyze_stakeholders(stakeholders, all_requirements)
        
        # Identify missing requirements
        missing_requirements = self._identify_missing_requirements(all_requirements, project_type)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "project_type": project_type,
            "requirements": all_requirements,
            "stakeholder_analysis": stakeholder_analysis,
            "missing_requirements": missing_requirements,
            "requirement_metrics": self._calculate_requirement_metrics(all_requirements),
            "next_steps": self._generate_next_steps(all_requirements)
        }
    
    async def _extract_requirements_with_ai(self, project_description: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use AI to extract requirements from project description"""
        system_prompt = """Du bist ein Senior Business Analyst mit 15+ Jahren Erfahrung. 
        Analysiere die Projektbeschreibung und extrahiere detaillierte Anforderungen.
        
        Kategorisiere Anforderungen in:
        1. Funktionale Anforderungen (was das System tun soll)
        2. Nicht-funktionale Anforderungen (Qualitätsmerkmale)
        3. Business-Anforderungen (Geschäftsziele)
        4. Technische Anforderungen (Constraints)
        5. User Stories (Nutzerperspektive)
        
        Antworte im JSON-Format:
        {
            "requirements": [
                {
                    "id": "REQ-001",
                    "type": "functional|non_functional|business|technical|user_story",
                    "title": "Kurzer Titel",
                    "description": "Detaillierte Beschreibung",
                    "priority": 1-5,
                    "acceptance_criteria": ["Kriterium 1", "Kriterium 2"],
                    "business_value": "Geschäftswert Beschreibung",
                    "estimated_effort": "small|medium|large|extra_large",
                    "dependencies": ["REQ-002"],
                    "risk_level": "low|medium|high"
                }
            ]
        }"""
        
        project_info = json.dumps(project_description, indent=2)
        
        user_prompt = f"""Analysiere dieses Projekt und extrahiere alle Anforderungen:
        
        Projektinformationen:
        {project_info}
        
        Berücksichtige auch:
        - Implizite Anforderungen (Sicherheit, Performance, Usability)
        - Compliance und rechtliche Anforderungen
        - Integrations-Anforderungen
        - Wartbarkeits- und Skalierbarkeits-Anforderungen
        
        Erstelle eine vollständige, priorisierte Liste aller Anforderungen."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('analyst', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                requirements_text = response.get('response', '{}')
                try:
                    result = json.loads(requirements_text)
                    return result.get('requirements', [])
                except json.JSONDecodeError:
                    self.logger.warning("AI returned invalid JSON, using fallback requirements")
                    return self._create_fallback_requirements(project_description)
                    
        except Exception as e:
            self.logger.error(f"Error extracting AI requirements: {str(e)}")
            return self._create_fallback_requirements(project_description)
    
    def _create_fallback_requirements(self, project_description: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create fallback requirements if AI fails"""
        project_type = project_description.get('type', 'web_application')
        
        basic_requirements = [
            {
                "id": "REQ-001",
                "type": "functional",
                "title": "User Interface",
                "description": "Provide intuitive user interface for main functionality",
                "priority": 1,
                "acceptance_criteria": ["UI is responsive", "Navigation is clear"],
                "business_value": "Essential for user adoption",
                "estimated_effort": "medium",
                "dependencies": [],
                "risk_level": "low"
            },
            {
                "id": "REQ-002", 
                "type": "non_functional",
                "title": "Performance",
                "description": "System should respond quickly to user actions",
                "priority": 2,
                "acceptance_criteria": ["Response time < 2 seconds", "Handles 100+ concurrent users"],
                "business_value": "User satisfaction and retention",
                "estimated_effort": "medium",
                "dependencies": ["REQ-001"],
                "risk_level": "medium"
            }
        ]
        
        return basic_requirements
    
    def _apply_requirement_templates(self, project_type: str, description: str) -> List[Dict[str, Any]]:
        """Apply requirement templates based on project type"""
        templates = self.requirement_templates.get(project_type, [])
        template_requirements = []
        
        req_id_counter = 100  # Start template requirements at REQ-100
        
        for template_category in templates:
            req_type = template_category['type']
            category = template_category['category']
            
            for req_text in template_category['requirements']:
                template_requirements.append({
                    "id": f"REQ-T{req_id_counter:03d}",
                    "type": req_type.value,
                    "title": req_text,
                    "description": f"{req_text} - {category} requirement",
                    "priority": 3,  # Medium priority for template requirements
                    "acceptance_criteria": [f"Implement {req_text.lower()}", "Test functionality works correctly"],
                    "business_value": "Standard functionality expected by users",
                    "estimated_effort": "medium",
                    "dependencies": [],
                    "risk_level": "low",
                    "source": "template"
                })
                req_id_counter += 1
        
        return template_requirements
    
    def _merge_requirements(self, ai_requirements: List[Dict[str, Any]], 
                           template_requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge AI-generated and template requirements, removing duplicates"""
        all_requirements = []
        seen_titles = set()
        
        # Add AI requirements first (higher priority)
        for req in ai_requirements:
            title_lower = req.get('title', '').lower()
            if title_lower not in seen_titles:
                all_requirements.append(req)
                seen_titles.add(title_lower)
        
        # Add template requirements if not already covered
        for req in template_requirements:
            title_lower = req.get('title', '').lower()
            # Check if similar requirement already exists
            if not any(title_lower in existing for existing in seen_titles):
                all_requirements.append(req)
                seen_titles.add(title_lower)
        
        # Sort by priority
        return sorted(all_requirements, key=lambda x: x.get('priority', 5))
    
    async def _analyze_stakeholders(self, stakeholders: List[str], requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze stakeholders and their relationship to requirements"""
        stakeholder_analysis = {
            "identified_stakeholders": stakeholders,
            "stakeholder_requirements": {},
            "influence_matrix": {},
            "communication_plan": {}
        }
        
        if not stakeholders:
            stakeholders = ["end_users", "product_owner", "development_team", "system_administrators"]
            stakeholder_analysis["identified_stakeholders"] = stakeholders
        
        # Map requirements to stakeholders
        for stakeholder in stakeholders:
            relevant_reqs = []
            for req in requirements:
                if self._is_requirement_relevant_to_stakeholder(req, stakeholder):
                    relevant_reqs.append(req['id'])
            stakeholder_analysis["stakeholder_requirements"][stakeholder] = relevant_reqs
        
        return stakeholder_analysis
    
    def _is_requirement_relevant_to_stakeholder(self, requirement: Dict[str, Any], stakeholder: str) -> bool:
        """Determine if a requirement is relevant to a stakeholder"""
        req_text = f"{requirement.get('title', '')} {requirement.get('description', '')}".lower()
        
        stakeholder_keywords = {
            "end_users": ["user", "interface", "experience", "usability"],
            "product_owner": ["business", "value", "feature", "functionality"],
            "development_team": ["technical", "implementation", "architecture", "code"],
            "system_administrators": ["security", "performance", "maintenance", "deployment"],
            "management": ["cost", "timeline", "resource", "budget"]
        }
        
        keywords = stakeholder_keywords.get(stakeholder, [])
        return any(keyword in req_text for keyword in keywords)
    
    def _identify_missing_requirements(self, requirements: List[Dict[str, Any]], project_type: str) -> List[str]:
        """Identify commonly missing requirements"""
        missing = []
        
        req_titles = [req.get('title', '').lower() for req in requirements]
        
        # Common missing requirements by category
        essential_categories = {
            "security": ["authentication", "authorization", "encryption", "audit"],
            "performance": ["response time", "scalability", "load handling"],
            "usability": ["accessibility", "user experience", "mobile responsive"],
            "maintenance": ["logging", "monitoring", "error handling", "backup"],
            "compliance": ["data protection", "privacy", "gdpr", "accessibility standards"]
        }
        
        for category, keywords in essential_categories.items():
            category_covered = any(
                any(keyword in title for keyword in keywords)
                for title in req_titles
            )
            
            if not category_covered:
                missing.append(f"Missing {category} requirements - consider adding requirements for {', '.join(keywords)}")
        
        return missing
    
    def _calculate_requirement_metrics(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate metrics for the requirements set"""
        total = len(requirements)
        
        if total == 0:
            return {"total": 0, "by_type": {}, "by_priority": {}, "effort_distribution": {}}
        
        by_type = {}
        by_priority = {}
        by_effort = {}
        
        for req in requirements:
            req_type = req.get('type', 'unknown')
            priority = req.get('priority', 3)
            effort = req.get('estimated_effort', 'medium')
            
            by_type[req_type] = by_type.get(req_type, 0) + 1
            by_priority[str(priority)] = by_priority.get(str(priority), 0) + 1
            by_effort[effort] = by_effort.get(effort, 0) + 1
        
        return {
            "total": total,
            "by_type": by_type,
            "by_priority": by_priority,
            "effort_distribution": by_effort,
            "high_priority_count": by_priority.get('1', 0),
            "complexity_score": self._calculate_complexity_score(requirements)
        }
    
    def _calculate_complexity_score(self, requirements: List[Dict[str, Any]]) -> float:
        """Calculate overall project complexity score (1-10)"""
        if not requirements:
            return 5.0
        
        score = 5.0  # Base score
        
        # Adjust based on number of requirements
        req_count = len(requirements)
        if req_count > 50:
            score += 2
        elif req_count > 20:
            score += 1
        elif req_count < 10:
            score -= 1
        
        # Adjust based on high-priority requirements
        high_priority_count = sum(1 for req in requirements if req.get('priority', 3) <= 2)
        if high_priority_count > req_count * 0.5:
            score += 1
        
        # Adjust based on effort distribution
        large_effort_count = sum(1 for req in requirements if req.get('estimated_effort') in ['large', 'extra_large'])
        if large_effort_count > req_count * 0.3:
            score += 1.5
        
        return min(max(score, 1.0), 10.0)
    
    def _generate_next_steps(self, requirements: List[Dict[str, Any]]) -> List[str]:
        """Generate recommended next steps based on requirements analysis"""
        next_steps = []
        
        high_priority_reqs = [req for req in requirements if req.get('priority', 3) <= 2]
        
        if high_priority_reqs:
            next_steps.append(f"Prioritize implementation of {len(high_priority_reqs)} high-priority requirements")
        
        missing_acceptance_criteria = [req for req in requirements if not req.get('acceptance_criteria')]
        if missing_acceptance_criteria:
            next_steps.append(f"Define acceptance criteria for {len(missing_acceptance_criteria)} requirements")
        
        unclear_requirements = [req for req in requirements if len(req.get('description', '')) < 50]
        if unclear_requirements:
            next_steps.append(f"Clarify and expand {len(unclear_requirements)} requirements with insufficient detail")
        
        next_steps.append("Validate requirements with stakeholders")
        next_steps.append("Create detailed user stories for functional requirements")
        next_steps.append("Perform technical feasibility assessment")
        
        return next_steps
    
    async def assess_technical_feasibility(self, requirements: List[Dict[str, Any]], 
                                         constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """Assess technical feasibility of requirements"""
        self.logger.info("Starting technical feasibility assessment")
        
        constraints = constraints or {}
        assessments = []
        
        for req in requirements:
            assessment = await self._assess_requirement_feasibility(req, constraints)
            assessments.append(assessment)
        
        # Overall feasibility analysis
        feasibility_distribution = {}
        for assessment in assessments:
            level = assessment.feasibility_level.value
            feasibility_distribution[level] = feasibility_distribution.get(level, 0) + 1
        
        # Identify high-risk requirements
        high_risk_reqs = [a for a in assessments if a.feasibility_level in [FeasibilityLevel.LOW, FeasibilityLevel.NOT_FEASIBLE]]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "assessments": [self._assessment_to_dict(a) for a in assessments],
            "feasibility_distribution": feasibility_distribution,
            "high_risk_requirements": [self._assessment_to_dict(a) for a in high_risk_reqs],
            "overall_feasibility": self._calculate_overall_feasibility(assessments),
            "resource_summary": self._summarize_resource_needs(assessments),
            "risk_mitigation_strategies": self._generate_risk_mitigations(high_risk_reqs)
        }
    
    async def _assess_requirement_feasibility(self, requirement: Dict[str, Any], 
                                            constraints: Dict[str, Any]) -> FeasibilityAssessment:
        """Assess feasibility of a single requirement"""
        req_id = requirement.get('id', 'unknown')
        
        # Use AI for detailed feasibility assessment
        feasibility_analysis = await self._ai_feasibility_assessment(requirement, constraints)
        
        # Apply rule-based assessment
        rule_based_assessment = self._rule_based_feasibility(requirement, constraints)
        
        # Combine assessments
        combined_level = self._combine_feasibility_levels(
            feasibility_analysis.get('level', 'medium'),
            rule_based_assessment['level']
        )
        
        return FeasibilityAssessment(
            requirement_id=req_id,
            feasibility_level=FeasibilityLevel(combined_level),
            technical_challenges=feasibility_analysis.get('challenges', []) + rule_based_assessment['challenges'],
            resource_requirements=rule_based_assessment['resources'],
            time_estimate=rule_based_assessment['time_estimate'],
            risk_factors=feasibility_analysis.get('risks', []),
            recommendations=feasibility_analysis.get('recommendations', [])
        )
    
    async def _ai_feasibility_assessment(self, requirement: Dict[str, Any], 
                                        constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to assess requirement feasibility"""
        system_prompt = """Du bist ein Senior Software-Architekt und Technical Lead. 
        Bewerte die technische Machbarkeit von Anforderungen unter Berücksichtigung der gegebenen Constraints.
        
        Analysiere:
        1. Technische Komplexität
        2. Verfügbare Technologien und Tools
        3. Team-Skills und Erfahrung
        4. Zeitrahmen und Ressourcen
        5. Risiken und Herausforderungen
        
        Antworte im JSON-Format:
        {
            "level": "high|medium|low|not_feasible",
            "challenges": ["Herausforderung 1", "Herausforderung 2"],
            "risks": ["Risiko 1", "Risiko 2"],
            "recommendations": ["Empfehlung 1", "Empfehlung 2"],
            "alternative_approaches": ["Alternative 1", "Alternative 2"]
        }"""
        
        req_info = json.dumps(requirement, indent=2)
        constraints_info = json.dumps(constraints, indent=2)
        
        user_prompt = f"""Bewerte die technische Machbarkeit dieser Anforderung:
        
        Anforderung:
        {req_info}
        
        Constraints und Rahmenbedingungen:
        {constraints_info}
        
        Berücksichtige aktuelle Technologie-Standards und Best Practices."""
        
        try:
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('analyst', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                assessment_text = response.get('response', '{}')
                try:
                    return json.loads(assessment_text)
                except json.JSONDecodeError:
                    return {"level": "medium", "challenges": [], "risks": [], "recommendations": []}
                    
        except Exception as e:
            self.logger.error(f"Error in AI feasibility assessment: {str(e)}")
            return {"level": "medium", "challenges": [], "risks": [], "recommendations": []}
    
    def _rule_based_feasibility(self, requirement: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Apply rule-based feasibility assessment"""
        req_type = requirement.get('type', 'functional')
        estimated_effort = requirement.get('estimated_effort', 'medium')
        priority = requirement.get('priority', 3)
        
        # Base feasibility assessment
        base_level = "high"
        challenges = []
        
        # Adjust based on effort
        if estimated_effort == 'extra_large':
            base_level = "low"
            challenges.append("Very high complexity requirement")
        elif estimated_effort == 'large':
            base_level = "medium"
            challenges.append("High complexity implementation needed")
        
        # Adjust based on constraints
        timeline = constraints.get('timeline', {})
        if timeline.get('type') == 'aggressive':
            if base_level == 'high':
                base_level = 'medium'
            else:
                base_level = 'low'
            challenges.append("Aggressive timeline constraint")
        
        budget = constraints.get('budget', {})
        if budget.get('level') == 'limited':
            challenges.append("Limited budget may impact implementation options")
        
        team_size = constraints.get('team', {}).get('size', 'medium')
        if team_size == 'small' and estimated_effort in ['large', 'extra_large']:
            base_level = 'low'
            challenges.append("Small team for complex requirement")
        
        # Resource requirements estimation
        effort_resources = {
            'small': {'developers': 1, 'weeks': 1},
            'medium': {'developers': 2, 'weeks': 3},
            'large': {'developers': 3, 'weeks': 6},
            'extra_large': {'developers': 4, 'weeks': 12}
        }
        
        resources = effort_resources.get(estimated_effort, effort_resources['medium'])
        
        return {
            'level': base_level,
            'challenges': challenges,
            'resources': resources,
            'time_estimate': f"{resources['weeks']} weeks with {resources['developers']} developers"
        }
    
    def _combine_feasibility_levels(self, ai_level: str, rule_level: str) -> str:
        """Combine AI and rule-based feasibility levels"""
        level_scores = {
            'high': 4,
            'medium': 3,
            'low': 2,
            'not_feasible': 1
        }
        
        ai_score = level_scores.get(ai_level, 3)
        rule_score = level_scores.get(rule_level, 3)
        
        # Take the more conservative assessment
        combined_score = min(ai_score, rule_score)
        
        score_to_level = {4: 'high', 3: 'medium', 2: 'low', 1: 'not_feasible'}
        return score_to_level[combined_score]
    
    def _assessment_to_dict(self, assessment: FeasibilityAssessment) -> Dict[str, Any]:
        """Convert FeasibilityAssessment to dictionary"""
        return {
            "requirement_id": assessment.requirement_id,
            "feasibility_level": assessment.feasibility_level.value,
            "technical_challenges": assessment.technical_challenges,
            "resource_requirements": assessment.resource_requirements,
            "time_estimate": assessment.time_estimate,
            "risk_factors": assessment.risk_factors,
            "recommendations": assessment.recommendations
        }
    
    def _calculate_overall_feasibility(self, assessments: List[FeasibilityAssessment]) -> str:
        """Calculate overall project feasibility"""
        if not assessments:
            return "unknown"
        
        level_counts = {}
        for assessment in assessments:
            level = assessment.feasibility_level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        total = len(assessments)
        
        # If more than 20% are not feasible or low, overall is low
        if (level_counts.get('not_feasible', 0) + level_counts.get('low', 0)) / total > 0.2:
            return "low"
        # If more than 70% are high feasibility, overall is high
        elif level_counts.get('high', 0) / total > 0.7:
            return "high"
        else:
            return "medium"
    
    def _summarize_resource_needs(self, assessments: List[FeasibilityAssessment]) -> Dict[str, Any]:
        """Summarize resource needs across all requirements"""
        total_developers = 0
        total_weeks = 0
        
        for assessment in assessments:
            resources = assessment.resource_requirements
            total_developers = max(total_developers, resources.get('developers', 1))
            total_weeks += resources.get('weeks', 2)
        
        return {
            "peak_developers_needed": total_developers,
            "total_development_weeks": total_weeks,
            "estimated_project_duration": f"{total_weeks // total_developers} weeks" if total_developers > 0 else "unknown"
        }
    
    def _generate_risk_mitigations(self, high_risk_assessments: List[FeasibilityAssessment]) -> List[str]:
        """Generate risk mitigation strategies for high-risk requirements"""
        mitigations = []
        
        if not high_risk_assessments:
            return ["No high-risk requirements identified"]
        
        mitigations.append("Consider phased implementation approach for high-risk requirements")
        mitigations.append("Allocate additional time for research and prototyping")
        mitigations.append("Identify alternative implementation approaches")
        mitigations.append("Engage external expertise if needed")
        mitigations.append("Create detailed risk monitoring and contingency plans")
        
        # Specific mitigations based on common challenges
        all_challenges = []
        for assessment in high_risk_assessments:
            all_challenges.extend(assessment.technical_challenges)
        
        if any("complexity" in challenge.lower() for challenge in all_challenges):
            mitigations.append("Break down complex requirements into smaller, manageable components")
        
        if any("timeline" in challenge.lower() for challenge in all_challenges):
            mitigations.append("Negotiate timeline adjustments or scope reduction")
        
        return mitigations
    
    async def generate_architecture_recommendations(self, requirements: List[Dict[str, Any]], 
                                                  constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive architecture recommendations"""
        self.logger.info("Generating architecture recommendations")
        
        constraints = constraints or {}
        project_type = constraints.get('project_type', 'web_application')
        
        # Analyze requirements for architectural patterns
        pattern_analysis = self._analyze_architectural_patterns(requirements, project_type)
        
        # Generate technology stack recommendations
        tech_stack = await self._recommend_technology_stack(requirements, constraints)
        
        # Create deployment and scaling recommendations
        deployment_recommendations = self._generate_deployment_recommendations(requirements, constraints)
        
        # Security architecture recommendations
        security_recommendations = self._generate_security_recommendations(requirements)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "project_type": project_type,
            "architectural_patterns": pattern_analysis,
            "technology_stack": tech_stack,
            "deployment_strategy": deployment_recommendations,
            "security_architecture": security_recommendations,
            "scalability_considerations": self._generate_scalability_recommendations(requirements),
            "integration_recommendations": self._generate_integration_recommendations(requirements),
            "monitoring_and_observability": self._generate_monitoring_recommendations()
        }
    
    def _analyze_architectural_patterns(self, requirements: List[Dict[str, Any]], project_type: str) -> Dict[str, Any]:
        """Analyze requirements to recommend architectural patterns"""
        patterns = self.architecture_patterns.get(project_type, {})
        
        # Analyze requirements for pattern indicators
        req_text = " ".join([
            f"{req.get('title', '')} {req.get('description', '')}"
            for req in requirements
        ]).lower()
        
        recommendations = {}
        
        # Frontend pattern analysis
        if "interactive" in req_text or "real-time" in req_text or "dashboard" in req_text:
            recommendations["frontend"] = {
                "recommended": "spa",
                "rationale": "Interactive requirements suggest Single Page Application",
                "technology": "React or Vue.js"
            }
        elif "seo" in req_text or "content" in req_text or "marketing" in req_text:
            recommendations["frontend"] = {
                "recommended": "mpa",
                "rationale": "SEO and content requirements suggest Multi Page Application",
                "technology": "Next.js or server-side rendering"
            }
        else:
            recommendations["frontend"] = {
                "recommended": "spa",
                "rationale": "Default recommendation for web applications",
                "technology": "React with TypeScript"
            }
        
        # Backend pattern analysis
        if len(requirements) > 50 or "microservice" in req_text or "scale" in req_text:
            recommendations["backend"] = {
                "recommended": "microservices",
                "rationale": "Large scale or explicit microservice requirements",
                "technology": "FastAPI or Spring Boot"
            }
        else:
            recommendations["backend"] = {
                "recommended": "monolithic",
                "rationale": "Appropriate for small to medium applications",
                "technology": "FastAPI or Django"
            }
        
        # Database pattern analysis
        if "nosql" in req_text or "flexible schema" in req_text or "scale" in req_text:
            recommendations["database"] = {
                "recommended": "nosql",
                "rationale": "Scalability or schema flexibility requirements",
                "technology": "MongoDB or PostgreSQL with JSONB"
            }
        else:
            recommendations["database"] = {
                "recommended": "relational",
                "rationale": "Structured data with relationships",
                "technology": "PostgreSQL"
            }
        
        return recommendations
    
    async def _recommend_technology_stack(self, requirements: List[Dict[str, Any]], 
                                        constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend complete technology stack"""
        team_experience = constraints.get('team', {}).get('experience', {})
        performance_reqs = constraints.get('performance', {})
        
        # Base recommendations
        stack = {
            "frontend": {
                "framework": "React",
                "language": "TypeScript",
                "styling": "Tailwind CSS",
                "state_management": "React Context API",
                "testing": "Jest + React Testing Library"
            },
            "backend": {
                "framework": "FastAPI",
                "language": "Python",
                "database_orm": "SQLAlchemy",
                "testing": "pytest",
                "documentation": "OpenAPI/Swagger"
            },
            "database": {
                "primary": "PostgreSQL",
                "caching": "Redis",
                "search": "PostgreSQL Full-Text Search"
            },
            "infrastructure": {
                "containerization": "Docker",
                "orchestration": "Docker Compose",
                "reverse_proxy": "Nginx",
                "monitoring": "Prometheus + Grafana"
            }
        }
        
        # Adjust based on team experience
        if team_experience.get('javascript') and not team_experience.get('typescript'):
            stack["frontend"]["language"] = "JavaScript"
        
        if team_experience.get('django') and not team_experience.get('fastapi'):
            stack["backend"]["framework"] = "Django"
            stack["backend"]["database_orm"] = "Django ORM"
        
        # Adjust based on performance requirements
        if performance_reqs.get('level') == 'high':
            stack["database"]["caching"] = "Redis + Memcached"
            stack["frontend"]["bundler"] = "Vite (for fast builds)"
            stack["backend"]["async"] = "Yes (async/await pattern)"
        
        return stack
    
    def _generate_deployment_recommendations(self, requirements: List[Dict[str, Any]], 
                                           constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deployment and infrastructure recommendations"""
        scale_requirements = constraints.get('scale', {})
        budget = constraints.get('budget', {})
        
        deployment = {
            "strategy": "containerized_deployment",
            "environment_stages": ["development", "staging", "production"],
            "ci_cd": {
                "recommended": True,
                "tools": ["GitHub Actions", "GitLab CI/CD"],
                "automated_testing": True,
                "automated_deployment": True
            }
        }
        
        if budget.get('level') == 'limited':
            deployment.update({
                "hosting": "Single VPS or cloud instance",
                "database": "Managed database service (cost-effective)",
                "cdn": "CloudFlare (free tier)",
                "monitoring": "Basic monitoring with free tools"
            })
        else:
            deployment.update({
                "hosting": "Cloud platform (AWS, GCP, Azure)",
                "database": "Managed database with read replicas",
                "cdn": "Premium CDN service",
                "monitoring": "Comprehensive monitoring suite",
                "backup_strategy": "Automated backups with point-in-time recovery"
            })
        
        if scale_requirements.get('expected_users', 1000) > 10000:
            deployment.update({
                "load_balancing": "Application load balancer",
                "auto_scaling": "Horizontal pod autoscaling",
                "caching_strategy": "Multi-layer caching (CDN, Redis, application)",
                "database_scaling": "Read replicas and connection pooling"
            })
        
        return deployment
    
    def _generate_security_recommendations(self, requirements: List[Dict[str, Any]]) -> List[str]:
        """Generate security architecture recommendations"""
        security_reqs = [req for req in requirements if 
                        'security' in req.get('title', '').lower() or 
                        'auth' in req.get('title', '').lower()]
        
        recommendations = [
            "Implement HTTPS/TLS encryption for all communications",
            "Use JWT tokens for API authentication with proper expiration",
            "Implement input validation and sanitization",
            "Apply principle of least privilege for user permissions",
            "Regular security audits and dependency updates"
        ]
        
        if security_reqs:
            recommendations.extend([
                "Implement comprehensive audit logging",
                "Use secure password hashing (bcrypt or Argon2)",
                "Implement rate limiting and DDoS protection",
                "Regular penetration testing",
                "Security headers (CORS, CSP, etc.)"
            ])
        
        return recommendations
    
    def _generate_scalability_recommendations(self, requirements: List[Dict[str, Any]]) -> List[str]:
        """Generate scalability recommendations"""
        return [
            "Design stateless application architecture",
            "Implement database connection pooling",
            "Use caching strategies (Redis, CDN)",
            "Consider database read replicas for read-heavy workloads",
            "Implement asynchronous processing for heavy operations",
            "Design API with pagination for large datasets",
            "Monitor performance metrics and set up alerting"
        ]
    
    def _generate_integration_recommendations(self, requirements: List[Dict[str, Any]]) -> List[str]:
        """Generate integration recommendations"""
        integration_needs = [req for req in requirements if 
                            'integration' in req.get('title', '').lower() or
                            'api' in req.get('title', '').lower()]
        
        recommendations = [
            "Design RESTful APIs with consistent naming conventions",
            "Implement comprehensive API documentation (OpenAPI/Swagger)",
            "Use standard HTTP status codes and error formats",
            "Implement API versioning strategy"
        ]
        
        if integration_needs:
            recommendations.extend([
                "Consider webhook support for real-time notifications",
                "Implement circuit breakers for external API calls",
                "Use message queues for asynchronous processing",
                "Implement comprehensive logging for integration points"
            ])
        
        return recommendations
    
    def _generate_monitoring_recommendations(self) -> Dict[str, Any]:
        """Generate monitoring and observability recommendations"""
        return {
            "application_monitoring": [
                "Performance metrics (response time, throughput)",
                "Error rates and exception tracking",
                "User behavior analytics",
                "Resource utilization (CPU, memory, disk)"
            ],
            "infrastructure_monitoring": [
                "Server health and uptime",
                "Database performance metrics",
                "Network latency and connectivity",
                "Security events and anomalies"
            ],
            "alerting": [
                "Critical system failures",
                "Performance degradation",
                "Security incidents",
                "Resource threshold breaches"
            ],
            "recommended_tools": [
                "Application: New Relic, DataDog, or Prometheus",
                "Logging: ELK Stack or Fluentd",
                "Error tracking: Sentry",
                "Uptime monitoring: Pingdom or UptimeRobot"
            ]
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process analyst-related tasks"""
        try:
            task_type = task.get("title", "").lower()
            description = task.get("description", "")
            requirements = task.get("requirements", {})
            output_dir = task.get("output_dir", "/tmp")
            
            if "analysis" in task_type or "requirement" in task_type:
                # Perform requirements analysis
                project_description = {
                    "type": self._infer_project_type_from_task(task),
                    "description": description,
                    "stakeholders": requirements.get("stakeholders", []),
                    "constraints": requirements.get("constraints", {})
                }
                
                requirements_analysis = await self.analyze_requirements(project_description)
                
                # Perform feasibility assessment
                feasibility_assessment = await self.assess_technical_feasibility(
                    requirements_analysis["requirements"],
                    requirements.get("constraints", {})
                )
                
                # Generate architecture recommendations
                architecture_recommendations = await self.generate_architecture_recommendations(
                    requirements_analysis["requirements"],
                    requirements.get("constraints", {})
                )
                
                # Write analysis documents
                analysis_files = await self._write_analysis_documents(
                    requirements_analysis,
                    feasibility_assessment,
                    architecture_recommendations,
                    output_dir
                )
                
                return {
                    "status": "completed",
                    "result": "Comprehensive analysis completed successfully",
                    "files_created": analysis_files,
                    "requirements_analysis": requirements_analysis,
                    "feasibility_assessment": feasibility_assessment,
                    "architecture_recommendations": architecture_recommendations,
                    "agent_id": self.agent_id
                }
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown analyst task type: {task_type}",
                    "agent_id": self.agent_id
                }
                
        except Exception as e:
            self.logger.error(f"Error processing analyst task: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "agent_id": self.agent_id
            }
    
    def _infer_project_type_from_task(self, task: Dict[str, Any]) -> str:
        """Infer project type from task description"""
        full_text = f"{task.get('title', '')} {task.get('description', '')}".lower()
        
        if "todo" in full_text or "task management" in full_text:
            return "todo_application"
        elif "blog" in full_text or "cms" in full_text:
            return "blog_system"
        elif "api" in full_text or "service" in full_text:
            return "api_service"
        else:
            return "web_application"
    
    async def _write_analysis_documents(self, requirements_analysis: Dict[str, Any],
                                      feasibility_assessment: Dict[str, Any],
                                      architecture_recommendations: Dict[str, Any],
                                      output_dir: str) -> List[str]:
        """Write analysis documents to files"""
        files_created = []
        
        # Create docs directory
        docs_dir = f"{output_dir}/docs"
        os.makedirs(docs_dir, exist_ok=True)
        
        # Write requirements document
        req_doc = self._generate_requirements_document(requirements_analysis)
        req_file = f"{docs_dir}/requirements_analysis.md"
        with open(req_file, 'w') as f:
            f.write(req_doc)
        files_created.append(req_file)
        
        # Write feasibility assessment
        feasibility_doc = self._generate_feasibility_document(feasibility_assessment)
        feasibility_file = f"{docs_dir}/feasibility_assessment.md"
        with open(feasibility_file, 'w') as f:
            f.write(feasibility_doc)
        files_created.append(feasibility_file)
        
        # Write architecture recommendations
        arch_doc = self._generate_architecture_document(architecture_recommendations)
        arch_file = f"{docs_dir}/architecture_recommendations.md"
        with open(arch_file, 'w') as f:
            f.write(arch_doc)
        files_created.append(arch_file)
        
        # Write summary document
        summary_doc = self._generate_analysis_summary(
            requirements_analysis, feasibility_assessment, architecture_recommendations
        )
        summary_file = f"{docs_dir}/analysis_summary.md"
        with open(summary_file, 'w') as f:
            f.write(summary_doc)
        files_created.append(summary_file)
        
        return files_created
    
    def _generate_requirements_document(self, analysis: Dict[str, Any]) -> str:
        """Generate requirements analysis document"""
        reqs = analysis.get('requirements', [])
        metrics = analysis.get('requirement_metrics', {})
        
        doc = f"""# Requirements Analysis

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Project Type: {analysis.get('project_type', 'Unknown')}

## Executive Summary

Total Requirements: {metrics.get('total', 0)}
High Priority Requirements: {metrics.get('high_priority_count', 0)}
Complexity Score: {metrics.get('complexity_score', 0):.1f}/10

## Requirements Breakdown

### By Type
"""
        
        for req_type, count in metrics.get('by_type', {}).items():
            doc += f"- {req_type.replace('_', ' ').title()}: {count}\n"
        
        doc += "\n### By Priority\n"
        for priority, count in metrics.get('by_priority', {}).items():
            doc += f"- Priority {priority}: {count}\n"
        
        doc += "\n## Detailed Requirements\n\n"
        
        for req in reqs:
            doc += f"""### {req.get('id', 'REQ-XXX')}: {req.get('title', 'Untitled')}

**Type:** {req.get('type', 'unknown').replace('_', ' ').title()}
**Priority:** {req.get('priority', 3)}/5
**Effort:** {req.get('estimated_effort', 'unknown').replace('_', ' ').title()}

**Description:** {req.get('description', 'No description provided')}

**Business Value:** {req.get('business_value', 'Not specified')}

**Acceptance Criteria:**
"""
            for criteria in req.get('acceptance_criteria', []):
                doc += f"- {criteria}\n"
            
            if req.get('dependencies'):
                doc += f"\n**Dependencies:** {', '.join(req.get('dependencies', []))}\n"
            
            doc += "\n---\n\n"
        
        # Add next steps
        next_steps = analysis.get('next_steps', [])
        if next_steps:
            doc += "## Next Steps\n\n"
            for step in next_steps:
                doc += f"- {step}\n"
        
        # Add missing requirements
        missing = analysis.get('missing_requirements', [])
        if missing:
            doc += "\n## Potential Missing Requirements\n\n"
            for item in missing:
                doc += f"- {item}\n"
        
        return doc
    
    def _generate_feasibility_document(self, assessment: Dict[str, Any]) -> str:
        """Generate feasibility assessment document"""
        doc = f"""# Technical Feasibility Assessment

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

**Overall Feasibility:** {assessment.get('overall_feasibility', 'unknown').upper()}

### Feasibility Distribution
"""
        
        distribution = assessment.get('feasibility_distribution', {})
        for level, count in distribution.items():
            doc += f"- {level.replace('_', ' ').title()}: {count} requirements\n"
        
        resource_summary = assessment.get('resource_summary', {})
        doc += f"""
## Resource Summary

- **Peak Developers Needed:** {resource_summary.get('peak_developers_needed', 'Unknown')}
- **Total Development Weeks:** {resource_summary.get('total_development_weeks', 'Unknown')}
- **Estimated Project Duration:** {resource_summary.get('estimated_project_duration', 'Unknown')}

## High-Risk Requirements
"""
        
        high_risk = assessment.get('high_risk_requirements', [])
        if high_risk:
            for risk_req in high_risk:
                doc += f"""
### {risk_req.get('requirement_id', 'Unknown')}

**Feasibility Level:** {risk_req.get('feasibility_level', 'unknown').replace('_', ' ').title()}

**Technical Challenges:**
"""
                for challenge in risk_req.get('technical_challenges', []):
                    doc += f"- {challenge}\n"
                
                doc += "\n**Risk Factors:**\n"
                for risk in risk_req.get('risk_factors', []):
                    doc += f"- {risk}\n"
                
                doc += "\n**Recommendations:**\n"
                for rec in risk_req.get('recommendations', []):
                    doc += f"- {rec}\n"
                
                doc += "\n---\n"
        else:
            doc += "\nNo high-risk requirements identified.\n"
        
        # Add risk mitigation strategies
        mitigations = assessment.get('risk_mitigation_strategies', [])
        if mitigations:
            doc += "\n## Risk Mitigation Strategies\n\n"
            for mitigation in mitigations:
                doc += f"- {mitigation}\n"
        
        return doc
    
    def _generate_architecture_document(self, recommendations: Dict[str, Any]) -> str:
        """Generate architecture recommendations document"""
        doc = f"""# Architecture Recommendations

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Project Type: {recommendations.get('project_type', 'Unknown')}

## Architectural Patterns

"""
        
        patterns = recommendations.get('architectural_patterns', {})
        for component, pattern_info in patterns.items():
            doc += f"""### {component.title()}

**Recommended Pattern:** {pattern_info.get('recommended', 'Unknown')}
**Technology:** {pattern_info.get('technology', 'Not specified')}
**Rationale:** {pattern_info.get('rationale', 'Not provided')}

"""
        
        # Technology Stack
        tech_stack = recommendations.get('technology_stack', {})
        doc += "## Technology Stack\n\n"
        
        for category, technologies in tech_stack.items():
            doc += f"### {category.replace('_', ' ').title()}\n"
            if isinstance(technologies, dict):
                for tech_type, tech_choice in technologies.items():
                    doc += f"- **{tech_type.replace('_', ' ').title()}:** {tech_choice}\n"
            else:
                doc += f"- {technologies}\n"
            doc += "\n"
        
        # Deployment Strategy
        deployment = recommendations.get('deployment_strategy', {})
        doc += f"""## Deployment Strategy

**Strategy:** {deployment.get('strategy', 'Not specified')}

### Environment Stages
"""
        for stage in deployment.get('environment_stages', []):
            doc += f"- {stage.title()}\n"
        
        # CI/CD
        cicd = deployment.get('ci_cd', {})
        if cicd.get('recommended'):
            doc += f"""
### CI/CD Pipeline

- **Automated Testing:** {'Yes' if cicd.get('automated_testing') else 'No'}
- **Automated Deployment:** {'Yes' if cicd.get('automated_deployment') else 'No'}
- **Recommended Tools:** {', '.join(cicd.get('tools', []))}
"""
        
        # Security Architecture
        security = recommendations.get('security_architecture', [])
        if security:
            doc += "\n## Security Architecture\n\n"
            for sec_rec in security:
                doc += f"- {sec_rec}\n"
        
        # Scalability Considerations
        scalability = recommendations.get('scalability_considerations', [])
        if scalability:
            doc += "\n## Scalability Considerations\n\n"
            for scale_rec in scalability:
                doc += f"- {scale_rec}\n"
        
        # Integration Recommendations
        integration = recommendations.get('integration_recommendations', [])
        if integration:
            doc += "\n## Integration Recommendations\n\n"
            for int_rec in integration:
                doc += f"- {int_rec}\n"
        
        # Monitoring
        monitoring = recommendations.get('monitoring_and_observability', {})
        if monitoring:
            doc += "\n## Monitoring and Observability\n\n"
            for category, items in monitoring.items():
                if isinstance(items, list):
                    doc += f"### {category.replace('_', ' ').title()}\n"
                    for item in items:
                        doc += f"- {item}\n"
                    doc += "\n"
        
        return doc
    
    def _generate_analysis_summary(self, requirements_analysis: Dict[str, Any],
                                 feasibility_assessment: Dict[str, Any],
                                 architecture_recommendations: Dict[str, Any]) -> str:
        """Generate comprehensive analysis summary"""
        metrics = requirements_analysis.get('requirement_metrics', {})
        
        doc = f"""# Project Analysis Summary

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

**Project Type:** {requirements_analysis.get('project_type', 'Unknown')}
**Total Requirements:** {metrics.get('total', 0)}
**Complexity Score:** {metrics.get('complexity_score', 0):.1f}/10
**Overall Feasibility:** {feasibility_assessment.get('overall_feasibility', 'unknown').upper()}

## Key Findings

### Requirements Analysis
- {metrics.get('total', 0)} requirements identified across {len(metrics.get('by_type', {}))} categories
- {metrics.get('high_priority_count', 0)} high-priority requirements require immediate attention
- Project complexity rated as {'High' if metrics.get('complexity_score', 0) > 7 else 'Medium' if metrics.get('complexity_score', 0) > 4 else 'Low'}

### Feasibility Assessment
- **Overall Project Feasibility:** {feasibility_assessment.get('overall_feasibility', 'unknown').title()}
- **High-Risk Requirements:** {len(feasibility_assessment.get('high_risk_requirements', []))}
- **Estimated Duration:** {feasibility_assessment.get('resource_summary', {}).get('estimated_project_duration', 'Unknown')}

### Architecture Recommendations
- **Frontend:** {architecture_recommendations.get('architectural_patterns', {}).get('frontend', {}).get('technology', 'Not specified')}
- **Backend:** {architecture_recommendations.get('architectural_patterns', {}).get('backend', {}).get('technology', 'Not specified')}
- **Database:** {architecture_recommendations.get('architectural_patterns', {}).get('database', {}).get('technology', 'Not specified')}

## Risk Assessment

"""
        
        high_risk_count = len(feasibility_assessment.get('high_risk_requirements', []))
        if high_risk_count > 0:
            doc += f"⚠️ **{high_risk_count} high-risk requirements identified** - Immediate attention required\n\n"
        else:
            doc += "✅ **No high-risk requirements identified** - Project appears technically sound\n\n"
        
        doc += """## Recommendations

### Immediate Actions
"""
        
        next_steps = requirements_analysis.get('next_steps', [])[:3]  # Top 3 next steps
        for i, step in enumerate(next_steps, 1):
            doc += f"{i}. {step}\n"
        
        doc += "\n### Risk Mitigation\n"
        mitigations = feasibility_assessment.get('risk_mitigation_strategies', [])[:3]  # Top 3 mitigations
        for i, mitigation in enumerate(mitigations, 1):
            doc += f"{i}. {mitigation}\n"
        
        doc += f"""
## Project Readiness

Based on this analysis, the project is **{feasibility_assessment.get('overall_feasibility', 'unknown').upper()} FEASIBILITY** for implementation.

### Success Factors
- Clear requirements with defined acceptance criteria
- Appropriate technology stack selection
- Comprehensive risk mitigation strategies
- Realistic resource and timeline estimates

### Next Phase
Proceed to detailed design and development planning phase with focus on high-priority requirements.
"""
        
        return doc

