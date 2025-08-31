"""
Invoke tasks for generating Robot Framework tests from example machine files.
This script creates organized examples for oral exam demonstrations.
"""

from invoke import task
import os
import sys
import glob
from pathlib import Path
from io import StringIO

# Add the parent directory to the path so we can import the generator modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

# Import after path modification
try:
    from generator.src.parsing import parse
    from generator.src.generation import Generator
    from generator.src.generation import DepthFirstSearchStrategy, RandomStrategy, AllPairsRandomStrategy
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


def get_machine_files():
    """Get all .machine files in the current directory."""
    return sorted(Path(current_dir).glob("*.machine"))


def load_machine(machine_file):
    """Load a machine from file."""
    with open(machine_file, 'r') as f:
        content = f.read()
    return parse(content)


def generate_robot_file(machine_file, strategy_class, output_dir):
    """Generate a Robot Framework test file for the given strategy and machine."""
    try:
        # Load the machine
        machine = load_machine(machine_file)
        
        # Collect all actions for coverage tracking
        all_actions = set()
        for state in machine.states:
            for action in state._actions:
                action._parent_state = state
                all_actions.add(action)
        
        # Generate tests
        generator = Generator()
        output = StringIO()
        
        # Determine test parameters based on machine complexity
        max_tests = 3
        max_actions = 6
        
        generator.generate(
            machine, 
            max_tests=max_tests, 
            max_actions=max_actions, 
            output=output, 
            strategy=strategy_class,
            all_actions=all_actions
        )
        
        result = output.getvalue()
        
        # Create output filename
        machine_name = machine_file.stem
        strategy_name = strategy_class.__name__.replace('Strategy', '').lower()
        output_filename = f"{machine_name}_{strategy_name}.robot"
        
        # Save to file in output directory
        output_file = output_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(result)
        
        return output_filename
        
    except Exception as e:
        print(f"❌ Error generating {machine_file.name} with {strategy_class.__name__}: {e}")
        return None


@task
def generate(ctx, machine=None, strategy=None):
    """
    Generate Robot Framework test files for example machines.
    
    Args:
        machine: Specific machine file to process (optional, defaults to all)
        strategy: Specific strategy to use (dfs, random, allpairs, defaults to all)
    
    Creates organized output in subdirectories:
    - out/01_basic_login/        - Basic login examples
    - out/02_complex_permissions/ - Complex permission rules  
    - out/03_shopping_cart/      - Shopping cart with comparisons
    - out/04_user_registration/  - User registration with regex
    - out/05_complex_parsing/    - Complex state machine parsing
    - out/06_logical_operators/  - Logical operator demonstrations
    
    Examples:
        inv generate                           # Generate all examples
        inv generate --machine=01_basic_login  # Generate specific machine
        inv generate --strategy=dfs            # Use only depth-first strategy
    """
    print("🚀 Generating Robot Framework examples for oral exam")
    print("=" * 70)
    
    # Get machine files to process
    machine_files = get_machine_files()
    if machine:
        machine_files = [f for f in machine_files if machine in f.name]
        if not machine_files:
            print(f"❌ No machine file found matching: {machine}")
            return
    
    # Define strategies to use
    strategies = [
        (DepthFirstSearchStrategy, "dfs", "Depth-First Search"),
        (RandomStrategy, "random", "Random"),
        (AllPairsRandomStrategy, "allpairs", "All-Pairs")
    ]
    
    if strategy:
        strategies = [s for s in strategies if strategy in s[1]]
        if not strategies:
            print(f"❌ No strategy found matching: {strategy}")
            return
    
    total_generated = 0
    
    for machine_file in machine_files:
        print(f"\n📁 Processing: {machine_file.name}")
        print(f"   Description: {get_machine_description(machine_file)}")
        
        # Create output directory for this machine
        machine_name = machine_file.stem
        output_dir = current_dir / "out" / machine_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = []
        
        for strategy_class, strategy_short, strategy_name in strategies:
            print(f"   🔄 Generating {strategy_name} strategy...")
            try:
                filename = generate_robot_file(machine_file, strategy_class, output_dir)
                if filename:
                    generated_files.append(filename)
                    total_generated += 1
                    print(f"      ✅ Generated: {machine_name}/{filename}")
            except AssertionError as e:
                if "AllPairs does not work correctly with rules" in str(e):
                    print(f"      ⚠️  {strategy_name} strategy skipped: Cannot be used with machines that have rules")
                else:
                    print(f"      ❌ Error with {strategy_name} strategy: {e}")
            except Exception as e:
                print(f"      ❌ Error with {strategy_name} strategy: {e}")
        
        # Files generated successfully
    
    print("\n" + "=" * 70)
    print(f"✅ Generation Complete! Generated {total_generated} files")
    
    if total_generated > 0:
        print("\n📂 Generated examples:")
        for machine_file in machine_files:
            machine_name = machine_file.stem
            output_dir = current_dir / "out" / machine_name
            if output_dir.exists():
                robot_files = list(output_dir.glob("*.robot"))
                if robot_files:
                    print(f"   📁 {machine_name}/")
                    for robot_file in sorted(robot_files):
                        print(f"      🤖 {robot_file.name}")
        
        print("\n🚀 Generated examples for oral exam presentation:")
        print("   cd tests/example")
        print("   inv generate                    # Generate all examples")
        print("   inv generate --machine=01       # Generate specific machine")


