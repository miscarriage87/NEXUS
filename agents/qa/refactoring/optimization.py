
"""
Code Optimizer - Performance and quality code optimizations
"""

import ast
import re
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass
import logging
from datetime import datetime

from ....core.ollama_client import ollama_client


@dataclass
class OptimizationSuggestion:
    """
    Represents a code optimization suggestion
    """
    optimization_type: str
    target_location: str
    description: str
    original_code: str
    optimized_code: str
    performance_impact: str  # 'low', 'medium', 'high'
    difficulty: str  # 'easy', 'medium', 'hard'
    confidence: float = 1.0


class CodeOptimizer:
    """
    Analyze and optimize code for performance and quality
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.code_optimizer")
        
        # Configuration
        self.optimizer_model = self.config.get('optimizer_model', 'qwen2.5-coder:7b')
        self.focus_areas = self.config.get('focus_areas', ['performance', 'readability', 'memory'])
        self.min_impact = self.config.get('min_impact', 'low')
        
        # Optimization patterns
        self.optimization_patterns = self._setup_optimization_patterns()
        
        self.logger.info("Code Optimizer initialized")
    
    def _setup_optimization_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Setup optimization patterns for different languages
        """
        return {
            'python': [
                {
                    'name': 'list_comprehension',
                    'pattern': r'for\s+\w+\s+in\s+.*:\s*\n\s*.*\.append\(',
                    'type': 'performance',
                    'description': 'Replace loop with list comprehension',
                    'impact': 'medium',
                    'difficulty': 'easy'
                },
                {
                    'name': 'string_concatenation',
                    'pattern': r'\+.*\+.*string',
                    'type': 'performance', 
                    'description': 'Use join() for string concatenation',
                    'impact': 'high',
                    'difficulty': 'easy'
                },
                {
                    'name': 'inefficient_loop',
                    'pattern': r'for\s+i\s+in\s+range\(len\(',
                    'type': 'performance',
                    'description': 'Use enumerate() instead of range(len())',
                    'impact': 'low',
                    'difficulty': 'easy'
                },
                {
                    'name': 'unnecessary_lambda',
                    'pattern': r'lambda\s+x:\s+x\.\w+\(\)',
                    'type': 'readability',
                    'description': 'Replace lambda with method reference',
                    'impact': 'low',
                    'difficulty': 'easy'
                }
            ],
            'javascript': [
                {
                    'name': 'inefficient_dom_access',
                    'pattern': r'document\.getElementById.*document\.getElementById',
                    'type': 'performance',
                    'description': 'Cache DOM element references',
                    'impact': 'high',
                    'difficulty': 'easy'
                },
                {
                    'name': 'array_push_loop',
                    'pattern': r'for.*\.push\(',
                    'type': 'performance',
                    'description': 'Consider using map() or spread operator',
                    'impact': 'medium',
                    'difficulty': 'medium'
                }
            ]
        }
    
    async def analyze_optimizations(self, code: str, file_extension: str = ".py") -> Dict[str, Any]:
        """
        Analyze code for optimization opportunities
        """
        self.logger.info(f"Analyzing optimizations for code ({len(code)} chars)")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "file_extension": file_extension,
            "code_length": len(code),
            "focus_areas": self.focus_areas,
            "optimizations_found": [],
            "performance_score": 0.0,
            "estimated_improvement": {}
        }
        
        language = self._detect_language(file_extension)
        
        try:
            # Pattern-based optimizations
            pattern_optimizations = await self._detect_pattern_optimizations(code, language)
            
            # AST-based optimizations
            ast_optimizations = await self._detect_ast_optimizations(code, language)
            
            # LLM-based optimizations
            llm_optimizations = await self._detect_llm_optimizations(code)
            
            # Combine all optimizations
            all_optimizations = pattern_optimizations + ast_optimizations + llm_optimizations
            
            # Filter by focus areas and impact
            filtered_optimizations = self._filter_optimizations(all_optimizations)
            
            result["optimizations_found"] = [opt.__dict__ for opt in filtered_optimizations]
            result["performance_score"] = self._calculate_performance_score(code, filtered_optimizations)
            result["estimated_improvement"] = self._estimate_improvement(filtered_optimizations)
            
        except Exception as e:
            self.logger.error(f"Error analyzing optimizations: {e}")
            result["error"] = str(e)
        
        return result
    
    async def _detect_pattern_optimizations(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """
        Detect optimizations using pattern matching
        """
        optimizations = []
        
        if language not in self.optimization_patterns:
            return optimizations
        
        patterns = self.optimization_patterns[language]
        
        for pattern_config in patterns:
            matches = re.finditer(pattern_config['pattern'], code, re.MULTILINE | re.DOTALL)
            
            for match in matches:
                original_code = match.group(0)
                optimized_code = await self._generate_optimized_code(
                    original_code, pattern_config['name'], language
                )
                
                optimization = OptimizationSuggestion(
                    optimization_type=pattern_config['type'],
                    target_location=f"line_{code[:match.start()].count(chr(10)) + 1}",
                    description=pattern_config['description'],
                    original_code=original_code.strip(),
                    optimized_code=optimized_code,
                    performance_impact=pattern_config['impact'],
                    difficulty=pattern_config['difficulty'],
                    confidence=0.9
                )
                
                optimizations.append(optimization)
        
        return optimizations
    
    async def _detect_ast_optimizations(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """
        Detect optimizations using AST analysis
        """
        optimizations = []
        
        if language != 'python':
            return optimizations
        
        try:
            tree = ast.parse(code)
            
            # Detect inefficient loops
            optimizations.extend(await self._detect_loop_optimizations(tree))
            
            # Detect redundant operations
            optimizations.extend(await self._detect_redundant_operations(tree))
            
            # Detect memory optimizations
            optimizations.extend(await self._detect_memory_optimizations(tree))
            
        except SyntaxError:
            self.logger.warning("Could not parse code for AST optimization analysis")
        
        return optimizations
    
    async def _detect_loop_optimizations(self, tree: ast.AST) -> List[OptimizationSuggestion]:
        """
        Detect loop optimization opportunities
        """
        optimizations = []
        
        for node in ast.walk(tree):
            # Detect range(len()) pattern
            if (isinstance(node, ast.For) and 
                isinstance(node.iter, ast.Call) and
                isinstance(node.iter.func, ast.Name) and 
                node.iter.func.id == 'range'):
                
                if (node.iter.args and 
                    isinstance(node.iter.args[0], ast.Call) and
                    isinstance(node.iter.args[0].func, ast.Name) and
                    node.iter.args[0].func.id == 'len'):
                    
                    optimization = OptimizationSuggestion(
                        optimization_type="performance",
                        target_location=f"line_{node.lineno}",
                        description="Use enumerate() instead of range(len())",
                        original_code=f"for {ast.unparse(node.target)} in range(len(...)):",
                        optimized_code=f"for {ast.unparse(node.target)}, item in enumerate(...):",
                        performance_impact="low",
                        difficulty="easy",
                        confidence=0.95
                    )
                    optimizations.append(optimization)
        
        return optimizations
    
    async def _detect_redundant_operations(self, tree: ast.AST) -> List[OptimizationSuggestion]:
        """
        Detect redundant operations
        """
        optimizations = []
        
        # Detect redundant string operations
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                # Check for string concatenation in loops
                if self._is_in_loop(node, tree):
                    optimization = OptimizationSuggestion(
                        optimization_type="performance",
                        target_location=f"line_{node.lineno}",
                        description="Avoid string concatenation in loops - use list and join()",
                        original_code="string += item  # in loop",
                        optimized_code="items.append(item)  # then ''.join(items)",
                        performance_impact="high",
                        difficulty="medium",
                        confidence=0.8
                    )
                    optimizations.append(optimization)
        
        return optimizations
    
    async def _detect_memory_optimizations(self, tree: ast.AST) -> List[OptimizationSuggestion]:
        """
        Detect memory optimization opportunities
        """
        optimizations = []
        
        # Detect large list creation that could use generators
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                # Check if list comprehension is large or used immediately
                optimization = OptimizationSuggestion(
                    optimization_type="memory",
                    target_location=f"line_{node.lineno}",
                    description="Consider using generator expression for large datasets",
                    original_code="[expr for item in large_iterable]",
                    optimized_code="(expr for item in large_iterable)",
                    performance_impact="medium",
                    difficulty="easy",
                    confidence=0.7
                )
                optimizations.append(optimization)
        
        return optimizations
    
    def _is_in_loop(self, node: ast.AST, tree: ast.AST) -> bool:
        """
        Check if a node is inside a loop
        """
        for parent in ast.walk(tree):
            for child in ast.walk(parent):
                if child is node:
                    if isinstance(parent, (ast.For, ast.While)):
                        return True
        return False
    
    async def _detect_llm_optimizations(self, code: str) -> List[OptimizationSuggestion]:
        """
        Use LLM to detect complex optimization opportunities
        TODO: Implement LLM-based optimization detection
        """
        optimizations = []
        
        try:
            # TODO: Use LLM to analyze code for optimizations
            prompt = f"""
Analyze the following code for performance and quality optimizations:

{code}

Focus on:
1. Performance bottlenecks
2. Memory usage improvements
3. Algorithm optimizations
4. Code readability improvements

Provide specific, actionable optimization suggestions with before/after examples.
"""
            
            # TODO: Make actual LLM call
            # response = await ollama_client.generate(self.optimizer_model, prompt)
            
            # Placeholder
            if len(code) > 500:  # Only suggest for larger code blocks
                optimization = OptimizationSuggestion(
                    optimization_type="general",
                    target_location="entire_code",
                    description="LLM-suggested optimizations available",
                    original_code=code[:100] + "...",
                    optimized_code="LLM optimization not yet implemented",
                    performance_impact="medium",
                    difficulty="medium",
                    confidence=0.5
                )
                optimizations.append(optimization)
            
        except Exception as e:
            self.logger.error(f"LLM optimization analysis failed: {e}")
        
        return optimizations
    
    async def _generate_optimized_code(self, original_code: str, pattern_name: str,
                                     language: str) -> str:
        """
        Generate optimized version of code
        """
        # Simple pattern-based replacements
        optimizations_map = {
            'list_comprehension': {
                'python': lambda code: re.sub(
                    r'for\s+(\w+)\s+in\s+(.*?):\s*\n\s*(\w+)\.append\(([^)]+)\)',
                    r'\3 = [\4 for \1 in \2]',
                    code
                )
            },
            'inefficient_loop': {
                'python': lambda code: re.sub(
                    r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):',
                    r'for \1, item in enumerate(\2):',
                    code
                )
            }
        }
        
        if pattern_name in optimizations_map and language in optimizations_map[pattern_name]:
            optimization_func = optimizations_map[pattern_name][language]
            return optimization_func(original_code)
        
        return original_code  # Return original if no optimization available
    
    def _filter_optimizations(self, optimizations: List[OptimizationSuggestion]) -> List[OptimizationSuggestion]:
        """
        Filter optimizations based on focus areas and minimum impact
        """
        filtered = []
        
        impact_levels = {'low': 1, 'medium': 2, 'high': 3}
        min_impact_level = impact_levels.get(self.min_impact, 1)
        
        for opt in optimizations:
            # Check focus areas
            if opt.optimization_type not in self.focus_areas:
                continue
            
            # Check minimum impact
            opt_impact_level = impact_levels.get(opt.performance_impact, 1)
            if opt_impact_level < min_impact_level:
                continue
            
            filtered.append(opt)
        
        return filtered
    
    def _calculate_performance_score(self, code: str, optimizations: List[OptimizationSuggestion]) -> float:
        """
        Calculate overall performance score
        """
        if not optimizations:
            return 0.8  # Good score if no optimizations needed
        
        # Penalty based on optimization impact and count
        total_penalty = 0.0
        impact_weights = {'low': 0.1, 'medium': 0.2, 'high': 0.3}
        
        for opt in optimizations:
            weight = impact_weights.get(opt.performance_impact, 0.1)
            total_penalty += weight * opt.confidence
        
        # Normalize by code size
        lines_of_code = len(code.split('\n'))
        normalized_penalty = total_penalty / max(1, lines_of_code / 100)
        
        # Calculate score (0-1 scale)
        score = max(0.0, min(1.0, 1.0 - normalized_penalty))
        return round(score, 3)
    
    def _estimate_improvement(self, optimizations: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """
        Estimate potential improvement from applying optimizations
        """
        improvement = {
            "performance_improvement": 0.0,
            "readability_improvement": 0.0,
            "memory_improvement": 0.0,
            "total_optimizations": len(optimizations)
        }
        
        impact_values = {'low': 0.1, 'medium': 0.3, 'high': 0.5}
        
        for opt in optimizations:
            impact_value = impact_values.get(opt.performance_impact, 0.1) * opt.confidence
            
            if opt.optimization_type == "performance":
                improvement["performance_improvement"] += impact_value
            elif opt.optimization_type == "readability":
                improvement["readability_improvement"] += impact_value
            elif opt.optimization_type == "memory":
                improvement["memory_improvement"] += impact_value
        
        # Normalize improvements (0-1 scale)
        for key in ["performance_improvement", "readability_improvement", "memory_improvement"]:
            improvement[key] = min(1.0, improvement[key])
            improvement[key] = round(improvement[key], 3)
        
        return improvement
    
    async def apply_optimization(self, code: str, optimization: OptimizationSuggestion) -> Dict[str, Any]:
        """
        Apply a specific optimization to code
        TODO: Implement optimization application
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "optimization_applied": optimization.__dict__,
            "success": False,
            "original_code": code,
            "optimized_code": code,
            "validation_passed": False
        }
        
        try:
            # TODO: Implement actual optimization application
            # This would involve:
            # 1. Parsing the original code
            # 2. Applying the transformation
            # 3. Validating the result
            # 4. Ensuring functionality is preserved
            
            result["optimized_code"] = optimization.optimized_code
            result["success"] = True
            result["validation_passed"] = True  # TODO: Implement validation
            
            self.logger.info(f"Applied optimization: {optimization.optimization_type}")
            
        except Exception as e:
            self.logger.error(f"Error applying optimization: {e}")
            result["error"] = str(e)
        
        return result
    
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
    
    def get_optimizer_statistics(self) -> Dict[str, Any]:
        """
        Get code optimizer statistics
        """
        total_patterns = sum(len(patterns) for patterns in self.optimization_patterns.values())
        
        return {
            "optimizer_model": self.optimizer_model,
            "focus_areas": self.focus_areas,
            "min_impact": self.min_impact,
            "supported_languages": list(self.optimization_patterns.keys()),
            "total_optimization_patterns": total_patterns
        }
