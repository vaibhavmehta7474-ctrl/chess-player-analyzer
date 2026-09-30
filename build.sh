#!/bin/bash

python - <<'PY'
import requests
import zipfile
import os

url = "https://ratings.fide.com/download/players_list_xml_legacy.zip"

print("Downloading FIDE player database...")

response = requests.get(url, timeout=180)
response.raise_for_status()

with open("fide_players.zip", "wb") as f:
    f.write(response.content)

print("Extracting FIDE database...")

with zipfile.ZipFile("fide_players.zip", "r") as z:
    z.extractall("fide_data")

os.remove("fide_players.zip")

print("FIDE database ready.")
PY
