import sqlite3
import json
from utils.escape import quote_identifier

db = sqlite3.connect("cippe.db")
db.execute("DROP TABLE recipies")
db.execute("CREATE TABLE IF NOT EXISTS recipies (id INTEGER PRIMARY KEY AUTOINCREMENT, food_name TEXT NOT NULL, description TEXT NOT NULL)")
db.execute("DROP TABLE ingredients")
db.execute(
    "CREATE TABLE IF NOT EXISTS ingredients (id INTEGER PRIMARY KEY AUTOINCREMENT, food_id INTEGER NOT NULL, category TEXT, name TEXT, quantity TEXT, type TEXT, requirement TEXT, size TEXT, FOREIGN KEY (food_id) REFERENCES recipies (id))"
)
db.execute("DROP TABLE steps")
db.execute("CREATE TABLE IF NOT EXISTS steps (id INTEGER PRIMARY KEY AUTOINCREMENT, food_id INTEGER NOT NULL, category TEXT, name TEXT, action TEXT, image TEXT, FOREIGN KEY (food_id) REFERENCES recipies (id))")

db.commit()

for index, items in enumerate(["african_salad", "classic_hamburger", "ewedu_soup", "pizza", "shawarma", "tuwo_shinkafa"]):
    with open("files/{}.json".format(items), "r") as data_file:
        food = json.load(data_file)
        db.execute("INSERT INTO recipies VALUES(NULL, '{0}', '{1}')".format(food["name"], food["description"]))

        ingredients = food["ingredients"]
        for item in ingredients:
            if type(item) is dict:
                if item.get("name"):
                    name = item["name"]
                    if item.get("quantity"):
                        quantity = item["quantity"]
                    else:
                        quantity = "NULL"
                    if item.get("type"):
                        types = item["type"]
                    else:
                        types = "NULL"
                    if item.get("requirement"):
                        requirement = item["requirement"]
                    else:
                        requirement = "NULL"
                    if item.get("size"):
                        size = item["size"]
                    else:
                        size = "NULL"
                    db.execute("INSERT INTO ingredients VALUES(NULL, {0}, NULL, '{1}', '{2}', '{3}', '{4}', '{5}')".format(index + 1, name, quantity, types, requirement, size))

                else:
                    for key in item.keys():
                        for names in item[key]:
                            if type(names) is dict:
                                if names.get("name"):
                                    named = names["name"]
                                else:
                                    named = "NULL"
                                if names.get("quantity"):
                                    quantity = names["quantity"]
                                else:
                                    quantity = "NULL"
                                if names.get("type"):
                                    types = names["type"]
                                else:
                                    types = "NULL"
                                if names.get("requirement"):
                                    requirement = names["requirement"]
                                else:
                                    requirement = "NULL"
                                if names.get("size"):
                                    size = names["size"]
                                else:
                                    size = "NULL" 
                                db.execute("INSERT INTO ingredients VALUES(NULL, '{0}', '{5}', '{6}', '{1}', '{2}', '{3}', '{4}')".format(index + 1, quantity, types, requirement, size, key, named))

                            else:
                                db.execute("INSERT INTO ingredients(id, food_id, category, name) VALUES(NULL, '{0}', '{2}', '{1}')".format(index + 1, names, key))

            else: 
                db.execute("INSERT INTO ingredients(id, food_id, name) VALUES(NULL, {0}, {1})".format(index + 1, item))

        
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
                    else:
                        image = "NULL"
                    if item.get("name"):
                        name = item["name"]
                    else: 
                        name = "NULL"
                    db.execute("INSERT INTO steps VALUES(NULL, '{0}', NULL, '{1}', {2}, '{3}')".format(index +1, name, quote_identifier(action), image))

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
                                    else:
                                        image = "NULL"
                                    db.execute("INSERT INTO steps VALUES(NULL, {0}, {1}, {2}, {3}, {4})".format(index +1, (item, names), name, action, image))    

                                elif names.get("action"):
                                    action = names["action"]
                                    if names.get("image"):
                                        if type(names["image"]) is list:
                                            image = ""
                                            for char in names["image"]:
                                                image += str(char) + " , " 
                                        else:
                                            image = str(names["image"])
                                    else: 
                                        image = "NULL"
                                    db.execute("INSERT INTO steps(food_id, category, action, image) VALUES('{0}', '{1}', '{2}', '{3}')".format(index +1, key, action, image))    

                                else:
                                    for keys in names.keys():
                                        for its in names[keys]:
                                            if type(its) is dict:
                                                if its.get("name"):
                                                    name = its["name"]
                                                else: 
                                                    name = "NULL"
                                                if its.get("action"):
                                                    action = its["action"]
                                                if its.get("image"):
                                                    if type(its["image"]) is list:
                                                        image = ""
                                                        for char in its["image"]:
                                                            image += str(char) + " , " 
                                                    else:
                                                        image = str(its["image"])  
                                                else:
                                                    image = "NULL"   
                                                category = key + ": " + keys
                                                db.execute("INSERT INTO steps VALUES(NULL, '{0}', '{1}', '{2}', {3}, '{4}')".format(index +1, quote_identifier(category), name, quote_identifier(action), image))   

                            else:
                                db.execute("INSERT INTO steps(food_id, category, action) VALUES('{0}', '{1}', {2})".format(index +1, key, quote_identifier(names)))        

            else:
                db.execute("INSERT INTO steps(food_id, action) VALUES('{0}', {1})".format(index +1, quote_identifier(item))) 
