from abc import ABC, abstractmethod

class Driver(ABC):
    @abstractmethod
    def __init__(self, config):
        '''
        '''
    
    @abstractmethod
    def variables(self):
        '''
        '''
    
    @abstractmethod 
    def rules(self):
        '''
        '''

    @abstractmethod
    def commands(self):
        '''
        '''