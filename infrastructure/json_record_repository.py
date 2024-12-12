import json
from typing import List, Optional

from core.models import Record
from core.record_repository import IRecordRepository

class JsonRecordRepository(IRecordRepository):
    def __init__(self, file_path: str = "records.json"):
        self.file_path = file_path

    def _load_records_from_file(self) -> List[Record]:
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return [Record(**record) for record in data]
        except FileNotFoundError:
            return []

    def _save_records_to_file(self, records: List[Record]) -> None:
        with open(self.file_path, "w") as f:
            json.dump([record.__dict__ for record in records], f, indent=4)

    def add(self, record: Record) -> None:
        records = self._load_records_from_file()
        records.append(record)
        self._save_records_to_file(records)

    def get_all(self) -> List[Record]:
        return self._load_records_from_file()

    def get(self, name: str) -> Optional[Record]:
        records = self._load_records_from_file()
        for record in records:
            if record.name == name:
                return record
        return None

    def delete(self, name: str) -> bool:
        records = self._load_records_from_file()
        updated_records = [record for record in records if record.name != name]

        if len(records) != len(updated_records):
            self._save_records_to_file(updated_records)
            return True
        return False

    def update(self, record: Record) -> bool:
        records = self._load_records_from_file()
        for i, existing_record in enumerate(records):
            if existing_record.name == record.name:
                records[i] = record
                self._save_records_to_file(records)
                return True
        return False
