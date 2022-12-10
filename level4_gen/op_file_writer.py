from pathlib import Path
from os import makedirs
from os.path import join
from formatters import *
from file_parser import write_func_output_to_file

from constants import *

"""
Operation specific files
"""
def write_operation_files(blis_dir, opname, o_types, p_types, dims, num_vars):
	# build operation directory
	op_dir = Path(join(blis_dir, "frame", "4", opname))

	# build the frame/4/<operation_name> directory if it
	# does not yet exist
	if not op_dir.exists():
		print(f"Making directory at {op_dir}")
		makedirs(op_dir)

	repacked_params = (opname, o_types, p_types, dims, num_vars)

	file_names_and_functions = [
	    (join(op_dir, f"bli_{opname}_blksz.c"), build_bli_op_blksz_c),
	    (join(op_dir, f"bli_{opname}_blksz.h"), build_bli_op_blksz_h),
	    (join(op_dir, f"bli_{opname}_cntl.c"), build_bli_op_cntl_c),
	    (join(op_dir, f"bli_{opname}_cntl.h"), build_bli_op_cntl_h),
	    (join(op_dir, f"bli_{opname}_int.c"), build_bli_op_int_c),
	    (join(op_dir, f"bli_{opname}_int.h"), build_bli_op_int_h),
	    (join(op_dir, f"bli_{opname}_var.h"), build_bli_op_var_h),
	    (join(op_dir, f"bli_{opname}.c"), build_bli_op_c),
	    (join(op_dir, f"bli_{opname}.h"), build_bli_op_h)
	]

	for file_name, function in file_names_and_functions:
		print("Writing " + file_name, end="")
		write_func_output_to_file(file_name, function, repacked_params)
		print(" -> Done.")

"""
bli_<opname>_blksz.c and bli_<opname>_blksz.h
"""
def build_bli_op_blksz_c(file_path, opname, o_types, p_types, dims, num_vars):
	return \
f"""{COPYRIGHT_HEADER}
#include "blis.h"

#ifdef BLIS_ENABLE_LEVEL4

dim_t bli_{opname}_determine_blocksize
     (
             dim_t   i,
             dim_t   dim,
       const obj_t*  obj,
       const cntx_t* cntx,
             cntl_t* cntl
     )
{{
	// Query the numerator and denomenator to use to scale the blocksizes
	// that we query from the context.
	const {opname}_params_t* params   = bli_cntl_params( cntl );
	const dim_t           scale_num = bli_{opname}_params_scale_num( params );
	const dim_t           scale_den = bli_{opname}_params_scale_den( params );
	const bszid_t         bszid     = bli_cntl_bszid( cntl );

	// Extract the execution datatype and use it to query the corresponding
	// blocksize and blocksize maximum values from the blksz_t object.
	const num_t    dt     = bli_obj_exec_dt( obj );
	const blksz_t* bsize  = bli_cntx_get_blksz( bszid, cntx );
	const dim_t    b_def0 = bli_blksz_get_def( dt, bsize );
	const dim_t    b_max0 = bli_blksz_get_max( dt, bsize );

	// Scale the queried blocksizes by the scalars.
	const dim_t    b_def  = ( b_def0 * scale_num ) / scale_den;
	const dim_t    b_max  = ( b_max0 * scale_num ) / scale_den;

	// Compute how much of the matrix dimension is left, including the
	// chunk that will correspond to the blocksize we are computing now.
	const dim_t dim_left_now = dim - i;

	// If the dimension currently remaining is less than the maximum
	// blocksize, use it instead of the default blocksize b_def.
	// Otherwise, use b_def.
	dim_t b_now;
	if ( dim_left_now <= b_max ) b_now = dim_left_now;
	else                         b_now = b_def;

	return b_now;
}}

#endif
"""

def build_bli_op_blksz_h(file_path, opname, o_types, p_types, dims, num_vars):
	return \
f"""{COPYRIGHT_HEADER}
#ifndef BLIS_{opname.upper()}_BLKSZ_H
#define BLIS_{opname.upper()}_BLKSZ_H

dim_t bli_{opname}_determine_blocksize
     (
             dim_t   i,
             dim_t   dim,
       const obj_t*  obj,
       const cntx_t* cntx,
             cntl_t* cntl
     );

#endif
"""

"""
bli_<opname>_cntl.c and bli_<opname>_cntl.h
"""
def build_bli_op_cntl_c(file_path, opname, o_types, p_types, dims, num_vars):
	# get the number of parameters
	np = len(p_types)

	arg_formatter = ", \n       "

	return \
