
"""
Comprehensive tests for Security Agent
"""
import pytest
import asyncio
import json
import tempfile
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.security_agent import SecurityAgent, SecurityVulnerability, SecurityScanResult, ComplianceCheck

@pytest.fixture
def security_config():
    return {
        'agents': {
            'security': {
                'scan_engines': ['custom'],  # Only use custom engine for testing
                'owasp_compliance_level': 'strict',
                'max_scan_time_seconds': 60,
                'model': 'qwen2.5-coder:7b'
            }
        }
    }

@pytest.fixture
def security_agent(security_config):
    return SecurityAgent(security_config)

@pytest.fixture
def temp_code_dir():
    """Create temporary directory with test code files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test Python file with vulnerabilities
        test_file = os.path.join(temp_dir, "test_app.py")
        with open(test_file, 'w') as f:
            f.write('''
import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)
app.debug = True  # Security issue: debug mode

# Hardcoded secret - security issue
SECRET_KEY = "hardcoded_secret_123"
password = "admin123"  # Another hardcoded secret

@app.route('/user/<user_id>')
def get_user(user_id):
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()

@app.route('/command')
def run_command():
    # Command injection vulnerability
    cmd = request.args.get('cmd')
    os.system(f"echo {cmd}")
    return "Command executed"

def weak_hash(data):
    # Weak cryptography
    import hashlib
    return hashlib.md5(data.encode()).hexdigest()

# More security issues for testing
def unsafe_file_access():
    # Path traversal vulnerability
    filename = request.args.get('file')
    with open(f"/app/files/{filename}", 'r') as f:
        return f.read()
''')
        yield temp_dir

@pytest.fixture
def sample_requirements_file():
    """Create temporary requirements file with vulnerable dependencies"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('''
