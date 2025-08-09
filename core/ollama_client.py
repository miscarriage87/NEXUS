
"""
Ollama Client für LLM-Integration
"""
import json
import aiohttp
import asyncio
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = None
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            config_path = Path(__file__).resolve().parent.parent / 'nexus_config.yaml'
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception:
            return {}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def generate(self, model: str, prompt: str, system: str = None, 
                      stream: bool = False) -> Dict[str, Any]:
        """Generate response from Ollama model"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        if system:
            payload["system"] = system
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.config.get('ollama', {}).get('timeout', 30))
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to connect to Ollama: {str(e)}")
    
    async def chat(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Chat with Ollama model using conversation format"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.config.get('ollama', {}).get('timeout', 30))
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to connect to Ollama: {str(e)}")
    
    async def list_models(self) -> List[str]:
        """List available models"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    result = await response.json()
                    return [model["name"] for model in result.get("models", [])]
                else:
                    return []
        except Exception:
            return []
    
    async def check_health(self) -> bool:
        """Check if Ollama is running"""
        try:
            models = await self.list_models()
            return len(models) >= 0
        except Exception:
            return False

# Singleton instance
ollama_client = OllamaClient()