f"""{COPYRIGHT_HEADER}
#include "blis.h"

#ifdef BLIS_ENABLE_LEVEL4

/*
// TODO: Change this to include all of your variants
static {opname}_oft unb_vars{"[2]"*np} = 
{{
	bli_chol_l_unb_var3, bli_chol_u_unb_var3
}};

static {opname}_oft blk_vars{"[2]"*np} = 
{{
}};
*/

cntl_t* bli_{opname}_cntl_create
     (
       {cntl_create_func_args_with_a(p_types, arg_formatter)},
       rntm_t* rntm
     )
{{

	// TODO: Extract parameters
	// dim_t uplo;

	// if ( bli_is_lower( uploa ) )      uplo = 0;
	// else                              uplo = 1;

	// TODO: Specify unblocked and blocked functions
	{opname}_oft unb_fp = NULL;
	{opname}_oft blk_fp = NULL;

	cntl_t* {opname}_{"x"*np}_leaf = bli_{opname}_cntl_create_node
	    (
	        rntm,
	        BLIS_NO_PART,
	        1, 1,
	        2,
	        unb_fp,
	        NULL
	    );

	cntl_t* {opname}_{"x"*np}_inner = bli_{opname}_cntl_create_node
	    (
	        rntm,
	        BLIS_NO_PART,
	        1, 1,
	        1,
	        blk_fp,
	        {opname}_{"x"*np}_leaf
	    );

	cntl_t* {opname}_{"x"*np}_outer = bli_{opname}_cntl_create_node
	    (
	        rntm,
	        BLIS_NO_PART,
	        1, 1,
	        0,
	        blk_fp,
	        {opname}_{"x"*np}_inner
	    );

	return {opname}_{"x"*np}_outer;
}}

// -----------------------------------------------------------------------------

void bli_{opname}_cntl_free
     (
       rntm_t*    rntm,
       cntl_t*    cntl,
       thrinfo_t* thread
     )
{{
	bli_cntl_free( rntm, cntl, thread );
}}

// -----------------------------------------------------------------------------

cntl_t* bli_{opname}_cntl_create_node
     (
       rntm_t* rntm,
       bszid_t bszid,
       dim_t   scale_num,
       dim_t   scale_den,
       dim_t   depth,
       void_fp var_func,
       cntl_t* sub_node
     )
{{
	{opname}_params_t* params = bli_sba_acquire( rntm, sizeof( {opname}_params_t ) );

	params->size      = sizeof( {opname}_params_t );
	params->scale_num = scale_num;
	params->scale_den = scale_den;
	params->depth     = depth;

	return bli_cntl_create_node
	(
	  rntm,
	  BLIS_NOID,
	  bszid,
	  var_func,
	  params,
	  sub_node
	);
}}

#endif
"""

def build_bli_op_cntl_h(file_path, opname, o_types, p_types, dims, num_vars):
	return \
f"""{COPYRIGHT_HEADER}
#ifndef BLIS_{opname.upper()}_CNTL_H
#define BLIS_{opname.upper()}_CNTL_H

typedef struct
{{
	uint64_t size;
	dim_t    scale_num;
	dim_t    scale_den;
	dim_t    depth;
}} {opname}_params_t;

BLIS_INLINE dim_t bli_{opname}_params_scale_num( const {opname}_params_t* params )
{{
	return params->scale_num;
}}

BLIS_INLINE dim_t bli_{opname}_params_scale_den( const {opname}_params_t* params )
{{
	return params->scale_den;
}}

BLIS_INLINE dim_t bli_{opname}_params_depth( const {opname}_params_t* params )
{{
	return params->depth;
}}

// -----------------------------------------------------------------------------

cntl_t* bli_{opname}_cntl_create( {cntl_create_args(p_types, ", ")}, rntm_t* rntm );

// -----------------------------------------------------------------------------

void bli_{opname}_cntl_free( rntm_t* rntm, cntl_t* cntl, thrinfo_t* thread );

// -----------------------------------------------------------------------------

cntl_t* bli_{opname}_cntl_create_node
     (
       rntm_t* rntm,
       bszid_t bszid,
       dim_t   scale_num,
       dim_t   scale_den,
       dim_t   depth,
       void_fp var_func,
       cntl_t* sub_node
     );

#endif
"""

"""
bli_<opname>_int.c and bli_<opname>_int.h
"""
def build_bli_op_int_c(file_path, opname, o_types, p_types, dims, num_vars):
	multiline_formatter = ", \n             "

	return \
f"""{COPYRIGHT_HEADER}
#include "blis.h"

#ifdef BLIS_ENABLE_LEVEL4

err_t bli_{opname}_int
     (
             {format_obj_func_args(o_types, multiline_formatter)},
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{{
	{opname}_oft {opname}_fp = bli_cntl_var_func( cntl );

	return {opname}_fp( {format_obj_func_call_args(o_types, ", ")}, cntx, rntm, cntl );
}}

#endif
"""

