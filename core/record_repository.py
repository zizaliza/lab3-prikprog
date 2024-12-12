from abc import ABC, abstractmethod
from typing import List, Optional

from core.models import Record


class IRecordRepository(ABC):

    @abstractmethod
    def add(self, record: Record) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Record]:
        pass

    @abstractmethod
    def get(self, name: str) -> Optional[Record]:
        pass

    @abstractmethod
    def delete(self, name: str) -> bool:
        pass

    @abstractmethod
    def update(self, record: Record) -> bool:
        pass