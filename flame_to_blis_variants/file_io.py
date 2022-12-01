def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def dump_content_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)
