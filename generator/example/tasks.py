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
    from src.generation import Generator
    from src.generation import DepthFirstSearchStrategy, RandomStrategy, AllPairsRandomStrategy
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
        
        # Ensure out directory exists
        out_dir = current_dir / "out"
        out_dir.mkdir(exist_ok=True)
        
        # Save to file in out directory
        output_file = out_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(full_content)
        
        print(f"✅ Generated: out/{output_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {output_filename}: {e}")
        return False


@task
def generate(ctx):
    """
    Generate Robot Framework test files for all three strategies.
    
    Creates files in the out/ directory:
    - out/example_depth_first.robot (Depth-First Search Strategy)
    - out/example_random.robot (Random Strategy)  
    - out/example_all_pairs.robot (All-Pairs Strategy)
    
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
            print(f"   • out/{filename}")
        print("\n🚀 Run individual files:")
        for filename in generated_files:
            print(f"   robot out/{filename}")
        print("\n🎯 Run all files:")
        out_files = [f"out/{filename}" for filename in generated_files]
        print(f"   robot {' '.join(out_files)}")
    else:
        print("❌ No files were generated successfully")


def generate_all_pairs_with_end_state(strategy_class, output_filename, end_state=None):
    """Generate a Robot Framework test file for All-Pairs strategy with optional end state."""
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
            max_tests=10, 
            max_actions=5, 
            to_state=end_state,  # Set the target end state
            output=output, 
            strategy=strategy_class,
            all_actions=all_actions
        )
        
        result = output.getvalue()
        
        # Create Robot Framework file with proper header
        full_content = f"""{result}"""
        
        # Ensure out directory exists
        out_dir = current_dir / "out"
        out_dir.mkdir(exist_ok=True)
        
        # Save to file in out directory
        output_file = out_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(full_content)
        
        print(f"✅ Generated: out/{output_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {output_filename}: {e}")
        return False


@task
def all_pairs_to_start(ctx):
    """
    Generate Robot Framework test file using All-Pairs strategy with end state set to "Start".
    
    Creates file:
    - out/example_all_pairs_to_start.robot (All-Pairs Strategy ending in Start state)
    
    This ensures all generated test cases end in the "Start" state, which can be useful
    for testing scenarios where you want to return to the initial state.
    
    Example:
        inv all-pairs-to-start
    """
    print("🚀 Generating All-Pairs strategy test file with end state 'Start'")
    print("=" * 70)
    
    try:
        success = generate_all_pairs_with_end_state(
            AllPairsRandomStrategy, 
            "example_all_pairs_to_start.robot", 
            end_state="Start"
        )
        
        if success:
            print("\n✅ Generation Complete!")
            print("\n📋 Generated file:")
            print("   • out/example_all_pairs_to_start.robot")
            print("\n🚀 Run the test file:")
            print("   robot out/example_all_pairs_to_start.robot")
        else:
            print("\n❌ Generation failed!")
            
    except AssertionError as e:
        if "AllPairs does not work correctly with rules" in str(e):
            print("⚠️  All-Pairs strategy skipped: Cannot be used with machines that have rules")
        else:
            print(f"❌ Error with All-Pairs strategy: {e}")
    except Exception as e:
        print(f"❌ Error with All-Pairs strategy: {e}")


@task
def clean(ctx):
    """
    Clean up generated Robot Framework test files.
    
    Removes:
    - out/example_*.robot files
    - Python cache files
    
    Example:
        inv clean
    """
    print("🧹 Cleaning up generated files...")
    
    # Remove generated .robot files from out directory
    out_dir = current_dir / "out"
    robot_files = []
    if out_dir.exists():
        robot_files = list(out_dir.glob("example_*.robot"))
    
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    
    removed_count = 0
    
    # Remove generated robot files from out directory (including the new all-pairs-to-start file)
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


@task(default=True)
def help(ctx):
    """
    Show available tasks and usage information.
    """
    print("🎯 Example Machine - Test Generation Tasks")
    print("=" * 50)
    print()
    print("Available tasks:")
    print("  inv generate           - Generate Robot Framework test files for all strategies")
    print("  inv all-pairs-to-start - Generate All-Pairs strategy test file ending in 'Start' state")
    print("  inv clean              - Clean up generated test files")
    print("  inv help               - Show this help message")
    print()
    print("Generated files:")
    print("  • out/example_depth_first.robot        - Depth-First Search Strategy")
    print("  • out/example_random.robot             - Random Strategy")
    print("  • out/example_all_pairs.robot          - All-Pairs Strategy")
    print("  • out/example_all_pairs_to_start.robot - All-Pairs Strategy (ending in Start)")
    print()
    print("Usage:")
    print("  inv generate               # Generate all test files")
    print("  inv all-pairs-to-start     # Generate All-Pairs tests ending in Start state")
    print("  inv clean                  # Remove generated files")
    print()
    print("Running tests:")
    print("  robot out/example_depth_first.robot        # Run depth-first tests")
    print("  robot out/example_random.robot             # Run random tests")
    print("  robot out/example_all_pairs.robot          # Run all-pairs tests")
    print("  robot out/example_all_pairs_to_start.robot # Run all-pairs tests (to Start)")
    print("  robot out/example_*.robot                  # Run all generated tests")
