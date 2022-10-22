import json
from typing import List, Dict, Any


class Exporter:
    def __init__(self, tasks_destination: str = "taski.json"):
        self.tasks_destination = tasks_destination

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        with open(self.tasks_destination, "w") as json_file:
            json.dump(tasks, json_file)
