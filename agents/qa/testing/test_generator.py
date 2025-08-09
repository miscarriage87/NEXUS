
"""
Intelligent Test Generator - Automatische Test-Generierung mit LLM
"""

import ast
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime

from ....core.ollama_client import ollama_client


class TestCase:
    """
    Represents a generated test case
    """
    
    def __init__(self, test_name: str, test_type: str, target_function: str,
                 test_code: str, description: str = ""):
        self.test_name = test_name
        self.test_type = test_type  # unit, integration, edge_case, error_case
        self.target_function = target_function
        self.test_code = test_code
        self.description = description
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'test_name': self.test_name,
            'test_type': self.test_type,
            'target_function': self.target_function,
            'test_code': self.test_code,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }


class IntelligentTestGenerator:
    """
    Generate intelligent tests for code using LLM and pattern analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.test_generator")
        
        # Configuration
        self.test_model = self.config.get('test_model', 'qwen2.5-coder:7b')
        self.test_frameworks = self.config.get('test_frameworks', ['pytest', 'unittest'])
        self.max_tests_per_function = self.config.get('max_tests_per_function', 5)
        
        # Test generation prompts
        self.test_prompts = self._setup_test_prompts()
        
        # Test templates
        self.test_templates = self._setup_test_templates()
        
        self.logger.info("Intelligent Test Generator initialized")
    
    def _setup_test_prompts(self) -> Dict[str, str]:
        """
        Setup LLM prompts for test generation
        """
        return {
            'unit_test': """
Generate comprehensive unit tests for the following function:

{code}

Requirements:
1. Test normal cases with valid inputs
2. Test edge cases (empty, null, boundary values)
3. Test error cases with invalid inputs
4. Use {framework} framework
5. Include docstrings explaining each test
6. Ensure good test coverage

Generate complete, runnable test code.
""",
            'integration_test': """
Generate integration tests for the following code:

{code}

Requirements:
1. Test interactions between components
2. Test data flow and state changes
3. Test external dependencies (mock if needed)
4. Use {framework} framework
5. Include setup and teardown if needed

Generate complete, runnable integration test code.
""",
            'property_test': """
Generate property-based tests for the following function:

{code}

Requirements:
1. Identify key properties the function should satisfy
2. Generate test cases that verify these properties
3. Use hypothesis library if appropriate
4. Test with random/generated inputs
5. Include property descriptions

Generate complete property-based test code.
"""
        }
    
    def _setup_test_templates(self) -> Dict[str, str]:
        """
        Setup test code templates
        """
        return {
            'pytest': """
import pytest
{imports}

{test_class}
""",
            'unittest': """
import unittest
{imports}

{test_class}

if __name__ == '__main__':
    unittest.main()
