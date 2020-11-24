from flask import Flask, jsonify, send_file, request, g
import json
import sqlite3
from core import get_ingredients, get_steps


app = Flask(__name__)
code = open("key.txt", "r")
app.secret_key = code.readlines()[0]


@app.route("/")
def home():
    return "Hello World"


@app.route("/selfie", methods=["GET"])
def selfie():
    return send_file("pictures/screenshot.jpeg", mimetype="image/jpeg")


# @app.before_request
# def before_request():
#     g.db = sqlite3.connect("cippedb.db")
    

@app.route("/recipies", methods=["GET", "POST"])
def recipies():
    cippe_db = sqlite3.connect("cippedb.db")
    cursor = cippe_db.cursor()
    if request.method == "POST":
        data = request.get_json()
        try:
            cippe_db.execute("INSERT INTO recipies VALUES(NULL, '{0}', '{1}', '{2}', '{3}')".format(
            data["name"], data["description"], data["top image"], data["bottom image"]))
            cippe_db.commit()
        except:
            return jsonify({"status": "error", "error": {"Important keys(in this order)": ["name", "description", "top image", "bottom image"]}}), 404
        finally:
            cippe_db.commit()
            return jsonify({"status": "success"}), 201
    recipe = cursor.execute("SELECT food_name FROM recipies")
    return jsonify({"status": "success", "data": recipe.fetchall()})


@app.route("/recipies/<name>", methods=["GET"])
def get_recipie(name):
    cippe_db = sqlite3.connect("cippedb.db")
    cursor = cippe_db.cursor()
    recipies = cursor.execute(
        "SELECT food_name, description, top_image, bottom_image FROM recipies WHERE food_name=? ORDER BY food_name ASC LIMIT 1", 
        (name, ))
    return jsonify({"status": "success", "data": recipies.fetchall()})


@app.route("/recipies/<name>/<act>", methods=["GET", "POST"])
def get_act(name, act):
    cippe_db = sqlite3.connect("cippedb.db")
    cursor = cippe_db.cursor()
    key = cursor.execute("SELECT id FROM recipies WHERE food_name=?", (name,))
    key_id = key.fetchone()[0]
    if act == "ingredients":
        if request.method == "POST":
            data = request.get_json()
            try:
                get_ingredients(data, key_id)
            except:
                cippe_db.rollback()
                return jsonify({"status": "error", "error": {"Keys(in this order)": ["category(optional)", "name(important)", "quantity(important)", "type(optional)", "requirement(optional)", "size(optional)"]}}), 404
            finally:
                cippe_db.commit()
                cippe_db.close()
        step_ingre = cippe_db.execute(
            "SELECT category, name, quantity, type, requirement, size FROM ingredients WHERE food_id=? ORDER BY name",
            (key_id, ))
    elif act == "steps":
        if request.method == "POST":
            data = request.get_json()
            try:
                get_steps(data, key_id)
            except:
                cippe_db.rollback()
                return jsonify({"status": "error", "error": {"Keys(in this order)": ["category(optional)", "name(optional)", "action(important)", "image(optional)"]}}), 404
            finally:
                cippe_db.commit()
                cippe_db.close()
        step_ingre = cippe_db.execute(
            "SELECT category, name, action, image FROM steps WHERE food_id=? ORDER BY action",(key_id, ))
    return jsonify({"status": "success", f"{act}": step_ingre.fetchall()})


# @app.after_request
# def after_request_func(response):
#     g.db.commit()
#     g.db.close()
#     return response


if __name__ == "__main__":
    app.run()
    code.close()
