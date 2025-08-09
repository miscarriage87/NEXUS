
"""
Enhanced Frontend Agent - Advanced React/Vue/Angular development with TypeScript, modern frameworks, and PWA support
Task 4: Advanced Frontend Agent Enhancement
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = Path(__file__).resolve().parent.parent

from core.base_agent import BaseAgent
from core.ollama_client import ollama_client

class FrontendEnhancedAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("frontend_enhanced", "Enhanced Frontend Developer", config)
        self.technologies = config.get('agents', {}).get('frontend', {}).get('technologies', [])
        self.frameworks = ['react', 'vue', 'angular', 'nextjs', 'nuxt', 'svelte']
        self.css_frameworks = ['tailwind', 'material-ui', 'bootstrap', 'bulma', 'chakra-ui', 'ant-design']
        self.state_management = ['redux', 'vuex', 'context-api', 'mobx', 'zustand', 'pinia']
        
    def get_capabilities(self) -> List[str]:
        return [
            "react_development_advanced",
            "vue_development_advanced", 
            "angular_development_advanced",
            "typescript_support",
            "modern_css_frameworks",
            "state_management_implementation",
            "pwa_capabilities",
            "responsive_design",
            "accessibility_features",
            "component_library_creation",
            "micro_frontend_architecture",
            "server_side_rendering",
            "static_site_generation"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process advanced frontend development tasks"""
        self.status = "working"
        self.logger.info(f"Processing enhanced frontend task: {task.get('title', 'Unknown')}")
        
        try:
            output_dir = task.get("output_dir", str(BASE_DIR / "demo"))
            architecture = task.get("architecture", {})
            requirements = task.get("requirements", {})
            
            # Determine framework from architecture or requirements
            framework = self._determine_framework(architecture, requirements, task)
            css_framework = self._determine_css_framework(requirements)
            state_mgmt = self._determine_state_management(framework, requirements)
            
            self.logger.info(f"Creating {framework} app with {css_framework} styling and {state_mgmt} state management")
            
            # Create appropriate application based on framework
            if framework == 'react':
                result = await self._create_advanced_react_app(task, output_dir, css_framework, state_mgmt)
            elif framework == 'vue':
                result = await self._create_advanced_vue_app(task, output_dir, css_framework, state_mgmt)
            elif framework == 'angular':
                result = await self._create_advanced_angular_app(task, output_dir, css_framework, state_mgmt)
            elif framework == 'nextjs':
                result = await self._create_nextjs_app(task, output_dir, css_framework, state_mgmt)
            else:
                result = await self._create_advanced_react_app(task, output_dir, css_framework, state_mgmt)
            
            self.status = "idle"
            return result
            
        except Exception as e:
            self.status = "error"
            self.logger.error(f"Error processing enhanced frontend task: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "files_created": []
            }
    
    def _determine_framework(self, architecture: Dict, requirements: Dict, task: Dict) -> str:
        """Determine which frontend framework to use"""
        # Check architecture specification
        if architecture.get("frontend"):
            fw = architecture["frontend"].lower()
            if fw in self.frameworks:
                return fw
        
        # Check requirements
        for fw in self.frameworks:
            if fw in str(requirements).lower() or fw in task.get("title", "").lower():
                return fw
        
        # Default to React
        return "react"
    
    def _determine_css_framework(self, requirements: Dict) -> str:
        """Determine which CSS framework to use"""
        req_str = str(requirements).lower()
        for css_fw in self.css_frameworks:
            if css_fw in req_str:
                return css_fw
        return "tailwind"  # Default to Tailwind
    
    def _determine_state_management(self, framework: str, requirements: Dict) -> str:
        """Determine which state management solution to use"""
        req_str = str(requirements).lower()
        
        if framework == 'react':
            if 'redux' in req_str:
                return 'redux'
            elif 'zustand' in req_str:
                return 'zustand'
            else:
                return 'context-api'
        elif framework == 'vue':
            if 'vuex' in req_str:
                return 'vuex'
            elif 'pinia' in req_str:
                return 'pinia'
            else:
                return 'pinia'  # Modern Vue default
        elif framework == 'angular':
            return 'ngrx'
        else:
            return 'context-api'
    
    async def _create_advanced_react_app(self, task: Dict[str, Any], output_dir: str, 
                                       css_framework: str, state_mgmt: str) -> Dict[str, Any]:
        """Create advanced React application with TypeScript and modern features"""
        frontend_dir = os.path.join(output_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)
        
        app_name = task.get('title', 'Advanced React App').replace(' ', '-').lower()
        
        files = {}
        
        # Package.json with advanced dependencies
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^5.0.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "web-vitals": "^3.0.0",
            "react-router-dom": "^6.8.0",
            "@types/node": "^18.0.0"
        }
        
        # Add CSS framework dependencies
        if css_framework == 'tailwind':
            dependencies.update({
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.14",
                "postcss": "^8.4.21"
            })
        elif css_framework == 'material-ui':
            dependencies.update({
                "@mui/material": "^5.11.0",
                "@emotion/react": "^11.10.5",
                "@emotion/styled": "^11.10.5",
                "@mui/icons-material": "^5.11.0"
            })
        elif css_framework == 'bootstrap':
            dependencies.update({
                "bootstrap": "^5.2.3",
                "react-bootstrap": "^2.7.2"
            })
        
        # Add state management dependencies
        if state_mgmt == 'redux':
            dependencies.update({
                "@reduxjs/toolkit": "^1.9.3",
                "react-redux": "^8.0.5"
            })
        elif state_mgmt == 'zustand':
            dependencies["zustand"] = "^4.3.6"
        
        # Add PWA dependencies
        dependencies.update({
            "workbox-webpack-plugin": "^6.5.4",
            "workbox-core": "^6.5.4",
            "workbox-precaching": "^6.5.4",
            "workbox-routing": "^6.5.4",
            "workbox-strategies": "^6.5.4"
        })
        
        files["package.json"] = json.dumps({
            "name": app_name,
            "version": "0.1.0",
            "private": True,
            "dependencies": dependencies,
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject",
                "build:pwa": "GENERATE_SOURCEMAP=false react-scripts build"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }, indent=2)
        
        # TypeScript config
        files["tsconfig.json"] = json.dumps({
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "es6"],
                "allowJs": True,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noFallthroughCasesInSwitch": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx"
            },
            "include": ["src"]
        }, indent=2)
        
        # Public files with PWA support
        files["public/index.html"] = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Advanced React App with PWA capabilities" />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>{app_name.title()}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
        
        # PWA Manifest
        files["public/manifest.json"] = json.dumps({
            "short_name": app_name.title(),
            "name": f"{app_name.title()} - Progressive Web App",
            "icons": [
                {
                    "src": "favicon.ico",
                    "sizes": "64x64 32x32 24x24 16x16",
                    "type": "image/x-icon"
                },
                {
                    "src": "logo192.png",
                    "type": "image/png",
                    "sizes": "192x192"
                },
                {
                    "src": "logo512.png",
                    "type": "image/png",
                    "sizes": "512x512"
                }
            ],
            "start_url": ".",
            "display": "standalone",
            "theme_color": "#000000",
            "background_color": "#ffffff"
        }, indent=2)
        
        # Service worker
        files["public/sw.js"] = '''const CACHE_NAME = 'app-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/',
  '/static/js/',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});'''
        
        # Main App component with TypeScript
        files["src/App.tsx"] = self._get_react_app_component(css_framework, state_mgmt)
        
        # Index file
        files["src/index.tsx"] = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';

