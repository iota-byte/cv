import sys
import subprocess

def factorial(n):
    """Compute factorial without direct recursion."""
    if n == 0 or n == 1:
        return 1  # Base case
    else:
        # Recurse by calling the Python interpreter to execute this script again
        result = subprocess.check_output(
            ["python", __file__, str(n - 1)],
            text=True
        )
        return n * int(result.strip())

if __name__ == "__main__":
    # Entry point
    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    print(factorial(n))
