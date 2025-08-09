
"""
Resource Monitor - System resource monitoring
"""

import psutil
import asyncio
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import platform


class ResourceMonitor:
    """
    Monitor system resources (CPU, Memory, Disk, Network)
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.resources")
        
        # Configuration
        self.monitoring_interval = self.config.get('monitoring_interval', 30)  # seconds
        self.cpu_alert_threshold = self.config.get('cpu_alert_threshold', 80.0)  # %
        self.memory_alert_threshold = self.config.get('memory_alert_threshold', 85.0)  # %
        self.disk_alert_threshold = self.config.get('disk_alert_threshold', 90.0)  # %
        
        # State
        self.last_cpu_times = None
        self.last_network_io = None
        self.last_disk_io = None
        
        self.logger.info("Resource Monitor initialized")
    
    async def get_current_resources(self) -> Dict[str, Any]:
        """
        Get current system resource utilization
        """
        try:
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk information
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network information
            network_io = psutil.net_io_counters()
            
            # Process information
            process = psutil.Process()
            process_info = {
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'memory_info': process.memory_info()._asdict(),
                'num_threads': process.num_threads(),
                'create_time': process.create_time()
            }
            
            resources = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'frequency': cpu_freq._asdict() if cpu_freq else None
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used,
                    'free': memory.free
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'free': swap.free,
                    'percent': swap.percent
                },
                'disk': {
                    'total': disk_usage.total,
                    'used': disk_usage.used,
                    'free': disk_usage.free,
                    'percent': (disk_usage.used / disk_usage.total) * 100
                },
                'disk_io': disk_io._asdict() if disk_io else None,
                'network_io': network_io._asdict() if network_io else None,
                'process': process_info
            }
            
            # Check for alerts
            alerts = self._check_resource_alerts(resources)
            resources['alerts'] = alerts
            
            return resources
            
        except Exception as e:
            self.logger.error(f"Error getting system resources: {e}")
            return {"error": str(e)}
    
    def _check_resource_alerts(self, resources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check for resource usage alerts
        """
        alerts = []
        
        # CPU alert
        cpu_percent = resources.get('cpu', {}).get('percent', 0)
        if cpu_percent > self.cpu_alert_threshold:
            alerts.append({
                'type': 'cpu_high',
                'message': f"High CPU usage: {cpu_percent:.1f}%",
                'threshold': self.cpu_alert_threshold,
                'current': cpu_percent
            })
        
        # Memory alert
        memory_percent = resources.get('memory', {}).get('percent', 0)
        if memory_percent > self.memory_alert_threshold:
            alerts.append({
                'type': 'memory_high',
                'message': f"High memory usage: {memory_percent:.1f}%",
                'threshold': self.memory_alert_threshold,
                'current': memory_percent
            })
        
        # Disk alert
        disk_percent = resources.get('disk', {}).get('percent', 0)
        if disk_percent > self.disk_alert_threshold:
            alerts.append({
                'type': 'disk_high',
                'message': f"High disk usage: {disk_percent:.1f}%",
                'threshold': self.disk_alert_threshold,
                'current': disk_percent
            })
        
        return alerts
    
    async def get_resource_trends(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Get resource usage trends over time
        TODO: Implement resource trend analysis
        """
        # TODO: Implement trend analysis
        # This would require storing historical data
        self.logger.info(f"Getting resource trends for {duration_minutes} minutes")
        return {"status": "TODO", "message": "get_resource_trends not yet implemented"}
    
    async def monitor_continuously(self, callback=None, interval: Optional[int] = None) -> None:
        """
        Monitor resources continuously and call callback with results
        TODO: Implement continuous monitoring
        """
        interval = interval or self.monitoring_interval
        
        self.logger.info(f"Starting continuous resource monitoring (interval: {interval}s)")
        
        while True:
            try:
                resources = await self.get_current_resources()
                
                if callback:
                    await callback(resources)
                
                # Log alerts
                alerts = resources.get('alerts', [])
                for alert in alerts:
                    self.logger.warning(f"Resource alert: {alert['message']}")
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Error in continuous monitoring: {e}")
                await asyncio.sleep(interval)
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get static system information
        """
        try:
            boot_time = psutil.boot_time()
            
            return {
                'platform': platform.system().lower(),
                'boot_time': datetime.fromtimestamp(boot_time).isoformat(),
                'cpu_count_physical': psutil.cpu_count(logical=False),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'memory_total': psutil.virtual_memory().total,
                'disk_partitions': [p._asdict() for p in psutil.disk_partitions()],
                'network_interfaces': list(psutil.net_if_addrs().keys())
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