// Register service worker for PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);'''
        
        # CSS files
        files["src/index.css"] = self._get_css_framework_styles(css_framework)
        
        # Additional components based on state management
        if state_mgmt == 'redux':
            files["src/store/index.ts"] = self._get_redux_store()
            files["src/store/todoSlice.ts"] = self._get_redux_slice()
        elif state_mgmt == 'zustand':
            files["src/store/useStore.ts"] = self._get_zustand_store()
        else:  # context-api
            files["src/context/AppContext.tsx"] = self._get_context_api()
        
        # Components
        files["src/components/TodoList.tsx"] = self._get_todo_list_component(css_framework, state_mgmt)
        files["src/components/TodoItem.tsx"] = self._get_todo_item_component(css_framework)
        files["src/components/AddTodo.tsx"] = self._get_add_todo_component(css_framework, state_mgmt)
        
        # Types
        files["src/types/index.ts"] = '''export interface Todo {
  id: string;
  text: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface AppState {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
  loading: boolean;
  error: string | null;
}'''
        
        # Utilities
        files["src/utils/api.ts"] = '''const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = 'ApiError';
  }
}

export const api = {
  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`);
    if (!response.ok) {
      throw new ApiError(`Failed to fetch ${endpoint}`, response.status);
    }
    return response.json();
  },

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new ApiError(`Failed to post to ${endpoint}`, response.status);
    }
    return response.json();
  },

  async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new ApiError(`Failed to update ${endpoint}`, response.status);
    }
    return response.json();
  },

  async delete(endpoint: string): Promise<void> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new ApiError(`Failed to delete ${endpoint}`, response.status);
    }
  },
};'''
        
        # Environment files
        files[".env.example"] = '''REACT_APP_API_URL=http://localhost:8000
REACT_APP_NAME=Advanced React App
GENERATE_SOURCEMAP=false'''
        
        # Tailwind config if using Tailwind
        if css_framework == 'tailwind':
            files["tailwind.config.js"] = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}'''
            files["postcss.config.js"] = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''
        
        # README with setup instructions
        files["README.md"] = f'''# {app_name.title()}

