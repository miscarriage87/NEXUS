
"""
Context Cache - LRU cache with memory tracking for context management
"""

import hashlib
import sys
from collections import OrderedDict
from typing import Dict, Any, Optional, Tuple
import logging


class ContextCache:
    """
    LRU cache with memory tracking for context chunks
    """
    
    def __init__(self, maxsize: int = 1000, max_memory_mb: int = 512):
        self.maxsize = maxsize
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache = OrderedDict()
        self.current_memory_usage = 0
        self.logger = logging.getLogger("nexus.context.cache")
        
        self.logger.info(f"Context Cache initialized: maxsize={maxsize}, max_memory={max_memory_mb}MB")
    
    def _get_memory_size(self, obj: Any) -> int:
        """
        Get memory size of an object
        TODO: Implement accurate memory size calculation
        """
        # TODO: Implement more accurate memory calculation
        return sys.getsizeof(obj)
    
    def _generate_key(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """
        Generate cache key from content and metadata
        """
        hasher = hashlib.md5()
        hasher.update(content.encode('utf-8'))
        if metadata:
            hasher.update(str(sorted(metadata.items())).encode('utf-8'))
        return hasher.hexdigest()
    
    def get(self, content: str, metadata: Dict[str, Any] = None) -> Optional[Any]:
        """
        Get item from cache
        """
        key = self._generate_key(content, metadata)
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.logger.debug(f"Cache hit for key: {key[:8]}...")
            return self.cache[key]
        
        self.logger.debug(f"Cache miss for key: {key[:8]}...")
        return None
    
    def put(self, content: str, value: Any, metadata: Dict[str, Any] = None) -> None:
        """
        Put item in cache with memory management
        """
        key = self._generate_key(content, metadata)
        value_size = self._get_memory_size(value)
        
        # Remove item if it already exists
        if key in self.cache:
            old_value = self.cache[key]
            old_size = self._get_memory_size(old_value)
            self.current_memory_usage -= old_size
            del self.cache[key]
        
        # Evict items if necessary
        while (len(self.cache) >= self.maxsize or 
               self.current_memory_usage + value_size > self.max_memory_bytes):
            if not self.cache:
                break
            self._evict_lru()
        
        # Add new item
        self.cache[key] = value
        self.current_memory_usage += value_size
        self.logger.debug(f"Cache put for key: {key[:8]}..., size: {value_size} bytes")
    
    def _evict_lru(self) -> None:
        """
        Evict least recently used item
        """
        if self.cache:
            key, value = self.cache.popitem(last=False)  # Remove first item (LRU)
            value_size = self._get_memory_size(value)
            self.current_memory_usage -= value_size
            self.logger.debug(f"Evicted LRU item: {key[:8]}..., freed: {value_size} bytes")
    
    def clear(self) -> None:
        """
        Clear all cached items
        """
        self.cache.clear()
        self.current_memory_usage = 0
        self.logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        """
        return {
            'size': len(self.cache),
            'maxsize': self.maxsize,
            'memory_usage_bytes': self.current_memory_usage,
            'max_memory_bytes': self.max_memory_bytes,
            'memory_usage_percentage': (self.current_memory_usage / self.max_memory_bytes) * 100
        }
    
    def __len__(self) -> int:
        return len(self.cache)
