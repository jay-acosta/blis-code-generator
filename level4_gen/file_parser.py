def write_to_file (path, output):
	with open(path, 'w') as f:
		f.write(output)

def write_func_output_to_file(file_name, f, params):
	c = f(file_name, *params)
	print(c)
	# with open(file_name, 'w') as file:
	# 	file.write(c)
	# write_to_file(file_name, c)

def check_if_string_in_file(file_name, string):
	with open(file_name) as file:
		return string in file.read()

def append_to_file(file_name, new_line):
	with open(file_name , "r") as file:
		return "".join(file.readlines()) + new_line

def insert_line_after_in_file(read_file_name, conditions, new_lines):
	combined_replacement = list(zip(conditions, new_lines))
	def replace_line(line):
		for cond, repl in combined_replacement:
			if cond in line:
				return f"{line}{repl}\n"
		return line

	with open(read_file_name, "r+") as rfile:
		return "".join([
			replace_line(line)
			for line in rfile.readlines() 
		])

def insert_line_before_in_file(read_file_name, conditions, new_lines):
	combined_replacement = list(zip(conditions, new_lines))
	def replace_line(line):
		for cond, repl in combined_replacement:
			if cond in line:
				return f"{repl}{line}\n"
		return line

	with open(read_file_name, "r+") as rfile:
		return "".join(map(replace_line, rfile.readlines()))
