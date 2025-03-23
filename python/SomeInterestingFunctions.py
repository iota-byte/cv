def add_numbers(a, b):
    # Assertion 1: Ensure both numbers are non-negative
    assert a >= 0, "First number must be non-negative"
    assert b >= 0, "Second number must be non-negative"
    
    # Add the numbers
    result = a + b
    
    assert result > 10, "The sum must be greater than 10"
    
    return result

print(add_numbers(6, 5)) 
