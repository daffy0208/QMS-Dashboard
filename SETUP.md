# Setup & Installation Guide

**Phase 9 Documentation** | QMS Dashboard v1.0-demo

**Purpose:** This guide provides detailed setup instructions for running the frozen QMS Dashboard proof harness in demonstration mode.

**Scope:** Installation and verification only. No configuration changes or system modifications.

---

## 1. Prerequisites

### 1.1 System Requirements

**Operating System:**
- Linux (any modern distribution)
- macOS 10.15 or later
- Windows 10/11 with WSL2 (recommended) or native Python

**Hardware:**
- 2 GB RAM minimum (4 GB recommended)
- 500 MB free disk space
- Internet connection (for dependency installation only)

### 1.2 Required Software

**Python Environment:**
- **Python 3.10 or higher** (required)
- Check version: `python3 --version` or `python --version`
- Download from: https://www.python.org/downloads/

**Package Manager:**
- **pip** (included with Python 3.10+)
- OR **uv** (faster alternative: https://github.com/astral-sh/uv)

**Optional (for development):**
- Git (for cloning repository)
- curl or wget (for testing API endpoints)

---

## 2. Installation Steps

### 2.1 Clone or Download Repository

**Option A: Using Git**
```bash
git clone [repository-url]
cd "QMS Dashboard"
```

**Option B: Download ZIP**
1. Download repository as ZIP file
2. Extract to desired location
3. Navigate to extracted directory

### 2.2 Verify Project Structure

Ensure you're in the correct directory:
```bash
ls -la
```

**Expected key files:**
```
QMS Dashboard/
├── README.md
├── SETUP.md (this file)
├── WS-2-SCOPE-FREEZE.md
├── requirements.txt
├── src/
│   └── backend/
│       ├── main.py
│       ├── artifacts/
│       │   ├── validator.py
│       │   └── dependency_manager.py
│       └── ...
├── test_ws2_dependency_manager.py
├── test_ws2_api_endpoints.py
└── data/
```

### 2.3 Create Virtual Environment (Recommended)

**Why:** Isolates Dashboard dependencies from system Python packages.

**Using venv (standard):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate  # On Windows
```

**Using uv (faster):**
```bash
uv venv
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate  # On Windows
```

**Verification:**
Your terminal prompt should now show `(venv)` or `(.venv)`.

### 2.4 Install Dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using uv:**
```bash
uv pip install -r requirements.txt
```

**Expected output:**
- Installing fastapi, pydantic, uvicorn, pytest, requests, and dependencies
- No errors or unresolved dependencies

**Common issues:**
- If you see "command not found: pip", ensure Python 3.10+ is installed
- If you see permission errors, use virtual environment (step 2.3)
- If you see SSL errors, check internet connection and firewall

---

## 3. Verification

### 3.1 Verify Python Environment

```bash
python --version
# Expected: Python 3.10.x or higher
```

### 3.2 Verify Dependencies Installed

```bash
pip list | grep -E "(fastapi|pydantic|uvicorn|pytest)"
# OR
uv pip list | grep -E "(fastapi|pydantic|uvicorn|pytest)"
```

**Expected output:**
```
fastapi          0.100.0+
pydantic         2.0.0+
pytest          7.0.0+
uvicorn         0.20.0+
```

(Exact versions may vary)

### 3.3 Run Unit Tests

**Test WS-2 Dependency Manager:**
```bash
python test_ws2_dependency_manager.py
```

**Expected output:**
```
======================================================================
WS-2 DEPENDENCY MANAGER UNIT TESTS
======================================================================

TEST: Dependency Manager Initialization
✓ Dependency manager initialized successfully
✓ Loaded 11 artifact dependencies
✓ Loaded thresholds for 4 risk levels

...

======================================================================
TEST RESULTS: 10 passed, 0 failed
======================================================================
```

**If tests fail:**
- Check Python version (must be 3.10+)
- Verify all dependencies installed
- Ensure you're in the project root directory

### 3.4 Start API Server

```bash
cd src/backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Expected output:**
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Verification:**
Open browser to http://127.0.0.1:8000/docs

You should see FastAPI auto-generated documentation (Swagger UI).

### 3.5 Test Health Endpoint

**In a new terminal (keep server running):**
```bash
curl http://127.0.0.1:8000/health
```

**Expected response:**
```json
{"status": "healthy"}
```

**Stop the server:**
Press `CTRL+C` in the server terminal.

---

## 4. Configuration Files

### 4.1 Frozen Configuration (Read-Only)

The following configuration files define WS-2 behavior and are **frozen**:

**Location:** `src/backend/artifacts/`

1. **dependencies.json** (v1.0)
   - Static dependency graph
   - 11 QMS artifacts with prerequisites
   - DO NOT modify

2. **artifact_volatility.json** (v1.0)
   - Volatility classes and modifiers
   - Draft-friendly (-10%), foundation (0%), rework-costly (+10%)
   - DO NOT modify

3. **readiness_thresholds.json** (v1.0)
   - Risk-level-specific thresholds
   - R0: 50%, R1: 60%, R2: 80%, R3: 90%
   - DO NOT modify without explicit policy approval

**Governance:** See `WS-2-SCOPE-FREEZE.md:143-149` for change approval process.

### 4.2 Data Storage

**Intake data location:** `data/intake-responses/`

The Dashboard stores intake responses as JSON files in this directory.

**Important:**
- This is file-based storage (not production-grade)
- Data persists between server restarts
- Files can be deleted safely (they will be regenerated on next intake)

---

## 5. Running the Dashboard

### 5.1 Start the Server

**From project root:**
```bash
cd src/backend
uvicorn main:app --reload
```

**Server will be available at:**
- API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### 5.2 Stop the Server

Press `CTRL+C` in the terminal running uvicorn.

### 5.3 View Logs

Uvicorn logs appear in the terminal where the server is running.

**Common log messages:**
- `INFO: Application startup complete` - Server ready
- `INFO: "POST /api/intake HTTP/1.1" 200 OK` - Successful request
- `WARNING: ...` - Non-fatal issues
- `ERROR: ...` - Request failures (check request format)

---

## 6. Troubleshooting

### 6.1 "Module not found" errors

**Symptom:** `ModuleNotFoundError: No module named 'fastapi'`

**Solutions:**
1. Verify you activated the virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check you're using Python 3.10+

### 6.2 "Address already in use" error

**Symptom:** `[Errno 48] Address already in use` or `[Errno 98] Address already in use`

**Solutions:**
1. Check if server is already running: `lsof -i :8000` (Linux/macOS) or `netstat -ano | findstr :8000` (Windows)
2. Stop existing server or use different port: `uvicorn main:app --port 8001`
3. Kill process using port: `kill -9 <PID>`

### 6.3 Tests fail with "File not found"

**Symptom:** Tests fail to find configuration files

**Solutions:**
1. Ensure you're running tests from project root directory
2. Verify configuration files exist in `src/backend/artifacts/`
3. Check file permissions (must be readable)

### 6.4 Import errors from main.py

**Symptom:** `ImportError: cannot import name 'DependencyManager'`

**Solutions:**
1. Verify `dependency_manager.py` exists in `src/backend/artifacts/`
2. Check Python path includes `src/backend`
3. Restart server after code changes

### 6.5 JSON decode errors

**Symptom:** `JSONDecodeError: Expecting value`

**Solutions:**
1. Check request body format matches API documentation
2. Use `Content-Type: application/json` header
3. Verify JSON is valid (use https://jsonlint.com/)

---

## 7. Next Steps

Once installation is verified:

1. **Read Usage Guide:** See `USAGE-GUIDE.md` for when/how to use the Dashboard
2. **Run Demo Scenarios:** See `DEMO-SCENARIOS.md` for canonical examples
3. **Explore API:** Use http://127.0.0.1:8000/docs for interactive API exploration

---

## 8. Support & Governance

**This is a frozen proof harness.** Installation support is limited to:
- ✅ Dependency installation issues
- ✅ Environment setup problems
- ✅ Test execution errors

**Out of scope:**
- ❌ Feature requests
- ❌ Behavior modifications
- ❌ Production deployment support
- ❌ Performance tuning

**For governance questions:** See `WS-2-SCOPE-FREEZE.md`

**For frozen logic questions:** See `README.md` Section 3.3 (Governance References)

---

## 9. Appendix: Alternative Setup Methods

### 9.1 Using Docker (Optional, Not Official)

**Note:** Docker is not officially supported, but community-provided Dockerfiles may exist.

If using Docker:
1. Ensure Dockerfile respects frozen configuration files
2. Mount `data/` directory as volume for persistence
3. Expose port 8000

### 9.2 Using Poetry (Optional)

If you prefer Poetry for dependency management:
```bash
poetry install
poetry run uvicorn src.backend.main:app --reload
```

### 9.3 Using conda (Optional)

If you prefer conda:
```bash
conda create -n qms-dashboard python=3.10
conda activate qms-dashboard
pip install -r requirements.txt
```

---

**End of Setup Guide**

**Next:** See `USAGE-GUIDE.md` for when and how to use the Dashboard.
