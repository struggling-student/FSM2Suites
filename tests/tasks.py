from invoke import task
import os
import sys
import glob
from pathlib import Path
from io import StringIO

current_dir = Path(__file__).parent
generator_dir = current_dir.parent / "generator"
sys.path.insert(0, str(generator_dir))

try:
    from src.parsing import parse
    from src.generation import Generator, DepthFirstSearchStrategy, RandomStrategy, AllPairsRandomStrategy
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
