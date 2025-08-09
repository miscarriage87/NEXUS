
"""
DevOps and Deployment Agent - Docker, Kubernetes, CI/CD, Infrastructure as Code
Task 6: DevOps and Deployment Agent
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.ollama_client import ollama_client

class DevOpsAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("devops", "DevOps Engineer", config)
        self.technologies = config.get('agents', {}).get('devops', {}).get('technologies', [])
        self.container_platforms = ['docker', 'podman', 'containerd']
        self.orchestrators = ['kubernetes', 'docker-swarm', 'nomad']
        self.ci_cd_platforms = ['github-actions', 'gitlab-ci', 'jenkins', 'azure-devops', 'circleci']
        self.iac_tools = ['terraform', 'ansible', 'pulumi', 'cloudformation']
        self.monitoring_stacks = ['prometheus-grafana', 'elk-stack', 'datadog', 'new-relic']
        
    def get_capabilities(self) -> List[str]:
        return [
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
            "elk_stack_setup",
            "service_mesh_integration",
            "load_balancing_configuration",
            "auto_scaling_setup",
            "security_scanning_integration",
            "secrets_management",
            "environment_management",
            "deployment_strategies",
            "blue_green_deployment",
            "canary_deployment",
            "rollback_strategies"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process DevOps deployment tasks"""
        self.status = "working"
        self.logger.info(f"Processing DevOps task: {task.get('title', 'Unknown')}")
        
        try:
            output_dir = task.get("output_dir", "/home/ubuntu/nexus/demo")
            architecture = task.get("architecture", {})
            requirements = task.get("requirements", {})
            
            # Determine DevOps requirements
            container_platform = self._determine_container_platform(requirements)
            orchestrator = self._determine_orchestrator(requirements)
            ci_cd_platform = self._determine_ci_cd_platform(requirements)
            iac_tool = self._determine_iac_tool(requirements)
            monitoring_stack = self._determine_monitoring_stack(requirements)
            
            self.logger.info(f"Creating DevOps setup with {container_platform}, {orchestrator}, {ci_cd_platform}")
            
            # Create comprehensive DevOps setup
            result = await self._create_devops_setup(
                task, output_dir, container_platform, orchestrator, 
                ci_cd_platform, iac_tool, monitoring_stack
            )
            
            self.status = "idle"
            return result
            
        except Exception as e:
            self.status = "error"
            self.logger.error(f"Error processing DevOps task: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "files_created": []
            }
    
    def _determine_container_platform(self, requirements: Dict) -> str:
        """Determine container platform to use"""
        req_str = str(requirements).lower()
        for platform in self.container_platforms:
            if platform in req_str:
                return platform
        return "docker"  # Default
    
    def _determine_orchestrator(self, requirements: Dict) -> str:
        """Determine orchestration platform"""
        req_str = str(requirements).lower()
        if 'kubernetes' in req_str or 'k8s' in req_str:
            return 'kubernetes'
        elif 'swarm' in req_str:
            return 'docker-swarm'
        elif 'nomad' in req_str:
            return 'nomad'
        return 'kubernetes'  # Default
    
    def _determine_ci_cd_platform(self, requirements: Dict) -> str:
        """Determine CI/CD platform"""
        req_str = str(requirements).lower()
        for platform in self.ci_cd_platforms:
            if platform.replace('-', ' ') in req_str or platform.replace('-', '') in req_str:
                return platform
        return 'github-actions'  # Default
    
    def _determine_iac_tool(self, requirements: Dict) -> str:
        """Determine Infrastructure as Code tool"""
        req_str = str(requirements).lower()
        for tool in self.iac_tools:
            if tool in req_str:
                return tool
        return 'terraform'  # Default
    
    def _determine_monitoring_stack(self, requirements: Dict) -> str:
        """Determine monitoring stack"""
        req_str = str(requirements).lower()
        if 'prometheus' in req_str or 'grafana' in req_str:
            return 'prometheus-grafana'
        elif 'elk' in req_str or 'elasticsearch' in req_str:
            return 'elk-stack'
        elif 'datadog' in req_str:
            return 'datadog'
        elif 'new relic' in req_str or 'newrelic' in req_str:
            return 'new-relic'
        return 'prometheus-grafana'  # Default
    
    async def _create_devops_setup(self, task: Dict[str, Any], output_dir: str,
                                 container_platform: str, orchestrator: str, 
                                 ci_cd_platform: str, iac_tool: str, monitoring_stack: str) -> Dict[str, Any]:
        """Create comprehensive DevOps setup"""
        devops_dir = os.path.join(output_dir, "devops")
        os.makedirs(devops_dir, exist_ok=True)
        
        files = {}
        
        # Docker setup
        if container_platform == 'docker':
            files.update(self._get_docker_files(task))
        
        # Kubernetes setup
        if orchestrator == 'kubernetes':
            files.update(self._get_kubernetes_files(task))
            files.update(self._get_helm_chart_files(task))
        
        # CI/CD setup
        if ci_cd_platform == 'github-actions':
            files.update(self._get_github_actions_files(task))
        elif ci_cd_platform == 'gitlab-ci':
            files.update(self._get_gitlab_ci_files(task))
        elif ci_cd_platform == 'jenkins':
            files.update(self._get_jenkins_files(task))
        
        # Infrastructure as Code
        if iac_tool == 'terraform':
            files.update(self._get_terraform_files(task))
        elif iac_tool == 'ansible':
            files.update(self._get_ansible_files(task))
        
        # Monitoring setup
        if monitoring_stack == 'prometheus-grafana':
            files.update(self._get_prometheus_grafana_files(task))
        elif monitoring_stack == 'elk-stack':
            files.update(self._get_elk_stack_files(task))
        
        # Additional DevOps files
        files.update(self._get_additional_devops_files(task))
        
        # Write all files
        created_files = []
        for filename, content in files.items():
            file_path = os.path.join(devops_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(file_path)
        
        return {
            "status": "completed",
            "files_created": created_files,
            "output_directory": devops_dir,
            "container_platform": container_platform,
            "orchestrator": orchestrator,
            "ci_cd_platform": ci_cd_platform,
            "iac_tool": iac_tool,
            "monitoring_stack": monitoring_stack,
            "features": [
                "Multi-stage Docker builds",
                "Kubernetes manifests",
                "Helm charts",
                "CI/CD pipelines",
                "Infrastructure as Code",
                "Monitoring setup",
                "Security scanning",
                "Auto-scaling",
                "Load balancing"
            ]
        }
    
    def _get_docker_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Docker configuration files"""
        return {
            "docker/Dockerfile.frontend": """# Multi-stage build for React frontend
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy source code
COPY frontend/ .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy build files
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:80/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]""",

            "docker/Dockerfile.backend": """# Multi-stage build for Python backend
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    libpq5 \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY backend/ .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]""",

            "docker/nginx.conf": """events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate no_last_modified no_etag auth;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/x-javascript
        application/javascript
        application/xml+rss
        application/json;

    server {
        listen 80;
        server_name localhost;

        root /usr/share/nginx/html;
        index index.html index.htm;

        # Handle client-side routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # API proxy
        location /api {
            proxy_pass http://backend:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        # Static files caching
        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}""",

            "docker/docker-compose.yml": """version: '3.8'

services:
  frontend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    networks:
      - app-network
    restart: unless-stopped

  backend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/appdb
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=your-secret-key-change-in-production
    volumes:
      - ../backend:/app
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge""",

            "docker/docker-compose.prod.yml": """version: '3.8'

services:
  frontend:
    image: your-registry/app-frontend:latest
    restart: unless-stopped
    environment:
      - REACT_APP_API_URL=https://api.yourdomain.com
    networks:
      - app-network

  backend:
    image: your-registry/app-backend:latest
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/appdb
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=false
    networks:
      - app-network
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - app-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: overlay""",

            "docker/.dockerignore": """# Git
.git
.gitignore

# Documentation
README.md
docs/

# Development files
.env
.env.local
.env.development
.env.test

# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test files
coverage/
.coverage
.pytest_cache/

# Build artifacts
dist/
build/
*.egg-info/"""
        }
    
    def _get_kubernetes_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Kubernetes manifest files"""
        app_name = task.get('title', 'app').lower().replace(' ', '-')
        
        return {
            "k8s/namespace.yaml": f"""apiVersion: v1
kind: Namespace
metadata:
  name: {app_name}
  labels:
    name: {app_name}
    environment: production""",

            "k8s/configmap.yaml": f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {app_name}-config
  namespace: {app_name}
data:
  DATABASE_URL: "postgresql://postgres:password@postgres-service:5432/appdb"
  REDIS_URL: "redis://redis-service:6379"
  DEBUG: "false"
  API_VERSION: "v1"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: {app_name}-frontend-config
  namespace: {app_name}
data:
  nginx.conf: |
    events {{
        worker_connections 1024;
    }}

    http {{
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        server {{
            listen 80;
            server_name localhost;

            root /usr/share/nginx/html;
            index index.html index.htm;

            location / {{
                try_files $uri $uri/ /index.html;
            }}

            location /api {{
                proxy_pass http://{app_name}-backend-service:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }}
        }}
    }}""",

            "k8s/secrets.yaml": f"""apiVersion: v1
kind: Secret
metadata:
  name: {app_name}-secrets
  namespace: {app_name}
type: Opaque
data:
  # Base64 encoded values
  # Use: echo -n 'your-secret' | base64
  SECRET_KEY: eW91ci1zdXBlci1zZWNyZXQta2V5LWNoYW5nZS1pbi1wcm9kdWN0aW9u
  POSTGRES_PASSWORD: cGFzc3dvcmQ=
  REDIS_PASSWORD: cGFzc3dvcmQ=""",

            "k8s/postgres.yaml": f"""apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: {app_name}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
  namespace: {app_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "appdb"
        - name: POSTGRES_USER
          value: "postgres"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {app_name}-secrets
              key: POSTGRES_PASSWORD
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: {app_name}
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
  type: ClusterIP""",

            "k8s/redis.yaml": f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  namespace: {app_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        command: ["redis-server"]
        args: ["--requirepass", "$(REDIS_PASSWORD)", "--appendonly", "yes"]
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {app_name}-secrets
              key: REDIS_PASSWORD
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: redis-data
        emptyDir: {{}}
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: {app_name}
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
  type: ClusterIP""",

            "k8s/backend.yaml": f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}-backend-deployment
  namespace: {app_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {app_name}-backend
  template:
    metadata:
      labels:
        app: {app_name}-backend
    spec:
      containers:
      - name: backend
        image: your-registry/{app_name}-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: {app_name}-config
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: {app_name}-secrets
              key: SECRET_KEY
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: app-logs
          mountPath: /app/logs
      volumes:
      - name: app-logs
        emptyDir: {{}}
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-backend-service
  namespace: {app_name}
spec:
  selector:
    app: {app_name}-backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP""",

            "k8s/frontend.yaml": f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}-frontend-deployment
  namespace: {app_name}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {app_name}-frontend
  template:
    metadata:
      labels:
        app: {app_name}-frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/{app_name}-frontend:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: nginx-config
        configMap:
          name: {app_name}-frontend-config
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-frontend-service
  namespace: {app_name}
spec:
  selector:
    app: {app_name}-frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP""",

            "k8s/ingress.yaml": f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {app_name}-ingress
  namespace: {app_name}
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/use-regex: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - yourdomain.com
    - api.yourdomain.com
    secretName: {app_name}-tls
  rules:
  - host: yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {app_name}-frontend-service
            port:
              number: 80
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {app_name}-backend-service
            port:
              number: 8000""",

            "k8s/hpa.yaml": f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {app_name}-backend-hpa
  namespace: {app_name}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {app_name}-backend-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {app_name}-frontend-hpa
  namespace: {app_name}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {app_name}-frontend-deployment
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70""",

            "k8s/network-policy.yaml": f"""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {app_name}-network-policy
  namespace: {app_name}
spec:
  podSelector: {{}}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
  - from:
    - podSelector:
        matchLabels:
          app: {app_name}-frontend
    ports:
    - protocol: TCP
      port: 8000
  - from:
    - podSelector:
        matchLabels:
          app: {app_name}-backend
    ports:
    - protocol: TCP
      port: 5432
  - from:
    - podSelector:
        matchLabels:
          app: {app_name}-backend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - {{}}"""
        }
    
    def _get_helm_chart_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Helm chart files"""
        app_name = task.get('title', 'app').lower().replace(' ', '-')
        
        return {
            "helm/Chart.yaml": f"""apiVersion: v2
name: {app_name}
description: A Helm chart for {app_name}
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
- name: postgresql
  version: 12.x.x
  repository: https://charts.bitnami.com/bitnami
  condition: postgresql.enabled
- name: redis
  version: 17.x.x
  repository: https://charts.bitnami.com/bitnami
  condition: redis.enabled""",

            "helm/values.yaml": f"""# Default values for {app_name}
replicaCount:
  frontend: 2
  backend: 3

image:
  frontend:
    repository: your-registry/{app_name}-frontend
    pullPolicy: IfNotPresent
    tag: latest
  backend:
    repository: your-registry/{app_name}-backend
    pullPolicy: IfNotPresent
    tag: latest

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {{}}
  name: ""

podAnnotations: {{}}

podSecurityContext:
  fsGroup: 2000

securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000

service:
  type: ClusterIP
  frontend:
    port: 80
  backend:
    port: 8000

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: yourdomain.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
    - host: api.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
          service: backend
  tls:
    - secretName: {app_name}-tls
      hosts:
        - yourdomain.com
        - api.yourdomain.com

resources:
  frontend:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
  backend:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

autoscaling:
  frontend:
    enabled: true
    minReplicas: 2
    maxReplicas: 6
    targetCPUUtilizationPercentage: 70
  backend:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80

nodeSelector: {{}}

tolerations: []

affinity: {{}}

# Database configuration
postgresql:
  enabled: true
  auth:
    postgresPassword: password
    database: appdb
  primary:
    persistence:
      enabled: true
      size: 10Gi

# Redis configuration
redis:
  enabled: true
  auth:
    enabled: true
    password: password
  master:
    persistence:
      enabled: false

# Application configuration
config:
  secretKey: your-super-secret-key-change-in-production
  debug: false
  apiVersion: v1""",

            "helm/templates/deployment-frontend.yaml": f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{{{ include "{app_name}.fullname" . }}}}-frontend
  labels:
    {{{{- include "{app_name}.labels" . | nindent 4 }}}}
    app.kubernetes.io/component: frontend
spec:
  {{{{- if not .Values.autoscaling.frontend.enabled }}}}
  replicas: {{{{ .Values.replicaCount.frontend }}}}
  {{{{- end }}}}
  selector:
    matchLabels:
      {{{{- include "{app_name}.selectorLabels" . | nindent 6 }}}}
      app.kubernetes.io/component: frontend
  template:
    metadata:
      {{{{- with .Values.podAnnotations }}}}
      annotations:
        {{{{- toYaml . | nindent 8 }}}}
      {{{{- end }}}}
      labels:
        {{{{- include "{app_name}.selectorLabels" . | nindent 8 }}}}
        app.kubernetes.io/component: frontend
    spec:
      {{{{- with .Values.imagePullSecrets }}}}
      imagePullSecrets:
        {{{{- toYaml . | nindent 8 }}}}
      {{{{- end }}}}
      serviceAccountName: {{{{ include "{app_name}.serviceAccountName" . }}}}
      securityContext:
        {{{{- toYaml .Values.podSecurityContext | nindent 8 }}}}
      containers:
        - name: frontend
          securityContext:
            {{{{- toYaml .Values.securityContext | nindent 12 }}}}
          image: "{{{{ .Values.image.frontend.repository }}}}:{{{{ .Values.image.frontend.tag | default .Chart.AppVersion }}}}"
          imagePullPolicy: {{{{ .Values.image.frontend.pullPolicy }}}}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{{{- toYaml .Values.resources.frontend | nindent 12 }}}}
      {{{{- with .Values.nodeSelector }}}}
      nodeSelector:
        {{{{- toYaml . | nindent 8 }}}}
      {{{{- end }}}}
      {{{{- with .Values.affinity }}}}
      affinity:
        {{{{- toYaml . | nindent 8 }}}}
      {{{{- end }}}}
      {{{{- with .Values.tolerations }}}}
      tolerations:
        {{{{- toYaml . | nindent 8 }}}}
      {{{{- end }}}}""",

            "helm/templates/_helpers.tpl": f"""{{{{/*
Expand the name of the chart.
*/}}}}
{{{{- define "{app_name}.name" -}}}}
{{{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}

{{{{/*
Create a default fully qualified app name.
*/}}}}
{{{{- define "{app_name}.fullname" -}}}}
{{{{- if .Values.fullnameOverride }}}}
{{{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}}}
{{{{- else }}}}
{{{{- $name := default .Chart.Name .Values.nameOverride }}}}
{{{{- if contains $name .Release.Name }}}}
{{{{- .Release.Name | trunc 63 | trimSuffix "-" }}}}
{{{{- else }}}}
{{{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}
{{{{- end }}}}
{{{{- end }}}}

{{{{/*
Create chart name and version as used by the chart label.
*/}}}}
{{{{- define "{app_name}.chart" -}}}}
{{{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}

{{{{/*
Common labels
*/}}}}
{{{{- define "{app_name}.labels" -}}}}
helm.sh/chart: {{{{ include "{app_name}.chart" . }}}}
{{{{ include "{app_name}.selectorLabels" . }}}}
{{{{- if .Chart.AppVersion }}}}
app.kubernetes.io/version: {{{{ .Chart.AppVersion | quote }}}}
{{{{- end }}}}
app.kubernetes.io/managed-by: {{{{ .Release.Service }}}}
{{{{- end }}}}

{{{{/*
Selector labels
*/}}}}
{{{{- define "{app_name}.selectorLabels" -}}}}
app.kubernetes.io/name: {{{{ include "{app_name}.name" . }}}}
app.kubernetes.io/instance: {{{{ .Release.Name }}}}
{{{{- end }}}}

{{{{/*
Create the name of the service account to use
*/}}}}
{{{{- define "{app_name}.serviceAccountName" -}}}}
{{{{- if .Values.serviceAccount.create }}}}
{{{{- default (include "{app_name}.fullname" .) .Values.serviceAccount.name }}}}
{{{{- else }}}}
{{{{- default "default" .Values.serviceAccount.name }}}}
{{{{- end }}}}
{{{{- end }}}}"""
        }
    
    def _get_github_actions_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate GitHub Actions workflow files"""
        return {
            ".github/workflows/ci-cd.yml": """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install Python dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio

    - name: Install Node dependencies
      run: |
        cd frontend
        npm ci

    - name: Run Python tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb
        REDIS_URL: redis://localhost:6379
        SECRET_KEY: test-secret-key
      run: |
        cd backend
        pytest --cov=. --cov-report=xml --cov-report=term

    - name: Run frontend tests
      run: |
        cd frontend
        npm test -- --coverage --watchAll=false

    - name: Lint Python code
      run: |
        cd backend
        pip install flake8 black
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check .

    - name: Lint frontend code
      run: |
        cd frontend
        npm run lint

    - name: Build frontend
      run: |
        cd frontend
        npm run build

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
        flags: backend
        name: backend-coverage

  security-scan:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Python security check
      run: |
        cd backend
        pip install bandit safety
        bandit -r . -f json -o bandit-report.json
        safety check --json --output safety-report.json

  build-and-push:
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata (tags, labels) for backend
      id: meta-backend
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-backend

    - name: Extract metadata (tags, labels) for frontend
      id: meta-frontend
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend

    - name: Build and push backend Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: docker/Dockerfile.backend
        push: true
        tags: ${{ steps.meta-backend.outputs.tags }}
        labels: ${{ steps.meta-backend.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Build and push frontend Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: docker/Dockerfile.frontend
        push: true
        tags: ${{ steps.meta-frontend.outputs.tags }}
        labels: ${{ steps.meta-frontend.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: Set up Helm
      uses: azure/setup-helm@v3
      with:
        version: 'latest'

    - name: Configure kubeconfig
      run: |
        mkdir -p ~/.kube
        echo "${{ secrets.KUBE_CONFIG }}" | base64 --decode > ~/.kube/config

    - name: Deploy to Kubernetes
      run: |
        helm upgrade --install myapp ./helm \\
          --set image.backend.tag=main \\
          --set image.frontend.tag=main \\
          --set config.secretKey="${{ secrets.SECRET_KEY }}" \\
          --namespace production \\
          --create-namespace \\
          --wait

    - name: Verify deployment
      run: |
        kubectl rollout status deployment/myapp-backend -n production
        kubectl rollout status deployment/myapp-frontend -n production

    - name: Run smoke tests
      run: |
        kubectl run smoke-test --rm -i --restart=Never --image=curlimages/curl -- \\
          curl -f http://myapp-backend-service:8000/health""",

            ".github/workflows/security-scan.yml": """name: Security Scanning

on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM
  push:
    branches: [ main ]

jobs:
  container-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Build backend image
      run: docker build -f docker/Dockerfile.backend -t backend-security-scan .

    - name: Build frontend image
      run: docker build -f docker/Dockerfile.frontend -t frontend-security-scan .

    - name: Scan backend image
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: backend-security-scan
        format: 'sarif'
        output: 'backend-scan.sarif'

    - name: Scan frontend image
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: frontend-security-scan
        format: 'sarif'
        output: 'frontend-scan.sarif'

    - name: Upload scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'backend-scan.sarif'

  dependency-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install Python dependencies
      run: |
        cd backend
        pip install -r requirements.txt

    - name: Python dependency scan
      run: |
        cd backend
        pip install safety
        safety check

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'

    - name: Node.js dependency scan
      run: |
        cd frontend
        npm audit""",

            ".github/workflows/performance-test.yml": """name: Performance Testing

on:
  schedule:
    - cron: '0 4 * * *'  # Daily at 4 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt

    - name: Start application
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb
        SECRET_KEY: test-secret-key
      run: |
        cd backend
        uvicorn main:app --host 0.0.0.0 --port 8000 &
        sleep 10

    - name: Install k6
      run: |
        sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6

    - name: Run load test
      run: |
        cat <<EOF > load-test.js
        import http from 'k6/http';
        import { check, sleep } from 'k6';

        export let options = {
          stages: [
            { duration: '2m', target: 10 },
            { duration: '5m', target: 10 },
            { duration: '2m', target: 20 },
            { duration: '5m', target: 20 },
            { duration: '2m', target: 0 },
          ],
        };

        export default function() {
          let response = http.get('http://localhost:8000/');
          check(response, {
            'status is 200': (r) => r.status === 200,
            'response time < 500ms': (r) => r.timings.duration < 500,
          });
          sleep(1);
        }
        EOF

        k6 run load-test.js"""
        }
    
    def _get_gitlab_ci_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate GitLab CI/CD pipeline files"""
        return {
            ".gitlab-ci.yml": """stages:
  - test
  - security
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  POSTGRES_DB: testdb
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres

services:
  - postgres:15
  - redis:7

before_script:
  - docker info

# Test stage
test-backend:
  stage: test
  image: python:3.11
  variables:
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/testdb
    REDIS_URL: redis://redis:6379
  before_script:
    - cd backend
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - pytest --cov=. --cov-report=xml --cov-report=term
  coverage: '/TOTAL.+?(\\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: backend/coverage.xml

test-frontend:
  stage: test
  image: node:18
  before_script:
    - cd frontend
    - npm ci
  script:
    - npm test -- --coverage --watchAll=false
    - npm run build
  artifacts:
    paths:
      - frontend/build/
    expire_in: 1 hour

# Security stage
security-scan:
  stage: security
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -f docker/Dockerfile.backend -t backend-scan .
    - docker run --rm -v $PWD:/workspace aquasec/trivy image backend-scan

dependency-check:
  stage: security
  image: python:3.11
  script:
    - cd backend
    - pip install safety bandit
    - safety check
    - bandit -r . -f json -o bandit-report.json
  artifacts:
    reports:
      sast: bandit-report.json

# Build stage
build-backend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -f docker/Dockerfile.backend -t $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA
  only:
    - main

build-frontend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -f docker/Dockerfile.frontend -t $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA
  only:
    - main

# Deploy stage
deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context $KUBE_CONTEXT_STAGING
    - helm upgrade --install myapp-staging ./helm 
      --set image.backend.tag=$CI_COMMIT_SHA
      --set image.frontend.tag=$CI_COMMIT_SHA
      --namespace staging
      --create-namespace
  environment:
    name: staging
    url: https://staging.yourdomain.com
  only:
    - main

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context $KUBE_CONTEXT_PRODUCTION
    - helm upgrade --install myapp-prod ./helm 
      --set image.backend.tag=$CI_COMMIT_SHA
      --set image.frontend.tag=$CI_COMMIT_SHA
      --namespace production
      --create-namespace
      --wait
  environment:
    name: production
    url: https://yourdomain.com
  when: manual
  only:
    - main"""
        }
    
    def _get_jenkins_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Jenkins pipeline files"""
        return {
            "Jenkinsfile": """pipeline {
    agent any
    
    environment {
        REGISTRY = 'your-registry'
        IMAGE_NAME = 'myapp'
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir('backend') {
                            sh '''
                                python -m venv venv
                                . venv/bin/activate
                                pip install -r requirements.txt
                                pip install pytest pytest-cov
                                pytest --cov=. --cov-report=xml
                            '''
                        }
                    }
                    post {
                        always {
                            publishCoverage adapters: [coberturaAdapter('backend/coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                        }
                    }
                }
                
                stage('Frontend Tests') {
                    steps {
                        dir('frontend') {
                            sh '''
                                npm ci
                                npm test -- --coverage --watchAll=false
                                npm run build
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh '''
                        docker build -f docker/Dockerfile.backend -t backend-scan .
                        docker run --rm -v $(pwd):/workspace aquasec/trivy image backend-scan
                    '''
                }
            }
        }
        
        stage('Build Images') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def backendImage = docker.build("${REGISTRY}/${IMAGE_NAME}-backend:${BUILD_NUMBER}", "-f docker/Dockerfile.backend .")
                    def frontendImage = docker.build("${REGISTRY}/${IMAGE_NAME}-frontend:${BUILD_NUMBER}", "-f docker/Dockerfile.frontend .")
                    
                    docker.withRegistry("https://${REGISTRY}", 'registry-credentials') {
                        backendImage.push()
                        backendImage.push("latest")
                        frontendImage.push()
                        frontendImage.push("latest")
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    helm upgrade --install myapp-staging ./helm \\
                        --set image.backend.tag=${BUILD_NUMBER} \\
                        --set image.frontend.tag=${BUILD_NUMBER} \\
                        --namespace staging \\
                        --create-namespace
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh '''
                    helm upgrade --install myapp-prod ./helm \\
                        --set image.backend.tag=${BUILD_NUMBER} \\
                        --set image.frontend.tag=${BUILD_NUMBER} \\
                        --namespace production \\
                        --create-namespace \\
                        --wait
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend channel: '#deployments',
                     color: 'good',
                     message: "Deployment successful: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#deployments',
                     color: 'danger',
                     message: "Deployment failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
        }
    }
}"""
        }
    
    def _get_terraform_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Terraform Infrastructure as Code files"""
        return {
            "terraform/main.tf": """terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }
  
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "myapp/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
    }
  }
}""",

            "terraform/variables.tf": """variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "myapp-cluster"
}

variable "cluster_version" {
  description = "EKS cluster version"
  type        = string
  default     = "1.28"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "node_groups" {
  description = "EKS node groups configuration"
  type = map(object({
    instance_types = list(string)
    capacity_type  = string
    min_size      = number
    max_size      = number
    desired_size  = number
  }))
  default = {
    main = {
      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
      min_size      = 1
      max_size      = 5
      desired_size  = 2
    }
  }
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Environment = "production"
    Project     = "myapp"
    ManagedBy   = "terraform"
  }
}""",

            "terraform/eks.tf": """module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = data.aws_availability_zones.available.names
  private_subnets = [for k, v in data.aws_availability_zones.available.names : cidrsubnet(var.vpc_cidr, 8, k)]
  public_subnets  = [for k, v in data.aws_availability_zones.available.names : cidrsubnet(var.vpc_cidr, 8, k + 100)]

  enable_nat_gateway = true
  enable_vpn_gateway = true
  enable_dns_hostnames = true
  enable_dns_support = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }

  tags = var.tags
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  eks_managed_node_groups = {
    for k, v in var.node_groups : k => {
      instance_types = v.instance_types
      capacity_type  = v.capacity_type
      
      min_size     = v.min_size
      max_size     = v.max_size
      desired_size = v.desired_size

      update_config = {
        max_unavailable_percentage = 25
      }

      tags = var.tags
    }
  }

  tags = var.tags
}

