# Flask server for project 
# Taking in data from dao and posting to a mysql database correctly. 
# All these calls work- could add some more such as delete by name/driver_id, update by driver id etc 

# 

# https://stackoverflow.com/questions/48008184/method-object-is-not-json-serializable

from flask import Flask, url_for,request,redirect,abort,jsonify, session
from dao_f1driver import DriverDAO as dao
app = Flask(__name__, static_url_path = "", static_folder = "staticpages")
# messing with sessions



# Send to home page
@app.route("/")
def index():
    return app.send_static_file("drivers.html")

# Get all data from the database
@app.route('/drivers')
def getAll():
    return jsonify(dao.getAll())

# Get a specific driver from the database
@app.route("/drivers/<id>")
def findByID(id):
    return jsonify(dao.findById(id))


# adding a new driver to the database
@app.route('/drivers', methods=['POST'])
def createdriver():
    if not request.json:
        abort(400)
    data = {
        "DriverNo":request.json["DriverNo"],
        "LastName":request.json["LastName"],
        "FirstName":request.json["FirstName"],
        "Nationality":request.json["Nationality"],
        "CurrentTeam":request.json["CurrentTeam"],

    }
    return jsonify(dao.create(data))


# update database from the webpage
@app.route('/drivers/<id>', methods = ['PUT'])
def update(id):
    foundDriver = dao.findById(id)
    print(foundDriver)
    if len(foundDriver) == 0:
        return jsonify ({}), 404
    currentDriver = foundDriver
    if "DriverNo" in request.json:
        currentDriver["DriverNo"] = request.json["DriverNo"]
    if "LastName" in request.json:
        currentDriver["LastName"] = request.json["LastName"]
    if "FirstName" in request.json:
        currentDriver["FirstName"] = request.json["FirstName"]
    if "Nationality" in request.json:
        currentDriver["Nationality"] = request.json["Nationality"]
    if "CurrentTeam" in request.json:
        currentDriver["CurrentTeam"] = request.json["CurrentTeam"]
   
    dao.update(currentDriver)
    return jsonify(currentDriver)


# delete by id
@app.route('/drivers/<id>', methods = ['DELETE'])
def delete(id):
    foundDriver = dao.findById(id)
    print(foundDriver)
    if len(foundDriver) == 0:
        return jsonify ({}), 404
    dao.delete(id)
    return jsonify({"done":True})






if __name__ == "__main__":
    
    app.run(debug=True)