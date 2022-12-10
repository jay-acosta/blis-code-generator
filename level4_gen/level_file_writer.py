import os
from pathlib import Path
from os.path import join

from formatters import *
from file_parser import write_func_output_to_file, check_if_string_in_file
from file_parser import append_to_file, insert_line_before_in_file

"""
Level specific files
"""

def build_level_files(blis_dir, opname, o_types, p_types, dims, num_variants):
	# build operation directory
	level4_dir = Path(join(blis_dir, "frame", "4"))
	if not level4_dir.exists():
		print(f"Making directory at {level4_dir}")
		os.makedirs(level4_dir)
	
	repacked_params = (opname, o_types, p_types, dims, num_variants)

	file_names_and_functions = [
	    (join(level4_dir, f"bli_l4_ft_opt.h"), build_l4_ft_opt_h),
	    (join(level4_dir, f"bli_l4_check.c"), build_l4_check_c),
	    (join(level4_dir, f"bli_l4_check.h"), build_l4_check_h),
	    (join(level4_dir, f"bli_l4_fpa.c"), build_l4_fpa_c),
	    (join(level4_dir, f"bli_l4_fpa.h"), build_l4_fpa_h),
	    (join(level4_dir, f"bli_l4_oft.h"), build_l4_oft_h),
	    (join(level4_dir, f"bli_l4_ft.h"), build_l4_ft_h),
	    (join(level4_dir, f"bli_l4.h"), build_l4_h)
	]

	for file_name, function in file_names_and_functions:
		if check_if_string_in_file(file_name, opname):
			# checked if opname is file
			print(f"Operation name already exists in {file_name} - skipping for now")
		elif os.path.exists(file_name):
			print("Writing " + file_name, end="")
			write_func_output_to_file(file_name, function, repacked_params)
			print(" -> Done.")
		else:
			print("An error occurred when writing " + file_name)
			print("Please edit this file before running BLIS...")

def build_l4_check_c(file_path, opname, o_types, p_types, dims, num_variants):
	obj_func_formatter = ", \n             "

	output = \
f"""
void bli_{opname}_check
     (
             {format_obj_func_args(o_types, obj_func_formatter)},
       const cntx_t* cntx
     )
{{
	err_t e_val;
	// TODO: perform error checking here

	// bli_check_error_code( e_val );
}}
"""

	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,) 
	)

def build_l4_check_h(file_path, opname, o_types, p_types, dims, num_variants):
	obj_func_formatter = ", \n             "
	output = \
f"""
void bli_{opname}_check
     (
             {format_obj_func_args(o_types, obj_func_formatter)},
       const cntx_t* cntx
     );
"""

	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,) 
	)

def build_l4_fpa_c(file_path, opname, o_types, p_types, dims, num_variants):
	output = \
f"""
#undef  GENFRONT
#define GENFRONT( opname, varname ) \\
\\
GENARRAY_FPA( PASTECH2(opname,_opt,_vft), \\
              varname ); \\
\\
PASTECH2(opname,_opt,_vft) \\
PASTEMAC(varname,_qfp)( num_t dt ) \\
{{ \\
    return PASTECH(varname,_fpa)[ dt ]; \\
}}

// GENFRONT( {opname}, {opname}_{"x" * len(p_types)}_opt_var1 )
"""

	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,) 
	)

def build_l4_fpa_h(file_path, opname, o_types, p_types, dims, num_variants):
	output = \
f"""
#undef  GENPROT
#define GENPROT( opname, varname ) \\
\\
PASTECH2(opname,_opt,_vft) \\
PASTEMAC(varname,_qfp)( num_t dt );

// GENPROT( {opname}, {opname}_{"x" * len(p_types)}_opt_var1 )
"""

	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,)
	)

def build_l4_ft_opt_h(file_path, opname, o_types, p_types, dims, num_variants):
	format_type_args = ", \\\n             "

	output = \
f"""
// {opname}

#undef  GENTDEF
#define GENTDEF( ctype, ch, opname, tsuf ) \\
\\
typedef err_t (*PASTECH3(ch,opname,_opt,tsuf)) \\
     ( \\
             {format_type_func_args(o_types, p_types, dims, format_type_args)}
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

INSERT_GENTDEF( {opname} )
"""

	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,) 
	)

def build_l4_ft_h(file_path, opname, o_types, p_types, dims, num_variants):
	type_func_args_formatter = ", \\\n             "
	output = \
f"""
// {opname}

#undef  GENTDEF
#define GENTDEF( ctype, ch, opname, tsuf ) \\
\\
typedef err_t (*PASTECH2(ch,opname,tsuf)) \\
     ( \\
             {format_type_func_args(o_types, p_types, dims, type_func_args_formatter)}
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

INSERT_GENTDEF( {opname} )
"""

	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,) 
	)

def build_l4_oft_h(file_path, opname, o_types, p_types, dims, num_variants):
	obj_arg_formatter = ", \\\n             "
	output = \
f"""// {opname}

#undef  GENTDEF
#define GENTDEF( opname ) \\
\\
typedef err_t (*PASTECH(opname,_oft)) \\
( \\
             {format_obj_func_args(o_types, obj_arg_formatter)}, \\
       const cntx_t* cntx, \\
             rntm_t* rntm, \\
             cntl_t* cntl  \\
);

GENTDEF( {opname} )

"""
	return insert_line_before_in_file(file_path,
		("#endif",),
		(output,) 
	)

def build_l4_h(file_path, opname, o_types, p_types, dims, num_variants):
	return append_to_file(file_path, f'\n#include "bli_{opname}.h"')