data "aws_availability_zones" "available" {
  state = "available"
}""",

            "terraform/addons.tf": """# AWS Load Balancer Controller
resource "helm_release" "aws_load_balancer_controller" {
  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"
  version    = "1.6.2"

  set {
    name  = "clusterName"
    value = module.eks.cluster_name
  }

  set {
    name  = "serviceAccount.create"
    value = "true"
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  depends_on = [module.eks]
}

# Cert Manager
resource "helm_release" "cert_manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  namespace  = "cert-manager"
  version    = "v1.13.2"
  
  create_namespace = true

  set {
    name  = "installCRDs"
    value = "true"
  }

  depends_on = [module.eks]
}

# Nginx Ingress Controller
resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  namespace  = "ingress-nginx"
  version    = "4.8.3"
  
  create_namespace = true

  set {
    name  = "controller.service.type"
    value = "LoadBalancer"
  }

  set {
    name  = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/aws-load-balancer-type"
    value = "nlb"
  }

  depends_on = [module.eks, helm_release.aws_load_balancer_controller]
}""",

            "terraform/outputs.tf": """output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = module.eks.cluster_certificate_authority_data
}

output "cluster_iam_role_name" {
  description = "IAM role name associated with EKS cluster"
  value       = module.eks.cluster_iam_role_name
}

