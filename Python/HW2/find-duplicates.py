import sys
import os
import hashlib


def read_file(path):
    file = b''
    with open(path, "rb") as f:
        file += f.read(1024)
    return file


def md5(file):
    digest = hashlib.md5()
    digest.update(file)
    return digest.hexdigest()


def find_duplicates(path):
    # Using a dictionary provides searching in O(1)
    # Store hashes as keys and lists of paths as values
    duplicates = {}
    for root, _, files in os.walk(path):
        for file in files:
            if not file.startswith(".") and not file.startswith("~"):
                file_path = os.path.join(root, file)
                if not os.path.islink(file_path):
                    file_hash = md5(read_file(file_path))
                    if file_hash in duplicates:
                        duplicates[file_hash].append(file_path)
                    else:
                        duplicates[file_hash] = [file_path]

    return duplicates


def print_duplicates(duplicates):
    for file_hash in duplicates:
        if len(duplicates[file_hash]) > 1:
            print(':'.join(duplicates[file_hash]))

for path in sys.argv[1:]:
    print_duplicates(find_duplicates(path))
