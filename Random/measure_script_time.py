import timeit
from pastpapersolver import main
def measure_speed(stmt, setup='pass', number=10):
    """
    Measures the execution time of a Python statement.

    :param stmt: The statement to measure (as a string).
    :param setup: Setup code to run before timing (as a string).
    :param number: The number of times to execute the statement.
    :return: The average execution time per execution.
    """
    time_taken = timeit.timeit(stmt, setup=setup, number=number,globals=globals())
    return time_taken / number


time = measure_speed("main()")
print(f"The time taken for one run of this function is: {time}")