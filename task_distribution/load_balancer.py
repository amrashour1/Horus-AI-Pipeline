#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load Balancer Module for Horus AI Pipeline

This module handles the distribution of tasks among available model instances
to optimize resource utilization and throughput.
"""

import logging
import time
from typing import Dict, Any, List, Optional, Tuple
import random

class LoadBalancer:
    """
    Load Balancer that distributes tasks among model instances based on workload and capacity.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the load balancer.
        
        Args:
            config: Configuration dictionary for the load balancer
        """
        self.config = config or {}
        self.logger = logging.getLogger("horus.task_distribution.load_balancer")
        self.model_instances = {}  # model_id -> {instance_id -> instance_info}
        self.health_checks = {}    # instance_id -> last_health_status
        
        # Load balancing strategy
        self.strategy = self.config.get('strategy', 'round_robin')
        self.last_used_indices = {}  # For round-robin strategy
        
        self.logger.info(f"Initialized LoadBalancer with strategy: {self.strategy}")
    
    def register_model_instance(self, model_id: str, instance_id: str, capacity: int = 1, 
                               metadata: Dict[str, Any] = None) -> bool:
        """
        Register a model instance with the load balancer.
        
        Args:
            model_id: The model type identifier
            instance_id: Unique identifier for this model instance
            capacity: Number of concurrent tasks this instance can handle
            metadata: Additional metadata about the instance
            
        Returns:
            True if registration was successful, False otherwise
        """
        if model_id not in self.model_instances:
            self.model_instances[model_id] = {}
        
        # Check if already registered
        if instance_id in self.model_instances[model_id]:
            self.logger.warning(f"Instance {instance_id} for model {model_id} already registered")
            return False
        
        # Register the instance
        self.model_instances[model_id][instance_id] = {
            'model_id': model_id,
            'instance_id': instance_id,
            'capacity': capacity,
            'current_load': 0,
            'total_processed': 0,
            'last_active': time.time(),
            'metadata': metadata or {}
        }
        
        # Initialize health check
        self.health_checks[instance_id] = {
            'status': 'healthy',
            'last_check': time.time(),
            'consecutive_failures': 0
        }
        
        self.logger.info(f"Registered instance {instance_id} for model {model_id} with capacity {capacity}")
        return True
    
    def unregister_model_instance(self, instance_id: str) -> bool:
        """
        Unregister a model instance from the load balancer.
        
        Args:
            instance_id: Unique identifier for the model instance
            
        Returns:
            True if unregistration was successful, False otherwise
        """
        for model_id, instances in self.model_instances.items():
            if instance_id in instances:
                # Check if instance is currently processing tasks
                if instances[instance_id]['current_load'] > 0:
                    self.logger.warning(f"Instance {instance_id} still has active tasks, marking for removal when idle")
                    instances[instance_id]['pending_removal'] = True
                    return True
                
                # Remove the instance
                del instances[instance_id]
                if instance_id in self.health_checks:
                    del self.health_checks[instance_id]
                
                self.logger.info(f"Unregistered instance {instance_id} from model {model_id}")
                return True
        
        self.logger.warning(f"Instance {instance_id} not found for unregistration")
        return False
    
    def allocate_instance(self, model_id: str, task_id: str) -> Optional[str]:
        """
        Allocate a model instance for a specific task based on current load.
        
        Args:
            model_id: The model type identifier
            task_id: The ID of the task to allocate an instance for
            
        Returns:
            instance_id of allocated instance, or None if no suitable instance found
        """
        if model_id not in self.model_instances or not self.model_instances[model_id]:
            self.logger.warning(f"No instances registered for model {model_id}")
            return None
        
        instances = self.model_instances[model_id]
        
        # Get only healthy instances
        healthy_instances = {}
        for inst_id, inst_info in instances.items():
            if inst_id in self.health_checks and self.health_checks[inst_id]['status'] == 'healthy':
                # Skip instances marked for removal
                if inst_info.get('pending_removal', False):
                    continue
                healthy_instances[inst_id] = inst_info
        
        if not healthy_instances:
            self.logger.warning(f"No healthy instances available for model {model_id}")
            return None
        
        # Select instance based on strategy
        if self.strategy == 'least_loaded':
            instance_id = self._select_least_loaded(healthy_instances)
        elif self.strategy == 'random':
            instance_id = self._select_random(healthy_instances)
        else:  # Default to round-robin
            instance_id = self._select_round_robin(model_id, healthy_instances)
        
        if instance_id:
            # Update instance load
            instances[instance_id]['current_load'] += 1
            instances[instance_id]['last_active'] = time.time()
            self.logger.info(f"Allocated instance {instance_id} for task {task_id}, current load: {instances[instance_id]['current_load']}")
        
        return instance_id
    
    def release_instance(self, instance_id: str, task_id: str, success: bool = True) -> bool:
        """
        Release a model instance after task completion.
        
        Args:
            instance_id: The instance ID to release
            task_id: The task ID that was processed
            success: Whether the task was processed successfully
            
        Returns:
            True if release was successful, False otherwise
        """
        for model_id, instances in self.model_instances.items():
            if instance_id in instances:
                instance = instances[instance_id]
                
                # Update instance info
                instance['current_load'] = max(0, instance['current_load'] - 1)
                instance['total_processed'] += 1
                instance['last_active'] = time.time()
                
                self.logger.info(f"Released instance {instance_id} after task {task_id}, new load: {instance['current_load']}")
                
                # Check if instance was pending removal and is now idle
                if instance.get('pending_removal', False) and instance['current_load'] == 0:
                    self.unregister_model_instance(instance_id)
                
                return True
        
        self.logger.warning(f"Instance {instance_id} not found for release")
        return False
    
    def update_health_status(self, instance_id: str, is_healthy: bool, details: Dict[str, Any] = None) -> bool:
        """
        Update the health status of a model instance.
        
        Args:
            instance_id: The instance ID to update
            is_healthy: Whether the instance is healthy
            details: Additional health check details
            
        Returns:
            True if update was successful, False otherwise
        """
        if instance_id not in self.health_checks:
            self.logger.warning(f"Instance {instance_id} not found for health update")
            return False
        
        health_info = self.health_checks[instance_id]
        current_status = health_info['status']
        
        health_info['last_check'] = time.time()
        
        if is_healthy:
            health_info['status'] = 'healthy'
            health_info['consecutive_failures'] = 0
            health_info['details'] = details or {}
            
            if current_status != 'healthy':
                self.logger.info(f"Instance {instance_id} recovered and is now healthy")
        else:
            health_info['consecutive_failures'] += 1
            threshold = self.config.get('failure_threshold', 3)
            
            if health_info['consecutive_failures'] >= threshold:
                health_info['status'] = 'unhealthy'
                health_info['details'] = details or {}
                
                if current_status == 'healthy':
                    self.logger.warning(f"Instance {instance_id} marked unhealthy after {threshold} consecutive failures")
            else:
                self.logger.warning(f"Instance {instance_id} health check failed ({health_info['consecutive_failures']}/{threshold})")
        
        return True
    
    def get_instance_stats(self, model_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics about registered model instances.
        
        Args:
            model_id: Optional model ID to filter stats, or None for all
            
        Returns:
            Dictionary with instance statistics
        """
        stats = {
            'total_instances': 0,
            'healthy_instances': 0,
            'unhealthy_instances': 0,
            'total_capacity': 0,
            'current_load': 0,
            'load_percentage': 0,
            'models': {}
        }
        
        # Filter by model_id if provided
        model_ids = [model_id] if model_id and model_id in self.model_instances else self.model_instances.keys()
        
        for mid in model_ids:
            model_stats = {
                'instance_count': 0,
                'healthy_instances': 0,
                'total_capacity': 0,
                'current_load': 0,
                'load_percentage': 0
            }
            
            for instance_id, instance in self.model_instances[mid].items():
                model_stats['instance_count'] += 1
                model_stats['total_capacity'] += instance['capacity']
                model_stats['current_load'] += instance['current_load']
                
                if instance_id in self.health_checks and self.health_checks[instance_id]['status'] == 'healthy':
                    model_stats['healthy_instances'] += 1
                    stats['healthy_instances'] += 1
                else:
                    stats['unhealthy_instances'] += 1
            
            if model_stats['total_capacity'] > 0:
                model_stats['load_percentage'] = (model_stats['current_load'] / model_stats['total_capacity']) * 100
            
            stats['models'][mid] = model_stats
            stats['total_instances'] += model_stats['instance_count']
            stats['total_capacity'] += model_stats['total_capacity']
            stats['current_load'] += model_stats['current_load']
        
        if stats['total_capacity'] > 0:
            stats['load_percentage'] = (stats['current_load'] / stats['total_capacity']) * 100
        
        return stats
    
    def _select_least_loaded(self, instances: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """
        Select the least loaded instance.
        
        Args:
            instances: Dictionary of instance_id -> instance_info
            
        Returns:
            Selected instance_id or None if no instances available
        """
        if not instances:
            return None
        
        # Calculate load ratio (current_load / capacity) for each instance
        load_ratios = {}
        for inst_id, inst_info in instances.items():
            capacity = max(1, inst_info['capacity'])  # Avoid division by zero
            load_ratios[inst_id] = inst_info['current_load'] / capacity
        
        # Select instance with lowest load ratio
        return min(load_ratios.items(), key=lambda x: x[1])[0]
    
    def _select_random(self, instances: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """
        Select a random instance.
        
        Args:
            instances: Dictionary of instance_id -> instance_info
            
        Returns:
            Selected instance_id or None if no instances available
        """
        if not instances:
            return None
        
        return random.choice(list(instances.keys()))
    
    def _select_round_robin(self, model_id: str, instances: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """
        Select an instance using round-robin strategy.
        
        Args:
            model_id: The model type identifier
            instances: Dictionary of instance_id -> instance_info
            
        Returns:
            Selected instance_id or None if no instances available
        """
        if not instances:
            return None
        
        instance_ids = list(instances.keys())
        
        # Initialize index for this model_id if not exists
        if model_id not in self.last_used_indices:
            self.last_used_indices[model_id] = -1
        
        # Move to next index, wrapping around if necessary
        self.last_used_indices[model_id] = (self.last_used_indices[model_id] + 1) % len(instance_ids)
        
        return instance_ids[self.last_used_indices[model_id]]
