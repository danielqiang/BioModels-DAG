__all__ = ['timeit']


def timeit(method):
    """
    Decorator. Prints how long a method took to execute in milliseconds.

    :param method: Method to measure and print execution time for.
    """
    import time

    def timed(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()
        print(method.__name__ + ' took ' + str(end - start) + ' seconds.')
        return result

    return timed
