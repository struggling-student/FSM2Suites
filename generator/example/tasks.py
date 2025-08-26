"""
Invoke tasks for demonstrating different test generation strategies
using the example.machine file.
"""

from invoke import task
import os
import sys
import glob
from pathlib import Path
from io import StringIO

# Add the parent directory to the path so we can import the generator modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import after path modification
try:
    from src.parsing import parse
    from src.generator import Generator
    from src.strategies import DepthFirstSearchStrategy, RandomStrategy
    from src.allpairsstrategy import AllPairsRandomStrategy
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


def load_example_machine():
    """Load the example machine."""
    machine_file = current_dir / "example.machine"
    with open(machine_file, 'r') as f:
        content = f.read()
    return parse(content)


def generate_robot_file(strategy_class, output_filename):
    """Generate a Robot Framework test file for the given strategy."""
    try:
        # Load the machine
        machine = load_example_machine()
        
        # Collect all actions for coverage tracking
        all_actions = set()
        for state in machine.states:
            for action in state._actions:
                action._parent_state = state
                all_actions.add(action)
        
        # Generate tests
        generator = Generator()
        output = StringIO()
        generator.generate(
            machine, 
            max_tests=5, 
            max_actions=5, 
            output=output, 
            strategy=strategy_class,
            all_actions=all_actions
        )
        
        result = output.getvalue()
        
        # Create Robot Framework file with proper header
        full_content = f"""{result}"""
        
        # Save to file
        output_file = current_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(full_content)
        
        print(f"✅ Generated: {output_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {output_filename}: {e}")
        return False


@task
def generate(ctx):
    """
    Generate Robot Framework test files for all three strategies.
    
    Creates:
    - example_depth_first.robot (Depth-First Search Strategy)
    - example_random.robot (Random Strategy)  
    - example_all_pairs.robot (All-Pairs Strategy)
    
    Example:
        inv generate
    """
    print("🚀 Generating Robot Framework test files for all strategies")
    print("=" * 70)
    
    strategies = [
        (DepthFirstSearchStrategy, "example_depth_first.robot", "Depth-First Search"),
        (RandomStrategy, "example_random.robot", "Random"),
        (AllPairsRandomStrategy, "example_all_pairs.robot", "All-Pairs")
    ]
    
    generated_files = []
    
    for strategy_class, filename, name in strategies:
        print(f"\n🔄 Generating {name} strategy...")
        try:
            if generate_robot_file(strategy_class, filename):
                generated_files.append(filename)
        except AssertionError as e:
            if "AllPairs does not work correctly with rules" in str(e):
                print(f"⚠️  {name} strategy skipped: Cannot be used with machines that have rules")
            else:
                print(f"❌ Error with {name} strategy: {e}")
        except Exception as e:
            print(f"❌ Error with {name} strategy: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Generation Complete!")
    
    if generated_files:
        print("\n📋 Generated files:")
        for filename in generated_files:
            print(f"   • {filename}")
        print("\n🚀 Run individual files:")
        for filename in generated_files:
            print(f"   robot {filename}")
        print("\n🎯 Run all files:")
        print(f"   robot {' '.join(generated_files)}")
    else:
        print("❌ No files were generated successfully")


@task
def clean(ctx):
    """
    Clean up generated Robot Framework test files.
    
    Removes:
    - example_*.robot files
    - Python cache files
    
    Example:
        inv clean
    """
    print("🧹 Cleaning up generated files...")
    
    # Remove generated .robot files
    robot_files = glob.glob("example_*.robot")
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    
    removed_count = 0
    
    # Remove generated robot files
    for robot_file in robot_files:
        try:
            os.remove(robot_file)
            removed_count += 1
            print(f"   🗑️  Removed: {robot_file}")
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


@task(default=True)
def help(ctx):
    """
    Show available tasks and usage information.
    """
    print("🎯 Example Machine - Test Generation Tasks")
    print("=" * 50)
    print()
    print("Available tasks:")
    print("  inv generate  - Generate Robot Framework test files for all strategies")
    print("  inv clean     - Clean up generated test files")
    print("  inv help      - Show this help message")
    print()
    print("Generated files:")
    print("  • example_depth_first.robot  - Depth-First Search Strategy")
    print("  • example_random.robot       - Random Strategy")
    print("  • example_all_pairs.robot    - All-Pairs Strategy")
    print()
    print("Usage:")
    print("  inv generate              # Generate all test files")
    print("  inv clean                 # Remove generated files")
    print()
    print("Running tests:")
    print("  robot example_depth_first.robot      # Run depth-first tests")
    print("  robot example_random.robot           # Run random tests")
    print("  robot example_all_pairs.robot        # Run all-pairs tests")
    print("  robot example_*.robot                # Run all generated tests")
