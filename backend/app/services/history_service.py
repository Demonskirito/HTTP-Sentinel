import json
import threading
from pathlib import Path
from typing import List, Dict


class HistoryService:

    def __init__(self):
        self.history_file = Path(
            "/app/data/http_history.jsonl"
        )
        self._lock = threading.Lock()

        print(
            f"[HistoryService] History file: "
            f"{self.history_file}"
        )

    def get_all(self) -> List[Dict]:
        if not self.history_file.exists():
            return []

        records = []

        with self._lock:
            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        records.append(
                            json.loads(line)
                        )
                    except json.JSONDecodeError:
                        continue

        return records

    def get_latest(
        self,
        limit: int = 100
    ) -> List[Dict]:

        records = self.get_all()

        return records[-limit:]


history_service = HistoryService()