"""
        }
    
    async def generate_tests_for_function(self, function_code: str, function_name: str,
                                        test_types: List[str] = None,
                                        framework: str = "pytest") -> Dict[str, Any]:
        """
        Generate tests for a specific function
        TODO: Implement intelligent test generation
        """
        test_types = test_types or ['unit_test', 'edge_case', 'error_case']
        
        self.logger.info(f"Generating tests for function: {function_name}")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "function_name": function_name,
            "test_types": test_types,
            "framework": framework,
            "generated_tests": [],
            "test_code": "",
            "imports_needed": [],
            "total_tests": 0
        }
        
        # Analyze function to understand its behavior
        function_analysis = await self._analyze_function(function_code, function_name)
        result["function_analysis"] = function_analysis
        
        # Generate tests for each type
        all_test_cases = []
        for test_type in test_types:
            test_cases = await self._generate_test_type(function_code, function_name, test_type, framework)
            all_test_cases.extend(test_cases)
        
        result["generated_tests"] = [tc.to_dict() for tc in all_test_cases]
        result["total_tests"] = len(all_test_cases)
        
        # Generate complete test file
        if all_test_cases:
            test_file_code = await self._generate_test_file(all_test_cases, framework, function_analysis)
            result["test_code"] = test_file_code
        
        return result
    
    async def _analyze_function(self, function_code: str, function_name: str) -> Dict[str, Any]:
        """
        Analyze function to understand its structure and behavior
        """
        analysis = {
            "function_name": function_name,
            "parameters": [],
            "return_type": "unknown",
            "complexity": "unknown",
            "docstring": "",
            "imports_needed": [],
            "error_conditions": []
        }
        
        try:
            # Parse the function using AST
            tree = ast.parse(function_code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    # Extract parameters
                    for arg in node.args.args:
                        analysis["parameters"].append(arg.arg)
                    
                    # Extract docstring
                    if (node.body and isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant)):
                        analysis["docstring"] = node.body[0].value.value
                    
                    # Analyze complexity (basic)
                    analysis["complexity"] = self._estimate_complexity(node)
                    
                    # Find potential error conditions
                    analysis["error_conditions"] = self._find_error_conditions(node)
                    
                    break
        
        except Exception as e:
            self.logger.warning(f"Error analyzing function {function_name}: {e}")
        
        return analysis
    
    def _estimate_complexity(self, node: ast.FunctionDef) -> str:
        """
        Estimate function complexity based on AST
        """
        # Count decision points
        decision_points = 0
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                decision_points += 1
            elif isinstance(child, ast.BoolOp):
                decision_points += len(child.values) - 1
        
        if decision_points <= 2:
            return "low"
        elif decision_points <= 5:
            return "medium"
        else:
            return "high"
    
    def _find_error_conditions(self, node: ast.FunctionDef) -> List[str]:
        """
        Find potential error conditions in function
        """
        error_conditions = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                if isinstance(child.exc, ast.Call) and isinstance(child.exc.func, ast.Name):
                    error_conditions.append(child.exc.func.id)
            elif isinstance(child, ast.Assert):
                error_conditions.append("AssertionError")
        
        return error_conditions
    
    async def _generate_test_type(self, function_code: str, function_name: str,
                                test_type: str, framework: str) -> List[TestCase]:
        """
        Generate tests for a specific test type
        TODO: Implement LLM-based test generation
        """
        test_cases = []
        
        try:
            # TODO: Use LLM to generate tests
            prompt_template = self.test_prompts.get(test_type, self.test_prompts['unit_test'])
            prompt = prompt_template.format(
                code=function_code,
                framework=framework
            )
            
            # TODO: Make actual LLM call
            # response = await ollama_client.generate(self.test_model, prompt)
            
            # Placeholder implementation
            if test_type == 'unit_test':
                test_cases = await self._generate_basic_unit_tests(function_name, framework)
            elif test_type == 'edge_case':
                test_cases = await self._generate_edge_case_tests(function_name, framework)
            elif test_type == 'error_case':
                test_cases = await self._generate_error_case_tests(function_name, framework)
        
        except Exception as e:
            self.logger.error(f"Error generating {test_type} tests: {e}")
        
        return test_cases
    
    async def _generate_basic_unit_tests(self, function_name: str, framework: str) -> List[TestCase]:
        """
        Generate basic unit tests (placeholder implementation)
        """
        test_cases = []
        
        # Basic positive test
        test_code = f"""
def test_{function_name}_basic():
    # TODO: Test basic functionality of {function_name}
    pass
"""
        test_cases.append(TestCase(
            test_name=f"test_{function_name}_basic",
            test_type="unit_test",
            target_function=function_name,
            test_code=test_code.strip(),
            description=f"Basic functionality test for {function_name}"
        ))
        
        return test_cases
    
    async def _generate_edge_case_tests(self, function_name: str, framework: str) -> List[TestCase]:
        """
        Generate edge case tests (placeholder implementation)
        """
        test_cases = []
        
        # Empty input test
        test_code = f"""
def test_{function_name}_empty_input():
    # TODO: Test {function_name} with empty input
    pass
"""
        test_cases.append(TestCase(
            test_name=f"test_{function_name}_empty_input",
            test_type="edge_case",
            target_function=function_name,
            test_code=test_code.strip(),
            description=f"Empty input edge case for {function_name}"
        ))
        
        return test_cases
    
    async def _generate_error_case_tests(self, function_name: str, framework: str) -> List[TestCase]:
        """
        Generate error case tests (placeholder implementation)
        """
        test_cases = []
        
        # Invalid input test
        test_code = f"""
def test_{function_name}_invalid_input():
    # TODO: Test {function_name} with invalid input
    pass
"""
        test_cases.append(TestCase(
            test_name=f"test_{function_name}_invalid_input",
            test_type="error_case",
            target_function=function_name,
            test_code=test_code.strip(),
            description=f"Invalid input error case for {function_name}"
        ))
        
        return test_cases
    
    async def _generate_test_file(self, test_cases: List[TestCase], framework: str,
                                function_analysis: Dict[str, Any]) -> str:
        """
        Generate complete test file from test cases
        """
        imports = ["import pytest"] if framework == "pytest" else ["import unittest"]
        
        # Determine additional imports based on function analysis
        additional_imports = function_analysis.get("imports_needed", [])
        imports.extend(additional_imports)
        
        # Generate test class
        class_name = f"Test{function_analysis['function_name'].title()}"
        test_methods = []
        
        for test_case in test_cases:
            test_methods.append(f"    {test_case.test_code.replace(chr(10), chr(10) + '    ')}")
        
        if framework == "pytest":
            test_class = f"""
