
import os
from pathlib import Path


LIBFLAME_DIR = "/Users/jayacosta/goodflame"

if __name__ == "__main__":

    libflame_dir = Path(LIBFLAME_DIR)
    lapack_dir = os.path.join(libflame_dir, "src", "lapack")

    test_op = "Trinv"

    for dirpath, dirnames, filenames in os.walk(lapack_dir):
        if test_op in dirpath.lower():
            print (f"{dirpath} {dirnames} {filenames}")
