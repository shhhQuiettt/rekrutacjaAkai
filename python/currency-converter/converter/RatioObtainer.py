import json, urllib.request
from typing import Any, Dict, Optional
from datetime import datetime
from pprint import pprint


class RatioObtainer:
    base = None
    target = None

    def __init__(self, base, target):
        self.base = base
        self.target = target
        self.exchange_ratio: Optional[float] = None
        self.cached_ratios = []

    def was_ratio_saved_today(self) -> bool:
        try:
            with open("ratios.json") as ratios_file:
                self.cached_ratios = json.load(ratios_file)
        except FileNotFoundError:
            return False

        for ratio in self.cached_ratios:
            if (
                self._is_the_same_ratio(ratio)
                and datetime.strptime(ratio["date_fetched"], "%Y-%m-%d")
                == datetime.today()
            ):
                self.exchange_ratio = ratio.ratio
                return True

        return False

    def _is_the_same_ratio(self, ratio: Dict[str, Any]):
        return (
            ratio["base_currency"] == self.base
            and ratio["target_currency"] == self.target
        )

    def fetch_ratio(self):
        with urllib.request.urlopen(
            f"https://api.exchangerate.host/convert?from={self.base}&to={self.target}"
        ) as response:
            body = response.read()

        json_body = json.loads(body)
        if json_body["success"] is False or json_body["result"] is None:
            raise ValueError(f"Convertion not found for pair {self.base}-{self.target}")
        new_ratio = self._normalize_json_response(json_body)

        self.exchange_ratio = new_ratio["ratio"]

        self.save_ratio(new_ratio)

    @staticmethod
    def _normalize_json_response(data: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_data = {
            "base_currency": data["query"]["from"],
            "target_currency": data["query"]["to"],
            "ratio": data["result"],
            "date_fetched": data["date"],
        }
        return cleaned_data

    def save_ratio(self, ratio: Dict[str, Any]) -> None:
        existed = False
        for i in range(len(self.cached_ratios)):
            if self._is_the_same_ratio(self.cached_ratios[i]):
                self.cached_ratios[i] = ratio
                existed = True
            break
        if not existed:
            self.cached_ratios.append(ratio)

        with open("ratios.json", "w") as ratios_file:
            json.dump(self.cached_ratios, ratios_file)

    def get_matched_ratio_value(self) -> float:
        return self.exchange_ratio
