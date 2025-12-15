# Runtime Configuration Guide
## QMS Dashboard - Phase 7 WS-1

**Document Version:** 1.0
**Last Updated:** 2025-12-15
**Phase:** 7 - Runtime & Environment Hardening

---

## Overview

The QMS Dashboard uses environment variables for runtime configuration. This allows the same codebase to run in different environments (development, verification, production) with appropriate settings.

**Configuration Module:** `src/backend/config.py`

---

## Environment Variables

### QMS_ENV (Required in Production)

**Purpose:** Defines the runtime environment

**Values:**
- `development` (default) - Local development with relaxed security
- `verification` - Test environment for Phase 6 verification
- `production` - Production deployment with strict validation

**Default:** `development`

**Example:**
```bash
export QMS_ENV=production
```

**Behavior by Environment:**

| Setting | Development | Verification | Production |
|---------|-------------|--------------|------------|
| Auto-reload | ✅ Enabled | ❌ Disabled | ❌ Disabled |
| CORS wildcard | ✅ Allowed | ❌ Denied | ❌ Denied |
| Data root default | ✅ Project /data | ✅ Project /data | ❌ Must specify |
| Startup validation | ⚠️ Warnings only | ✅ Strict | ✅ Fail-fast |

---

### QMS_DATA_ROOT (Required in Production)

**Purpose:** Absolute path to data storage root directory

**Default:** `{project_root}/data` (development/verification only)

**Production Requirement:** **MUST** be explicitly set (no default)

**Example:**
```bash
export QMS_DATA_ROOT=/var/lib/qms-dashboard/data
```

**Directory Structure:**

The system will create the following structure under `QMS_DATA_ROOT`:

```
$QMS_DATA_ROOT/
├── intake-responses/     # Intake JSON files
│   ├── abc123-uuid.json
│   └── def456-uuid.json
├── reviews/              # Expert review files
│   ├── ER-20251215-abc.json
│   └── ER-20251215-abc_response.json
├── artifacts/            # Generated QMS artifacts
│   └── abc123-uuid/
│       ├── QMS-Quality-Plan.md
│       └── ...
└── Expert-Review-Log.md  # Audit log
```

**Permissions:** Directory must be writable by the application user.

---

### QMS_LOG_LEVEL (Optional)

**Purpose:** Application logging verbosity

**Values:** `DEBUG`, `INFO`, `WARNING`, `ERROR`

**Default:** `INFO`

**Example:**
```bash
export QMS_LOG_LEVEL=DEBUG  # Development debugging
export QMS_LOG_LEVEL=WARNING  # Production (quieter)
```

---

### QMS_HOST (Optional)

**Purpose:** Server bind address

**Default:** `0.0.0.0` (all interfaces)

**Example:**
```bash
export QMS_HOST=127.0.0.1  # Localhost only
export QMS_HOST=0.0.0.0    # All interfaces
```

---

### QMS_PORT (Optional)

**Purpose:** Server port number

**Default:** `8000`

**Range:** 1-65535

**Example:**
```bash
export QMS_PORT=8080
```

---

### QMS_CORS_ORIGINS (Required in Production)

**Purpose:** Comma-separated list of allowed CORS origins

**Default:**
- Development: `*` (allow all)
- Production: **MUST** be specified (no wildcard)

**Example:**
```bash
# Development (default)
# No need to set - allows all origins

# Production
export QMS_CORS_ORIGINS=https://qms.example.com,https://qms-app.example.com
```

**Security Note:** Wildcard (`*`) CORS is **not allowed** in production mode. Application will fail to start if `QMS_ENV=production` and `QMS_CORS_ORIGINS` is not set.

---

## Configuration Validation

### Startup Validation

The application validates configuration on startup (`main.py:51-58`):

1. **Loads** environment variables
2. **Validates** configuration completeness
3. **Prints** configuration summary
4. **Fails fast** if invalid (production mode)

**Example Output:**
```
[CONFIG] ============================================================
QMS Dashboard Runtime Configuration
Environment: production
Data Root: /var/lib/qms-dashboard/data
  - Intake Responses: /var/lib/qms-dashboard/data/intake-responses
  - Reviews: /var/lib/qms-dashboard/data/reviews
  - Artifacts: /var/lib/qms-dashboard/data/artifacts
  - Review Log: /var/lib/qms-dashboard/data/Expert-Review-Log.md
Server: 0.0.0.0:8000
CORS Origins: https://qms.example.com
Log Level: INFO
[CONFIG] ============================================================
```

### Configuration Errors

If configuration is invalid, the application will:

1. **Print error message** to stderr
2. **Exit with code 1** (fail-fast)
3. **Not start the server**

**Example Error:**
```
❌ Configuration Error:
Configuration validation failed:
  - QMS_ENV=production requires explicit QMS_DATA_ROOT (no default paths in production)
  - QMS_ENV=production requires QMS_CORS_ORIGINS (wildcard CORS not allowed in production)

Please check environment variables and try again.
```

---

## Environment Setup Examples

### Development (Default)

**Minimal setup** - uses all defaults:

