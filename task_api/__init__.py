"""Tiny educational task manager API for a DevSecOps CI demonstration."""

from itertools import count

from flask import Flask, jsonify, render_template, request


def create_app() -> Flask:
    """Create an isolated application instance with in-memory demo tasks."""
    app = Flask(__name__)
    tasks: dict[int, dict] = {}
    next_task_id = count(1)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"service": "TaskFlow Demo", "status": "ok"})

    @app.get("/api/tasks")
    def list_tasks():
        return jsonify({"tasks": list(tasks.values())})

    @app.post("/api/tasks")
    def add_task():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Send a JSON object."}), 400

        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "A non-empty title is required."}), 400
        title = title.strip()
        if len(title) > 80:
            return jsonify({"error": "Title must be 80 characters or fewer."}), 400

        task_id = next(next_task_id)
        task = {"id": task_id, "title": title, "completed": False}
        tasks[task_id] = task
        return jsonify(task), 201

    @app.post("/api/tasks/<int:task_id>/complete")
    def complete_task(task_id: int):
        task = tasks.get(task_id)
        if task is None:
            return jsonify({"error": "Task not found."}), 404
        task["completed"] = True
        return jsonify(task)

    return app
