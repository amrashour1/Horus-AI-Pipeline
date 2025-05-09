#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task Scheduler Module for Horus AI Pipeline

This module handles the scheduling and distribution of tasks among different AI models.
"""

import logging
import time
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

class TaskScheduler:
    """
    Task Scheduler that distributes processing tasks among different AI models.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the task scheduler.
        
        Args:
            config: Configuration dictionary for the scheduler
        """
        self.config = config or {}
        self.logger = logging.getLogger("horus.task_distribution.scheduler")
        self.task_queue = []
        self.active_tasks = {}  # task_id -> task_info
        self.completed_tasks = {}  # task_id -> task_info
        self.max_queue_size = self.config.get('max_queue_size', 100)
        self.logger.info("Initialized TaskScheduler")
    
    def create_task(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task from the request data.
        
        Args:
            request_data: The incoming request data
            
        Returns:
            Created task information
        """
        task_id = self._generate_task_id()
        task_type = request_data.get('task_type', 'unknown')
        priority = request_data.get('priority', 1)  # Default priority: 1 (normal)
        
        task = {
            'task_id': task_id,
            'task_type': task_type,
            'priority': priority,
            'status': 'pending',
            'request_data': request_data,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'result': None
        }
        
        self._add_to_queue(task)
        
        self.logger.info(f"Created task {task_id} of type {task_type} with priority {priority}")
        return task
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Get the next task from the queue based on priority.
        
        Returns:
            The next task to process, or None if queue is empty
        """
        if not self.task_queue:
            return None
        
        # Sort queue by priority (higher numbers are higher priority)
        self.task_queue.sort(key=lambda x: x['priority'], reverse=True)
        
        # Get the highest priority task
        task = self.task_queue.pop(0)
        
        # Move to active tasks
        task['status'] = 'processing'
        task['updated_at'] = datetime.now().isoformat()
        task['started_at'] = datetime.now().isoformat()
        self.active_tasks[task['task_id']] = task
        
        self.logger.info(f"Retrieved task {task['task_id']} for processing")
        return task
    
    def update_task_status(self, task_id: str, status: str, result: Dict[str, Any] = None) -> bool:
        """
        Update the status and result of a task.
        
        Args:
            task_id: The ID of the task to update
            status: The new status ('completed', 'failed', etc.)
            result: Optional result data
            
        Returns:
            True if update was successful, False otherwise
        """
        if task_id not in self.active_tasks:
            self.logger.error(f"Cannot update task {task_id}: not in active tasks")
            return False
        
        task = self.active_tasks[task_id]
        task['status'] = status
        task['updated_at'] = datetime.now().isoformat()
        
        if status in ['completed', 'failed']:
            task['completed_at'] = datetime.now().isoformat()
            if result is not None:
                task['result'] = result
            
            # Move from active to completed
            self.completed_tasks[task_id] = task
            del self.active_tasks[task_id]
            
            self.logger.info(f"Task {task_id} marked as {status}")
        else:
            self.logger.info(f"Task {task_id} status updated to {status}")
        
        return True
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current status and information about a task.
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            Task information or None if task not found
        """
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        elif task_id in self.completed_tasks:
            return self.completed_tasks[task_id]
        else:
            for task in self.task_queue:
                if task['task_id'] == task_id:
                    return task
        
        self.logger.warning(f"Task {task_id} not found")
        return None
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a pending or active task.
        
        Args:
            task_id: The ID of the task to cancel
            
        Returns:
            True if cancellation was successful, False otherwise
        """
        # Check if in queue
        for i, task in enumerate(self.task_queue):
            if task['task_id'] == task_id:
                cancelled_task = self.task_queue.pop(i)
                cancelled_task['status'] = 'cancelled'
                cancelled_task['updated_at'] = datetime.now().isoformat()
                self.completed_tasks[task_id] = cancelled_task
                
                self.logger.info(f"Cancelled queued task {task_id}")
                return True
        
        # Check if active
        if task_id in self.active_tasks:
            self.update_task_status(task_id, 'cancelled')
            self.logger.info(f"Cancelled active task {task_id}")
            return True
        
        self.logger.warning(f"Cannot cancel task {task_id}: not found or already completed")
        return False
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the task queue.
        
        Returns:
            Dictionary with queue statistics
        """
        return {
            'queue_length': len(self.task_queue),
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'total_tasks': len(self.task_queue) + len(self.active_tasks) + len(self.completed_tasks),
            'queue_by_priority': self._count_by_priority(),
            'queue_by_type': self._count_by_type()
        }
    
    def _generate_task_id(self) -> str:
        """
        Generate a unique task ID.
        
        Returns:
            Unique task ID string
        """
        return f"task_{uuid.uuid4().hex[:12]}_{int(time.time())}"
    
    def _add_to_queue(self, task: Dict[str, Any]) -> None:
        """
        Add a task to the queue, respecting max queue size.
        
        Args:
            task: The task to add to the queue
        """
        # Check if queue is full
        if len(self.task_queue) >= self.max_queue_size:
            # Remove the lowest priority task
            self.task_queue.sort(key=lambda x: x['priority'])
            removed_task = self.task_queue.pop(0)
            self.logger.warning(f"Queue full, removed lowest priority task {removed_task['task_id']}")
        
        self.task_queue.append(task)
    
    def _count_by_priority(self) -> Dict[int, int]:
        """
        Count tasks in queue by priority level.
        
        Returns:
            Dictionary mapping priority levels to counts
        """
        priority_counts = {}
        for task in self.task_queue:
            priority = task['priority']
            if priority in priority_counts:
                priority_counts[priority] += 1
            else:
                priority_counts[priority] = 1
        return priority_counts
    
    def _count_by_type(self) -> Dict[str, int]:
        """
        Count tasks in queue by task type.
        
        Returns:
            Dictionary mapping task types to counts
        """
        type_counts = {}
        for task in self.task_queue:
            task_type = task['task_type']
            if task_type in type_counts:
                type_counts[task_type] += 1
            else:
                type_counts[task_type] = 1
        return type_counts
