import os


def abs_path(relative_path) -> str:
    '''Returns absolute path of a file from its relative path.'''
    file_path = os.path.realpath(__file__)
    return f'{os.path.dirname(os.path.dirname(file_path))}\\{relative_path}'
