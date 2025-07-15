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

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b" 

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

@app.route("/students/<int:student_id>/summary", methods=["GET"])
def summarize_student(student_id):
    student = students.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    prompt = f"""
    Summarize the following student in 2-3 professional sentences.
    Only output the summary. Do not ask any questions or provide options.

    Name: {student['name']}
    Age: {student['age']}
    Email: {student['email']}
    """

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        result = response.json()
        return jsonify({"summary": result["response"].strip()})
    except requests.RequestException as e:
        return jsonify({"error": "Failed to generate summary", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
