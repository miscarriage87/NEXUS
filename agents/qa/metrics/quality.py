
"""
Quality Metrics Collector - Collection and calculation of code quality metrics
"""

import ast
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime
from collections import defaultdict
import subprocess
import json


class QualityMetric:
    """
    Represents a single quality metric
    """
    
    def __init__(self, name: str, value: float, unit: str = "", 
                 category: str = "general", description: str = ""):
        self.name = name
        self.value = value
        self.unit = unit
        self.category = category
        self.description = description
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'value': self.value,
            'unit': self.unit,
            'category': self.category,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }


class QualityMetricsCollector:
    """
    Collect and calculate various code quality metrics
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.quality_metrics")
        
        # Configuration
        self.enable_external_tools = self.config.get('enable_external_tools', False)
        self.complexity_threshold = self.config.get('complexity_threshold', 10)
        self.maintainability_threshold = self.config.get('maintainability_threshold', 70)
        
        # Metrics history
        self.metrics_history = []
        
        self.logger.info("Quality Metrics Collector initialized")
    
    async def collect_metrics(self, code: str, file_path: str = "", 
                            language: str = "python") -> Dict[str, Any]:
        """
        Collect comprehensive quality metrics for code
        """
        self.logger.info(f"Collecting quality metrics for: {file_path}")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "language": language,
            "code_length": len(code),
            "metrics": {},
            "overall_score": 0.0,
            "quality_grade": "C"
        }
        
        try:
            metrics = []
            
            # Basic metrics
            metrics.extend(await self._collect_basic_metrics(code))
            
            # Complexity metrics
            metrics.extend(await self._collect_complexity_metrics(code, language))
            
            # Maintainability metrics
            metrics.extend(await self._collect_maintainability_metrics(code, language))
            
            # Quality metrics
            metrics.extend(await self._collect_quality_metrics(code, language))
            
            # External tool metrics (if enabled)
            if self.enable_external_tools and file_path:
                metrics.extend(await self._collect_external_metrics(file_path, language))
            
            # Organize metrics by category
            result["metrics"] = self._organize_metrics_by_category(metrics)
            
            # Calculate overall score
            result["overall_score"] = self._calculate_overall_score(metrics)
            result["quality_grade"] = self._calculate_quality_grade(result["overall_score"])
            
            # Store in history
            self.metrics_history.append(result)
            
        except Exception as e:
            self.logger.error(f"Error collecting quality metrics: {e}")
            result["error"] = str(e)
        
        return result
    
    async def _collect_basic_metrics(self, code: str) -> List[QualityMetric]:
        """
        Collect basic code metrics
        """
        metrics = []
        lines = code.split('\n')
        
        # Lines of code
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        code_lines = non_empty_lines - comment_lines
        
        metrics.extend([
            QualityMetric("total_lines", total_lines, "lines", "basic", "Total lines in file"),
            QualityMetric("code_lines", code_lines, "lines", "basic", "Lines containing code"),
            QualityMetric("comment_lines", comment_lines, "lines", "basic", "Lines containing comments"),
            QualityMetric("blank_lines", total_lines - non_empty_lines, "lines", "basic", "Blank lines"),
            QualityMetric("comment_ratio", (comment_lines / max(1, code_lines)) * 100, "%", "basic", "Comment to code ratio")
        ])
        
        return metrics
    
    async def _collect_complexity_metrics(self, code: str, language: str) -> List[QualityMetric]:
        """
        Collect complexity metrics
        """
        metrics = []
        
        if language == "python":
            metrics.extend(await self._collect_python_complexity(code))
        
        return metrics
    
    async def _collect_python_complexity(self, code: str) -> List[QualityMetric]:
        """
        Collect Python-specific complexity metrics
        """
        metrics = []
        
        try:
            tree = ast.parse(code)
            
            # Cyclomatic complexity
            total_complexity = 0
            function_count = 0
            max_complexity = 0
            complex_functions = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_count += 1
                    complexity = self._calculate_cyclomatic_complexity(node)
                    total_complexity += complexity
                    max_complexity = max(max_complexity, complexity)
                    
                    if complexity > self.complexity_threshold:
                        complex_functions += 1
            
            avg_complexity = total_complexity / max(1, function_count)
            
            metrics.extend([
                QualityMetric("cyclomatic_complexity_avg", avg_complexity, "points", "complexity", "Average cyclomatic complexity"),
                QualityMetric("cyclomatic_complexity_max", max_complexity, "points", "complexity", "Maximum cyclomatic complexity"),
                QualityMetric("complex_functions", complex_functions, "count", "complexity", f"Functions with complexity > {self.complexity_threshold}"),
                QualityMetric("total_functions", function_count, "count", "complexity", "Total number of functions")
            ])
            
            # Nesting depth
            max_nesting = self._calculate_max_nesting_depth(tree)
            metrics.append(QualityMetric("max_nesting_depth", max_nesting, "levels", "complexity", "Maximum nesting depth"))
            
            # Class metrics
            class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            metrics.append(QualityMetric("class_count", class_count, "count", "structure", "Number of classes"))
            
        except SyntaxError as e:
            self.logger.warning(f"Could not parse Python code for complexity analysis: {e}")
        
        return metrics
    
    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """
        Calculate cyclomatic complexity for a function
        """
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Decision points increase complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def _calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        """
        Calculate maximum nesting depth
        """
        max_depth = 0
        
        def calculate_depth(node, current_depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                current_depth += 1
            
            for child in ast.iter_child_nodes(node):
                calculate_depth(child, current_depth)
        
        calculate_depth(tree)
        return max_depth
    
    async def _collect_maintainability_metrics(self, code: str, language: str) -> List[QualityMetric]:
        """
        Collect maintainability metrics
        """
        metrics = []
        
        if language == "python":
            metrics.extend(await self._collect_python_maintainability(code))
        
        return metrics
    
    async def _collect_python_maintainability(self, code: str) -> List[QualityMetric]:
        """
        Collect Python maintainability metrics
        """
        metrics = []
        
        try:
            tree = ast.parse(code)
            
            # Function length metrics
            function_lengths = []
            long_functions = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                        length = node.end_lineno - node.lineno + 1
                        function_lengths.append(length)
                        
                        if length > 50:  # Threshold for long function
                            long_functions += 1
            
            if function_lengths:
                avg_function_length = sum(function_lengths) / len(function_lengths)
                max_function_length = max(function_lengths)
                
                metrics.extend([
                    QualityMetric("avg_function_length", avg_function_length, "lines", "maintainability", "Average function length"),
                    QualityMetric("max_function_length", max_function_length, "lines", "maintainability", "Maximum function length"),
                    QualityMetric("long_functions", long_functions, "count", "maintainability", "Functions longer than 50 lines")
                ])
            
            # Parameter count metrics
            parameter_counts = []
            functions_with_many_params = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    param_count = len(node.args.args)
                    parameter_counts.append(param_count)
                    
                    if param_count > 5:  # Threshold
                        functions_with_many_params += 1
            
            if parameter_counts:
                avg_parameters = sum(parameter_counts) / len(parameter_counts)
                metrics.extend([
                    QualityMetric("avg_parameters", avg_parameters, "count", "maintainability", "Average parameters per function"),
                    QualityMetric("functions_many_params", functions_with_many_params, "count", "maintainability", "Functions with >5 parameters")
                ])
        
        except SyntaxError:
            pass
        
        return metrics
    
    async def _collect_quality_metrics(self, code: str, language: str) -> List[QualityMetric]:
        """
        Collect code quality metrics
        """
        metrics = []
        
        # Duplication metrics
        duplication_ratio = self._calculate_duplication_ratio(code)
        metrics.append(QualityMetric("duplication_ratio", duplication_ratio, "%", "quality", "Code duplication ratio"))
        
        # Naming quality (basic heuristic)
        naming_score = self._calculate_naming_score(code, language)
        metrics.append(QualityMetric("naming_score", naming_score, "score", "quality", "Naming quality score (0-100)"))
        
        # TODO: Add more quality metrics
        # - Cohesion metrics
        # - Coupling metrics
        # - Documentation coverage
        # - Test coverage (if test files available)
        
        return metrics
    
    def _calculate_duplication_ratio(self, code: str) -> float:
        """
        Calculate code duplication ratio (simplified)
        """
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        if len(lines) < 2:
            return 0.0
        
        line_counts = defaultdict(int)
        for line in lines:
            if len(line) > 10:  # Only consider non-trivial lines
                line_counts[line] += 1
        
        duplicated_lines = sum(count - 1 for count in line_counts.values() if count > 1)
        duplication_ratio = (duplicated_lines / len(lines)) * 100
        
        return round(duplication_ratio, 2)
    
    def _calculate_naming_score(self, code: str, language: str) -> float:
        """
        Calculate naming quality score (basic heuristic)
        """
        if language != "python":
            return 50.0  # Default score for unsupported languages
        
        try:
            tree = ast.parse(code)
            
            good_names = 0
            total_names = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_names += 1
                    if self._is_good_name(node.name):
                        good_names += 1
                
                elif isinstance(node, ast.ClassDef):
                    total_names += 1
                    if self._is_good_class_name(node.name):
                        good_names += 1
                
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    total_names += 1
                    if self._is_good_variable_name(node.id):
                        good_names += 1
            
            if total_names == 0:
                return 50.0
            
            score = (good_names / total_names) * 100
            return round(score, 1)
        
        except SyntaxError:
            return 50.0
    
    def _is_good_name(self, name: str) -> bool:
        """Check if a function name is good"""
        return (len(name) >= 3 and 
                name.islower() and 
                '_' in name and
                not name.startswith('_') and
                name not in {'func', 'function', 'method'})
    
    def _is_good_class_name(self, name: str) -> bool:
        """Check if a class name is good"""
        return (len(name) >= 3 and 
                name[0].isupper() and
                name.isalnum())
    
    def _is_good_variable_name(self, name: str) -> bool:
        """Check if a variable name is good"""
        poor_names = {'a', 'b', 'c', 'x', 'y', 'z', 'tmp', 'temp', 'data', 'item', 'i', 'j', 'k'}
        return len(name) >= 3 and name not in poor_names
    
    async def _collect_external_metrics(self, file_path: str, language: str) -> List[QualityMetric]:
        """
        Collect metrics using external tools
        TODO: Implement external tool integration
        """
        metrics = []
        
        if language == "python":
            # TODO: Integrate with tools like:
            # - pylint
            # - flake8
            # - mypy
            # - bandit (security)
            pass
        
        return metrics
    
    def _organize_metrics_by_category(self, metrics: List[QualityMetric]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Organize metrics by category
        """
        categorized = defaultdict(list)
        
        for metric in metrics:
            categorized[metric.category].append(metric.to_dict())
        
        return dict(categorized)
    
    def _calculate_overall_score(self, metrics: List[QualityMetric]) -> float:
        """
        Calculate overall quality score
        """
        if not metrics:
            return 0.0
        
        # Weight different categories
        category_weights = {
            'basic': 0.2,
            'complexity': 0.3,
            'maintainability': 0.3,
            'quality': 0.2,
            'structure': 0.1
        }
        
        category_scores = defaultdict(list)
        
        # Normalize metrics to 0-100 scale and group by category
        for metric in metrics:
            normalized_score = self._normalize_metric_score(metric)
            category_scores[metric.category].append(normalized_score)
        
        # Calculate weighted average
        weighted_score = 0.0
        total_weight = 0.0
        
        for category, scores in category_scores.items():
            if scores:
                category_average = sum(scores) / len(scores)
                weight = category_weights.get(category, 0.1)
                weighted_score += category_average * weight
                total_weight += weight
        
        if total_weight > 0:
            overall_score = weighted_score / total_weight
        else:
            overall_score = 0.0
        
        return round(overall_score, 1)
    
    def _normalize_metric_score(self, metric: QualityMetric) -> float:
        """
        Normalize metric value to 0-100 scale
        """
        # Normalization logic based on metric type
        if metric.name == "comment_ratio":
            # 10-30% comments is good
            if 10 <= metric.value <= 30:
                return 100.0
            elif metric.value < 10:
                return max(0, metric.value * 10)
            else:
                return max(0, 100 - (metric.value - 30) * 2)
        
        elif metric.name == "cyclomatic_complexity_avg":
            # Lower complexity is better
            return max(0, 100 - metric.value * 10)
        
        elif metric.name == "max_nesting_depth":
            # Lower nesting is better
            return max(0, 100 - metric.value * 20)
        
        elif metric.name == "duplication_ratio":
            # Lower duplication is better
            return max(0, 100 - metric.value * 5)
        
        elif metric.name in ["naming_score"]:
            # Already normalized to 0-100
            return metric.value
        
        else:
            # Default normalization for positive metrics
            return min(100.0, metric.value)
    
    def _calculate_quality_grade(self, score: float) -> str:
        """
        Calculate quality grade based on score
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def get_metrics_summary(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get summary of recent metrics
        """
        recent_metrics = self.metrics_history[-limit:]
        
        if not recent_metrics:
            return {"message": "No metrics collected yet"}
        
        scores = [m.get("overall_score", 0) for m in recent_metrics]
        
        return {
            "total_files_analyzed": len(recent_metrics),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "grade_distribution": self._calculate_grade_distribution(recent_metrics)
        }
    
    def _calculate_grade_distribution(self, metrics_list: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate distribution of quality grades
        """
        grades = [m.get("quality_grade", "F") for m in metrics_list]
        distribution = defaultdict(int)
        
        for grade in grades:
            distribution[grade] += 1
        
        return dict(distribution)
    
    def get_collector_statistics(self) -> Dict[str, Any]:
        """
        Get quality metrics collector statistics
        """
        return {
            "enable_external_tools": self.enable_external_tools,
            "complexity_threshold": self.complexity_threshold,
            "maintainability_threshold": self.maintainability_threshold,
            "metrics_history_count": len(self.metrics_history),
            "supported_languages": ["python"]  # Add more as implemented
        }
