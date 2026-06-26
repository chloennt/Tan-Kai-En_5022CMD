#factorial function for the concurrency test
def compute_factorial(n):
    #calculate n! using a simple loop
    result = 1

    for i in range(2, n + 1): #loop runs n-1 times -> O(n)
        result *= i
    return result