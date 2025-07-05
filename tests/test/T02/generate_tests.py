#!/usr/bin/env python3
"""
Generate Robot Framework test cases from RoboMachine model for Shopping Cart testing.
"""
import os
import sys
import subprocess
from pathlib import Path

def generate_tests():
    """Generate tests from the RoboMachine model."""
    
    # Get current directory
    current_dir = Path(__file__).parent.absolute()
    
    # Input and output files
    robomachine_file = current_dir / "T02.robomachine"
    output_file = current_dir / "T02_generated.robot"
    
    # Check if RoboMachine file exists
    if not robomachine_file.exists():
        print(f"Error: RoboMachine file not found: {robomachine_file}")
        return False
    
    print(f"Generating tests from: {robomachine_file}")
    print(f"Output file: {output_file}")
    
    try:
        # Set up environment with RoboMachine source path
        env = os.environ.copy()
        robomachine_src_path = "/Users/lucian/University/SoftwareEngineering/test/RoboMachine/src"
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{robomachine_src_path}:{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = robomachine_src_path
        
        # Generate tests using RoboMachine
        # Using the robomachine command with various strategies
        
        # Strategy 1: Comprehensive coverage using multiple approaches
        cmd_all = [
            "python3", "-c", 
            "exec(open('generate_full_coverage.py').read())"
        ]
        
        print("Running RoboMachine generator...")
        print(" ".join(cmd_all))
        
        result = subprocess.run(cmd_all, capture_output=True, text=True, env=env, cwd=current_dir)
        
        # The comprehensive script creates T02_comprehensive.robot, rename it to our expected output
        comprehensive_file = current_dir / "T02_comprehensive.robot" 
        if comprehensive_file.exists():
            comprehensive_file.rename(output_file)
        
        # Check if the output file was generated, even if return code is non-zero
        # (RoboMachine might fail when trying to run tests but succeed in generating them)
        if output_file.exists():
            print("✅ Test generation successful!")
            print(f"Generated tests saved to: {output_file}")
            
            # Print RoboMachine output for information
            if result.stdout:
                print("\n📋 RoboMachine output:")
                print(result.stdout)
            
            # Show some statistics
            with open(output_file, 'r') as f:
                content = f.read()
                test_count = content.count('*** Test Cases ***')
                if test_count > 0:
                    # Count individual test cases
                    lines = content.split('\n')
                    test_case_count = 0
                    in_test_section = False
                    
                    for line in lines:
                        if '*** Test Cases ***' in line:
                            in_test_section = True
                            continue
                        elif line.startswith('***') and in_test_section:
                            break
                        elif in_test_section and line.strip() and not line.startswith(' '):
                            test_case_count += 1
                    
                    print(f"📊 Generated {test_case_count} test cases")
                
            return True
        else:
            print("❌ Test generation failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ Error: robomachine not found in Python path")
        print("Make sure RoboMachine is installed:")
        print("pip install robomachine")
        return False
    except Exception as e:
        print(f"❌ Error generating tests: {e}")
        return False

def generate_with_different_strategies():
    """Generate tests with different RoboMachine strategies."""
    
    current_dir = Path(__file__).parent.absolute()
    robomachine_file = current_dir / "T02.robomachine"
    
    strategies = [
        ("depth-first", "T02_depth_first.robot"),
        ("random", "T02_random.robot"),
        ("allpairs-random", "T02_allpairs.robot")
    ]
    
    print("🚀 Generating tests with multiple strategies...")
    
    for strategy, output_name in strategies:
        output_file = current_dir / output_name
        
        cmd = [
            "python", "-m", "robomachine.runner",
            "--output", str(output_file),
            "--tests-max", "30",
            "--generation-algorithm", strategy,
            str(robomachine_file)
        ]
        
        print(f"\n📋 Generating with {strategy} strategy...")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {strategy} strategy successful!")
                print(f"   Output: {output_file}")
            else:
                print(f"❌ {strategy} strategy failed:")
                print(f"   {result.stderr}")
        except Exception as e:
            print(f"❌ Error with {strategy}: {e}")

if __name__ == "__main__":
    print("🛒 Shopping Cart RoboMachine Test Generator")
    print("=" * 50)
    
    # Check if we should generate with multiple strategies
    if len(sys.argv) > 1 and sys.argv[1] == "--all-strategies":
        generate_with_different_strategies()
    else:
        success = generate_tests()
        
        if success:
            print("\n🎉 Test generation completed!")
            print("\nNext steps:")
            print("1. Review the generated test file")
            print("2. Make sure your shopping app is running:")
            print("   - Frontend: http://localhost:5173")
            print("   - Backend: http://localhost:8000")
            print("3. Install Selenium WebDriver for Chrome")
            print("4. Run the tests with: python run_tests.py")
        else:
            print("\n💥 Test generation failed!")
            print("Please check the error messages above.")
            sys.exit(1)
