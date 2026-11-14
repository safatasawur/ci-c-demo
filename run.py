"""Local runner for the independent CI/CD demonstration application."""

from task_api import create_app

app = create_app()

if __name__ == "__main__":
    # Loopback only. This is a teaching demo, not a production deployment.
    app.run(host="127.0.0.1", port=5000, debug=False)
