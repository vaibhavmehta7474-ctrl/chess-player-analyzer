from flask import Flask, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)
CORS(app)

FIDE_DATA_DIR = "fide_data"


def find_fide_xml():
    if not os.path.exists(FIDE_DATA_DIR):
        return None

    for filename in os.listdir(FIDE_DATA_DIR):
        if filename.lower().endswith(".xml"):
            return os.path.join(FIDE_DATA_DIR, filename)

    return None


def find_player(fide_id):
    xml_file = find_fide_xml()

    if not xml_file:
        return None

    for event, elem in ET.iterparse(xml_file, events=("end",)):

        if elem.tag.lower().endswith("player"):
            player_id = elem.attrib.get("fideid") or elem.attrib.get("id")

            if player_id == fide_id:
                return {
                    "fide_id": fide_id,
                    "name": elem.attrib.get("name"),
                    "title": elem.attrib.get("title"),
                    "federation": elem.attrib.get("country"),
                    "standard": elem.attrib.get("standard"),
                    "rapid": elem.attrib.get("rapid"),
                    "blitz": elem.attrib.get("blitz")
                }

            elem.clear()

    return None


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

    result = find_player(fide_id)

    if result is None:
        return jsonify({
            "error": "Player not found"
        }), 404

    return jsonify(result)