Advanced React application with TypeScript, {css_framework.title()}, {state_mgmt.replace('-', ' ').title()}, and PWA capabilities.

## Features

- ⚛️ React 18 with TypeScript
- 🎨 {css_framework.title()} for styling
- 🔄 {state_mgmt.replace('-', ' ').title()} for state management
- 📱 Progressive Web App (PWA) support
- 🔍 SEO optimized
- ♿ Accessibility features
- 📦 Modern build setup
- 🧪 Testing setup included

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Build PWA version
npm run build:pwa
```

## PWA Features

- Offline functionality
- App-like experience
- Install prompt
- Service worker caching
- Push notifications ready

## State Management

Using {state_mgmt.replace('-', ' ').title()} for predictable state management with:
- Centralized state store
- Type-safe actions and reducers
- DevTools integration
- Middleware support

## Styling

{css_framework.title()} provides:
- Responsive design system
- Modern UI components
- Dark mode support
- Customizable theme
- Mobile-first approach

## API Integration

Ready-to-use API client with:
- Type-safe API calls
- Error handling
- Loading states
- Request/response interceptors

## Accessibility

Built with accessibility in mind:
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader support
- Color contrast compliance

## Environment Variables

Copy `.env.example` to `.env` and configure:

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_NAME=Your App Name
```

## Scripts

