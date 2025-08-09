
"""
Metrics Collector - Performance metrics collection and tracking
"""

import time
import asyncio
from collections import defaultdict, deque
from typing import Dict, Any, List, Optional, Deque
import logging
from datetime import datetime, timedelta


class MetricsCollector:
    """
    Collector for various performance metrics
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.metrics")
        
        # Configuration
        self.retention_period = timedelta(days=self.config.get('retention_days', 7))
        self.max_samples = self.config.get('max_samples', 10000)
        
        # Metrics storage
        self.metrics: Dict[str, Deque] = defaultdict(lambda: deque(maxlen=self.max_samples))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        
        self.logger.info("Metrics Collector initialized")
    
    def record_metric(self, name: str, value: float, timestamp: Optional[datetime] = None, 
                     tags: Dict[str, str] = None) -> None:
        """
        Record a metric value
        """
        timestamp = timestamp or datetime.now()
        tags = tags or {}
        
        metric_entry = {
            'timestamp': timestamp,
            'value': value,
            'tags': tags
        }
        
        self.metrics[name].append(metric_entry)
        self.logger.debug(f"Recorded metric {name}: {value}")
    
    def increment_counter(self, name: str, value: int = 1) -> None:
        """
        Increment a counter metric
        """
        self.counters[name] += value
        self.logger.debug(f"Incremented counter {name} by {value}")
    
    def set_gauge(self, name: str, value: float) -> None:
        """
        Set a gauge metric
        """
        self.gauges[name] = value
        self.logger.debug(f"Set gauge {name}: {value}")
    
    def record_histogram(self, name: str, value: float) -> None:
        """
        Record a value in a histogram
        """
        self.histograms[name].append(value)
        
        # Keep histogram size manageable
        max_histogram_size = self.config.get('max_histogram_size', 1000)
        if len(self.histograms[name]) > max_histogram_size:
            self.histograms[name] = self.histograms[name][-max_histogram_size:]
        
        self.logger.debug(f"Recorded histogram {name}: {value}")
    
    def get_metric_stats(self, name: str, duration: Optional[timedelta] = None) -> Dict[str, Any]:
        """
        Get statistics for a metric over a time duration
        TODO: Implement comprehensive metric statistics
        """
        if name not in self.metrics:
            return {"error": f"Metric {name} not found"}
        
        # TODO: Implement metric statistics calculation
        samples = self.metrics[name]
        if not samples:
            return {"count": 0}
        
        # Filter by duration if specified
        if duration:
            cutoff_time = datetime.now() - duration
            samples = [s for s in samples if s['timestamp'] >= cutoff_time]
        
        if not samples:
            return {"count": 0}
        
        values = [s['value'] for s in samples]
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "latest": values[-1] if values else None
        }
    
    def get_counter_value(self, name: str) -> int:
        """
        Get current counter value
        """
        return self.counters.get(name, 0)
    
    def get_gauge_value(self, name: str) -> Optional[float]:
        """
        Get current gauge value
        """
        return self.gauges.get(name)
    
    def get_histogram_stats(self, name: str) -> Dict[str, Any]:
        """
        Get histogram statistics
        TODO: Implement detailed histogram statistics
        """
        if name not in self.histograms:
            return {"error": f"Histogram {name} not found"}
        
        values = self.histograms[name]
        if not values:
            return {"count": 0}
        
        # TODO: Add percentile calculations
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values)
        }
    
    def cleanup_old_metrics(self) -> int:
        """
        Remove old metrics beyond retention period
        """
        cutoff_time = datetime.now() - self.retention_period
        removed_count = 0
        
        for metric_name, samples in self.metrics.items():
            original_count = len(samples)
            
            # Remove old samples
            while samples and samples[0]['timestamp'] < cutoff_time:
                samples.popleft()
                removed_count += 1
        
        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} old metric samples")
        
        return removed_count
    
    def get_all_metrics_summary(self) -> Dict[str, Any]:
        """
        Get summary of all metrics
        """
        summary = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {}
        }
        
        # Add metrics summaries
        for name in self.metrics:
            summary["metrics"][name] = self.get_metric_stats(name)
        
        # Add histogram summaries
        for name in self.histograms:
            summary["histograms"][name] = self.get_histogram_stats(name)
        
        return summary
    
    def reset_all_metrics(self) -> None:
        """
        Reset all metrics (useful for testing)
        """
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()
        
        self.logger.info("All metrics reset")
