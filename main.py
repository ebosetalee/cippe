from flask import Flask, jsonify, send_file
import json
import sqlite3


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World"


@app.route("/selfie", methods=["GET"])
def selfie():
    return send_file("pictures/screenshot.jpeg", mimetype="image/jpeg")


@app.route("/recipies", methods=["GET"])
def recipies():
    cippie_db = sqlite3.connect("cippedb.db")
    cursor = cippie_db.cursor()
    recipe = cursor.execute("SELECT food_name FROM recipies")
    return jsonify({"status": "success", "data": recipe.fetchall()})


@app.route("/recipies/<name>", methods=["GET"])
def get_recipie(name):
    cippie_db = sqlite3.connect("cippedb.db")
    cursor = cippie_db.cursor()
    recipies = cursor.execute(
        "SELECT food_name, description, top_image, bottom_image FROM recipies WHERE food_name=? ORDER BY food_name ASC LIMIT 1", 
        (name, ))
    return jsonify({"status": "success", "data": recipies.fetchall()})


@app.route("/recipies/<name>/<act>", methods=["GET"])
def get_act(name, act):
    cippe_db = sqlite3.connect("cippedb.db")
    cursor = cippe_db.cursor()
    key = cursor.execute("SELECT id FROM recipies WHERE food_name=?", (name, ))
    key_id = key.fetchone()[0]
    if act == "ingredients":
        step_ingre = cursor.execute(
            "SELECT category, name, quantity, type, requirement, size FROM ingredients WHERE food_id=?",
            (key_id, ))
    elif act == "steps":
        step_ingre = cursor.execute(
            "SELECT category, name, action, image FROM steps WHERE food_id=?",(key_id, ))
    return jsonify({"status": "success", f"{act}": step_ingre.fetchall()})


if __name__ == "__main__":
    app.run()
