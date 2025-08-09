
"""
Pattern Matcher - Detection and analysis of code patterns and anti-patterns
"""

import ast
import re
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime

from ....core.ollama_client import ollama_client


@dataclass
class CodePattern:
    """
    Represents a code pattern (good or anti-pattern)
    """
    name: str
    pattern_type: str  # 'good_practice', 'anti_pattern', 'design_pattern'
    severity: str  # 'info', 'warning', 'error', 'critical'
    description: str
    example_code: str = ""
    suggested_fix: str = ""
    confidence: float = 1.0


class PatternMatcher:
    """
    Detect and analyze code patterns and anti-patterns
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.pattern_matcher")
        
        # Configuration
        self.pattern_model = self.config.get('pattern_model', 'qwen2.5-coder:7b')
        self.include_good_patterns = self.config.get('include_good_patterns', True)
        self.min_confidence = self.config.get('min_confidence', 0.7)
        
        # Pattern definitions
        self.anti_patterns = self._setup_anti_patterns()
        self.good_patterns = self._setup_good_patterns()
        self.design_patterns = self._setup_design_patterns()
        
        self.logger.info("Pattern Matcher initialized")
    
    def _setup_anti_patterns(self) -> Dict[str, List[CodePattern]]:
        """
        Setup definitions for common anti-patterns
        """
        return {
            'python': [
                CodePattern(
                    name="god_class",
                    pattern_type="anti_pattern",
                    severity="error",
                    description="Class with too many responsibilities",
                    suggested_fix="Split class into smaller, focused classes"
                ),
                CodePattern(
                    name="long_method",
                    pattern_type="anti_pattern", 
                    severity="warning",
                    description="Method with too many lines of code",
                    suggested_fix="Extract smaller methods from large method"
                ),
                CodePattern(
                    name="magic_numbers",
                    pattern_type="anti_pattern",
                    severity="warning",
                    description="Hard-coded numeric values without explanation",
                    suggested_fix="Replace with named constants"
                ),
                CodePattern(
                    name="duplicate_code",
                    pattern_type="anti_pattern",
                    severity="error",
                    description="Identical or very similar code in multiple places",
                    suggested_fix="Extract common code into reusable function/method"
                ),
                CodePattern(
                    name="deep_nesting",
                    pattern_type="anti_pattern",
                    severity="warning",
                    description="Too many nested levels (if/for/while)",
                    suggested_fix="Extract methods or use early returns"
                ),
                CodePattern(
                    name="shotgun_surgery",
                    pattern_type="anti_pattern",
                    severity="error",
                    description="Single change requires modifications in many classes",
                    suggested_fix="Improve encapsulation and reduce coupling"
                )
            ],
            'javascript': [
                CodePattern(
                    name="callback_hell",
                    pattern_type="anti_pattern",
                    severity="error",
                    description="Deep nesting of callback functions",
                    suggested_fix="Use Promises or async/await"
                ),
                CodePattern(
                    name="global_variables",
                    pattern_type="anti_pattern",
                    severity="warning",
                    description="Excessive use of global variables",
                    suggested_fix="Use modules or proper scoping"
                )
            ]
        }
    
    def _setup_good_patterns(self) -> Dict[str, List[CodePattern]]:
        """
        Setup definitions for good coding practices
        """
        return {
            'python': [
                CodePattern(
                    name="single_responsibility",
                    pattern_type="good_practice",
                    severity="info",
                    description="Class or function has single, well-defined responsibility"
                ),
                CodePattern(
                    name="descriptive_naming",
                    pattern_type="good_practice",
                    severity="info",
                    description="Clear, descriptive names for variables and functions"
                ),
                CodePattern(
                    name="proper_error_handling",
                    pattern_type="good_practice",
                    severity="info",
                    description="Appropriate exception handling with specific exception types"
                ),
                CodePattern(
                    name="documentation",
                    pattern_type="good_practice",
                    severity="info",
                    description="Good docstrings and comments"
                )
            ]
        }
    
    def _setup_design_patterns(self) -> Dict[str, List[CodePattern]]:
        """
        Setup definitions for common design patterns
        """
        return {
            'python': [
                CodePattern(
                    name="singleton",
                    pattern_type="design_pattern",
                    severity="info",
                    description="Singleton pattern implementation"
                ),
                CodePattern(
                    name="factory",
                    pattern_type="design_pattern",
                    severity="info",
                    description="Factory pattern for object creation"
                ),
                CodePattern(
                    name="observer",
                    pattern_type="design_pattern",
                    severity="info",
                    description="Observer pattern for event handling"
                ),
                CodePattern(
                    name="decorator",
                    pattern_type="design_pattern",
                    severity="info",
                    description="Decorator pattern implementation"
                )
            ]
        }
    
    async def analyze_patterns(self, code: str, file_extension: str = ".py") -> Dict[str, Any]:
        """
        Analyze code for patterns and anti-patterns
        """
        self.logger.info(f"Analyzing patterns in code ({len(code)} chars)")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "file_extension": file_extension,
            "code_length": len(code),
            "anti_patterns_found": [],
            "good_patterns_found": [],
            "design_patterns_found": [],
            "pattern_score": 0.0,
            "recommendations": []
        }
        
        language = self._detect_language(file_extension)
        
        try:
            # Detect anti-patterns
            anti_patterns = await self._detect_anti_patterns(code, language)
            result["anti_patterns_found"] = [p.name for p in anti_patterns]
            
            # Detect good patterns (if enabled)
            if self.include_good_patterns:
                good_patterns = await self._detect_good_patterns(code, language)
                result["good_patterns_found"] = [p.name for p in good_patterns]
            
            # Detect design patterns
            design_patterns = await self._detect_design_patterns(code, language)
            result["design_patterns_found"] = [p.name for p in design_patterns]
            
            # Calculate pattern score
            result["pattern_score"] = self._calculate_pattern_score(
                anti_patterns, result.get("good_patterns_found", []), design_patterns
            )
            
            # Generate recommendations
            result["recommendations"] = self._generate_pattern_recommendations(
                anti_patterns, result.get("good_patterns_found", []), design_patterns
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing patterns: {e}")
            result["error"] = str(e)
        
        return result
    
    async def _detect_anti_patterns(self, code: str, language: str) -> List[CodePattern]:
        """
        Detect anti-patterns in code
        """
        detected_patterns = []
        
        if language not in self.anti_patterns:
            return detected_patterns
        
        try:
            # Parse AST for structural analysis
            if language == 'python':
                tree = ast.parse(code)
                detected_patterns.extend(await self._detect_python_anti_patterns(tree, code))
                
        except SyntaxError:
            self.logger.warning("Could not parse code for anti-pattern detection")
        
        return detected_patterns
    
    async def _detect_python_anti_patterns(self, tree: ast.AST, code: str) -> List[CodePattern]:
        """
        Detect Python-specific anti-patterns
        """
        detected = []
        
        # God Class detection
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                line_count = 0
                
                if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                    line_count = node.end_lineno - node.lineno + 1
                
                if method_count > 20 or line_count > 500:  # Thresholds
                    pattern = next(p for p in self.anti_patterns['python'] if p.name == 'god_class')
                    pattern.confidence = min(1.0, (method_count - 20) / 10 + (line_count - 500) / 200)
                    detected.append(pattern)
        
        # Long Method detection
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                    line_count = node.end_lineno - node.lineno + 1
                    
                    if line_count > 50:  # Threshold
                        pattern = next(p for p in self.anti_patterns['python'] if p.name == 'long_method')
                        pattern.confidence = min(1.0, (line_count - 50) / 50)
                        detected.append(pattern)
        
        # Magic Numbers detection
        magic_number_pattern = re.compile(r'\b(?<![\w.])\d{2,}\b(?![\w.])')
        if magic_number_pattern.search(code):
            pattern = next(p for p in self.anti_patterns['python'] if p.name == 'magic_numbers')
            detected.append(pattern)
        
        # Deep Nesting detection
        max_nesting = self._calculate_max_nesting_depth(tree)
        if max_nesting > 4:  # Threshold
            pattern = next(p for p in self.anti_patterns['python'] if p.name == 'deep_nesting')
            pattern.confidence = min(1.0, (max_nesting - 4) / 3)
            detected.append(pattern)
        
        return detected
    
    def _calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        """
        Calculate maximum nesting depth in AST
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
    
    async def _detect_good_patterns(self, code: str, language: str) -> List[CodePattern]:
        """
        Detect good coding patterns
        """
        detected = []
        
        if language not in self.good_patterns:
            return detected
        
        try:
            if language == 'python':
                tree = ast.parse(code)
                detected.extend(await self._detect_python_good_patterns(tree, code))
                
        except SyntaxError:
            pass
        
        return detected
    
    async def _detect_python_good_patterns(self, tree: ast.AST, code: str) -> List[CodePattern]:
        """
        Detect Python good patterns
        """
        detected = []
        
        # Check for docstrings
        docstring_count = 0
        function_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                function_count += 1
                
                # Check if has docstring
                if (node.body and isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    docstring_count += 1
        
        if function_count > 0 and docstring_count / function_count > 0.7:  # 70% have docstrings
            pattern = next(p for p in self.good_patterns['python'] if p.name == 'documentation')
            pattern.confidence = docstring_count / function_count
            detected.append(pattern)
        
        # Check for proper exception handling
        proper_exception_count = 0
        total_except_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                total_except_count += 1
                if node.type:  # Specific exception type
                    proper_exception_count += 1
        
        if total_except_count > 0 and proper_exception_count / total_except_count > 0.8:
            pattern = next(p for p in self.good_patterns['python'] if p.name == 'proper_error_handling')
            pattern.confidence = proper_exception_count / total_except_count
            detected.append(pattern)
        
        return detected
    
    async def _detect_design_patterns(self, code: str, language: str) -> List[CodePattern]:
        """
        Detect design patterns
        TODO: Implement design pattern detection
        """
        detected = []
        
        # TODO: Implement design pattern detection
        # This is complex and would require sophisticated analysis
        
        return detected
    
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
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust'
        }
        
        return extension_map.get(file_extension.lower(), 'unknown')
    
    def _calculate_pattern_score(self, anti_patterns: List[CodePattern], 
                               good_patterns: List[str], 
                               design_patterns: List[CodePattern]) -> float:
        """
        Calculate overall pattern quality score
        """
        if not anti_patterns and not good_patterns and not design_patterns:
            return 0.5  # Neutral score
        
        # Penalty for anti-patterns
        anti_pattern_penalty = 0.0
        for pattern in anti_patterns:
            severity_weights = {'critical': -0.4, 'error': -0.3, 'warning': -0.2, 'info': -0.1}
            weight = severity_weights.get(pattern.severity, -0.2)
            anti_pattern_penalty += weight * pattern.confidence
        
        # Bonus for good patterns
        good_pattern_bonus = len(good_patterns) * 0.1
        
        # Bonus for design patterns
        design_pattern_bonus = len(design_patterns) * 0.15
        
        # Calculate final score (0-1 scale)
        score = 0.7 + anti_pattern_penalty + good_pattern_bonus + design_pattern_bonus
        return max(0.0, min(1.0, score))
    
    def _generate_pattern_recommendations(self, anti_patterns: List[CodePattern],
                                        good_patterns: List[str],
                                        design_patterns: List[CodePattern]) -> List[str]:
        """
        Generate recommendations based on detected patterns
        """
        recommendations = []
        
        # Recommendations for anti-patterns
        critical_anti_patterns = [p for p in anti_patterns if p.severity == 'critical']
        if critical_anti_patterns:
            recommendations.append(f"Address {len(critical_anti_patterns)} critical anti-patterns immediately")
        
        error_anti_patterns = [p for p in anti_patterns if p.severity == 'error']
        if error_anti_patterns:
            recommendations.append(f"Fix {len(error_anti_patterns)} error-level anti-patterns")
        
        # Specific recommendations
        for pattern in anti_patterns:
            if pattern.suggested_fix:
                recommendations.append(f"{pattern.name}: {pattern.suggested_fix}")
        
        # Positive reinforcement for good patterns
        if good_patterns:
            recommendations.append(f"Good job! Found {len(good_patterns)} positive patterns")
        
        # Design pattern suggestions
        if not design_patterns and len(anti_patterns) > 3:
            recommendations.append("Consider applying design patterns to improve code structure")
        
        return recommendations
    
    async def suggest_pattern_improvements(self, code: str, 
                                         detected_anti_patterns: List[CodePattern]) -> Dict[str, Any]:
        """
        Use LLM to suggest specific improvements for detected patterns
        TODO: Implement LLM-based improvement suggestions
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "anti_patterns_count": len(detected_anti_patterns),
            "suggestions": [],
            "status": "TODO"
        }
        
        try:
            # TODO: Use LLM to generate specific improvement suggestions
            for pattern in detected_anti_patterns:
                prompt = f"""
