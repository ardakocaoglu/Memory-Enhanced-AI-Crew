from abc import ABC, abstractmethod
import json
from datetime import datetime

class BaseMemory(ABC):
    @abstractmethod
    def save(self, data):
        pass
    
    @abstractmethod
    def load(self):
        pass


class ShortTermMemory(BaseMemory):
    # Short-term memory is designed to hold information temporarily during a conversation or session.
    def __init__(self, limit: int = 5):
        self.limit = limit
        self.chat_history = []
    
    def save(self, data):
        self.chat_history.append(data)
        if len(self.chat_history) > self.limit:
            self.chat_history.pop(0)  # Remove the oldest entry to maintain the limit

    def load(self):
        return self.chat_history
    

class LongTermMemory(BaseMemory):
    # Long-term memory is designed to store information persistently across sessions.

    def __init__(self, file_path: str = 'memory.json'):
        self.__file_path = file_path
        self.__init_file()

    def __init_file(self):
        # If the file does not exist, create it with an empty dict
        try:
            with open(self.__file_path, 'r', encoding = 'utf-8') as f:
                json.read(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.__file_path, 'w', encoding = 'utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)


    def save(self, data: dict) -> None:
        current_dict: dict = self.load()
        current_dict.update(data)
        with open(self.__file_path, 'w', encoding = 'utf-8') as f:
            json.dump(current_dict, f, ensure_ascii=False, indent=4)


    def load(self) -> dict:
        with open(self.__file_path, 'r', encoding = 'utf-8') as f:
            return json.load(f)
        