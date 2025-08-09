
"""
Tests for DevOps Agent (Task 6)
"""
import pytest
import asyncio
import tempfile
import os
import yaml
from unittest.mock import Mock, patch

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.devops import DevOpsAgent

class TestDevOpsAgent:
    """Test cases for the DevOps Agent"""
    
    @pytest.fixture
    def agent_config(self):
        return {
            'agents': {
                'devops': {
                    'model': 'test-model',
                    'technologies': ['docker', 'kubernetes', 'terraform']
                }
            }
        }
    
    @pytest.fixture
    def devops_agent(self, agent_config):
        return DevOpsAgent(agent_config)
    
    def test_initialization(self, devops_agent):
        """Test agent initialization"""
        assert devops_agent.agent_id == "devops"
        assert devops_agent.name == "DevOps Engineer"
        assert "docker" in devops_agent.container_platforms
        assert "kubernetes" in devops_agent.orchestrators
        assert "github-actions" in devops_agent.ci_cd_platforms
        assert "terraform" in devops_agent.iac_tools
        assert "prometheus-grafana" in devops_agent.monitoring_stacks
    
    def test_capabilities(self, devops_agent):
        """Test agent capabilities"""
        capabilities = devops_agent.get_capabilities()
        
        expected_capabilities = [
            "docker_containerization",
            "multi_stage_docker_builds",
            "docker_optimization",
            "kubernetes_manifests",
            "helm_charts",
            "ci_cd_pipeline_generation",
            "github_actions_workflows",
            "gitlab_ci_pipelines",
            "jenkins_pipelines",
            "infrastructure_as_code",
            "terraform_templates",
            "ansible_playbooks",
            "monitoring_setup",
            "prometheus_grafana_config",
            "elk_stack_setup"
        ]
        
        for capability in expected_capabilities:
            assert capability in capabilities
    
    def test_determine_container_platform(self, devops_agent):
        """Test container platform determination"""
        # Test Docker detection
        requirements = {"containerization": "docker", "containers": True}
        platform = devops_agent._determine_container_platform(requirements)
        assert platform == "docker"
        
        # Test Podman detection
        requirements = {"container": "podman", "rootless": True}
        platform = devops_agent._determine_container_platform(requirements)
        assert platform == "podman"
        
        # Test default
        platform = devops_agent._determine_container_platform({})
        assert platform == "docker"
    
    def test_determine_orchestrator(self, devops_agent):
        """Test orchestrator determination"""
        # Test Kubernetes detection
        requirements = {"orchestration": "kubernetes", "k8s": True}
        orchestrator = devops_agent._determine_orchestrator(requirements)
        assert orchestrator == "kubernetes"
        
        # Test Docker Swarm detection
        requirements = {"swarm": True, "docker-swarm": True}
        orchestrator = devops_agent._determine_orchestrator(requirements)
        assert orchestrator == "docker-swarm"
        
        # Test default
        orchestrator = devops_agent._determine_orchestrator({})
        assert orchestrator == "kubernetes"
    
    def test_determine_ci_cd_platform(self, devops_agent):
        """Test CI/CD platform determination"""
        # Test GitHub Actions detection
        requirements = {"ci": "github actions", "github": True}
        ci_cd = devops_agent._determine_ci_cd_platform(requirements)
        assert ci_cd == "github-actions"
        
        # Test GitLab CI detection
        requirements = {"pipeline": "gitlab ci", "gitlab": True}
        ci_cd = devops_agent._determine_ci_cd_platform(requirements)
        assert ci_cd == "gitlab-ci"
        
        # Test Jenkins detection
        requirements = {"jenkins": True, "build": "jenkins"}
        ci_cd = devops_agent._determine_ci_cd_platform(requirements)
        assert ci_cd == "jenkins"
        
        # Test default
        ci_cd = devops_agent._determine_ci_cd_platform({})
        assert ci_cd == "github-actions"
    
    def test_determine_iac_tool(self, devops_agent):
        """Test Infrastructure as Code tool determination"""
        # Test Terraform detection
        requirements = {"infrastructure": "terraform", "iac": "terraform"}
        iac = devops_agent._determine_iac_tool(requirements)
        assert iac == "terraform"
        
        # Test Ansible detection
        requirements = {"config": "ansible", "playbooks": True}
        iac = devops_agent._determine_iac_tool(requirements)
        assert iac == "ansible"
        
        # Test default
        iac = devops_agent._determine_iac_tool({})
        assert iac == "terraform"
    
    def test_determine_monitoring_stack(self, devops_agent):
        """Test monitoring stack determination"""
        # Test Prometheus/Grafana detection
        requirements = {"monitoring": "prometheus", "grafana": True}
        monitoring = devops_agent._determine_monitoring_stack(requirements)
        assert monitoring == "prometheus-grafana"
        
        # Test ELK Stack detection
        requirements = {"logging": "elk", "elasticsearch": True}
        monitoring = devops_agent._determine_monitoring_stack(requirements)
        assert monitoring == "elk-stack"
        
        # Test default
        monitoring = devops_agent._determine_monitoring_stack({})
        assert monitoring == "prometheus-grafana"
    
    def test_get_docker_files(self, devops_agent):
        """Test Docker configuration files generation"""
        task = {"title": "Test App"}
        docker_files = devops_agent._get_docker_files(task)
        
        # Check required Docker files
        assert "docker/Dockerfile.frontend" in docker_files
        assert "docker/Dockerfile.backend" in docker_files
        assert "docker/nginx.conf" in docker_files
        assert "docker/docker-compose.yml" in docker_files
        assert "docker/docker-compose.prod.yml" in docker_files
        assert "docker/.dockerignore" in docker_files
        
        # Check Dockerfile content
        backend_dockerfile = docker_files["docker/Dockerfile.backend"]
        assert "FROM python:3.11-slim as builder" in backend_dockerfile
        assert "WORKDIR /app" in backend_dockerfile
        assert "HEALTHCHECK" in backend_dockerfile
        assert "uvicorn main:app" in backend_dockerfile
        
        # Check multi-stage build
        assert "FROM python:3.11-slim as builder" in backend_dockerfile
        assert "FROM python:3.11-slim" in backend_dockerfile
        assert "COPY --from=builder" in backend_dockerfile
    
    def test_get_kubernetes_files(self, devops_agent):
        """Test Kubernetes manifest files generation"""
        task = {"title": "test-app"}
        k8s_files = devops_agent._get_kubernetes_files(task)
        
        # Check required Kubernetes files
        assert "k8s/namespace.yaml" in k8s_files
        assert "k8s/configmap.yaml" in k8s_files
        assert "k8s/secrets.yaml" in k8s_files
        assert "k8s/postgres.yaml" in k8s_files
        assert "k8s/redis.yaml" in k8s_files
        assert "k8s/backend.yaml" in k8s_files
        assert "k8s/frontend.yaml" in k8s_files
        assert "k8s/ingress.yaml" in k8s_files
        assert "k8s/hpa.yaml" in k8s_files
        assert "k8s/network-policy.yaml" in k8s_files
        
        # Check namespace content
        namespace = k8s_files["k8s/namespace.yaml"]
        assert "apiVersion: v1" in namespace
        assert "kind: Namespace" in namespace
        assert "name: test-app" in namespace
        
        # Check deployment content
        backend_deployment = k8s_files["k8s/backend.yaml"]
        assert "apiVersion: apps/v1" in backend_deployment
        assert "kind: Deployment" in backend_deployment
        assert "replicas: 3" in backend_deployment
        assert "livenessProbe:" in backend_deployment
        assert "readinessProbe:" in backend_deployment
        
        # Check HPA content
        hpa = k8s_files["k8s/hpa.yaml"]
        assert "apiVersion: autoscaling/v2" in hpa
        assert "kind: HorizontalPodAutoscaler" in hpa
        assert "minReplicas:" in hpa
        assert "maxReplicas:" in hpa
    
    def test_get_helm_chart_files(self, devops_agent):
        """Test Helm chart files generation"""
        task = {"title": "test-app"}
        helm_files = devops_agent._get_helm_chart_files(task)
        
        # Check required Helm files
        assert "helm/Chart.yaml" in helm_files
        assert "helm/values.yaml" in helm_files
        assert "helm/templates/deployment-frontend.yaml" in helm_files
        assert "helm/templates/_helpers.tpl" in helm_files
        
        # Check Chart.yaml content
        chart_yaml = helm_files["helm/Chart.yaml"]
        chart_data = yaml.safe_load(chart_yaml)
        assert chart_data["name"] == "test-app"
        assert chart_data["type"] == "application"
        assert chart_data["version"] == "0.1.0"
        assert "dependencies" in chart_data
        
        # Check values.yaml content
        values_yaml = helm_files["helm/values.yaml"]
        values_data = yaml.safe_load(values_yaml)
        assert "replicaCount" in values_data
        assert "image" in values_data
        assert "service" in values_data
        assert "ingress" in values_data
        assert "autoscaling" in values_data
        
        # Check template content
        deployment = helm_files["helm/templates/deployment-frontend.yaml"]
        assert "{{ include \"test-app.fullname\" . }}-frontend" in deployment
        assert "{{ .Values.replicaCount.frontend }}" in deployment
    
    def test_get_github_actions_files(self, devops_agent):
        """Test GitHub Actions workflow files generation"""
        task = {"title": "Test App"}
        ga_files = devops_agent._get_github_actions_files(task)
        
        # Check required workflow files
        assert ".github/workflows/ci-cd.yml" in ga_files
        assert ".github/workflows/security-scan.yml" in ga_files
        assert ".github/workflows/performance-test.yml" in ga_files
        
        # Check CI/CD workflow content
        ci_cd = ga_files[".github/workflows/ci-cd.yml"]
        assert "name: CI/CD Pipeline" in ci_cd
        assert "on:" in ci_cd
        assert "jobs:" in ci_cd
        assert "test:" in ci_cd
        assert "build-and-push:" in ci_cd
        assert "deploy:" in ci_cd
        
        # Check services configuration
        assert "postgres:" in ci_cd
        assert "redis:" in ci_cd
        
        # Check security scanning
        assert "trivy-action" in ci_cd
        assert "security-scan:" in ga_files[".github/workflows/security-scan.yml"]
        
        # Check Docker build steps
        assert "docker/build-push-action" in ci_cd
        assert "REGISTRY" in ci_cd
    
    def test_get_gitlab_ci_files(self, devops_agent):
        """Test GitLab CI pipeline files generation"""
        task = {"title": "Test App"}
        gitlab_files = devops_agent._get_gitlab_ci_files(task)
        
        # Check GitLab CI file
        assert ".gitlab-ci.yml" in gitlab_files
        
        gitlab_ci = gitlab_files[".gitlab-ci.yml"]
        assert "stages:" in gitlab_ci
        assert "- test" in gitlab_ci
        assert "- security" in gitlab_ci
        assert "- build" in gitlab_ci
        assert "- deploy" in gitlab_ci
        
        # Check job definitions
        assert "test-backend:" in gitlab_ci
        assert "test-frontend:" in gitlab_ci
        assert "security-scan:" in gitlab_ci
        assert "build-backend:" in gitlab_ci
        assert "deploy-production:" in gitlab_ci
        
        # Check services
        assert "postgres:15" in gitlab_ci
        assert "redis:7" in gitlab_ci
    
    def test_get_jenkins_files(self, devops_agent):
        """Test Jenkins pipeline files generation"""
        task = {"title": "Test App"}
        jenkins_files = devops_agent._get_jenkins_files(task)
        
        # Check Jenkinsfile
        assert "Jenkinsfile" in jenkins_files
        
        jenkinsfile = jenkins_files["Jenkinsfile"]
        assert "pipeline {" in jenkinsfile
        assert "agent any" in jenkinsfile
        assert "environment {" in jenkinsfile
        assert "stages {" in jenkinsfile
        
        # Check stages
        assert "stage('Checkout')" in jenkinsfile
        assert "stage('Test')" in jenkinsfile
        assert "stage('Security Scan')" in jenkinsfile
        assert "stage('Build Images')" in jenkinsfile
        assert "stage('Deploy to Production')" in jenkinsfile
        
        # Check parallel execution
        assert "parallel {" in jenkinsfile
        assert "'Backend Tests'" in jenkinsfile
        assert "'Frontend Tests'" in jenkinsfile
    
    def test_get_terraform_files(self, devops_agent):
        """Test Terraform Infrastructure as Code files generation"""
        task = {"title": "Test App"}
        terraform_files = devops_agent._get_terraform_files(task)
        
        # Check required Terraform files
        assert "terraform/main.tf" in terraform_files
        assert "terraform/variables.tf" in terraform_files
        assert "terraform/eks.tf" in terraform_files
        assert "terraform/addons.tf" in terraform_files
        assert "terraform/outputs.tf" in terraform_files
        
        # Check main.tf content
        main_tf = terraform_files["terraform/main.tf"]
        assert "terraform {" in main_tf
        assert "required_version = \">= 1.0\"" in main_tf
        assert "hashicorp/aws" in main_tf
        assert "hashicorp/kubernetes" in main_tf
        assert "backend \"s3\"" in main_tf
        
        # Check variables.tf content
        variables_tf = terraform_files["terraform/variables.tf"]
        assert "variable \"aws_region\"" in variables_tf
        assert "variable \"cluster_name\"" in variables_tf
        assert "variable \"node_groups\"" in variables_tf
        
        # Check EKS configuration
        eks_tf = terraform_files["terraform/eks.tf"]
        assert "module \"vpc\"" in eks_tf
        assert "module \"eks\"" in eks_tf
        assert "terraform-aws-modules/vpc/aws" in eks_tf
        assert "terraform-aws-modules/eks/aws" in eks_tf
        
        # Check addons
        addons_tf = terraform_files["terraform/addons.tf"]
        assert "aws-load-balancer-controller" in addons_tf
        assert "cert-manager" in addons_tf
        assert "ingress-nginx" in addons_tf
    
    def test_get_ansible_files(self, devops_agent):
        """Test Ansible playbook files generation"""
        task = {"title": "Test App"}
        ansible_files = devops_agent._get_ansible_files(task)
        
        # Check required Ansible files
        assert "ansible/inventory.yml" in ansible_files
        assert "ansible/playbook.yml" in ansible_files
        assert "ansible/templates/docker-compose.yml.j2" in ansible_files
        assert "ansible/group_vars/all.yml" in ansible_files
        
        # Check inventory content
        inventory = yaml.safe_load(ansible_files["ansible/inventory.yml"])
        assert "all" in inventory
        assert "children" in inventory["all"]
        assert "web" in inventory["all"]["children"]
        assert "db" in inventory["all"]["children"]
        
        # Check playbook content
        playbook = ansible_files["ansible/playbook.yml"]
        assert "- name: Deploy Application Infrastructure" in playbook
        assert "hosts: all" in playbook
        assert "- name: Setup Docker" in playbook
        assert "- name: Deploy Web Servers" in playbook
        assert "- name: Setup Database Servers" in playbook
        
        # Check template content
        template = ansible_files["ansible/templates/docker-compose.yml.j2"]
        assert "version: '3.8'" in template
        assert "{{ registry }}/{{ app_name }}" in template
        assert "{{ db_password }}" in template
    
    def test_get_prometheus_grafana_files(self, devops_agent):
        """Test Prometheus and Grafana monitoring files generation"""
        task = {"title": "Test App"}
        monitoring_files = devops_agent._get_prometheus_grafana_files(task)
        
        # Check required monitoring files
        assert "monitoring/prometheus-config.yml" in monitoring_files
        assert "monitoring/alert_rules.yml" in monitoring_files
        assert "monitoring/grafana/dashboards/application-dashboard.json" in monitoring_files
        assert "monitoring/docker-compose.monitoring.yml" in monitoring_files
        
        # Check Prometheus configuration
        prometheus_config = yaml.safe_load(monitoring_files["monitoring/prometheus-config.yml"])
        assert "global" in prometheus_config
        assert "scrape_configs" in prometheus_config
        assert prometheus_config["global"]["scrape_interval"] == "15s"
        
        # Check alert rules
        alert_rules = yaml.safe_load(monitoring_files["monitoring/alert_rules.yml"])
        assert "groups" in alert_rules
        assert len(alert_rules["groups"]) >= 2
        assert "application_alerts" in [group["name"] for group in alert_rules["groups"]]
        assert "kubernetes_alerts" in [group["name"] for group in alert_rules["groups"]]
        
        # Check Grafana dashboard
        dashboard_json = monitoring_files["monitoring/grafana/dashboards/application-dashboard.json"]
        dashboard = json.loads(dashboard_json)
        assert "dashboard" in dashboard
        assert dashboard["dashboard"]["title"] == "Application Monitoring Dashboard"
        assert len(dashboard["dashboard"]["panels"]) > 5
        
        # Check Docker Compose for monitoring
        monitoring_compose = monitoring_files["monitoring/docker-compose.monitoring.yml"]
        assert "prometheus:" in monitoring_compose
        assert "grafana:" in monitoring_compose
        assert "node-exporter:" in monitoring_compose
        assert "alertmanager:" in monitoring_compose
    
    def test_get_elk_stack_files(self, devops_agent):
        """Test ELK Stack logging files generation"""
        task = {"title": "Test App"}
        elk_files = devops_agent._get_elk_stack_files(task)
        
        # Check required ELK files
        assert "logging/docker-compose.elk.yml" in elk_files
        assert "logging/logstash/config/logstash.yml" in elk_files
        assert "logging/logstash/pipeline/logstash.conf" in elk_files
        assert "logging/filebeat/filebeat.yml" in elk_files
        
        # Check ELK Docker Compose
        elk_compose = elk_files["logging/docker-compose.elk.yml"]
        assert "elasticsearch:" in elk_compose
        assert "logstash:" in elk_compose
        assert "kibana:" in elk_compose
        assert "filebeat:" in elk_compose
        
        # Check Logstash configuration
        logstash_config = yaml.safe_load(elk_files["logging/logstash/config/logstash.yml"])
        assert logstash_config["http.host"] == "0.0.0.0"
        
        # Check Logstash pipeline
        logstash_conf = elk_files["logging/logstash/pipeline/logstash.conf"]
        assert "input {" in logstash_conf
        assert "filter {" in logstash_conf
        assert "output {" in logstash_conf
        assert "beats {" in logstash_conf
        assert "elasticsearch {" in logstash_conf
        
        # Check Filebeat configuration
        filebeat_config = yaml.safe_load(elk_files["logging/filebeat/filebeat.yml"])
        assert "filebeat.inputs" in filebeat_config
        assert filebeat_config["filebeat.inputs"][0]["type"] == "container"
    
    def test_get_additional_devops_files(self, devops_agent):
        """Test additional DevOps utility files generation"""
        task = {"title": "Test App"}
        additional_files = devops_agent._get_additional_devops_files(task)
        
        # Check required utility files
        assert "scripts/deploy.sh" in additional_files
        assert "scripts/rollback.sh" in additional_files
        assert "scripts/monitoring-setup.sh" in additional_files
        assert ".dockerignore" in additional_files
        assert "README.md" in additional_files
        
        # Check deploy script
        deploy_script = additional_files["scripts/deploy.sh"]
        assert "#!/bin/bash" in deploy_script
        assert "set -e" in deploy_script
        assert "ENVIRONMENT=${1:-staging}" in deploy_script
        assert "docker build" in deploy_script
        assert "helm upgrade" in deploy_script
        assert "kubectl rollout status" in deploy_script
        
        # Check rollback script
        rollback_script = additional_files["scripts/rollback.sh"]
        assert "helm rollback" in rollback_script
        assert "helm history" in rollback_script
        
        # Check monitoring setup script
        monitoring_script = additional_files["scripts/monitoring-setup.sh"]
        assert "prometheus-community" in monitoring_script
        assert "kube-prometheus-stack" in monitoring_script
        
        # Check .dockerignore
        dockerignore = additional_files[".dockerignore"]
        assert ".git" in dockerignore
        assert "node_modules/" in dockerignore
        assert "__pycache__/" in dockerignore
        
        # Check comprehensive README
        readme = additional_files["README.md"]
        assert "# DevOps Configuration" in readme
        assert "## Technologies" in readme
        assert "## Quick Start" in readme
        assert "## Monitoring & Observability" in readme
        assert "## Security" in readme
        assert "## Troubleshooting" in readme
    
    @pytest.mark.asyncio
    async def test_create_devops_setup(self, devops_agent):
        """Test comprehensive DevOps setup creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Test Application",
                "description": "Create complete DevOps setup",
                "requirements": {
                    "kubernetes": True,
                    "terraform": True,
                    "monitoring": "prometheus"
                },
                "output_dir": temp_dir
            }
            
            result = await devops_agent._create_devops_setup(
                task, temp_dir, "docker", "kubernetes", "github-actions", 
                "terraform", "prometheus-grafana"
            )
            
            assert result["status"] == "completed"
            assert result["container_platform"] == "docker"
            assert result["orchestrator"] == "kubernetes"
            assert result["ci_cd_platform"] == "github-actions"
            assert result["iac_tool"] == "terraform"
            assert result["monitoring_stack"] == "prometheus-grafana"
            assert len(result["files_created"]) > 50  # Should create many files
            
            # Check that some key features are included
            expected_features = [
                "Multi-stage Docker builds",
                "Kubernetes manifests", 
                "Helm charts",
                "CI/CD pipelines",
                "Infrastructure as Code",
                "Monitoring setup"
            ]
            for feature in expected_features:
                assert feature in result["features"]
    
    @pytest.mark.asyncio
    async def test_process_task(self, devops_agent):
        """Test task processing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "DevOps Setup",
                "description": "Complete DevOps infrastructure",
                "architecture": {"deployment": "kubernetes"},
                "requirements": {"ci_cd": "github actions", "monitoring": "prometheus"},
                "output_dir": temp_dir
            }
            
            result = await devops_agent.process_task(task)
            
            assert result["status"] == "completed"
            assert result["container_platform"] == "docker"
            assert result["orchestrator"] == "kubernetes" 
            assert result["ci_cd_platform"] == "github-actions"
            assert devops_agent.status == "idle"
    
    @pytest.mark.asyncio
    async def test_process_task_error_handling(self, devops_agent):
        """Test error handling in task processing"""
        task = {
            "title": "Broken DevOps task",
            "output_dir": "/invalid/path/that/does/not/exist"
        }
        
        result = await devops_agent.process_task(task)
        
        assert result["status"] == "error"
        assert "message" in result
        assert result["files_created"] == []
        assert devops_agent.status == "error"
    
    def test_docker_compose_structure(self, devops_agent):
        """Test Docker Compose file structure"""
        task = {"title": "test-app"}
        docker_files = devops_agent._get_docker_files(task)
        
        compose_content = docker_files["docker/docker-compose.yml"]
        
        # Parse YAML to ensure it's valid
        compose_data = yaml.safe_load(compose_content)
        assert compose_data["version"] == "3.8"
        assert "services" in compose_data
        assert "frontend" in compose_data["services"]
        assert "backend" in compose_data["services"]
        assert "db" in compose_data["services"]
        assert "redis" in compose_data["services"]
        assert "volumes" in compose_data
        assert "networks" in compose_data
    
    def test_kubernetes_yaml_validity(self, devops_agent):
        """Test that generated Kubernetes manifests are valid YAML"""
        task = {"title": "test-app"}
        k8s_files = devops_agent._get_kubernetes_files(task)
        
        # Test that all YAML files are valid
        for filename, content in k8s_files.items():
            try:
                # Split multi-document YAML files
                for doc in content.split("---"):
                    if doc.strip():
                        yaml.safe_load(doc)
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in {filename}: {e}")
    
    def test_terraform_syntax_validity(self, devops_agent):
        """Test that generated Terraform files have basic syntax validity"""
        task = {"title": "test-app"}
        terraform_files = devops_agent._get_terraform_files(task)
        
        # Check that Terraform files contain expected blocks
        main_tf = terraform_files["terraform/main.tf"]
        assert "terraform {" in main_tf
        assert "provider \"aws\" {" in main_tf
        assert "provider \"kubernetes\" {" in main_tf
        
        variables_tf = terraform_files["terraform/variables.tf"]
        assert 'variable "aws_region"' in variables_tf
        assert 'variable "cluster_name"' in variables_tf
        
        outputs_tf = terraform_files["terraform/outputs.tf"]
        assert 'output "cluster_endpoint"' in outputs_tf
        assert 'output "cluster_name"' in outputs_tf
    
    def test_comprehensive_feature_coverage(self, devops_agent):
        """Test that all advertised features are actually implemented"""
        task = {"title": "comprehensive-app"}
        
        # Test Docker features
        docker_files = devops_agent._get_docker_files(task)
        backend_dockerfile = docker_files["docker/Dockerfile.backend"]
        
        # Multi-stage builds
        assert "as builder" in backend_dockerfile
        assert "COPY --from=builder" in backend_dockerfile
        
        # Security features
        assert "useradd" in backend_dockerfile
        assert "USER " in backend_dockerfile
        
        # Health checks
        assert "HEALTHCHECK" in backend_dockerfile
        
        # Test Kubernetes features
        k8s_files = devops_agent._get_kubernetes_files(task)
        
        # Auto-scaling
        assert "k8s/hpa.yaml" in k8s_files
        hpa = k8s_files["k8s/hpa.yaml"]
        assert "HorizontalPodAutoscaler" in hpa
        
        # Security policies
        assert "k8s/network-policy.yaml" in k8s_files
        
        # Load balancing
        assert "k8s/ingress.yaml" in k8s_files
        
        # Test CI/CD features
        github_files = devops_agent._get_github_actions_files(task)
        ci_cd = github_files[".github/workflows/ci-cd.yml"]
        
        # Security scanning
        assert "trivy" in ci_cd
        assert "security-scan:" in github_files[".github/workflows/security-scan.yml"]
        
        # Performance testing
        assert ".github/workflows/performance-test.yml" in github_files
    
    def test_script_executability_markers(self, devops_agent):
        """Test that shell scripts have proper shebang and structure"""
        task = {"title": "test-app"}
        additional_files = devops_agent._get_additional_devops_files(task)
        
        scripts = [
            "scripts/deploy.sh",
            "scripts/rollback.sh", 
            "scripts/monitoring-setup.sh"
        ]
        
        for script_path in scripts:
            script_content = additional_files[script_path]
            
            # Check shebang
            assert script_content.startswith("#!/bin/bash")
            
            # Check error handling
            assert "set -e" in script_content
            
            # Check functions are defined properly
            if "deploy.sh" in script_path:
                assert "log()" in script_content
                assert "error()" in script_content
                assert "warn()" in script_content

