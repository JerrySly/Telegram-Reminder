from abstract import Provider
import os


class FileProvider(Provider):
  def __init__(self, filePath: str) -> None:
    super().__init__()
    self.filePath = filePath


  def save(self, message):
    with open(self.filePath, 'a') as f:
      f.write(message + '\n')


  def get_data(self):
    with open(self.filePath, 'r') as f:
      data = f.read()
      return data
    
  def clear_data(self):
    open(self.filePath, 'w').close()

  def get_action_on_time_exist(self, hour, min):
    data = self.get_data().split('\n')
    result = []
    for str in data:
      if not str.strip():
        pass
      strData = str.split('-')
      if strData.__len__() < 2:
        pass
      if strData[0].strip() == f'{f"0{hour}" if hour < 10 else hour}:{f"0{min}" if min < 10 else min}':
        result.append(strData[1])
    return result

