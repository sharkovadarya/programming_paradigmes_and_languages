import sys, os, hashlib

def md5(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        digest.update(f.read())
    return digest.hexdigest()

def find_duplicates(path):
    # Using a dictionary provides searching in O(1)
    # Store hashes as keys and lists of pathes as values
    from collections import defaultdict
    duplicates = defaultdict(list)
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.startswith(".") and not file.startswith("~"):
                file_path = os.path.join(root, file)
                file_hash = md5(file_path)
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