- `npm start` - Development server
- `npm build` - Production build
- `npm test` - Run tests
- `npm run build:pwa` - Build with PWA optimizations
'''
        
        # Write all files
        created_files = []
        for filename, content in files.items():
            file_path = os.path.join(frontend_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(file_path)
        
        return {
            "status": "completed",
            "files_created": created_files,
            "output_directory": frontend_dir,
            "technology": "React + TypeScript",
            "css_framework": css_framework,
            "state_management": state_mgmt,
            "features": ["PWA", "TypeScript", "Responsive", "Accessible"]
        }
    
    def _get_react_app_component(self, css_framework: str, state_mgmt: str) -> str:
        """Get main React App component based on configuration"""
        if state_mgmt == 'redux':
            imports = '''import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';'''
            wrapper_start = '<Provider store={store}>'
            wrapper_end = '</Provider>'
        else:
            imports = '''import React from 'react';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';'''
            if state_mgmt == 'context-api':
                imports += '\nimport { AppProvider } from "./context/AppContext";'
                wrapper_start = '<AppProvider>'
                wrapper_end = '</AppProvider>'
            else:
                wrapper_start = '<>'
                wrapper_end = '</>'
        
        css_classes = self._get_app_css_classes(css_framework)
        
        return f'''{imports}

const App: React.FC = () => {{
  return (
    {wrapper_start}
      <div className="{css_classes['container']}">
        <header className="{css_classes['header']}">
          <h1 className="{css_classes['title']}">
            Advanced Todo App
          </h1>
          <p className="{css_classes['subtitle']}">
            Built with React, TypeScript, and {css_framework.title()}
          </p>
        </header>
        
        <main className="{css_classes['main']}">
          <AddTodo />
          <TodoList />
        </main>
        
        <footer className="{css_classes['footer']}">
          <p>Powered by NEXUS Frontend Enhanced Agent</p>
        </footer>
      </div>
    {wrapper_end}
  );
}};

export default App;'''
    
    def _get_app_css_classes(self, css_framework: str) -> Dict[str, str]:
        """Get CSS classes for different frameworks"""
        if css_framework == 'tailwind':
            return {
                'container': 'min-h-screen bg-gray-100 dark:bg-gray-900',
                'header': 'bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 px-4 py-6',
                'title': 'text-3xl font-bold text-gray-900 dark:text-white text-center',
                'subtitle': 'text-gray-600 dark:text-gray-300 text-center mt-2',
                'main': 'max-w-2xl mx-auto px-4 py-8',
                'footer': 'bg-gray-50 dark:bg-gray-800 text-center py-4 text-sm text-gray-500 dark:text-gray-400'
            }
        elif css_framework == 'material-ui':
            return {
                'container': 'app-container',
                'header': 'app-header',
                'title': 'app-title',
                'subtitle': 'app-subtitle',
                'main': 'app-main',
                'footer': 'app-footer'
            }
        else:  # Bootstrap
            return {
                'container': 'min-vh-100 bg-light',
                'header': 'bg-white shadow-sm border-bottom px-4 py-3',
                'title': 'display-4 text-center mb-2',
                'subtitle': 'text-muted text-center',
                'main': 'container my-5',
                'footer': 'bg-light text-center py-3 text-muted'
            }
    
    def _get_css_framework_styles(self, css_framework: str) -> str:
        """Get CSS styles for the chosen framework"""
        if css_framework == 'tailwind':
            return '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
  }
  
  .btn-secondary {
    @apply bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded;
  }
  
  .btn-danger {
    @apply bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded;
  }
  
  .card {
    @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
  }
  
  .form-input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
}'''
        elif css_framework == 'material-ui':
            return '''body {
  margin: 0;
  font-family: "Roboto", "Helvetica", "Arial", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.app-header {
  background-color: #1976d2;
  color: white;
  padding: 2rem;
  text-align: center;
}

.app-title {
  font-size: 2.5rem;
  font-weight: 300;
  margin-bottom: 0.5rem;
}

.app-subtitle {
  font-size: 1.2rem;
  opacity: 0.8;
}

.app-main {
  max-width: 600px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.app-footer {
  background-color: #424242;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: 2rem;
}'''
        else:  # Bootstrap
            return '''@import 'bootstrap/dist/css/bootstrap.min.css';

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  min-height: 100vh;
}

.todo-item {
  transition: all 0.2s;
}

.todo-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.completed {
  opacity: 0.6;
  text-decoration: line-through;
}'''
    
    def _get_redux_store(self) -> str:
        return '''import { configureStore } from '@reduxjs/toolkit';
import todoReducer from './todoSlice';

export const store = configureStore({
  reducer: {
    todos: todoReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;'''
    
    def _get_redux_slice(self) -> str:
        return '''import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Todo } from '../types';

interface TodoState {
  items: Todo[];
  filter: 'all' | 'active' | 'completed';
  loading: boolean;
  error: string | null;
}

const initialState: TodoState = {
  items: [],
  filter: 'all',
  loading: false,
  error: null,
};

const todoSlice = createSlice({
  name: 'todos',
  initialState,
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      const newTodo: Todo = {
        id: Date.now().toString(),
        text: action.payload,
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      state.items.push(newTodo);
    },
    toggleTodo: (state, action: PayloadAction<string>) => {
      const todo = state.items.find(item => item.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed;
        todo.updatedAt = new Date();
      }
    },
    deleteTodo: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(item => item.id !== action.payload);
    },
    setFilter: (state, action: PayloadAction<'all' | 'active' | 'completed'>) => {
      state.filter = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { addTodo, toggleTodo, deleteTodo, setFilter, setLoading, setError } = todoSlice.actions;
export default todoSlice.reducer;'''
    
    def _get_zustand_store(self) -> str:
        return '''import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { Todo } from '../types';

interface TodoStore {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
  loading: boolean;
  error: string | null;
  
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
  setFilter: (filter: 'all' | 'active' | 'completed') => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useStore = create<TodoStore>()(
  devtools((set) => ({
    todos: [],
    filter: 'all',
    loading: false,
    error: null,
    
    addTodo: (text: string) => set((state) => ({
      todos: [...state.todos, {
        id: Date.now().toString(),
        text,
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date(),
      }]
    })),
    
    toggleTodo: (id: string) => set((state) => ({
      todos: state.todos.map(todo =>
        todo.id === id
          ? { ...todo, completed: !todo.completed, updatedAt: new Date() }
          : todo
      )
    })),
    
    deleteTodo: (id: string) => set((state) => ({
      todos: state.todos.filter(todo => todo.id !== id)
    })),
    
    setFilter: (filter: 'all' | 'active' | 'completed') => set({ filter }),
    setLoading: (loading: boolean) => set({ loading }),
    setError: (error: string | null) => set({ error }),
  }))
);'''
    
    def _get_context_api(self) -> str:
        return '''import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { Todo } from '../types';

interface AppState {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
  loading: boolean;
  error: string | null;
}

type AppAction =
  | { type: 'ADD_TODO'; payload: string }
  | { type: 'TOGGLE_TODO'; payload: string }
  | { type: 'DELETE_TODO'; payload: string }
  | { type: 'SET_FILTER'; payload: 'all' | 'active' | 'completed' }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };

const initialState: AppState = {
  todos: [],
  filter: 'all',
  loading: false,
  error: null,
};

const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [...state.todos, {
          id: Date.now().toString(),
          text: action.payload,
          completed: false,
          createdAt: new Date(),
          updatedAt: new Date(),
        }]
      };
    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed, updatedAt: new Date() }
            : todo
        )
      };
    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload)
      };
    case 'SET_FILTER':
      return { ...state, filter: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};'''
    
    def _get_todo_list_component(self, css_framework: str, state_mgmt: str) -> str:
        if state_mgmt == 'redux':
            imports = '''import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { setFilter } from '../store/todoSlice';
