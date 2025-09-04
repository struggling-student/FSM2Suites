"""
Invoke tasks for the Shopping App project.

Usage:
    invoke start               # Start both backend and frontend
    invoke start-backend       # Start backend only
    invoke start-frontend      # Start frontend only
    invoke stop               # Stop all running services
    invoke install            # Install dependencies for both backend and frontend
    invoke test               # Run tests for both backend and frontend
    invoke test-backend       # Run backend tests only
    invoke test-frontend      # Run frontend tests only
"""

import sys
import subprocess
from invoke import task
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent
BACKEND_PATH = PROJECT_ROOT / "backend"
FRONTEND_PATH = PROJECT_ROOT / "frontend"

# Store process PIDs for cleanup
running_processes = []

def cleanup_processes():
    """Clean up any running processes"""
    for proc in running_processes:
        try:
            if proc.poll() is None:  # Process is still running
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
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    
    # Check if requirements are installed
    try:
        with c.cd(str(BACKEND_PATH)):
            result = c.run("python -c 'import fastapi, uvicorn'", hide=True, warn=True)
            if result.exited != 0:
                print("📦 Installing backend dependencies...")
                c.run("pip install -r requirements.txt")
    except Exception as e:
        print(f"Warning: Could not verify backend dependencies: {e}")
    
    with c.cd(str(BACKEND_PATH)):
        print("Backend server starting at http://localhost:8000")
        # Use pty=True to handle keyboard interrupts properly
        c.run("python main.py", pty=True)

@task
def start_frontend(c):
    """Start the React frontend development server"""
    print("🚀 Starting frontend development server...")
    
    # Check if node_modules exists
    if not (FRONTEND_PATH / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        with c.cd(str(FRONTEND_PATH)):
            c.run("npm install")
    
    with c.cd(str(FRONTEND_PATH)):
        print("Frontend server starting at http://localhost:5173")
        # Use pty=True to handle keyboard interrupts properly
        c.run("npm run dev", pty=True)

@task
def start(c):
    """Start both backend and frontend servers concurrently"""
    print("🚀 Starting both backend and frontend servers...")
    print("Backend will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:5173")
    print("Press Ctrl+C to stop both servers")
    
    try:
        # Start backend in background
        print("Starting backend...")
        with c.cd(str(BACKEND_PATH)):
            # Check and install backend dependencies if needed
            result = c.run("python -c 'import fastapi, uvicorn'", hide=True, warn=True)
            if result.exited != 0:
                print("📦 Installing backend dependencies...")
                c.run("pip install -r requirements.txt")
            
            backend_proc = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=str(BACKEND_PATH)
            )
            running_processes.append(backend_proc)
        
        # Start frontend
        print("Starting frontend...")
        with c.cd(str(FRONTEND_PATH)):
            # Check and install frontend dependencies if needed
            if not (FRONTEND_PATH / "node_modules").exists():
                print("📦 Installing frontend dependencies...")
                c.run("npm install")
            
            # Run frontend in foreground so we can catch Ctrl+C
            c.run("npm run dev", pty=True)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        cleanup_processes()
        print("✅ Servers stopped")
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        cleanup_processes()
        sys.exit(1)

@task
def stop(c):
    """Stop all running services"""
    print("🛑 Stopping all services...")
    cleanup_processes()
    
    # Also try to kill any processes on the default ports
    try:
        # Kill processes on port 8000 (backend)
        c.run("lsof -ti:8000 | xargs kill -9", warn=True, hide=True)
        # Kill processes on port 5173 (frontend)
        c.run("lsof -ti:5173 | xargs kill -9", warn=True, hide=True)
    except Exception:
        pass
    
    print("✅ All services stopped")

@task
def install(c):
    """Install dependencies for both backend and frontend"""
    print("📦 Installing dependencies...")
    
    # Install backend dependencies
    print("Installing backend dependencies...")
    with c.cd(str(BACKEND_PATH)):
        c.run("pip install -r requirements.txt")
    
    # Install frontend dependencies
    print("Installing frontend dependencies...")
    with c.cd(str(FRONTEND_PATH)):
        c.run("npm install")
    
    print("✅ All dependencies installed!")

@task
def test_backend(c):
    """Run backend tests"""
    print("🧪 Running backend tests...")
    
    with c.cd(str(BACKEND_PATH)):
        # Install test dependencies if needed
        c.run("pip install pytest pytest-asyncio httpx", warn=True)
        
        # Run tests
        result = c.run("python -m pytest -v", warn=True)
        
        if result.exited == 0:
            print("✅ Backend tests passed!")
        else:
            print("❌ Backend tests failed!")
            sys.exit(1)

@task
def test_frontend(c):
    """Run frontend tests"""
    print("🧪 Running frontend tests...")
    
    with c.cd(str(FRONTEND_PATH)):
        result = c.run("npm test", warn=True)
        
        if result.exited == 0:
            print("✅ Frontend tests passed!")
        else:
            print("❌ Frontend tests failed!")
            sys.exit(1)

@task
def test(c):
    """Run tests for both backend and frontend"""
    print("🧪 Running all tests...")
    
    try:
        test_backend(c)
        test_frontend(c)
        print("✅ All tests passed!")
    except SystemExit:
        print("❌ Some tests failed!")
        sys.exit(1)

@task
def lint(c):
    """Run linting for both backend and frontend"""
    print("🔍 Running linting...")
    
    # Backend linting (if flake8 or black is available)
    print("Linting backend...")
    with c.cd(str(BACKEND_PATH)):
        # Try to install and run basic linting
        c.run("pip install flake8", warn=True)
        c.run("flake8 . --max-line-length=88", warn=True)
    
    # Frontend linting
    print("Linting frontend...")
    with c.cd(str(FRONTEND_PATH)):
        c.run("npm run lint", warn=True)
    
    print("✅ Linting complete!")

@task
def build_frontend(c):
    """Build the frontend for production"""
    print("🏗️ Building frontend for production...")
    
    with c.cd(str(FRONTEND_PATH)):
        c.run("npm run build")
    
    print("✅ Frontend build complete!")

@task
def clean(c):
    """Clean up build artifacts and cache"""
    print("🧹 Cleaning up...")
    
    # Clean Python cache
    c.run("find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true")
    c.run("find . -name '*.pyc' -delete 2>/dev/null || true")
    
    # Clean frontend build
    with c.cd(str(FRONTEND_PATH)):
        c.run("rm -rf dist node_modules/.cache", warn=True)
    
    print("✅ Cleanup complete!")

@task
def dev(c):
    """Alias for start - start development servers"""
    start(c)

@task
def setup(c):
    """Initial project setup - install all dependencies"""
    print("🔧 Setting up project...")
    install(c)
    print("✅ Project setup complete!")
    print("\nNext steps:")
    print("  invoke start    # Start both servers")
    print("  invoke test     # Run tests")
