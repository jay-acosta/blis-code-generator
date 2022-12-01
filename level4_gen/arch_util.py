import os

PARAM_TMAP = {
	"s": "side",
	"u": "uplo",
	"c": "conj",
	"h": "trans",
	"d": "diag"
}

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
		# return "".join([
		# 	replace_line(line)
		# 	for line in rfile.readlines() 
		# ])
		return "".join(map(replace_line, rfile.readlines()))

def convert_obj_to_name(o_types):
	scalars = ["alpha", "beta", "gamma", "delta"]
	vectors = ["x", "y", "z"]
	matrix  = ["a", "b", "c", "d", "e", "f", "g", "h"]

	s_idx, v_idx, m_idx = 0, 0, 0

	names = []

	for name in o_types:
		if name == "s":
			names += [scalars[s_idx]]
			s_idx += 1
		elif name == "v":
			names += [vectors[v_idx]]
			v_idx += 1
		else:
			names += [matrix[m_idx]]
			m_idx += 1

	return names

def convert_param_to_name(p_types):
	return map(PARAM_TMAP.__getitem__, p_types)

def function_inline(o_types):
	scalars = ["alpha", "beta", "gamma", "delta"]
	vectors = ["x", "y", "z"]
	matrix  = ["a", "b", "c", "d", "e", "f", "g", "h"]

	s_idx, v_idx, m_idx = 0, 0, 0

	names = []
	for name in o_types:
		if name == "s":
			n = scalars[s_idx]
			names += [f"ctype*  {n}"]
			s_idx += 1
		elif name == "v":
			n = vectors[v_idx]
			names += [f"ctype*  {n}, inc_t inc{n}"]
			v_idx += 1
		else:
			n = matrix[m_idx]
			names += [f"ctype*  {n}, inc_t rs_{n}, inc_t cs_{n}"]
			m_idx += 1
	
	return names

def write_wout_check(file_name, f, params):
	print("Writing " + file_name, end="") 

	c = f(file_name, *params)
	with open(file_name, 'w') as file:
		file.write(c)
	
	print(" Done.")

def check_if_string_in_file(file_name, string):
	with open(file_name) as file:
		if string in file.read():
			return True
	return False

def write_w_check(file_name, f, params):
	if check_if_string_in_file(file_name, params[0]):
		# checked if opname is file
		print(f"Operation name already exists in {file_name} - skipping for now")
	elif os.path.exists(file_name):
		write_wout_check(file_name, f, params)
	else:
		print("An error occurred when writing " + file_name)
		print("Please edit this file before running BLIS...")