def get_machine_description(machine_file):
    """Get a description of what the machine demonstrates."""
    descriptions = {
        "01_basic_login_fixed": "Basic login system with simple implication rules", 
        "07_simple_shopping": "Simple shopping cart with comparison operators",
        "08_logical_simple": "Logical operators and rules demonstration"
    }
    
    for key, desc in descriptions.items():
        if key in machine_file.name:
            return desc
    return "Example machine file"


@task
def clean(ctx):
    """
    Clean up generated Robot Framework test files and output directories.
    
    Removes:
    - out/ directory and all contents
    - Python cache files
    - Robot Framework logs and reports
    
    Example:
        inv clean
    """
    print("🧹 Cleaning up generated files...")
    
    removed_count = 0
    
    # Remove output directory
    out_dir = current_dir / "out" 
    if out_dir.exists():
        import shutil
        shutil.rmtree(out_dir)
        removed_count += 1
        print("   🗑️  Removed: out/ directory")
    
    # Remove Robot Framework output files
    rf_files = []
    rf_files.extend(glob.glob("*.html"))
    rf_files.extend(glob.glob("*.xml"))
    rf_files.extend(glob.glob("log.html"))
    rf_files.extend(glob.glob("report.html"))
    rf_files.extend(glob.glob("output.xml"))
    
    for rf_file in rf_files:
        try:
            os.remove(rf_file)
            removed_count += 1
            print(f"   🗑️  Removed: {rf_file}")
        except OSError:
            pass
    
    # Remove Python cache files
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    
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
def list_examples(ctx):
    """
    List all available example machine files with descriptions.
    """
    print("📋 Available Example Machine Files")
    print("=" * 50)
    
    machine_files = get_machine_files()
    
    if not machine_files:
        print("❌ No machine files found")
        return
    
    for machine_file in machine_files:
        print(f"\n📁 {machine_file.name}")
        print(f"   📝 {get_machine_description(machine_file)}")
        
        # Try to parse and show basic info
        try:
            machine = load_machine(machine_file)
            print(f"   📊 {len(machine.variables)} variables, {len(machine.states)} states, {len(machine.rules)} rules")
        except Exception as e:
            print(f"   ❌ Parse error: {e}")


@task(default=True)
def help(ctx):
    """
    Show available tasks and usage information for oral exam examples.
    """
    print("🎓 Oral Exam Examples - Test Generation Tasks")
    print("=" * 60)
    print()
    print("📁 Example Machine Files:")
    print("  01_basic_login_fixed.machine     - Basic login with implication rules")
    print("  07_simple_shopping.machine       - Shopping cart with comparison operators")
    print("  08_logical_simple.machine        - Logical operators and rules demonstration")
    print()
    print("🚀 Available Tasks:")
    print("  inv generate                  - Generate Robot Framework tests")
    print("  inv generate --machine=01     - Generate specific machine")
    print("  inv generate --strategy=dfs   - Use specific strategy")
    print("  inv clean                     - Remove generated files")
    print("  inv list-examples             - List all examples")
    print("  inv help                      - Show this help")
    print()
    print("🎯 Demonstration Focus Areas:")
    print("  • Rule Logic: Implication rules and logical operators")
    print("  • Parsing: State machines with various constructs")
    print("  • Strategies: Different test generation approaches")
    print("  • Comparison: Numerical comparison operators")
    print()
    print("💡 Usage Examples:")
    print("  inv generate                          # Generate all examples")
    print("  inv generate --machine=01_basic       # Focus on basic login")
    print("  inv generate --strategy=random        # Use random strategy")
    print("  inv clean                             # Clean up generated files")
