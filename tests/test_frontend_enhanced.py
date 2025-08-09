
"""
Tests for Enhanced Frontend Agent (Task 4)
"""
import pytest
import asyncio
import tempfile
import os
import json
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.frontend_enhanced import FrontendEnhancedAgent

class TestFrontendEnhancedAgent:
    """Test cases for the Enhanced Frontend Agent"""
    
    @pytest.fixture
    def agent_config(self):
        return {
            'agents': {
                'frontend': {
                    'model': 'test-model',
                    'technologies': ['react', 'vue', 'angular']
                }
            }
        }
    
    @pytest.fixture
    def frontend_agent(self, agent_config):
        return FrontendEnhancedAgent(agent_config)
    
    def test_initialization(self, frontend_agent):
        """Test agent initialization"""
        assert frontend_agent.agent_id == "frontend_enhanced"
        assert frontend_agent.name == "Enhanced Frontend Developer"
        assert "react" in frontend_agent.frameworks
        assert "tailwind" in frontend_agent.css_frameworks
        assert "redux" in frontend_agent.state_management
    
    def test_capabilities(self, frontend_agent):
        """Test agent capabilities"""
        capabilities = frontend_agent.get_capabilities()
        
        expected_capabilities = [
            "react_development_advanced",
            "vue_development_advanced", 
            "angular_development_advanced",
            "typescript_support",
            "modern_css_frameworks",
            "state_management_implementation",
            "pwa_capabilities",
            "responsive_design",
            "accessibility_features"
        ]
        
        for capability in expected_capabilities:
            assert capability in capabilities
    
    def test_determine_framework(self, frontend_agent):
        """Test framework determination"""
        # Test React detection
        architecture = {"frontend": "react"}
        framework = frontend_agent._determine_framework(architecture, {}, {})
        assert framework == "react"
        
        # Test Vue detection from requirements
        requirements = {"framework": "vue", "ui": "modern"}
        framework = frontend_agent._determine_framework({}, requirements, {})
        assert framework == "vue"
        
        # Test Angular detection from task title
        task = {"title": "Create Angular dashboard"}
        framework = frontend_agent._determine_framework({}, {}, task)
        assert framework == "angular"
        
        # Test default fallback
        framework = frontend_agent._determine_framework({}, {}, {})
        assert framework == "react"
    
    def test_determine_css_framework(self, frontend_agent):
        """Test CSS framework determination"""
        # Test Tailwind detection
        requirements = {"styling": "tailwind css", "ui": "modern"}
        css_fw = frontend_agent._determine_css_framework(requirements)
        assert css_fw == "tailwind"
        
        # Test Material-UI detection
        requirements = {"ui": "material-ui", "design": "google"}
        css_fw = frontend_agent._determine_css_framework(requirements)
        assert css_fw == "material-ui"
        
        # Test Bootstrap detection
        requirements = {"framework": "bootstrap", "responsive": True}
        css_fw = frontend_agent._determine_css_framework(requirements)
        assert css_fw == "bootstrap"
        
        # Test default
        css_fw = frontend_agent._determine_css_framework({})
        assert css_fw == "tailwind"
    
    def test_determine_state_management(self, frontend_agent):
        """Test state management determination"""
        # Test React with Redux
        requirements = {"state": "redux", "complex": True}
        state_mgmt = frontend_agent._determine_state_management("react", requirements)
        assert state_mgmt == "redux"
        
        # Test React with Context API (default)
        state_mgmt = frontend_agent._determine_state_management("react", {})
        assert state_mgmt == "context-api"
        
        # Test Vue with Pinia (default)
        state_mgmt = frontend_agent._determine_state_management("vue", {})
        assert state_mgmt == "pinia"
        
        # Test Angular with NgRx
        state_mgmt = frontend_agent._determine_state_management("angular", {})
        assert state_mgmt == "ngrx"
    
    def test_get_app_css_classes(self, frontend_agent):
        """Test CSS class generation for different frameworks"""
        # Test Tailwind classes
        classes = frontend_agent._get_app_css_classes("tailwind")
        assert "min-h-screen" in classes['container']
        assert "text-3xl" in classes['title']
        
        # Test Material-UI classes
        classes = frontend_agent._get_app_css_classes("material-ui")
        assert classes['container'] == 'app-container'
        assert classes['title'] == 'app-title'
        
        # Test Bootstrap classes
        classes = frontend_agent._get_bootstrap_css_classes()
        assert "min-vh-100" in classes['container']
        assert "display-4" in classes['title']
    
    def test_get_css_framework_styles(self, frontend_agent):
        """Test CSS framework styles generation"""
        # Test Tailwind styles
        styles = frontend_agent._get_css_framework_styles("tailwind")
        assert "@tailwind base;" in styles
        assert "@tailwind components;" in styles
        assert "@tailwind utilities;" in styles
        
        # Test Material-UI styles
        styles = frontend_agent._get_css_framework_styles("material-ui")
        assert "Roboto" in styles
        assert "#1976d2" in styles
        
        # Test Bootstrap styles
        styles = frontend_agent._get_css_framework_styles("bootstrap")
        assert "bootstrap/dist/css/bootstrap.min.css" in styles
    
    def test_get_redux_store(self, frontend_agent):
        """Test Redux store generation"""
        store_code = frontend_agent._get_redux_store()
        
        assert "configureStore" in store_code
        assert "todoReducer" in store_code
        assert "RootState" in store_code
        assert "AppDispatch" in store_code
    
    def test_get_redux_slice(self, frontend_agent):
        """Test Redux slice generation"""
        slice_code = frontend_agent._get_redux_slice()
        
        assert "createSlice" in slice_code
        assert "addTodo" in slice_code
        assert "toggleTodo" in slice_code
        assert "deleteTodo" in slice_code
        assert "TodoState" in slice_code
    
    def test_get_zustand_store(self, frontend_agent):
        """Test Zustand store generation"""
        store_code = frontend_agent._get_zustand_store()
        
        assert "create" in store_code
        assert "devtools" in store_code
        assert "TodoStore" in store_code
        assert "addTodo:" in store_code
        assert "toggleTodo:" in store_code
    
    def test_get_context_api(self, frontend_agent):
        """Test Context API generation"""
        context_code = frontend_agent._get_context_api()
        
        assert "createContext" in context_code
        assert "useContext" in context_code
        assert "useReducer" in context_code
        assert "AppProvider" in context_code
        assert "useAppContext" in context_code
    
    def test_get_react_app_component(self, frontend_agent):
        """Test React App component generation"""
        # Test with Redux
        app_component = frontend_agent._get_react_app_component("tailwind", "redux")
        assert "Provider" in app_component
        assert "store={store}" in app_component
        
        # Test with Context API
        app_component = frontend_agent._get_react_app_component("tailwind", "context-api")
        assert "AppProvider" in app_component
        
        # Test with Zustand
        app_component = frontend_agent._get_react_app_component("tailwind", "zustand")
        assert "TodoList" in app_component
        assert "AddTodo" in app_component
    
    def test_get_todo_list_component(self, frontend_agent):
        """Test TodoList component generation"""
        # Test with Redux
        component = frontend_agent._get_todo_list_component("tailwind", "redux")
        assert "useSelector" in component
        assert "useDispatch" in component
        assert "RootState" in component
        
        # Test with Zustand
        component = frontend_agent._get_todo_list_component("tailwind", "zustand")
        assert "useStore" in component
        
        # Test with Context API
        component = frontend_agent._get_todo_list_component("tailwind", "context-api")
        assert "useAppContext" in component
    
    def test_get_default_react_files(self, frontend_agent):
        """Test default React files generation"""
        task = {"title": "React Todo App"}
        files = frontend_agent._get_default_react_files(task)
        
        # Check that all required files are present
        required_files = ["package.json", "public/index.html", "src/index.js", "src/App.js", "src/App.css"]
        for file in required_files:
            assert file in files
        
        # Check package.json structure
        package_json = json.loads(files["package.json"])
        assert "react" in package_json["dependencies"]
        assert "react-dom" in package_json["dependencies"]
        assert "react-scripts" in package_json["dependencies"]
        
        # Check that scripts are defined
        assert "start" in package_json["scripts"]
        assert "build" in package_json["scripts"]
        assert "test" in package_json["scripts"]
    
    @pytest.mark.asyncio
    async def test_create_advanced_react_app(self, frontend_agent):
        """Test advanced React app creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Advanced React Dashboard",
                "description": "Create a modern React dashboard with TypeScript",
                "requirements": {
                    "typescript": True,
                    "pwa": True,
                    "state_management": "redux"
                },
                "output_dir": temp_dir
            }
            
            # Mock the LLM client
            with patch('agents.frontend_enhanced.ollama_client') as mock_client:
                mock_client.__aenter__ = AsyncMock(return_value=mock_client)
                mock_client.__aexit__ = AsyncMock(return_value=None)
                mock_client.generate = AsyncMock(return_value={
                    'response': '{"files": {"custom.js": "// Custom file"}}'
                })
                
                result = await frontend_agent._create_advanced_react_app(
                    task, temp_dir, "tailwind", "redux"
                )
                
                assert result["status"] == "completed"
                assert result["technology"] == "React + TypeScript"
                assert result["css_framework"] == "tailwind"
                assert result["state_management"] == "redux"
                assert "PWA" in result["features"]
                assert len(result["files_created"]) > 0
    
    @pytest.mark.asyncio
    async def test_process_task(self, frontend_agent):
        """Test task processing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Create React application",
                "description": "Modern React app with TypeScript and Tailwind",
                "architecture": {"frontend": "react"},
                "requirements": {"typescript": True, "tailwind": True},
                "output_dir": temp_dir
            }
            
            # Mock the LLM client
            with patch('agents.frontend_enhanced.ollama_client') as mock_client:
                mock_client.__aenter__ = AsyncMock(return_value=mock_client)
                mock_client.__aexit__ = AsyncMock(return_value=None)
                mock_client.generate = AsyncMock(return_value={
                    'response': '{"files": {}}'
                })
                
                result = await frontend_agent.process_task(task)
                
                assert result["status"] == "completed"
                assert result["technology"] == "React + TypeScript"
                assert result["css_framework"] == "tailwind"
                assert frontend_agent.status == "idle"
    
    @pytest.mark.asyncio
    async def test_process_task_vue_support(self, frontend_agent):
        """Test Vue.js support placeholder"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Create Vue application",
                "architecture": {"frontend": "vue"},
                "output_dir": temp_dir
            }
            
            result = await frontend_agent.process_task(task)
            
            # Vue support is placeholder for now
            assert result["status"] == "completed"
            assert "Vue.js support will be implemented" in result["message"]
    
    @pytest.mark.asyncio
    async def test_process_task_angular_support(self, frontend_agent):
        """Test Angular support placeholder"""
        with tempfile.TemporaryDirectory() as temp_dir:
            task = {
                "title": "Create Angular application",
                "architecture": {"frontend": "angular"},
                "output_dir": temp_dir
            }
            
            result = await frontend_agent.process_task(task)
            
            # Angular support is placeholder for now
            assert result["status"] == "completed"
            assert "Angular support will be implemented" in result["message"]
    
    @pytest.mark.asyncio
    async def test_process_task_error_handling(self, frontend_agent):
        """Test error handling in task processing"""
        task = {
            "title": "Broken task",
            "output_dir": "/invalid/path/that/does/not/exist"
        }
        
        result = await frontend_agent.process_task(task)
        
        assert result["status"] == "error"
        assert "message" in result
        assert result["files_created"] == []
        assert frontend_agent.status == "error"
    
    def test_component_generation_integration(self, frontend_agent):
        """Test integration of component generation"""
        # Test that all components work together
        app_component = frontend_agent._get_react_app_component("tailwind", "redux")
        todo_list = frontend_agent._get_todo_list_component("tailwind", "redux")
        add_todo = frontend_agent._get_add_todo_component("tailwind", "redux")
        
        # Check that components reference each other correctly
        assert "TodoList" in app_component
        assert "AddTodo" in app_component
        assert "useSelector" in todo_list
        assert "useDispatch" in add_todo
    
    def test_file_structure_completeness(self, frontend_agent):
        """Test that generated file structure is complete"""
        task = {"title": "Complete React App"}
        files = frontend_agent._get_default_react_files(task)
        
        # Essential files
        assert "package.json" in files
        assert "public/index.html" in files
        assert "src/index.js" in files
        assert "src/App.js" in files
        assert "src/App.css" in files
        
        # Check that package.json is valid JSON
        package_data = json.loads(files["package.json"])
        assert isinstance(package_data["dependencies"], dict)
        assert isinstance(package_data["scripts"], dict)
    
    def test_accessibility_features(self, frontend_agent):
        """Test accessibility features in generated components"""
        component = frontend_agent._get_todo_item_component("tailwind")
        
        # Check for ARIA labels
        assert 'aria-label="Toggle todo completion"' in component
        assert 'aria-label="Delete todo"' in component
        
        # Check for semantic HTML
        assert 'type="checkbox"' in component
        assert 'onClick=' in component
    
    def test_responsive_design_features(self, frontend_agent):
        """Test responsive design in CSS classes"""
        classes = frontend_agent._get_app_css_classes("tailwind")
        
        # Check for responsive utility classes
        assert "min-h-screen" in classes['container']
        assert "max-w-2xl" in classes['main']
        
        # Check for mobile-first approach
        styles = frontend_agent._get_css_framework_styles("tailwind")
        assert "@tailwind utilities;" in styles

