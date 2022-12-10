from constants import *

SCALAR_SYMBOLS = ["alpha", "beta", "gamma", "delta"]
VECTOR_SYMBOLS = ["x", "y", "z"]
MATRIX_SYMBOLS = ["a", "b", "c", "d", "e", "f", "g", "h"]

def convert_obj_types_to_names(o_types):
	s_idx, v_idx, m_idx = 0, 0, 0

	names = []
	for object_type in o_types:
		# iterate through object types "s", "v", "m"
		# select a name for a given datatype then move to the next object
		if object_type == "s":
			names += [SCALAR_SYMBOLS[s_idx]]
			s_idx += 1
		elif object_type == "v":
			names += [VECTOR_SYMBOLS[v_idx]]
			v_idx += 1
		else:
			names += [MATRIX_SYMBOLS[m_idx]]
			m_idx += 1

	return names

def parameters_to_struct_names(p_types):
	# translate all single letter parameter types into 
	# the name of the datatype
	return map(PARAM_TMAP.__getitem__, p_types)

def convert_types_to_type_func_args(o_types):
	object_names = convert_obj_types_to_names(o_types)

	names = []

	for object_type, object_name in zip(o_types, object_names):
		if object_type == "s":
			names += [f"ctype*  {object_name}"]
		elif object_type == "v":
			names += [f"ctype*  {object_name}, inc_t inc{object_name}"]
		else:
			names += [f"ctype*  {object_name}, inc_t rs_{object_name}, inc_t cs_{object_name}"]

	return names

# idea, might be better for the separator to be outside of the return
# statement

def format_obj_func_args(o_types, separator):
	return separator.join(map(
		lambda x: f"obj_t*  {x}",
		convert_obj_types_to_names(o_types)
	))

def format_obj_func_call_args(o_types, separator):
	return separator.join(convert_obj_types_to_names(o_types))

def format_type_func_args(o_types, p_types, dims, separator):
	return \
f"""{
separator.join(map(
	lambda x: f"{x}_t  {x}a",
	parameters_to_struct_names(p_types) ))}{separator}{
separator.join(map(
	lambda x: f"dim_t   {x}",
	dims ))}{separator}{
separator.join(map(
	lambda x: x,
	convert_types_to_type_func_args(o_types) ))}, \\"""

"""
Create arguments for the control tree
"""
def cntl_create_func_args_with_a(p_types, separator):
	return separator.join(map(lambda x: f"{x}_t  {x}a", parameters_to_struct_names(p_types)))

def cntl_create_call_args_with_a(p_types, separator):
	return separator.join(map(lambda x: x + "a", parameters_to_struct_names(p_types)))

def cntl_create_args(p_types, separator):
	return separator.join(map(lambda x: f"{x}_t {x}", parameters_to_struct_names(p_types)))
