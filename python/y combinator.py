import numpy as np

# Define the Y combinator
def Y_combinator(F):
    return (lambda x: F(lambda *args: x(x)(*args)))(lambda x: F(lambda *args: x(x)(*args)))

# Define the script (E) for matrix exponentiation
matrix_exponentiation_script = lambda f: lambda matrix, exp: (
    np.eye(len(matrix), dtype=int) if exp == 0 else
    matrix if exp == 1 else
    f(matrix, exp // 2) @ f(matrix, exp // 2) if exp % 2 == 0 else
    matrix @ f(matrix, exp - 1)
)

# Combine script with Y combinator to create a recursive matrix exponentiation function
matrix_exponentiation = Y_combinator(matrix_exponentiation_script)

# Define a test matrix
test_matrix = np.array([[1, 2], [3, 4]])

# Compute the matrix raised to a power
result = matrix_exponentiation(test_matrix, 3)
print("Result of matrix exponentiation:")
print(result)
