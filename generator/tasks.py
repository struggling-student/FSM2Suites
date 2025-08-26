"""
Invoke tasks for running machine generator tests.

Usage:
    invoke test                    # Run all tests
    invoke test-unit               # Run all unit tests
    invoke test-integration        # Run integration tests only
    invoke test-model              # Run model tests
    invoke test-rules              # Run rules tests
    invoke test-strategies         # Run strategies tests
    invoke test-parsing            # Run parsing tests
    invoke test-generator          # Run generator tests
    invoke verify-env              # Verify test environment
    invoke test-coverage           # Run tests with coverage
"""

import os
import sys
from invoke import task

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
TESTS_PATH = os.path.join(PROJECT_ROOT, 'tests')

def setup_python_path():
    """Add src directory to Python path for tests"""
    if SRC_PATH not in sys.path:
        sys.path.insert(0, SRC_PATH)

@task
def test(c):
    """Run all tests (unit and integration)"""
    print("Running all tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            f"python -m unittest discover {TESTS_PATH} -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ All tests passed!")
        else:
            print("\n✗ Some tests failed!")
            sys.exit(1)

@task
def test_unit(c):
    """Run all unit tests (excluding integration tests)"""
    print("Running unit tests...")
    setup_python_path()
    
    unit_test_modules = [
        "test_model",
        "test_rules", 
        "test_strategies",
        "test_parsing",
        "test_generator"
    ]
    
    with c.cd(PROJECT_ROOT):
        for module in unit_test_modules:
            print(f"\n--- Running {module} ---")
            result = c.run(
                f"python -m unittest tests.{module} -v",
                warn=True
            )
            if result.exited != 0:
                print(f"\n✗ Tests in {module} failed!")
                sys.exit(1)
    
    print("\n✓ All unit tests passed!")

@task
def test_integration(c):
    """Run integration tests only"""
    print("Running integration tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python -m unittest tests.test_integration -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Integration tests passed!")
        else:
            print("\n✗ Integration tests failed!")
            sys.exit(1)

@task
def test_model(c):
    """Run model tests"""
    print("Running model tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python -m unittest tests.test_model -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Model tests passed!")
        else:
            print("\n✗ Model tests failed!")
            sys.exit(1)

@task
def test_rules(c):
    """Run rules tests"""
    print("Running rules tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python -m unittest tests.test_rules -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Rules tests passed!")
        else:
            print("\n✗ Rules tests failed!")
            sys.exit(1)

@task
def test_strategies(c):
    """Run strategies tests"""
    print("Running strategies tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python -m unittest tests.test_strategies -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Strategies tests passed!")
        else:
            print("\n✗ Strategies tests failed!")
            sys.exit(1)

@task
def test_parsing(c):
    """Run parsing tests"""
    print("Running parsing tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python -m unittest tests.test_parsing -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Parsing tests passed!")
        else:
            print("\n✗ Parsing tests failed!")
            sys.exit(1)

@task
def test_generator(c):
    """Run generator tests"""
    print("Running generator tests...")
    setup_python_path()
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python -m unittest tests.test_generator -v",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Generator tests passed!")
        else:
            print("\n✗ Generator tests failed!")
            sys.exit(1)

@task
def verify_env(c):
    """Verify that the test environment is set up correctly"""
    print("Verifying test environment...")
    
    with c.cd(PROJECT_ROOT):
        result = c.run(
            "python verify_test_env.py",
            warn=True
        )
        
        if result.exited == 0:
            print("\n✓ Test environment verification passed!")
        else:
            print("\n✗ Test environment verification failed!")
            sys.exit(1)

@task
def test_coverage(c):
    """Run tests with coverage report (requires coverage.py)"""
    print("Running tests with coverage...")
    setup_python_path()
    
    try:
        # Try to import coverage to check if it's installed
        import importlib.util
        spec = importlib.util.find_spec("coverage")
        if spec is None:
            raise ImportError("coverage not found")
    except ImportError:
        print("Coverage.py not installed. Installing...")
        c.run("pip install coverage")
    
    with c.cd(PROJECT_ROOT):
        # Run tests with coverage
        c.run(f"coverage run --source=src -m unittest discover {TESTS_PATH}")
        
        # Generate coverage report
        print("\nCoverage Report:")
        c.run("coverage report -m")
        
        # Generate HTML coverage report
        c.run("coverage html")
        print("\nHTML coverage report generated in htmlcov/")

