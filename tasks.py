import sys
import subprocess
from invoke import task
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
BACKEND_PATH = PROJECT_ROOT / "backend"
FRONTEND_PATH = PROJECT_ROOT / "frontend"

running_processes = []

def cleanup_processes():
    for proc in running_processes:
        try:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=5)
        except (subprocess.TimeoutExpired, ProcessLookupError):
            try:
                proc.kill()
            except ProcessLookupError:
                pass
    running_processes.clear()

@task
def start_backend(c):
    try:
        with c.cd(str(BACKEND_PATH)):
            result = c.run("python -c 'import fastapi, uvicorn'", hide=True, warn=True)
            if result.exited != 0:
                c.run("pip install -r requirements.txt")
    except Exception:
        pass
    
    with c.cd(str(BACKEND_PATH)):
        c.run("python main.py", pty=True)

@task
def start_frontend(c):
    if not (FRONTEND_PATH / "node_modules").exists():
        with c.cd(str(FRONTEND_PATH)):
            c.run("npm install")
    
    with c.cd(str(FRONTEND_PATH)):
        c.run("npm run dev", pty=True)

@task
def start(c):
    try:
        with c.cd(str(BACKEND_PATH)):
            result = c.run("python -c 'import fastapi, uvicorn'", hide=True, warn=True)
            if result.exited != 0:
                c.run("pip install -r requirements.txt")
            
            backend_proc = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=str(BACKEND_PATH)
            )
            running_processes.append(backend_proc)
        
        with c.cd(str(FRONTEND_PATH)):
            if not (FRONTEND_PATH / "node_modules").exists():
                c.run("npm install")
            
            c.run("npm run dev", pty=True)
            
    except KeyboardInterrupt:
        cleanup_processes()
    except Exception:
        cleanup_processes()
        sys.exit(1)
