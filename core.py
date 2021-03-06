import sqlite3
import json
from utils.escape import quote_identifier


db = sqlite3.connect("cippedb.db")

def drop_table():
    db.execute("DROP TABLE recipies") #if table exist
    db.execute("DROP TABLE ingredients") # if table exist
    db.execute("DROP TABLE steps") 
    db.commit()


def create_table():
    db.execute(
        "CREATE TABLE IF NOT EXISTS recipies (id INTEGER PRIMARY KEY AUTOINCREMENT, food_name TEXT NOT NULL, description "
        "TEXT NOT NULL, top_image TEXT NOT NULL, bottom_image TEXT NOT NULL)")

    db.execute(
        "CREATE TABLE IF NOT EXISTS ingredients (id INTEGER PRIMARY KEY AUTOINCREMENT, food_id INTEGER NOT NULL, "
        "category TEXT, name TEXT, quantity TEXT, ingredient_type TEXT, requirement TEXT, size TEXT, FOREIGN KEY (food_id) "
        "REFERENCES recipies (id))")

    db.execute(
        "CREATE TABLE IF NOT EXISTS steps (id INTEGER PRIMARY KEY AUTOINCREMENT, food_id INTEGER NOT NULL, category TEXT, "
        "name TEXT, action TEXT, image TEXT, FOREIGN KEY (food_id) REFERENCES recipies (id))")
    db.commit()


def get_ingredients(food, count):
    """
    gets the ingredients from each food's Json file

    :param food: The json file
    :param count:the index for foreign key
    """
    ingredients = food["ingredients"]
    for item in ingredients:
        if type(item) is dict:
            if item.get("name"):
                named = item["name"]
                if item.get("quantity"):
                    quantity = ""
                    if type(item["quantity"]) is list:
                        for char in item["quantity"]:
                            quantity += char.strip("],['")
                    else:
                        quantity = str(item["quantity"])
                # else:
                #     quantity = ""
                if item.get("ingredient_type"):
                    if type(item["ingredient_type"]) is list:
                        types = ""
                        for char in item["ingredient_type"]:
                            types += (str(char).strip("{][}'"))
                        types = types.replace(":", " = ")
                        types = types.replace("'", "")
                    else:
                        types = item["ingredient_type"]
                else:
                    types = ""
                if item.get("requirement"):
                    requirement = item["requirement"]
                else:
                    requirement = ""
                if item.get("size"):
                    size = item["size"]
                else:
                    size = ""
                db.execute(
                    "INSERT INTO ingredients(food_id, name, quantity, ingredient_type, requirement, size) VALUES('{0}', '{1}', "
                    "'{2}', {3}, '{4}', '{5}') "
                        .format(count, named, quantity, quote_identifier(types), requirement, size))

            else:
                for key in item.keys():
                    for names in item[key]:
                        if type(names) is dict:
                            if names.get("name"):
                                named = names["name"]
                                if names.get("quantity"):
                                    quantity = names["quantity"]
                                # else:
                                #     quantity = ""
                                if names.get("ingredient_type"):
                                    types = names["ingredient_type"]
                                else:
                                    types = ""
                                if names.get("requirement"):
                                    requirement = names["requirement"]
                                else:
                                    requirement = ""
                                if names.get("size"):
                                    size = names["size"]
                                else:
                                    size = ""
                                db.execute(
                                    "INSERT INTO ingredients VALUES(NULL, {0}, '{5}', {6}, '{1}', '{2}', '{3}', '{4}')"
                                        .format(count, quantity, types, requirement, size, key,
                                                quote_identifier(named)))
                            else:
                                for topping in names:
                                    name = str(names[topping]).replace("],[", "")
                                    category = key + ": " + topping
                                    db.execute(
                                        "INSERT INTO ingredients(food_id, category, name) VALUES('{0}', {1}, {2})"
                                            .format(count, quote_identifier(category), quote_identifier(name)))

                        else:
                            db.execute(
                                "INSERT INTO ingredients(food_id, category, name) VALUES('{0}', '{2}', '{1}')"
                                    .format(count, names, key))

        else:
            db.execute(
                "INSERT INTO ingredients(food_id, name) VALUES('{0}', '{1}')"
                    .format(count, item))
    db.commit()


