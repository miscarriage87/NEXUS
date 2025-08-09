
"""
Adaptive Model Selector - Intelligente Modell-Auswahl basierend auf Task-Requirements
"""

import asyncio
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

from ..core.ollama_client import ollama_client


class AdaptiveModelSelector:
    """
    Adaptive model selection based on task complexity and performance metrics
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.model_selector")
        
        # Configuration
        self.model_preferences = self.config.get('model_preferences', {})
        self.performance_weights = self.config.get('performance_weights', {
            'response_time': 0.4,
            'accuracy': 0.3,
            'resource_usage': 0.2,
            'context_handling': 0.1
        })
        
        # Model capabilities and performance cache
        self.model_capabilities = {}
        self.model_performance = {}
        self.available_models = []
        
        # Task complexity mapping
        self.complexity_models = {
            'simple': ['qwen2.5-coder:1.5b', 'codellama:7b'],
            'medium': ['qwen2.5-coder:7b', 'codellama:13b'],
            'complex': ['qwen2.5-coder:14b', 'codellama:34b'],
            'enterprise': ['qwen2.5-coder:32b', 'codellama:70b']
        }
        
        self.logger.info("Adaptive Model Selector initialized")
    
    async def select_optimal_model(self, task_complexity: str = "medium", 
                                 context_size: int = 4096,
                                 task_type: str = "general",
                                 performance_requirements: Dict[str, float] = None) -> str:
        """
        Select optimal model for given requirements
        TODO: Implement comprehensive model selection logic
        """
        self.logger.info(f"Selecting model for: complexity={task_complexity}, context={context_size}, type={task_type}")
        
        # Ensure we have available models
        if not self.available_models:
            await self.refresh_available_models()
        
        # TODO: Implement model selection algorithm
        # For now, return simple selection based on complexity
        preferred_models = self.complexity_models.get(task_complexity, self.complexity_models['medium'])
        
        # Check which models are actually available
        available_preferred = [model for model in preferred_models if model in self.available_models]
        
        if available_preferred:
            selected_model = available_preferred[0]
        elif self.available_models:
            selected_model = self.available_models[0]
        else:
            selected_model = "qwen2.5-coder:7b"  # Default fallback
        
        self.logger.info(f"Selected model: {selected_model}")
        return selected_model
    
    async def refresh_available_models(self) -> List[str]:
        """
        Refresh list of available models from Ollama
        """
        try:
            self.available_models = await ollama_client.list_models()
            self.logger.info(f"Found {len(self.available_models)} available models")
            return self.available_models
        except Exception as e:
            self.logger.error(f"Error refreshing available models: {e}")
            return []
    
    async def benchmark_model(self, model: str, test_prompts: List[str] = None) -> Dict[str, Any]:
        """
        Benchmark a model's performance
        TODO: Implement comprehensive model benchmarking
        """
        if test_prompts is None:
            test_prompts = [
                "Write a simple Python function that adds two numbers.",
                "Explain the concept of recursion in programming.",
                "Create a basic REST API endpoint in FastAPI."
            ]
        
        self.logger.info(f"Benchmarking model: {model}")
        
        benchmark_results = {
            "model": model,
            "test_count": len(test_prompts),
            "response_times": [],
            "avg_response_time": 0.0,
            "total_tokens": 0,
            "tokens_per_second": 0.0,
            "success_rate": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        successful_tests = 0
        
        for i, prompt in enumerate(test_prompts):
            try:
                start_time = asyncio.get_event_loop().time()
                
                # Make request to Ollama
                response = await ollama_client.generate(model, prompt)
                
                end_time = asyncio.get_event_loop().time()
                response_time = end_time - start_time
                
                benchmark_results["response_times"].append(response_time)
                
                # Count tokens (approximate)
                response_text = response.get('response', '')
                estimated_tokens = len(response_text.split()) * 1.3  # Rough token estimation
                benchmark_results["total_tokens"] += estimated_tokens
                
                successful_tests += 1
                
                self.logger.debug(f"Test {i+1}/{len(test_prompts)} completed in {response_time:.2f}s")
                
            except Exception as e:
                self.logger.warning(f"Benchmark test {i+1} failed for model {model}: {e}")
        
        # Calculate statistics
        if benchmark_results["response_times"]:
            benchmark_results["avg_response_time"] = sum(benchmark_results["response_times"]) / len(benchmark_results["response_times"])
            total_time = sum(benchmark_results["response_times"])
            benchmark_results["tokens_per_second"] = benchmark_results["total_tokens"] / total_time if total_time > 0 else 0.0
        
        benchmark_results["success_rate"] = (successful_tests / len(test_prompts)) * 100
        
        # Cache benchmark results
        self.model_performance[model] = benchmark_results
        
        self.logger.info(f"Benchmark completed for {model}: {successful_tests}/{len(test_prompts)} tests successful")
        
        return benchmark_results
    
    async def get_model_capabilities(self, model: str) -> Dict[str, Any]:
        """
        Get or determine model capabilities
        TODO: Implement model capability detection
        """
        if model in self.model_capabilities:
            return self.model_capabilities[model]
        
        # TODO: Implement capability detection logic
        # For now, use hardcoded capabilities based on model name
        capabilities = self._infer_capabilities_from_name(model)
        
        self.model_capabilities[model] = capabilities
        return capabilities
    
    def _infer_capabilities_from_name(self, model: str) -> Dict[str, Any]:
        """
        Infer model capabilities from model name
        """
        capabilities = {
            "max_context_size": 4096,
            "specializations": [],
            "parameter_count": "unknown",
            "performance_tier": "medium"
        }
        
        # Parse model name for information
        model_lower = model.lower()
        
        # Context size inference
        if "32k" in model_lower:
            capabilities["max_context_size"] = 32768
        elif "16k" in model_lower:
            capabilities["max_context_size"] = 16384
        elif "8k" in model_lower:
            capabilities["max_context_size"] = 8192
        
        # Parameter count inference
        if "70b" in model_lower:
            capabilities["parameter_count"] = "70B"
            capabilities["performance_tier"] = "enterprise"
        elif "34b" in model_lower:
            capabilities["parameter_count"] = "34B"
            capabilities["performance_tier"] = "complex"
        elif "13b" in model_lower:
            capabilities["parameter_count"] = "13B"
            capabilities["performance_tier"] = "medium"
        elif "7b" in model_lower:
            capabilities["parameter_count"] = "7B"
            capabilities["performance_tier"] = "medium"
        elif "1.5b" in model_lower:
            capabilities["parameter_count"] = "1.5B"
            capabilities["performance_tier"] = "simple"
        
        # Specialization inference
        if "coder" in model_lower or "code" in model_lower:
            capabilities["specializations"].append("code_generation")
        if "chat" in model_lower:
            capabilities["specializations"].append("conversational")
        if "instruct" in model_lower:
            capabilities["specializations"].append("instruction_following")
        
        return capabilities
    
    async def update_model_performance(self, model: str, performance_data: Dict[str, Any]) -> None:
        """
        Update model performance data
        """
        if model not in self.model_performance:
            self.model_performance[model] = {}
        
        self.model_performance[model].update(performance_data)
        self.logger.debug(f"Updated performance data for model: {model}")
    
    def get_model_recommendations(self, requirements: Dict[str, Any]) -> List[Tuple[str, float]]:
        """
        Get ranked model recommendations based on requirements
        TODO: Implement intelligent model ranking
        """
        # TODO: Implement sophisticated ranking algorithm
        recommendations = []
        
        for model in self.available_models:
            score = self._calculate_model_score(model, requirements)
            recommendations.append((model, score))
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def _calculate_model_score(self, model: str, requirements: Dict[str, Any]) -> float:
        """
        Calculate model suitability score based on requirements
        TODO: Implement comprehensive scoring algorithm
        """
        # TODO: Implement sophisticated scoring
        # For now, return a simple score based on availability
        return 1.0 if model in self.available_models else 0.0
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """
        Get model selection statistics
        """
        return {
            "available_models": len(self.available_models),
            "benchmarked_models": len(self.model_performance),
            "cached_capabilities": len(self.model_capabilities),
            "models": self.available_models
        }
