
"""
Learning Agent - Adaptive intelligence and continuous learning for NEXUS system
Task 11: Pattern analysis, knowledge base management, and adaptive recommendations
"""
import asyncio
import json
import pickle
import sqlite3
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import re
import ast
from collections import defaultdict, Counter
import os
import sys

# Add parent directory to path for imports  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = Path(__file__).resolve().parent.parent

from core.base_agent import BaseAgent
from core.messaging import MessageBus, Message, MessageType
from core.ollama_client import ollama_client

@dataclass
class CodePattern:
    pattern_id: str
    pattern_type: str  # function, class, import, architecture, etc.
    code_snippet: str
    description: str
    frequency: int = 1
    success_rate: float = 1.0
    technologies: List[str] = field(default_factory=list)
    contexts: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)

@dataclass
class ProjectOutcome:
    project_id: str
    project_type: str
    technologies: List[str]
    requirements: Dict[str, Any]
    success_metrics: Dict[str, Any]
    patterns_used: List[str]
    completion_time: float
    success_score: float
    issues_encountered: List[str] = field(default_factory=list)
    completed_at: datetime = field(default_factory=datetime.now)

@dataclass
class Recommendation:
    recommendation_id: str
    type: str  # pattern, technology, architecture, improvement
    title: str
    description: str
    confidence: float
    context: Dict[str, Any]
    supporting_evidence: List[str] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)
    estimated_impact: str = "medium"  # low, medium, high

class LearningAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("learning", "Adaptive Learning Agent", config)
        
        # Learning infrastructure
        self.knowledge_base_path = config.get('agents', {}).get('learning', {}).get(
            'knowledge_base_path', str(BASE_DIR / 'knowledge')
        )
        self.setup_knowledge_base()
        
        # Pattern recognition
        self.code_patterns: Dict[str, CodePattern] = {}
        self.project_outcomes: Dict[str, ProjectOutcome] = {}
        self.pattern_similarity_threshold = config.get('agents', {}).get('learning', {}).get(
            'pattern_similarity_threshold', 0.85
        )
        
        # Learning models and algorithms
        self.pattern_frequencies: Dict[str, int] = defaultdict(int)
        self.technology_correlations: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.success_predictors: Dict[str, float] = defaultdict(float)
        
        # Recommendation engine
        self.recommendation_cache: Dict[str, List[Recommendation]] = {}
        self.feedback_data: List[Dict[str, Any]] = []
        
        # Learning metrics
        self.learning_metrics = {
            "patterns_learned": 0,
            "projects_analyzed": 0,
            "recommendations_made": 0,
            "recommendation_accuracy": 0.0,
            "knowledge_base_size": 0,
            "learning_rate": 0.01,
            "model_version": "1.0.0"
        }
        
        # Load existing knowledge
        self.load_knowledge_base()
        self.load_learning_models()
        
        # Start background learning tasks
        self._start_background_learning()
    
    def get_capabilities(self) -> List[str]:
        return [
            "code_pattern_analysis",
            "project_outcome_analysis", 
            "adaptive_recommendations",
            "knowledge_base_management",
            "style_learning_adaptation",
            "performance_pattern_recognition",
            "technology_trend_analysis",
            "agent_capability_enhancement",
            "predictive_analytics",
            "continuous_learning",
            "pattern_mining",
            "semantic_similarity_search",
            "recommendation_engine",
            "feedback_processing",
            "knowledge_extraction"
        ]
    
    def setup_knowledge_base(self):
        """Setup SQLite knowledge base for persistent storage"""
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        
        self.db_path = os.path.join(self.knowledge_base_path, "learning.db")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS code_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT,
                    code_snippet TEXT,
                    description TEXT,
                    frequency INTEGER,
                    success_rate REAL,
                    technologies TEXT,
                    contexts TEXT,
                    metrics TEXT,
                    created_at TEXT,
                    last_seen TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_outcomes (
                    project_id TEXT PRIMARY KEY,
                    project_type TEXT,
                    technologies TEXT,
                    requirements TEXT,
                    success_metrics TEXT,
                    patterns_used TEXT,
                    completion_time REAL,
                    success_score REAL,
                    issues_encountered TEXT,
                    completed_at TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    recommendation_id TEXT PRIMARY KEY,
                    type TEXT,
                    title TEXT,
                    description TEXT,
                    confidence REAL,
                    context TEXT,
                    supporting_evidence TEXT,
                    implementation_steps TEXT,
                    estimated_impact TEXT,
                    created_at TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id TEXT PRIMARY KEY,
                    recommendation_id TEXT,
                    rating INTEGER,
                    feedback_text TEXT,
                    implemented BOOLEAN,
                    outcome TEXT,
                    created_at TEXT
                )
            ''')
            
            conn.commit()
    
    def load_knowledge_base(self):
        """Load existing knowledge from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Load code patterns
                cursor.execute("SELECT * FROM code_patterns")
                for row in cursor.fetchall():
                    pattern = CodePattern(
                        pattern_id=row[0],
                        pattern_type=row[1],
                        code_snippet=row[2],
                        description=row[3],
                        frequency=row[4],
                        success_rate=row[5],
                        technologies=json.loads(row[6]) if row[6] else [],
                        contexts=json.loads(row[7]) if row[7] else [],
                        metrics=json.loads(row[8]) if row[8] else {},
                        created_at=datetime.fromisoformat(row[9]),
                        last_seen=datetime.fromisoformat(row[10])
                    )
                    self.code_patterns[pattern.pattern_id] = pattern
                
                # Load project outcomes
                cursor.execute("SELECT * FROM project_outcomes")
                for row in cursor.fetchall():
                    outcome = ProjectOutcome(
                        project_id=row[0],
                        project_type=row[1],
                        technologies=json.loads(row[2]) if row[2] else [],
                        requirements=json.loads(row[3]) if row[3] else {},
                        success_metrics=json.loads(row[4]) if row[4] else {},
                        patterns_used=json.loads(row[5]) if row[5] else [],
                        completion_time=row[6],
                        success_score=row[7],
                        issues_encountered=json.loads(row[8]) if row[8] else [],
                        completed_at=datetime.fromisoformat(row[9])
                    )
                    self.project_outcomes[outcome.project_id] = outcome
                
                self.learning_metrics["knowledge_base_size"] = len(self.code_patterns)
                self.learning_metrics["projects_analyzed"] = len(self.project_outcomes)
                
        except Exception as e:
            self.logger.error(f"Error loading knowledge base: {str(e)}")
    
    def load_learning_models(self):
        """Load pre-trained learning models"""
        models_path = os.path.join(self.knowledge_base_path, "models")
        os.makedirs(models_path, exist_ok=True)
        
        try:
            # Load pattern frequencies
            freq_path = os.path.join(models_path, "pattern_frequencies.pkl")
            if os.path.exists(freq_path):
                with open(freq_path, 'rb') as f:
                    self.pattern_frequencies = pickle.load(f)
            
            # Load technology correlations
            corr_path = os.path.join(models_path, "tech_correlations.pkl")
            if os.path.exists(corr_path):
                with open(corr_path, 'rb') as f:
                    self.technology_correlations = pickle.load(f)
            
            # Load success predictors
            pred_path = os.path.join(models_path, "success_predictors.pkl")
            if os.path.exists(pred_path):
                with open(pred_path, 'rb') as f:
                    self.success_predictors = pickle.load(f)
                    
        except Exception as e:
            self.logger.error(f"Error loading learning models: {str(e)}")
    
    def save_learning_models(self):
        """Save learning models to disk"""
        models_path = os.path.join(self.knowledge_base_path, "models")
        
        try:
            # Save pattern frequencies
            with open(os.path.join(models_path, "pattern_frequencies.pkl"), 'wb') as f:
                pickle.dump(dict(self.pattern_frequencies), f)
            
            # Save technology correlations
            with open(os.path.join(models_path, "tech_correlations.pkl"), 'wb') as f:
                pickle.dump(dict(self.technology_correlations), f)
            
            # Save success predictors
            with open(os.path.join(models_path, "success_predictors.pkl"), 'wb') as f:
                pickle.dump(dict(self.success_predictors), f)
                
        except Exception as e:
            self.logger.error(f"Error saving learning models: {str(e)}")
    
    def _start_background_learning(self):
        """Start background tasks for continuous learning"""
        try:
            # Only start background tasks if there's a running event loop
            loop = asyncio.get_running_loop()
            self.background_tasks = [
                loop.create_task(self._continuous_pattern_analysis()),
                loop.create_task(self._model_retraining()),
                loop.create_task(self._knowledge_optimization())
            ]
        except RuntimeError:
            # No running event loop (e.g., during tests) - skip background tasks
            self.logger.debug("No running event loop - skipping background learning tasks")
            self.background_tasks = []
    
    async def _continuous_pattern_analysis(self):
        """Background task for continuous pattern analysis"""
        while True:
            try:
                # Analyze new patterns from recent projects
                await self._analyze_recent_patterns()
                await asyncio.sleep(300)  # Run every 5 minutes
            except Exception as e:
                self.logger.error(f"Error in continuous pattern analysis: {str(e)}")
    
    async def _model_retraining(self):
        """Background task for retraining learning models"""
        while True:
            try:
                await self._retrain_models()
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                self.logger.error(f"Error in model retraining: {str(e)}")
    
    async def _knowledge_optimization(self):
        """Background task for knowledge base optimization"""
        while True:
            try:
                await self._optimize_knowledge_base()
                await asyncio.sleep(1800)  # Run every 30 minutes
            except Exception as e:
                self.logger.error(f"Error in knowledge optimization: {str(e)}")
    
    async def analyze_code_patterns(self, code_samples: List[str], 
                                   context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze code samples to identify and learn patterns"""
        if context is None:
            context = {}
            
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "samples_analyzed": len(code_samples),
            "patterns_found": [],
            "new_patterns": [],
            "pattern_improvements": [],
            "recommendations": []
        }
        
        for i, code in enumerate(code_samples):
            try:
                # Extract patterns from code
                patterns = await self._extract_patterns_from_code(code, context)
                
                for pattern_data in patterns:
                    # Generate pattern ID
                    pattern_id = self._generate_pattern_id(pattern_data["code"])
                    
                    if pattern_id in self.code_patterns:
                        # Update existing pattern
                        existing_pattern = self.code_patterns[pattern_id]
                        existing_pattern.frequency += 1
                        existing_pattern.last_seen = datetime.now()
                        
                        # Update success rate based on context
                        if context.get("success_metrics"):
                            success_score = context["success_metrics"].get("overall_score", 1.0)
                            existing_pattern.success_rate = (
                                existing_pattern.success_rate * (existing_pattern.frequency - 1) + success_score
                            ) / existing_pattern.frequency
                        
                        analysis_results["pattern_improvements"].append({
                            "pattern_id": pattern_id,
                            "frequency": existing_pattern.frequency,
                            "success_rate": existing_pattern.success_rate
                        })
                        
                    else:
                        # Create new pattern
                        new_pattern = CodePattern(
                            pattern_id=pattern_id,
                            pattern_type=pattern_data["type"],
                            code_snippet=pattern_data["code"],
                            description=pattern_data["description"],
                            technologies=context.get("technologies", []),
                            contexts=[context.get("project_type", "unknown")],
                            metrics=context.get("success_metrics", {})
                        )
                        
                        self.code_patterns[pattern_id] = new_pattern
                        analysis_results["new_patterns"].append({
                            "pattern_id": pattern_id,
                            "type": pattern_data["type"],
                            "description": pattern_data["description"]
                        })
                        
                        self.learning_metrics["patterns_learned"] += 1
                    
                    analysis_results["patterns_found"].append({
                        "pattern_id": pattern_id,
                        "type": pattern_data["type"],
                        "sample_index": i
                    })
                
            except Exception as e:
                self.logger.error(f"Error analyzing code sample {i}: {str(e)}")
        
        # Generate recommendations based on analysis
        recommendations = await self._generate_pattern_recommendations(analysis_results, context)
        analysis_results["recommendations"] = recommendations
        
        # Save patterns to database
        await self._save_patterns_to_db()
        
        # Update learning metrics
        self.learning_metrics["knowledge_base_size"] = len(self.code_patterns)
        
        return {
            "status": "completed",
            "result": "Code pattern analysis completed",
            "analysis": analysis_results
        }
    
    async def _extract_patterns_from_code(self, code: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract patterns from code using AST and LLM analysis"""
        patterns = []
        
        try:
            # AST-based pattern extraction
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    patterns.append({
                        "type": "function",
                        "code": ast.get_source_segment(code, node) or code,
                        "description": f"Function: {node.name}",
                        "ast_info": {
                            "name": node.name,
                            "args": len(node.args.args),
                            "decorators": len(node.decorator_list)
                        }
                    })
                
                elif isinstance(node, ast.ClassDef):
                    patterns.append({
                        "type": "class",
                        "code": ast.get_source_segment(code, node) or code,
                        "description": f"Class: {node.name}",
                        "ast_info": {
                            "name": node.name,
                            "bases": len(node.bases),
                            "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                        }
                    })
        
        except SyntaxError:
            # If AST fails, use regex patterns
            patterns.extend(self._extract_regex_patterns(code))
        
        # LLM-enhanced pattern analysis
        if len(patterns) > 0:
            enhanced_patterns = await self._enhance_patterns_with_llm(patterns, context)
            return enhanced_patterns
        
        return patterns
    
    def _extract_regex_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Extract patterns using regex when AST fails"""
        patterns = []
        
        # Common patterns
        regex_patterns = {
            "import": r"^(import|from)\s+[\w\.]+",
            "async_function": r"async\s+def\s+(\w+)",
            "class_definition": r"class\s+(\w+)",
            "decorator": r"@\w+",
            "exception_handling": r"try:|except|finally:",
            "comprehension": r"\[(.*?)\s+for\s+.*?\]"
        }
        
        for pattern_type, regex in regex_patterns.items():
            matches = re.findall(regex, code, re.MULTILINE)
            for match in matches:
                patterns.append({
                    "type": pattern_type,
                    "code": match if isinstance(match, str) else str(match),
                    "description": f"{pattern_type.title()} pattern"
                })
        
        return patterns
    
    async def _enhance_patterns_with_llm(self, patterns: List[Dict[str, Any]], 
                                       context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use LLM to enhance pattern descriptions and categorization"""
        if not patterns:
            return patterns
        
        try:
            system_prompt = """Du bist ein erfahrener Software-Architekt mit Expertise in Codeanalyse und Mustererkennung.
            Analysiere die gegebenen Code-Patterns und verbessere ihre Beschreibungen mit:
            1. Technische Kategorisierung
            2. Verwendungszweck und Kontext
            3. Best-Practice-Bewertung
            4. Potentielle Verbesserungen
            
            Antworte im JSON-Format mit erweiterten Pattern-Beschreibungen."""
            
            user_prompt = f"""Analysiere diese Code-Patterns:
            
            Patterns: {json.dumps(patterns, indent=2)}
            
            Kontext: {json.dumps(context, indent=2)}
            
            Erweitere jeden Pattern mit:
            - Verbesserte Beschreibung
            - Technische Kategorie
            - Verwendungskontext
            - Quality Score (1-10)
            - Verbesserungsvorschläge
            """
            
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('learning', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                enhanced_text = response.get('response', '{}')
                try:
                    enhanced_patterns = json.loads(enhanced_text)
                    if isinstance(enhanced_patterns, list):
                        return enhanced_patterns
                except json.JSONDecodeError:
                    pass
                
        except Exception as e:
            self.logger.error(f"Error enhancing patterns with LLM: {str(e)}")
        
        return patterns
    
    def _generate_pattern_id(self, code: str) -> str:
        """Generate unique ID for a code pattern"""
        # Normalize code by removing whitespace and comments
        normalized = re.sub(r'\s+', ' ', code.strip())
        normalized = re.sub(r'#.*?\n', '', normalized)
        
        return hashlib.md5(normalized.encode()).hexdigest()[:16]
    
    async def learn_from_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from completed project outcomes"""
        project_id = project_data.get("project_id", str(datetime.now().timestamp()))
        
        # Extract project outcome data
        outcome = ProjectOutcome(
            project_id=project_id,
            project_type=project_data.get("project_type", "unknown"),
            technologies=project_data.get("technologies", []),
            requirements=project_data.get("requirements", {}),
            success_metrics=project_data.get("success_metrics", {}),
            patterns_used=project_data.get("patterns_used", []),
            completion_time=project_data.get("completion_time", 0),
            success_score=project_data.get("success_score", 0.5),
            issues_encountered=project_data.get("issues_encountered", [])
        )
        
        # Store project outcome
        self.project_outcomes[project_id] = outcome
        
        # Update learning models
        await self._update_learning_models(outcome)
        
        # Analyze patterns used in successful projects
        if outcome.success_score > 0.7:  # Successful project
            for pattern_id in outcome.patterns_used:
                if pattern_id in self.code_patterns:
                    pattern = self.code_patterns[pattern_id]
                    # Increase pattern success rate
                    pattern.success_rate = min(1.0, pattern.success_rate * 1.1)
        
        # Save to database
        await self._save_project_outcome_to_db(outcome)
        
        self.learning_metrics["projects_analyzed"] += 1
        
        return {
            "status": "completed",
            "result": "Project learning completed",
            "project_id": project_id,
            "patterns_updated": len(outcome.patterns_used),
            "success_score": outcome.success_score
        }
    
    async def _update_learning_models(self, outcome: ProjectOutcome):
        """Update learning models based on project outcome"""
        # Update technology correlations
        for i, tech1 in enumerate(outcome.technologies):
            for tech2 in outcome.technologies[i+1:]:
                if tech2 not in self.technology_correlations[tech1]:
                    self.technology_correlations[tech1][tech2] = 0
                
                # Increase correlation based on success
                correlation_boost = outcome.success_score * 0.1
                self.technology_correlations[tech1][tech2] += correlation_boost
                self.technology_correlations[tech2][tech1] += correlation_boost
        
        # Update success predictors
        project_features = self._extract_project_features(outcome)
        for feature, value in project_features.items():
            if feature not in self.success_predictors:
                self.success_predictors[feature] = 0
            
            # Simple moving average update
            learning_rate = self.learning_metrics["learning_rate"]
            self.success_predictors[feature] = (
                (1 - learning_rate) * self.success_predictors[feature] +
                learning_rate * outcome.success_score * value
            )
    
    def _extract_project_features(self, outcome: ProjectOutcome) -> Dict[str, float]:
        """Extract numerical features from project outcome"""
        features = {}
        
        # Technology features
        for tech in outcome.technologies:
            features[f"uses_{tech}"] = 1.0
        
        # Complexity features
        features["tech_count"] = len(outcome.technologies)
        features["completion_time"] = min(outcome.completion_time / 100.0, 1.0)  # Normalize
        features["patterns_used"] = len(outcome.patterns_used)
        features["issues_count"] = len(outcome.issues_encountered)
        
        # Project type features
        features[f"type_{outcome.project_type}"] = 1.0
        
        return features
    
    async def get_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate context-aware recommendations"""
        context_hash = hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()
        
        # Check cache first
        if context_hash in self.recommendation_cache:
            cached_recommendations = self.recommendation_cache[context_hash]
            # Return if cache is fresh (less than 1 hour old)
            if (datetime.now() - cached_recommendations[0].created_at if cached_recommendations else timedelta(hours=2)) < timedelta(hours=1):
                return [self._recommendation_to_dict(rec) for rec in cached_recommendations]
        
        recommendations = []
        
        # Pattern-based recommendations
        pattern_recs = await self._get_pattern_recommendations(context)
        recommendations.extend(pattern_recs)
        
        # Technology recommendations
        tech_recs = await self._get_technology_recommendations(context)
        recommendations.extend(tech_recs)
        
        # Architecture recommendations
        arch_recs = await self._get_architecture_recommendations(context)
        recommendations.extend(arch_recs)
        
        # Performance optimization recommendations
        perf_recs = await self._get_performance_recommendations(context)
        recommendations.extend(perf_recs)
        
        # Sort by confidence and relevance
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        
        # Limit to top recommendations
        top_recommendations = recommendations[:10]
        
        # Cache recommendations
        self.recommendation_cache[context_hash] = top_recommendations
        
        # Update metrics
        self.learning_metrics["recommendations_made"] += len(top_recommendations)
        
        return [self._recommendation_to_dict(rec) for rec in top_recommendations]
    
    def _recommendation_to_dict(self, rec: Recommendation) -> Dict[str, Any]:
        """Convert Recommendation object to dictionary"""
        return {
            "recommendation_id": rec.recommendation_id,
            "type": rec.type,
            "title": rec.title,
            "description": rec.description,
            "confidence": rec.confidence,
            "context": rec.context,
            "supporting_evidence": rec.supporting_evidence,
            "implementation_steps": rec.implementation_steps,
            "estimated_impact": rec.estimated_impact
        }
    
    async def _get_pattern_recommendations(self, context: Dict[str, Any]) -> List[Recommendation]:
        """Get pattern-based recommendations"""
        recommendations = []
        
        project_type = context.get("project_type", "")
        technologies = context.get("technologies", [])
        
        # Find high-success patterns for similar contexts
        relevant_patterns = []
        for pattern in self.code_patterns.values():
            if (pattern.success_rate > 0.8 and 
                pattern.frequency > 3 and
                any(tech in pattern.technologies for tech in technologies)):
                relevant_patterns.append(pattern)
        
        # Sort by success rate and frequency
        relevant_patterns.sort(key=lambda p: p.success_rate * p.frequency, reverse=True)
        
        for pattern in relevant_patterns[:5]:
            rec = Recommendation(
                recommendation_id=f"pattern_{pattern.pattern_id}",
                type="pattern",
                title=f"Use {pattern.pattern_type} pattern: {pattern.description}",
                description=f"This pattern has a {pattern.success_rate:.0%} success rate "
                           f"and has been used {pattern.frequency} times successfully.",
                confidence=min(0.95, pattern.success_rate * (pattern.frequency / 10)),
                context={"pattern_id": pattern.pattern_id},
                supporting_evidence=[
                    f"Success rate: {pattern.success_rate:.0%}",
                    f"Usage frequency: {pattern.frequency}",
                    f"Compatible technologies: {', '.join(pattern.technologies)}"
                ],
                implementation_steps=[
                    "Review the pattern implementation",
                    "Adapt pattern to your specific context",
                    "Test pattern integration",
                    "Monitor pattern performance"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _get_technology_recommendations(self, context: Dict[str, Any]) -> List[Recommendation]:
        """Get technology stack recommendations"""
        recommendations = []
        
        current_technologies = set(context.get("technologies", []))
        project_type = context.get("project_type", "")
        
        # Find technology combinations that work well together
        for tech1 in current_technologies:
            if tech1 in self.technology_correlations:
                for tech2, correlation in self.technology_correlations[tech1].items():
                    if tech2 not in current_technologies and correlation > 0.5:
                        rec = Recommendation(
                            recommendation_id=f"tech_{tech1}_{tech2}",
                            type="technology",
                            title=f"Consider adding {tech2}",
                            description=f"{tech2} works well with {tech1} and could enhance your project.",
                            confidence=min(0.9, correlation),
                            context={"suggested_tech": tech2, "based_on": tech1},
                            supporting_evidence=[
                                f"Correlation with {tech1}: {correlation:.2f}",
                                f"Successful projects using both: {int(correlation * 100)}"
                            ],
                            implementation_steps=[
                                f"Evaluate {tech2} compatibility",
                                f"Plan {tech2} integration",
                                "Update project dependencies",
                                "Test integration"
                            ]
                        )
                        recommendations.append(rec)
        
        return recommendations
    
    async def _get_architecture_recommendations(self, context: Dict[str, Any]) -> List[Recommendation]:
        """Get architecture recommendations using LLM"""
        recommendations = []
        
        try:
            system_prompt = """Du bist ein Senior Software-Architekt mit 20+ Jahren Erfahrung.
            Analysiere den Projektkontext und gib spezifische Architektur-Empfehlungen basierend auf:
            1. Best Practices für den Projekttyp
            2. Technologie-Stack Kompatibilität 
            3. Skalierbarkeits-Überlegungen
            4. Wartbarkeit und Testbarkeit
            
            Fokussiere auf umsetzbare, konkrete Empfehlungen."""
            
            user_prompt = f"""Projektkontext:
            {json.dumps(context, indent=2)}
            
            Basierend auf erfolgreichen Mustern, empfehle 2-3 spezifische Architektur-Verbesserungen.
            Für jede Empfehlung gib an:
            - Titel (kurz und prägnant)
            - Beschreibung (detailliert)
            - Implementierungsschritte
            - Geschätzter Impact (low/medium/high)
            
            Antworte im JSON-Format:
            [{
                "title": "...",
                "description": "...",
                "implementation_steps": ["...", "..."],
                "estimated_impact": "medium"
            }]"""
            
            async with ollama_client:
                response = await ollama_client.generate(
                    model=self.config.get('agents', {}).get('learning', {}).get('model', 'qwen2.5-coder:7b'),
                    prompt=user_prompt,
                    system=system_prompt
                )
                
                arch_text = response.get('response', '[]')
                try:
                    arch_suggestions = json.loads(arch_text)
                    
                    for i, suggestion in enumerate(arch_suggestions):
                        rec = Recommendation(
                            recommendation_id=f"arch_{i}_{datetime.now().timestamp()}",
                            type="architecture",
                            title=suggestion.get("title", "Architecture Improvement"),
                            description=suggestion.get("description", ""),
                            confidence=0.75,  # Medium confidence for LLM recommendations
                            context=context,
                            supporting_evidence=["Based on architectural best practices"],
                            implementation_steps=suggestion.get("implementation_steps", []),
                            estimated_impact=suggestion.get("estimated_impact", "medium")
                        )
                        recommendations.append(rec)
                        
                except json.JSONDecodeError:
                    self.logger.warning("Could not parse architecture recommendations from LLM")
                    
        except Exception as e:
            self.logger.error(f"Error getting architecture recommendations: {str(e)}")
        
        return recommendations
    
    async def _get_performance_recommendations(self, context: Dict[str, Any]) -> List[Recommendation]:
        """Get performance optimization recommendations"""
        recommendations = []
        
        # Analyze patterns for performance insights
        perf_patterns = [
            pattern for pattern in self.code_patterns.values()
            if "performance" in pattern.description.lower() or 
               "optimization" in pattern.description.lower() or
               "async" in pattern.code_snippet.lower()
        ]
        
        if perf_patterns:
            best_perf_pattern = max(perf_patterns, key=lambda p: p.success_rate * p.frequency)
            
            rec = Recommendation(
                recommendation_id=f"perf_{best_perf_pattern.pattern_id}",
                type="performance", 
                title="Performance Optimization Pattern",
                description=f"Apply the {best_perf_pattern.description} pattern to improve performance.",
                confidence=best_perf_pattern.success_rate * 0.8,
                context={"pattern_id": best_perf_pattern.pattern_id},
                supporting_evidence=[
                    f"Pattern success rate: {best_perf_pattern.success_rate:.0%}",
                    f"Used in {best_perf_pattern.frequency} successful projects"
                ],
                implementation_steps=[
                    "Identify performance bottlenecks",
                    "Apply optimization pattern",
                    "Benchmark before and after",
                    "Monitor performance impact"
                ],
                estimated_impact="high"
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _generate_pattern_recommendations(self, analysis: Dict[str, Any], 
                                             context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on pattern analysis"""
        recommendations = []
        
        # Recommend similar successful patterns
        if analysis["patterns_found"]:
            similar_patterns = self._find_similar_patterns(analysis["patterns_found"], context)
            
            for pattern_id in similar_patterns[:3]:
                if pattern_id in self.code_patterns:
                    pattern = self.code_patterns[pattern_id]
                    recommendations.append({
                        "type": "similar_pattern",
                        "title": f"Consider pattern: {pattern.description}",
                        "description": f"This pattern is similar to ones you're using and has {pattern.success_rate:.0%} success rate",
                        "confidence": pattern.success_rate * 0.8,
                        "pattern_id": pattern_id
                    })
        
        return recommendations
    
    def _find_similar_patterns(self, current_patterns: List[Dict[str, Any]], 
                             context: Dict[str, Any]) -> List[str]:
        """Find similar patterns in knowledge base"""
        similar = []
        
        current_types = set(p["type"] for p in current_patterns)
        context_techs = set(context.get("technologies", []))
        
        for pattern_id, pattern in self.code_patterns.items():
            if pattern.pattern_type in current_types:
                tech_overlap = len(set(pattern.technologies) & context_techs)
                if tech_overlap > 0:
                    similar.append((pattern_id, tech_overlap, pattern.success_rate))
        
        # Sort by tech overlap and success rate
        similar.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        return [pattern_id for pattern_id, _, _ in similar]
    
    async def predict_project_outcome(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Predict project outcome based on learned patterns"""
        features = self._extract_config_features(project_config)
        
        # Calculate success probability
        success_score = 0.5  # Base score
        confidence = 0.5
        
        # Apply learned predictors
        for feature, value in features.items():
            if feature in self.success_predictors:
                predictor_weight = self.success_predictors[feature]
                success_score += predictor_weight * value * 0.1
                confidence += 0.05
        
        # Normalize scores
        success_score = max(0.0, min(1.0, success_score))
        confidence = max(0.0, min(1.0, confidence))
        
        # Find similar historical projects
        similar_projects = self._find_similar_projects(project_config)
        
        prediction = {
            "predicted_success_score": success_score,
            "confidence": confidence,
            "risk_factors": [],
            "success_factors": [],
            "similar_projects": similar_projects,
            "estimated_completion_time": self._estimate_completion_time(project_config),
            "recommended_technologies": [],
            "potential_issues": []
        }
        
        # Add risk factors
        if features.get("tech_count", 0) > 5:
            prediction["risk_factors"].append("High technology complexity")
        
        if features.get("issues_count", 0) > 0:
            prediction["risk_factors"].append("Historical issues in similar projects")
        
        # Add success factors
        high_success_techs = [
            tech for tech in project_config.get("technologies", [])
            if self.success_predictors.get(f"uses_{tech}", 0) > 0.7
        ]
        
        if high_success_techs:
            prediction["success_factors"].append(f"Using proven technologies: {', '.join(high_success_techs)}")
        
        return {
            "status": "completed",
            "result": "Project outcome prediction completed",
            "prediction": prediction
        }
    
    def _extract_config_features(self, config: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from project configuration"""
        features = {}
        
        # Technology features
        for tech in config.get("technologies", []):
            features[f"uses_{tech}"] = 1.0
        
        # Complexity features  
        features["tech_count"] = len(config.get("technologies", []))
        
        # Project type features
        project_type = config.get("project_type", "unknown")
        features[f"type_{project_type}"] = 1.0
        
        return features
    
    def _find_similar_projects(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find similar historical projects"""
        config_techs = set(config.get("technologies", []))
        project_type = config.get("project_type", "")
        
        similar = []
        for outcome in self.project_outcomes.values():
            similarity_score = 0
            
            # Technology overlap
            tech_overlap = len(set(outcome.technologies) & config_techs)
            similarity_score += tech_overlap
            
            # Project type match
            if outcome.project_type == project_type:
                similarity_score += 3
            
            if similarity_score > 0:
                similar.append({
                    "project_id": outcome.project_id,
                    "similarity_score": similarity_score,
                    "success_score": outcome.success_score,
                    "completion_time": outcome.completion_time,
                    "technologies": outcome.technologies
                })
        
        # Sort by similarity
        similar.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return similar[:5]
    
    def _estimate_completion_time(self, config: Dict[str, Any]) -> float:
        """Estimate project completion time based on historical data"""
        project_type = config.get("project_type", "unknown")
        tech_count = len(config.get("technologies", []))
        
        # Base estimates by project type
        base_estimates = {
            "web_application": 40.0,
            "api_service": 25.0,
            "mobile_app": 60.0,
            "data_pipeline": 30.0,
            "unknown": 35.0
        }
        
        base_time = base_estimates.get(project_type, 35.0)
        
        # Adjust for complexity
        complexity_factor = 1.0 + (tech_count - 3) * 0.2
        
        # Use historical data if available
        similar_projects = self._find_similar_projects(config)
        if similar_projects:
            avg_time = sum(p["completion_time"] for p in similar_projects) / len(similar_projects)
            base_time = (base_time + avg_time) / 2
        
        return base_time * complexity_factor
    
    async def _save_patterns_to_db(self):
        """Save code patterns to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for pattern in self.code_patterns.values():
                    cursor.execute('''
                        INSERT OR REPLACE INTO code_patterns 
                        (pattern_id, pattern_type, code_snippet, description, frequency, 
                         success_rate, technologies, contexts, metrics, created_at, last_seen)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        pattern.pattern_id,
                        pattern.pattern_type,
                        pattern.code_snippet,
                        pattern.description,
                        pattern.frequency,
                        pattern.success_rate,
                        json.dumps(pattern.technologies),
                        json.dumps(pattern.contexts),
                        json.dumps(pattern.metrics),
                        pattern.created_at.isoformat(),
                        pattern.last_seen.isoformat()
                    ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error saving patterns to database: {str(e)}")
    
    async def _save_project_outcome_to_db(self, outcome: ProjectOutcome):
        """Save project outcome to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO project_outcomes
                    (project_id, project_type, technologies, requirements, success_metrics,
                     patterns_used, completion_time, success_score, issues_encountered, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    outcome.project_id,
                    outcome.project_type,
                    json.dumps(outcome.technologies),
                    json.dumps(outcome.requirements),
                    json.dumps(outcome.success_metrics),
                    json.dumps(outcome.patterns_used),
                    outcome.completion_time,
                    outcome.success_score,
                    json.dumps(outcome.issues_encountered),
                    outcome.completed_at.isoformat()
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error saving project outcome to database: {str(e)}")
    
    async def get_learning_metrics(self) -> Dict[str, Any]:
        """Get comprehensive learning metrics"""
        # Calculate advanced metrics
        if self.learning_metrics["recommendations_made"] > 0:
            # Simple accuracy calculation based on feedback
            accuracy = len([f for f in self.feedback_data if f.get("rating", 0) >= 4]) / max(len(self.feedback_data), 1)
            self.learning_metrics["recommendation_accuracy"] = accuracy
        
        return {
            "timestamp": datetime.now().isoformat(),
            "learning_metrics": self.learning_metrics,
            "knowledge_base_stats": {
                "patterns": len(self.code_patterns),
                "project_outcomes": len(self.project_outcomes),
                "technology_correlations": len(self.technology_correlations),
                "success_predictors": len(self.success_predictors)
            },
            "pattern_distribution": self._get_pattern_distribution(),
            "technology_success_rates": self._get_technology_success_rates()
        }
    
    def _get_pattern_distribution(self) -> Dict[str, int]:
        """Get distribution of pattern types"""
        distribution = defaultdict(int)
        for pattern in self.code_patterns.values():
            distribution[pattern.pattern_type] += 1
        return dict(distribution)
    
    def _get_technology_success_rates(self) -> Dict[str, float]:
        """Get success rates by technology"""
        tech_success = defaultdict(list)
        
        for outcome in self.project_outcomes.values():
            for tech in outcome.technologies:
                tech_success[tech].append(outcome.success_score)
        
        success_rates = {}
        for tech, scores in tech_success.items():
            success_rates[tech] = sum(scores) / len(scores) if scores else 0
        
        return success_rates
    
    async def _analyze_recent_patterns(self):
        """Analyze patterns from recent projects"""
        # This would analyze new patterns from recent project files
        # Implementation depends on file system monitoring
        pass
    
    async def _retrain_models(self):
        """Retrain learning models with new data"""
        self.save_learning_models()
        self.logger.info("Learning models retrained and saved")
    
    async def _optimize_knowledge_base(self):
        """Optimize knowledge base for better performance"""
        # Remove low-value patterns
        patterns_to_remove = [
            pattern_id for pattern_id, pattern in self.code_patterns.items()
            if pattern.frequency < 2 and pattern.success_rate < 0.5 and
               (datetime.now() - pattern.last_seen).days > 30
        ]
        
        for pattern_id in patterns_to_remove:
            del self.code_patterns[pattern_id]
        
        if patterns_to_remove:
            self.logger.info(f"Removed {len(patterns_to_remove)} low-value patterns")
            await self._save_patterns_to_db()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process learning tasks"""
        self.status = "working"
        task_type = task.get("task_type", task.get("type", "unknown"))
        
        try:
            if task_type == "analyze_patterns":
                code_samples = task.get("code_samples", [])
                context = task.get("context", {})
                result = await self.analyze_code_patterns(code_samples, context)
                
            elif task_type == "learn_from_project":
                project_data = task.get("project_data", {})
                result = await self.learn_from_project(project_data)
                
            elif task_type == "get_recommendations":
                context = task.get("context", {})
                recommendations = await self.get_recommendations(context)
                result = {
                    "status": "completed", 
                    "result": "Recommendations generated",
                    "recommendations": recommendations
                }
                
            elif task_type == "predict_outcome":
                project_config = task.get("project_config", {})
                result = await self.predict_project_outcome(project_config)
                
            elif task_type == "get_metrics":
                result = await self.get_learning_metrics()
                
            elif task_type == "security_pattern_analysis":
                # Special case for security agent integration
                code_samples = task.get("code_samples", [])
                context = {**task.get("context", {}), "focus": "security"}
                result = await self.analyze_code_patterns(code_samples, context)
                
            else:
                result = {
                    "status": "error",
                    "message": f"Unknown task type: {task_type}",
                    "available_tasks": ["analyze_patterns", "learn_from_project", "get_recommendations", "predict_outcome", "get_metrics"]
                }
            
            self.status = "idle"
            return result
            
        except Exception as e:
            self.status = "error"
            self.logger.error(f"Error processing learning task: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
