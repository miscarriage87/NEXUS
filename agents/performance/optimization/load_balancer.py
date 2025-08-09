
"""
Load Balancer - Request distribution across multiple Ollama instances
"""

import asyncio
import random
from typing import Dict, Any, List, Optional, Callable
import logging
from datetime import datetime, timedelta
import aiohttp
from enum import Enum


class LoadBalancingStrategy(str, Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    RANDOM = "random"
    RESPONSE_TIME = "response_time"


class OllamaInstance:
    """
    Represents an Ollama instance for load balancing
    """
    
    def __init__(self, url: str, weight: float = 1.0):
        self.url = url
        self.weight = weight
        self.active_connections = 0
        self.total_requests = 0
        self.total_response_time = 0.0
        self.error_count = 0
        self.last_error = None
        self.is_healthy = True
        self.last_health_check = datetime.now()
    
    @property
    def avg_response_time(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_response_time / self.total_requests
    
    @property
    def error_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.error_count / self.total_requests
    
    def update_stats(self, response_time: float, success: bool):
        """Update instance statistics"""
        self.total_requests += 1
        self.total_response_time += response_time
        
        if not success:
            self.error_count += 1
            self.last_error = datetime.now()


class LoadBalancer:
    """
    Load balancer for distributing requests across multiple Ollama instances
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.load_balancer")
        
        # Configuration
        self.strategy = LoadBalancingStrategy(self.config.get('strategy', 'round_robin'))
        self.health_check_interval = self.config.get('health_check_interval', 60)  # seconds
        self.max_retries = self.config.get('max_retries', 3)
        self.timeout = self.config.get('timeout', 30)
        
        # Ollama instances
        self.instances: List[OllamaInstance] = []
        self._load_instances_from_config()
        
        # Load balancing state
        self.current_index = 0  # For round robin
        self.health_check_task = None
        
        self.logger.info(f"Load Balancer initialized with {len(self.instances)} instances using {self.strategy} strategy")
    
    def _load_instances_from_config(self):
        """
        Load Ollama instances from configuration
        """
        instances_config = self.config.get('instances', [])
        
        if not instances_config:
            # Default to single local instance
            instances_config = [{'url': 'http://localhost:11434', 'weight': 1.0}]
        
        for instance_config in instances_config:
            url = instance_config.get('url')
            weight = instance_config.get('weight', 1.0)
            
            if url:
                instance = OllamaInstance(url, weight)
                self.instances.append(instance)
                self.logger.info(f"Added Ollama instance: {url} (weight: {weight})")
    
    def add_instance(self, url: str, weight: float = 1.0) -> None:
        """
        Add an Ollama instance to the load balancer
        """
        instance = OllamaInstance(url, weight)
        self.instances.append(instance)
        self.logger.info(f"Added Ollama instance: {url} (weight: {weight})")
    
    def remove_instance(self, url: str) -> bool:
        """
        Remove an Ollama instance from the load balancer
        """
        for i, instance in enumerate(self.instances):
            if instance.url == url:
                del self.instances[i]
                self.logger.info(f"Removed Ollama instance: {url}")
                return True
        return False
    
    async def select_instance(self) -> Optional[OllamaInstance]:
        """
        Select an instance based on the load balancing strategy
        """
        healthy_instances = [instance for instance in self.instances if instance.is_healthy]
        
        if not healthy_instances:
            self.logger.warning("No healthy Ollama instances available")
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._select_round_robin(healthy_instances)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._select_weighted_round_robin(healthy_instances)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._select_least_connections(healthy_instances)
        elif self.strategy == LoadBalancingStrategy.RANDOM:
            return self._select_random(healthy_instances)
        elif self.strategy == LoadBalancingStrategy.RESPONSE_TIME:
            return self._select_best_response_time(healthy_instances)
        else:
            return healthy_instances[0]  # Default fallback
    
    def _select_round_robin(self, instances: List[OllamaInstance]) -> OllamaInstance:
        """Select instance using round robin"""
        instance = instances[self.current_index % len(instances)]
        self.current_index += 1
        return instance
    
    def _select_weighted_round_robin(self, instances: List[OllamaInstance]) -> OllamaInstance:
        """
        Select instance using weighted round robin
        TODO: Implement proper weighted round robin algorithm
        """
        # TODO: Implement weighted selection
        # For now, use simple round robin
        return self._select_round_robin(instances)
    
    def _select_least_connections(self, instances: List[OllamaInstance]) -> OllamaInstance:
        """Select instance with least active connections"""
        return min(instances, key=lambda x: x.active_connections)
    
    def _select_random(self, instances: List[OllamaInstance]) -> OllamaInstance:
        """Select random instance"""
        return random.choice(instances)
    
    def _select_best_response_time(self, instances: List[OllamaInstance]) -> OllamaInstance:
        """Select instance with best average response time"""
        # Prefer instances with some history, but not exclude new ones
        instances_with_history = [i for i in instances if i.total_requests > 0]
        if instances_with_history:
            return min(instances_with_history, key=lambda x: x.avg_response_time)
        else:
            return random.choice(instances)
    
    async def make_request(self, endpoint: str, method: str = "POST", 
                          payload: Dict[str, Any] = None,
                          headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Make a load-balanced request to Ollama instances
        TODO: Implement comprehensive request handling with retries
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            instance = await self.select_instance()
            
            if not instance:
                return {"error": "No healthy Ollama instances available"}
            
            try:
                # Track active connection
                instance.active_connections += 1
                start_time = asyncio.get_event_loop().time()
                
                # Make the request
                url = f"{instance.url}{endpoint}"
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    if method.upper() == "POST":
                        async with session.post(url, json=payload, headers=headers) as response:
                            result = await response.json()
                            
                    elif method.upper() == "GET":
                        async with session.get(url, headers=headers) as response:
                            result = await response.json()
                    else:
                        raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Update statistics
                end_time = asyncio.get_event_loop().time()
                response_time = end_time - start_time
                instance.update_stats(response_time, True)
                
                self.logger.debug(f"Request to {instance.url} completed in {response_time:.3f}s")
                return result
                
            except Exception as e:
                # Update statistics
                end_time = asyncio.get_event_loop().time()
                response_time = end_time - start_time if 'start_time' in locals() else 0
                instance.update_stats(response_time, False)
                
                last_error = e
                self.logger.warning(f"Request to {instance.url} failed: {e}")
                
                # Mark instance as unhealthy if too many errors
                if instance.error_rate > 0.5:  # More than 50% error rate
                    instance.is_healthy = False
                    self.logger.warning(f"Marked instance {instance.url} as unhealthy")
            
            finally:
                # Decrease active connection count
                instance.active_connections = max(0, instance.active_connections - 1)
        
        # All retries failed
        return {"error": f"All retries failed. Last error: {str(last_error)}"}
    
    async def start_health_checks(self) -> None:
        """
        Start periodic health checks for all instances
        """
        if self.health_check_task:
            return  # Already running
        
        self.health_check_task = asyncio.create_task(self._health_check_loop())
        self.logger.info("Started health check monitoring")
    
    async def stop_health_checks(self) -> None:
        """
        Stop periodic health checks
        """
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
            self.health_check_task = None
            self.logger.info("Stopped health check monitoring")
    
    async def _health_check_loop(self) -> None:
        """
        Periodic health check loop
        """
        while True:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(self.health_check_interval)
    
    async def _perform_health_checks(self) -> None:
        """
        Perform health checks on all instances
        """
        for instance in self.instances:
            try:
                start_time = asyncio.get_event_loop().time()
                
                # Simple health check using /api/tags endpoint
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    async with session.get(f"{instance.url}/api/tags") as response:
                        if response.status == 200:
                            instance.is_healthy = True
                            instance.last_health_check = datetime.now()
                            
                            # Update response time
                            end_time = asyncio.get_event_loop().time()
                            response_time = end_time - start_time
                            
                            self.logger.debug(f"Health check passed for {instance.url} ({response_time:.3f}s)")
                        else:
                            instance.is_healthy = False
                            self.logger.warning(f"Health check failed for {instance.url}: HTTP {response.status}")
            
            except Exception as e:
                instance.is_healthy = False
                self.logger.warning(f"Health check failed for {instance.url}: {e}")
    
    def get_instance_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all instances
        """
        stats = []
        
        for instance in self.instances:
            stats.append({
                'url': instance.url,
                'weight': instance.weight,
                'is_healthy': instance.is_healthy,
                'active_connections': instance.active_connections,
                'total_requests': instance.total_requests,
                'avg_response_time': round(instance.avg_response_time, 3),
                'error_rate': round(instance.error_rate * 100, 2),
                'last_health_check': instance.last_health_check.isoformat()
            })
        
        return stats
    
    def get_load_balancer_stats(self) -> Dict[str, Any]:
        """
        Get load balancer statistics
        """
        healthy_count = sum(1 for instance in self.instances if instance.is_healthy)
        total_requests = sum(instance.total_requests for instance in self.instances)
        
        return {
            'strategy': self.strategy,
            'total_instances': len(self.instances),
            'healthy_instances': healthy_count,
            'total_requests': total_requests,
            'health_check_interval': self.health_check_interval,
            'instances': self.get_instance_stats()
        }
