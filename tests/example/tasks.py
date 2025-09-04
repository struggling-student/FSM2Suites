"""
Invoke tasks for generating comprehensive rules test files
using the comprehensive_rules.machine file with Random Strategy.
"""

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
    
except Exception as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory")
    import traceback
    traceback.print_exc()
    sys.exit(1)


def load_comprehensive_rules_machine():
    """Load the comprehensive rules machine."""
    machine_file = current_dir / "rules.machine"
    with open(machine_file, 'r') as f:
        content = f.read()
    return parse(content)


def generate_robot_file(strategy_class, output_filename, max_tests=50, max_actions=50):
    """Generate a Robot Framework test file for the given strategy with specified limits."""
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
        
        print(f"✅ Generated: out/{output_filename}")
        print(f"   📊 Max Tests: {max_tests}, Max Actions: {max_actions}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {output_filename}: {e}")
        return False


@task
def generate_random(ctx):
    """
    Generate Robot Framework test file using Random Strategy.
    
    Creates:
    - comprehensive_rules_random.robot (Random Strategy with max 50 tests, 50 actions)
    
    Example:
        inv generate-random
    """
    print("🚀 Generating Robot Framework test file using Random Strategy")
    print("=" * 70)
    print("📋 Configuration:")
    print("   • Strategy: Random")
    print("   • Max Tests: 50")
    print("   • Max Actions: 50")
    print("   • Machine: comprehensive_rules.machine")
    print("=" * 70)
    
    filename = "comprehensive_rules_random.robot"
    strategy_name = "Random"
    
    print(f"\n🔄 Generating {strategy_name} strategy...")
    success = generate_robot_file(RandomStrategy, filename, max_tests=50, max_actions=50)
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Generation Complete!")
        print("\n📋 Generated file:")
        print(f"   • out/{filename}")
        print("\n🚀 Run the generated test:")
        print(f"   robot out/{filename}")
        print("\n📊 Coverage Analysis:")
        print("   Check the generated file for test coverage information")
    else:
        print("❌ Generation failed!")


@task
def generate(ctx):
    """
    Alias for generate-random task.
    
    Example:
        inv generate
    """
    generate_random(ctx)


@task
def clean(ctx):
    """
    Clean up generated Robot Framework test files.
    
    Removes:
    - comprehensive_rules_*.robot files
    - Python cache files
    
    Example:
        inv clean
    """
    print("🧹 Cleaning up generated files...")
    
    # Remove generated .robot files from out directory
    out_dir = current_dir / "out"
    robot_files = list(out_dir.glob("comprehensive_rules_*.robot")) if out_dir.exists() else []
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    
    removed_count = 0
    
    # Remove generated robot files
    for robot_file in robot_files:
        try:
            robot_file.unlink()
            removed_count += 1
            print(f"   🗑️  Removed: out/{robot_file.name}")
        except OSError:
            pass
    
    # Remove cache files
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            removed_count += 1
        except OSError:
            pass
    
    for pycache_dir in pycache_dirs:
        try:
            import shutil
            shutil.rmtree(pycache_dir)
            removed_count += 1
        except OSError:
            pass
    
    if removed_count > 0:
        print(f"✅ Removed {removed_count} files/directories")
    else:
        print("✅ No files to clean")


@task
def info(ctx):
    """
    Show information about the comprehensive rules machine.
    
    Example:
        inv info
    """
    print("📊 Comprehensive Rules Machine Information")
    print("=" * 50)
    
    try:
        machine = load_comprehensive_rules_machine()
        
        print("📁 Machine File: rules.machine")
        print(f"🏭 States: {len(machine.states)}")
        print(f"🔧 Variables: {len(machine.variables)}")
        print(f"📜 Rules: {len(machine.rules)}")
        
        print("\n🏭 States:")
        for state in machine.states:
            action_count = len(state._actions)
            print(f"   • {state.name} ({action_count} actions)")
            for action in state._actions:
                print(f"     - {action.name} -> {action._next_state_name}")
        
        print("\n🔧 Variables:")
        for var in machine.variables:
            value_count = len(var.values)
            print(f"   • {var.name} ({value_count} values)")
        
        if machine.rules:
            print("\n📜 Rules:")
            for i, rule in enumerate(machine.rules, 1):
                print(f"   • Rule {i}: {rule}")
        
        print("\n🎯 Generation Configuration:")
        print("   • Strategy: Random")
        print("   • Max Tests: 50")
        print("   • Max Actions: 50")
        
    except Exception as e:
        print(f"❌ Error loading machine: {e}")
        import traceback
        traceback.print_exc()


@task(default=True)
def help(ctx):
    """
    Show available tasks and usage information.
    """
    print("🔬 Comprehensive Rules Machine - Test Generation Tasks")
    print("=" * 60)
    print()
    print("Available tasks:")
    print("  inv generate         - Generate Robot Framework test file (Random Strategy)")
    print("  inv generate-random  - Generate test file using Random Strategy")
    print("  inv clean            - Clean up generated test files")
    print("  inv info             - Show machine information")
    print("  inv help             - Show this help message")
    print()
    print("Configuration:")
    print("  • Strategy: Random")
    print("  • Max Tests: 50")
    print("  • Max Actions: 50")
    print("  • Machine: comprehensive_rules.machine")
    print()
    print("Generated files:")
    print("  • out/comprehensive_rules_random.robot  - Random Strategy tests")
    print()
    print("Usage:")
    print("  inv generate              # Generate test file with Random Strategy")
    print("  inv clean                 # Remove generated files")
    print("  inv info                  # Show machine details")
    print()
    print("Running tests:")
    print("  robot out/comprehensive_rules_random.robot    # Run generated tests")
    print()
    print("Features:")
    print("  ✅ Random test generation with rule support")
    print("  ✅ Comprehensive variable condition testing")
    print("  ✅ Coverage analysis and reporting")
    print("  ✅ Maximum test and action limits (50 each)")