def build_bli_op_int_h(file_path, opname, o_types, p_types, dims, num_vars):
	arg_formatter = ", \n             "

	return \
f"""{COPYRIGHT_HEADER}
#include "blis.h"

#ifndef BLIS_{opname.upper()}_INT_H
#define BLIS_{opname.upper()}_INT_H

err_t bli_{opname}_int
     (
             {format_obj_func_args(o_types, arg_formatter)},
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     );

#endif
"""

"""
bli_<opname>_var.h
"""
def build_bli_op_var_h(file_path, opname, o_types, p_types, dims, num_vars):
	obj_func_args_formatter = ", \\\n             "
	multiline_formatter = f", \\\n             "

	return \
f"""{COPYRIGHT_HEADER}
#ifndef BLIS_{opname.upper()}_VAR_H
#define BLIS_{opname.upper()}_VAR_H

//
// Prototype object-based interfaces.
//

#undef  GENPROT
#define GENPROT( opname ) \\
\\
err_t PASTEMAC0(opname) \\
     ( \\
             {format_obj_func_args(o_types, obj_func_args_formatter)}, \\
       const cntx_t* cntx, \\
             rntm_t* rntm, \\
             cntl_t* cntl  \\
     );

//TODO: INSERT ALL INVARIANT NAMES HERE!
//GENPROT(  )

//
// Prototype BLAS-like interfaces with void pointer operands.
//

#undef  GENTPROT
#define GENTPROT( ctype, ch, varname ) \\
\\
err_t PASTEMAC(ch,varname) \\
     ( \\
             {format_type_func_args(o_types, p_types, dims, multiline_formatter)}
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

//TODO: INSERT OPTIMIZED INVARIANT NAMES HERE!
//INSERT_GENTPROT_BASIC0(  )

#endif
"""

"""
bli_<opname>.c and bli_<opname>.h
"""
def build_bli_op_c(file_path, opname, o_types, p_types, dims, num_vars):
	multiline_formatter = ",\n       "

	return \
f"""{COPYRIGHT_HEADER}
#include "blis.h"

#ifdef BLIS_ENABLE_LEVEL4

err_t bli_{opname}
     (
       {format_obj_func_args(o_types, multiline_formatter)}
     )
{{
	return bli_{opname}_ex( {format_obj_func_call_args(o_types, ", ")}, NULL, NULL );
}}

err_t bli_{opname}_ex
     (
       {format_obj_func_args(o_types, multiline_formatter)},
       const cntx_t* cntx,
             rntm_t* rntm
     )
{{
	bli_init_once();

	if ( bli_error_checking_is_enabled() )
		bli_{opname}_check( {format_obj_func_call_args(o_types, ", ")}, cntx );

	// If necessary, obtain a valid context from the gks using the induced
	// method id determined above.
	if ( cntx == NULL ) cntx = bli_gks_query_cntx();

	// Initialize a local runtime with global settings if necessary. Note
	// that in the case that a runtime is passed in, we make a local copy.
	rntm_t rntm_l;
	if ( rntm == NULL ) {{ bli_rntm_init_from_global( &rntm_l ); rntm = &rntm_l; }}
	else                {{ rntm_l = *rntm;                       rntm = &rntm_l; }}

	// TODO: CHOOSE CORRECT PARAMETERS HERE
	{f"{NL}{TB}".join(map(
		lambda x: f"const {x}_t {x}a = bli_obj_{x}( a );",
		parameters_to_struct_names(p_types)
	))}

	// Create a control tree for the parameters encoded in A.
	cntl_t* cntl = bli_{opname}_cntl_create( {cntl_create_call_args_with_a(p_types, ", ")}, rntm );

	// Pass the control tree into the internal back-end.
	err_t r_val = bli_{opname}_int( {format_obj_func_call_args(o_types, ", ")}, cntx, rntm, cntl );

	// Free the control tree.
	bli_{opname}_cntl_free( rntm, cntl, NULL );

	return r_val;
}}

#endif
"""

def build_bli_op_h(file_path, opname, o_types, p_types, dims, num_vars):
	multiline_formatter = ", \n        "

	return \
f"""{COPYRIGHT_HEADER}
#ifndef BLIS_{opname.upper()}_H
#define BLIS_{opname.upper()}_H

#include "bli_{opname}_var.h"
#include "bli_{opname}_blksz.h"
#include "bli_{opname}_cntl.h"
#include "bli_{opname}_int.h"

err_t bli_{opname}
     (
        {format_obj_func_args(o_types, multiline_formatter)}
     );

err_t bli_{opname}_ex
     (
        {format_obj_func_args(o_types, multiline_formatter)},
        const cntx_t* cntx,
        rntm_t* rntm
     );

#endif
"""
