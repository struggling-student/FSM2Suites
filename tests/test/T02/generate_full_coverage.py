#!/usr/bin/env python3
"""
Comprehensive test generation script that combines multiple strategies 
to achieve maximum coverage of states and actions.
"""
import os
import sys
import subprocess
from pathlib import Path

def generate_comprehensive_tests():
    """Generate tests using multiple strategies to achieve full coverage."""
    
    current_dir = Path(__file__).parent.absolute()
    robomachine_file = current_dir / "T02.robomachine"
    
    if not robomachine_file.exists():
        print(f"❌ Error: {robomachine_file} not found")
        return False
    
    # Set up environment
    env = os.environ.copy()
    robomachine_src_path = "/Users/lucian/University/SoftwareEngineering/test/RoboMachine/src"
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{robomachine_src_path}:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = robomachine_src_path
    
    # Multiple generation strategies for comprehensive coverage
    strategies = [
        {
            "name": "DFS - Main Coverage",
            "algorithm": "dfs",
            "tests_max": 80,
            "actions_max": 15,
            "output": "T02_dfs_main.robot",
            "target_state": None
        },
        {
            "name": "Random - Edge Cases", 
            "algorithm": "random",
            "tests_max": 60,
            "actions_max": 12,
            "output": "T02_random_edge.robot", 
            "target_state": None
        },
        {
            "name": "Target PaymentFailed",
            "algorithm": "random", 
            "tests_max": 40,
            "actions_max": 10,
            "output": "T02_payment_failed.robot",
            "target_state": "PaymentFailed"
        },
        {
            "name": "Target LoginFailed",
            "algorithm": "random",
            "tests_max": 30, 
            "actions_max": 8,
            "output": "T02_login_failed.robot",
            "target_state": "LoginFailed"
        },
        {
            "name": "Target OrderConfirmed", 
            "algorithm": "random",
            "tests_max": 40,
            "actions_max": 12, 
            "output": "T02_order_confirmed.robot",
            "target_state": "OrderConfirmed"
        }
    ]
    
    print("🎯 Comprehensive Test Generation for Full Coverage")
    print("=" * 60)
    
    all_files = []
    
    for strategy in strategies:
        print(f"\n🔄 {strategy['name']}...")
        
        output_file = current_dir / strategy["output"]
        
        cmd = [
            "python3", "-m", "robomachine.runner",
            "--output", str(output_file),
            "--tests-max", str(strategy["tests_max"]),
            "--actions-max", str(strategy["actions_max"]),
            "--generation-algorithm", strategy["algorithm"],
        ]
        
        if strategy["target_state"]:
            cmd.extend(["--to-state", strategy["target_state"]])
            
        cmd.append(str(robomachine_file))
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        if output_file.exists():
            print(f"   ✅ Generated {strategy['output']}")
            all_files.append(output_file)
            
            # Extract coverage info
            if result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'tests generated' in line:
                        print(f"   📊 {line}")
                    elif 'Covered states' in line:
                        print(f"   🎯 {line}")
        else:
            print(f"   ❌ Failed to generate {strategy['output']}")
    
    # Combine all generated tests into one comprehensive file
    if all_files:
        combine_test_files(all_files, current_dir / "T02_comprehensive.robot")
    
    return True

def combine_test_files(input_files, output_file):
    """Combine multiple Robot Framework test files into one comprehensive file."""
    
    print(f"\n🔗 Combining {len(input_files)} test files into comprehensive suite...")
    
    # Read all test files and extract unique tests
    all_tests = set()
    settings_section = None
    variables_section = None
    keywords_section = None
    
    for file_path in input_files:
        if not file_path.exists():
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Extract sections
        if "*** Settings ***" in content and not settings_section:
            settings_start = content.find("*** Settings ***")
            settings_end = content.find("*** Variables ***")
            settings_section = content[settings_start:settings_end].strip()
            
        if "*** Variables ***" in content and not variables_section:
            vars_start = content.find("*** Variables ***")
            vars_end = content.find("*** Test Cases ***")
            variables_section = content[vars_start:vars_end].strip()
            
        if "*** Keywords ***" in content and not keywords_section:
            keywords_start = content.find("*** Keywords ***")
            keywords_section = content[keywords_start:].strip()
        
        # Extract test cases
        if "*** Test Cases ***" in content:
            tests_start = content.find("*** Test Cases ***") + len("*** Test Cases ***")
            tests_end = content.find("*** Keywords ***")
            if tests_end == -1:
                tests_end = len(content)
                
            tests_content = content[tests_start:tests_end].strip()
            
            # Split into individual tests and add to set
            test_blocks = tests_content.split('\n\nTest ')
            for i, block in enumerate(test_blocks):
                if i == 0:
                    # First block doesn't need "Test " prefix added back
                    if block.strip():
                        all_tests.add(block.strip())
                else:
                    # Add back the "Test " prefix
                    all_tests.add(f"Test {block.strip()}")
    
    # Write combined file
    with open(output_file, 'w') as f:
        if settings_section:
            f.write(f"{settings_section}\n\n")
        if variables_section:
            f.write(f"{variables_section}\n\n")
            
        f.write("*** Test Cases ***\n")
        
        # Sort tests and write them
        sorted_tests = sorted(all_tests)
        for i, test in enumerate(sorted_tests, 1):
            # Rename tests to have sequential numbers
            lines = test.split('\n')
            if lines[0].startswith('Test '):
                lines[0] = f"Test {i}"
            f.write('\n'.join(lines))
            f.write('\n\n')
            
        if keywords_section:
            f.write(f"{keywords_section}\n")
    
    print(f"   ✅ Combined {len(sorted_tests)} unique tests into {output_file.name}")
    print(f"   📁 Saved as: {output_file}")

if __name__ == "__main__":
    generate_comprehensive_tests()
