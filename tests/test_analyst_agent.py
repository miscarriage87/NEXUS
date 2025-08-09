
"""
Tests for Analyst Agent
"""
import pytest
import asyncio
import json
import os
import tempfile
from unittest.mock import Mock, AsyncMock, patch
from agents.analyst.agent import AnalystAgent, RequirementType, FeasibilityLevel, RiskLevel

class TestAnalystAgent:
    @pytest.fixture
    def config(self):
        return {
            'agents': {
                'analyst': {
                    'model': 'test-model'
                }
            }
        }
    
    @pytest.fixture
    def analyst_agent(self, config):
        return AnalystAgent(config)
    
    def test_initialization(self, analyst_agent):
        """Test analyst agent initialization"""
        assert analyst_agent.agent_id == "analyst"
        assert analyst_agent.name == "Requirements & Architecture Analysis Agent"
        assert len(analyst_agent.requirement_templates) > 0
        assert len(analyst_agent.feasibility_criteria) > 0
        assert len(analyst_agent.architecture_patterns) > 0
    
    def test_capabilities(self, analyst_agent):
        """Test analyst agent capabilities"""
        capabilities = analyst_agent.get_capabilities()
        expected_capabilities = [
            "requirements_analysis",
            "stakeholder_analysis",
            "technical_feasibility_assessment",
            "risk_analysis",
            "architecture_recommendations",
            "technology_stack_selection"
        ]
        
        for capability in expected_capabilities:
            assert capability in capabilities
    
    def test_requirement_templates(self, analyst_agent):
        """Test requirement templates initialization"""
        templates = analyst_agent.requirement_templates
        
        assert "web_application" in templates
        assert "todo_application" in templates
        assert "api_service" in templates
        
        # Test web_application template structure
        web_app = templates["web_application"]
        assert len(web_app) > 0
        
        for category in web_app:
            assert "type" in category
            assert "category" in category
            assert "requirements" in category
            assert isinstance(category["requirements"], list)
    
    def test_feasibility_criteria(self, analyst_agent):
        """Test feasibility criteria initialization"""
        criteria = analyst_agent.feasibility_criteria
        
        assert "technical_complexity" in criteria
        assert "resource_availability" in criteria
        assert "time_constraints" in criteria
        
        # Test structure
        for criterion_name, levels in criteria.items():
            assert isinstance(levels, dict)
            for level_name, level_info in levels.items():
                assert "score" in level_info
                assert "description" in level_info
    
    def test_architecture_patterns(self, analyst_agent):
        """Test architecture patterns initialization"""
        patterns = analyst_agent.architecture_patterns
        
        assert "web_application" in patterns
        
        web_patterns = patterns["web_application"]
        assert "frontend" in web_patterns
        assert "backend" in web_patterns
        assert "database" in web_patterns
        
        # Test frontend patterns
        frontend = web_patterns["frontend"]
        assert "spa" in frontend
        assert "mpa" in frontend
        
        # Test structure
        spa = frontend["spa"]
        assert "technologies" in spa
        assert "pros" in spa
        assert "cons" in spa
        assert "use_cases" in spa
    
    @pytest.mark.asyncio
    async def test_analyze_requirements_with_template(self, analyst_agent):
        """Test requirements analysis using templates"""
        project_description = {
            "type": "todo_application",
            "description": "Simple todo list with user authentication",
            "stakeholders": ["end_users", "product_owner"]
        }
        
        with patch('agents.analyst.agent.ollama_client') as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.generate = AsyncMock(return_value={
                'response': json.dumps({
                    "requirements": [
                        {
                            "id": "REQ-001",
                            "type": "functional",
                            "title": "Create Todo Items",
                            "description": "Users can create new todo items",
                            "priority": 1,
                            "acceptance_criteria": ["User can add todo", "Todo is saved"],
                            "business_value": "Core functionality",
                            "estimated_effort": "medium"
                        }
                    ]
                })
            })
            
            result = await analyst_agent.analyze_requirements(project_description)
            
            assert "requirements" in result
            assert "stakeholder_analysis" in result
            assert "requirement_metrics" in result
            assert result["project_type"] == "todo_application"
            
            requirements = result["requirements"]
            assert len(requirements) > 0
            
            # Should include both AI and template requirements
            req_titles = [req["title"] for req in requirements]
            assert any("todo" in title.lower() for title in req_titles)
    
    def test_apply_requirement_templates(self, analyst_agent):
        """Test application of requirement templates"""
        template_reqs = analyst_agent._apply_requirement_templates("todo_application", "task management app")
        
        assert len(template_reqs) > 0
        
        # Check structure
        for req in template_reqs:
            assert "id" in req
            assert "type" in req
            assert "title" in req
            assert "description" in req
            assert "priority" in req
            assert req["source"] == "template"
    
    def test_merge_requirements(self, analyst_agent):
        """Test merging of AI and template requirements"""
        ai_requirements = [
            {
                "id": "REQ-001",
                "title": "User Authentication",
                "description": "Users can log in",
                "priority": 1
            }
        ]
        
        template_requirements = [
            {
                "id": "REQ-T001",
                "title": "User Registration",
                "description": "Users can register",
                "priority": 2
            },
            {
                "id": "REQ-T002",
                "title": "User Authentication",  # Duplicate
                "description": "Authentication system",
                "priority": 3
            }
        ]
        
        merged = analyst_agent._merge_requirements(ai_requirements, template_requirements)
        
        # Should not include duplicate
        titles = [req["title"] for req in merged]
        assert titles.count("User Authentication") == 1
        assert "User Registration" in titles
    
    def test_identify_missing_requirements(self, analyst_agent):
        """Test identification of missing requirements"""
        requirements = [
            {"title": "User Interface", "description": "Basic UI"},
            {"title": "Data Storage", "description": "Store data"}
        ]
        
        missing = analyst_agent._identify_missing_requirements(requirements, "web_application")
        
        assert len(missing) > 0
        # Should identify missing security, performance, etc.
        missing_text = " ".join(missing).lower()
        assert "security" in missing_text or "performance" in missing_text
    
    def test_calculate_requirement_metrics(self, analyst_agent):
        """Test requirement metrics calculation"""
        requirements = [
            {"type": "functional", "priority": 1, "estimated_effort": "large"},
            {"type": "functional", "priority": 2, "estimated_effort": "medium"},
            {"type": "non_functional", "priority": 1, "estimated_effort": "small"}
        ]
        
        metrics = analyst_agent._calculate_requirement_metrics(requirements)
        
        assert metrics["total"] == 3
        assert metrics["by_type"]["functional"] == 2
        assert metrics["by_type"]["non_functional"] == 1
        assert metrics["by_priority"]["1"] == 2
        assert metrics["high_priority_count"] == 2
        assert "complexity_score" in metrics
    
    def test_calculate_complexity_score(self, analyst_agent):
        """Test complexity score calculation"""
        simple_requirements = [
            {"priority": 3, "estimated_effort": "small"} for _ in range(5)
        ]
        
        complex_requirements = [
            {"priority": 1, "estimated_effort": "extra_large"} for _ in range(30)
        ]
        
        simple_score = analyst_agent._calculate_complexity_score(simple_requirements)
        complex_score = analyst_agent._calculate_complexity_score(complex_requirements)
        
        assert 1.0 <= simple_score <= 10.0
        assert 1.0 <= complex_score <= 10.0
        assert complex_score > simple_score
    
    @pytest.mark.asyncio
    async def test_assess_technical_feasibility(self, analyst_agent):
        """Test technical feasibility assessment"""
        requirements = [
            {
                "id": "REQ-001",
                "type": "functional",
                "title": "Basic CRUD Operations", 
                "priority": 1,
                "estimated_effort": "medium"
            },
            {
                "id": "REQ-002",
                "type": "non_functional",
                "title": "Real-time Synchronization",
                "priority": 1,
                "estimated_effort": "extra_large"
            }
        ]
        
        constraints = {
            "timeline": {"type": "aggressive"},
            "budget": {"level": "limited"},
            "team": {"size": "small"}
        }
        
        with patch('agents.analyst.agent.ollama_client') as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.generate = AsyncMock(return_value={
                'response': json.dumps({
                    "level": "medium",
                    "challenges": ["Complex implementation"],
                    "risks": ["Timeline pressure"],
                    "recommendations": ["Use proven technologies"]
                })
            })
            
            result = await analyst_agent.assess_technical_feasibility(requirements, constraints)
            
            assert "assessments" in result
            assert "feasibility_distribution" in result
            assert "overall_feasibility" in result
            assert "resource_summary" in result
            
            assessments = result["assessments"]
            assert len(assessments) == 2
            
            # Check assessment structure
            for assessment in assessments:
                assert "requirement_id" in assessment
                assert "feasibility_level" in assessment
                assert "technical_challenges" in assessment
    
    def test_rule_based_feasibility(self, analyst_agent):
        """Test rule-based feasibility assessment"""
        requirement = {
            "type": "functional",
            "estimated_effort": "extra_large",
            "priority": 1
        }
        
        constraints = {
            "timeline": {"type": "aggressive"},
            "budget": {"level": "limited"},
            "team": {"size": "small"}
        }
        
        result = analyst_agent._rule_based_feasibility(requirement, constraints)
        
        assert result["level"] == "low"  # Should be low due to constraints
        assert len(result["challenges"]) > 0
        assert "resources" in result
        assert "time_estimate" in result
    
    def test_combine_feasibility_levels(self, analyst_agent):
        """Test combining feasibility levels"""
        # Conservative combination - takes the lower level
        result1 = analyst_agent._combine_feasibility_levels("high", "low")
        assert result1 == "low"
        
        result2 = analyst_agent._combine_feasibility_levels("medium", "high")
        assert result2 == "medium"
        
        result3 = analyst_agent._combine_feasibility_levels("high", "high")
        assert result3 == "high"
    
    def test_calculate_overall_feasibility(self, analyst_agent):
        """Test overall feasibility calculation"""
        from agents.analyst.agent import FeasibilityAssessment
        
        # Mostly high feasibility
        high_assessments = [
            Mock(feasibility_level=FeasibilityLevel.HIGH) for _ in range(8)
        ] + [Mock(feasibility_level=FeasibilityLevel.MEDIUM) for _ in range(2)]
        
        overall = analyst_agent._calculate_overall_feasibility(high_assessments)
        assert overall == "high"
        
        # Many low feasibility
        low_assessments = [
            Mock(feasibility_level=FeasibilityLevel.LOW) for _ in range(3)
        ] + [Mock(feasibility_level=FeasibilityLevel.HIGH) for _ in range(2)]
        
        overall_low = analyst_agent._calculate_overall_feasibility(low_assessments)
        assert overall_low == "low"
    
    def test_analyze_architectural_patterns(self, analyst_agent):
        """Test architectural pattern analysis"""
        requirements = [
            {"title": "Interactive Dashboard", "description": "Real-time data visualization"},
            {"title": "User Authentication", "description": "Secure login system"},
            {"title": "API Endpoints", "description": "RESTful API for data access"}
        ]
        
        patterns = analyst_agent._analyze_architectural_patterns(requirements, "web_application")
        
        assert "frontend" in patterns
        assert "backend" in patterns
        assert "database" in patterns
        
        # Should recommend SPA for interactive requirements
        frontend = patterns["frontend"]
        assert frontend["recommended"] == "spa"
        assert "rationale" in frontend
    
    @pytest.mark.asyncio
    async def test_generate_architecture_recommendations(self, analyst_agent):
        """Test architecture recommendations generation"""
        requirements = [
            {"title": "User Management", "description": "Handle user accounts"},
            {"title": "Data Processing", "description": "Process large datasets"},
            {"title": "API Integration", "description": "Integrate with external APIs"}
        ]
        
        constraints = {
            "project_type": "web_application",
            "team": {"experience": {"react": True, "python": True}},
            "scale": {"expected_users": 5000}
        }
        
        result = await analyst_agent.generate_architecture_recommendations(requirements, constraints)
        
        assert "architectural_patterns" in result
        assert "technology_stack" in result
        assert "deployment_strategy" in result
        assert "security_architecture" in result
        assert "scalability_considerations" in result
        
        # Check technology stack structure
        tech_stack = result["technology_stack"]
        assert "frontend" in tech_stack
        assert "backend" in tech_stack
        assert "database" in tech_stack
        assert "infrastructure" in tech_stack
    
    @pytest.mark.asyncio
    async def test_recommend_technology_stack(self, analyst_agent):
        """Test technology stack recommendations"""
        requirements = []
        constraints = {
            "team": {
                "experience": {
                    "javascript": True,
                    "python": False,
                    "django": True
                }
            },
            "performance": {"level": "high"}
        }
        
        stack = await analyst_agent._recommend_technology_stack(requirements, constraints)
        
        assert "frontend" in stack
        assert "backend" in stack
        
        # Should adjust based on team experience
        frontend = stack["frontend"]
        assert frontend["language"] == "JavaScript"  # Not TypeScript due to experience
    
    @pytest.mark.asyncio
    async def test_process_task_requirements_analysis(self, analyst_agent):
        """Test processing requirements analysis task"""
        task = {
            "title": "Requirements Analysis",
            "description": "Analyze requirements for todo application",
            "requirements": {
                "stakeholders": ["users", "admin"],
                "constraints": {"timeline": {"type": "normal"}}
            },
            "output_dir": "/tmp/test_output"
        }
        
        with patch('agents.analyst.agent.ollama_client') as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.generate = AsyncMock(return_value={
                'response': json.dumps({
                    "requirements": [
                        {
                            "id": "REQ-001",
                            "type": "functional",
                            "title": "Test Requirement",
                            "description": "Test description",
                            "priority": 1,
                            "acceptance_criteria": ["Test criteria"],
                            "business_value": "Test value",
                            "estimated_effort": "medium"
                        }
                    ]
                })
            })
            
            with patch('os.makedirs'):
                with patch('builtins.open', create=True) as mock_open:
                    mock_file = Mock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    
                    result = await analyst_agent.process_task(task)
                    
                    assert result["status"] == "completed"
                    assert "files_created" in result
                    assert "requirements_analysis" in result
                    assert "feasibility_assessment" in result
                    assert "architecture_recommendations" in result
                    assert result["agent_id"] == "analyst"
    
    def test_infer_project_type_from_task(self, analyst_agent):
        """Test project type inference from task"""
        todo_task = {"title": "Todo App Analysis", "description": "Analyze todo application"}
        assert analyst_agent._infer_project_type_from_task(todo_task) == "todo_application"
        
        blog_task = {"title": "Blog System", "description": "Content management system"}
        assert analyst_agent._infer_project_type_from_task(blog_task) == "blog_system"
        
        api_task = {"title": "API Service", "description": "REST API development"}
        assert analyst_agent._infer_project_type_from_task(api_task) == "api_service"
        
        web_task = {"title": "Web Application", "description": "General web app"}
        assert analyst_agent._infer_project_type_from_task(web_task) == "web_application"
    
    def test_generate_requirements_document(self, analyst_agent):
        """Test requirements document generation"""
        analysis = {
            "project_type": "web_application",
            "requirements": [
                {
                    "id": "REQ-001",
                    "type": "functional",
                    "title": "User Login",
                    "description": "Users can log in to the system",
                    "priority": 1,
                    "acceptance_criteria": ["User enters credentials", "System validates"],
                    "business_value": "Security and personalization",
                    "estimated_effort": "medium",
                    "dependencies": []
                }
            ],
            "requirement_metrics": {
                "total": 1,
                "high_priority_count": 1,
                "complexity_score": 5.5,
                "by_type": {"functional": 1},
                "by_priority": {"1": 1}
            },
            "next_steps": ["Define detailed acceptance criteria"]
        }
        
        doc = analyst_agent._generate_requirements_document(analysis)
        
        assert "# Requirements Analysis" in doc
        assert "REQ-001: User Login" in doc
        assert "User enters credentials" in doc
        assert "Next Steps" in doc
        assert "Security and personalization" in doc
    
    def test_generate_feasibility_document(self, analyst_agent):
        """Test feasibility document generation"""
        assessment = {
            "overall_feasibility": "medium",
            "feasibility_distribution": {"high": 2, "medium": 1, "low": 1},
            "resource_summary": {
                "peak_developers_needed": 3,
                "total_development_weeks": 12,
                "estimated_project_duration": "4 weeks"
            },
            "high_risk_requirements": [
                {
                    "requirement_id": "REQ-002",
                    "feasibility_level": "low",
                    "technical_challenges": ["Complex algorithm needed"],
                    "risk_factors": ["Unproven technology"],
                    "recommendations": ["Research alternatives"]
                }
            ],
            "risk_mitigation_strategies": ["Phase implementation", "Get external expertise"]
        }
        
        doc = analyst_agent._generate_feasibility_document(assessment)
        
        assert "# Technical Feasibility Assessment" in doc
        assert "MEDIUM" in doc
        assert "**Peak Developers Needed:** 3" in doc
        assert "REQ-002" in doc
        assert "Complex algorithm needed" in doc
        assert "Risk Mitigation Strategies" in doc

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

