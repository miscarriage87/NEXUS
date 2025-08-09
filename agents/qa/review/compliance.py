
"""
Compliance Checker - Standards compliance checking and validation
"""

import re
import ast
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
import logging
from datetime import datetime


class ComplianceViolation:
    """
    Represents a compliance violation
    """
    
    def __init__(self, rule: str, severity: str, line: int,
                 description: str, suggestion: Optional[str] = None):
        self.rule = rule
        self.severity = severity  # critical, major, minor, info
        self.line = line
        self.description = description
        self.suggestion = suggestion
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'rule': self.rule,
            'severity': self.severity,
            'line': self.line,
            'description': self.description,
            'suggestion': self.suggestion,
            'timestamp': self.timestamp.isoformat()
        }


class ComplianceChecker:
    """
    Check code compliance against various standards and best practices
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.qa.compliance")
        
        # Configuration
        self.standards = self.config.get('standards', ['pep8', 'best_practices'])
        self.strict_mode = self.config.get('strict_mode', False)
        
        # Compliance rules
        self.compliance_rules = self._setup_compliance_rules()
        
        self.logger.info(f"Compliance Checker initialized with standards: {self.standards}")
    
    def _setup_compliance_rules(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Setup compliance rules for different standards
        """
        return {
            'pep8': {
                'python': [
                    {
                        'rule': 'E701',
                        'pattern': r':\s*[^#\n]*;\s*[^#\n]',
                        'severity': 'minor',
                        'description': 'Multiple statements on one line (colon)',
                        'suggestion': 'Put each statement on a separate line'
                    },
                    {
                        'rule': 'E501',
                        'pattern': r'^.{80,}$',
                        'severity': 'minor',
                        'description': 'Line too long (>79 characters)',
                        'suggestion': 'Break line into multiple lines'
                    },
                    {
                        'rule': 'W292',
                        'pattern': r'[^\n]$',
                        'severity': 'info',
                        'description': 'No newline at end of file',
                        'suggestion': 'Add newline at end of file'
                    },
                    {
                        'rule': 'E302',
                        'pattern': r'^(class|def)\s+\w+',
                        'severity': 'minor',
                        'description': 'Expected 2 blank lines',
                        'suggestion': 'Add blank lines before class/function definitions'
                    }
                ]
            },
            'best_practices': {
                'python': [
                    {
                        'rule': 'BP001',
                        'pattern': r'except\s*:',
                        'severity': 'major',
                        'description': 'Bare except clause',
                        'suggestion': 'Specify exception type(s) to catch'
                    },
                    {
                        'rule': 'BP002',
                        'pattern': r'eval\s*\(',
                        'severity': 'critical',
                        'description': 'Use of eval() function',
                        'suggestion': 'Avoid eval() - use safer alternatives'
                    },
                    {
                        'rule': 'BP003',
                        'pattern': r'exec\s*\(',
                        'severity': 'critical',
                        'description': 'Use of exec() function',
                        'suggestion': 'Avoid exec() - use safer alternatives'
                    },
                    {
                        'rule': 'BP004',
                        'pattern': r'import\s+\*',
                        'severity': 'major',
                        'description': 'Wildcard import',
                        'suggestion': 'Import specific names instead of using *'
                    }
                ],
                'javascript': [
                    {
                        'rule': 'JS001',
                        'pattern': r'==\s*[^=]',
                        'severity': 'major',
                        'description': 'Use of == instead of ===',
                        'suggestion': 'Use === for strict equality comparison'
                    },
                    {
                        'rule': 'JS002',
                        'pattern': r'!=\s*[^=]',
                        'severity': 'major',
                        'description': 'Use of != instead of !==',
                        'suggestion': 'Use !== for strict inequality comparison'
                    }
                ]
            },
            'security': {
                'python': [
                    {
                        'rule': 'S001',
                        'pattern': r'password\s*=\s*[\'"][^\'"]+[\'"]',
                        'severity': 'critical',
                        'description': 'Hardcoded password',
                        'suggestion': 'Use environment variables or secure storage'
                    },
                    {
                        'rule': 'S002',
                        'pattern': r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
                        'severity': 'critical',
                        'description': 'Hardcoded API key',
                        'suggestion': 'Use environment variables or secure storage'
                    },
                    {
                        'rule': 'S003',
                        'pattern': r'subprocess\.(call|run|Popen)',
                        'severity': 'major',
                        'description': 'Use of subprocess without shell=False',
                        'suggestion': 'Use shell=False to prevent shell injection'
                    }
                ]
            }
        }
    
    async def check_file_compliance(self, file_path: Path, 
                                  standards: List[str] = None) -> Dict[str, Any]:
        """
        Check compliance of a single file
        """
        standards = standards or self.standards
        
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.logger.info(f"Checking compliance for: {file_path}")
            
            result = await self._check_content_compliance(content, file_path.suffix, standards)
            result['file_path'] = str(file_path)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error checking compliance for {file_path}: {e}")
            return {"error": str(e), "file_path": str(file_path)}
    
    async def _check_content_compliance(self, content: str, file_extension: str,
                                      standards: List[str]) -> Dict[str, Any]:
        """
        Check compliance of content against specified standards
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "standards_checked": standards,
            "file_extension": file_extension,
            "violations": [],
            "compliance_score": 0.0,
            "lines_checked": len(content.split('\n'))
        }
        
        language = self._detect_language(file_extension)
        all_violations = []
        
        # Check each standard
        for standard in standards:
            standard_violations = await self._check_standard_compliance(
                content, language, standard
            )
            all_violations.extend(standard_violations)
        
        result["violations"] = [v.to_dict() for v in all_violations]
        result["violation_count"] = len(all_violations)
        result["compliance_score"] = self._calculate_compliance_score(all_violations, len(content.split('\n')))
        
        # Group violations by severity
        result["violations_by_severity"] = self._group_violations_by_severity(all_violations)
        
        return result
    
    async def _check_standard_compliance(self, content: str, language: str, 
                                       standard: str) -> List[ComplianceViolation]:
        """
        Check compliance against a specific standard
        """
        violations = []
        
        if standard not in self.compliance_rules:
            self.logger.warning(f"Unknown standard: {standard}")
            return violations
        
        if language not in self.compliance_rules[standard]:
            return violations
        
        rules = self.compliance_rules[standard][language]
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for rule in rules:
                if self._check_rule_match(line, rule):
                    violation = ComplianceViolation(
                        rule=rule['rule'],
                        severity=rule['severity'],
                        line=line_num,
                        description=rule['description'],
                        suggestion=rule.get('suggestion')
                    )
                    violations.append(violation)
        
        # Additional checks based on standard
        if standard == 'pep8' and language == 'python':
            violations.extend(await self._check_pep8_specific(content))
        
        return violations
    
    def _check_rule_match(self, line: str, rule: Dict[str, Any]) -> bool:
        """
        Check if a line matches a compliance rule
        """
        pattern = rule['pattern']
        
        # Handle special cases
        if rule['rule'] == 'E501':  # Line length check
            return len(line) > 79
        elif rule['rule'] == 'W292':  # End of file newline
            return False  # Handled separately
        
        return bool(re.search(pattern, line))
    
    async def _check_pep8_specific(self, content: str) -> List[ComplianceViolation]:
        """
        Check PEP8 specific rules that require more complex analysis
        """
        violations = []
        
        try:
            # Parse AST for more complex checks
            tree = ast.parse(content)
            
            # Check for proper spacing around functions/classes
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    # TODO: Implement more sophisticated PEP8 checks
                    pass
            
        except SyntaxError:
            # If code doesn't parse, we can't do AST-based checks
            pass
        
        return violations
    
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
    
    def _calculate_compliance_score(self, violations: List[ComplianceViolation], 
                                  total_lines: int) -> float:
        """
        Calculate overall compliance score
        """
        if not violations:
            return 1.0
        
        # Weight violations by severity
        severity_weights = {
            'critical': -0.5,
            'major': -0.3,
            'minor': -0.1,
            'info': -0.05
        }
        
        total_deduction = 0.0
        for violation in violations:
            weight = severity_weights.get(violation.severity, -0.1)
            total_deduction += weight
        
        # Normalize by number of lines (larger files can have more violations)
        if total_lines > 0:
            total_deduction = total_deduction * (100.0 / total_lines)
        
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, 1.0 + total_deduction))
        return round(score, 3)
    
    def _group_violations_by_severity(self, violations: List[ComplianceViolation]) -> Dict[str, int]:
        """
        Group violations by severity level
        """
        grouped = {'critical': 0, 'major': 0, 'minor': 0, 'info': 0}
        
        for violation in violations:
            if violation.severity in grouped:
                grouped[violation.severity] += 1
        
        return grouped
    
    async def check_multiple_files(self, file_paths: List[Path],
                                 standards: List[str] = None) -> Dict[str, Any]:
        """
        Check compliance for multiple files
        """
        standards = standards or self.standards
        
        self.logger.info(f"Checking compliance for {len(file_paths)} files against: {standards}")
        
        aggregate_result = {
            "timestamp": datetime.now().isoformat(),
            "standards_checked": standards,
            "total_files": len(file_paths),
            "files_checked": 0,
            "files_failed": 0,
            "overall_compliance_score": 0.0,
            "total_violations": 0,
            "violations_by_severity": {'critical': 0, 'major': 0, 'minor': 0, 'info': 0},
            "file_results": []
        }
        
        compliance_scores = []
        total_violations = 0
        total_violations_by_severity = {'critical': 0, 'major': 0, 'minor': 0, 'info': 0}
        
        for file_path in file_paths:
            try:
                file_result = await self.check_file_compliance(file_path, standards)
                
                if "error" not in file_result:
                    aggregate_result["files_checked"] += 1
                    compliance_scores.append(file_result.get("compliance_score", 0.0))
                    total_violations += file_result.get("violation_count", 0)
                    
                    # Aggregate violations by severity
                    file_severity_counts = file_result.get("violations_by_severity", {})
                    for severity, count in file_severity_counts.items():
                        if severity in total_violations_by_severity:
                            total_violations_by_severity[severity] += count
                else:
                    aggregate_result["files_failed"] += 1
                
                aggregate_result["file_results"].append(file_result)
                
            except Exception as e:
                self.logger.error(f"Error checking compliance for {file_path}: {e}")
                aggregate_result["files_failed"] += 1
                aggregate_result["file_results"].append({
                    "file_path": str(file_path),
                    "error": str(e)
                })
        
        # Calculate aggregate metrics
        if compliance_scores:
            aggregate_result["overall_compliance_score"] = sum(compliance_scores) / len(compliance_scores)
        
        aggregate_result["total_violations"] = total_violations
        aggregate_result["violations_by_severity"] = total_violations_by_severity
        
        return aggregate_result
    
    def add_custom_rule(self, standard: str, language: str, rule: Dict[str, Any]) -> None:
        """
        Add custom compliance rule
        """
        if standard not in self.compliance_rules:
            self.compliance_rules[standard] = {}
        
        if language not in self.compliance_rules[standard]:
            self.compliance_rules[standard][language] = []
        
        self.compliance_rules[standard][language].append(rule)
        self.logger.info(f"Added custom rule {rule['rule']} for {standard}/{language}")
    
    def get_compliance_statistics(self) -> Dict[str, Any]:
        """
        Get compliance checker statistics
        """
        total_rules = 0
        for standard, languages in self.compliance_rules.items():
            for language, rules in languages.items():
                total_rules += len(rules)
        
        return {
            "standards": self.standards,
            "strict_mode": self.strict_mode,
            "total_standards": len(self.compliance_rules),
            "total_rules": total_rules,
            "supported_languages": list(set(
                lang for langs in self.compliance_rules.values() 
                for lang in langs.keys()
            ))
        }
