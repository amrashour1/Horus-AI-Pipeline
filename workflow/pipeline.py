#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pipeline Module for Horus AI Pipeline

This module implements the main pipeline for processing tasks through various AI models.
"""

import logging
import time
from typing import Dict, Any, List, Optional, Union, Callable
import json

class Pipeline:
    """
    Main pipeline that orchestrates data flow between different AI models.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Configuration dictionary for the pipeline
        """
        self.config = config or {}
        self.logger = logging.getLogger("horus.workflow.pipeline")
        self.stages = []  # List of pipeline stages
        self.stage_models = {}  # stage_name -> list of models
        self.pre_processors = {}  # stage_name -> preprocessor function
        self.post_processors = {}  # stage_name -> postprocessor function
        
        # Execution statistics
        self.execution_stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'average_execution_time': 0
        }
        
        self.logger.info("Initialized Pipeline")
    
    def add_stage(self, stage_name: str, models: List[Any], 
                 pre_processor: Optional[Callable] = None,
                 post_processor: Optional[Callable] = None) -> bool:
        """
        Add a processing stage to the pipeline.
        
        Args:
            stage_name: Unique name for this pipeline stage
            models: List of model objects that implement the BaseModel interface
            pre_processor: Optional function to process data before model execution
            post_processor: Optional function to process results after model execution
            
        Returns:
            True if stage was added successfully, False otherwise
        """
        if stage_name in self.stage_models:
            self.logger.warning(f"Stage '{stage_name}' already exists in pipeline")
            return False
        
        self.stages.append(stage_name)
        self.stage_models[stage_name] = models
        
        if pre_processor:
            self.pre_processors[stage_name] = pre_processor
        
        if post_processor:
            self.post_processors[stage_name] = post_processor
        
        self.logger.info(f"Added pipeline stage '{stage_name}' with {len(models)} models")
        return True
    
    def execute(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a task through the pipeline.
        
        Args:
            task: Task data to process
            context: Optional context information for processing
            
        Returns:
            Processing results
        """
        start_time = time.time()
        task_id = task.get('task_id', 'unknown')
        context = context or {}
        
        # Initialize processing state
        state = {
            'task': task,
            'context': context,
            'stage_results': {},
            'final_result': None,
            'errors': [],
            'execution_times': {}
        }
        
        self.logger.info(f"Starting pipeline execution for task {task_id}")
        
        # Execute each stage in order
        for stage_name in self.stages:
            state = self._execute_stage(stage_name, state)
            
            # Check for stage failure
            if state.get('failed', False):
                self.logger.error(f"Pipeline execution failed at stage '{stage_name}' for task {task_id}")
                break
        
        # Compute final results
        if not state.get('failed', False):
            state['final_result'] = self._compile_results(state)
            state['success'] = True
        else:
            state['success'] = False
        
        # Calculate execution time
        execution_time = time.time() - start_time
        state['total_execution_time'] = execution_time
        
        # Update statistics
        self._update_statistics(state['success'], execution_time)
        
        self.logger.info(f"Completed pipeline execution for task {task_id} in {execution_time:.4f} seconds")
        
        return {
            'task_id': task_id,
            'success': state['success'],
            'result': state['final_result'],
            'errors': state['errors'],
            'execution_time': execution_time,
            'stage_times': state['execution_times']
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get pipeline execution statistics.
        
        Returns:
            Dictionary with pipeline statistics
        """
        return self.execution_stats
    
    def _execute_stage(self, stage_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single pipeline stage.
        
        Args:
            stage_name: Name of the stage to execute
            state: Current pipeline execution state
            
        Returns:
            Updated pipeline state
        """
        stage_start_time = time.time()
        task_id = state['task'].get('task_id', 'unknown')
        input_data = state['task'].get('request_data', {})
        
        self.logger.debug(f"Executing stage '{stage_name}' for task {task_id}")
        
        # Apply pre-processor if defined
        if stage_name in self.pre_processors:
            try:
                input_data = self.pre_processors[stage_name](input_data, state['context'])
                self.logger.debug(f"Applied pre-processor for stage '{stage_name}'")
            except Exception as e:
                error_msg = f"Pre-processor error in stage '{stage_name}': {str(e)}"
                self.logger.error(error_msg)
                state['errors'].append(error_msg)
                state['failed'] = True
                return state
        
        # Get models for this stage
        models = self.stage_models.get(stage_name, [])
        if not models:
            error_msg = f"No models found for stage '{stage_name}'"
            self.logger.error(error_msg)
            state['errors'].append(error_msg)
            state['failed'] = True
            return state
        
        # Execute each model
        stage_results = []
        for model in models:
            try:
                result = model.process(input_data)
                stage_results.append(result)
                self.logger.debug(f"Model {model.model_id} executed successfully in stage '{stage_name}'")
            except Exception as e:
                error_msg = f"Model error in stage '{stage_name}' with model {model.model_id}: {str(e)}"
                self.logger.error(error_msg)
                state['errors'].append(error_msg)
                # Don't fail the stage if at least one model succeeded
                if not stage_results:
                    state['failed'] = True
                    return state
        
        # Apply post-processor if defined
        if stage_name in self.post_processors:
            try:
                processed_results = self.post_processors[stage_name](stage_results, state['context'])
                self.logger.debug(f"Applied post-processor for stage '{stage_name}'")
            except Exception as e:
                error_msg = f"Post-processor error in stage '{stage_name}': {str(e)}"
                self.logger.error(error_msg)
                state['errors'].append(error_msg)
                state['failed'] = True
                return state
        else:
            # If no post-processor, use all results or the first one if there's only one model
            processed_results = stage_results[0] if len(stage_results) == 1 else stage_results
        
        # Update state with stage results
        state['stage_results'][stage_name] = processed_results
        
        # Record execution time for this stage
        stage_execution_time = time.time() - stage_start_time
        state['execution_times'][stage_name] = stage_execution_time
        
        self.logger.info(f"Stage '{stage_name}' completed in {stage_execution_time:.4f} seconds")
        
        return state
    
    def _compile_results(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compile final results from all pipeline stages.
        
        Args:
            state: Current pipeline execution state
            
        Returns:
            Compiled final results
        """
        # Default implementation: combine all stage results
        final_result = {
            'stages': {}
        }
        
        for stage_name, result in state['stage_results'].items():
            final_result['stages'][stage_name] = result
        
        # If we only have one stage, simplify output
        if len(state['stage_results']) == 1:
            stage_name = next(iter(state['stage_results']))
            stage_result = state['stage_results'][stage_name]
            
            # Add stage result to the top level, keeping the stages structure for reference
            if isinstance(stage_result, dict):
                for key, value in stage_result.items():
                    if key not in final_result:  # Don't overwrite the stages structure
                        final_result[key] = value
        
        return final_result
    
    def _update_statistics(self, success: bool, execution_time: float) -> None:
        """
        Update pipeline execution statistics.
        
        Args:
            success: Whether execution was successful
            execution_time: Total execution time in seconds
        """
        stats = self.execution_stats
        stats['total_tasks'] += 1
        
        if success:
            stats['successful_tasks'] += 1
        else:
            stats['failed_tasks'] += 1
        
        # Update average execution time
        if stats['total_tasks'] == 1:
            stats['average_execution_time'] = execution_time
        else:
            # Weighted average
            prev_total = stats['total_tasks'] - 1
            stats['average_execution_time'] = (
                (stats['average_execution_time'] * prev_total) + execution_time
            ) / stats['total_tasks']
