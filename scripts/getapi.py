import os
import json
from datetime import datetime
from typing import Any, Dict, Optional
import requests


class velibAPI:
    """
    Fetch Velib real-time data from OpenDataParis and save as JSON files
    into the project's src/data folder with filename "velib-YYYYMMDD_HHMMSS.json".
    """

    def __init__(self, save_dir: Optional[str] = None, rows: int = 10000, timeout: int = 30) -> None:
        # API endpoint for the Velib real-time availability dataset
        self.base_url = "https://opendata.paris.fr/api/records/1.0/search/"
        self.params = {"dataset": "velib-disponibilite-en-temps-reel", "rows": rows}
        self.timeout = timeout

        # Default save directory: ../src/datas relative to this script
        if save_dir:
            self.save_dir = os.path.abspath(save_dir)
        else:
            self.save_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "datas")
            )
        os.makedirs(self.save_dir, exist_ok=True)

    def _make_filename(self) -> str:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"velib-{now}.json"

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch data from the OpenDataParis Velib API and return the parsed JSON.
        Raises requests.HTTPError on non-2xx responses.
        """
        resp = requests.get(self.base_url, params=self.params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def fetch_and_save(self) -> str:
        """
        Fetch data and save it to the configured src/data folder.
        Returns the full path to the saved file.
        """
        data = self.fetch()
        filename = self._make_filename()
        path = os.path.join(self.save_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path


if __name__ == "__main__":
    api = velibAPI()
    try:
        saved_path = api.fetch_and_save()
        print(saved_path)
    except Exception as e:
        print("Failed to fetch/save Velib data:", e)