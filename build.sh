#!/bin/bash

python - <<'PY'
import requests

url = "https://ratings.fide.com/download/standard_rating_list_xml.zip"

response = requests.get(url, timeout=120)
response.raise_for_status()

with open("fide_ratings.zip", "wb") as f:
    f.write(response.content)

print("FIDE ratings downloaded successfully.")
PY
