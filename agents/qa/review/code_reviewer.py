
"""
Autonomous Code Reviewer - LLM-basierte Code-Analysis mit Improvement-Suggestions
"""

import ast
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime

from ....core.ollama_client import ollama_client


class CodeIssue:
    """
    Represents a code issue found during review
    """
    
    def __init__(self, issue_type: str, severity: str, line: int, 
                 description: str, suggestion: Optional[str] = None):
        self.issue_type = issue_type
        self.severity = severity  # critical, major, minor, info
        self.line = line
        self.description = description
        self.suggestion = suggestion
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.issue_type,
            'severity': self.severity,
            'line': self.line,
            'description': self.description,
            'suggestion': self.suggestion,
            'timestamp': self.timestamp.isoformat()
        }


class AutonomousCodeReviewer:
    """
    Autonomous code reviewer using LLM analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.code_reviewer")
        
        # Configuration
        self.review_model = self.config.get('review_model', 'qwen2.5-coder:7b')
        self.max_file_size = self.config.get('max_file_size', 50000)  # 50KB
        self.severity_levels = ['critical', 'major', 'minor', 'info']
        
        # Issue patterns (static analysis)
        self.issue_patterns = self._setup_issue_patterns()
        
        # Review templates
        self.review_prompts = self._setup_review_prompts()
        
        self.logger.info("Autonomous Code Reviewer initialized")
    
    def _setup_issue_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Setup static analysis patterns for common issues
        """
        return {
            'python': [
                {
                    'pattern': r'print\s*\(',
                    'type': 'debug_code',
                    'severity': 'minor',
                    'description': 'Debug print statement found'
                },
                {
                    'pattern': r'except\s*:',
                    'type': 'bare_except',
                    'severity': 'major',
                    'description': 'Bare except clause - should specify exception type'
                },
                {
                    'pattern': r'#\s*TODO',
                    'type': 'todo_comment',
                    'severity': 'info',
                    'description': 'TODO comment found'
                },
                {
                    'pattern': r'#\s*FIXME',
                    'type': 'fixme_comment',
                    'severity': 'minor',
                    'description': 'FIXME comment found'
                }
            ],
            'javascript': [
                {
                    'pattern': r'console\.log\s*\(',
                    'type': 'debug_code',
                    'severity': 'minor',
                    'description': 'Console.log statement found'
                },
                {
                    'pattern': r'==\s*[^=]',
                    'type': 'loose_equality',
                    'severity': 'major',
                    'description': 'Use === instead of == for comparison'
                }
            ]
        }
    
    def _setup_review_prompts(self) -> Dict[str, str]:
        """
        Setup LLM prompts for different types of code review
        """
        return {
            'general': """
You are an expert code reviewer. Analyze the following code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance optimizations
4. Security concerns
5. Maintainability improvements

Code to review:
{code}

Provide a structured response with:
- Issues found (with severity: critical/major/minor/info)
- Specific line numbers where applicable
- Improvement suggestions
- Overall quality score (0-1)
""",
            'security': """
You are a security-focused code reviewer. Analyze the following code for security vulnerabilities:
1. Input validation issues
2. Authentication/authorization problems
3. SQL injection vulnerabilities
4. XSS vulnerabilities
5. Insecure data handling

Code to review:
{code}

Focus on security aspects and provide specific recommendations.
""",
            'performance': """
You are a performance-focused code reviewer. Analyze the following code for performance issues:
1. Algorithm efficiency
2. Memory usage
3. Database query optimization
4. Caching opportunities
5. Resource management

Code to review:
{code}

Focus on performance aspects and suggest optimizations.
"""
        }
    
    async def review_file(self, file_path: Path, review_type: str = "general") -> Dict[str, Any]:
        """
        Review a single file
        TODO: Implement comprehensive file review
        """
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content) > self.max_file_size:
                return {"error": f"File too large: {len(content)} bytes > {self.max_file_size}"}
            
            self.logger.info(f"Reviewing file: {file_path} (type: {review_type})")
            
            # Perform review
            review_result = await self._analyze_code(content, file_path.suffix, review_type)
            review_result['file_path'] = str(file_path)
            review_result['file_size'] = len(content)
            
            return review_result
            
        except Exception as e:
            self.logger.error(f"Error reviewing file {file_path}: {e}")
            return {"error": str(e), "file_path": str(file_path)}
    
    async def _analyze_code(self, content: str, file_extension: str, review_type: str) -> Dict[str, Any]:
        """
        Analyze code content using both static analysis and LLM
        TODO: Implement comprehensive code analysis
        """
        analysis_result = {
            "timestamp": datetime.now().isoformat(),
            "review_type": review_type,
            "file_extension": file_extension,
            "lines_of_code": len(content.split('\n')),
            "static_issues": [],
            "llm_analysis": {},
            "overall_score": 0.0,
            "issues_found": 0
        }
        
        # Static analysis
        static_issues = await self._static_analysis(content, file_extension)
        analysis_result["static_issues"] = [issue.to_dict() for issue in static_issues]
        analysis_result["issues_found"] += len(static_issues)
        
        # LLM analysis
        if len(content.strip()) > 0:
            llm_analysis = await self._llm_analysis(content, review_type)
            analysis_result["llm_analysis"] = llm_analysis
        
        # Calculate overall score
        analysis_result["overall_score"] = self._calculate_quality_score(analysis_result)
        
        return analysis_result
    
    async def _static_analysis(self, content: str, file_extension: str) -> List[CodeIssue]:
        """
        Perform static analysis using pattern matching
        """
        issues = []
        language = self._detect_language(file_extension)
        
        if language not in self.issue_patterns:
            return issues
        
        patterns = self.issue_patterns[language]
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern_config in patterns:
                pattern = pattern_config['pattern']
                if re.search(pattern, line):
                    issue = CodeIssue(
                        issue_type=pattern_config['type'],
                        severity=pattern_config['severity'],
                        line=line_num,
                        description=pattern_config['description']
                    )
                    issues.append(issue)
        
        return issues
    
    async def _llm_analysis(self, content: str, review_type: str) -> Dict[str, Any]:
        """
        Perform LLM-based code analysis
        TODO: Implement LLM-based analysis
        """
        try:
            prompt_template = self.review_prompts.get(review_type, self.review_prompts['general'])
            prompt = prompt_template.format(code=content)
            
            # TODO: Make actual LLM call
            # response = await ollama_client.generate(self.review_model, prompt)
            
            # Placeholder implementation
            llm_result = {
                "status": "TODO",
                "model_used": self.review_model,
                "review_type": review_type,
                "analysis": "LLM analysis not yet implemented",
                "suggestions": [],
                "confidence_score": 0.0
            }
            
            return llm_result
            
        except Exception as e:
            self.logger.error(f"LLM analysis failed: {e}")
            return {"error": str(e)}
    
    def _detect_language(self, file_extension: str) -> str:
        """
        Detect programming language from file extension
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust'
        }
        
        return extension_map.get(file_extension.lower(), 'unknown')
    
    def _calculate_quality_score(self, analysis_result: Dict[str, Any]) -> float:
        """
        Calculate overall quality score based on issues found
        """
        static_issues = analysis_result.get("static_issues", [])
        
        if not static_issues:
            return 1.0  # Perfect score if no issues
        
        # Weight issues by severity
        severity_weights = {
            'critical': -0.3,
            'major': -0.2,
            'minor': -0.1,
            'info': -0.05
        }
        
        total_deduction = 0.0
        for issue in static_issues:
            severity = issue.get('severity', 'minor')
            total_deduction += severity_weights.get(severity, -0.1)
        
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, 1.0 + total_deduction))
        return round(score, 3)
    
    async def review_multiple_files(self, file_paths: List[Path], 
                                  review_type: str = "general") -> Dict[str, Any]:
        """
        Review multiple files and aggregate results
        """
        self.logger.info(f"Reviewing {len(file_paths)} files")
        
        aggregate_result = {
            "timestamp": datetime.now().isoformat(),
            "review_type": review_type,
            "total_files": len(file_paths),
            "files_reviewed": 0,
            "files_failed": 0,
            "overall_quality_score": 0.0,
            "total_issues": 0,
            "file_results": []
        }
        
        quality_scores = []
        total_issues = 0
        
        for file_path in file_paths:
            try:
                file_result = await self.review_file(file_path, review_type)
                
                if "error" not in file_result:
                    aggregate_result["files_reviewed"] += 1
                    quality_scores.append(file_result.get("overall_score", 0.0))
                    total_issues += file_result.get("issues_found", 0)
                else:
                    aggregate_result["files_failed"] += 1
                
                aggregate_result["file_results"].append(file_result)
                
            except Exception as e:
                self.logger.error(f"Error reviewing {file_path}: {e}")
                aggregate_result["files_failed"] += 1
                aggregate_result["file_results"].append({
                    "file_path": str(file_path),
                    "error": str(e)
                })
        
        # Calculate aggregate metrics
        if quality_scores:
            aggregate_result["overall_quality_score"] = sum(quality_scores) / len(quality_scores)
        
        aggregate_result["total_issues"] = total_issues
        
        return aggregate_result
    
    def get_review_statistics(self) -> Dict[str, Any]:
        """
        Get code reviewer statistics
        """
        return {
            "review_model": self.review_model,
            "max_file_size": self.max_file_size,
            "supported_languages": list(self.issue_patterns.keys()),
            "review_types": list(self.review_prompts.keys()),
            "severity_levels": self.severity_levels
        }
