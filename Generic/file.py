

def read_file(file_path):
    with open(file_path, 'r') as file:
        return ''.join(file.readlines())