The following code has a {pattern.name} anti-pattern:

{code}

Problem: {pattern.description}
Current suggestion: {pattern.suggested_fix}

Provide specific, actionable code improvements to fix this anti-pattern.
Include before/after code examples if possible.
"""
                
                # TODO: Make actual LLM call
                # response = await ollama_client.generate(self.pattern_model, prompt)
                
                # Placeholder
                result["suggestions"].append({
                    "pattern": pattern.name,
                    "suggestion": f"LLM suggestion for {pattern.name} not yet implemented"
                })
            
        except Exception as e:
            self.logger.error(f"Error generating pattern improvements: {e}")
            result["error"] = str(e)
        
        return result
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """
        Get pattern matcher statistics
        """
        total_anti_patterns = sum(len(patterns) for patterns in self.anti_patterns.values())
        total_good_patterns = sum(len(patterns) for patterns in self.good_patterns.values())
        total_design_patterns = sum(len(patterns) for patterns in self.design_patterns.values())
        
        return {
            "pattern_model": self.pattern_model,
            "include_good_patterns": self.include_good_patterns,
            "min_confidence": self.min_confidence,
            "supported_languages": list(self.anti_patterns.keys()),
            "total_anti_patterns": total_anti_patterns,
            "total_good_patterns": total_good_patterns,
            "total_design_patterns": total_design_patterns
        }
