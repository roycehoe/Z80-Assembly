from pathlib import Path
from functools import partial
from io import DEFAULT_BUFFER_SIZE

def file_byte_iterator(path = './Pokemon_red.dump'):
    """given a path, return an iterator over the file
    that lazily loads the file
    """
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read1, DEFAULT_BUFFER_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            yield from chunk

print(list(file_byte_iterator()))