class {class_name}:
{chr(10).join(test_methods)}
"""
        else:  # unittest
            test_class = f"""
class {class_name}(unittest.TestCase):
{chr(10).join(test_methods)}
"""
        
        # Use template
        template = self.test_templates[framework]
        test_file_code = template.format(
            imports=chr(10).join(imports),
            test_class=test_class
        )
        
        return test_file_code
    
    async def generate_tests_for_file(self, file_path: Path, 
                                    test_types: List[str] = None,
                                    framework: str = "pytest") -> Dict[str, Any]:
        """
        Generate tests for all functions in a file
        TODO: Implement file-level test generation
        """
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.logger.info(f"Generating tests for file: {file_path}")
            
            # Extract functions from file
            functions = await self._extract_functions(content)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "file_path": str(file_path),
                "framework": framework,
                "functions_found": len(functions),
                "function_tests": {},
                "complete_test_file": "",
                "total_tests_generated": 0
            }
            
            # Generate tests for each function
            all_test_cases = []
            for func_name, func_code in functions.items():
                func_result = await self.generate_tests_for_function(
                    func_code, func_name, test_types, framework
                )
                result["function_tests"][func_name] = func_result
                
                # Collect test cases
                for test_dict in func_result.get("generated_tests", []):
                    test_case = TestCase(
                        test_name=test_dict["test_name"],
                        test_type=test_dict["test_type"],
                        target_function=test_dict["target_function"],
                        test_code=test_dict["test_code"],
                        description=test_dict["description"]
                    )
                    all_test_cases.append(test_case)
            
            # Generate complete test file
            if all_test_cases:
                test_file_code = await self._generate_complete_test_file(
                    all_test_cases, framework, str(file_path)
                )
                result["complete_test_file"] = test_file_code
            
            result["total_tests_generated"] = len(all_test_cases)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating tests for file {file_path}: {e}")
            return {"error": str(e), "file_path": str(file_path)}
    
    async def _extract_functions(self, content: str) -> Dict[str, str]:
        """
        Extract functions from Python code
        """
        functions = {}
        
        try:
            tree = ast.parse(content)
            lines = content.split('\n')
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Extract function code
                    start_line = node.lineno - 1
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else len(lines)
                    
                    func_code = '\n'.join(lines[start_line:end_line])
                    functions[node.name] = func_code
        
        except Exception as e:
            self.logger.warning(f"Error extracting functions: {e}")
        
        return functions
    
    async def _generate_complete_test_file(self, test_cases: List[TestCase], 
                                         framework: str, source_file: str) -> str:
        """
        Generate complete test file with proper structure
        """
        # Group test cases by target function
        functions_tests = {}
        for test_case in test_cases:
            func_name = test_case.target_function
            if func_name not in functions_tests:
                functions_tests[func_name] = []
            functions_tests[func_name].append(test_case)
        
        # Generate imports
        imports = [
            "import pytest" if framework == "pytest" else "import unittest",
            f"# Tests generated for {Path(source_file).name}",
            f"from {Path(source_file).stem} import *"
        ]
        
        # Generate test classes/functions
        test_sections = []
        
        for func_name, func_test_cases in functions_tests.items():
            class_name = f"Test{func_name.title()}"
            
            test_methods = []
            for test_case in func_test_cases:
                method_code = f"    def {test_case.test_name}(self):\n"
                method_code += f"        \"\"\"{test_case.description}\"\"\"\n"
                method_code += f"        {test_case.test_code.replace(chr(10), chr(10) + '        ')}"
                test_methods.append(method_code)
            
            if framework == "pytest":
                class_code = f"class {class_name}:\n" + "\n\n".join(test_methods)
            else:
                class_code = f"class {class_name}(unittest.TestCase):\n" + "\n\n".join(test_methods)
            
            test_sections.append(class_code)
        
        # Combine everything
        complete_test_file = "\n".join(imports) + "\n\n\n" + "\n\n\n".join(test_sections)
        
        if framework == "unittest":
            complete_test_file += "\n\nif __name__ == '__main__':\n    unittest.main()"
        
        return complete_test_file
    
    def get_test_generator_statistics(self) -> Dict[str, Any]:
        """
        Get test generator statistics
        """
        return {
            "test_model": self.test_model,
            "supported_frameworks": self.test_frameworks,
            "max_tests_per_function": self.max_tests_per_function,
            "test_types": list(self.test_prompts.keys()),
            "template_frameworks": list(self.test_templates.keys())
        }
