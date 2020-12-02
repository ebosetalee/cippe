from flask import Flask, jsonify, send_file, request #, g, current_app
from core import get_ingredients, get_steps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import sqlite3
import json


app = Flask(__name__)
code = open("key.txt", "r")
app.secret_key = code.readlines()[0]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cippedb.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# db.Model.metadata.reflect(db.engine)

# class Recipies(db.Model):
#     __tablename__ = 'recipies'
#     __table_args__ = { 'extend_existing': True }
#     LOC_CODE = db.Column(db.Text, primary_key=True) 
Base = automap_base()

Base.prepare(db.engine, reflect=True)
recipie = Base.classes.recipies

@app.route("/")
def home():
    return "Hello World"


@app.route("/selfie", methods=["GET"])
def selfie():
    return send_file("pictures/screenshot.jpeg", mimetype="image/jpeg")

    
@app.route("/recipies", methods=["GET", "POST"])
def get_recipies():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        try:
            new_recipie = recipie(food_name = data["name"], description = data["description"], top_image = data["top image"], botttom_image = data["bottom image"])
            recipie.session.add(new_recipie)
            recipie.session.commit()
        except:
            recipie.session.rollback()
            return jsonify({"status": "error", "error": {"Important keys(in this order)": ["name", "description", "top image", "bottom image"]}}), 404
        finally:
            return jsonify({"status": "success"}), 201
    all_recipe = db.session.query(recipie)
    print(all_recipe)

    return jsonify({"status": "success", "data": all_recipe})


@app.route("/recipies/<name>", methods=["GET"])
def get_recipie(name):
    cippe_db = connect_db()
    cursor = cippe_db.cursor()
    recipies = cursor.execute(
        "SELECT food_name, description, top_image, bottom_image FROM recipies WHERE food_name=? ORDER BY food_name ASC LIMIT 1", 
        (name, ))
    return jsonify({"status": "success", "data": recipies.fetchall()})


@app.route("/recipies/<name>/<act>", methods=["GET", "POST"])
def get_act(name, act):
    cippe_db = connect_db()
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
        step_ingre = cippe_db.execute(
            "SELECT category, name, action, image FROM steps WHERE food_id=? ORDER BY action",(key_id, ))
    return jsonify({"status": "success", f"{act}": step_ingre.fetchall()})

# @app.after_request
# def after_request_func(response):
#     connect_db().commit()
#     connect_db().close()
#     return response

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


if __name__ == "__main__":
    app.run()