db.commit()                                  


for index, item in enumerate(["pancakes", "scrambled_eggs"]):     
    with open("files/pancakes_and_scrambled_eggs/{}.json".format(item), "r") as data_file:
        food = json.load(data_file)
        db.execute("INSERT INTO recipies VALUES(NULL, {0}, {1})".format(quote_identifier(food["name"]), quote_identifier(food["description"])))

        ingredients = food["ingredients"]
        for item in ingredients:
            if type(item) is dict:
                if item.get("name"):
                    named = item["name"]
                    if item.get("quantity"):
                        quantity = item["quantity"]
                    else:
                        quantity = "NULL"
                    if item.get("type"):
                        types = ""
                        if type(item["type"]) is list:
                            for char in item["type"]:
                                types += str(char).strip("{][}'")
                            types = types.replace(":", "=")
                            types = types.replace("'", "")
                        else:
                            types = item["type"]
                    else:
                        types = "NULL"
                    if item.get("requirement"):
                        requirement = item["requirement"]
                    else:
                        requirement = "NULL"
                    if item.get("size"):
                        size = item["size"]
                    else:
                        size = "NULL"
                    db.execute("INSERT INTO ingredients(food_id, name, quantity, type, requirement, size) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(index + 7, named, quantity, quote_identifier(types), requirement, size))

                else:
                    for key in item.keys():
                        for names in item[key]:
                            if type(names) is dict:
                                if names.get("name"):
                                    named = names["name"]
                                else:
                                    named = "NULL"
                                if names.get("quantity"):
                                    quantity = names["quantity"]
                                else:
                                    quantity = "NULL"
                                if names.get("type"):
                                    types = names["type"]
                                else:
                                    types = "NULL"
                                if names.get("requirement"):
                                    requirement = names["requirement"]
                                else:
                                    requirement = "NULL"
                                if names.get("size"):
                                    size = names["size"]
                                else:
                                    size = "NULL" 
                                db.execute("INSERT INTO ingredients VALUES(NULL, '{0}', '{5}', '{6}', '{1}', '{2}', '{3}', '{4}')".format(index + 7, quantity, types, requirement, size, key, named))

                            else:
                                db.execute("INSERT INTO ingredients(id, food_id, category, name) VALUES(NULL, '{0}', '{2}', '{1}')".format(index + 7, names, key))

            else: 
                db.execute("INSERT INTO ingredients(id, food_id, name) VALUES(NULL, '{0}', '{1}')".format(index + 7, item))
                

        steps = food["steps"]
        for item in steps:
            if type(item) is dict:
                if item.get("action"):
                    action = item["action"]
                    if item.get("image"):
                        if type(item["image"]) is list:
                            image = ""
                            for char in item["image"]:
                                image += str(char)+ " , " 
                        else:
                            image = str(item["image"])
                    else:
                        image = "NULL"
                    if item.get("name"):
                        name = item["name"]
                    else: 
                        name = "NULL"
                    db.execute("INSERT INTO steps VALUES(NULL, '{0}', NULL, '{1}', {2}, '{3}')".format(index +7, name, quote_identifier(action), image))

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
                                    else:
                                        image = "NULL"
                                    db.execute("INSERT INTO steps VALUES(NULL, {0}, {1}, {2}, {3}, {4})".format(index +7, (item, names), name, action, image))    

                                elif names.get("action"):
                                    action = names["action"]
                                    if names.get("image"):
                                        if type(names["image"]) is list:
                                            image = ""
                                            for char in names["image"]:
                                                image += str(char)+ " , " 
                                        else:
                                            image = str(names["image"])
                                    else: 
                                        image = "NULL"
                                    db.execute("INSERT INTO steps(food_id, category, action, image) VALUES('{0}', '{1}', '{2}', '{3}')".format(index +7, key, action, image))    

                                else:
                                    for keys in names.keys():
                                        for its in names[keys]:
                                            if type(its) is dict:
                                                if its.get("name"):
                                                    name = its["name"]
                                                else: 
                                                    name = "NULL"
                                                if its.get("action"):
                                                    action = its["action"]
                                                if its.get("image"):
                                                    if type(its["image"]) is list:
                                                        image = ""
                                                        for char in its["image"]:
                                                            image += str(char)+ " , " 
                                                    else:
                                                        image = str(its["image"])  
                                                else:
                                                    image = "NULL"   
                                                category = key + ": " + keys
                                                db.execute("INSERT INTO steps VALUES(NULL, '{0}', '{1}', '{2}', {3}, '{4}')".format(index + 7, quote_identifier(category), name, quote_identifier(action), image))   

                            else:
                                db.execute("INSERT INTO steps(food_id, category, action) VALUES('{0}', '{1}', {2})".format(index +7, key, quote_identifier(names)))        

            else:
                db.execute("INSERT INTO steps(food_id, action) VALUES('{0}', {1})".format(index +1, quote_identifier(item))) 
db.commit()


for index, item in enumerate(["mosa", "puff_puff", "samosa", "spring_roll"]):
    with open("files/small_chops/{}.json".format(item), "r") as data_file:
        food = json.load(data_file)
        db.execute("INSERT INTO recipies VALUES(NULL, {0}, {1})".format(quote_identifier(food["name"]), quote_identifier(food["description"])))

        ingredients = food["ingredients"]
        for item in ingredients:
            if type(item) is dict:
                if item.get("name"):
                    name = item["name"]
                    if item.get("quantity"):
                        quantity = ""
                        if type(item["quantity"]) is list:
                            for char in item["quantity"]:
                                quantity += char.strip("],['")
                        else:
                            quantity = str(item["quantity"])
                    else:
                        quantity = "NULL"
                    if item.get("type"):
                        types = item["type"]
                    else:
                        types = "NULL"
                    if item.get("requirement"):
                        requirement = item["requirement"]
                    else:
                        requirement = "NULL"
                    if item.get("size"):
                        size = item["size"]
                    else:
                        size = "NULL"
                    db.execute("INSERT INTO ingredients(food_id, name, quantity, type, requirement, size) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(index + 9, name, quantity, types, requirement, size))

                else:
                    for key in item.keys():
                        for names in item[key]:
                            if type(names) is dict:
                                if names.get("name"):
                                    named = names["name"]
                                else:
                                    named = "NULL"
                                if names.get("quantity"):
                                    quantity = names["quantity"]
                                else:
                                    quantity = "NULL"
                                if names.get("type"):
                                    types = names["type"]
                                else:
                                    types = "NULL"
                                if names.get("requirement"):
                                    requirement = names["requirement"]
                                else:
                                    requirement = "NULL"
                                if names.get("size"):
                                    size = names["size"]
                                else:
                                    size = "NULL" 
                                db.execute("INSERT INTO ingredients VALUES(NULL, '{0}', '{5}', '{6}', '{1}', '{2}', '{3}', '{4}')".format(index + 9, quantity, types, requirement, size, key, named))
                            else:
                                db.execute("INSERT INTO ingredients(id, food_id, category, name) VALUES(NULL, '{0}', '{2}', '{1}')".format(index + 9, names, key))
            else: 
                db.execute("INSERT INTO ingredients(id, food_id, name) VALUES(NULL, {0}, {1})".format(index + 7, item))

        steps = food["steps"]
        for item in steps:
            if type(item) is dict:
                if item.get("action"):
                    action = item["action"]
                    if item.get("image"):
                        if type(item["image"]) is list:
                            image = ""
                            for char in item["image"]:
                                image += str(char)+ " , " 
                        else:
                            image = str(item["image"])
                    else:
                        image = "NULL"
                    if item.get("name"):
                        name = item["name"]
                    else: 
                        name = "NULL"
                    db.execute("INSERT INTO steps VALUES(NULL, '{0}', NULL, '{1}', {2}, '{3}')".format(index +9, name, quote_identifier(action), image))

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
                                    else:
                                        image = "NULL"
                                    db.execute("INSERT INTO steps VALUES(NULL, {0}, {1}, {2}, {3}, {4})".format(index +9, (item, names), name, action, image))    

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
                                                image += str(char)+ " , " 
                                        else:
                                            image = str(names["image"])
                                    else: 
                                        image = "NULL"
                                    db.execute("INSERT INTO steps(food_id, category, action, image) VALUES('{0}', '{1}', '{2}', '{3}')".format(index +9, key, action, image))    

                                else:
                                    for keys in names.keys():
                                        for its in names[keys]:
                                            if type(its) is dict:
                                                if its.get("name"):
                                                    name = its["name"]
                                                else: 
                                                    name = "NULL"
                                                if its.get("action"):
                                                    action = its["action"]
                                                if its.get("image"):
                                                    if type(its["image"]) is list:
                                                        image = ""
                                                        for char in its["image"]:
                                                            image += str(char)+ " , " 
                                                    else:
                                                        image = str(its["image"])  
                                                else:
                                                    image = "NULL"   
                                                category = key + ": " + keys
                                                db.execute("INSERT INTO steps VALUES(NULL, '{0}', '{1}', '{2}', {3}, '{4}')".format(index +9, quote_identifier(category), name, quote_identifier(action), image))   

                            else:
                                db.execute("INSERT INTO steps(food_id, category, action) VALUES('{0}', '{1}', {2})".format(index +9, key, quote_identifier(names)))        

            else:
                db.execute("INSERT INTO steps(food_id, action) VALUES('{0}', {1})".format(index +1, quote_identifier(item)))   
db.commit()                         
