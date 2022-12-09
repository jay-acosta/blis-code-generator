def check_if_string_in_file(file_name, string):
	with open(file_name) as file:
		return string in file.read()
