import os
import sys
from typing import List


def tail(file_path: str, n_lines=5) -> List[str]:
    """ Returns the last n_lines of the given file """
    with open(os.path.expanduser(file_path), "rb") as f:
        f.seek(-2, os.SEEK_END)
        counter = 0
        while counter < n_lines:
            f.seek(-2, os.SEEK_CUR)
            if f.read(1) == b"\n":
                counter += 1
        lines = f.readlines()
    return [l.decode("UTF-8") for l in lines]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: seek.py path/to/file")
        sys.exit(1)

    last_lines = tail(sys.argv[1])

    print("".join(last_lines), end="")
