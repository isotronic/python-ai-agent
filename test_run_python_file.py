import os
from pathlib import Path
from functions.run_python_file import run_python_file


def _print_test_result(header: str, result: str):
    """Helper to print test headers and results consistently."""
    print("\n" + header)
    print(result)
    print("=" * 40)


def main():
    calculator_dir = "calculator"
    
    # Test 1: Run calculator main.py without arguments (should print usage instructions)
    result1 = run_python_file(calculator_dir, "main.py")
    _print_test_result(
        "=== Test 1: run_python_file('calculator', 'main.py') ===",
        result1
    )
    
    # Test 2: Run calculator main.py with arguments (should run the calculator)
    result2 = run_python_file(calculator_dir, "main.py", ["3 + 5"])
    _print_test_result(
        "=== Test 2: run_python_file('calculator', 'main.py', ['3 + 5']) ===",
        result2
    )
    
    # Test 3: Run calculator tests.py (should run the calculator's tests successfully)
    result3 = run_python_file(calculator_dir, "tests.py")
    _print_test_result(
        "=== Test 3: run_python_file('calculator', 'tests.py') ===",
        result3
    )
    
    # Test 4: Try to run file outside working directory (should return an error)
    result4 = run_python_file(calculator_dir, "../main.py")
    _print_test_result(
        "=== Test 4: run_python_file('calculator', '../main.py') ===",
        result4
    )
    
    # Test 5: Try to run a nonexistent file (should return an error)
    result5 = run_python_file(calculator_dir, "nonexistent.py")
    _print_test_result(
        "=== Test 5: run_python_file('calculator', 'nonexistent.py') ===",
        result5
    )
    
    # Test 6: Try to run a non-Python file (should return an error)
    result6 = run_python_file(calculator_dir, "lorem.txt")
    _print_test_result(
        "=== Test 6: run_python_file('calculator', 'lorem.txt') ===",
        result6
    )


if __name__ == "__main__":
    main()
