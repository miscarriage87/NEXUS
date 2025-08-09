
"""
Integration Tests for Enhanced Agents (Tasks 4-6)
Test the interaction between all three enhanced agents
"""
import pytest
import asyncio
import tempfile
import os
import json
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.frontend_enhanced import FrontendEnhancedAgent
from agents.backend_enhanced import BackendEnhancedAgent
from agents.devops import DevOpsAgent

class TestEnhancedAgentsIntegration:
    """Integration tests for all three enhanced agents"""
    
    @pytest.fixture
    def agent_config(self):
        return {
            'agents': {
                'frontend': {
                    'model': 'test-model',
                    'technologies': ['react', 'vue', 'angular']
                },
                'backend': {
                    'model': 'test-model', 
                    'technologies': ['fastapi', 'flask', 'django']
                },
                'devops': {
                    'model': 'test-model',
                    'technologies': ['docker', 'kubernetes', 'terraform']
                }
            }
        }
    
    @pytest.fixture
    def all_agents(self, agent_config):
        return {
            'frontend': FrontendEnhancedAgent(agent_config),
            'backend': BackendEnhancedAgent(agent_config),
            'devops': DevOpsAgent(agent_config)
        }
    
    def test_all_agents_initialization(self, all_agents):
        """Test that all agents initialize correctly"""
        assert len(all_agents) == 3
        
        # Check agent IDs
        assert all_agents['frontend'].agent_id == "frontend_enhanced"
        assert all_agents['backend'].agent_id == "backend_enhanced"  
        assert all_agents['devops'].agent_id == "devops"
        
        # Check capabilities are comprehensive
        frontend_caps = all_agents['frontend'].get_capabilities()
        backend_caps = all_agents['backend'].get_capabilities()
        devops_caps = all_agents['devops'].get_capabilities()
        
        assert len(frontend_caps) >= 9  # Should have many capabilities
        assert len(backend_caps) >= 10
        assert len(devops_caps) >= 15
    
    @pytest.mark.asyncio
    async def test_full_stack_application_creation(self, all_agents):
        """Test creating a complete full-stack application with all agents"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define a comprehensive task
            task = {
                "title": "Advanced Todo Application",
                "description": "Full-stack todo app with modern architecture",
                "architecture": {
                    "frontend": "react",
                    "backend": "fastapi",
                    "database": "postgresql"
                },
                "requirements": {
                    "frontend": {
                        "typescript": True,
                        "pwa": True,
                        "state_management": "redux",
                        "css_framework": "tailwind"
                    },
                    "backend": {
                        "graphql": True,
                        "authentication": "jwt",
                        "websockets": True,
                        "api_documentation": True
                    },
                    "devops": {
                        "kubernetes": True,
                        "ci_cd": "github-actions",
                        "monitoring": "prometheus",
                        "infrastructure": "terraform"
                    }
                },
                "output_dir": temp_dir
            }
            
            # Mock LLM client for backend agent
            with patch('agents.backend_enhanced.ollama_client') as mock_backend_client, \
                 patch('agents.frontend_enhanced.ollama_client') as mock_frontend_client:
                
                mock_backend_client.__aenter__ = AsyncMock(return_value=mock_backend_client)
                mock_backend_client.__aexit__ = AsyncMock(return_value=None)
                mock_backend_client.generate = AsyncMock(return_value={'response': '{}'})
                
                mock_frontend_client.__aenter__ = AsyncMock(return_value=mock_frontend_client)
                mock_frontend_client.__aexit__ = AsyncMock(return_value=None)
                mock_frontend_client.generate = AsyncMock(return_value={'response': '{}'})
                
                # Process task with each agent
                frontend_result = await all_agents['frontend'].process_task({
                    **task,
                    "architecture": {"frontend": "react"},
                    "requirements": task["requirements"]["frontend"]
                })
                
                backend_result = await all_agents['backend'].process_task({
                    **task,
                    "architecture": {"backend": "fastapi"},
                    "requirements": task["requirements"]["backend"]
                })
                
                devops_result = await all_agents['devops'].process_task({
                    **task,
                    "requirements": task["requirements"]["devops"]
                })
                
                # Verify all agents completed successfully
                assert frontend_result["status"] == "completed"
                assert backend_result["status"] == "completed"
                assert devops_result["status"] == "completed"
                
                # Check technologies match requirements
                assert frontend_result["technology"] == "React + TypeScript"
                assert frontend_result["css_framework"] == "tailwind"
                assert frontend_result["state_management"] == "redux"
                
                assert backend_result["technology"] == "FastAPI"
                assert backend_result["database"] == "postgresql"
                assert backend_result["authentication"] == "jwt"
                
                assert devops_result["container_platform"] == "docker"
                assert devops_result["orchestrator"] == "kubernetes"
                assert devops_result["ci_cd_platform"] == "github-actions"
                
                # Verify files were created
                assert len(frontend_result["files_created"]) > 10
                assert len(backend_result["files_created"]) > 20
                assert len(devops_result["files_created"]) > 50
    
    def test_agent_compatibility_matrix(self, all_agents):
        """Test that agents are compatible with each other's outputs"""
        # Frontend-Backend compatibility
        frontend_frameworks = all_agents['frontend'].frameworks
        backend_frameworks = all_agents['backend'].frameworks
        
        # Should support all major combinations
        assert "react" in frontend_frameworks
        assert "fastapi" in backend_frameworks
        
        # Backend-DevOps compatibility
        backend_databases = all_agents['backend'].databases
        devops_capabilities = all_agents['devops'].get_capabilities()
        
        assert "postgresql" in backend_databases
        assert "docker_containerization" in devops_capabilities
        assert "kubernetes_manifests" in devops_capabilities
    
    def test_technology_stack_coherence(self, all_agents):
        """Test that generated technology stacks are coherent"""
        # Test React + FastAPI + Docker stack
        frontend_task = {
            "architecture": {"frontend": "react"},
            "requirements": {"typescript": True}
        }
        
        backend_task = {
            "architecture": {"backend": "fastapi"},
            "requirements": {"database": "postgresql"}
        }
        
        devops_task = {
            "requirements": {"docker": True, "kubernetes": True}
        }
        
        # Check framework selections
        frontend_framework = all_agents['frontend']._determine_framework(
            frontend_task["architecture"], frontend_task["requirements"], frontend_task
        )
        backend_framework = all_agents['backend']._determine_framework(
            backend_task["architecture"], backend_task["requirements"], backend_task
        )
        devops_container = all_agents['devops']._determine_container_platform(
            devops_task["requirements"]
        )
        
        assert frontend_framework == "react"
        assert backend_framework == "fastapi"
        assert devops_container == "docker"
        
        # These should work well together
        compatible_stacks = [
            ("react", "fastapi", "docker"),
            ("vue", "flask", "docker"),
            ("angular", "django", "kubernetes")
        ]
        
        assert (frontend_framework, backend_framework, devops_container) in compatible_stacks
    
    @pytest.mark.asyncio
    async def test_error_handling_coordination(self, all_agents):
        """Test error handling across agents"""
        invalid_task = {
            "title": "Invalid Task",
            "output_dir": "/invalid/nonexistent/path",
            "requirements": {}
        }
        
        # All agents should handle errors gracefully
        frontend_result = await all_agents['frontend'].process_task(invalid_task)
        backend_result = await all_agents['backend'].process_task(invalid_task)
        devops_result = await all_agents['devops'].process_task(invalid_task)
        
        assert frontend_result["status"] == "error"
        assert backend_result["status"] == "error"
        assert devops_result["status"] == "error"
        
        # All should return empty file lists on error
        assert frontend_result["files_created"] == []
        assert backend_result["files_created"] == []
        assert devops_result["files_created"] == []
    
    def test_configuration_consistency(self, all_agents):
        """Test that agents use consistent configurations"""
        # All agents should have similar configuration patterns
        frontend_config = all_agents['frontend'].config
        backend_config = all_agents['backend'].config
        devops_config = all_agents['devops'].config
        
        # Should all reference the same config structure
        assert frontend_config == backend_config == devops_config
        
        # Should all have agent-specific configurations
        assert 'agents' in frontend_config
        assert 'frontend' in frontend_config['agents']
        assert 'backend' in backend_config['agents']
        assert 'devops' in devops_config['agents']
    
    def test_feature_coverage_completeness(self, all_agents):
        """Test that all advertised features are covered by agents"""
        # Check Task 4 features (Frontend)
        frontend_caps = all_agents['frontend'].get_capabilities()
        task4_features = [
            "react_development_advanced",
            "typescript_support", 
            "modern_css_frameworks",
            "state_management_implementation",
            "pwa_capabilities",
            "responsive_design",
            "accessibility_features"
        ]
        for feature in task4_features:
            assert feature in frontend_caps
        
        # Check Task 5 features (Backend)
        backend_caps = all_agents['backend'].get_capabilities()
        task5_features = [
            "advanced_fastapi_development",
            "graphql_api_development",
            "authentication_systems",
            "authorization_rbac",
            "api_documentation_generation",
            "microservices_architecture"
        ]
        for feature in task5_features:
            assert feature in backend_caps
        
        # Check Task 6 features (DevOps)
        devops_caps = all_agents['devops'].get_capabilities()
        task6_features = [
            "docker_containerization",
            "kubernetes_manifests",
            "helm_charts",
            "ci_cd_pipeline_generation",
            "terraform_templates",
            "ansible_playbooks",
            "monitoring_setup"
        ]
        for feature in task6_features:
            assert feature in devops_caps
    
    def test_file_structure_integration(self, all_agents):
        """Test that generated file structures integrate well"""
        # Frontend should generate files that work with backend
        frontend_task = {"title": "React App"}
        frontend_files = all_agents['frontend']._get_default_react_files(frontend_task)
        
        # Should have package.json that can connect to backend
        package_json = json.loads(frontend_files["package.json"])
        assert "react" in package_json["dependencies"]
        
        # Backend should generate API that frontend can consume
        backend_task = {"title": "FastAPI Backend"}
        backend_health = all_agents['backend']._get_health_check_file("postgresql")
        
        # Should have CORS enabled and health endpoint
        assert "CORSMiddleware" in backend_health or "/health" in backend_health
        
        # DevOps should containerize both
        devops_task = {"title": "test-app"}
        docker_files = all_agents['devops']._get_docker_files(devops_task)
        
        # Should have Dockerfiles for both frontend and backend
        assert "docker/Dockerfile.frontend" in docker_files
        assert "docker/Dockerfile.backend" in docker_files
        
        # Docker compose should connect them
        docker_compose = docker_files["docker/docker-compose.yml"]
        assert "frontend:" in docker_compose
        assert "backend:" in docker_compose
        assert "depends_on:" in docker_compose
    
    def test_security_consistency(self, all_agents):
        """Test security features are consistently implemented"""
        # Frontend should implement security best practices
        frontend_component = all_agents['frontend']._get_add_todo_component("tailwind", "redux")
        # Should sanitize inputs and use proper form handling
        assert "trim()" in frontend_component  # Input sanitization
        
        # Backend should implement authentication
        backend_auth = all_agents['backend']._get_fastapi_auth_file("jwt")
        assert "verify_password" in backend_auth
        assert "get_password_hash" in backend_auth
        assert "create_access_token" in backend_auth
        
        # DevOps should implement security scanning
        devops_github = all_agents['devops']._get_github_actions_files({"title": "test"})
        ci_cd = devops_github[".github/workflows/ci-cd.yml"]
        assert "trivy" in ci_cd or "security-scan" in ci_cd
        
        # All should use HTTPS/secure connections
        backend_cors = all_agents['backend']._get_fastapi_middleware(["cors"])
        assert "CORSMiddleware" in backend_cors  # Enables secure cross-origin requests
        
        devops_k8s = all_agents['devops']._get_kubernetes_files({"title": "test-app"})
        ingress = devops_k8s["k8s/ingress.yaml"]
        assert "tls:" in ingress  # HTTPS termination
    
    def test_scalability_features(self, all_agents):
        """Test scalability features across all agents"""
        # Frontend should support scalable architectures
        frontend_caps = all_agents['frontend'].get_capabilities()
        assert "component_library_creation" in frontend_caps
        
        # Backend should support microservices
        backend_caps = all_agents['backend'].get_capabilities()
        assert "microservices_architecture" in backend_caps
        
        # DevOps should support auto-scaling
        devops_k8s = all_agents['devops']._get_kubernetes_files({"title": "test-app"})
        assert "k8s/hpa.yaml" in devops_k8s  # Horizontal Pod Autoscaler
        
        hpa = devops_k8s["k8s/hpa.yaml"]
        assert "HorizontalPodAutoscaler" in hpa
        assert "minReplicas:" in hpa
        assert "maxReplicas:" in hpa
    
    def test_monitoring_integration(self, all_agents):
        """Test monitoring and observability integration"""
        # Backend should expose metrics
        backend_health = all_agents['backend']._get_health_check_file("postgresql")
        assert "/health" in backend_health
        
        # DevOps should set up comprehensive monitoring
        devops_monitoring = all_agents['devops']._get_prometheus_grafana_files({"title": "test"})
        
        # Should monitor the application
        prometheus_config = devops_monitoring["monitoring/prometheus-config.yml"]
        assert "backend:8000" in prometheus_config  # Should scrape backend metrics
        
        # Should have comprehensive dashboards
        dashboard = devops_monitoring["monitoring/grafana/dashboards/application-dashboard.json"]
        dashboard_data = json.loads(dashboard)
        assert len(dashboard_data["dashboard"]["panels"]) >= 5  # Multiple monitoring panels
    
    def test_development_to_production_pipeline(self, all_agents):
        """Test complete development to production pipeline"""
        # Should support development workflow
        frontend_package = all_agents['frontend']._get_default_react_files({"title": "Test App"})
        package_json = json.loads(frontend_package["package.json"])
        
        # Should have development and production scripts
        assert "start" in package_json["scripts"]  # Development
        assert "build" in package_json["scripts"]  # Production build
        
        # Backend should have development and production configs
        backend_env = all_agents['backend']._get_env_example("postgresql", "jwt")
        assert "DEBUG=" in backend_env
        
        # DevOps should support staging and production environments
        devops_scripts = all_agents['devops']._get_additional_devops_files({"title": "test"})
        deploy_script = devops_scripts["scripts/deploy.sh"]
        
        assert "staging" in deploy_script
        assert "production" in deploy_script
        assert "ENVIRONMENT=${1:-staging}" in deploy_script
    
    @pytest.mark.asyncio
    async def test_concurrent_agent_execution(self, all_agents):
        """Test that agents can work concurrently without conflicts"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create separate subdirectories for each agent
            frontend_dir = os.path.join(temp_dir, "frontend_output")
            backend_dir = os.path.join(temp_dir, "backend_output")
            devops_dir = os.path.join(temp_dir, "devops_output")
            
            os.makedirs(frontend_dir)
            os.makedirs(backend_dir)
            os.makedirs(devops_dir)
            
            tasks = [
                {
                    "agent": "frontend",
                    "task": {
                        "title": "React App",
                        "architecture": {"frontend": "react"},
                        "output_dir": frontend_dir
                    }
                },
                {
                    "agent": "backend", 
                    "task": {
                        "title": "FastAPI Backend",
                        "architecture": {"backend": "fastapi"},
                        "output_dir": backend_dir
                    }
                },
                {
                    "agent": "devops",
                    "task": {
                        "title": "DevOps Setup",
                        "requirements": {"kubernetes": True},
                        "output_dir": devops_dir
                    }
                }
            ]
            
            # Mock LLM clients
            with patch('agents.backend_enhanced.ollama_client') as mock_backend_client, \
                 patch('agents.frontend_enhanced.ollama_client') as mock_frontend_client:
                
                mock_backend_client.__aenter__ = AsyncMock(return_value=mock_backend_client)
                mock_backend_client.__aexit__ = AsyncMock(return_value=None)
                mock_backend_client.generate = AsyncMock(return_value={'response': '{}'})
                
                mock_frontend_client.__aenter__ = AsyncMock(return_value=mock_frontend_client)
                mock_frontend_client.__aexit__ = AsyncMock(return_value=None)
                mock_frontend_client.generate = AsyncMock(return_value={'response': '{}'})
                
                # Execute all agents concurrently
                results = await asyncio.gather(*[
                    all_agents[task["agent"]].process_task(task["task"])
                    for task in tasks
                ])
                
                # All should complete successfully
                for result in results:
                    assert result["status"] == "completed"
                    assert len(result["files_created"]) > 0
                
                # No conflicts should occur - each should work in its own directory
                assert len(set(result["output_directory"] for result in results)) == 3

