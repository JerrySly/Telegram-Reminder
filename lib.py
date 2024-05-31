from abstract import Provider
from datetime import datetime
import time
from typing import Callable
from threading import Timer

def parse_message(text: str):
  if not text:
    pass
  [time, action] = text.split('-')
  return [time, action]

def save_action(provider: Provider, message):
  return provider.save(message)
