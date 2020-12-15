from flask import Flask, jsonify, send_file, request 
from flask_sqlalchemy import SQLAlchemy
from database import Recipie, Ingredient, Step
from core import get_ingredients, get_steps
from peewee import *
import sqlite3
import json


app = Flask(__name__)
code = open("key.txt", "r")
app.secret_key = code.readlines()[0]


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
        try:
            recipie = Recipie(food_name = data["name"], description = data["description"], top_image = data["top image"], bottom_image = data["bottom image"])
            recipie.save()
            return jsonify({"status": "success", "data": data}), 201
        except:
            return jsonify({"status": "error", "error": {"Important keys(in this order)": ["name", "description", "top image", "bottom image"]}}), 404
    query = Recipie.select().dicts()
    all_recipies = []
    for item in query:
        all_recipies.append(item)
    return jsonify({"status": "success", "data": all_recipies})


@app.route("/recipies/<name>", methods=["GET"])
def get_recipie(name):
    query = Recipie.select().where(Recipie.food_name == name).tuples()
    one_recipie = []
    for item in query:
        one_recipie.append(item)
    return jsonify({"status": "success", "data": one_recipie})


@app.route("/recipies/<idnumber>", methods=["PUT", "DELETE"])
def update_recipie(idnumber):
    if request.method == "PUT":
        data = request.get_json()
        update_data = Recipie.update(food_name = data["name"], description = data["description"], top_image = data["top image"], bottom_image = data["bottom image"].where(Recipie.id == idnumber))
        update_data.execute()
        query = Recipie.select().where(Recipie.id == idnumber).tuples()
        updated_recipie = []
        for item in query:
            updated_recipie.append(item)
        return jsonify({"status": "success", "data": updated_recipie})
    elif request.method == "DELETE":
        recipie = Recipie.get(Recipie.id == idnumber)
        recipie.delete_instance()
        return Recipie.get_or_none(Recipie.id == idnumber)


@app.route("/recipies/<name>/<act>", methods=["GET", "POST"])
def get_act(name, act):
    key = Recipie.get(Recipie.food_name == name).id
    if act == "ingredients":
        if request.method == "POST":
            data = request.get_json()
            try:
                get_ingredients(data, key)
            except:
                return jsonify({"status": "error", "error": {"Keys(in this order)": ["category(optional)", "name(important)", "quantity(important)", "type(optional)", "requirement(optional)", "size(optional)"]}}), 404
        query = Ingredient.select().where(Ingredient.food_id == key).dicts()
        step_ingre = []
        for item in query:
            step_ingre.append(item)
    elif act == "steps":
        if request.method == "POST":
            data = request.get_json()
            try:
                get_steps(data, key)
            except:
                print(Error)
                return jsonify({"status": "error", "error": {"Keys(in this order)": ["category(optional)", "name(optional)", "action(important)", "image(optional)"]}}), 404
        query = Step.select().where(Step.food_id == key).dicts()
        step_ingre = []
        for item in query:
            step_ingre.append(item)
    else:
        return jsonify({"status": "error", "Key Error": "Act available in database: steps and ingredients"})
    return jsonify({"status": "success", f"{act}": step_ingre})


@app.route("/recipies/<act>/<idnumber>", methods=["PUT", "DELETE"])
def update_act(act, idnumber):
    if request.method == "PUT":
        if act == "ingredients":
            pass
        elif act == "steps":
            pass
        else:
            return jsonify({"status": "error", "Key Error": "Act available in database: steps and ingredients"})
    elif request.method == "DELETE":
        if act == "ingredients":
            pass
        elif act == "steps":
            pass
        else:
            return jsonify({"status": "error", "Key Error": "Act available in database: steps and ingredients"})


if __name__ == "__main__":
    app.run()
