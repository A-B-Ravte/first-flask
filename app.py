from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

@app.route("/")
def hello_world():
    return f"<h1>Hellow World !!<h1"

@app.route("/api/status")
def get_status():
    data = {
            "status": "success",
            "message": "API is running",
            "version": 1.0
        }
    return jsonify(data)

# Define a route for the "/no_content" URL
@app.route("/no_content")
def no_content():
    """Return 'no content found' with a status of 204.
    Returns:
        tuple: A tuple containing a dictionary and a status code.
    """
    # Create a dictionary with a message and return it with a 204 No Content status code
    return ({"message": "No content found"}, 204)
# Define a route for the "/exp" URL
@app.route("/exp")
def index_explicit():
    """Return 'Hello World' message with a status code of 200.
    Returns:
        response: A response object containing the message and status code 200.
    """
    # Create a response object with the message "Hello World"
    resp = make_response({"message": "Hello World"})
    # Set the status code of the response to 200
    #resp.status_code = 200
    # Return the response object
    return resp

@app.route("/name_search")
def name_search():

    query = request.args.get("q")

    if query is None:
        return {"message": "Query parameter 'q' is missing"}, 400
    
    if query.strip() == "" or query.isdigit():
        return {"message": "Invalid input parameter"}, 422
    
    for person in data:
        if query.lower() in  person["first_name"].lower():
            return person, 200  
    return {"message": "Person not found"}, 404    

@app.route("/count")
def count():
    try:
        return {"count":len(data)}, 200
    
    except NameError:
        return {"message":"Data not defined"}, 500

@app.route("/person/<uuid:id>")    
def find_by_id(id):    
    for person in data:
        print(f"person id is {person["id"]}")
        print(f"url id is {id}")
        if person["id"] == str(id):
            return person, 200
        
    return {"message":"something went wrong"}

@app.route("/remove/<uuid:id>")    
def remove_by_id(id):    
    for person in data:
        
        if person["id"] == str(id):
            data.remove(person)
            return {"Messeage":"Successfully removed"}, 200
        
    return {"message":"something went wrong"}

@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    # code to validate new_person ommited
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": f"{new_person['id']}"}, 200

@app.route("/data")
def get_data():
    return data, 200

@app.errorhandler(404)
def api_not_found(error):
    # This function is a custom error handler for 404 Not Found errors
    # It is triggered whenever a 404 error occurs within the Flask application
    return {"message": "API not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)