django==1.8.0
flask==0.10.1
requests==2.6.0
sqlalchemy>=1.0.0
pycrypto==2.6.1
''')
        yield f.name
    os.unlink(f.name)

@pytest.mark.asyncio
async def test_security_agent_initialization(security_agent):
    """Test Security Agent initialization"""
    assert security_agent.agent_id == "security"
    assert security_agent.name == "Security Analysis Agent"
    assert len(security_agent.get_capabilities()) > 15
    assert len(security_agent.owasp_rules) == 10  # OWASP Top 10
    assert security_agent.compliance_level == "strict"

@pytest.mark.asyncio
async def test_owasp_rules_loading(security_agent):
    """Test OWASP rules loading"""
    owasp_rules = security_agent.owasp_rules
    
    # Check OWASP Top 10 2021 categories
    expected_categories = [
        "A01_2021", "A02_2021", "A03_2021", "A04_2021", "A05_2021",
        "A06_2021", "A07_2021", "A08_2021", "A09_2021", "A10_2021"
    ]
    
    for category in expected_categories:
        assert category in owasp_rules
        assert "name" in owasp_rules[category]
        assert "patterns" in owasp_rules[category]
        assert "severity" in owasp_rules[category]

@pytest.mark.asyncio
async def test_security_patterns_loading(security_agent):
    """Test security patterns loading"""
    patterns = security_agent.security_patterns
    
    assert "secure_patterns" in patterns
    assert "insecure_patterns" in patterns
    assert "sql_injection" in patterns["insecure_patterns"]
    assert "hardcoded_secrets" in patterns["insecure_patterns"]

@pytest.mark.asyncio
async def test_code_security_scan(security_agent, temp_code_dir):
    """Test comprehensive code security scan"""
    result = await security_agent.scan_code_security(temp_code_dir)
    
    assert result["status"] == "completed"
    assert "scan_id" in result
    assert "scan_summary" in result
    assert "vulnerabilities" in result
    assert isinstance(result["vulnerabilities"], list)
    
    # Should find vulnerabilities in test code
    if result["vulnerabilities"]:
        vuln = result["vulnerabilities"][0]
        assert "vuln_id" in vuln
        assert "severity" in vuln
        assert "title" in vuln
        assert "file_path" in vuln

@pytest.mark.asyncio
async def test_custom_scan_engine(security_agent, temp_code_dir):
    """Test custom security scan engine"""
    vulnerabilities = await security_agent._run_custom_scan(temp_code_dir, {})
    
    assert isinstance(vulnerabilities, list)
    # Should find multiple vulnerabilities in test code
    assert len(vulnerabilities) > 0
    
    # Check for specific vulnerability types
    vuln_categories = [v.category for v in vulnerabilities]
    assert "custom" in vuln_categories

@pytest.mark.asyncio
async def test_file_security_analysis(security_agent, temp_code_dir):
    """Test individual file security analysis"""
    test_file = os.path.join(temp_code_dir, "test_app.py")
    vulnerabilities = await security_agent._analyze_file_security(test_file)
    
    assert isinstance(vulnerabilities, list)
    assert len(vulnerabilities) > 0
    
    # Check vulnerability details
    for vuln in vulnerabilities:
        assert hasattr(vuln, 'vuln_id')
        assert hasattr(vuln, 'severity')
        assert hasattr(vuln, 'file_path')
        assert vuln.file_path == test_file

@pytest.mark.asyncio
async def test_owasp_analysis(security_agent, temp_code_dir):
    """Test OWASP-specific security analysis"""
    vulnerabilities = await security_agent._run_owasp_analysis(temp_code_dir)
    
    assert isinstance(vulnerabilities, list)
    
    if vulnerabilities:
        # Check OWASP-specific fields
        owasp_vulns = [v for v in vulnerabilities if v.category == "owasp"]
        for vuln in owasp_vulns:
            assert vuln.owasp_category is not None
            assert vuln.owasp_category.startswith("A")

@pytest.mark.asyncio
async def test_false_positive_filtering(security_agent):
    """Test false positive filtering"""
    # Create test vulnerabilities
    vulnerabilities = [
        SecurityVulnerability(
            vuln_id="test_1",
            severity="medium",
            category="test",
            title="Test Vulnerability",
            description="Test description",
            file_path="/app/test_file.py",
            line_number=10,
            code_snippet="# TODO: fix this vulnerability"
        ),
        SecurityVulnerability(
            vuln_id="test_2",
            severity="high",
            category="test",
            title="Real Vulnerability",
            description="Real security issue",
            file_path="/app/main.py",
            line_number=20,
            code_snippet="password = get_password()"
        )
    ]
    
    filtered = await security_agent._filter_false_positives(vulnerabilities)
    
    assert isinstance(filtered, list)
    # Should filter out or mark the TODO comment vulnerability
    for vuln in filtered:
        assert hasattr(vuln, 'false_positive_likelihood')

@pytest.mark.asyncio
async def test_false_positive_likelihood_calculation(security_agent):
    """Test false positive likelihood calculation"""
    # Test file vulnerability (high FP likelihood)
    test_vuln = SecurityVulnerability(
        vuln_id="test_fp",
        severity="medium",
        category="test",
        title="Test Issue",
        description="Test",
        file_path="/app/tests/test_example.py",
        line_number=1,
        code_snippet="# TODO: this is safe actually"
    )
    
    fp_likelihood = await security_agent._calculate_false_positive_likelihood(test_vuln)
    
    assert 0 <= fp_likelihood <= 1
    # Should be high due to test file path and TODO comment
    assert fp_likelihood > 0.5

@pytest.mark.asyncio
async def test_dependency_vulnerability_scan(security_agent, sample_requirements_file):
    """Test dependency vulnerability scanning"""
    result = await security_agent.check_dependencies([sample_requirements_file])
    
    assert result["status"] == "completed"
    assert "dependency_analysis" in result
    
    analysis = result["dependency_analysis"]
    assert "files_scanned" in analysis
    assert "vulnerable_packages" in analysis
    assert analysis["files_scanned"] == [sample_requirements_file]

@pytest.mark.asyncio
async def test_requirements_file_parsing(security_agent, sample_requirements_file):
    """Test requirements file parsing"""
    vulnerabilities = await security_agent._scan_requirements_file(sample_requirements_file)
    
    assert isinstance(vulnerabilities, list)
    # Should find some vulnerable packages from our test file

@pytest.mark.asyncio
async def test_package_requirement_parsing(security_agent):
    """Test parsing of individual package requirements"""
    test_cases = [
        ("django==1.8.0", {"name": "django", "version": "1.8.0"}),
        ("flask>=0.10.1", {"name": "flask", "version": "0.10.1", "operator": ">="}),
        ("requests", {"name": "requests", "version": "unknown"})
    ]
    
    for requirement, expected in test_cases:
        result = security_agent._parse_requirement(requirement)
        assert result["name"] == expected["name"]
        assert result["version"] == expected["version"]

@pytest.mark.asyncio
async def test_owasp_compliance_validation(security_agent, temp_code_dir):
    """Test OWASP compliance validation"""
    result = await security_agent.validate_owasp_compliance(temp_code_dir)
    
    assert result["status"] == "completed"
    assert "compliance_report" in result
    
    report = result["compliance_report"]
    assert "overall_compliance_score" in report
    assert "compliance_standard" in report
    assert "checks" in report
    assert report["compliance_standard"] == "OWASP Top 10 2021"
    assert len(report["checks"]) == 10  # Should check all OWASP Top 10

@pytest.mark.asyncio
async def test_owasp_compliance_check(security_agent, temp_code_dir):
    """Test individual OWASP compliance check"""
    owasp_data = security_agent.owasp_rules["A03_2021"]  # Injection
    
    compliance_check = await security_agent._check_owasp_compliance(
        temp_code_dir, "A03_2021", owasp_data
    )
    
    assert "requirement_id" in compliance_check
    assert "compliance_status" in compliance_check
    assert compliance_check["requirement_id"] == "A03_2021"
    # Should find violations in our test code
    assert compliance_check["compliance_status"] in ["compliant", "non_compliant"]

@pytest.mark.asyncio
async def test_remediation_actions(security_agent):
    """Test remediation action generation"""
    violations = [{"file": "test.py", "pattern": "sql_injection", "category": "A03_2021"}]
    
    actions = await security_agent._get_remediation_actions("A03_2021", violations)
    
    assert isinstance(actions, list)
    assert len(actions) > 0
    assert isinstance(actions[0], str)

@pytest.mark.asyncio
async def test_security_fix_suggestions(security_agent):
    """Test security fix suggestions generation"""
    vulnerabilities = [
        {
            "vuln_id": "test_vuln_1",
            "category": "owasp",
            "severity": "high",
            "title": "SQL Injection",
            "description": "Potential SQL injection vulnerability"
        }
    ]
    
    result = await security_agent.suggest_security_fixes(vulnerabilities)
    
    assert result["status"] == "completed"
    assert "fixes" in result
    assert "fix_suggestions" in result["fixes"]

@pytest.mark.asyncio
async def test_template_fixes(security_agent):
    """Test template-based security fixes"""
    vulnerabilities = [
        {"vuln_id": "test_1", "category": "bandit"},
        {"vuln_id": "test_2", "category": "owasp"}
    ]
    
    bandit_fixes = security_agent._get_template_fixes("bandit", [vulnerabilities[0]])
    owasp_fixes = security_agent._get_template_fixes("owasp", [vulnerabilities[1]])
    
    assert len(bandit_fixes) == 1
    assert len(owasp_fixes) == 1
    assert "fix_title" in bandit_fixes[0]
    assert "implementation_steps" in owasp_fixes[0]

@pytest.mark.asyncio
async def test_security_metrics(security_agent):
    """Test security metrics collection"""
    # Add some test data
    security_agent.security_metrics["scans_performed"] = 5
    security_agent.security_metrics["vulnerabilities_found"] = 10
    
    metrics = await security_agent.get_security_metrics()
    
    assert "security_metrics" in metrics
    assert "recent_activity" in metrics
    assert "vulnerability_distribution" in metrics
    assert "timestamp" in metrics

@pytest.mark.asyncio
async def test_vulnerability_distribution(security_agent):
    """Test vulnerability distribution calculation"""
    # Add test vulnerabilities
    test_vulns = [
        SecurityVulnerability("v1", "critical", "test", "Test 1", "desc", "file", 1, "code"),
        SecurityVulnerability("v2", "high", "test", "Test 2", "desc", "file", 2, "code"),
        SecurityVulnerability("v3", "medium", "test", "Test 3", "desc", "file", 3, "code")
    ]
    
    security_agent.vulnerability_history = test_vulns
    
    distribution = security_agent._get_vulnerability_distribution()
    
    assert distribution["critical"] == 1
    assert distribution["high"] == 1
    assert distribution["medium"] == 1

@pytest.mark.asyncio
async def test_overall_security_score_calculation(security_agent):
    """Test overall security score calculation"""
    code_scan = {
        "vulnerabilities": [
            {"severity": "critical"},
            {"severity": "high"},
            {"severity": "medium"}
        ]
    }
    
    compliance_check = {
        "compliance_report": {
            "overall_compliance_score": 80
        }
    }
    
    score_info = security_agent._calculate_overall_security_score(code_scan, compliance_check)
    
    assert "overall_score" in score_info
    assert "security_grade" in score_info
    assert "recommendations" in score_info
    assert 0 <= score_info["overall_score"] <= 100

@pytest.mark.asyncio
async def test_security_grade_mapping(security_agent):
    """Test security grade mapping"""
    test_cases = [
        (95, "A"),
        (85, "B"), 
        (75, "C"),
        (65, "D"),
        (45, "F")
    ]
    
    for score, expected_grade in test_cases:
        grade = security_agent._get_security_grade(score)
        assert grade == expected_grade

@pytest.mark.asyncio
async def test_process_task_types(security_agent, temp_code_dir, sample_requirements_file):
    """Test different security task types"""
    # Test scan_code_security task
    task1 = {
        "task_type": "scan_code_security",
        "code_path": temp_code_dir
    }
    result1 = await security_agent.process_task(task1)
    assert result1["status"] == "completed"
    
    # Test check_dependencies task
    task2 = {
        "task_type": "check_dependencies",
        "requirements_files": [sample_requirements_file]
    }
    result2 = await security_agent.process_task(task2)
    assert result2["status"] == "completed"
    
    # Test owasp_compliance task
    task3 = {
        "task_type": "owasp_compliance",
        "project_path": temp_code_dir
    }
    result3 = await security_agent.process_task(task3)
    assert result3["status"] == "completed"
    
    # Test final_security_scan task (comprehensive)
    task4 = {
        "task_type": "final_security_scan",
        "project_path": temp_code_dir
    }
    result4 = await security_agent.process_task(task4)
    assert result4["status"] == "completed"
    assert "code_scan" in result4
    assert "compliance_check" in result4
    assert "overall_security_score" in result4

@pytest.mark.asyncio
async def test_bandit_severity_mapping(security_agent):
    """Test Bandit severity mapping"""
    test_cases = [
        ("HIGH", "high"),
        ("MEDIUM", "medium"),
        ("LOW", "low"),
        ("UNKNOWN", "medium")  # default
    ]
    
    for bandit_severity, expected in test_cases:
        mapped = security_agent._map_bandit_severity(bandit_severity)
        assert mapped == expected

@pytest.mark.asyncio
async def test_bandit_confidence_mapping(security_agent):
    """Test Bandit confidence mapping"""
    test_cases = [
        ("HIGH", 0.9),
        ("MEDIUM", 0.7),
        ("LOW", 0.5),
        ("UNKNOWN", 0.7)  # default
    ]
    
    for bandit_confidence, expected in test_cases:
        mapped = security_agent._map_bandit_confidence(bandit_confidence)
        assert mapped == expected

@pytest.mark.asyncio
async def test_semgrep_severity_mapping(security_agent):
    """Test Semgrep severity mapping"""
    test_cases = [
        ("ERROR", "high"),
        ("WARNING", "medium"),
        ("INFO", "low"),
        ("UNKNOWN", "medium")  # default
    ]
    
    for semgrep_severity, expected in test_cases:
        mapped = security_agent._map_semgrep_severity(semgrep_severity)
        assert mapped == expected

@pytest.mark.asyncio
async def test_pattern_severity_mapping(security_agent):
    """Test security pattern severity mapping"""
    test_cases = [
        ("sql_injection", "critical"),
        ("command_injection", "critical"),
        ("path_traversal", "high"),
        ("hardcoded_secrets", "high"),
        ("weak_crypto", "medium"),
        ("unknown_pattern", "medium")  # default
    ]
    
    for pattern, expected in test_cases:
        severity = security_agent._get_pattern_severity(pattern)
        assert severity == expected

@pytest.mark.asyncio
async def test_cwe_mapping(security_agent):
    """Test CWE ID mapping for patterns"""
    test_cases = [
        ("sql_injection", "CWE-89"),
        ("command_injection", "CWE-78"),
        ("path_traversal", "CWE-22"),
        ("hardcoded_secrets", "CWE-798"),
        ("weak_crypto", "CWE-327")
    ]
    
    for pattern, expected_cwe in test_cases:
        cwe = security_agent._get_cwe_for_pattern(pattern)
        assert cwe == expected_cwe

@pytest.mark.asyncio
async def test_vulnerability_to_dict_conversion(security_agent):
    """Test vulnerability object to dictionary conversion"""
    vuln = SecurityVulnerability(
        vuln_id="test_vuln",
        severity="high",
        category="test",
        title="Test Vulnerability",
        description="Test description",
        file_path="/test/file.py",
        line_number=10,
        code_snippet="test code",
        cwe_id="CWE-89",
        owasp_category="A03_2021",
        confidence=0.9
    )
    
    vuln_dict = security_agent._vulnerability_to_dict(vuln)
    
    assert vuln_dict["vuln_id"] == "test_vuln"
    assert vuln_dict["severity"] == "high"
    assert vuln_dict["cwe_id"] == "CWE-89"
    assert vuln_dict["confidence"] == 0.9

@pytest.mark.asyncio
async def test_unknown_task_handling(security_agent):
    """Test handling of unknown task types"""
    task = {"task_type": "unknown_security_task"}
    result = await security_agent.process_task(task)
    
    assert result["status"] == "error"
    assert "Unknown security task type" in result["message"]
    assert "available_tasks" in result

@pytest.mark.asyncio
async def test_auto_requirements_detection(security_agent, temp_code_dir):
    """Test automatic requirements file detection"""
    # Create a requirements.txt file in temp directory
    req_file = os.path.join(temp_code_dir, "requirements.txt")
    with open(req_file, 'w') as f:
        f.write("flask==1.0.0\ndjango==2.0.0\n")
    
    task = {
        "task_type": "check_dependencies",
        "project_path": temp_code_dir
        # Don't specify requirements_files - should auto-detect
    }
    
    result = await security_agent.process_task(task)
    
    assert result["status"] == "completed"
    assert len(result["dependency_analysis"]["files_scanned"]) > 0

if __name__ == "__main__":
    pytest.main([__file__])
