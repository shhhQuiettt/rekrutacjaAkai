import json
from typing import List, Dict, Any


class Importer:
    def __init__(self, tasks_source: str = "taski.json"):
        self.tasks = []
        self.tasks_source = tasks_source

    def read_tasks(self) -> None:
        with open(self.tasks_source) as json_file:
            self.tasks = json.load(json_file)

    def get_tasks(self) -> List[Dict[str, Any]]:
        return self.tasks