output "cluster_iam_role_arn" {
  description = "IAM role ARN associated with EKS cluster"
  value       = module.eks.cluster_iam_role_arn
}

output "node_groups" {
  description = "EKS node groups"
  value       = module.eks.eks_managed_node_groups
}

output "vpc_id" {
  description = "ID of the VPC where the cluster is deployed"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "List of IDs of public subnets"
  value       = module.vpc.public_subnets
}"""
        }
    
    def _get_ansible_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Ansible playbook files"""
        return {
            "ansible/inventory.yml": """all:
  children:
    web:
      hosts:
        web1:
          ansible_host: 10.0.1.10
        web2:
          ansible_host: 10.0.1.11
    db:
      hosts:
        db1:
          ansible_host: 10.0.2.10
        db2:
          ansible_host: 10.0.2.11
    load_balancers:
      hosts:
        lb1:
          ansible_host: 10.0.0.10
  vars:
    ansible_user: ubuntu
    ansible_ssh_private_key_file: ~/.ssh/id_rsa""",

            "ansible/playbook.yml": """---
- name: Deploy Application Infrastructure
  hosts: all
  become: yes
  gather_facts: yes
  
  vars:
    app_name: myapp
    app_version: "{{ app_version | default('latest') }}"
    docker_compose_version: "2.21.0"
    
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"
    
    - name: Install required packages
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
          - software-properties-common
          - python3-pip
        state: present
      when: ansible_os_family == "Debian"

- name: Setup Docker
  hosts: all
  become: yes
  
  tasks:
    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present
    
    - name: Add Docker repository
      apt_repository:
        repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present
    
    - name: Install Docker
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
          - docker-buildx-plugin
          - docker-compose-plugin
        state: present
    
    - name: Start and enable Docker
      systemd:
        name: docker
        state: started
        enabled: yes
    
    - name: Add user to docker group
      user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes

- name: Deploy Web Servers
  hosts: web
  become: yes
  
  tasks:
    - name: Create application directory
      file:
        path: /opt/{{ app_name }}
        state: directory
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0755'
    
    - name: Copy docker-compose file
      template:
        src: docker-compose.yml.j2
        dest: /opt/{{ app_name }}/docker-compose.yml
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0644'
    
    - name: Copy environment file
      template:
        src: .env.j2
        dest: /opt/{{ app_name }}/.env
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0600'
    
    - name: Pull and start application containers
      docker_compose:
        project_src: /opt/{{ app_name }}
        pull: yes
        state: present
      become_user: "{{ ansible_user }}"

- name: Setup Database Servers
  hosts: db
  become: yes
  
  tasks:
    - name: Install PostgreSQL
      apt:
        name:
          - postgresql
          - postgresql-contrib
          - python3-psycopg2
        state: present
    
    - name: Start and enable PostgreSQL
      systemd:
        name: postgresql
        state: started
        enabled: yes
    
    - name: Create database user
      postgresql_user:
        name: "{{ db_user }}"
        password: "{{ db_password }}"
        encrypted: yes
      become_user: postgres
    
    - name: Create database
      postgresql_db:
        name: "{{ db_name }}"
        owner: "{{ db_user }}"
      become_user: postgres
    
    - name: Configure PostgreSQL for remote connections
      lineinfile:
        path: /etc/postgresql/15/main/postgresql.conf
        regexp: "^#?listen_addresses"
        line: "listen_addresses = '*'"
      notify: restart postgresql
    
    - name: Configure PostgreSQL client authentication
      lineinfile:
        path: /etc/postgresql/15/main/pg_hba.conf
        line: "host    all             all             10.0.0.0/16            md5"
      notify: restart postgresql
  
  handlers:
    - name: restart postgresql
      systemd:
        name: postgresql
        state: restarted

- name: Setup Load Balancers
  hosts: load_balancers
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Configure nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
        backup: yes
      notify: restart nginx
    
    - name: Enable site
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
      notify: restart nginx
    
    - name: Remove default site
      file:
        path: /etc/nginx/sites-enabled/default
        state: absent
      notify: restart nginx
    
    - name: Start and enable nginx
      systemd:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted""",

            "ansible/templates/docker-compose.yml.j2": """version: '3.8'

services:
  frontend:
    image: {{ registry }}/{{ app_name }}-frontend:{{ app_version }}
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://{{ ansible_default_ipv4.address }}:8000
    restart: unless-stopped
    depends_on:
      - backend

  backend:
    image: {{ registry }}/{{ app_name }}-backend:{{ app_version }}
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://{{ db_user }}:{{ db_password }}@{{ db_host }}:5432/{{ db_name }}
      - SECRET_KEY={{ secret_key }}
      - DEBUG=false
    restart: unless-stopped
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --requirepass {{ redis_password }}
    restart: unless-stopped""",

            "ansible/group_vars/all.yml": """# Application configuration
app_name: myapp
app_version: latest
registry: your-registry

# Database configuration
db_host: "{{ hostvars[groups['db'][0]]['ansible_default_ipv4']['address'] }}"
db_name: appdb
db_user: appuser
db_password: "{{ vault_db_password }}"

# Security
secret_key: "{{ vault_secret_key }}"
redis_password: "{{ vault_redis_password }}"

# SSL configuration
ssl_certificate_path: /etc/ssl/certs/{{ app_name }}.crt
ssl_private_key_path: /etc/ssl/private/{{ app_name }}.key"""
        }
    
    def _get_prometheus_grafana_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate Prometheus and Grafana monitoring configuration"""
        return {
            "monitoring/prometheus-config.yml": """global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  # Application metrics
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: /metrics
    scrape_interval: 5s

  # Postgres Exporter
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  # Redis Exporter
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # Nginx metrics
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']

  # Kubernetes API server (if running on K8s)
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
    - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
      action: keep
      regex: default;kubernetes;https""",

            "monitoring/alert_rules.yml": """groups:
