
"""
Auto Scaler - Automatic scaling decisions based on performance metrics
"""

import asyncio
from typing import Dict, Any, List, Optional, Callable
import logging
from datetime import datetime, timedelta
from enum import Enum


class ScalingAction(str, Enum):
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    NO_ACTION = "no_action"


class ScalingTrigger:
    """
    Represents a scaling trigger condition
    """
    
    def __init__(self, metric: str, threshold: float, comparison: str, duration: int = 60):
        self.metric = metric
        self.threshold = threshold
        self.comparison = comparison  # 'gt', 'lt', 'gte', 'lte'
        self.duration = duration  # seconds
        self.triggered_time = None
    
    def evaluate(self, current_value: float) -> bool:
        """
        Evaluate if trigger condition is met
        """
        if self.comparison == 'gt':
            return current_value > self.threshold
        elif self.comparison == 'gte':
            return current_value >= self.threshold
        elif self.comparison == 'lt':
            return current_value < self.threshold
        elif self.comparison == 'lte':
            return current_value <= self.threshold
        else:
            return False
    
    def check_duration(self) -> bool:
        """
        Check if trigger has been active for required duration
        """
        if self.triggered_time is None:
            return False
        
        return (datetime.now() - self.triggered_time).total_seconds() >= self.duration


class AutoScaler:
    """
    Automatic scaling based on performance metrics and resource utilization
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("nexus.performance.auto_scaler")
        
        # Configuration
        self.enabled = self.config.get('enabled', True)
        self.check_interval = self.config.get('check_interval', 30)  # seconds
        self.cooldown_period = self.config.get('cooldown_period', 300)  # 5 minutes
        
        # Scaling triggers
        self.scale_up_triggers = self._setup_scale_up_triggers()
        self.scale_down_triggers = self._setup_scale_down_triggers()
        
        # State
        self.last_scaling_action = None
        self.last_scaling_time = None
        self.scaling_task = None
        self.is_scaling_active = False
        
        # Callbacks
        self.scale_up_callback: Optional[Callable] = None
        self.scale_down_callback: Optional[Callable] = None
        
        self.logger.info(f"Auto Scaler initialized: enabled={self.enabled}")
    
    def _setup_scale_up_triggers(self) -> List[ScalingTrigger]:
        """
        Setup triggers for scaling up
        """
        triggers = []
        
        # CPU utilization trigger
        cpu_threshold = self.config.get('cpu_scale_up_threshold', 80.0)
        triggers.append(ScalingTrigger('cpu_percent', cpu_threshold, 'gt', 60))
        
        # Memory utilization trigger
        memory_threshold = self.config.get('memory_scale_up_threshold', 85.0)
        triggers.append(ScalingTrigger('memory_percent', memory_threshold, 'gt', 60))
        
        # Response time trigger
        response_time_threshold = self.config.get('response_time_scale_up_threshold', 5.0)
        triggers.append(ScalingTrigger('avg_response_time', response_time_threshold, 'gt', 120))
        
        # Queue length trigger
        queue_threshold = self.config.get('queue_scale_up_threshold', 10)
        triggers.append(ScalingTrigger('queue_length', queue_threshold, 'gt', 30))
        
        return triggers
    
    def _setup_scale_down_triggers(self) -> List[ScalingTrigger]:
        """
        Setup triggers for scaling down
        """
        triggers = []
        
        # CPU utilization trigger (low usage)
        cpu_threshold = self.config.get('cpu_scale_down_threshold', 30.0)
        triggers.append(ScalingTrigger('cpu_percent', cpu_threshold, 'lt', 300))  # 5 minutes
        
        # Memory utilization trigger (low usage)
        memory_threshold = self.config.get('memory_scale_down_threshold', 40.0)
        triggers.append(ScalingTrigger('memory_percent', memory_threshold, 'lt', 300))
        
        # Response time trigger (fast responses)
        response_time_threshold = self.config.get('response_time_scale_down_threshold', 1.0)
        triggers.append(ScalingTrigger('avg_response_time', response_time_threshold, 'lt', 300))
        
        return triggers
    
    async def start_auto_scaling(self) -> Dict[str, Any]:
        """
        Start the auto-scaling monitoring process
        """
        if not self.enabled:
            return {"status": "disabled", "message": "Auto-scaling is disabled"}
        
        if self.is_scaling_active:
            return {"status": "already_active", "message": "Auto-scaling is already active"}
        
        self.is_scaling_active = True
        self.scaling_task = asyncio.create_task(self._scaling_loop())
        
        self.logger.info("Auto-scaling started")
        return {"status": "started", "check_interval": self.check_interval}
    
    async def stop_auto_scaling(self) -> Dict[str, Any]:
        """
        Stop the auto-scaling monitoring process
        """
        if not self.is_scaling_active:
            return {"status": "not_active", "message": "Auto-scaling is not active"}
        
        self.is_scaling_active = False
        
        if self.scaling_task:
            self.scaling_task.cancel()
            try:
                await self.scaling_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Auto-scaling stopped")
        return {"status": "stopped"}
    
    async def _scaling_loop(self) -> None:
        """
        Main auto-scaling monitoring loop
        """
        while self.is_scaling_active:
            try:
                # Check if we're in cooldown period
                if self._in_cooldown_period():
                    await asyncio.sleep(self.check_interval)
                    continue
                
                # Get current metrics (placeholder - would be provided by performance monitor)
                current_metrics = await self._get_current_metrics()
                
                # Evaluate scaling decision
                scaling_decision = await self._evaluate_scaling_decision(current_metrics)
                
                # Execute scaling action if needed
                if scaling_decision != ScalingAction.NO_ACTION:
                    await self._execute_scaling_action(scaling_decision, current_metrics)
                
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in auto-scaling loop: {e}")
                await asyncio.sleep(self.check_interval)
    
    def _in_cooldown_period(self) -> bool:
        """
        Check if we're currently in a cooldown period after the last scaling action
        """
        if self.last_scaling_time is None:
            return False
        
        cooldown_end = self.last_scaling_time + timedelta(seconds=self.cooldown_period)
        return datetime.now() < cooldown_end
    
    async def _get_current_metrics(self) -> Dict[str, float]:
        """
        Get current performance metrics
        TODO: Integrate with actual metrics collection
        """
        # TODO: Get real metrics from performance monitor
        # This is a placeholder implementation
        return {
            'cpu_percent': 50.0,
            'memory_percent': 60.0,
            'avg_response_time': 2.0,
            'queue_length': 5,
            'active_connections': 10
        }
    
    async def _evaluate_scaling_decision(self, metrics: Dict[str, float]) -> ScalingAction:
        """
        Evaluate whether scaling action is needed
        """
        current_time = datetime.now()
        
        # Check scale-up triggers
        scale_up_triggered = False
        for trigger in self.scale_up_triggers:
            metric_value = metrics.get(trigger.metric, 0.0)
            
            if trigger.evaluate(metric_value):
                if trigger.triggered_time is None:
                    trigger.triggered_time = current_time
                    self.logger.debug(f"Scale-up trigger activated: {trigger.metric} = {metric_value}")
                
                if trigger.check_duration():
                    scale_up_triggered = True
                    self.logger.info(f"Scale-up triggered by {trigger.metric}: {metric_value} > {trigger.threshold}")
                    break
            else:
                # Reset trigger if condition is not met
                if trigger.triggered_time is not None:
                    trigger.triggered_time = None
                    self.logger.debug(f"Scale-up trigger reset: {trigger.metric} = {metric_value}")
        
        if scale_up_triggered:
            return ScalingAction.SCALE_UP
        
        # Check scale-down triggers (only if not scaling up)
        scale_down_triggered = True
        for trigger in self.scale_down_triggers:
            metric_value = metrics.get(trigger.metric, 0.0)
            
            if trigger.evaluate(metric_value):
                if trigger.triggered_time is None:
                    trigger.triggered_time = current_time
                    self.logger.debug(f"Scale-down condition met: {trigger.metric} = {metric_value}")
            else:
                scale_down_triggered = False
                # Reset trigger if condition is not met
                if trigger.triggered_time is not None:
                    trigger.triggered_time = None
                    self.logger.debug(f"Scale-down condition not met: {trigger.metric} = {metric_value}")
        
        # All scale-down triggers must be met for the required duration
        if scale_down_triggered:
            all_duration_met = all(trigger.check_duration() for trigger in self.scale_down_triggers if trigger.triggered_time is not None)
            
            if all_duration_met:
                self.logger.info("Scale-down triggered by sustained low resource usage")
                return ScalingAction.SCALE_DOWN
        
        return ScalingAction.NO_ACTION
    
    async def _execute_scaling_action(self, action: ScalingAction, metrics: Dict[str, float]) -> None:
        """
        Execute the determined scaling action
        """
        self.logger.info(f"Executing scaling action: {action}")
        
        try:
            if action == ScalingAction.SCALE_UP:
                if self.scale_up_callback:
                    await self.scale_up_callback(metrics)
                else:
                    await self._default_scale_up(metrics)
            
            elif action == ScalingAction.SCALE_DOWN:
                if self.scale_down_callback:
                    await self.scale_down_callback(metrics)
                else:
                    await self._default_scale_down(metrics)
            
            # Update scaling history
            self.last_scaling_action = action
            self.last_scaling_time = datetime.now()
            
            # Reset all triggers
            self._reset_all_triggers()
            
        except Exception as e:
            self.logger.error(f"Error executing scaling action {action}: {e}")
    
    def _reset_all_triggers(self) -> None:
        """
        Reset all trigger timers
        """
        for trigger in self.scale_up_triggers + self.scale_down_triggers:
            trigger.triggered_time = None
    
    async def _default_scale_up(self, metrics: Dict[str, float]) -> None:
        """
        Default scale-up action
        TODO: Implement default scaling logic
        """
        self.logger.info("Default scale-up action executed")
        # TODO: Implement default scaling behavior
    
    async def _default_scale_down(self, metrics: Dict[str, float]) -> None:
        """
        Default scale-down action
        TODO: Implement default scaling logic
        """
        self.logger.info("Default scale-down action executed")
        # TODO: Implement default scaling behavior
    
    def set_scale_up_callback(self, callback: Callable) -> None:
        """
        Set callback function for scale-up actions
        """
        self.scale_up_callback = callback
        self.logger.info("Scale-up callback set")
    
    def set_scale_down_callback(self, callback: Callable) -> None:
        """
        Set callback function for scale-down actions
        """
        self.scale_down_callback = callback
        self.logger.info("Scale-down callback set")
    
    def get_scaling_status(self) -> Dict[str, Any]:
        """
        Get current auto-scaling status
        """
        return {
            "enabled": self.enabled,
            "active": self.is_scaling_active,
            "last_action": self.last_scaling_action,
            "last_action_time": self.last_scaling_time.isoformat() if self.last_scaling_time else None,
            "in_cooldown": self._in_cooldown_period(),
            "check_interval": self.check_interval,
            "cooldown_period": self.cooldown_period
        }
    
    def get_trigger_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get status of all scaling triggers
        """
        def trigger_info(trigger):
            return {
                "metric": trigger.metric,
                "threshold": trigger.threshold,
                "comparison": trigger.comparison,
                "duration": trigger.duration,
                "triggered": trigger.triggered_time is not None,
                "triggered_time": trigger.triggered_time.isoformat() if trigger.triggered_time else None,
                "duration_met": trigger.check_duration()
            }
        
        return {
            "scale_up_triggers": [trigger_info(t) for t in self.scale_up_triggers],
            "scale_down_triggers": [trigger_info(t) for t in self.scale_down_triggers]
        }
