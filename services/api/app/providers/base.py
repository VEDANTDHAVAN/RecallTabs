from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def chat(self, *, system: str, user: str):
        pass

    @abstractmethod
    def stream_chat(self, *, system: str, user: str):
        pass

    @abstractmethod
    def completion(self, prompt: str):
        pass