- name: application_alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected
      description: "Error rate is {{ $value }} errors per second"

  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: High response time detected
      description: "95th percentile response time is {{ $value }} seconds"

  - alert: DatabaseConnectionFailure
    expr: up{job="postgres"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: Database connection failure
      description: "PostgreSQL database is not responding"

  - alert: RedisDown
    expr: up{job="redis"} == 0
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: Redis is down
      description: "Redis cache is not responding"

  - alert: HighCPUUsage
    expr: (100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: High CPU usage
      description: "CPU usage is {{ $value }}%"

  - alert: HighMemoryUsage
    expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: High memory usage
      description: "Memory usage is {{ $value }}%"

  - alert: DiskSpaceLow
    expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: Low disk space
      description: "Disk space is {{ $value }}% available"

- name: kubernetes_alerts
  rules:
  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Pod is crash looping
      description: "Pod {{ $labels.pod }} is crash looping in namespace {{ $labels.namespace }}"

  - alert: PodNotReady
    expr: kube_pod_status_ready{condition="false"} == 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Pod not ready
      description: "Pod {{ $labels.pod }} is not ready in namespace {{ $labels.namespace }}"

  - alert: NodeNotReady
    expr: kube_node_status_condition{condition="Ready",status="true"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: Node not ready
      description: "Node {{ $labels.node }} is not ready"

  - alert: DeploymentReplicasMismatch
    expr: kube_deployment_spec_replicas != kube_deployment_status_available_replicas
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Deployment replicas mismatch
      description: "Deployment {{ $labels.deployment }} has {{ $value }} available replicas, expected {{ $labels.spec_replicas }}"

  - alert: HorizontalPodAutoscalerScalingLimited
    expr: kube_hpa_status_current_replicas == kube_hpa_spec_max_replicas
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: HPA scaling limited
      description: "HPA {{ $labels.hpa }} in namespace {{ $labels.namespace }} has reached maximum replicas"

  - alert: PersistentVolumeClaimPending
    expr: kube_persistentvolumeclaim_status_phase{phase="Pending"} == 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: PVC pending
      description: "PVC {{ $labels.persistentvolumeclaim }} in namespace {{ $labels.namespace }} is pending"
""",

            "monitoring/grafana/dashboards/application-dashboard.json": """{
  "dashboard": {
    "id": null,
    "title": "Application Monitoring Dashboard",
    "tags": ["application", "monitoring"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "yAxes": [
          {
            "label": "Requests/sec",
            "min": 0
          }
        ],
        "xAxis": {
          "mode": "time"
        },
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 0
        }
      },
      {
        "id": 2,
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ],
        "yAxes": [
          {
            "label": "Seconds",
            "min": 0
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 0
        }
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ],
        "thresholds": [
          {
            "value": 1,
            "color": "green"
          },
          {
            "value": 5,
            "color": "yellow"
          },
          {
            "value": 10,
            "color": "red"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 6,
          "x": 0,
          "y": 8
        }
      },
      {
        "id": 4,
        "title": "Active Connections",
        "type": "singlestat",
        "targets": [
          {
            "expr": "sum(up{job=\"backend\"})",
            "legendFormat": "Active Instances"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 6,
          "x": 6,
          "y": 8
        }
      },
      {
        "id": 5,
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(1 - rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "yAxes": [
          {
            "label": "Percent",
            "min": 0,
            "max": 100
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 8
        }
      },
      {
        "id": 6,
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "yAxes": [
          {
            "label": "Percent",
            "min": 0,
            "max": 100
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 16
        }
      },
      {
        "id": 7,
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends",
            "legendFormat": "{{datname}}"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 16
        }
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "10s"
  }
}""",

            "monitoring/docker-compose.monitoring.yml": """version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus-config.yml:/etc/prometheus/prometheus.yml:ro
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    restart: unless-stopped
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./grafana/datasources:/etc/grafana/provisioning/datasources:ro
    restart: unless-stopped
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
      - '--web.external-url=http://localhost:9093'
    restart: unless-stopped
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  monitoring:
    driver: bridge"""
        }
    
    def _get_elk_stack_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate ELK Stack logging configuration"""
        return {
            "logging/docker-compose.elk.yml": """version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.4
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
      - xpack.security.enrollment.enabled=false
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - elk
    restart: unless-stopped

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.4
    container_name: logstash
    ports:
      - "5000:5000"
      - "5044:5044"
      - "9600:9600"
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/config:/usr/share/logstash/config:ro
    networks:
      - elk
    depends_on:
      - elasticsearch
    restart: unless-stopped

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.4
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - xpack.security.enabled=false
    networks:
      - elk
    depends_on:
      - elasticsearch
    restart: unless-stopped

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.10.4
    container_name: filebeat
    user: root
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - elk
    depends_on:
      - elasticsearch
      - logstash
    restart: unless-stopped

volumes:
  elasticsearch_data:

networks:
  elk:
    driver: bridge""",

            "logging/logstash/config/logstash.yml": """http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: ["http://elasticsearch:9200"]""",

            "logging/logstash/pipeline/logstash.conf": """input {
  beats {
    port => 5044
  }
  
  tcp {
    port => 5000
    codec => json
  }
}

filter {
  if [container][name] == "backend" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{WORD:level} - %{GREEDYDATA:log_message}" }
    }
    
    date {
      match => [ "timestamp", "yyyy-MM-dd HH:mm:ss,SSS" ]
    }
  }
  
  if [container][name] == "nginx" {
    grok {
      match => { "message" => "%{NGINXACCESS}" }
    }
  }
  
  # Parse JSON logs
  if [message] =~ /^{.*}$/ {
    json {
      source => "message"
    }
  }
  
  # Add environment information
  mutate {
    add_field => { "environment" => "production" }
    add_field => { "application" => "myapp" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "myapp-logs-%{+YYYY.MM.dd}"
  }
  
  stdout {
    codec => rubydebug
  }
}""",

            "logging/filebeat/filebeat.yml": """filebeat.inputs:
- type: container
  paths:
    - /var/lib/docker/containers/*/*.log
  processors:
    - add_docker_metadata:
        host: "unix:///var/run/docker.sock"

output.logstash:
  hosts: ["logstash:5044"]

logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0644"""
        }
    
    def _get_additional_devops_files(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Generate additional DevOps utility files"""
        return {
            "scripts/deploy.sh": """#!/bin/bash
set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
REGISTRY=${REGISTRY:-your-registry}
APP_NAME=${APP_NAME:-myapp}

echo -e "${BLUE}Starting deployment to ${ENVIRONMENT}${NC}"
echo -e "${BLUE}Version: ${VERSION}${NC}"

# Function to print colored output
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Validate environment
case $ENVIRONMENT in
    staging|production)
        log "Deploying to ${ENVIRONMENT} environment"
        ;;
    *)
        error "Invalid environment. Use 'staging' or 'production'"
        ;;
esac

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    error "Docker is not running"
fi

# Check if kubectl is available and configured
if ! kubectl cluster-info > /dev/null 2>&1; then
    error "kubectl is not configured or cluster is not accessible"
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    error "Helm is not installed"
fi

# Build and push images
log "Building Docker images..."
docker build -f docker/Dockerfile.backend -t $REGISTRY/$APP_NAME-backend:$VERSION .
docker build -f docker/Dockerfile.frontend -t $REGISTRY/$APP_NAME-frontend:$VERSION .

log "Pushing images to registry..."
docker push $REGISTRY/$APP_NAME-backend:$VERSION
docker push $REGISTRY/$APP_NAME-frontend:$VERSION

# Run security scan
log "Running security scan..."
if command -v trivy &> /dev/null; then
    trivy image --exit-code 1 --severity HIGH,CRITICAL $REGISTRY/$APP_NAME-backend:$VERSION
    trivy image --exit-code 1 --severity HIGH,CRITICAL $REGISTRY/$APP_NAME-frontend:$VERSION
else
    warn "Trivy not installed, skipping security scan"
fi

# Deploy with Helm
log "Deploying to Kubernetes..."
helm upgrade --install $APP_NAME-$ENVIRONMENT ./helm \\
    --set image.backend.tag=$VERSION \\
    --set image.frontend.tag=$VERSION \\
    --set environment=$ENVIRONMENT \\
    --namespace $ENVIRONMENT \\
    --create-namespace \\
    --wait \\
    --timeout=10m

# Verify deployment
log "Verifying deployment..."
kubectl rollout status deployment/$APP_NAME-backend-deployment -n $ENVIRONMENT
kubectl rollout status deployment/$APP_NAME-frontend-deployment -n $ENVIRONMENT

# Run health checks
log "Running health checks..."
sleep 30

BACKEND_URL=$(kubectl get service $APP_NAME-backend-service -n $ENVIRONMENT -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL=$(kubectl get service $APP_NAME-backend-service -n $ENVIRONMENT -o jsonpath='{.spec.clusterIP}')
    kubectl port-forward service/$APP_NAME-backend-service 8000:8000 -n $ENVIRONMENT &
    PORT_FORWARD_PID=$!
    BACKEND_URL="localhost"
fi

# Wait for service to be ready
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -f http://$BACKEND_URL:8000/health > /dev/null 2>&1; then
        log "Health check passed"
        break
    fi
    attempt=$((attempt + 1))
    echo "Waiting for service to be ready... ($attempt/$max_attempts)"
    sleep 10
done

# Clean up port forward if used
if [ ! -z "$PORT_FORWARD_PID" ]; then
    kill $PORT_FORWARD_PID
fi

if [ $attempt -eq $max_attempts ]; then
    error "Health check failed after $max_attempts attempts"
fi

log "Deployment completed successfully!"
echo -e "${GREEN}Application is deployed and healthy at: http://$BACKEND_URL${NC}"

# Show useful commands
echo -e "${BLUE}Useful commands:${NC}"
echo -e "  kubectl get pods -n $ENVIRONMENT"
echo -e "  kubectl logs -f deployment/$APP_NAME-backend-deployment -n $ENVIRONMENT"
echo -e "  kubectl port-forward service/$APP_NAME-frontend-service 3000:80 -n $ENVIRONMENT"
echo -e "  helm rollback $APP_NAME-$ENVIRONMENT -n $ENVIRONMENT"
""",

            "scripts/rollback.sh": """#!/bin/bash
set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-staging}
REVISION=${2:-}
APP_NAME=${APP_NAME:-myapp}

echo -e "${BLUE}Starting rollback for ${ENVIRONMENT}${NC}"

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Validate environment
case $ENVIRONMENT in
    staging|production)
        log "Rolling back ${ENVIRONMENT} environment"
        ;;
    *)
        error "Invalid environment. Use 'staging' or 'production'"
        ;;
esac

# Check if helm is available
if ! command -v helm &> /dev/null; then
    error "Helm is not installed"
fi

# Show current release history
log "Current release history:"
helm history $APP_NAME-$ENVIRONMENT -n $ENVIRONMENT

# Determine revision to rollback to
if [ -z "$REVISION" ]; then
    log "No revision specified, rolling back to previous version"
    ROLLBACK_CMD="helm rollback $APP_NAME-$ENVIRONMENT -n $ENVIRONMENT"
else
    log "Rolling back to revision $REVISION"
    ROLLBACK_CMD="helm rollback $APP_NAME-$ENVIRONMENT $REVISION -n $ENVIRONMENT"
fi

# Confirm rollback
if [ "$ENVIRONMENT" == "production" ]; then
    echo -e "${YELLOW}WARNING: You are about to rollback production!${NC}"
    read -p "Are you sure you want to continue? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Rollback cancelled"
        exit 0
    fi
fi

# Execute rollback
log "Executing rollback..."
$ROLLBACK_CMD --wait --timeout=10m

# Verify rollback
log "Verifying rollback..."
kubectl rollout status deployment/$APP_NAME-backend-deployment -n $ENVIRONMENT
kubectl rollout status deployment/$APP_NAME-frontend-deployment -n $ENVIRONMENT

log "Rollback completed successfully!"

# Show updated history
log "Updated release history:"
helm history $APP_NAME-$ENVIRONMENT -n $ENVIRONMENT
""",

            "scripts/monitoring-setup.sh": """#!/bin/bash
set -e

# Setup monitoring stack
echo "Setting up monitoring stack..."

# Create monitoring namespace
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Prometheus
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \\
    --namespace monitoring \\
    --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \\
    --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \\
    --set prometheus.prometheusSpec.retention=30d \\
    --set grafana.adminPassword=admin123 \\
    --wait

# Install additional exporters
helm upgrade --install node-exporter prometheus-community/prometheus-node-exporter \\
    --namespace monitoring

# Create ServiceMonitor for the application
cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-backend-monitor
  namespace: monitoring
  labels:
    app: myapp-backend
spec:
  selector:
    matchLabels:
      app: myapp-backend
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
EOF

echo "Monitoring stack setup completed!"
echo "Access Grafana at: http://localhost:3000 (admin/admin123)"
echo "Port forward command: kubectl port-forward service/prometheus-grafana 3000:80 -n monitoring"
""",

            ".dockerignore": """# Git
.git
.gitignore

# Documentation
*.md
docs/
.github/

# Development
.env*
.vscode/
.idea/
*.log

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
.pytest_cache/

# Build artifacts
dist/
build/
*.egg-info/

# DevOps files
devops/
k8s/
helm/
terraform/
ansible/
monitoring/
scripts/

# OS
.DS_Store
Thumbs.db
""",

            "README.md": f"""# DevOps Configuration

This directory contains comprehensive DevOps configurations for deploying and managing the application infrastructure.

## 🛠️ Technologies

- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes with Helm charts
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins
- **Infrastructure as Code**: Terraform, Ansible
- **Monitoring**: Prometheus & Grafana, ELK Stack
- **Security**: Trivy scanning, Security policies

## 📁 Directory Structure

```
devops/
├── docker/                  # Docker configurations
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
├── k8s/                     # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── deployments/
├── helm/                    # Helm charts
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── terraform/               # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ansible/                 # Configuration management
│   ├── inventory.yml
│   ├── playbook.yml
│   └── roles/
├── monitoring/              # Monitoring setup
│   ├── prometheus-config.yml
│   ├── grafana/
│   └── elk/
├── .github/workflows/       # CI/CD pipelines
└── scripts/                 # Utility scripts
```

## 🚀 Quick Start

### Local Development with Docker

```bash
# Build and run the full stack
docker-compose -f docker/docker-compose.yml up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: localhost:5432
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Or use Helm
helm install myapp ./helm --namespace production --create-namespace
```

### Infrastructure Provisioning

```bash
# Initialize Terraform
cd terraform/
terraform init

# Plan and apply infrastructure
terraform plan
terraform apply
```

## 🔧 Configuration

### Environment Variables

Create environment-specific configuration files:

```bash
# .env.staging
DATABASE_URL=postgresql://user:pass@staging-db:5432/db
SECRET_KEY=staging-secret
DEBUG=true

# .env.production  
DATABASE_URL=postgresql://user:pass@prod-db:5432/db
SECRET_KEY=super-secure-production-secret
DEBUG=false
```

### Secrets Management

Kubernetes secrets are managed via:

```bash
# Create secrets
kubectl create secret generic myapp-secrets \\
  --from-literal=SECRET_KEY=your-secret \\
  --from-literal=DATABASE_PASSWORD=db-password \\
  --namespace=production

# Or use sealed-secrets for GitOps
kubeseal --format yaml < secrets.yaml > sealed-secrets.yaml
```

## 🔄 CI/CD Pipelines

### GitHub Actions

Automatic pipeline triggered on:
- Push to `main` branch
- Pull requests
- Scheduled security scans

Pipeline stages:
1. **Test** - Run unit tests and linting
2. **Security** - Vulnerability scanning
3. **Build** - Build and push Docker images
4. **Deploy** - Deploy to staging/production

### Manual Deployment

```bash
# Deploy to staging
./scripts/deploy.sh staging v1.2.3

# Deploy to production (requires confirmation)
./scripts/deploy.sh production v1.2.3

# Rollback if needed
./scripts/rollback.sh production
```

## 📊 Monitoring & Observability

### Prometheus & Grafana

```bash
# Setup monitoring stack
./scripts/monitoring-setup.sh

# Access Grafana
kubectl port-forward service/prometheus-grafana 3000:80 -n monitoring
# Open: http://localhost:3000 (admin/admin123)
```

### Available Dashboards

- **Application Metrics**: Request rate, response time, error rate
- **Infrastructure**: CPU, memory, disk usage
- **Kubernetes**: Pod status, resource usage, events
- **Database**: Connection count, query performance

### Log Management

ELK Stack for centralized logging:

```bash
# Start ELK stack
docker-compose -f logging/docker-compose.elk.yml up -d

# Access Kibana
# http://localhost:5601
```

## 🔒 Security

### Container Security

- Multi-stage builds for minimal attack surface
- Non-root users in containers
- Regular vulnerability scanning with Trivy
- Security contexts and policies

### Network Security

- Network policies for pod-to-pod communication
- Ingress with TLS termination
- Service mesh ready (Istio/Linkerd)

### Secrets Management

- Kubernetes secrets with encryption at rest
- External secrets operator integration
- Sealed secrets for GitOps workflows

## 🏗️ Infrastructure

### AWS EKS Setup

```bash
cd terraform/
terraform init
terraform apply

# Configure kubectl
aws eks update-kubeconfig --region us-west-2 --name myapp-cluster
```

### Features

- **Auto-scaling**: HPA and cluster autoscaler
- **Load Balancing**: ALB with SSL termination
- **Storage**: EBS CSI driver for persistent volumes
- **Networking**: VPC with private/public subnets
- **Security**: IAM roles and security groups

## 📋 Operational Procedures

### Health Checks

```bash
# Application health
curl http://backend-service:8000/health

# Kubernetes cluster
kubectl get nodes
kubectl get pods --all-namespaces

# Database connectivity
kubectl run test-db --rm -it --image=postgres:15 -- psql $DATABASE_URL
```

### Backup & Recovery

```bash
# Database backup
kubectl create job backup-$(date +%Y%m%d) --from=cronjob/postgres-backup

# Restore from backup
kubectl apply -f restore-job.yaml
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment myapp-backend --replicas=5

# Auto-scaling is configured via HPA
kubectl get hpa
```

## 🚨 Troubleshooting

### Common Issues

1. **Pod not starting**
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Service unreachable**
   ```bash
   kubectl get endpoints
   kubectl port-forward service/<service-name> <local-port>:<service-port>
   ```

3. **Database connection issues**
   ```bash
   kubectl exec -it deployment/postgres -- psql -U postgres
   ```

### Log Analysis

```bash
# Application logs
kubectl logs -f deployment/myapp-backend

# System logs
kubectl logs -n kube-system deployment/coredns

# Events
kubectl get events --sort-by=.metadata.creationTimestamp
```

## 📚 Documentation

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 🤝 Contributing

1. Follow GitOps principles
2. Test all changes in staging first
3. Use semantic versioning for releases
4. Update documentation for any configuration changes

## 📞 Support

For issues and support:
- Check monitoring dashboards first
- Review application and system logs
- Consult runbooks in `/docs/runbooks/`
- Contact DevOps team via Slack #devops
"""
        }

    def __init__(self, config: Dict[str, Any]):
        super().__init__("devops", "DevOps Engineer", config)
        self.technologies = config.get('agents', {}).get('devops', {}).get('technologies', [])
        self.container_platforms = ['docker', 'podman', 'containerd']
        self.orchestrators = ['kubernetes', 'docker-swarm', 'nomad']
        self.ci_cd_platforms = ['github-actions', 'gitlab-ci', 'jenkins', 'azure-devops', 'circleci']
        self.iac_tools = ['terraform', 'ansible', 'pulumi', 'cloudformation']
        self.monitoring_stacks = ['prometheus-grafana', 'elk-stack', 'datadog', 'new-relic']
