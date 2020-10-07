from abc import ABC, abstractmethod

class UIComponent(ABC):

    @abstractmethod
    def get_layout(self):
        pass

    @abstractmethod
    def process_event(self, window, event, values):
        pass
