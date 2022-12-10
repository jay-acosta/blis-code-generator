def read_file(path):
	with open(path, 'r') as f:
		return f.read()

def write_to_file (path, output):
	with open(path, 'w') as f:
		f.write(output)

def write_func_output_to_file(file_name, f, params):
	c = f(file_name, *params)
	write_to_file(file_name, c)

def check_if_string_in_file(file_name, string):
	with open(file_name) as file:
		return string in file.read()

def append_to_file(file_name, new_line):
	with open(file_name , "r") as file:
		return "".join(file.readlines()) + new_line

def insert_into_file(replace_function, file_path):
	with open(file_path, "r+") as rfile:
		return "".join(map(replace_function, rfile.readlines()))

def insert_line_after_in_file(file_path, conditions, new_lines):
	output = read_file(file_path)

	# only replace the last line
	for condition, replacement in zip(conditions, new_lines):
		output = f"{condition}\n{replacement}".join(output.rsplit(condition, 1))

	return output

def insert_line_before_in_file(file_path, conditions, new_lines):
	output = read_file(file_path)

	# only replace the last
	for condition, replacement in zip(conditions, new_lines):
		output = f"{replacement}{condition}\n".join(output.rsplit(condition, 1))

	return output