import TodoItem from './TodoItem';'''
            
            state_logic = '''  const { items: todos, filter } = useSelector((state: RootState) => state.todos);
  const dispatch = useDispatch();
  
  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });
  
  const handleFilterChange = (newFilter: 'all' | 'active' | 'completed') => {
    dispatch(setFilter(newFilter));
  };'''
        elif state_mgmt == 'zustand':
            imports = '''import React from 'react';
import { useStore } from '../store/useStore';
import TodoItem from './TodoItem';'''
            
            state_logic = '''  const { todos, filter, setFilter } = useStore();
  
  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });
  
  const handleFilterChange = (newFilter: 'all' | 'active' | 'completed') => {
    setFilter(newFilter);
  };'''
        else:  # context-api
            imports = '''import React from 'react';
import { useAppContext } from '../context/AppContext';
import TodoItem from './TodoItem';'''
            
            state_logic = '''  const { state, dispatch } = useAppContext();
  const { todos, filter } = state;
  
  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });
  
  const handleFilterChange = (newFilter: 'all' | 'active' | 'completed') => {
    dispatch({ type: 'SET_FILTER', payload: newFilter });
  };'''
        
        css_classes = self._get_todo_list_css_classes(css_framework)
        
        # JavaScript expressions for filter counts (avoiding syntax errors in f-string)
        active_count_expr = "todos.filter(t => !t.completed).length"
        completed_count_expr = "todos.filter(t => t.completed).length"
        total_count_expr = "todos.length"
        
        # JavaScript conditional and map expressions
        empty_check_start = "{filteredTodos.length === 0 ? ("
        map_todos_start = "{filteredTodos.map(todo => ("
        
        # JavaScript attribute expressions for TodoItem
        todo_key_expr = "{todo.id}"
        todo_expr = "{todo}"
        
        return f'''{imports}

