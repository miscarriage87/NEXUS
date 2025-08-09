
"""
Memory Quota Manager - Memory usage tracking and enforcement
"""

import psutil
from typing import Dict, Any, Union
import logging


class MemoryQuotaManager:
    """
    Memory quota management for context operations
    """
    
    def __init__(self, quota: Union[str, int] = '2GB'):
        self.logger = logging.getLogger("nexus.context.memory_quota")
        
        # Parse quota specification
        self.quota_bytes = self._parse_quota(quota)
        self.current_usage = 0
        self.process = psutil.Process()
        
        self.logger.info(f"Memory Quota Manager initialized: quota={quota}")
    
    def _parse_quota(self, quota: Union[str, int]) -> int:
        """
        Parse quota specification into bytes
        """
        if isinstance(quota, int):
            return quota
        
        quota_str = quota.upper()
        if quota_str.endswith('GB'):
            return int(float(quota_str[:-2]) * 1024 * 1024 * 1024)
        elif quota_str.endswith('MB'):
            return int(float(quota_str[:-2]) * 1024 * 1024)
        elif quota_str.endswith('KB'):
            return int(float(quota_str[:-2]) * 1024)
        elif quota_str.endswith('B'):
            return int(quota_str[:-1])
        else:
            # Assume bytes
            return int(quota_str)
    
    def check_quota(self, additional_bytes: int = 0) -> bool:
        """
        Check if adding additional bytes would exceed quota
        """
        current_memory = self._get_current_memory_usage()
        projected_usage = current_memory + additional_bytes
        
        return projected_usage <= self.quota_bytes
    
    def _get_current_memory_usage(self) -> int:
        """
        Get current memory usage of the process
        """
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss  # Resident Set Size
        except Exception as e:
            self.logger.warning(f"Failed to get memory usage: {e}")
            return 0
    
    def get_available_memory(self) -> int:
        """
        Get available memory within quota
        """
        current_memory = self._get_current_memory_usage()
        return max(0, self.quota_bytes - current_memory)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get detailed memory statistics
        """
        current_memory = self._get_current_memory_usage()
        available_memory = self.get_available_memory()
        usage_percentage = (current_memory / self.quota_bytes) * 100
        
        return {
            'quota_bytes': self.quota_bytes,
            'current_usage_bytes': current_memory,
            'available_bytes': available_memory,
            'usage_percentage': usage_percentage,
            'quota_exceeded': current_memory > self.quota_bytes
        }
    
    def enforce_quota(self, required_bytes: int = 0) -> bool:
        """
        Enforce memory quota, return True if operation can proceed
        TODO: Implement quota enforcement with cleanup
        """
        if self.check_quota(required_bytes):
            return True
        
        self.logger.warning(f"Memory quota would be exceeded. Required: {required_bytes}, Available: {self.get_available_memory()}")
        
        # TODO: Implement cleanup strategies
        # - Clear caches
        # - Release unused resources
        # - Trigger garbage collection
        
        return False
    
    def format_bytes(self, bytes_value: int) -> str:
        """
        Format bytes value to human readable string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"
