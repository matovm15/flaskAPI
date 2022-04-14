from flask import Flask, request, Response, jsonify

app = Flask(__name__)
app.debug = True

# a class acting as a blue print for all to-do items
class Item:
    id = ""
    title = ""
    desc = ""

    def __init__(self, id, title, desc):
        self.id = id
        self.title = title
        self.desc = desc

    def toJson(self):
        in_json = {"id":self.id, "title":self.title, "desc":self.desc}
        return in_json

    def toJson2(self):
        return self.__dict__

# an empty list to store our todos
toDoList = []

# append todos to an empty list
item1 = Item(id="1", title="RestFul API", desc="Build a Restful API with Flask")

item2 = Item(id="2", title="Delpoyment", desc="Deploy the Flask API on Heroku")

# change app data to json format
toDoList.append(item1.toJson())
toDoList.append(item2.toJson())


# /todo/list endpoint - returns all items in our todo (GET REQUEST)

@app.route("/todo/list")
def getAllTodos():
    return jsonify(toDoList) # convert item object to JSON and add it to todo list

# /todo/list endpoint - adds a new item in our todo list (POST REQUEST)
@app.route("/todo", methods=["POST"]) 
def createNewTodoItem():
    item = Item(**request.get_json())
    toDoList.append(item.toJson())
    return Response('{"message":"success"}', status=201, mimetype='application/json')

# /todo/list/{id} endpoint - returns specific todo item by it's id (GET REQUEST)
@app.route("/todo/<id>")
def getTodoItembyId(id):
    receivedId = None
    for item in toDoList:
        if item["id"] == id:
            receivedId = item
        else:
            continue
    if receivedId == None:
        return Response('{"message":"Item not found"}', status=404, mimetype='application/json')
    else:
        response = jsonify(receivedId)
        response.status_code = 200
        return response

# This endpoint update a todo item based on it's id (PUT REQUEST)
@app.route("/todo", methods=["PUT"])
def updateTodoItem():
    item = Item(**request.get_json())
    itemExist = False
    for i in toDoList:
        if i["id"] == item.id:
            i["title"] = item.title
            i["desc"] = item.desc
            itemExist = True
            break
    if itemExist:
        response = jsonify({"message":"item updated succesfully"})
        response.status_code = 201
        return response
    else:
        response = jsonify({"message":"An Error Ocurred"})
        response.status_code = 404
        return response

# This endpoint deletes a todo item based on it's id (DELETE REQUEST)
@app.route("/todo/<id>", methods=["DELETE"])
def deleteToDoItemById(id):
    itemToDelete = None
    for item in toDoList:
        if item["id"] == id:
            itemToDelete = item
        else:
            continue
    if itemToDelete == None:
        response = jsonify({"message":"item does not exist"})
        response.status_code = 404
        return response
    else:
        toDoList.remove(itemToDelete)
        response = jsonify({"message":"item succesfully removed"})
        response.status_code = 200
        return response

        
if __name__ == "__main__":
    app.run()