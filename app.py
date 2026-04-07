from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)
TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Task text is required"}), 400
    tasks = load_tasks()
    task = {"id": int(__import__("time").time() * 1000), "text": text, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Task text is required"}), 400
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["text"] = text
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
