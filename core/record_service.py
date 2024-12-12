from typing import List, Optional

from core.models import Record
from core.record_repository import IRecordRepository

class RecordService:

    def __init__(self, repository: IRecordRepository):
        self.repository = repository

    def add_record(self, record: Record) -> None:
        self.repository.add(record)

    def get_top_records(self) -> List[Record]:
        return sorted(self.repository.get_all(), key=lambda r: r.score, reverse=True)[:5]

    def get_record(self, name: str) -> Optional[Record]:
        return self.repository.get(name)
