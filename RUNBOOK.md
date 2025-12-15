# Runbook
## QMS Dashboard - Troubleshooting & Incident Response

**Document Version:** 1.0
**Last Updated:** 2025-12-15
**Phase:** 7 WS-3 - Operational Readiness
**Audience:** On-call engineers, incident responders

---

## Table of Contents

1. [Quick Incident Response](#quick-incident-response)
2. [Common Issues](#common-issues)
3. [Error Messages Reference](#error-messages-reference)
4. [Failure Scenarios](#failure-scenarios)
5. [Recovery Procedures](#recovery-procedures)
6. [Debug Procedures](#debug-procedures)
7. [Data Recovery](#data-recovery)
8. [Performance Issues](#performance-issues)
9. [Security Incidents](#security-incidents)

---

## Quick Incident Response

### Severity Levels

| Severity | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| **P0 - Critical** | Service down | < 15 minutes | Application not responding |
| **P1 - High** | Major functionality broken | < 1 hour | Cannot create intakes |
| **P2 - Medium** | Degraded performance | < 4 hours | Slow artifact generation |
| **P3 - Low** | Minor issue | < 1 business day | Cosmetic UI issue |

### Incident Response Checklist

**For all incidents:**
1. [ ] Check application status: `systemctl status qms-dashboard`
2. [ ] Check health endpoint: `curl http://localhost:8000/health`
3. [ ] Check recent logs: `journalctl -u qms-dashboard -n 100`
4. [ ] Check disk space: `df -h $QMS_DATA_ROOT`
5. [ ] Document findings
6. [ ] Apply fix (see specific issues below)
7. [ ] Verify resolution
8. [ ] Write post-incident report

---

## Common Issues

### Issue 1: Application Won't Start

**Symptoms:**
- `systemctl start qms-dashboard` fails
- Error in logs: "Configuration validation failed"

**Diagnosis:**
```bash
# Check service status
sudo systemctl status qms-dashboard

# View error logs
sudo journalctl -u qms-dashboard -n 50
```

**Common Causes:**

#### Cause A: Missing Environment Variables

**Error Message:**
```
❌ Configuration Error:
QMS_ENV=production requires explicit QMS_DATA_ROOT
```

**Solution:**
```bash
# Edit service file
sudo vim /etc/systemd/system/qms-dashboard.service

# Add missing environment variables
[Service]
Environment="QMS_ENV=production"
Environment="QMS_DATA_ROOT=/var/lib/qms-dashboard/data"
Environment="QMS_CORS_ORIGINS=https://qms.example.com"

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl start qms-dashboard
```

#### Cause B: Port Already in Use

**Error Message:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill conflicting process
sudo kill <PID>

# Or change port
export QMS_PORT=8001

# Restart
sudo systemctl start qms-dashboard
```

#### Cause C: Permission Denied (Data Directory)

**Error Message:**
```
PermissionError: [Errno 13] Permission denied: '/var/lib/qms-dashboard/data'
```

**Solution:**
```bash
# Check permissions
ls -ld /var/lib/qms-dashboard/data

# Fix ownership
sudo chown -R qms:qms /var/lib/qms-dashboard/data

# Fix permissions
sudo chmod 750 /var/lib/qms-dashboard/data

# Restart
sudo systemctl start qms-dashboard
```

---

### Issue 2: Health Check Failing

**Symptoms:**
- `curl http://localhost:8000/health` returns error or times out
- Application appears to be running but not responding

**Diagnosis:**
```bash
# Check if process is running
ps aux | grep "main.py"

# Check if port is listening
sudo netstat -tulpn | grep 8000

# Check recent errors
sudo journalctl -u qms-dashboard -p err -n 50
```

**Solutions:**

#### Solution A: Application Stuck

```bash
# Restart application
sudo systemctl restart qms-dashboard

# Wait 10 seconds
sleep 10

# Verify health
curl http://localhost:8000/health
```

#### Solution B: Network Issue

```bash
# Check firewall
sudo iptables -L | grep 8000

# Check if listening on correct interface
sudo netstat -tulpn | grep 8000
# Should show: 0.0.0.0:8000 (all interfaces)
```

---

### Issue 3: Intakes Not Saving

**Symptoms:**
- POST /api/intake returns 500 error
- Intake files not appearing in data directory

**Diagnosis:**
```bash
# Check data directory writable
touch $QMS_DATA_ROOT/intake-responses/.test && rm $QMS_DATA_ROOT/intake-responses/.test

# Check disk space
df -h $QMS_DATA_ROOT

# Check recent errors
sudo journalctl -u qms-dashboard | grep -i "intake" | tail -20
```

**Solutions:**

#### Solution A: Disk Full

```bash
# Check disk space
df -h $QMS_DATA_ROOT

# If disk is full, clean up old artifacts (backup first!)
cd $QMS_DATA_ROOT/artifacts
# Remove oldest artifact directories
ls -t | tail -n +100 | xargs rm -rf

# Verify space available
df -h $QMS_DATA_ROOT
```

#### Solution B: Permission Issue

```bash
# Check directory permissions
ls -ld $QMS_DATA_ROOT/intake-responses

# Fix permissions
sudo chown -R qms:qms $QMS_DATA_ROOT/intake-responses
sudo chmod 755 $QMS_DATA_ROOT/intake-responses
```

---

### Issue 4: Artifact Generation Fails

**Symptoms:**
- POST /api/intake/{id}/generate-artifacts returns 500
- Artifacts directory is empty

**Diagnosis:**
```bash
# Check if intake exists
ls $QMS_DATA_ROOT/intake-responses/{intake_id}.json

# Check artifacts directory writable
touch $QMS_DATA_ROOT/artifacts/.test && rm $QMS_DATA_ROOT/artifacts/.test

# Check error logs
sudo journalctl -u qms-dashboard | grep -i "artifact" | tail -20
```

**Solutions:**

#### Solution A: Intake Not Found

**Error:** `Intake {id} not found`

```bash
# Verify intake ID is correct
curl http://localhost:8000/api/intakes

# Use correct intake ID from response
```

#### Solution B: Template File Missing

**Error:** `FileNotFoundError: ...templates...`

```bash
# Verify template files exist
ls src/backend/artifacts/templates/

# If missing, restore from Git
git checkout src/backend/artifacts/templates/
```

---

### Issue 5: Expert Review Not Saving

**Symptoms:**
- POST /api/review/{id}/approve returns error
- Review responses not appearing in data directory

**Diagnosis:**
```bash
# Check reviews directory
ls -la $QMS_DATA_ROOT/reviews/

# Check review request exists
cat $QMS_DATA_ROOT/reviews/{review_id}.json

# Check error logs
sudo journalctl -u qms-dashboard | grep -i "review" | tail -20
```

**Solutions:**

#### Solution A: Review Not Found

```bash
# List available reviews
ls $QMS_DATA_ROOT/reviews/*.json | grep -v "_response"

# Use correct review ID
```

#### Solution B: Invalid Review Data

```bash
# Check review request format
cat $QMS_DATA_ROOT/reviews/{review_id}.json | jq .

# Verify all required fields present
```

---

## Error Messages Reference

### Configuration Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `Invalid QMS_ENV='prod'` | Invalid environment name | Use: development, verification, or production |
| `QMS_ENV=production requires explicit QMS_DATA_ROOT` | Missing required env var | Set `QMS_DATA_ROOT=/path/to/data` |
| `Data root directory is not writable` | Permission issue | Fix permissions: `chmod 750 $QMS_DATA_ROOT` |
| `Invalid QMS_PORT=99999` | Port out of range | Use port 1-65535 |

### Application Errors

| HTTP Code | Error | Meaning | Fix |
|-----------|-------|---------|-----|
| **400** | Invalid intake ID format | Malformed ID | Check ID format (UUID-like) |
| **400** | Invalid review ID format | Malformed review ID | Check format: ER-YYYYMMDD-{id} |
| **404** | Intake {id} not found | Intake doesn't exist | Verify intake ID |
| **404** | Review {id} not found | Review doesn't exist | Verify review ID |
| **413** | Request too large | > 10 MB payload | Reduce request size |
| **415** | Unsupported Media Type | Wrong content-type | Use: application/json |
| **500** | Internal server error | Application error | Check logs for details |

### Runtime Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Dependencies not installed | `pip install -r requirements.txt` |
| `PermissionError: [Errno 13]` | Permission denied | Fix file/directory permissions |
| `FileNotFoundError: [Errno 2]` | File not found | Verify file path, restore from backup |
| `Address already in use` | Port conflict | Change port or kill conflicting process |

---

## Failure Scenarios

### Scenario 1: Complete System Failure

**What Happens:**
- Application crashes
- No responses to any requests
- Health check fails

**Impact:**
- Users cannot submit intakes
- Cannot generate artifacts
- Cannot perform expert reviews

**Recovery:**

1. **Check application status:**
   ```bash
   sudo systemctl status qms-dashboard
   ```

2. **View crash logs:**
   ```bash
   sudo journalctl -u qms-dashboard -n 100
   ```

3. **Restart application:**
   ```bash
   sudo systemctl restart qms-dashboard
   ```

4. **Verify recovery:**
   ```bash
   curl http://localhost:8000/health
   ```

5. **If restart fails:**
   ```bash
   # Check configuration
   python3 src/backend/config.py

   # Fix any configuration errors
   # Then restart
   sudo systemctl start qms-dashboard
   ```

**Rollback Plan:**
- Restore previous version from Git
- Restore data from last backup
- Revert environment variable changes

---

### Scenario 2: Data Directory Corruption

**What Happens:**
- JSON files have invalid syntax
- Files are truncated or empty
- Directory structure is wrong

**Impact:**
- Cannot load existing intakes
- Cannot access reviews
- Data may be lost

**Recovery:**

1. **Stop application:**
   ```bash
   sudo systemctl stop qms-dashboard
   ```

2. **Assess damage:**
   ```bash
   # Check for invalid JSON files
   for file in $QMS_DATA_ROOT/intake-responses/*.json; do
     jq . "$file" > /dev/null 2>&1 || echo "INVALID: $file"
   done
   ```

3. **Restore from backup:**
   ```bash
   # Move corrupted data
   mv $QMS_DATA_ROOT $QMS_DATA_ROOT.corrupted

   # Restore from backup
   tar -xzf /backup/qms-data-latest.tar.gz -C /

   # Verify restored data
   ls -la $QMS_DATA_ROOT
   ```

4. **Restart application:**
   ```bash
   sudo systemctl start qms-dashboard
   ```

5. **Verify functionality:**
   ```bash
   # List intakes
   curl http://localhost:8000/api/intakes

   # Verify count matches expectation
   ```

---

### Scenario 3: Disk Full

**What Happens:**
- Cannot write new intakes
- Cannot generate artifacts
- Application may crash

**Impact:**
- Service degradation
- Data loss risk

**Recovery:**

1. **Check disk space:**
   ```bash
   df -h $QMS_DATA_ROOT
   ```

2. **Identify large files:**
   ```bash
   du -sh $QMS_DATA_ROOT/*
   du -sh $QMS_DATA_ROOT/artifacts/* | sort -h | tail -20
   ```

3. **Create emergency backup:**
   ```bash
   # Backup to alternate location
   rsync -av $QMS_DATA_ROOT /mnt/backup/qms-emergency/
   ```

4. **Free up space:**
   ```bash
   # Option A: Remove old artifacts (can be regenerated)
   cd $QMS_DATA_ROOT/artifacts
   ls -t | tail -n +100 | xargs rm -rf

   # Option B: Compress old intakes
   cd $QMS_DATA_ROOT/intake-responses
   find . -name "*.json" -mtime +90 -exec gzip {} \;
   ```

5. **Verify space available:**
   ```bash
   df -h $QMS_DATA_ROOT
   ```

6. **Resume operations:**
   ```bash
   # Application should auto-recover
   curl http://localhost:8000/health
   ```

---

### Scenario 4: Configuration Error After Update

**What Happens:**
- Application won't start after environment variable change
- Configuration validation fails

**Impact:**
- Service unavailable

**Recovery:**

1. **Check configuration:**
   ```bash
   python3 src/backend/config.py
   ```

2. **View error message:**
   ```bash
   sudo journalctl -u qms-dashboard -n 20
   ```

3. **Restore previous configuration:**
   ```bash
   # If using systemd, edit service file
   sudo vim /etc/systemd/system/qms-dashboard.service

   # Restore previous environment variables
   # Reload and restart
   sudo systemctl daemon-reload
   sudo systemctl start qms-dashboard
   ```

4. **Verify configuration:**
   ```bash
   python3 src/backend/config.py
   ```

---

## Recovery Procedures

### Full System Restore

**When to Use:**
- Complete data loss
- Unrecoverable corruption
- Disaster recovery

**Prerequisites:**
- Recent backup available
- Application code available (Git)
- System meets requirements

**Procedure:**

1. **Prepare system:**
   ```bash
   # Install Python and dependencies
   pip install -r requirements.txt

   # Create data directory
   sudo mkdir -p /var/lib/qms-dashboard/data
   sudo chown qms:qms /var/lib/qms-dashboard/data
   ```

2. **Restore data:**
   ```bash
   # Extract backup
   sudo tar -xzf /backup/qms-data-latest.tar.gz -C /var/lib/qms-dashboard/

   # Verify permissions
   sudo chown -R qms:qms /var/lib/qms-dashboard/data
   ```

3. **Configure application:**
   ```bash
   # Set environment variables
   export QMS_ENV=production
   export QMS_DATA_ROOT=/var/lib/qms-dashboard/data
   export QMS_CORS_ORIGINS=https://qms.example.com

   # Verify configuration
   python3 src/backend/config.py
   ```

4. **Start application:**
   ```bash
   sudo systemctl start qms-dashboard
   ```

5. **Verify data integrity:**
   ```bash
   # Count intakes
   ls $QMS_DATA_ROOT/intake-responses/*.json | wc -l

   # Verify via API
   curl http://localhost:8000/api/intakes | jq length
   ```

6. **Test functionality:**
   ```bash
   # Test health check
   curl http://localhost:8000/health

   # Test intake retrieval
   curl http://localhost:8000/api/intakes | jq '.[0].intake_id'

   # Verify review log
   head $QMS_DATA_ROOT/Expert-Review-Log.md
   ```

**Estimated Time:** 15-30 minutes

---

### Restore Single Intake

**When to Use:**
- Specific intake corrupted or deleted
- Need to recover one item

**Procedure:**

1. **Identify intake ID:**
   ```bash
   # From user report or logs
   INTAKE_ID="abc123-uuid"
   ```

2. **Find in backup:**
   ```bash
   # Extract from backup
   tar -xzf /backup/qms-data-20251215.tar.gz \
     --strip-components=3 \
     "data/intake-responses/$INTAKE_ID.json"
   ```

3. **Restore file:**
   ```bash
   # Copy to data directory
   cp "$INTAKE_ID.json" $QMS_DATA_ROOT/intake-responses/

   # Fix permissions
   chown qms:qms $QMS_DATA_ROOT/intake-responses/$INTAKE_ID.json
   ```

4. **Verify:**
   ```bash
   # Check file
   cat $QMS_DATA_ROOT/intake-responses/$INTAKE_ID.json | jq .

   # Test via API
   curl http://localhost:8000/api/intake/$INTAKE_ID
   ```

**Estimated Time:** 5 minutes

---

### Regenerate Artifacts

**When to Use:**
- Artifacts corrupted or deleted
- Artifacts can be regenerated from intake

**Procedure:**

1. **Identify intake:**
   ```bash
   INTAKE_ID="abc123-uuid"
   ```

2. **Remove corrupted artifacts:**
   ```bash
   rm -rf $QMS_DATA_ROOT/artifacts/$INTAKE_ID
   ```

3. **Regenerate via API:**
   ```bash
   curl -X POST http://localhost:8000/api/intake/$INTAKE_ID/generate-artifacts
   ```

4. **Verify:**
   ```bash
   ls $QMS_DATA_ROOT/artifacts/$INTAKE_ID/
   # Should see: QMS-*.md files and ZIP archive
   ```

**Estimated Time:** 1 minute per intake

---

## Debug Procedures

### Enable Debug Logging

```bash
# Temporary (current session)
export QMS_LOG_LEVEL=DEBUG
sudo systemctl restart qms-dashboard

# Watch logs
sudo journalctl -u qms-dashboard -f
```

### Trace Specific Request

```bash
# Enable debug logging
export QMS_LOG_LEVEL=DEBUG

# Make request with curl
curl -v -X POST http://localhost:8000/api/intake \
  -H "Content-Type: application/json" \
  -d @test-intake.json

# Check logs for request details
sudo journalctl -u qms-dashboard --since "1 minute ago"
```

### Inspect Data Files

```bash
# View intake JSON (pretty-printed)
cat $QMS_DATA_ROOT/intake-responses/$INTAKE_ID.json | jq .

# Validate JSON syntax
jq . $QMS_DATA_ROOT/intake-responses/$INTAKE_ID.json > /dev/null && echo "Valid JSON"

# Search for specific value
grep -r "R3" $QMS_DATA_ROOT/intake-responses/
```

### Test Configuration

```bash
# Validate configuration without starting server
python3 src/backend/config.py

# Test with different environment
QMS_ENV=production QMS_DATA_ROOT=/tmp/test python3 src/backend/config.py
```

---

## Data Recovery

### Recover Deleted Intake

**If backup available:**
```bash
# Restore from backup (see "Restore Single Intake" above)
```

**If no backup:**
- Data is unrecoverable
- Request user to resubmit intake

### Recover Corrupted JSON

**If partially readable:**
```bash
# View file
cat $QMS_DATA_ROOT/intake-responses/$INTAKE_ID.json

# Attempt to fix common issues
# - Missing closing brace: add }
# - Trailing comma: remove comma before }
# - Invalid escape sequences: fix manually

# Validate fix
jq . $QMS_DATA_ROOT/intake-responses/$INTAKE_ID.json
```

**If completely corrupted:**
- Restore from backup
- If no backup, data is lost

---

## Performance Issues

### Slow Response Times

**Diagnosis:**
```bash
# Time a request
time curl http://localhost:8000/api/intakes

# Check CPU usage
top -p $(pgrep -f "main.py")

# Check I/O wait
iostat -x 1 10
```

**Solutions:**

**Cause A: High CPU Usage**
```bash
# Check if Python process using high CPU
top | grep python

# May need to scale horizontally (multiple instances)
```

**Cause B: Slow Disk I/O**
```bash
# Check disk performance
iostat -x 1 10

# Consider moving data directory to faster disk
# Or enable disk caching
```

**Cause C: Large Data Directory**
```bash
# Archive old intakes
cd $QMS_DATA_ROOT/intake-responses
find . -name "*.json" -mtime +180 -exec mv {} ../archive/ \;
```

---

## Security Incidents

### Suspected Breach

**Immediate Actions:**

1. **Isolate system:**
   ```bash
   # Stop application
   sudo systemctl stop qms-dashboard

   # Block external access (firewall)
   sudo iptables -A INPUT -p tcp --dport 8000 -j DROP
   ```

2. **Preserve evidence:**
   ```bash
   # Copy logs
   sudo journalctl -u qms-dashboard > /tmp/qms-logs-$(date +%Y%m%d).txt

   # Copy data directory
   sudo cp -r $QMS_DATA_ROOT /tmp/qms-data-evidence
   ```

3. **Notify security team**

4. **Investigate:**
   ```bash
   # Check for unauthorized access
   grep -i "401\|403" /tmp/qms-logs-*.txt

   # Check for unusual file modifications
   find $QMS_DATA_ROOT -mtime -1 -ls
   ```

### Path Traversal Attempt

**Detection:**
```bash
# Search logs for path traversal patterns
grep -i "\.\.\/" /var/log/qms-dashboard.log
```

**Response:**
- Phase 7 WS-2 sanitization should block these attempts
- Verify sanitization is active
- Review logs for successful attacks (none expected)

---

## Escalation

### When to Escalate

**Escalate to senior engineer if:**
- Issue not resolved within SLA timeframe
- Data loss occurred
- Security incident suspected
- Multiple systems affected

**Escalation Contacts:**
- See internal documentation for on-call rotation

---

## Post-Incident Tasks

**After resolving any P0 or P1 incident:**

1. [ ] Write post-incident report
2. [ ] Document root cause
3. [ ] Identify preventive measures
4. [ ] Update runbook with new findings
5. [ ] Schedule retrospective meeting

---

**Document Version:** 1.0
**Last Updated:** 2025-12-15
**Phase 7 WS-3:** Operational Readiness Complete
