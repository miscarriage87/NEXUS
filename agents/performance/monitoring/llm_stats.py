
"""
LLM Stats Collector - LLM-specific performance statistics
"""

import time
import asyncio
from typing import Dict, Any, List, Optional, Callable
import logging
from datetime import datetime, timedelta
from collections import defaultdict, deque


class LLMStatsCollector:
    """
    Collector for LLM-specific performance statistics
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.llm_stats")
        
        # Configuration
        self.max_history = self.config.get('max_history', 1000)
        self.track_token_usage = self.config.get('track_token_usage', True)
        
        # Statistics storage
        self.request_history = deque(maxlen=self.max_history)
        self.model_stats = defaultdict(lambda: {
            'requests': 0,
            'total_time': 0.0,
            'total_tokens': 0,
            'errors': 0,
            'avg_response_time': 0.0,
            'tokens_per_second': 0.0
        })
        
        self.logger.info("LLM Stats Collector initialized")
    
    def start_request_tracking(self, model: str, prompt: str = "", context_size: int = 0) -> str:
        """
        Start tracking an LLM request
        """
        request_id = f"{int(time.time() * 1000)}_{len(self.request_history)}"
        
        request_info = {
            'request_id': request_id,
            'model': model,
            'prompt_length': len(prompt),
            'context_size': context_size,
            'start_time': time.time(),
            'status': 'in_progress'
        }
        
        self.request_history.append(request_info)
        self.logger.debug(f"Started tracking request {request_id} for model {model}")
        
        return request_id
    
    def end_request_tracking(self, request_id: str, response: str = "", tokens_used: int = 0, 
                           error: Optional[str] = None) -> Dict[str, Any]:
        """
        End tracking an LLM request and record statistics
        """
        # Find the request in history
        request_info = None
        for req in reversed(self.request_history):
            if req.get('request_id') == request_id:
                request_info = req
                break
        
        if not request_info:
            self.logger.warning(f"Request {request_id} not found in tracking history")
            return {"error": "Request not found"}
        
        end_time = time.time()
        duration = end_time - request_info['start_time']
        
        # Update request info
        request_info.update({
            'end_time': end_time,
            'duration': duration,
            'response_length': len(response),
            'tokens_used': tokens_used,
            'error': error,
            'status': 'error' if error else 'completed'
        })
        
        # Update model statistics
        model = request_info['model']
        stats = self.model_stats[model]
        
        stats['requests'] += 1
        stats['total_time'] += duration
        
        if error:
            stats['errors'] += 1
        else:
            stats['total_tokens'] += tokens_used
        
        # Calculate averages
        if stats['requests'] > 0:
            stats['avg_response_time'] = stats['total_time'] / stats['requests']
        
        if stats['total_time'] > 0:
            stats['tokens_per_second'] = stats['total_tokens'] / stats['total_time']
        
        self.logger.debug(f"Completed tracking request {request_id}: {duration:.2f}s, {tokens_used} tokens")
        
        return {
            'request_id': request_id,
            'duration': duration,
            'tokens_used': tokens_used,
            'status': request_info['status']
        }
    
    def get_model_statistics(self, model: str = None) -> Dict[str, Any]:
        """
        Get statistics for a specific model or all models
        """
        if model:
            if model not in self.model_stats:
                return {"error": f"No statistics found for model {model}"}
            
            stats = self.model_stats[model].copy()
            stats['model'] = model
            return stats
        else:
            # Return all model statistics
            return {model: stats.copy() for model, stats in self.model_stats.items()}
    
    def get_recent_requests(self, count: int = 10, model: str = None) -> List[Dict[str, Any]]:
        """
        Get recent request history
        """
        requests = list(self.request_history)
        
        # Filter by model if specified
        if model:
            requests = [req for req in requests if req.get('model') == model]
        
        # Return most recent requests
        return requests[-count:]
    
    def calculate_performance_metrics(self, time_window: timedelta = None) -> Dict[str, Any]:
        """
        Calculate performance metrics over a time window
        TODO: Implement comprehensive performance metrics calculation
        """
        if time_window is None:
            time_window = timedelta(hours=1)
        
        cutoff_time = time.time() - time_window.total_seconds()
        
        # Filter recent requests
        recent_requests = [
            req for req in self.request_history
            if req.get('start_time', 0) >= cutoff_time and req.get('status') == 'completed'
        ]
        
        if not recent_requests:
            return {
                "time_window": str(time_window),
                "total_requests": 0,
                "metrics": {}
            }
        
        # Calculate metrics
        total_requests = len(recent_requests)
        total_duration = sum(req.get('duration', 0) for req in recent_requests)
        total_tokens = sum(req.get('tokens_used', 0) for req in recent_requests)
        
        durations = [req.get('duration', 0) for req in recent_requests]
        
        metrics = {
            "time_window": str(time_window),
            "total_requests": total_requests,
            "avg_response_time": total_duration / total_requests if total_requests > 0 else 0,
            "total_tokens": total_tokens,
            "tokens_per_second": total_tokens / total_duration if total_duration > 0 else 0,
            "requests_per_minute": (total_requests / time_window.total_seconds()) * 60 if time_window.total_seconds() > 0 else 0,
            "min_response_time": min(durations) if durations else 0,
            "max_response_time": max(durations) if durations else 0
        }
        
        # Per-model breakdown
        model_breakdown = defaultdict(list)
        for req in recent_requests:
            model_breakdown[req.get('model', 'unknown')].append(req)
        
        metrics["by_model"] = {}
        for model, requests in model_breakdown.items():
            model_durations = [req.get('duration', 0) for req in requests]
            model_tokens = sum(req.get('tokens_used', 0) for req in requests)
            model_duration_sum = sum(model_durations)
            
            metrics["by_model"][model] = {
                "requests": len(requests),
                "avg_response_time": model_duration_sum / len(requests) if requests else 0,
                "total_tokens": model_tokens,
                "tokens_per_second": model_tokens / model_duration_sum if model_duration_sum > 0 else 0
            }
        
        return metrics
    
    def reset_statistics(self) -> None:
        """
        Reset all statistics (useful for testing)
        """
        self.request_history.clear()
        self.model_stats.clear()
        self.logger.info("LLM statistics reset")
    
    def export_statistics(self) -> Dict[str, Any]:
        """
        Export all statistics for persistence
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "request_history": list(self.request_history),
            "model_stats": dict(self.model_stats)
        }
