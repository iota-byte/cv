import os

def find_flags(start_dir):
    flag_pattern = "THM{"  
    found_flags = []

    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    if flag_pattern in content:
                        found_flags.append(file_path)
                        print(f"Flag found in: {file_path}")
                        for line in content.splitlines():
                            if flag_pattern in line:
                                print(f"  -> {line.strip()}")
            except (IOError, UnicodeDecodeError):
                continue

    if not found_flags:
        print("No flags found.")

find_flags('/')
