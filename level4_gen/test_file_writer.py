import os
from pathlib import Path
from os.path import join

from constants import COPYRIGHT_HEADER

from formatters import parameters_to_struct_names, format_obj_func_args, format_obj_func_call_args
from file_parser import write_func_output_to_file, check_if_string_in_file, insert_line_after_in_file, append_to_file

"""
Build test files
"""

def build_test_files(blis_dir, opname, o_types, p_types, dims, num_variants):
	# build operation directory
	test_dir = Path(join(blis_dir, "testsuite"))
	src_dir  = Path(join(test_dir, "src"))
	
	repacked_params = (opname, o_types, p_types, dims, num_variants)

	file_names_and_functions = [
		(join(src_dir, f"test_libblis.c"), build_test_libflame_c),
		(join(src_dir, f"test_libblis.h"), build_test_libflame_h),
		(join(test_dir, f"input.operations"), build_input_operations),
		(join(test_dir, f"input.operations.fast"), build_input_operations),
		(join(test_dir, f"input.operations.mixed"), build_input_operations),
		(join(test_dir, f"input.operations.salt"), build_input_operations)
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

	file_names_and_functions = [
		(join(src_dir, f"test_{opname}.c"), build_test_op_c),
		(join(src_dir, f"test_{opname}.h"), build_test_op_h)
	]

	# write to file without checking if string appears 
	for file_name, function in file_names_and_functions:
		print("Writing " + file_name, end="")
		write_func_output_to_file(file_name, function, repacked_params)
		print(" -> Done.")

def build_input_operations(file_name, opname, o_types, p_types, dims, num_variants):
    new_op = \
f"""
{"1":8s} # {opname}
{" ".join(["-1"] * len(dims)):8s} #   dimensions: {" ".join([*dims])}
{"?"*len(p_types):8s} #   parameters: {" ".join(list(parameters_to_struct_names(p_types)))}
"""
    return append_to_file(file_name, new_op)


def build_test_libflame_c(file_name, opname, o_types, p_types, dims, num_variants):
    return insert_line_after_in_file(file_name, 
        ("params, &(ops->chol) );", 
         "1, &(ops->chol) );"),
        (f"\tlibblis_test_{opname}( tdata, params, &(ops->{opname}) );", 
         f"\tlibblis_test_read_op_info( ops, input_stream, BLIS_NOID,  BLIS_TEST_DIMS_{dims.upper()},   {len(p_types)}, &(ops->{opname}) );")
    )

def build_test_libflame_h(file_name, opname, o_types, p_types, dims, num_variants):
    return insert_line_after_in_file(file_name, 
        ("#include \"test_chol.h\"",       "test_op_t chol;"),
        (f"#include \"test_{opname}.h\"", f"\ttest_op_t {opname};")
    )

def build_test_op_c(file_path, opname, o_types, p_types, dims, num_variants):
    obj_func_params_formatter = ", \n       "

    return f"""{COPYRIGHT_HEADER}

#include "blis.h"
#include "test_libblis.h"


// Static variables.
static char*     op_str                    = "{opname}";
static char*     o_types                   = "{o_types}";  // TODO: add description/check here
static char*     p_types                   = "{p_types}";  // TODO: add description/check here
static thresh_t  thresh[BLIS_NUM_FP_TYPES] = {{ {{ 1e-02, 1e-03 }},   // warn, pass for s
                                               {{ 1e-02, 1e-03 }},   // warn, pass for c
                                               {{ 1e-11, 1e-12 }},   // warn, pass for d
                                               {{ 1e-11, 1e-12 }} }}; // warn, pass for z

// Local prototypes.
void libblis_test_{opname}_deps
     (
       thread_data_t* tdata,
       test_params_t* params,
       test_op_t*     op
     );

void libblis_test_{opname}_experiment
     (
       test_params_t* params,
       test_op_t*     op,
       iface_t        iface,
       char*          dc_str,
       char*          pc_str,
       char*          sc_str,
       unsigned int   p_cur,
       double*        perf,
       double*        resid
     );

void libblis_test_{opname}_impl
     (
       iface_t iface,
       {format_obj_func_args(o_types, obj_func_params_formatter)}
     );

void libblis_test_{opname}_check
     (
       test_params_t* params,
       obj_t*         a,
       obj_t*         a_orig,
       double*        resid
     );



void libblis_test_{opname}_deps
     (
       thread_data_t* tdata,
       test_params_t* params,
       test_op_t*     op
     )
{{
    // TODO: Add dependencies here!
}}



void libblis_test_{opname}
     (
       thread_data_t* tdata,
       test_params_t* params,
       test_op_t*     op
     )
{{

	// Return early if this test has already been done.
	if ( libblis_test_op_is_done( op ) ) return;

	// Return early if operation is disabled.
	if ( libblis_test_op_is_disabled( op ) ||
	     libblis_test_l4_is_disabled( op ) ) return;

	// Call dependencies first.
	if ( TRUE ) libblis_test_{opname}_deps( tdata, params, op );

	// Execute the test driver for each implementation requested.
	//if ( op->front_seq == ENABLE )
	{{
		libblis_test_op_driver( tdata,
		                        params,
		                        op,
		                        BLIS_TEST_SEQ_FRONT_END,
		                        op_str,
		                        p_types,
		                        o_types,
		                        thresh,
		                        libblis_test_{opname}_experiment );
	}}
}}



void libblis_test_{opname}_experiment
     (
       test_params_t* params,
       test_op_t*     op,
       iface_t        iface,
       char*          dc_str,
       char*          pc_str,
       char*          sc_str,
       unsigned int   p_cur,
       double*        perf,
       double*        resid
     )
{{
	unsigned int n_repeats = params->n_repeats;
	unsigned int i;

	double       time_min  = DBL_MAX;
	double       time;

	num_t        datatype;

	dim_t        m;

	obj_t        a;
	obj_t        a_save;


	// Use the datatype of the first char in the datatype combination string.
	bli_param_map_char_to_blis_dt( dc_str[0], &datatype );

	// Map the dimension specifier to actual dimensions.
	m = libblis_test_get_dim_from_prob_size( op->dim_spec[0], p_cur );

	// Map parameter characters to BLIS constants.

	// Create test operands (vectors and/or matrices).
	libblis_test_mobj_create( params, datatype, BLIS_NO_TRANSPOSE,
	                          sc_str[0], m,       m,       &a );
	libblis_test_mobj_create( params, datatype, BLIS_NO_TRANSPOSE,
	                          sc_str[0], m,       m,       &a_save );

	// Set the properties of A and A_save.
	bli_obj_set_struc( BLIS_GENERAL, &a );
	bli_obj_set_struc( BLIS_GENERAL, &a_save );

	// Randomize A
	libblis_test_mobj_randomize( params, TRUE, &a );

	// Save A.
	bli_copym( &a, &a_save );

	// Repeat the experiment n_repeats times and record results. 
	for ( i = 0; i < n_repeats; ++i )
	{{
		bli_copym( &a_save, &a );

		time = bli_clock();

		// libblis_test_{opname}_impl( iface, {format_obj_func_call_args(o_types, ", ")} );

		time_min = bli_clock_min_diff( time_min, time );
	}}

	// Estimate the performance of the best experiment repeat.
	// *perf = ( ( 1.0 / 4.0 ) * m * m * m ) / time_min / FLOPS_PER_UNIT_PERF;
	*perf = 0;
	if ( bli_obj_is_complex( &a ) ) *perf *= 4.0;

	// Perform checks.
	libblis_test_{opname}_check( params, &a, &a_save, resid );

	// Zero out performance and residual if output matrix is empty.
	libblis_test_check_empty_problem( &a, perf, resid );

	// Free the test objects.
	bli_obj_free( &a );
	bli_obj_free( &a_save );
}}



void libblis_test_{opname}_impl
     (
       iface_t iface,
       {format_obj_func_args(o_types, obj_func_params_formatter)}
     )
{{
	switch ( iface )
	{{
		case BLIS_TEST_SEQ_FRONT_END:
			bli_{opname}( {format_obj_func_call_args(o_types, ", ")} );
		break;

		default:
		libblis_test_printf_error( "Invalid interface type.\\n" );
	}}
}}



void libblis_test_{opname}_check
     (
       test_params_t* params,
       obj_t*         a,
       obj_t*         a_orig,
       double*        resid
     )
{{
	num_t  dt      = bli_obj_dt( a );
	num_t  dt_real = bli_obj_dt_proj_to_real( a );

	dim_t  m       = bli_obj_length( a );

	obj_t  norm;

	double junk;

	//
	// Pre-conditions:
	// - 
	//
	// Under these conditions, we assume that the implementation for
	//
	//   A      := {opname}(A_orig)    (uploa = lower)
	//
	// is functioning correctly if
	//
	//   normfv( x - z )
	//
	// is negligible, where
	//
	//
	//

	bli_obj_scalar_init_detached( dt_real, &norm );

	bli_getsc( &norm, resid, &junk );
}}
"""

def build_test_op_h(file_path, opname, o_types, p_types, dims, num_variants):
    return f"""{COPYRIGHT_HEADER}

void libblis_test_{opname}
     (
       thread_data_t* tdata,
       test_params_t* params,
       test_op_t*     op
     );
"""