@task
def clean(c):
    """Clean up test artifacts and cache files"""
    print("Cleaning up test artifacts...")
    
    with c.cd(PROJECT_ROOT):
        # Remove Python cache files
        c.run("find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true")
        c.run("find . -name '*.pyc' -delete 2>/dev/null || true")
        c.run("find . -name '*.pyo' -delete 2>/dev/null || true")
        
        # Remove coverage files
        c.run("rm -f .coverage 2>/dev/null || true")
        c.run("rm -rf htmlcov 2>/dev/null || true")
        
        # Remove test output files
        c.run("rm -f test_output.robot 2>/dev/null || true")
        
    print("✓ Cleanup completed!")

@task
def install_deps(c):
    """Install test dependencies"""
    print("Installing test dependencies...")
    
    with c.cd(PROJECT_ROOT):
        c.run("pip install -r test-requirements.txt")
        c.run("pip install invoke")  # Ensure invoke is installed
        
    print("✓ Test dependencies installed!")

@task
def help_tests(c):
    """Show detailed help for all test tasks"""
    print("""
Machine Generator Test Tasks
============================

Available tasks:

Basic Test Commands:
  invoke test                 - Run all working tests (unit tests only)
  invoke test-unit            - Run all working unit tests
  invoke quick-test           - Run a quick subset of tests for fast feedback

Individual Test Commands:
  invoke test-model           - Run model class tests (working)
  invoke test-rules           - Run rule evaluation tests (working)
  invoke test-strategies      - Run test generation strategy tests (working)

Note: test-parsing and test-generator are currently excluded as they need fixes.

Utility Commands:
  invoke verify-env           - Verify test environment setup
  invoke test-coverage        - Run tests with coverage analysis
  invoke clean                - Clean up test artifacts and cache
  invoke install-deps         - Install test dependencies
  invoke help-tests           - Show this help message

Examples:
  invoke test                 # Run all working tests
  invoke test-unit            # Just unit tests
  invoke test-model           # Only model tests
  invoke quick-test           # Fast subset for development

Working Test Structure:
  tests/
  ├── test_model.py          - Variable, State, Action, Machine classes (✓ working)
  ├── test_rules.py          - Condition and rule evaluation (✓ working)
  ├── test_strategies.py     - DepthFirst and Random strategies (✓ working)
  ├── test_parsing.py        - Machine definition parsing (⚠ needs fixes)
  ├── test_generator.py      - Main Generator class (⚠ needs fixes)
  └── test_integration.py    - End-to-end workflow tests (⚠ needs fixes)

For more details, see tests/README.md
""")

@task  
def quick_test(c):
    """Run a quick subset of tests for fast feedback"""
    print("Running quick test suite...")
    setup_python_path()
    
    # Only include working test classes
    quick_modules = [
        "test_model.TestVariable",
        "test_rules.TestConditions", 
        "test_strategies.TestDepthFirstSearchStrategy"
    ]
    
    with c.cd(PROJECT_ROOT):
        for test_class in quick_modules:
            module, class_name = test_class.split('.')
            print(f"\n--- Running {class_name} from {module} ---")
            result = c.run(
                f"python -m unittest tests.{test_class} -v",
                warn=True
            )
            if result.exited != 0:
                print(f"\n✗ Quick test {test_class} failed!")
                sys.exit(1)
    
    print("\n✓ Quick tests passed!")

# Default task
@task(default=True)
def default(c):
    """Default task - show available test commands"""
    print("""
Machine Generator Tests
=======================

Run 'invoke --list' to see all available tasks
Run 'invoke help-tests' for detailed help

Quick start:
  invoke test              # Run all working tests
  invoke test-unit         # Run unit tests only  
  invoke quick-test        # Fast subset for development

Working test modules: test_model, test_rules, test_strategies
""")
