import os
from pathlib import Path
from os.path import join
from arch_util import *

NL = "\n"
TB = "\t"
BS = "\\"

"""
Operation specific files
"""

def build_operation_files(blis_dir, opname, o_types, p_types, dims):
	# build operation directory
	op_dir = Path(join(blis_dir, "frame", "4", opname))
	if not op_dir.exists():
		print(f"Making directory at {op_dir}")
		os.makedirs(op_dir)
	
	repacked_params = (opname, o_types, p_types, dims)
	
	write_wout_check(join(op_dir, f"bli_{opname}_blksz.c"), build_bli_op_blksz_c, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}_blksz.h"), build_bli_op_blksz_h, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}_cntl.c"), build_bli_op_cntl_c, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}_cntl.h"), build_bli_op_cntl_h, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}_int.c"), build_bli_op_int_c, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}_int.h"), build_bli_op_int_h, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}_var.h"), build_bli_op_var_h, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}.c"), build_bli_op_c, repacked_params)
	write_wout_check(join(op_dir, f"bli_{opname}.h"), build_bli_op_h, repacked_params)

"""
bli_<opname>_blksz.c and bli_<opname>_blksz.h
"""
def build_bli_op_blksz_c(file_path, opname, o_types, p_types, dims):
	return f"""/*

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

def build_bli_op_blksz_h(file_path, opname, o_types, p_types, dims):
	return f"""/*

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
def build_bli_op_cntl_c(file_path, opname, o_types, p_types, dims):

	np = len(p_types)

	return f"""/*

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

/*
// TODO: Change this to include all of your variants
static {opname}_oft unb_vars[2] = 
{{

}};

static {opname}_oft blk_vars[2] = 
{{
  
}};
*/

cntl_t* bli_{opname}_cntl_create
     (
       {", ".join(map(lambda x: PARAM_TMAP[x] + "_t " + PARAM_TMAP[x] + "a", p_types))},
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

def build_bli_op_cntl_h(file_path, opname, o_types, p_types, dims):

	params_func_args = map(lambda x: f"{x}_t {x}", convert_param_to_name(p_types))

	return f"""/*

   BLIS
   An object-based framework for developing high-performance BLAS-like
   libraries.

   Copyright (C) 2014, The University of Texas at Austin

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

cntl_t* bli_{opname}_cntl_create( {", ".join(params_func_args)}, rntm_t* rntm );

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
def build_bli_op_int_c(file_path, opname, o_types, p_types, dims):
	obj_func_params = ", \n             ".join(map(
		lambda x: f"obj_t* {x}",
		convert_obj_to_name(o_types)
	))

	return f"""/*

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

err_t bli_{opname}_int
     (
             {obj_func_params},
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{{
	{opname}_oft {opname}_fp = bli_cntl_var_func( cntl );

	return {opname}_fp( {", ".join(convert_obj_to_name(o_types))}, cntx, rntm, cntl );
}}

#endif
"""

def build_bli_op_int_h(file_path, opname, o_types, p_types, dims):
	obj_func_params = ", \n             ".join(map(
		lambda x: f"obj_t* {x}",
		convert_obj_to_name(o_types)
	))
	return f"""/*

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

#ifndef BLIS_{opname.upper()}_INT_H
#define BLIS_{opname.upper()}_INT_H

err_t bli_{opname}_int
     (
             {obj_func_params},
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     );

#endif
"""

"""
bli_<opname>_var.h
"""
def build_bli_op_var_h(file_path, opname, o_types, p_types, dims):
	obj_func_params = ", \\\n             ".join(map(
		lambda x: f"obj_t* {x}",
		convert_obj_to_name(o_types)
	))

	params_struc = list(convert_param_to_name(p_types))

	return f"""
	/*

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
       {obj_func_params}, \\
       const cntx_t* cntx, \\
             rntm_t* rntm, \\
             cntl_t* cntl  \\
     );

// TODO: INSERT ALL INVARIANT NAMES HERE!
//GENPROT(  )

//
// Prototype BLAS-like interfaces with void pointer operands.
//

#undef  GENTPROT
#define GENTPROT( ctype, ch, varname ) \\
\\
err_t PASTEMAC(ch,varname) \\
     ( \\
             {f", {BS}{NL}{TB}{TB}{TB}{TB}{TB}{TB} ".join(map(
                 lambda x: f"{x}_t  {x}a",
                 params_struc
			))}, \\
             {f", {BS}{NL}{TB}{TB}{TB}{TB}{TB}{TB} ".join(map(
                 lambda x: f"dim_t   {x}",
                 dims
			 ))}, \\
             {f", {BS}{NL}{TB}{TB}{TB}{TB}{TB}{TB} ".join(map(
                 lambda x: x,
                 function_inline(o_types)
			 ))}, \\
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

// TODO: INSERT OPTIMIZED INVARIANT NAMES HERE!
//INSERT_GENTPROT_BASIC0(  )

#endif
"""

"""
bli_<opname>.c and bli_<opname>.h
"""
def build_bli_op_c(file_path, opname, o_types, p_types, dims):

	obj_func_params = ",\n\t\t\t".join(map(
		lambda x: f"obj_t* {x}",
		convert_obj_to_name(o_types)
	))

	params_struc = list(convert_param_to_name(p_types))

	return f"""/*

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

err_t bli_{opname}
     (
       {obj_func_params}
     )
{{
	return bli_{opname}_ex( {", ".join(convert_obj_to_name(o_types))}, NULL, NULL );
}}

err_t bli_{opname}_ex
     (
       {obj_func_params},
       const cntx_t* cntx,
             rntm_t* rntm
     )
{{
	bli_init_once();

	if ( bli_error_checking_is_enabled() )
		bli_{opname}_check( {", ".join(convert_obj_to_name(o_types))}, cntx );

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
		params_struc
	))}

	// Create a control tree for the parameters encoded in A.
	cntl_t* cntl = bli_{opname}_cntl_create( {", ".join(map(lambda x: x + "a", params_struc))}, rntm );

	// Pass the control tree into the internal back-end.
	err_t r_val = bli_{opname}_int( {", ".join(convert_obj_to_name(o_types))}, cntx, rntm, cntl );

	// Free the control tree.
	bli_{opname}_cntl_free( rntm, cntl, NULL );

	return r_val;
}}

#endif
"""

def build_bli_op_h(file_path, opname, o_types, p_types, dims):

	obj_param = ",\n\t\t\t".join(map(
		lambda x: f"obj_t* {x}",
		convert_obj_to_name(o_types)
	))

	return f"""/*

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

#ifndef BLIS_{opname}_H
#define BLIS_{opname}_H

#include "bli_{opname}_var.h"
#include "bli_{opname}_blksz.h"
#include "bli_{opname}_cntl.h"
#include "bli_{opname}_int.h"

err_t bli_{opname}
		(
			{obj_param}
		);

err_t bli_{opname}_ex
		(
			{obj_param},
			const cntx_t* cntx,
			rntm_t* rntm
		);

#endif
"""
