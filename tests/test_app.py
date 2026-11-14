"""Automated checks for TaskFlow's main behavior."""


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Small app. Real CI checks." in response.data


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_tasks_start_empty(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == {"tasks": []}


def test_create_task(client):
    response = client.post("/api/tasks", json={"title": "Check pipeline"})
    assert response.status_code == 201
    task = response.get_json()
    assert task == {"id": 1, "title": "Check pipeline", "completed": False}
    assert client.get("/api/tasks").get_json()["tasks"] == [task]


def test_complete_task(client):
    created = client.post("/api/tasks", json={"title": "Run tests"}).get_json()
    response = client.post(f"/api/tasks/{created['id']}/complete")
    assert response.status_code == 200
    assert response.get_json()["completed"] is True


def test_unknown_task_returns_404(client):
    response = client.post("/api/tasks/999/complete")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found."


def test_reject_empty_title(client):
    response = client.post("/api/tasks", json={"title": "    "})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_reject_non_json_input(client):
    response = client.post("/api/tasks", data="hello", content_type="text/plain")
    assert response.status_code == 400


def test_reject_title_over_80_chars(client):
    response = client.post("/api/tasks", json={"title": "x" * 81})
    assert response.status_code == 400


def test_title_is_trimmed(client):
    response = client.post("/api/tasks", json={"title": "  Test CI   "})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Test CI"