```bash
# No environment variables needed
python3 src/backend/main.py
```

**Custom data directory:**
```bash
export QMS_DATA_ROOT=/tmp/qms-dev-data
python3 src/backend/main.py
```

---

### Verification (Testing)

**For Phase 6 regression tests:**

```bash
export QMS_ENV=verification
export QMS_LOG_LEVEL=WARNING  # Quieter logs
python3 test_regression_phase6.py
```

---

### Production

**Full production configuration:**

```bash
export QMS_ENV=production
export QMS_DATA_ROOT=/var/lib/qms-dashboard/data
export QMS_CORS_ORIGINS=https://qms.example.com
export QMS_HOST=0.0.0.0
export QMS_PORT=8000
export QMS_LOG_LEVEL=WARNING

python3 src/backend/main.py
```

**Using systemd service file:**

```ini
[Unit]
Description=QMS Dashboard API
After=network.target

[Service]
Type=simple
User=qms
Group=qms
WorkingDirectory=/opt/qms-dashboard
Environment="QMS_ENV=production"
Environment="QMS_DATA_ROOT=/var/lib/qms-dashboard/data"
Environment="QMS_CORS_ORIGINS=https://qms.example.com"
Environment="QMS_LOG_LEVEL=WARNING"
ExecStart=/usr/bin/python3 src/backend/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## Testing Configuration

### Validate Configuration

Test configuration without starting the server:

```bash
cd src/backend
python3 config.py
```

**Success:**
```
[CONFIG] ============================================================
... configuration summary ...
[CONFIG] ============================================================

✅ Configuration valid
```

**Failure:**
```
❌ Configuration error:
Invalid QMS_ENV='prod'. Must be: development, verification, or production
```

---

## Filesystem Boundaries

### Write Operations

All file writes are confined to `QMS_DATA_ROOT`:

| Operation | Path |
|-----------|------|
| Save intake | `{DATA_ROOT}/intake-responses/{intake_id}.json` |
| Save review request | `{DATA_ROOT}/reviews/{review_id}.json` |
| Save review response | `{DATA_ROOT}/reviews/{review_id}_response.json` |
| Generate artifacts | `{DATA_ROOT}/artifacts/{intake_id}/` |
| Append review log | `{DATA_ROOT}/Expert-Review-Log.md` |

**No writes occur outside `QMS_DATA_ROOT`.**

### Read Operations

Read operations include:

- **Application code:** `src/backend/` (read-only)
- **Specification docs:** `doc/` (read-only)
- **Frontend assets:** `src/frontend/` (read-only, if present)
- **Data files:** `{DATA_ROOT}/*` (read/write)

---

## Configuration Changes (Phase 7 vs Phase 6)

### What Changed

**Phase 6 (Hard-coded):**
```python
# main.py
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "intake-responses"
```

**Phase 7 (Configurable):**
```python
# main.py
from config import get_config
config = get_config()
DATA_DIR = config.intake_dir
```

### Behavior Changes

**No functional behavior changes** - Phase 6 tests still pass.

**New capabilities:**
- ✅ Environment-aware configuration
- ✅ Production validation (fail-fast)
- ✅ Centralized path management
- ✅ CORS policy enforcement

---

## Troubleshooting

### Application won't start

**Error:** `Configuration validation failed`

**Solution:** Check that required environment variables are set for your environment.

**Production checklist:**
- [ ] `QMS_ENV=production` set
- [ ] `QMS_DATA_ROOT` set to absolute path
- [ ] `QMS_CORS_ORIGINS` set (no wildcards)
- [ ] Data root directory exists and is writable

---

### CORS errors in browser

**Error:** `Access to fetch at ... from origin ... has been blocked by CORS policy`

**Solution:**

**Development:**
```bash
# Default allows all origins - no action needed
```

**Production:**
```bash
# Add your frontend origin to allowed list
export QMS_CORS_ORIGINS=https://your-frontend.example.com
```

---

### Data directory not writable

**Error:** `Data root directory is not writable: /path/to/data`

**Solution:**

```bash
# Check permissions
ls -ld $QMS_DATA_ROOT

# Fix permissions
sudo chown -R qms:qms $QMS_DATA_ROOT
sudo chmod 755 $QMS_DATA_ROOT
```

---

## Migration Guide (Phase 6 → Phase 7)

### For Existing Deployments

**Phase 7 is backward compatible** - no migration required for development use.

**Action required for production:**

1. **Set environment variables** (see Production example above)
2. **Restart application** with new config
3. **Verify startup** - check configuration summary
4. **Test CORS** - ensure frontend can connect

**Data files:** No changes needed - directory structure is identical.

---

## Future Enhancements (Phase 8+)

**Planned:**
- Database connection configuration (when moving off file storage)
- Authentication provider settings (OAuth, LDAP, etc.)
- Email/notification service configuration
- Backup/retention policy settings

**Not planned for Phase 7** - filesystem-only deployment.

---

**Document Version:** 1.0
**Phase 7 WS-1 Complete:** Runtime & Environment Hardening
