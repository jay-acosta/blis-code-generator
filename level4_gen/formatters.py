from constants import *

SCALAR_SYMBOLS = ["alpha", "beta", "gamma", "delta"]
VECTOR_SYMBOLS = ["x", "y", "z"]
MATRIX_SYMBOLS = ["a", "b", "c", "d", "e", "f", "g", "h"]

def convert_obj_to_name(o_types):
	s_idx, v_idx, m_idx = 0, 0, 0

	names = []

	for name in o_types:
		if name == "s":
			names += [SCALAR_SYMBOLS[s_idx]]
			s_idx += 1
		elif name == "v":
			names += [VECTOR_SYMBOLS[v_idx]]
			v_idx += 1
		else:
			names += [MATRIX_SYMBOLS[m_idx]]
			m_idx += 1

	return names

def convert_param_to_name(p_types):
	return map(PARAM_TMAP.__getitem__, p_types)

def format_func_arguments_inline(o_types):
	s_idx, v_idx, m_idx = 0, 0, 0

	names = []
	for name in o_types:
		if name == "s":
			n = SCALAR_SYMBOLS[s_idx]
			names += [f"ctype*  {n}"]
			s_idx += 1
		elif name == "v":
			n = VECTOR_SYMBOLS[v_idx]
			names += [f"ctype*  {n}, inc_t inc{n}"]
			v_idx += 1
		else:
			n = MATRIX_SYMBOLS[m_idx]
			names += [f"ctype*  {n}, inc_t rs_{n}, inc_t cs_{n}"]
			m_idx += 1

	return names

def format_obj_func_params(o_types, separator=", \n             "):
	return separator.join(map(
		lambda x: f"obj_t*  {x}",
		convert_obj_to_name(o_types)
	))

def cntl_create_arguments_with_a(p_types, separator):
	return separator.join(map(lambda x: f"{x}_t  {x}a", convert_param_to_name(p_types)))

def parameter_arguments_with_a(p_types, separator):
	return separator.join(map(lambda x: x + "a", convert_param_to_name(p_types)))

def cntl_create_arguments(p_types, separator):
	return separator.join(map(lambda x: f"{x}_t {x}", convert_param_to_name(p_types)))

def format_obj_func_args_multiline(o_types, separator):
	return separator.join(map(
		lambda x: f"obj_t*  {x}",
		convert_obj_to_name(o_types)
	))

def format_obj_func_args_inline(o_types, separator):
	return separator.join(convert_obj_to_name(o_types))

def format_type_func_args_multiline(o_types, p_types, dims, separator):
	return \
f"""{
separator.join(map(
	lambda x: f"{x}_t  {x}a",
	convert_param_to_name(p_types) ))}{separator}{
separator.join(map(
	lambda x: f"dim_t   {x}",
	dims ))}{separator}{
separator.join(map(
	lambda x: x,
	format_func_arguments_inline(o_types) ))}, \\"""

