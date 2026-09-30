from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

FIDE_PROFILE_URL = "https://ratings.fide.com/profile/{}"


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Chess Player Analyzer API is working"
    })


@app.route("/player/<fide_id>")
def player(fide_id):

    if not fide_id.isdigit():
        return jsonify({
            "error": "FIDE ID must contain numbers only"
        }), 400

    url = FIDE_PROFILE_URL.format(fide_id)

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "ChessPlayerAnalyzer/1.0"
            }
        )

        if response.status_code == 404:
            return jsonify({
                "error": "FIDE player not found"
            }), 404

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        # Player name
        name = None

        title_tag = soup.find("title")

        if title_tag:
            title_text = title_tag.get_text(" ", strip=True)
            name = re.sub(
                r"\s+FIDE Profile.*$",
                "",
                title_text,
                flags=re.IGNORECASE
            ).strip()

        # FIDE ID
        fide_id_found = fide_id

        # Federation
        federation = None

        federation_label = soup.find(
            string=re.compile(r"Federation", re.IGNORECASE)
        )

        if federation_label:
            parent_text = federation_label.parent.get_text(
                " ",
                strip=True
            )

            match = re.search(
                r"Federation\s+([A-Z]{3})",
                parent_text
            )

            if match:
                federation = match.group(1)

        # Title
        fide_title = None

        title_match = re.search(
            r"FIDE title\s+([A-Za-z ]+?)(?=\s+World Rank|\s+Titles|\s+Info)",
            text,
            re.IGNORECASE
        )

        if title_match:
            fide_title = title_match.group(1).strip()

        # Ratings
        standard = None
        rapid = None
        blitz = None

        rating_patterns = {
            "standard": r"(\d{3,4})\s+STANDARD",
            "rapid": r"(\d{3,4})\s+RAPID",
            "blitz": r"(\d{3,4})\s+BLITZ"
        }

        for rating_type, pattern in rating_patterns.items():

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                rating = int(match.group(1))

                if rating_type == "standard":
                    standard = rating

                elif rating_type == "rapid":
                    rapid = rating

                elif rating_type == "blitz":
                    blitz = rating

        return jsonify({
            "fide_id": fide_id_found,
            "name": name,
            "federation": federation,
            "title": fide_title,
            "ratings": {
                "standard": standard,
                "rapid": rapid,
                "blitz": blitz
            },
            "source": url
        })

    except requests.RequestException as error:

        return jsonify({
            "error": "Could not reach FIDE ratings server",
            "details": str(error)
        }), 502

    except Exception as error:

        return jsonify({
            "error": "Could not read FIDE player profile",
            "details": str(error)
        }), 500
