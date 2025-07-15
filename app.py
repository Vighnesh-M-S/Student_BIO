from flask import Flask, request, jsonify
import threading
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

students = {}
student_id_counter = 1
lock = threading.Lock()

@app.route("/")
def home():
    return "API is working!"

@app.route("/students", methods=["POST"])
def create_student():
    global student_id_counter
    data = request.json
    if not data or not all(k in data for k in ("name", "age", "email")):
        return jsonify({"error": "Missing student data"}), 400

    with lock:
        student_id = student_id_counter
        students[student_id] = {
            "id": student_id,
            "name": data["name"],
            "age": data["age"],
            "email": data["email"]
        }
        student_id_counter += 1

    return jsonify(students[student_id]), 201

@app.route("/students", methods=["GET"])
def get_all_students():
    return jsonify(list(students.values()))

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = students.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    with lock:
        student = students[student_id]
        student["name"] = data.get("name", student["name"])
        student["age"] = data.get("age", student["age"])
        student["email"] = data.get("email", student["email"])

    return jsonify(student)

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    with lock:
        if student_id not in students:
            return jsonify({"error": "Student not found"}), 404
        del students[student_id]
    return jsonify({"message": "Student deleted"})



if __name__ == "__main__":
    app.run(debug=True)
