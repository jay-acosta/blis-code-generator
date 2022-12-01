from re import sub
from file_io import read_file
from flame_parser import *
from format_code_sections import *

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
f"""/*

   BLIS
   An object-based framework for developing high-performance BLAS-like
   libraries.

   Copyright (C) 2022, The University of Texas at Austin

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:
    - Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    - Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    - Neither the name(s) of the copyright holder(s) nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

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
		/*------------------------------------------------------------*/
		{loop_body}
		/*------------------------------------------------------------*/

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
f"""/*

   BLIS
   An object-based framework for developing high-performance BLAS-like
   libraries.

   Copyright (C) 2022, The University of Texas at Austin

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:
    - Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    - Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    - Neither the name(s) of the copyright holder(s) nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

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
	for ( dim_t i = 0; i < m; ++i ) \\
	{{ \\
		const dim_t mn_behind = i; \\
		const dim_t mn_ahead  = m - i - 1; \\
\\
		ctype*   a00       = a + (0  )*rs_a + (0  )*cs_a; \\
		ctype*   a01       = a + (0  )*rs_a + (i  )*cs_a; \\
		ctype*   a02       = a + (0  )*rs_a + (i+1)*cs_a; \\
		ctype*   alpha11   = a + (i  )*rs_a + (i  )*cs_a; \\
		ctype*   a12       = a + (i  )*rs_a + (i+1)*cs_a; \\
		ctype*   a22       = a + (i+1)*rs_a + (i+1)*cs_a; \\
\\
{ loop_body } \\
	}} \\
\\
	return BLIS_SUCCESS; \\
}}

INSERT_GENTFUNCR_BASIC0( {func_name.replace("bli_","")} )

#endif
"""

