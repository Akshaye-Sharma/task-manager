from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="manager",
    user="akshayesharma",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id" : user_id,
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    return jsonify(data), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    cursor.execute("SELECT description FROM tasks")
    rows = cursor.fetchall()
    print("PRINTED HERE: "+str(rows))
    if not rows:
        return "No tasks found."
    else:
        result = ""
        for i in range(len(rows)):
            result += str(i+1) + " " + rows[0][0]
            return jsonify(result)
        #return jsonify([{"id": row, "description": row[0]} for row in rows])


if __name__ == "__main__":
    app.run(debug=True)