import timeit
from functools import lru_cache
import pickle
import csv
import pandas as pd

# Zmienna globalna dla formatu zapisu
SAVE_FORMAT = 'csv'


class Tree:
    def __init__(self, value):
        self.value = value
        self.children = []

    @property
    def min_value(self):
        return min([self.value] + [child.min_value for child in self.children])


def fibonacci_recursive(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_cached(n):
    if n <= 1:
        return n
    else:
        return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def save_result_to_disk(filename, result, format='pickle'):
    if format == 'pickle':
        with open(filename, 'wb') as file:
            pickle.dump(result, file)
    elif format == 'csv' or format == 'excel':
        if isinstance(result, pd.DataFrame):
            result.to_csv(filename, index=False) if format == 'csv' else result.to_excel(filename, index=False)
        else:
            result_df = pd.DataFrame(result, columns=['value'])
            result_df.to_csv(filename, index=False) if format == 'csv' else result_df.to_excel(filename, index=False)
    else:
        raise ValueError("Invalid format. Supported formats: 'pickle', 'csv', 'excel'.")


def load_result_from_disk(filename, format='pickle'):
    if format == 'pickle':
        with open(filename, 'rb') as file:
            result = pickle.load(file)
    elif format == 'csv':
        result_df = pd.read_csv(filename)
        result = result_df['value'].tolist()
    elif format == 'excel':
        result_df = pd.read_excel(filename)
        result = result_df['value'].tolist()
    else:
        raise ValueError("Invalid format. Supported formats: 'pickle', 'csv', 'excel'.")
    return result


def save_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        filename = f'{func.__name__}_result.{SAVE_FORMAT}'

        if isinstance(result, (list, pd.DataFrame)):
            save_result_to_disk(filename, result, format=SAVE_FORMAT)
        else:
            save_result_to_disk(filename, [result], format=SAVE_FORMAT)

        return result

    return wrapper


def measure_time(func, *args, **kwargs):
    start_time = timeit.default_timer()
    result = func(*args, **kwargs)
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print(f"Function {func.__name__} took {elapsed_time:.6f} seconds to execute.")
    return result


if __name__ == "__main__":
    # Utwórz instancję drzewa
    root = Tree(10)
    child1 = Tree(5)
    child2 = Tree(8)
    child3 = Tree(3)
    root.children = [child1, child2, child3]

    print("Minimum value in the tree:", root.min_value)

    n = 30
    print("\nMeasure time for Fibonacci Recursive:")
    measure_time(fibonacci_recursive, n)

    print("\nMeasure time for Fibonacci Cached:")
    measure_time(fibonacci_cached, n)


    @save_result
    def fibonacci_cached_save(n):
        return fibonacci_cached(n)


    n = 12
    print("\nMeasure time for Fibonacci Cached with Save Decorator:")
    measure_time(fibonacci_cached_save, n)

    loaded_result = load_result_from_disk('fibonacci_cached_save_result.csv', format=SAVE_FORMAT)
    print("Loaded result from disk:", loaded_result)
