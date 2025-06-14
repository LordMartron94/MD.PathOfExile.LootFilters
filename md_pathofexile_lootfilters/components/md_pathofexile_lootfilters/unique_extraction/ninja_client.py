import requests


class PoeNinjaClient:
    """
    Concrete client for the poe.ninja ItemOverview API endpoints.
    """
    def __init__(self, base_url: str = "https://poe.ninja/api/data/itemoverview"):
        self._base_url = base_url

    def fetch_unique_items(self, league: str, item_type: str) -> dict:
        params = {"league": league, "type": item_type}
        response = requests.get(self._base_url, params=params)
        response.raise_for_status()
        return response.json()
