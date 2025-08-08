import requests
import os

API_KEY = os.getenv("AVIATIONSTACK_KEY")
BASE = "http://api.aviationstack.com/v1"

def search_flights(dep, arr):
    resp = requests.get(f"{BASE}/flights", params={
      "access_key": API_KEY,
      "dep_iata": dep,
      "arr_iata": arr
    })
    return resp.json().get("data", [])[:5]  # limit to 5 results
