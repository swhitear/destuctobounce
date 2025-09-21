from abc import ABC, abstractmethod
from .block import Block

class BlockGen(ABC):
    """Base class for block generation strategies"""
    
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def generate(self):
        """Generate and return a list of blocks"""
        pass