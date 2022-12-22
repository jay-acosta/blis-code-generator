from re import sub
from file_io import read_file
from flame_parser import *
from format_code_sections import *
from constants import COPYRIGHT_HEADER

def translate_flame_to_blis_oapi_file(input_file):
    input_content = read_file(input_file)
    func_name = get_op_func_name_from_path(input_file)
    ftype = get_type_from_func_name(func_name)
    updates = translate_flame_updates_to_blis(ftype, input_content)

    define_b_alg = format_define_b_alg(ftype)
    calc_b_alg = format_calc_b_alg(ftype)

    loop_body = format_loop_body(ftype, updates)
    func_args = format_func_args(input_content)
    partitions = format_partition_step(ftype, input_content, updates)
    repartitions = format_repartition_step(ftype, input_content, updates)
    loop_conditional = format_loop_conditional(ftype, input_content)

    return \
f"""{COPYRIGHT_HEADER}

#include "blis.h"

#ifdef BLIS_ENABLE_LEVEL4

err_t {func_name}
     (
{func_args},
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{{
	const dim_t m = bli_obj_length( a );
	{partitions}
	{define_b_alg}
	for ( {loop_conditional} )
	{{
		{calc_b_alg}
		{repartitions}
		{loop_body}
	}}

	return BLIS_SUCCESS;
}}

#endif
"""

def translate_flame_to_blis_tapi_file(input_file):
    input_content = read_file(input_file)
    func_name = sub("(blk|unb)", "opt", get_op_func_name_from_path(input_file))
    op_name = get_op_func_name_from_path(input_file).split("_")[1]
    ftype = "opt"
    updates = translate_flame_updates_to_blis(ftype, input_content)

    # define_b_alg = ""
    # calc_b_alg = ""
    # if ftype == "blk":
    #     define_b_alg = "dim_t b_alg;"
    #     calc_b_alg = "b_alg = bli_chol_determine_blocksize( ij, m, a, cntx, cntl );"

    loop_body = format_loop_body(ftype, updates)
    func_args = format_func_args(input_content)
    # partitions, repartitions = formatted_partition_steps(ftype, input_content, update_statements)
    # loop_conditional = format_loop_conditional(ftype, input_content)

    return \
f"""{COPYRIGHT_HEADER}

#include "blis.h"

#ifdef BLIS_ENABLE_LEVEL4

err_t {func_name}
     (
{func_args},
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{{
	/* TODO: fill out this area */

	/*
	num_t     dt        = bli_obj_dt( a );

	uplo_t    uploa     = bli_obj_uplo( a );
	diag_t    diaga     = bli_obj_diag( a );
	dim_t     m         = bli_obj_length( a );
	void*     buf_a     = bli_obj_buffer_at_off( a );
	inc_t     rs_a      = bli_obj_row_stride( a );
	inc_t     cs_a      = bli_obj_col_stride( a );
	*/

	if ( bli_error_checking_is_enabled() )
		PASTEMAC({op_name},_check)( {", ".join(get_op_func_args(input_content))}, cntx );

	// Query a type-specific function pointer, except one that uses
	// void* for function arguments instead of typed pointers.
	{op_name}_opt_vft f = PASTEMAC({func_name.replace("bli_", "")},_qfp)( dt );

	/*
	 TODO: figure out function call here
	*/
	return
	f
	(
	  uploa,
	  diaga,
	  m,
	  buf_a, rs_a, cs_a,
	  cntx,
	  rntm
	);
}}

#undef  GENTFUNCR
#define GENTFUNCR( ctype, ctype_r, ch, chr, varname ) \\
\\
err_t PASTEMAC(ch,varname) \\
     ( \\
             /*
             TODO: FILL IN PARAMETERS HERE!
             */ \\
     ) \\
{{ \\
\\
	const ctype one       = *PASTEMAC(ch,1); \\
	const ctype minus_one = *PASTEMAC(ch,m1); \\
\\
	for ( dim_t i = 0; i < m; ++i ) \\
	{{ \\
		const dim_t mn_behind = i; \\
		const dim_t mn_ahead  = m - i - 1; \\
\\
		/* Identify subpartitions: /  a00  a01      a02  \\
		                           |  a10  alpha11  a12  |
		                           \  a20  a21      a22  / */ \\
\\
		ctype*   a00       = a + (0  )*rs_a + (0  )*cs_a; \\
		ctype*   a01       = a + (0  )*rs_a + (i  )*cs_a; \\
		ctype*   a02       = a + (0  )*rs_a + (i+1)*cs_a; \\
		ctype*   a10       = a + (i  )*rs_a + (0  )*cs_a; \\
		ctype*   alpha11   = a + (i  )*rs_a + (i  )*cs_a; \\
		ctype*   a12       = a + (i  )*rs_a + (i+1)*cs_a; \\
		ctype*   a20       = a + (i+1)*rs_a + (0  )*cs_a; \\
		ctype*   a21       = a + (i+1)*rs_a + (i  )*cs_a; \\
		ctype*   a22       = a + (i+1)*rs_a + (i+1)*cs_a; \\
\\
{ loop_body }\\
	}} \\
\\
	return BLIS_SUCCESS; \\
}}

INSERT_GENTFUNCR_BASIC0( {func_name.replace("bli_","")} )

#endif
"""

