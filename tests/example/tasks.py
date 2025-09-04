from invoke import task
import os
import sys
import glob
from pathlib import Path
from io import StringIO

# Add the generator source to the path
current_dir = Path(__file__).parent
generator_dir = current_dir.parent.parent / "generator" / "src"
sys.path.insert(0, str(generator_dir))

# Import after path modification
try:
    # Create a module namespace that mimics the generator package structure
    import types
    
    # Create core module namespace
    core_module = types.ModuleType('core')
    sys.modules['core'] = core_module
    
    # Load rules module
    with open(generator_dir / "core" / "rules.py", 'r') as f:
        rules_code = f.read()
    exec(compile(rules_code, str(generator_dir / "core" / "rules.py"), 'exec'), vars(core_module))
    
    # Load model module
    with open(generator_dir / "core" / "model.py", 'r') as f:
        model_code = f.read()
    exec(compile(model_code, str(generator_dir / "core" / "model.py"), 'exec'), vars(core_module))
    
    # Create parsing module namespace
    parsing_module = types.ModuleType('parsing')
    sys.modules['parsing'] = parsing_module
    
    # Load parsing module with modified imports
    with open(generator_dir / "parsing" / "parsing.py", 'r') as f:
        parsing_code = f.read()
        # Replace relative imports with absolute
        parsing_code = parsing_code.replace('from ..core.model import', 'from core import')
        parsing_code = parsing_code.replace('from ..core.rules import', 'from core import')
    
    exec(compile(parsing_code, str(generator_dir / "parsing" / "parsing.py"), 'exec'), vars(parsing_module))
    
    # Create generation module namespace
    generation_module = types.ModuleType('generation')
    sys.modules['generation'] = generation_module
    
    # Load strategies
    with open(generator_dir / "generation" / "strategies.py", 'r') as f:
        strategies_code = f.read()
    exec(compile(strategies_code, str(generator_dir / "generation" / "strategies.py"), 'exec'), vars(generation_module))
    
    # Load generator with modified imports
    with open(generator_dir / "generation" / "generator.py", 'r') as f:
        generator_code = f.read()
        # Replace relative imports
        generator_code = generator_code.replace('from ..parsing.parsing import', 'from parsing import')
        generator_code = generator_code.replace('from .strategies import', 'from generation import')
    
    exec(compile(generator_code, str(generator_dir / "generation" / "generator.py"), 'exec'), vars(generation_module))
    
    # Extract the classes and functions we need
    parse = parsing_module.parse
    Generator = generation_module.Generator
    RandomStrategy = generation_module.RandomStrategy
    
except Exception:
    sys.exit(1)


def load_comprehensive_rules_machine():
    machine_file = current_dir / "rules.machine"
    with open(machine_file, 'r') as f:
        content = f.read()
    return parse(content)


def generate_robot_file(strategy_class, output_filename, max_tests, max_actions):
    try:
        # Load the machine
        machine = load_comprehensive_rules_machine()
        
        # Collect all actions for coverage tracking
        all_actions = set()
        for state in machine.states:
            for action in state._actions:
                action._parent_state = state
                all_actions.add(action)
        
        # Generate tests with specified limits
        generator = Generator()
        output = StringIO()
        generator.generate(
            machine, 
            max_tests=max_tests, 
            max_actions=max_actions, 
            output=output, 
            strategy=strategy_class,
            all_actions=all_actions
        )
        
        result = output.getvalue()
        
        # Create Robot Framework file with proper header
        full_content = f"""{result}"""
        
        # Create output directory if it doesn't exist
        output_dir = current_dir / "out"
        output_dir.mkdir(exist_ok=True)
        
        # Save to file in the out directory
        output_file = output_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(full_content)
        
        return True
        
    except Exception:
        return False


@task
def generate_random(ctx):
    filename = "comprehensive_rules_random.robot"
    generate_robot_file(RandomStrategy, filename, max_tests=100, max_actions=100)


@task
def generate(ctx):
    generate_random(ctx)


@task
def clean(ctx):
    # Remove generated .robot files from out directory
    out_dir = current_dir / "out"
    robot_files = list(out_dir.glob("comprehensive_rules_*.robot")) if out_dir.exists() else []
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    
    # Remove generated robot files
    for robot_file in robot_files:
        try:
            robot_file.unlink()
        except OSError:
            pass
    
    # Remove cache files
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
        except OSError:
            pass
    
    for pycache_dir in pycache_dirs:
        try:
            import shutil
            shutil.rmtree(pycache_dir)
        except OSError:
            pass
