from abc import ABC, abstractmethod

class Provider(ABC):
  @abstractmethod
  def save(self, message):
    pass
  
  @abstractmethod
  def get_data(self):
    pass

  @abstractmethod
  def clear_data(self):
    pass
  