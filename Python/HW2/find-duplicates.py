import sys
import os
import hashlib


def md5(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024), b''):
            digest.update(block)
    return digest.hexdigest()


def find_duplicates(path):
    # Using a dictionary provides searching in O(1)
    # Store hashes as keys and lists of paths as values
    from collections import defaultdict
    duplicates = defaultdict(list)
    for root, _, files in os.walk(path):
        for file in files:
            if file.startswith(".") or file.startswith("~"):
                continue
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                continue
            file_hash = md5(file_path)
            duplicates[file_hash].append(file_path)

    return duplicates


def print_duplicates(duplicates):
    for file_hash in duplicates:
        if len(duplicates[file_hash]) > 1:
            print(':'.join(duplicates[file_hash]))

for path in sys.argv[1:]:
    print_duplicates(find_duplicates(path))
