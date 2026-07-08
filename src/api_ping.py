import json
import requests
import os

url = "https://dragonball-api.com/api/characters"

# file_path = r"C:/Users/Sibug/Desktop/CLMagno_Bootcamp/July_04_2026_ETL/"

""" 
try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response. json()
        print(json.dumps(data, indent=2)[:500])
    else:
        print(f"Request failed with status: {response.status_code}")
except requests.RequestException as exc:
    print(f"Network error: {exc}") 
"""


all_rows = []
page = 1
print("fetching data ... ")
while True:
    try:
        res = requests.get(url, params={"page": page, "limit": 10}, timeout=30)
        res.raise_for_status()
        payload = res.json()
        rows = payload.get("items", [])
        if not rows:
            print("no more rows to fetch, exiting loop.")
            break

        all_rows.extend(rows)
        print("successfully fetched page", page, "with", len(rows), "rows.")
        
        characters = [row.get("name") for row in rows]
        print("character names:", characters)
        # print(rows)

        next_page = payload.get("links", {}).get("next","")
        if not next_page:
            print("no next page link found, exiting loop.")
            break

        page += 1
            

    except requests.RequestException as exc:
        print(f"Error fetching data from page {page}: {exc}")
        break

print("---------")
print("Total rows fetched:", len(all_rows))

# if all_rows:
#     print("Sample data:")
#     print(json.dumps(all_rows[0], indent=2)[:500])

if all_rows:
    try:
        raw_path = os.getenv("RAW_DATA_PATH")
        with open(f"{raw_path}dragonball_characters.json", "w") as f:
            json.dump(all_rows, f, indent=2)
        print("Data saved to dragonball_characters.json")
    except IOError as e:
        print(f"Error saving data to file: {e}")