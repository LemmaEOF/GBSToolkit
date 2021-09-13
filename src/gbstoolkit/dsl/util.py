from abc import ABC, abstractmethod


class NameUtil(ABC):

    @abstractmethod
    def actor_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_actor(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def trigger_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_trigger(self, name: str) -> str:
        return NotImplemented