def get_steps(food, count):
    """
    gets the steps from each food's Json file

    :param food: The json file
    :param count:the index for foreign key
    """
    steps = food["steps"]
    for item in steps:
        if type(item) is dict:
            if item.get("action"):
                action = item["action"]
                if item.get("image"):
                    if type(item["image"]) is list:
                        image = ""
                        for char in item["image"]:
                            image += str(char) + " , "
                    else:
                        image = str(item["image"])
                # else:
                #     image = ""
                if item.get("name"):
                    name = item["name"]
                else:
                    name = ""
                db.execute(
                    "INSERT INTO steps VALUES(NULL, '{0}', '', '{1}', {2}, '{3}')"
                        .format(count, name, quote_identifier(action), image))

            elif item.get("description"):
                pass

            else:
                for key in item.keys():
                    for names in item[key]:
                        if type(names) is dict:
                            if names.get("name"):
                                name = names["name"]
                                action = names["action"]
                                if names.get("image"):
                                    image = names["image"]
                                # else:
                                    # image = ""
                                db.execute(
                                    "INSERT INTO steps VALUES(NULL, {0}, {1}, {2}, {3}, {4})"
                                        .format(count, (item + names), name, action,
                                                image))

                            elif names.get("action"):
                                if type(names["action"]) is list:
                                    action = ""
                                    for char in names["action"]:
                                        action += str(char)
                                else:
                                    action = names["action"]
                                if names.get("image"):
                                    if type(names["image"]) is list:
                                        image = ""
                                        for char in names["image"]:
                                            image += str(char) + " , "
                                    else:
                                        image = str(names["image"])
                                # else:
                                #     image = "NULL"
                                db.execute(
                                    "INSERT INTO steps(food_id, category, action, image) VALUES('{0}', '{1}', '{2}', "
                                    "'{3}') ".format(count, key, action, image))

                            else:
                                for keys in names.keys():
                                    for its in names[keys]:
                                        if type(its) is dict:
                                            if its.get("name"):
                                                name = its["name"]
                                            # else:
                                            #     name = "NULL"
                                            if its.get("action"):
                                                action = its["action"]
                                            if its.get("image"):
                                                if type(its["image"]) is list:
                                                    image = ""
                                                    for char in its["image"]:
                                                        image += str(
                                                            char) + " , "
                                                else:
                                                    image = str(its["image"])
                                            # else:
                                            #     image = "NULL"
                                            category = key + ": " + keys
                                            db.execute(
                                                "INSERT INTO steps VALUES(NULL, '{0}', '{1}', '{2}', {3}, '{4}')"
                                                    .format(count, quote_identifier(category), name,
                                                            quote_identifier(action), image))

                        else:
                            db.execute(
                                "INSERT INTO steps(food_id, category, action) VALUES('{0}', '{1}', {2})"
                                    .format(count, key, quote_identifier(names)))

        else:
            db.execute(
                "INSERT INTO steps(food_id, action) VALUES('{0}', {1})".format(
                    count, quote_identifier(item)))
    db.commit()


def add_data():
    for index, items in enumerate([
            "african_salad", "classic_hamburger", "ewedu_soup", "pizza",
            "shawarma", "tuwo_shinkafa"]):
        with open("files/{}.json".format(items), "r") as data_file:
            food = json.load(data_file)
            db.execute("INSERT INTO recipies VALUES(NULL, '{0}', '{1}', '{2}', '{3}')".format(
                food["name"], food["description"], food["top image"], food["bottom image"]))
            db.commit()
            count = (index + 1)

            get_ingredients(food, count)
            get_steps(food, count)

    for index, item in enumerate(["pancakes", "scrambled_eggs"]):
        with open("files/pancakes_and_scrambled_eggs/{}.json".format(item),
                "r") as data_file:
            food = json.load(data_file)
            db.execute("INSERT INTO recipies VALUES(NULL, {0}, {1}, '{2}', '{3}')".format(
                quote_identifier(food["name"]), quote_identifier(food["description"]), 
                food["top image"], food["bottom image"]))
            db.commit()

            count = (index + 7)
            get_ingredients(food, count)
            get_steps(food, count)

    for index, item in enumerate(["mosa", "puff_puff", "samosa", "spring_roll"]):
        with open("files/small_chops/{}.json".format(item), "r") as data_file:
            food = json.load(data_file)
            db.execute("INSERT INTO recipies VALUES(NULL, {0}, {1}, '{2}', '{3}')".format(
                quote_identifier(food["name"]), quote_identifier(food["description"]), 
                food["top image"], food["bottom image"]))
            db.commit()

            count = (index + 9)
            get_ingredients(food, count)
            get_steps(food, count)

# db.close()
