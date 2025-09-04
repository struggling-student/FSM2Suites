from invoke import task
import os
import sys
import glob
from pathlib import Path
from io import StringIO

current_dir = Path(__file__).parent
generator_dir = current_dir.parent.parent / "generator"
sys.path.insert(0, str(generator_dir))

try:
    from src.parsing import parse
    from src.generation import Generator, RandomStrategy
except Exception:
    sys.exit(1)


def load_comprehensive_rules_machine():
    machine_file = current_dir / "rules.machine"
    with open(machine_file, 'r') as f:
        content = f.read()
    return parse(content)


def generate_robot_file(strategy_class, output_filename, max_tests, max_actions):
    try:
        machine = load_comprehensive_rules_machine()
        
        all_actions = set()
        for state in machine.states:
            for action in state._actions:
                action._parent_state = state
                all_actions.add(action)
        
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
def generate_random(ctx):
    filename = "comprehensive_rules_random.robot"
    generate_robot_file(RandomStrategy, filename, max_tests=100, max_actions=100)


@task
def generate(ctx):
    generate_random(ctx)


@task
def clean(ctx):
    out_dir = current_dir / "out"
    robot_files = list(out_dir.glob("comprehensive_rules_*.robot")) if out_dir.exists() else []
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
