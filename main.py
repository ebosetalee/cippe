from flask import Flask, jsonify, send_file, request
from database import Recipie, Ingredient, Step
from playhouse.shortcuts import model_to_dict
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
            recipie = Recipie(food_name=data["name"],
                              description=data["description"],
                              top_image=data["top image"],
                              bottom_image=data["bottom image"])
            recipie.save()
            return jsonify({"status": "success", "data": data}), 201
        except:
            return jsonify({
                "status": "error",
                "error": {
                    "Important keys(in this order)":
                    ["name", "description", "top image", "bottom image"]}}), 404
    query = Recipie.select()
    return jsonify({"status": "success", "data": model_to_dict(query.get(), recurse=False, backrefs=True)})


@app.route("/recipies/<name>", methods=["GET"])
def get_recipie(name):
    query = Recipie.select().where(Recipie.food_name == name)
    return jsonify({"status": "success", "data": model_to_dict(query.get(), backrefs=True)})


@app.route("/recipies/<id_number>", methods=["PUT", "DELETE"])
def update_recipie(id_number):
    if request.method == "PUT":
        data = request.get_json()
        update_data = Recipie.update(
            food_name=data["name"],
            description=data["description"],
            top_image=data["top image"],
            bottom_image=data["bottom image"]).where(Recipie.id == id_number)
        update_data.execute()
        query = Recipie.select().where(Recipie.id == id_number)
        return jsonify({"status": "success", "data": model_to_dict(query.get(), recurse=False, backrefs=True)})
    elif request.method == "DELETE":
        recipie = Recipie.get(Recipie.id == id_number)
        recipie.delete_instance()
        return Recipie.get_or_none(Recipie.id == id_number)


@app.route("/recipies/<name>/<act>", methods=["GET", "POST"])
def get_act(name, act):
    key = Recipie.get(Recipie.food_name == name).id
    if request.method == "POST":
        data = request.get_json()
        if act == "ingredients":
            try:
                if not data.get("category"):
                    data["category"] = "null"
                if not data.get("type"):
                    data["type"] = "null"
                if not data.get("requirement"):
                    data["requirement"] = "null"
                if not data.get("size"):
                    data["size"] = "null"
                Ingredient.create(food_id=key,
                                  category=data["category"],
                                  name=data["name"],
                                  quantity=data["quantity"],
                                  ingredient_type=data["type"],
                                  requirement=data["requirement"],
                                  size=data["size"])
                return jsonify({"status": "success", "data": data}), 201
            except:
                return jsonify({
                    "status": "error",
                    "error": {
                        "Keys(in this order)": [
                            "category(optional)", "name(important)",
                            "quantity(important)", "type(optional)",
                            "requirement(optional)", "size(optional)"]}
                }), 404
        elif act == "steps":
            try:
                if not data.get("category"):
                    data["category"] = "null"
                if not data.get("name"):
                    data["name"] = "null"
                if not data.get("image"):
                    data["image"] = "null"
                Step.create(food_id=key,
                            category=data["category"],
                            name=data["name"],
                            action=data["action"],
                            image=data["image"])
                return jsonify({"status": "success", "data": data}), 201
            except:
                return jsonify({
                    "status": "error",
                    "error": { "Keys(in this order)": [
                            "category(optional)", "name(optional)",
                            "action(important)", "image(optional)"]}}), 404
        else:
            return jsonify({
                "status": "error",
                "Key Error": "Act available in database: steps and ingredients"})
    else:
        if act == "ingredients":
            query = Ingredient.select().where(Ingredient.food_id == key)
            step_ingre = model_to_dict(query.get(), recurse=False, backrefs=True)
        elif act == "steps":
            query = Step.select().where(Step.food_id == key)
            step_ingre = model_to_dict(query.get(), recurse=False, backrefs=True)
        else:
            return jsonify({
                "status": "error",
                "Key Error": "Act available in database: steps and ingredients"})
        return jsonify({"status": "success", f"{act}": step_ingre}), 201


@app.route("/recipies/<act>/<id_number>", methods=["PUT", "DELETE"])
def update_act(act, id_number):
    if request.method == "PUT":
        data = request.get_json()
        if act == "ingredients":
            if not data.get("category"):
                data["category"] = "null"
            if not data.get("type"):
                data["type"] = "null"
            if not data.get("requirement"):
                data["requirement"] = "null"
            if not data.get("size"):
                data["size"] = "null"
            update_data = Ingredient.update(
                category=data["category"],
                name=data["name"],
                quantity=data["quantity"],
                ingredient_type=data["type"],
                requirement=data["requirement"],
                size=data["size"]).where(Ingredient.id == id_number)
            update_data.execute()
            return jsonify({"status": "success", "data": data}), 201
        elif act == "steps":
            if not data.get("category"):
                data["category"] = "null"
            if not data.get("name"):
                data["name"] = "null"
            if not data.get("image"):
                data["image"] = "null"
            update_data = Step.update(category=data["category"],
                        name=data["name"],
                        action=data["action"],
                        image=data["image"]).where(Step.id == id_number)
            update_data.execute()
            return jsonify({"status": "success", "data": data}), 201
        else:
            return jsonify({
                "status": "error",
                "Key Error": "Act available in database: steps and ingredients"})
    elif request.method == "DELETE":
        if act == "ingredients":
            ingredient = Ingredient.get(Ingredient.id == id_number)
            ingredient.delete_instance()
            return jsonify({
                "status": "success",
                "data": (Ingredient.get_or_none(Ingredient.id == id_number))}), 201
        elif act == "steps":
            step = Step.get(Step.id == id_number)
            step.delete_instance()
            return jsonify({
                "status": "success",
                "data": Step.get_or_none(Step.id == id_number)}), 201
        else:
            return jsonify({
                "status": "error",
                "Key Error": "Act available in database: steps and ingredients"})


if __name__ == "__main__":
    app.run()
