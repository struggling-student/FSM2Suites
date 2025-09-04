from invoke import task
import os
import sys
import glob
from pathlib import Path
from io import StringIO

# Add the generator source to the path
current_dir = Path(__file__).parent
generator_dir = current_dir.parent / "generator" / "src"
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
    
    # Load allpairs strategy
    with open(generator_dir / "generation" / "allpairsstrategy.py", 'r') as f:
        allpairs_code = f.read()
        # Replace relative imports
        allpairs_code = allpairs_code.replace('from .strategies import', 'from generation import')
    
    exec(compile(allpairs_code, str(generator_dir / "generation" / "allpairsstrategy.py"), 'exec'), vars(generation_module))
    
    # Extract the classes and functions we need
    parse = parsing_module.parse
    Generator = generation_module.Generator
    DepthFirstSearchStrategy = generation_module.DepthFirstSearchStrategy
    RandomStrategy = generation_module.RandomStrategy
    AllPairsRandomStrategy = generation_module.AllPairsRandomStrategy
    
except Exception:
    import traceback
    traceback.print_exc()
    sys.exit(1)


def load_shopping_machine():
    machine_file = current_dir / "state.machine"
    with open(machine_file, 'r') as f:
        content = f.read()
    return parse(content)


def generate_robot_file(strategy_class, output_filename):
    try:
        machine = load_shopping_machine()
        
        all_actions = set()
        for state in machine.states:
            for action in state._actions:
                action._parent_state = state
                all_actions.add(action)
        
        generator = Generator()
        output = StringIO()
        generator.generate(
            machine, 
            max_tests=50, 
            max_actions=20, 
            output=output, 
            strategy=strategy_class,
            all_actions=all_actions
        )
        
        result = output.getvalue()
        
        full_content = f"""{result}"""
        
        output_dir = current_dir / "out"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(full_content)
        
        return True
        
    except Exception:
        return False


@task
def generate(ctx):
    strategies = [
        (DepthFirstSearchStrategy, "shopping_depth_first.robot", "Depth-First Search"),
        (RandomStrategy, "shopping_random.robot", "Random"),
        (AllPairsRandomStrategy, "shopping_all_pairs.robot", "All-Pairs")
    ]
    
    generated_files = []
    
    for strategy_class, filename, name in strategies:
        try:
            if generate_robot_file(strategy_class, filename):
                generated_files.append(filename)
        except AssertionError:
            pass
        except Exception:
            pass


@task
def clean(ctx):
    out_dir = current_dir / "out"
    robot_files = list(out_dir.glob("shopping_*.robot")) if out_dir.exists() else []
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    
    for robot_file in robot_files:
        try:
            robot_file.unlink()
        except OSError:
            pass
    
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
