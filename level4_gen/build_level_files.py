import os
from pathlib import Path
from os.path import join
from arch_util import *

"""
Level specific files
"""

def build_level_files(blis_dir, opname, o_types, p_types, dims):
	# build operation directory
	level4_dir = Path(join(blis_dir, "frame", "4"))
	if not level4_dir.exists():
		print(f"Making directory at {level4_dir}")
		os.makedirs(level4_dir)
	
	repacked_params = (opname, o_types, p_types, dims)
	
	write_w_check(join(level4_dir, f"bli_l4_check.c"), build_l4_check_c, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4_check.h"), build_l4_check_h, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4_fpa.c"), build_l4_fpa_c, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4_fpa.h"), build_l4_fpa_h, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4_ft_opt.h"), build_l4_ft_opt_h, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4_ft.h"), build_l4_ft_h, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4_oft.h"), build_l4_oft_h, repacked_params)
	write_w_check(join(level4_dir, f"bli_l4.h"), build_l4_h, repacked_params)
	
def make_obj_func_params(o_types):
	return ", \n             ".join(map(
		lambda x: f"obj_t*  {x}",
		convert_obj_to_name(o_types)
	))

def build_l4_check_c(file_path, opname, o_types, p_types, dims):
	obj_func_params = make_obj_func_params(o_types)
	output = \
f"""
void bli_{opname}_check
     (
             {obj_func_params},
       const cntx_t* cntx
     )
{{
	err_t e_val;
	// TODO: perform error checking here

	// bli_check_error_code( e_val );
}}
"""
	return append_to_file(file_path, output)

def build_l4_check_h(file_path, opname, o_types, p_types, dims):
	obj_func_params = make_obj_func_params(o_types)

	output = \
f"""
void bli_{opname}_check
     (
             {obj_func_params},
       const cntx_t* cntx
     );
"""
	return append_to_file(file_path, output)

def build_l4_fpa_c(file_path, opname, o_types, p_types, dims):
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
	return append_to_file(file_path, output)

def build_l4_fpa_h(file_path, opname, o_types, p_types, dims):
	output = \
f"""
#undef  GENPROT
#define GENPROT( opname, varname ) \\
\\
PASTECH2(opname,_opt,_vft) \\
PASTEMAC(varname,_qfp)( num_t dt );

// GENPROT( {opname}, {opname}_{"x" * len(p_types)}_opt_var1 )
"""
	return append_to_file(file_path, output)

def build_l4_ft_opt_h(file_path, opname, o_types, p_types, dims):
	func_string = ", \\\n             "
	params_struc = list(convert_param_to_name(p_types))
	
	output = \
f"""
// {opname}

#undef  GENTDEF
#define GENTDEF( ctype, ch, opname, tsuf ) \\
\\
typedef err_t (*PASTECH3(ch,opname,_opt,tsuf)) \\
     ( \\
             {func_string.join(map(
                lambda x: f"{x}_t  {x}a",
                params_struc
            ))}, \\
             {func_string.join(map(
                lambda x: f"dim_t   {x}",
                dims
            ))}, \\
             {func_string.join(map(
                lambda x: x,
                function_inline(o_types)
            ))}, \\
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

INSERT_GENTDEF( {opname} )
"""
	return append_to_file(file_path, output)

def build_l4_ft_h(file_path, opname, o_types, p_types, dims):
	func_string = ", \\\n             "
	params_struc = list(convert_param_to_name(p_types))
	
	output = \
f"""
// {opname}

#undef  GENTDEF
#define GENTDEF( ctype, ch, opname, tsuf ) \\
\\
typedef err_t (*PASTECH2(ch,opname,tsuf)) \\
     ( \\
             {func_string.join(map(
                lambda x: f"{x}_t  {x}a",
                params_struc
            ))}, \\
             {func_string.join(map(
                lambda x: f"dim_t   {x}",
                dims
            ))}, \\
             {func_string.join(map(
                lambda x: x,
                function_inline(o_types)
            ))}, \\
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

INSERT_GENTDEF( {opname} )
"""
	return append_to_file(file_path, output)

def build_l4_oft_h(file_path, opname, o_types, p_types, dims):
	obj_func_params = ", \\\n             ".join(map(
		lambda x: f"obj_t* {x}",
		convert_obj_to_name(o_types)
	))

	output = \
f"""// {opname}

#undef  GENTDEF
#define GENTDEF( opname ) \\
\\
typedef err_t (*PASTECH(opname,_oft)) \\
( \\
             {obj_func_params}, \\
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

def build_l4_h(file_path, opname, o_types, p_types, dims):
	return append_to_file(file_path, f'\n#include "bli_{opname}.h"')
