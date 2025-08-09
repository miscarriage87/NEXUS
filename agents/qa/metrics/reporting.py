
"""
Quality Reporter - Generate comprehensive quality reports and visualizations
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import logging
from dataclasses import asdict

from .quality import QualityMetric, QualityMetricsCollector
from .trends import QualityTrendAnalyzer


class QualityReporter:
    """
    Generate comprehensive quality reports and visualizations
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.quality_reporter")
        
        # Configuration
        self.output_directory = Path(self.config.get('output_directory', '/tmp/quality_reports'))
        self.include_charts = self.config.get('include_charts', True)
        self.report_formats = self.config.get('report_formats', ['html', 'json'])
        
        # Create output directory
        self.output_directory.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Quality Reporter initialized with output directory: {self.output_directory}")
    
    async def generate_comprehensive_report(self, project_id: str, 
                                          metrics_data: Dict[str, Any],
                                          trend_data: Optional[Dict[str, Any]] = None,
                                          include_recommendations: bool = True) -> Dict[str, Any]:
        """
        Generate comprehensive quality report
        """
        self.logger.info(f"Generating comprehensive report for project: {project_id}")
        
        report_data = {
            "report_metadata": {
                "project_id": project_id,
                "generation_timestamp": datetime.now().isoformat(),
                "report_type": "comprehensive_quality_report",
                "version": "1.0"
            },
            "executive_summary": {},
            "metrics_analysis": metrics_data,
            "trend_analysis": trend_data or {},
            "recommendations": [],
            "appendices": {}
        }
        
        try:
            # Generate executive summary
            report_data["executive_summary"] = self._generate_executive_summary(
                metrics_data, trend_data
            )
            
            # Generate recommendations
            if include_recommendations:
                report_data["recommendations"] = self._generate_recommendations(
                    metrics_data, trend_data
                )
            
            # Add appendices
            report_data["appendices"] = self._generate_appendices(metrics_data)
            
            # Generate report files
            report_paths = await self._generate_report_files(project_id, report_data)
            
            return {
                "status": "success",
                "project_id": project_id,
                "report_data": report_data,
                "report_files": report_paths,
                "generation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating comprehensive report: {e}")
            return {
                "status": "error",
                "error": str(e),
                "project_id": project_id
            }
    
    def _generate_executive_summary(self, metrics_data: Dict[str, Any],
                                  trend_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate executive summary of quality metrics
        """
        summary = {
            "overall_quality_score": metrics_data.get("overall_score", 0),
            "quality_grade": metrics_data.get("quality_grade", "F"),
            "total_metrics_analyzed": 0,
            "key_strengths": [],
            "key_concerns": [],
            "trend_summary": "No trend data available"
        }
        
        # Count metrics
        metrics_by_category = metrics_data.get("metrics", {})
        summary["total_metrics_analyzed"] = sum(len(category_metrics) 
                                              for category_metrics in metrics_by_category.values())
        
        # Identify strengths and concerns
        summary["key_strengths"], summary["key_concerns"] = self._identify_strengths_and_concerns(
            metrics_by_category
        )
        
        # Add trend summary if available
        if trend_data:
            summary["trend_summary"] = self._summarize_trends(trend_data)
        
        return summary
    
    def _identify_strengths_and_concerns(self, metrics_by_category: Dict[str, List[Dict[str, Any]]]) -> Tuple[List[str], List[str]]:
        """
        Identify key strengths and concerns from metrics
        """
        strengths = []
        concerns = []
        
        for category, category_metrics in metrics_by_category.items():
            for metric in category_metrics:
                metric_name = metric.get("name", "")
                metric_value = metric.get("value", 0)
                
                # Define good/bad thresholds for common metrics
                if metric_name == "comment_ratio":
                    if 15 <= metric_value <= 30:
                        strengths.append(f"Good comment ratio ({metric_value:.1f}%)")
                    elif metric_value < 5:
                        concerns.append(f"Low comment ratio ({metric_value:.1f}%)")
                
                elif metric_name == "cyclomatic_complexity_avg":
                    if metric_value <= 5:
                        strengths.append(f"Low average complexity ({metric_value:.1f})")
                    elif metric_value > 10:
                        concerns.append(f"High average complexity ({metric_value:.1f})")
                
                elif metric_name == "duplication_ratio":
                    if metric_value <= 5:
                        strengths.append(f"Low code duplication ({metric_value:.1f}%)")
                    elif metric_value > 20:
                        concerns.append(f"High code duplication ({metric_value:.1f}%)")
                
                elif metric_name == "naming_score":
                    if metric_value >= 80:
                        strengths.append(f"Good naming conventions ({metric_value:.1f})")
                    elif metric_value < 50:
                        concerns.append(f"Poor naming conventions ({metric_value:.1f})")
        
        # Limit to top items
        return strengths[:5], concerns[:5]
    
    def _summarize_trends(self, trend_data: Dict[str, Any]) -> str:
        """
        Create summary of trend analysis
        """
        if not trend_data or "summary" not in trend_data:
            return "No trend analysis available"
        
        summary_data = trend_data["summary"]
        improving = summary_data.get("improving_metrics", 0)
        declining = summary_data.get("declining_metrics", 0)
        stable = summary_data.get("stable_metrics", 0)
        overall_trend = summary_data.get("overall_trend", "unknown")
        
        trend_descriptions = {
            "overall_improving": "Overall quality is improving",
            "overall_declining": "Overall quality is declining",
            "mixed_improving": "Mixed trends with slight improvement",
            "mixed_declining": "Mixed trends with slight decline",
            "mixed_stable": "Mixed trends, generally stable"
        }
        
        description = trend_descriptions.get(overall_trend, "Trend analysis inconclusive")
        
        return f"{description}. Improving: {improving}, Stable: {stable}, Declining: {declining}"
    
    def _generate_recommendations(self, metrics_data: Dict[str, Any],
                                trend_data: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate actionable recommendations based on metrics and trends
        """
        recommendations = []
        
        overall_score = metrics_data.get("overall_score", 0)
        quality_grade = metrics_data.get("quality_grade", "F")
        metrics_by_category = metrics_data.get("metrics", {})
        
        # Priority recommendations based on overall score
        if overall_score < 60:
            recommendations.append({
                "priority": "high",
                "category": "overall",
                "title": "Critical Quality Issues",
                "description": f"Overall quality score is {overall_score:.1f} (Grade {quality_grade}). Immediate attention required.",
                "actions": [
                    "Focus on addressing high-impact quality issues",
                    "Implement code review processes",
                    "Set up automated quality checks"
                ]
            })
        
        # Complexity recommendations
        complexity_metrics = metrics_by_category.get("complexity", [])
        for metric in complexity_metrics:
            if metric.get("name") == "cyclomatic_complexity_avg" and metric.get("value", 0) > 10:
                recommendations.append({
                    "priority": "medium",
                    "category": "complexity",
                    "title": "High Code Complexity",
                    "description": f"Average cyclomatic complexity is {metric.get('value'):.1f}, which exceeds recommended threshold.",
                    "actions": [
                        "Refactor complex functions into smaller ones",
                        "Use early returns to reduce nesting",
                        "Consider design patterns to simplify logic"
                    ]
                })
        
        # Maintainability recommendations
        maintainability_metrics = metrics_by_category.get("maintainability", [])
        for metric in maintainability_metrics:
            if metric.get("name") == "long_functions" and metric.get("value", 0) > 5:
                recommendations.append({
                    "priority": "medium",
                    "category": "maintainability",
                    "title": "Long Functions Detected",
                    "description": f"Found {int(metric.get('value'))} functions longer than 50 lines.",
                    "actions": [
                        "Break down long functions into smaller, focused functions",
                        "Extract reusable logic into utility functions",
                        "Follow single responsibility principle"
                    ]
                })
        
        # Quality recommendations
        quality_metrics = metrics_by_category.get("quality", [])
        for metric in quality_metrics:
            if metric.get("name") == "duplication_ratio" and metric.get("value", 0) > 15:
                recommendations.append({
                    "priority": "high",
                    "category": "quality",
                    "title": "High Code Duplication",
                    "description": f"Code duplication ratio is {metric.get('value'):.1f}%, indicating significant duplicate code.",
                    "actions": [
                        "Identify and extract common code into shared functions",
                        "Use inheritance or composition to eliminate duplication",
                        "Implement DRY (Don't Repeat Yourself) principle"
                    ]
                })
        
        # Trend-based recommendations
        if trend_data:
            declining_metrics = trend_data.get("summary", {}).get("declining_metrics", 0)
            if declining_metrics > 2:
                recommendations.append({
                    "priority": "medium",
                    "category": "trends",
                    "title": "Declining Quality Trends",
                    "description": f"{declining_metrics} metrics show declining trends.",
                    "actions": [
                        "Review recent code changes for quality regressions",
                        "Strengthen code review process",
                        "Add automated quality gates to CI/CD pipeline"
                    ]
                })
        
        # Sort recommendations by priority
        priority_order = {"high": 3, "medium": 2, "low": 1}
        recommendations.sort(key=lambda r: priority_order.get(r["priority"], 1), reverse=True)
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _generate_appendices(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate appendices with detailed information
        """
        return {
            "metrics_glossary": self._generate_metrics_glossary(),
            "thresholds_used": self._get_quality_thresholds(),
            "calculation_methods": self._get_calculation_methods()
        }
    
    def _generate_metrics_glossary(self) -> Dict[str, str]:
        """
        Generate glossary of metrics used
        """
        return {
            "cyclomatic_complexity_avg": "Average cyclomatic complexity across all functions. Measures code complexity based on decision points.",
            "comment_ratio": "Percentage of comment lines relative to code lines. Indicates documentation quality.",
            "duplication_ratio": "Percentage of duplicated code lines. Higher values indicate more code duplication.",
            "naming_score": "Quality score for variable and function names. Based on naming conventions and clarity.",
            "max_nesting_depth": "Maximum nesting level in code. Deeper nesting can reduce readability.",
            "long_functions": "Count of functions exceeding 50 lines. Long functions may be harder to maintain.",
            "overall_score": "Composite quality score combining all metrics. Range: 0-100."
        }
    
    def _get_quality_thresholds(self) -> Dict[str, Any]:
        """
        Get quality thresholds used in analysis
        """
        return {
            "complexity_threshold": 10,
            "long_function_threshold": 50,
            "high_nesting_threshold": 4,
            "duplication_threshold": 15,
            "comment_ratio_min": 10,
            "comment_ratio_max": 30,
            "naming_score_min": 50
        }
    
    def _get_calculation_methods(self) -> Dict[str, str]:
        """
        Get calculation methods for metrics
        """
        return {
            "overall_score": "Weighted average of normalized category scores",
            "cyclomatic_complexity": "Count of decision points (if/while/for/except) + 1",
            "comment_ratio": "(comment_lines / code_lines) * 100",
            "duplication_ratio": "(duplicated_lines / total_lines) * 100",
            "naming_score": "Percentage of well-named identifiers based on conventions"
        }
    
    async def _generate_report_files(self, project_id: str, report_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate report files in specified formats
        """
        report_paths = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for format_type in self.report_formats:
            if format_type == "json":
                file_path = self.output_directory / f"{project_id}_quality_report_{timestamp}.json"
                with open(file_path, 'w') as f:
                    json.dump(report_data, f, indent=2)
                report_paths["json"] = str(file_path)
            
            elif format_type == "html":
                file_path = self.output_directory / f"{project_id}_quality_report_{timestamp}.html"
                html_content = self._generate_html_report(report_data)
                with open(file_path, 'w') as f:
                    f.write(html_content)
                report_paths["html"] = str(file_path)
            
            elif format_type == "md":
                file_path = self.output_directory / f"{project_id}_quality_report_{timestamp}.md"
                md_content = self._generate_markdown_report(report_data)
                with open(file_path, 'w') as f:
                    f.write(md_content)
                report_paths["markdown"] = str(file_path)
        
        return report_paths
    
    def _generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """
        Generate HTML report content
        """
        metadata = report_data["report_metadata"]
        summary = report_data["executive_summary"]
        recommendations = report_data["recommendations"]
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Report - {metadata['project_id']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
        .summary {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .concern {{ background: #fff2e8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .metric {{ background: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 4px solid #007acc; }}
        .recommendation {{ background: #f0f8ff; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .priority-high {{ border-left: 4px solid #ff4444; }}
        .priority-medium {{ border-left: 4px solid #ffaa44; }}
        .priority-low {{ border-left: 4px solid #44ff44; }}
        .grade-A {{ color: #22aa22; font-weight: bold; }}
        .grade-B {{ color: #88aa22; font-weight: bold; }}
        .grade-C {{ color: #aaaa22; font-weight: bold; }}
        .grade-D {{ color: #aa8822; font-weight: bold; }}
        .grade-F {{ color: #aa2222; font-weight: bold; }}
        ul {{ padding-left: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Code Quality Report</h1>
        <p><strong>Project:</strong> {metadata['project_id']}</p>
        <p><strong>Generated:</strong> {metadata['generation_timestamp']}</p>
        <p><strong>Report Type:</strong> {metadata['report_type']}</p>
    </div>

    <div class="summary">
        <h2>Executive Summary</h2>
        <p><strong>Overall Quality Score:</strong> {summary['overall_quality_score']:.1f}/100</p>
        <p><strong>Quality Grade:</strong> <span class="grade-{summary['quality_grade']}">{summary['quality_grade']}</span></p>
        <p><strong>Metrics Analyzed:</strong> {summary['total_metrics_analyzed']}</p>
        <p><strong>Trend Summary:</strong> {summary['trend_summary']}</p>
        
        <h3>Key Strengths</h3>
        <ul>
            {''.join(f'<li>{strength}</li>' for strength in summary['key_strengths'])}
        </ul>
        
        <h3>Key Concerns</h3>
        <ul>
            {''.join(f'<li>{concern}</li>' for concern in summary['key_concerns'])}
        </ul>
    </div>

    <h2>Recommendations</h2>
    {''.join(self._format_html_recommendation(rec) for rec in recommendations)}
    
    <h2>Detailed Metrics</h2>
    {self._format_html_metrics(report_data['metrics_analysis'])}
    
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; color: #666; font-size: 0.9em;">
        <p>Report generated by NEXUS Quality Assurance Agent</p>
    </div>
</body>
</html>
"""
        return html_content
    
    def _format_html_recommendation(self, recommendation: Dict[str, Any]) -> str:
        """
        Format a single recommendation for HTML
        """
        priority_class = f"priority-{recommendation['priority']}"
        actions_html = ''.join(f'<li>{action}</li>' for action in recommendation['actions'])
        
        return f"""
        <div class="recommendation {priority_class}">
            <h3>{recommendation['title']} ({recommendation['priority'].upper()} PRIORITY)</h3>
            <p><strong>Category:</strong> {recommendation['category']}</p>
            <p>{recommendation['description']}</p>
            <h4>Recommended Actions:</h4>
            <ul>{actions_html}</ul>
        </div>
        """
    
    def _format_html_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """
        Format metrics data for HTML
        """
        if "metrics" not in metrics_data:
            return "<p>No detailed metrics available</p>"
        
        html_content = ""
        
        for category, category_metrics in metrics_data["metrics"].items():
            html_content += f"<h3>{category.title()} Metrics</h3>"
            
            for metric in category_metrics:
                html_content += f"""
                <div class="metric">
                    <strong>{metric['name']}:</strong> {metric['value']} {metric['unit']}
                    <br><small>{metric['description']}</small>
                </div>
                """
        
        return html_content
    
    def _generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """
        Generate Markdown report content
        """
        metadata = report_data["report_metadata"]
        summary = report_data["executive_summary"]
        recommendations = report_data["recommendations"]
        
        md_content = f"""# Code Quality Report

**Project:** {metadata['project_id']}  
**Generated:** {metadata['generation_timestamp']}  
**Report Type:** {metadata['report_type']}

## Executive Summary

- **Overall Quality Score:** {summary['overall_quality_score']:.1f}/100
- **Quality Grade:** {summary['quality_grade']}
- **Metrics Analyzed:** {summary['total_metrics_analyzed']}
- **Trend Summary:** {summary['trend_summary']}

### Key Strengths
{chr(10).join(f'- {strength}' for strength in summary['key_strengths'])}

### Key Concerns
{chr(10).join(f'- {concern}' for concern in summary['key_concerns'])}

## Recommendations

{chr(10).join(self._format_md_recommendation(rec) for rec in recommendations)}

## Detailed Metrics

{self._format_md_metrics(report_data['metrics_analysis'])}

---
*Report generated by NEXUS Quality Assurance Agent*
"""
        return md_content
    
    def _format_md_recommendation(self, recommendation: Dict[str, Any]) -> str:
        """
        Format a single recommendation for Markdown
        """
        actions_md = '\n'.join(f'  - {action}' for action in recommendation['actions'])
        
        return f"""### {recommendation['title']} ({recommendation['priority'].upper()} PRIORITY)

**Category:** {recommendation['category']}

{recommendation['description']}

**Recommended Actions:**
{actions_md}

"""
    
    def _format_md_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """
        Format metrics data for Markdown
        """
        if "metrics" not in metrics_data:
            return "No detailed metrics available"
        
        md_content = ""
        
        for category, category_metrics in metrics_data["metrics"].items():
            md_content += f"### {category.title()} Metrics\n\n"
            
            for metric in category_metrics:
                md_content += f"- **{metric['name']}:** {metric['value']} {metric['unit']} - {metric['description']}\n"
            
            md_content += "\n"
        
        return md_content
    
    async def generate_dashboard_data(self, project_id: str, 
                                    metrics_data: Dict[str, Any],
                                    trend_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate data for quality dashboard visualization
        TODO: Implement dashboard data generation
        """
        self.logger.info(f"Generating dashboard data for project: {project_id}")
        
        dashboard_data = {
            "project_id": project_id,
            "timestamp": datetime.now().isoformat(),
            "summary_cards": self._generate_summary_cards(metrics_data),
            "charts": self._generate_chart_data(metrics_data, trend_data),
            "alerts": self._generate_dashboard_alerts(metrics_data, trend_data)
        }
        
        return dashboard_data
    
    def _generate_summary_cards(self, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate summary cards for dashboard
        """
        cards = [
            {
                "title": "Overall Score",
                "value": metrics_data.get("overall_score", 0),
                "unit": "/100",
                "type": "score",
                "color": self._get_score_color(metrics_data.get("overall_score", 0))
            },
            {
                "title": "Quality Grade",
                "value": metrics_data.get("quality_grade", "F"),
                "unit": "",
                "type": "grade",
                "color": self._get_grade_color(metrics_data.get("quality_grade", "F"))
            }
        ]
        
        # Add metric-specific cards
        metrics_by_category = metrics_data.get("metrics", {})
        
        for category, category_metrics in metrics_by_category.items():
            for metric in category_metrics[:2]:  # Limit to 2 per category
                cards.append({
                    "title": metric["name"].replace("_", " ").title(),
                    "value": metric["value"],
                    "unit": metric["unit"],
                    "type": "metric",
                    "category": category,
                    "color": self._get_metric_color(metric["name"], metric["value"])
                })
        
        return cards[:8]  # Limit total cards
    
    def _generate_chart_data(self, metrics_data: Dict[str, Any], 
                           trend_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate data for charts and visualizations
        TODO: Implement chart data generation
        """
        return {
            "quality_breakdown": self._generate_quality_breakdown_chart(metrics_data),
            "trend_charts": self._generate_trend_charts(trend_data) if trend_data else {},
            "comparison_charts": {}  # TODO: Implement comparison charts
        }
    
    def _generate_quality_breakdown_chart(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate quality breakdown pie chart data
        """
        metrics_by_category = metrics_data.get("metrics", {})
        
        chart_data = {
            "type": "pie",
            "title": "Quality Metrics by Category",
            "data": []
        }
        
        for category, category_metrics in metrics_by_category.items():
            chart_data["data"].append({
                "label": category.title(),
                "value": len(category_metrics),
                "color": self._get_category_color(category)
            })
        
        return chart_data
    
    def _generate_trend_charts(self, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trend chart data
        TODO: Implement trend chart data generation
        """
        return {
            "overall_trend": {
                "type": "line",
                "title": "Overall Quality Trend",
                "data": []  # TODO: Extract trend data points
            }
        }
    
    def _generate_dashboard_alerts(self, metrics_data: Dict[str, Any],
                                 trend_data: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate alerts for dashboard
        """
        alerts = []
        
        overall_score = metrics_data.get("overall_score", 0)
        
        if overall_score < 50:
            alerts.append({
                "type": "error",
                "title": "Critical Quality Issues",
                "message": f"Overall quality score is very low ({overall_score:.1f}/100)",
                "priority": "high"
            })
        elif overall_score < 70:
            alerts.append({
                "type": "warning",
                "title": "Quality Concerns",
                "message": f"Overall quality score needs improvement ({overall_score:.1f}/100)",
                "priority": "medium"
            })
        
        # Add trend-based alerts
        if trend_data:
            declining_count = trend_data.get("summary", {}).get("declining_metrics", 0)
            if declining_count > 2:
                alerts.append({
                    "type": "warning",
                    "title": "Declining Trends",
                    "message": f"{declining_count} metrics showing declining trends",
                    "priority": "medium"
                })
        
        return alerts
    
    def _get_score_color(self, score: float) -> str:
        """Get color for score visualization"""
        if score >= 90:
            return "green"
        elif score >= 80:
            return "lightgreen"
        elif score >= 70:
            return "yellow"
        elif score >= 60:
            return "orange"
        else:
            return "red"
    
    def _get_grade_color(self, grade: str) -> str:
        """Get color for grade visualization"""
        grade_colors = {
            "A": "green",
            "B": "lightgreen", 
            "C": "yellow",
            "D": "orange",
            "F": "red"
        }
        return grade_colors.get(grade, "gray")
    
    def _get_metric_color(self, metric_name: str, value: float) -> str:
        """Get color for specific metric"""
        # Define good/bad ranges for common metrics
        if metric_name == "cyclomatic_complexity_avg":
            return "green" if value <= 5 else "yellow" if value <= 10 else "red"
        elif metric_name == "comment_ratio":
            return "green" if 10 <= value <= 30 else "yellow" if 5 <= value <= 40 else "red"
        elif metric_name == "duplication_ratio":
            return "green" if value <= 5 else "yellow" if value <= 15 else "red"
        else:
            return "blue"  # Default color
    
    def _get_category_color(self, category: str) -> str:
        """Get color for category visualization"""
        category_colors = {
            "basic": "#3498db",
            "complexity": "#e74c3c",
            "maintainability": "#f39c12",
            "quality": "#2ecc71",
            "structure": "#9b59b6"
        }
        return category_colors.get(category, "#95a5a6")
    
    def get_reporter_statistics(self) -> Dict[str, Any]:
        """
        Get quality reporter statistics
        """
        return {
            "output_directory": str(self.output_directory),
            "include_charts": self.include_charts,
            "report_formats": self.report_formats,
            "reports_generated": len(list(self.output_directory.glob("*.html"))) + 
                               len(list(self.output_directory.glob("*.json"))) +
                               len(list(self.output_directory.glob("*.md")))
        }