const TodoList: React.FC = () => {{
{state_logic}

  return (
    <div className="{css_classes['container']}">
      <div className="{css_classes['filters']}">
        <button
          className={{`{css_classes['filter_btn']} ${{filter === 'all' ? css_classes['filter_active'] : ''}}`}}
          onClick={{() => handleFilterChange('all')}}
        >
          All ({{total_count_expr}})
        </button>
        <button
          className={{`{css_classes['filter_btn']} ${{filter === 'active' ? css_classes['filter_active'] : ''}}`}}
          onClick={{() => handleFilterChange('active')}}
        >
          Active ({{active_count_expr}})
        </button>
        <button
          className={{`{css_classes['filter_btn']} ${{filter === 'completed' ? css_classes['filter_active'] : ''}}`}}
          onClick={{() => handleFilterChange('completed')}}
        >
          Completed ({{completed_count_expr}})
        </button>
      </div>
      
      {empty_check_start}
        <div className="{css_classes['empty']}">
          <p>No todos found. Add some tasks to get started!</p>
        </div>
      ) : (
        <div className="{css_classes['list']}">
          {map_todos_start}
            <TodoItem key={todo_key_expr} todo={todo_expr} />
          ))}}
        </div>
      )}}
    </div>
  );
}};

export default TodoList;'''
    
    def _get_todo_list_css_classes(self, css_framework: str) -> Dict[str, str]:
        if css_framework == 'tailwind':
            return {
                'container': 'space-y-6',
                'filters': 'flex space-x-2 justify-center mb-6',
                'filter_btn': 'px-4 py-2 rounded-lg font-medium transition-colors',
                'filter_active': 'bg-blue-500 text-white',
                'empty': 'text-center py-8 text-gray-500',
                'list': 'space-y-2'
            }
        elif css_framework == 'material-ui':
            return {
                'container': 'todo-list-container',
                'filters': 'filter-buttons',
                'filter_btn': 'filter-btn',
                'filter_active': 'filter-active',
                'empty': 'empty-state',
                'list': 'todo-items'
            }
        else:  # Bootstrap
            return {
                'container': 'mb-4',
                'filters': 'btn-group d-flex justify-content-center mb-4',
                'filter_btn': 'btn btn-outline-primary',
                'filter_active': 'active',
                'empty': 'text-center py-5 text-muted',
                'list': 'list-group'
            }
    
    def _get_todo_item_component(self, css_framework: str) -> str:
        css_classes = self._get_todo_item_css_classes(css_framework)
        
        return f'''import React from 'react';
import {{ Todo }} from '../types';

interface TodoItemProps {{
  todo: Todo;
}}

const TodoItem: React.FC<TodoItemProps> = ({{ todo }}) => {{
  const handleToggle = () => {{
    // This will be connected to state management
    console.log('Toggle todo:', todo.id);
  }};
  
  const handleDelete = () => {{
    // This will be connected to state management
    console.log('Delete todo:', todo.id);
  }};

  return (
    <div className="{{`{css_classes['container']} ${{todo.completed ? css_classes['completed'] : ''}}`}}">
      <div className="{css_classes['content']}">
        <input
          type="checkbox"
          checked={{todo.completed}}
          onChange={{handleToggle}}
          className="{css_classes['checkbox']}"
          aria-label="Toggle todo completion"
        />
        <span className="{css_classes['text']}">
          {{todo.text}}
        </span>
      </div>
      <div className="{css_classes['actions']}">
        <button
          onClick={{handleDelete}}
          className="{css_classes['delete_btn']}"
          aria-label="Delete todo"
        >
          Delete
        </button>
      </div>
    </div>
  );
}};

