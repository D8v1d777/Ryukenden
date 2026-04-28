from abc import ABC, abstractmethod
from typing import Any, Dict
from utils.logging import get_logger

class BaseModule(ABC):
    """Abstract base class for all Ryukenden modules."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def execute(self, data: Any = None) -> Any:
        """
        The primary execution logic for the module.
        Must be implemented by all subclasses.
        """
        self.logger.info(f"Executing {self.__class__.__name__}...")
        pass