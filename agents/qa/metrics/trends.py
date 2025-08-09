
"""
Quality Trend Analyzer - Analysis of quality trends over time
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import statistics

from .quality import QualityMetric


class TrendPoint:
    """
    Represents a single point in a quality trend
    """
    
    def __init__(self, timestamp: datetime, value: float, metadata: Dict[str, Any] = None):
        self.timestamp = timestamp
        self.value = value
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'value': self.value,
            'metadata': self.metadata
        }


class QualityTrendAnalyzer:
    """
    Analyze quality trends over time and provide insights
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.trend_analyzer")
        
        # Configuration
        self.max_history_days = self.config.get('max_history_days', 30)
        self.trend_sensitivity = self.config.get('trend_sensitivity', 0.1)
        self.significant_change_threshold = self.config.get('significant_change_threshold', 10.0)
        
        # Trend data storage
        self.quality_trends = defaultdict(list)  # metric_name -> [TrendPoint]
        self.project_trends = defaultdict(lambda: defaultdict(list))  # project -> metric -> [TrendPoint]
        
        self.logger.info("Quality Trend Analyzer initialized")
    
    def add_quality_data(self, project_id: str, metrics: List[QualityMetric], 
                        timestamp: Optional[datetime] = None) -> None:
        """
        Add quality data point for trend analysis
        """
        timestamp = timestamp or datetime.now()
        
        for metric in metrics:
            # Add to global trends
            trend_point = TrendPoint(timestamp, metric.value, {
                'project_id': project_id,
                'category': metric.category,
                'unit': metric.unit,
                'description': metric.description
            })
            
            self.quality_trends[metric.name].append(trend_point)
            
            # Add to project-specific trends
            self.project_trends[project_id][metric.name].append(trend_point)
        
        # Cleanup old data
        self._cleanup_old_data()
        
        self.logger.debug(f"Added quality data for project {project_id} with {len(metrics)} metrics")
    
    def _cleanup_old_data(self) -> None:
        """
        Remove data older than max_history_days
        """
        cutoff_date = datetime.now() - timedelta(days=self.max_history_days)
        
        # Cleanup global trends
        for metric_name in self.quality_trends:
            self.quality_trends[metric_name] = [
                point for point in self.quality_trends[metric_name]
                if point.timestamp >= cutoff_date
            ]
        
        # Cleanup project trends
        for project_id in self.project_trends:
            for metric_name in self.project_trends[project_id]:
                self.project_trends[project_id][metric_name] = [
                    point for point in self.project_trends[project_id][metric_name]
                    if point.timestamp >= cutoff_date
                ]
    
    def analyze_trend(self, metric_name: str, project_id: Optional[str] = None,
                     time_window_days: int = 7) -> Dict[str, Any]:
        """
        Analyze trend for a specific metric
        """
        self.logger.info(f"Analyzing trend for metric: {metric_name}, project: {project_id}")
        
        # Get data points
        if project_id:
            data_points = self.project_trends[project_id].get(metric_name, [])
        else:
            data_points = self.quality_trends.get(metric_name, [])
        
        if not data_points:
            return {"error": f"No data available for metric {metric_name}"}
        
        # Filter by time window
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        filtered_points = [p for p in data_points if p.timestamp >= cutoff_date]
        
        if len(filtered_points) < 2:
            return {"error": f"Insufficient data points for trend analysis (need >= 2, got {len(filtered_points)})"}
        
        return self._calculate_trend_analysis(metric_name, filtered_points, time_window_days)
    
    def _calculate_trend_analysis(self, metric_name: str, data_points: List[TrendPoint],
                                time_window_days: int) -> Dict[str, Any]:
        """
        Calculate comprehensive trend analysis
        """
        values = [point.value for point in data_points]
        timestamps = [point.timestamp for point in data_points]
        
        # Sort by timestamp
        sorted_data = sorted(zip(timestamps, values))
        sorted_values = [v for _, v in sorted_data]
        
        # Basic statistics
        current_value = sorted_values[-1]
        previous_value = sorted_values[0]
        min_value = min(sorted_values)
        max_value = max(sorted_values)
        avg_value = statistics.mean(sorted_values)
        
        # Trend direction and magnitude
        total_change = current_value - previous_value
        percentage_change = (total_change / max(abs(previous_value), 0.001)) * 100
        
        # Linear trend calculation (simple slope)
        n = len(sorted_values)
        x_values = list(range(n))
        slope = self._calculate_slope(x_values, sorted_values)
        
        # Trend classification
        trend_direction = self._classify_trend_direction(slope, percentage_change)
        trend_strength = self._classify_trend_strength(abs(percentage_change))
        
        # Volatility (standard deviation)
        volatility = statistics.stdev(sorted_values) if len(sorted_values) > 1 else 0.0
        
        # Recent trend (last 3 points if available)
        recent_trend = "stable"
        if len(sorted_values) >= 3:
            recent_values = sorted_values[-3:]
            recent_slope = self._calculate_slope(list(range(3)), recent_values)
            recent_change = (recent_values[-1] - recent_values[0]) / max(abs(recent_values[0]), 0.001) * 100
            recent_trend = self._classify_trend_direction(recent_slope, recent_change)
        
        # Anomaly detection
        anomalies = self._detect_anomalies(sorted_values)
        
        return {
            "metric_name": metric_name,
            "time_window_days": time_window_days,
            "data_points": len(data_points),
            "current_value": current_value,
            "previous_value": previous_value,
            "min_value": min_value,
            "max_value": max_value,
            "average_value": round(avg_value, 3),
            "total_change": round(total_change, 3),
            "percentage_change": round(percentage_change, 2),
            "trend_direction": trend_direction,
            "trend_strength": trend_strength,
            "recent_trend": recent_trend,
            "volatility": round(volatility, 3),
            "slope": round(slope, 6),
            "anomalies_detected": len(anomalies),
            "is_improving": self._is_improving_trend(metric_name, trend_direction),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _calculate_slope(self, x_values: List[int], y_values: List[float]) -> float:
        """
        Calculate linear regression slope
        """
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
        
        n = len(x_values)
        x_mean = sum(x_values) / n
        y_mean = sum(y_values) / n
        
        numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _classify_trend_direction(self, slope: float, percentage_change: float) -> str:
        """
        Classify trend direction based on slope and percentage change
        """
        if abs(percentage_change) < self.trend_sensitivity:
            return "stable"
        elif slope > 0 and percentage_change > 0:
            return "improving"
        elif slope < 0 and percentage_change < 0:
            return "declining"
        else:
            return "volatile"
    
    def _classify_trend_strength(self, abs_percentage_change: float) -> str:
        """
        Classify trend strength based on absolute percentage change
        """
        if abs_percentage_change < 2:
            return "weak"
        elif abs_percentage_change < 10:
            return "moderate"
        elif abs_percentage_change < 25:
            return "strong"
        else:
            return "very_strong"
    
    def _is_improving_trend(self, metric_name: str, trend_direction: str) -> bool:
        """
        Determine if trend direction represents improvement for specific metric
        """
        # Metrics where higher values are better
        higher_is_better = {
            'comment_ratio', 'naming_score', 'documentation_coverage',
            'test_coverage', 'overall_score'
        }
        
        # Metrics where lower values are better
        lower_is_better = {
            'cyclomatic_complexity_avg', 'max_nesting_depth', 'duplication_ratio',
            'long_functions', 'complex_functions', 'functions_many_params'
        }
        
        if metric_name in higher_is_better:
            return trend_direction == "improving"
        elif metric_name in lower_is_better:
            return trend_direction == "declining"  # Declining is good for these metrics
        else:
            return trend_direction == "stable"  # Stable is generally good for unknown metrics
    
    def _detect_anomalies(self, values: List[float]) -> List[int]:
        """
        Detect anomalous values using simple statistical methods
        """
        if len(values) < 5:
            return []
        
        # Calculate z-scores
        mean_val = statistics.mean(values)
        stdev_val = statistics.stdev(values)
        
        if stdev_val == 0:
            return []
        
        anomalies = []
        threshold = 2.0  # Standard deviations
        
        for i, value in enumerate(values):
            z_score = abs((value - mean_val) / stdev_val)
            if z_score > threshold:
                anomalies.append(i)
        
        return anomalies
    
    def analyze_multiple_metrics(self, metric_names: List[str], project_id: Optional[str] = None,
                                time_window_days: int = 7) -> Dict[str, Any]:
        """
        Analyze trends for multiple metrics
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "project_id": project_id,
            "time_window_days": time_window_days,
            "metrics_analyzed": len(metric_names),
            "metric_trends": {},
            "summary": {}
        }
        
        improving_count = 0
        declining_count = 0
        stable_count = 0
        
        for metric_name in metric_names:
            trend_analysis = self.analyze_trend(metric_name, project_id, time_window_days)
            
            if "error" not in trend_analysis:
                results["metric_trends"][metric_name] = trend_analysis
                
                # Count trend types
                if trend_analysis.get("is_improving", False):
                    improving_count += 1
                elif trend_analysis.get("trend_direction") == "declining":
                    declining_count += 1
                else:
                    stable_count += 1
            else:
                results["metric_trends"][metric_name] = trend_analysis
        
        # Summary
        results["summary"] = {
            "improving_metrics": improving_count,
            "declining_metrics": declining_count,
            "stable_metrics": stable_count,
            "overall_trend": self._classify_overall_trend(improving_count, declining_count, stable_count)
        }
        
        return results
    
    def _classify_overall_trend(self, improving: int, declining: int, stable: int) -> str:
        """
        Classify overall trend across multiple metrics
        """
        total = improving + declining + stable
        
        if total == 0:
            return "no_data"
        
        improving_ratio = improving / total
        declining_ratio = declining / total
        
        if improving_ratio > 0.6:
            return "overall_improving"
        elif declining_ratio > 0.6:
            return "overall_declining"
        elif improving_ratio > declining_ratio:
            return "mixed_improving"
        elif declining_ratio > improving_ratio:
            return "mixed_declining"
        else:
            return "mixed_stable"
    
    def get_quality_forecast(self, metric_name: str, project_id: Optional[str] = None,
                           forecast_days: int = 7) -> Dict[str, Any]:
        """
        Generate simple quality forecast based on current trends
        TODO: Implement more sophisticated forecasting
        """
        self.logger.info(f"Generating forecast for metric: {metric_name}")
        
        # Get trend analysis
        trend_analysis = self.analyze_trend(metric_name, project_id, 14)  # Use 2 weeks of data
        
        if "error" in trend_analysis:
            return trend_analysis
        
        current_value = trend_analysis["current_value"]
        slope = trend_analysis["slope"]
        trend_direction = trend_analysis["trend_direction"]
        
        # Simple linear forecast
        forecasted_value = current_value + (slope * forecast_days)
        
        # Calculate confidence based on trend strength and volatility
        confidence = self._calculate_forecast_confidence(trend_analysis)
        
        return {
            "metric_name": metric_name,
            "current_value": current_value,
            "forecasted_value": round(forecasted_value, 3),
            "forecast_days": forecast_days,
            "trend_direction": trend_direction,
            "confidence": confidence,
            "forecast_timestamp": datetime.now().isoformat(),
            "note": "Simple linear forecast - actual results may vary"
        }
    
    def _calculate_forecast_confidence(self, trend_analysis: Dict[str, Any]) -> str:
        """
        Calculate confidence level for forecast
        """
        trend_strength = trend_analysis.get("trend_strength", "weak")
        volatility = trend_analysis.get("volatility", 0)
        data_points = trend_analysis.get("data_points", 0)
        
        # Base confidence on trend strength
        confidence_score = 0
        
        if trend_strength == "very_strong":
            confidence_score += 40
        elif trend_strength == "strong":
            confidence_score += 30
        elif trend_strength == "moderate":
            confidence_score += 20
        else:  # weak
            confidence_score += 10
        
        # Adjust for volatility (lower volatility = higher confidence)
        if volatility < 1:
            confidence_score += 30
        elif volatility < 5:
            confidence_score += 20
        elif volatility < 10:
            confidence_score += 10
        
        # Adjust for data points
        if data_points >= 10:
            confidence_score += 20
        elif data_points >= 5:
            confidence_score += 15
        elif data_points >= 3:
            confidence_score += 10
        
        # Convert to confidence level
        if confidence_score >= 70:
            return "high"
        elif confidence_score >= 50:
            return "medium"
        else:
            return "low"
    
    def get_trend_alerts(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate alerts based on significant trend changes
        """
        alerts = []
        
        # Determine which trends to check
        if project_id:
            trends_to_check = self.project_trends.get(project_id, {})
        else:
            trends_to_check = self.quality_trends
        
        for metric_name, data_points in trends_to_check.items():
            if len(data_points) < 3:
                continue
            
            # Analyze recent trend
            trend_analysis = self.analyze_trend(metric_name, project_id, 3)
            
            if "error" in trend_analysis:
                continue
            
            # Check for significant changes
            percentage_change = abs(trend_analysis.get("percentage_change", 0))
            
            if percentage_change >= self.significant_change_threshold:
                alert_type = "improvement" if trend_analysis.get("is_improving", False) else "degradation"
                
                alerts.append({
                    "metric_name": metric_name,
                    "project_id": project_id,
                    "alert_type": alert_type,
                    "percentage_change": percentage_change,
                    "current_value": trend_analysis["current_value"],
                    "trend_direction": trend_analysis["trend_direction"],
                    "severity": self._calculate_alert_severity(percentage_change),
                    "timestamp": datetime.now().isoformat()
                })
        
        return alerts
    
    def _calculate_alert_severity(self, percentage_change: float) -> str:
        """
        Calculate alert severity based on percentage change
        """
        if percentage_change >= 50:
            return "critical"
        elif percentage_change >= 25:
            return "high"
        elif percentage_change >= 15:
            return "medium"
        else:
            return "low"
    
    def export_trend_data(self, metric_name: str, project_id: Optional[str] = None,
                         format: str = "json") -> Dict[str, Any]:
        """
        Export trend data for external analysis
        """
        # Get data points
        if project_id:
            data_points = self.project_trends[project_id].get(metric_name, [])
        else:
            data_points = self.quality_trends.get(metric_name, [])
        
        if not data_points:
            return {"error": f"No data available for metric {metric_name}"}
        
        export_data = {
            "metric_name": metric_name,
            "project_id": project_id,
            "export_timestamp": datetime.now().isoformat(),
            "data_points": [point.to_dict() for point in data_points],
            "total_points": len(data_points)
        }
        
        if format == "json":
            return export_data
        else:
            return {"error": f"Unsupported export format: {format}"}
    
    def get_trend_statistics(self) -> Dict[str, Any]:
        """
        Get trend analyzer statistics
        """
        total_global_metrics = len(self.quality_trends)
        total_global_points = sum(len(points) for points in self.quality_trends.values())
        
        project_count = len(self.project_trends)
        
        return {
            "max_history_days": self.max_history_days,
            "trend_sensitivity": self.trend_sensitivity,
            "significant_change_threshold": self.significant_change_threshold,
            "global_metrics_tracked": total_global_metrics,
            "total_global_data_points": total_global_points,
            "projects_tracked": project_count,
            "oldest_data": self._get_oldest_data_timestamp(),
            "newest_data": self._get_newest_data_timestamp()
        }
    
    def _get_oldest_data_timestamp(self) -> Optional[str]:
        """Get timestamp of oldest data point"""
        oldest = None
        
        for points in self.quality_trends.values():
            for point in points:
                if oldest is None or point.timestamp < oldest:
                    oldest = point.timestamp
        
        return oldest.isoformat() if oldest else None
    
    def _get_newest_data_timestamp(self) -> Optional[str]:
        """Get timestamp of newest data point"""
        newest = None
        
        for points in self.quality_trends.values():
            for point in points:
                if newest is None or point.timestamp > newest:
                    newest = point.timestamp
        
        return newest.isoformat() if newest else None
