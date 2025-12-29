# FacultyPlus - Python Virtual Environment Setup Guide (Tamil)

## Virtual Environment Creation & Installation Commands

### Step 1: Virtual Environment Create Pannu
```bash
cd /home/inpathtamilan/facultyplus

# Virtual environment create pannu
python3 -m venv venv

# Activate pannu (Linux/Mac)
source venv/bin/activate

# Activate pannu (Windows)
venv\Scripts\activate
```

### Step 2: Pip Upgrade Pannu
```bash
# Venv activate aana mathiri
source venv/bin/activate

# Pip, setuptools, wheel upgrade pannu
pip install --upgrade pip setuptools wheel
```

### Step 3: Requirements Install Pannu
```bash
# Venv activate aana mathiri
source venv/bin/activate

# All dependencies install pannu
pip install -r requirements.txt
```

---

## Complete Commands Sequence (Copy-Paste Ready)

### Linux/Mac lo:
```bash
cd /home/inpathtamilan/facultyplus
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Windows lo:
```bash
cd /home/inpathtamilan/facultyplus
python3 -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## Verification Commands

### Installed Packages Paarpan
```bash
# Venv activate aana mathiri
source venv/bin/activate

# All installed packages paarpan
pip list

# Django installed pannathu paarpan
python -c "import django; print(django.get_version())"

# Django REST Framework installed pannathu paarpan
python -c "import rest_framework; print(rest_framework.VERSION)"
```

---

## Django Setup Commands

### Step 1: Database Migration
```bash
# Venv activate aana mathiri
source venv/bin/activate

# Faculty Plus folder lo navigate pannu
cd /home/inpathtamilan/facultyplus

# Migrations create pannu
python manage.py migrate
```

### Step 2: Super Admin Create Pannu
```bash
# Venv activate aana mathiri
source venv/bin/activate

# Faculty Plus folder lo navigate pannu
cd /home/inpathtamilan/facultyplus

# Super admin create pannu (interactive)
python manage.py createsuperuser

# Prompts:
# Username: admin
# Email: admin@example.com
# Password: secure_password
# Password (again): secure_password
```

### Step 3: Development Server Run Pannu
```bash
# Venv activate aana mathiri
source venv/bin/activate

# Faculty Plus folder lo navigate pannu
cd /home/inpathtamilan/facultyplus

# Server start pannu
python manage.py runserver

# Output:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

---

## Quick Reference

### Daily Usage

**Morning lo server start pannu:**
```bash
cd /home/inpathtamilan/facultyplus
source venv/bin/activate
python manage.py runserver
```

**Server stop pannu:**
```
CTRL+C
```

**Venv deactivate pannu:**
```bash
deactivate
```

---

## Troubleshooting

### `python` command not found
```bash
# Use python3 instead
python3 -m venv venv
python3 -c "import django"
```

### `pip` not found
```bash
# Venv activate aana mathiri check pannu
source venv/bin/activate
which pip
```

### Module install error
```bash
# Pip upgrade pannu first
pip install --upgrade pip

# Then try install pannu again
pip install -r requirements.txt
```

### `django` not found
```bash
# Check installed packages
pip list | grep Django

# If not found, install manually
pip install Django==4.2.0
```

---

## Commands Summary Table

| Command | Purpose | Notes |
|---------|---------|-------|
| `python3 -m venv venv` | Create virtual environment | Linux/Mac/Windows |
| `source venv/bin/activate` | Activate (Linux/Mac) | Run this always before work |
| `venv\Scripts\activate` | Activate (Windows) | Windows users only |
| `deactivate` | Deactivate virtual environment | Exit venv |
| `pip install -r requirements.txt` | Install all dependencies | Internet required |
| `python manage.py migrate` | Create database tables | Run once after setup |
| `python manage.py createsuperuser` | Create admin user | Interactive |
| `python manage.py runserver` | Start development server | Port 8000 |
| `python manage.py shell` | Django interactive shell | Test code |
| `python manage.py auto_close_expired_jobs` | Auto-close job deadlines | Run daily |

---

## Installation Status

✅ **Virtual Environment**: Created  
✅ **Pip**: Upgraded to 25.3  
✅ **Setuptools**: Upgraded to 80.9.0  
✅ **Wheel**: Installed  
✅ **All Dependencies**: Installed successfully  
✅ **Django**: 4.2.0 installed  
✅ **Django REST Framework**: 3.14.0 installed  
✅ **Channels**: 4.0.0 installed  
✅ **Celery**: 5.2.7 installed  

---

## Next Steps

1. **Database Setup**: `python manage.py migrate`
2. **Create Super Admin**: `python manage.py createsuperuser`
3. **Run Server**: `python manage.py runserver`
4. **Access API**: `http://localhost:8000/api/`
5. **Access Admin**: `http://localhost:8000/admin/`

---

## Important Notes

- Venv activate aana mathiri **hamesha** Django commands run pannu
- Requirements.txt lo all dependencies iruku
- Production deploy aanukkara `.env` file create pannu
- Database migrate panna mathiri hamesha first setup lo pandanum

---

**Created**: 29 December 2025  
**Status**: Ready for Development  
**Location**: `/home/inpathtamilan/facultyplus/`
