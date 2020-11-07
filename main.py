from flask import Flask, jsonify, send_file
import json

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World"


@app.route("/selfie", methods=["GET"])
def selfie():
    return send_file("pictures/screenshot.jpeg", mimetype="image/jpeg")


@app.route("/recipies", methods=["GET"])
def recipies():
    food = ["Ewedu Soup = ewedu_soup", "African Salad - Abacha and Ugba = african_salad", "Tuwo Shinkafa = tuwo_shinkafa",
            "Classic Hamburger = classic_hamburger", "Pizza = pizza", "Pancakes and Scrambled Eggs = pancakes_and_scrambled_eggs",
            "Shawarma = shawarma", "Small Chops = small_chops"]  
    with open("files/cippe.json", "r") as items: 
        return jsonify({"status": "success", "data": json.load(items)})


@app.route("/recipies/<name>", methods=["GET"])
def get_recipie(name):
    with open("files/{}.json".format(name), "r") as food:
        return jsonify({"status": "success", "data": json.load(food)})


@app.route("/recipies/small_chops/<name>", methods=["GET"])
def get_small_chops_recipie(name):
    with open("files/small_chops/{}.json".format(name), "r") as food:
        return jsonify({"status": "success", "data": json.load(food)})


@app.route("/recipies/pancakes_and_scrambled_eggs/<name>", methods=["GET"])
def get_pancakes_and_scrambled_eggs_recipie(name):
    with open("files/pancakes_and_scrambled_eggs/{}.json".format(name), "r") as food:
        return jsonify({"status": "success", "data": json.load(food)})


if __name__ == "__main__":
    app.run()
