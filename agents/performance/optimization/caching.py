
"""
Intelligent Cache - Advanced LLM response caching with semantic similarity
"""

import hashlib
import json
import time
from collections import OrderedDict
from typing import Dict, Any, Optional, List, Tuple
import logging
from datetime import datetime, timedelta


class IntelligentCache:
    """
    Intelligent caching system for LLM responses with semantic similarity matching
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.cache")
        
        # Configuration
        self.max_size = self.config.get('max_size', 1000)
        self.ttl_seconds = self.config.get('ttl_seconds', 3600)  # 1 hour default
        self.similarity_threshold = self.config.get('similarity_threshold', 0.85)
        self.enable_semantic_matching = self.config.get('enable_semantic_matching', True)
        
        # Cache storage
        self.cache = OrderedDict()  # LRU cache
        self.metadata = {}  # Cache metadata
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'semantic_matches': 0
        }
        
        self.logger.info(f"Intelligent Cache initialized: max_size={self.max_size}, ttl={self.ttl_seconds}s")
    
    def _generate_key(self, model: str, prompt: str, system: Optional[str] = None, 
                     context: Dict[str, Any] = None) -> str:
        """
        Generate cache key from request parameters
        """
        key_data = {
            'model': model,
            'prompt': prompt,
            'system': system or '',
            'context': context or {}
        }
        
        # Create deterministic hash
        key_string = json.dumps(key_data, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(key_string.encode('utf-8')).hexdigest()
    
    def _is_expired(self, key: str) -> bool:
        """
        Check if cache entry is expired
        """
        if key not in self.metadata:
            return True
        
        created_time = self.metadata[key].get('created_time', 0)
        return time.time() - created_time > self.ttl_seconds
    
    def get(self, model: str, prompt: str, system: Optional[str] = None,
            context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Get cached response if available
        """
        key = self._generate_key(model, prompt, system, context)
        
        # Direct cache hit
        if key in self.cache and not self._is_expired(key):
            self.cache.move_to_end(key)  # Update LRU order
            self.stats['hits'] += 1
            self.logger.debug(f"Cache hit for key: {key[:8]}...")
            return self.cache[key]
        
        # Remove expired entry
        if key in self.cache:
            self._remove_entry(key)
        
        # Try semantic similarity matching if enabled
        if self.enable_semantic_matching:
            similar_response = self._find_similar_cached_response(prompt, model)
            if similar_response:
                self.stats['semantic_matches'] += 1
                self.logger.debug(f"Semantic cache hit for prompt: {prompt[:50]}...")
                return similar_response
        
        self.stats['misses'] += 1
        self.logger.debug(f"Cache miss for key: {key[:8]}...")
        return None
    
    def put(self, model: str, prompt: str, response: Dict[str, Any],
            system: Optional[str] = None, context: Dict[str, Any] = None) -> None:
        """
        Cache LLM response
        """
        key = self._generate_key(model, prompt, system, context)
        
        # Remove existing entry if present
        if key in self.cache:
            self._remove_entry(key)
        
        # Evict entries if cache is full
        while len(self.cache) >= self.max_size:
            self._evict_lru()
        
        # Add new entry
        self.cache[key] = response
        self.metadata[key] = {
            'created_time': time.time(),
            'model': model,
            'prompt': prompt,
            'system': system,
            'context': context or {},
            'access_count': 0,
            'last_access': time.time()
        }
        
        self.logger.debug(f"Cached response for key: {key[:8]}...")
    
    def _remove_entry(self, key: str) -> None:
        """
        Remove cache entry and its metadata
        """
        if key in self.cache:
            del self.cache[key]
        if key in self.metadata:
            del self.metadata[key]
    
    def _evict_lru(self) -> None:
        """
        Evict least recently used entry
        """
        if self.cache:
            lru_key = next(iter(self.cache))  # First item in OrderedDict is LRU
            self._remove_entry(lru_key)
            self.stats['evictions'] += 1
            self.logger.debug(f"Evicted LRU entry: {lru_key[:8]}...")
    
    def _find_similar_cached_response(self, prompt: str, model: str) -> Optional[Dict[str, Any]]:
        """
        Find semantically similar cached response
        TODO: Implement semantic similarity matching
        """
        if not self.enable_semantic_matching:
            return None
        
        # TODO: Implement semantic similarity using embeddings or NLP techniques
        # For now, use simple string similarity as a placeholder
        
        best_match_key = None
        best_similarity = 0.0
        
        for key, metadata in self.metadata.items():
            if metadata['model'] != model:
                continue
                
            if self._is_expired(key):
                continue
            
            # Simple similarity check (placeholder)
            similarity = self._calculate_string_similarity(prompt, metadata['prompt'])
            
            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match_key = key
        
        if best_match_key:
            # Update access metadata
            self.metadata[best_match_key]['access_count'] += 1
            self.metadata[best_match_key]['last_access'] = time.time()
            
            # Move to end for LRU
            self.cache.move_to_end(best_match_key)
            
            return self.cache[best_match_key]
        
        return None
    
    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate simple string similarity
        TODO: Replace with more sophisticated similarity calculation
        """
        # Simple Jaccard similarity on words
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries
        """
        expired_keys = []
        
        for key in list(self.cache.keys()):
            if self._is_expired(key):
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_entry(key)
        
        if expired_keys:
            self.logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)
    
    def clear(self) -> None:
        """
        Clear all cache entries
        """
        self.cache.clear()
        self.metadata.clear()
        self.logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        """
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate_percent': round(hit_rate, 2),
            'evictions': self.stats['evictions'],
            'semantic_matches': self.stats['semantic_matches'],
            'ttl_seconds': self.ttl_seconds
        }
    
    def get_cache_info(self) -> List[Dict[str, Any]]:
        """
        Get information about cached entries
        """
        cache_info = []
        
        for key, metadata in self.metadata.items():
            entry_info = {
                'key': key[:16] + '...',  # Truncated key for readability
                'model': metadata['model'],
                'prompt_preview': metadata['prompt'][:100] + '...' if len(metadata['prompt']) > 100 else metadata['prompt'],
                'created_time': datetime.fromtimestamp(metadata['created_time']).isoformat(),
                'access_count': metadata['access_count'],
                'last_access': datetime.fromtimestamp(metadata['last_access']).isoformat(),
                'expired': self._is_expired(key)
            }
            cache_info.append(entry_info)
        
        return cache_info
    
    def reset_stats(self) -> None:
        """
        Reset cache statistics
        """
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'semantic_matches': 0
        }
        self.logger.info("Cache statistics reset")
