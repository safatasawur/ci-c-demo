# TaskFlow — Python DevSecOps CI Demo

A small, independent Python **task manager** that demonstrates **CI/CD, automated tests, SAST, and SCA** using GitHub Actions. This is a teaching/portfolio sample, **not bank software or an internal enterprise pipeline**.

The app has a simple light-themed web page where you can add and complete tasks. Its task data is kept **only in memory** and resets whenever the app restarts. It has **no user accounts or database** and is not intended for public production deployment.

## What will appear in GitHub Actions?

When you push the repo, GitHub Actions automatically starts **three parallel jobs**:

| Job | Tool | What it checks |
| --- | --- | --- |
| **1 · Unit tests** | pytest | Does the application behave as expected? |
| **2 · SAST** | Bandit | Are common unsafe Python code patterns present? |
| **3 · SCA** | pip-audit | Are known vulnerabilities reported in Python dependencies? |

These are complementary checks and do **not** replace comprehensive QA, threat modeling, manual review, or DAST. DAST (e.g. OWASP ZAP) is discussed in the internship presentation but is **not run** by this mini pipeline.

> GitHub-hosted runners can download dependencies from the internet. This demo is **not a model of SBP's network or infrastructure**. In a restricted enterprise environment, dependencies, tools, runners and approvals may need to be provisioned differently.

## How to publish to GitHub (recommended)

1. Extract the ZIP to a folder on your computer.
2. Create a **new empty** GitHub repository, e.g. `python-devsecops-demo` (do **not** select “Add a README”).
3. Open a terminal in the extracted `python-devsecops-demo` folder. Run:

   ```bash
   git init -b main
   git add .
   git commit -m "Add Python DevSecOps CI demo"
   git remote add origin https://github.com/YOUR-USERNAME/python-devsecops-demo.git
   git push -u origin main
   ```

   Replace `YOUR-USERNAME` with your own GitHub username. Sign in to GitHub if asked.

4. Open the repository's **Actions** tab. Choose **Python DevSecOps CI Demo**, then open the first run. Check the three jobs.

**Critical:** Ensure `.github/workflows/ci.yml` is uploaded! That hidden folder is what tells GitHub to run the workflow. Using Git from the terminal or GitHub Desktop is often simpler than browser uploads for preserving this folder structure.

If your repository already has a README or other files, use a new empty repo for this first demo to avoid unrelated merge issues.

## Run the web app locally (optional)

Use **Python 3.12 or later** (3.12 is the version used in CI).

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python run.py
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python run.py
```

Visit **http://127.0.0.1:5000** to add and complete tasks. Stop the server with Ctrl+C.

To run the checks yourself:

```bash
python -m pytest -v
bandit -r task_api run.py -q
pip-audit -r requirements.txt
```

The dependency audit needs internet access for vulnerability advisory data. Installation and some other checks require a working Python package source.

## Simple demo flow (about 60 seconds)

**0–10 sec:** Open the repository and explain: “This is a separate educational Python app, not code from my internship organization.”

**10–25 sec:** Show `.github/workflows/ci.yml`. Highlight the three jobs: unit tests, static security analysis, and dependency audit.

**25–45 sec:** Open **Actions → latest workflow run**. Show the green job results and briefly open the test output.

**45–60 sec:** Explain: “Every push can trigger these checks, so issues are reported earlier in development. This complements later manual QA and security reviews.”

For a safe, optional **failure → fix** demonstration, temporarily change the expected text in `tests/test_app.py` (`b"Small app. Real CI checks."`) to a different sentence, commit, and observe the **unit tests** job fail. Restore the original text and push again to see it pass. This demonstrates CI feedback without introducing insecure application code.

## Project structure

```text
python-devsecops-demo/
├── .github/workflows/ci.yml      # GitHub Actions workflow
├── task_api/
│   ├── __init__.py               # Flask API routes
│   ├── templates/index.html      # Browser interface
│   └── static/
│       ├── styles.css            # Light-theme design
│       └── app.js                # Browser interactions
├── tests/
│   ├── conftest.py               # Test setup
│   └── test_app.py               # 10 automated tests
├── run.py                        # Run server locally
├── requirements.txt              # Runtime dependency
├── requirements-dev.txt          # CI & test tools
└── README.md
```

### Scope and accuracy

This demo intentionally focuses on three visible CI checks. It does not use enterprise GitLab Runners, company repositories, production deployment, authenticated user data, or actual enterprise infrastructure. Use it to illustrate skills learned; describe your actual internship work separately in the presentation.