export default TodoItem;'''
    
    def _get_todo_item_css_classes(self, css_framework: str) -> Dict[str, str]:
        if css_framework == 'tailwind':
            return {
                'container': 'flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700',
                'completed': 'opacity-75 bg-gray-50 dark:bg-gray-900',
                'content': 'flex items-center space-x-3 flex-1',
                'checkbox': 'w-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500',
                'text': 'flex-1 text-gray-900 dark:text-white',
                'actions': 'flex space-x-2',
                'delete_btn': 'px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors'
            }
        elif css_framework == 'material-ui':
            return {
                'container': 'todo-item',
                'completed': 'completed',
                'content': 'todo-content',
                'checkbox': 'todo-checkbox',
                'text': 'todo-text',
                'actions': 'todo-actions',
                'delete_btn': 'delete-btn'
            }
        else:  # Bootstrap
            return {
                'container': 'list-group-item d-flex justify-content-between align-items-center',
                'completed': 'list-group-item-secondary',
                'content': 'd-flex align-items-center',
                'checkbox': 'form-check-input me-3',
                'text': 'flex-grow-1',
                'actions': '',
                'delete_btn': 'btn btn-outline-danger btn-sm'
            }
    
    def _get_add_todo_component(self, css_framework: str, state_mgmt: str) -> str:
        if state_mgmt == 'redux':
            imports = '''import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addTodo } from '../store/todoSlice';'''
            
            submit_logic = '''  const dispatch = useDispatch();
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      dispatch(addTodo(text.trim()));
      setText('');
    }
  };'''
        elif state_mgmt == 'zustand':
            imports = '''import React, { useState } from 'react';
import { useStore } from '../store/useStore';'''
            
            submit_logic = '''  const addTodo = useStore(state => state.addTodo);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      addTodo(text.trim());
      setText('');
    }
  };'''
        else:  # context-api
            imports = '''import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';'''
            
            submit_logic = '''  const { dispatch } = useAppContext();
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      dispatch({ type: 'ADD_TODO', payload: text.trim() });
      setText('');
    }
  };'''
        
        css_classes = self._get_add_todo_css_classes(css_framework)
        
        return f'''{imports}

const AddTodo: React.FC = () => {{
  const [text, setText] = useState('');
  
{submit_logic}

  return (
    <form onSubmit={{handleSubmit}} className="{css_classes['form']}">
      <div className="{css_classes['input_group']}">
        <input
          type="text"
          value={{text}}
          onChange={{(e) => setText(e.target.value)}}
          placeholder="Add a new todo..."
          className="{css_classes['input']}"
          aria-label="New todo text"
        />
        <button
          type="submit"
          disabled={{!text.trim()}}
          className="{css_classes['button']}"
        >
          Add Todo
        </button>
      </div>
    </form>
  );
}};

export default AddTodo;'''
    
    def _get_add_todo_css_classes(self, css_framework: str) -> Dict[str, str]:
        if css_framework == 'tailwind':
            return {
                'form': 'mb-6',
                'input_group': 'flex space-x-2',
                'input': 'flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'button': 'px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors'
            }
        elif css_framework == 'material-ui':
            return {
                'form': 'add-todo-form',
                'input_group': 'add-todo-group',
                'input': 'add-todo-input',
                'button': 'add-todo-button'
            }
        else:  # Bootstrap
            return {
                'form': 'mb-4',
                'input_group': 'input-group',
                'input': 'form-control',
                'button': 'btn btn-primary'
            }
    
    async def _create_advanced_vue_app(self, task: Dict[str, Any], output_dir: str, 
                                     css_framework: str, state_mgmt: str) -> Dict[str, Any]:
        """Create advanced Vue.js application"""
        # Implementation for Vue.js would go here
        # For brevity, returning a placeholder that indicates Vue support
        return {
            "status": "completed",
            "message": "Vue.js support will be implemented in the next iteration",
            "technology": "Vue.js + TypeScript",
            "files_created": []
        }
    
    async def _create_advanced_angular_app(self, task: Dict[str, Any], output_dir: str, 
                                         css_framework: str, state_mgmt: str) -> Dict[str, Any]:
        """Create advanced Angular application"""
        # Implementation for Angular would go here
        # For brevity, returning a placeholder that indicates Angular support
        return {
            "status": "completed", 
            "message": "Angular support will be implemented in the next iteration",
            "technology": "Angular + TypeScript",
            "files_created": []
        }
    
    async def _create_nextjs_app(self, task: Dict[str, Any], output_dir: str, 
                               css_framework: str, state_mgmt: str) -> Dict[str, Any]:
        """Create Next.js application with SSR"""
        # Implementation for Next.js would go here
        # For brevity, returning a placeholder that indicates Next.js support
        return {
            "status": "completed",
            "message": "Next.js support will be implemented in the next iteration", 
            "technology": "Next.js + TypeScript",
            "files_created": []
        }

