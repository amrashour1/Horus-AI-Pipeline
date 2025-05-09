#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base Model Module for Horus AI Pipeline

This module defines the BaseModel abstract class that all AI models in the system
must inherit from. It provides a common interface for all models.
"""

from abc import ABC, abstractmethod
import logging
import time
import json
from typing import Dict, Any, Optional

class BaseModel(ABC):
    """
    Abstract base class for all models in Horus AI Pipeline.
    All specific model implementations should inherit from this class.
    """
    
    def __init__(self, model_id: str, model_config: Dict[str, Any] = None):
        """
        Initialize the base model.
        
        Args:
            model_id: Unique identifier for the model
            model_config: Configuration dictionary for the model
        """
        self.model_id = model_id
        self.model_config = model_config or {}
        self.logger = logging.getLogger(f"horus.models.{model_id}")
        self.creation_time = time.time()
        self.last_run_time = None
        self.total_runs = 0
        
    @abstractmethod
    def load(self) -> bool:
        """
        Load the model from disk or initialize it.
        
        Returns:
            True if loading was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data with the model and return results.
        
        Args:
            input_data: Dictionary containing the input data to process
            
        Returns:
            Dictionary containing the processing results
        """
        pass
    
    @abstractmethod
    def train(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Train the model with the provided data.
        
        Args:
            training_data: Dictionary containing the training data
            
        Returns:
            Dictionary containing training metrics and results
        """
        pass
    
    def log_execution(self, input_data: Dict[str, Any], results: Dict[str, Any], 
                      execution_time: float) -> None:
        """
        Log execution details for monitoring and analytics.
        
        Args:
            input_data: The data that was processed
            results: The results of the processing
            execution_time: The time taken for execution in seconds
        """
        self.last_run_time = time.time()
        self.total_runs += 1
        
        # Log execution summary
        self.logger.info(
            f"Model {self.model_id} executed in {execution_time:.4f} seconds. "
            f"Total runs: {self.total_runs}"
        )
    
    def to_json(self) -> str:
        """
        Convert model metadata to JSON for storage or transmission.
        
        Returns:
            JSON string representing the model's metadata
        """
        metadata = {
            "model_id": self.model_id,
            "creation_time": self.creation_time,
            "last_run_time": self.last_run_time,
            "total_runs": self.total_runs,
            "config": self.model_config
        }
        return json.dumps(metadata)
    
    @classmethod
    def from_json(cls, json_str: str) -> Dict[str, Any]:
        """
        Parse JSON metadata into a dictionary.
        
        Args:
            json_str: JSON string containing model metadata
            
        Returns:
            Dictionary containing the parsed metadata
        """
        return json.loads(json_str)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the model.
        
        Returns:
            Dictionary containing status information
        """
        return {
            "model_id": self.model_id,
            "active": True,
            "last_run": self.last_run_time,
            "total_runs": self.total_runs,
            "uptime": time.time() - self.creation_time
        }
