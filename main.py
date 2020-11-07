from flask import Flask, jsonify, send_file

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World"


@app.route("/selfie", methods=["GET"])
def selfie():
    return send_file("pictures/screenshot.jpeg", mimetype="image/jpeg")


@app.route("/recipies", methods=["GET"])
def recipies():
    food = ["Ewedu Soup", "African Salad - Abacha and Ugba", "Tuwo Shinkafa",
            "Classic Hamburger", "Pizza", "Pancakes and Scrambled Eggs",
            "Shawarma", "Small Chops"]
    return jsonify({"status": "success", "data": food})


if __name__ == "__main__":
    app.run()
