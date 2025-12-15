# Operations Guide
## QMS Dashboard - Day-to-Day Operations

**Document Version:** 1.0
**Last Updated:** 2025-12-15
**Phase:** 7 WS-3 - Operational Readiness
**Audience:** System operators, DevOps, SRE teams

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Data Directory Structure](#data-directory-structure)
4. [Startup Procedures](#startup-procedures)
5. [Shutdown Procedures](#shutdown-procedures)
6. [Health Checks](#health-checks)
7. [Common Operations](#common-operations)
8. [Monitoring](#monitoring)
9. [Log Files](#log-files)
10. [Backup Procedures](#backup-procedures)
11. [Maintenance Windows](#maintenance-windows)

---

## System Overview

### What is QMS Dashboard?

QMS Dashboard is a Quality Management System for AI/ML project intake and risk classification. It provides:

- **7-question intake form** for project characteristics
- **Automated risk classification** (R0-R3 levels)
- **QMS artifact generation** (5/8/11 artifacts per risk level)
- **Expert review workflow** (Phase 5 v1 - recorded decisions)

### Architecture

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ HTTP/REST
┌──────▼──────────────────┐
│  FastAPI Application    │
│  (src/backend/main.py)  │
├─────────────────────────┤
│  - Intake API           │
│  - Classification       │
│  - Artifact Generation  │
│  - Expert Review        │
└──────┬──────────────────┘
       │ File I/O
┌──────▼──────────────────┐
│  Data Directory         │
│  (Configured via env)   │
├─────────────────────────┤
│  - intake-responses/    │
│  - reviews/             │
│  - artifacts/           │
│  - Expert-Review-Log.md │
└─────────────────────────┘
```

### Technology Stack

- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)
- **Storage:** File-based (JSON + Markdown)
- **Validation:** Pydantic models

---

## Prerequisites

### System Requirements

**Minimum:**
- Python 3.9 or higher
- 512 MB RAM
- 1 GB disk space (data directory)
- Linux, macOS, or Windows

**Recommended:**
- Python 3.11+
- 2 GB RAM
- 10 GB disk space
- Linux (Ubuntu 20.04+ or RHEL 8+)

### Dependencies

Install Python dependencies:

```bash
pip install -r requirements.txt
```

**Required packages:**
- fastapi
- uvicorn
- pydantic
- python-multipart

### Permissions

**File System:**
- Read access to `src/` directory
- Write access to data directory (configured via `QMS_DATA_ROOT`)

**Network:**
- Bind permission for configured port (default: 8000)

---

## Data Directory Structure

### Standard Layout

```
$QMS_DATA_ROOT/
├── intake-responses/           # Intake JSON files
│   ├── abc123-uuid.json
│   ├── def456-uuid.json
│   └── ...
├── reviews/                    # Expert review files
│   ├── ER-20251215-abc.json             # Review request
│   ├── ER-20251215-abc_response.json    # Review response
│   └── ...
├── artifacts/                  # Generated QMS artifacts
│   ├── abc123-uuid/
│   │   ├── QMS-Quality-Plan.md
│   │   ├── QMS-CTQ-Tree.md
│   │   ├── QMS-Risk-Register.md
│   │   ├── ...
│   │   └── Project-Name-QMS-Artifacts.zip
│   └── ...
└── Expert-Review-Log.md        # Audit log (append-only)
```

### Directory Ownership

**Development:**
```bash
# User owns everything
chown -R $USER:$USER $QMS_DATA_ROOT
chmod 755 $QMS_DATA_ROOT
```

**Production:**
```bash
# Dedicated service user
chown -R qms:qms /var/lib/qms-dashboard/data
chmod 750 /var/lib/qms-dashboard/data
```

### Disk Space Management

**Growth Rate:**
- Intake: ~5 KB per intake
- Artifacts: ~50-100 KB per intake (varies by risk level)
- Reviews: ~10 KB per review

**Estimation:**
- 1,000 intakes ≈ 150 MB
- 10,000 intakes ≈ 1.5 GB

**Monitoring:**
```bash
# Check disk usage
du -sh $QMS_DATA_ROOT
df -h $QMS_DATA_ROOT
```

---

## Startup Procedures

### Pre-Startup Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables configured (see runtime-config.md)
- [ ] Data directory exists and is writable
- [ ] Port 8000 (or configured port) is available
- [ ] No conflicting processes running

### Starting the Application

#### Development Mode

```bash
cd "/path/to/QMS Dashboard"
export QMS_ENV=development
python3 src/backend/main.py
```

**Expected Output:**
```
[CONFIG] ============================================================
QMS Dashboard Runtime Configuration
Environment: development
Data Root: /path/to/QMS Dashboard/data
  - Intake Responses: .../data/intake-responses
  - Reviews: .../data/reviews
  - Artifacts: .../data/artifacts
  - Review Log: .../data/Expert-Review-Log.md
Server: 0.0.0.0:8000
CORS Origins: *
Log Level: INFO
[CONFIG] ============================================================
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Production Mode (systemd)

**Service file:** `/etc/systemd/system/qms-dashboard.service`

```bash
# Start service
sudo systemctl start qms-dashboard

# Check status
sudo systemctl status qms-dashboard

# Enable auto-start on boot
sudo systemctl enable qms-dashboard
```

**Expected Status:**
```
● qms-dashboard.service - QMS Dashboard API
   Loaded: loaded (/etc/systemd/system/qms-dashboard.service; enabled)
   Active: active (running) since Sun 2025-12-15 10:00:00 UTC
   Main PID: 12345 (python3)
```

#### Verification

1. **Check health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "version": "1.0.0",
     "timestamp": "2025-12-15T10:00:00.000000"
   }
   ```

2. **Check logs:**
   ```bash
   # Development
   # Logs output to terminal

   # Production (systemd)
   sudo journalctl -u qms-dashboard -f
   ```

3. **Verify data directory:**
   ```bash
   ls -la $QMS_DATA_ROOT
   # Should see: intake-responses/ reviews/ artifacts/
   ```

### Startup Issues

**Port already in use:**
```
ERROR: [Errno 48] Address already in use
```

Solution:
```bash
# Find process using port
lsof -i :8000
sudo kill <PID>
```

**Permission denied (data directory):**
```
PermissionError: [Errno 13] Permission denied: '/var/lib/qms-dashboard/data'
```

Solution:
```bash
# Fix permissions
sudo chown -R qms:qms /var/lib/qms-dashboard/data
sudo chmod 750 /var/lib/qms-dashboard/data
```

**Configuration error:**
```
❌ Configuration Error:
QMS_ENV=production requires explicit QMS_DATA_ROOT
```

Solution:
```bash
# Set required environment variables
export QMS_DATA_ROOT=/var/lib/qms-dashboard/data
export QMS_CORS_ORIGINS=https://qms.example.com
```

---

## Shutdown Procedures

### Graceful Shutdown

#### Development Mode

```bash
# Press CTRL+C in terminal
# Application will shutdown gracefully
```

**Expected Output:**
```
^C
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12345]
```

#### Production Mode (systemd)

```bash
# Stop service
sudo systemctl stop qms-dashboard

# Verify stopped
sudo systemctl status qms-dashboard
```

**Expected Status:**
```
● qms-dashboard.service - QMS Dashboard API
   Loaded: loaded (...)
   Active: inactive (dead)
```

### Emergency Shutdown

**If graceful shutdown fails:**

```bash
# Find process
ps aux | grep "main.py"

# Kill process
sudo kill -9 <PID>
```

### Post-Shutdown Checklist

- [ ] Application process terminated
- [ ] Port released (verify with `lsof -i :8000`)
- [ ] No error messages in logs
- [ ] Data directory intact (no corruption)

---

## Health Checks

### Health Endpoint

**Endpoint:** `GET /health`

**Purpose:** Verify application is running and responsive

**Example:**
```bash
curl http://localhost:8000/health
```

**Response (Healthy):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-15T10:00:00.000000"
}
```

### Readiness Checks

**Check 1: Application Running**
```bash
curl -f http://localhost:8000/health || echo "FAIL: Application not responding"
```

**Check 2: Data Directory Writable**
```bash
touch $QMS_DATA_ROOT/.write_test && rm $QMS_DATA_ROOT/.write_test || echo "FAIL: Data directory not writable"
```

**Check 3: Recent Intakes**
```bash
# Check if intakes are being created
find $QMS_DATA_ROOT/intake-responses -name "*.json" -mtime -1
```

### Automated Health Monitoring

**cron job** (every 5 minutes):
```bash
*/5 * * * * curl -f http://localhost:8000/health > /dev/null 2>&1 || /usr/local/bin/alert-ops.sh "QMS Dashboard health check failed"
```

**systemd timer** (alternative):
```ini
[Unit]
Description=QMS Dashboard Health Check Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

---

## Common Operations

### View Recent Intakes

```bash
# List recent intake files
ls -lt $QMS_DATA_ROOT/intake-responses/*.json | head -10

# View specific intake
cat $QMS_DATA_ROOT/intake-responses/abc123-uuid.json | jq .
```

### View Expert Reviews

```bash
# List pending reviews
grep -l '"status": "pending"' $QMS_DATA_ROOT/reviews/*.json

# View review log
less $QMS_DATA_ROOT/Expert-Review-Log.md
```

### Generate Artifacts (Manual)

```bash
# Via API
curl -X POST http://localhost:8000/api/intake/{intake_id}/generate-artifacts
```

### Check System Statistics

```bash
# Count intakes by risk level
grep -h '"risk_level"' $QMS_DATA_ROOT/intake-responses/*.json | sort | uniq -c

# Example output:
#  45 "risk_level": "R0"
#  32 "risk_level": "R1"
#  18 "risk_level": "R2"
#   5 "risk_level": "R3"
```

### Data Directory Cleanup

**Remove old test intakes:**
```bash
# Backup first!
cp -r $QMS_DATA_ROOT $QMS_DATA_ROOT.backup.$(date +%Y%m%d)

# Remove test intakes (use with caution!)
find $QMS_DATA_ROOT/intake-responses -name "test-*.json" -delete
```

---

## Monitoring

### Key Metrics

**Application Metrics:**
- Request rate (requests per minute)
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx responses)
- Active connections

**System Metrics:**
- CPU usage
- Memory usage
- Disk I/O
- Disk space available

### Monitoring Tools

**Basic (curl + cron):**
```bash
#!/bin/bash
# /usr/local/bin/qms-health-check.sh

ENDPOINT="http://localhost:8000/health"
RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null $ENDPOINT)

if [ "$RESPONSE" != "200" ]; then
    echo "QMS Dashboard health check failed: HTTP $RESPONSE"
    # Send alert
fi
```

**Prometheus (if available):**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'qms-dashboard'
    static_configs:
      - targets: ['localhost:8000']
```

**Log Analysis:**
```bash
# Count errors in logs (systemd)
journalctl -u qms-dashboard --since "1 hour ago" | grep -i error | wc -l
```

### Alert Thresholds

**Critical:**
- Application not responding (health check fails)
- Disk space < 10% remaining
- Error rate > 5%

**Warning:**
- Response time p95 > 1 second
- Disk space < 25% remaining
- Error rate > 1%

---

## Log Files

### Development Mode

**Location:** Terminal output (stdout/stderr)

**Log Level:** Controlled by `QMS_LOG_LEVEL` (default: INFO)

**View logs:**
```bash
# Logs appear in terminal where application was started
```

### Production Mode (systemd)

**Location:** systemd journal

**View logs:**
```bash
# All logs
sudo journalctl -u qms-dashboard

# Follow logs (tail -f equivalent)
sudo journalctl -u qms-dashboard -f

# Recent logs (last hour)
sudo journalctl -u qms-dashboard --since "1 hour ago"

# Errors only
sudo journalctl -u qms-dashboard -p err

# Specific date range
sudo journalctl -u qms-dashboard --since "2025-12-15 09:00" --until "2025-12-15 17:00"
```

### Log Levels

| Level | When Used | Example |
|-------|-----------|---------|
| **DEBUG** | Development debugging | Variable values, function calls |
| **INFO** | Normal operations | Request received, file saved |
| **WARNING** | Potential issues | Deprecated feature, slow response |
| **ERROR** | Operation failures | Invalid input, file not found |

**Set log level:**
```bash
export QMS_LOG_LEVEL=DEBUG  # Development
export QMS_LOG_LEVEL=WARNING  # Production (quieter)
```

### Application Logs

**Startup logs:**
```
[CONFIG] QMS Dashboard Runtime Configuration
INFO: Started server process [12345]
INFO: Application startup complete.
```

**Request logs:**
```
INFO: POST /api/intake - 201 Created
[STORAGE] Review request saved: /path/to/reviews/ER-20251215-abc.json
```

**Error logs:**
```
ERROR: Configuration validation failed
ERROR: Intake abc123 not found
```

### Audit Log

**File:** `$QMS_DATA_ROOT/Expert-Review-Log.md`

**Purpose:** Immutable audit trail of expert reviews

**Format:** Markdown (append-only)

**View:**
```bash
less $QMS_DATA_ROOT/Expert-Review-Log.md
```

**Rotation:** Not required (append-only, slow growth)

---

## Backup Procedures

### What to Backup

**Critical (must backup):**
- ✅ `$QMS_DATA_ROOT/intake-responses/` - All intake data
- ✅ `$QMS_DATA_ROOT/reviews/` - Expert review decisions
- ✅ `$QMS_DATA_ROOT/Expert-Review-Log.md` - Audit log

**Optional (can regenerate):**
- ⚠️ `$QMS_DATA_ROOT/artifacts/` - Can be regenerated from intakes

**Not needed:**
- ❌ Application code (version controlled in Git)
- ❌ Dependencies (reinstallable via pip)

### Backup Frequency

**Recommended:**
- **Daily:** Full backup of data directory
- **Weekly:** Archive to long-term storage
- **Monthly:** Verify restore procedures

### Backup Methods

#### Method 1: Simple Copy (Development)

```bash
#!/bin/bash
# Backup script: /usr/local/bin/qms-backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/qms-dashboard"
DATA_ROOT="$QMS_DATA_ROOT"

# Create backup
mkdir -p "$BACKUP_DIR"
cp -r "$DATA_ROOT" "$BACKUP_DIR/data-$DATE"

# Compress
tar -czf "$BACKUP_DIR/qms-data-$DATE.tar.gz" -C "$BACKUP_DIR" "data-$DATE"
rm -rf "$BACKUP_DIR/data-$DATE"

echo "Backup complete: $BACKUP_DIR/qms-data-$DATE.tar.gz"
```

#### Method 2: rsync (Production)

```bash
#!/bin/bash
# Incremental backup with rsync

BACKUP_HOST="backup-server.example.com"
BACKUP_PATH="/backup/qms-dashboard"
DATA_ROOT="$QMS_DATA_ROOT"

rsync -avz --delete \
  "$DATA_ROOT/" \
  "$BACKUP_HOST:$BACKUP_PATH/current/"

# Keep 7 daily snapshots
ssh $BACKUP_HOST "cd $BACKUP_PATH && \
  rm -rf day7 && \
  mv day6 day7 && mv day5 day6 && mv day4 day5 && \
  mv day3 day4 && mv day2 day3 && mv day1 day2 && \
  cp -al current day1"
```

#### Method 3: Cloud Backup (AWS S3)

```bash
#!/bin/bash
# Backup to S3

DATE=$(date +%Y%m%d)
BUCKET="s3://qms-backups"
DATA_ROOT="$QMS_DATA_ROOT"

aws s3 sync "$DATA_ROOT" "$BUCKET/$DATE/" --delete
```

### Backup Verification

```bash
# Verify backup integrity
tar -tzf /backup/qms-dashboard/qms-data-20251215.tar.gz | head

# Check backup size
ls -lh /backup/qms-dashboard/

# Verify file count
tar -tzf backup.tar.gz | wc -l
```

### Restore Procedures

**See RUNBOOK.md** for detailed restore procedures.

---

## Maintenance Windows

### Planned Maintenance

**Recommended schedule:**
- **Weekly:** Dependency updates (security patches)
- **Monthly:** Full system update (OS, Python)
- **Quarterly:** Major version upgrades

### Pre-Maintenance Checklist

- [ ] Notify users of maintenance window
- [ ] Create full backup
- [ ] Test restore procedure
- [ ] Prepare rollback plan
- [ ] Document changes

### During Maintenance

1. **Stop application**
   ```bash
   sudo systemctl stop qms-dashboard
   ```

2. **Perform updates**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Verify configuration**
   ```bash
   python3 src/backend/config.py
   ```

4. **Start application**
   ```bash
   sudo systemctl start qms-dashboard
   ```

5. **Verify health**
   ```bash
   curl http://localhost:8000/health
   ```

### Post-Maintenance Checklist

- [ ] Application running
- [ ] Health check passing
- [ ] No errors in logs
- [ ] Test key workflows (intake, review, artifacts)
- [ ] Notify users maintenance is complete

---

## Quick Reference

### Useful Commands

```bash
# Check if application is running
systemctl status qms-dashboard

# View recent logs
journalctl -u qms-dashboard -n 50

# Check disk space
df -h $QMS_DATA_ROOT

# Count intakes
ls $QMS_DATA_ROOT/intake-responses/*.json | wc -l

# Find recent reviews
find $QMS_DATA_ROOT/reviews -name "*_response.json" -mtime -7

# Backup data directory
tar -czf qms-backup-$(date +%Y%m%d).tar.gz $QMS_DATA_ROOT
```

### Configuration Files

| File | Purpose |
|------|---------|
| `src/backend/main.py` | Application entry point |
| `src/backend/config.py` | Configuration module |
| `doc/runtime-config.md` | Configuration reference |
| `/etc/systemd/system/qms-dashboard.service` | systemd service file |

### Important Paths

| Path | Description |
|------|-------------|
| `$QMS_DATA_ROOT` | Data root directory |
| `$QMS_DATA_ROOT/intake-responses/` | Intake JSON files |
| `$QMS_DATA_ROOT/reviews/` | Review files |
| `$QMS_DATA_ROOT/artifacts/` | Generated artifacts |
| `$QMS_DATA_ROOT/Expert-Review-Log.md` | Audit log |

---

## Support

### Documentation

- **Configuration:** `doc/runtime-config.md`
- **Security:** `doc/SECURITY-UPDATES-PHASE7-WS2.md`
- **Troubleshooting:** `RUNBOOK.md`
- **Changes:** `CHANGELOG.md`

### Getting Help

**Internal Team:**
- Check `RUNBOOK.md` for common issues
- Review logs: `journalctl -u qms-dashboard`
- Verify configuration: `python3 src/backend/config.py`

**Issue Reporting:**
- Include error messages from logs
- Include configuration (sanitize secrets!)
- Include steps to reproduce

---

**Document Version:** 1.0
**Last Updated:** 2025-12-15
**Phase 7 WS-3:** Operational Readiness Complete
