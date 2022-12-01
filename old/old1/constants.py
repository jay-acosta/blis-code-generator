from func_mappings import *

CONVERT_OAPI = {
    "FLA_Trmm_internal": trmm_mapping,
    "FLA_Trsm_internal": trsm_mapping,
    "FLA_Trmv_external": trmv_mapping,
    "FLA_Trsv_external": trsv_mapping,
    "FLA_Trinv_internal": trinv_mapping,
    "FLA_Scal_external": scalv_mapping,
    "FLA_Inv_scal_external": invscalv_mapping,
    "FLA_Invert": invertsc_mapping,
    "FLA_Ger_external": ger_mapping,
    "FLA_Gemm_internal": gemm_mapping,
}

CONVERT_TAPI = {
    "FLA_Trmv_external": tapi_trmv_mapping,
    "FLA_Trsv_external": tapi_trsv_mapping,
    "FLA_Scal_external": tapi_scalv_mapping,
    "FLA_Inv_scal_external": tapi_invscalv_mapping,
    "FLA_Invert": tapi_invertsc_mapping,
    "FLA_Ger_external": tapi_ger_mapping
}

UNB_LOWER_TEMPLATE = \
"""/*

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

err_t bli_%s_%s_unb_var%s
     (
       const obj_t*  a,
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{
	const dim_t m = bli_obj_length( a );

	obj_t    a00;
	obj_t    a10,   alpha11;
	obj_t    a20,   a21,      a22;

	for ( dim_t ij = 0; ij < m; ij += 1 )
	{
		bli_acquire_mparts_tl2br( ij, 1, a,
		                          &a00, NULL,     NULL,
		                          &a10, &alpha11, NULL,
		                          &a20, &a21,     &a22 );

%s

	}

	return BLIS_SUCCESS;
}

#endif
"""

UNB_UPPER_TEMPLATE = \
"""/*

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

err_t bli_%s_%s_unb_var%s
     (
       const obj_t*  a,
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{
	const dim_t m = bli_obj_length( a );

	obj_t    a00,   a01,     a02;
	obj_t           alpha11, a12;
	obj_t                    a22;

	for ( dim_t ij = 0; ij < m; ij += 1 )
	{
		bli_acquire_mparts_tl2br( ij, 1, a,
		                          &a00, &a01,     &a02,
		                          NULL, &alpha11, &a12,
		                          NULL, NULL,     &a22 );

%s

	}

	return BLIS_SUCCESS;
}

#endif
"""

BLK_LOWER_TEMPLATE = \
"""/*

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

err_t bli_%s_%s_blk_var%s
     (
       const obj_t*  a,
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{
	const dim_t m = bli_obj_length( a );

    dim_t b_alg;

	obj_t    a00;
	obj_t    a10,   a11;
	obj_t    a20,   a21,      a22;

	for ( dim_t ij = 0; ij < m; ij += b_alg )
	{
        b_alg = bli_chol_determine_blocksize( ij, m, a, cntx, cntl );

		bli_acquire_mparts_tl2br( ij, b_alg, a,
		                          &a00, NULL, NULL,
		                          &a10, &a11, NULL,
		                          &a20, &a21, &a22 );

%s

	}

	return BLIS_SUCCESS;
}

#endif
"""

BLK_UPPER_TEMPLATE = \
"""/*

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

err_t bli_%s_%s_blk_var%s
     (
       const obj_t*  a,
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{
	const dim_t m = bli_obj_length( a );

    dim_t b_alg;

	obj_t    a00,   a01,     a02;
	obj_t           a11,     a12;
	obj_t                    a22;

	for ( dim_t ij = 0; ij < m; ij += b_alg )
	{
        b_alg = bli_chol_determine_blocksize( ij, m, a, cntx, cntl );
        
		bli_acquire_mparts_tl2br( ij, b_alg, a,
		                          &a00, &a01, &a02,
		                          NULL, &a11, &a12,
		                          NULL, NULL, &a22 );

%s

	}

	return BLIS_SUCCESS;
}

#endif
"""

OPT_LOWER_TEMPLATE = \
"""/*

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

err_t bli_%s_%s_opt_var%s
     (
       const obj_t*  a,
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{
	num_t     dt        = bli_obj_dt( a );

	uplo_t    uploa     = bli_obj_uplo( a );
	diag_t    diaga     = bli_obj_diag( a );
	dim_t     m         = bli_obj_length( a );
	void*     buf_a     = bli_obj_buffer_at_off( a );
	inc_t     rs_a      = bli_obj_row_stride( a );
	inc_t     cs_a      = bli_obj_col_stride( a );

	if ( bli_error_checking_is_enabled() )
		PASTEMAC(%s,_check)( a, cntx );

	// Query a type-specific function pointer, except one that uses
	// void* for function arguments instead of typed pointers.
	%s_opt_vft f = PASTEMAC(%s_%s_opt_var%s,_qfp)( dt );

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
}

#undef  GENTFUNCR
#define GENTFUNCR( ctype, ctype_r, ch, chr, varname ) \\
\\
err_t PASTEMAC(ch,varname) \\
     ( \\
             uplo_t  uploa, \\
             diag_t  diaga, \\
             dim_t   m, \\
             ctype*  a, inc_t rs_a, inc_t cs_a, \\
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     ) \\
{ \\
\\
	for ( dim_t i = 0; i < m; ++i ) \\
	{ \\
		const dim_t mn_behind = i; \\
\\
		ctype*   a00       = a + (0  )*rs_a + (0  )*cs_a; \\
		ctype*   a10       = a + (i  )*rs_a + (0  )*cs_a; \\
		ctype*   alpha11   = a + (i  )*rs_a + (i  )*cs_a; \\
		ctype*   a20       = a + (i+1)*rs_a + (0  )*cs_a; \\
		ctype*   a21       = a + (i+1)*rs_a + (i  )*cs_a; \\
		ctype*   a22       = a + (i+1)*rs_a + (i+1)*cs_a; \\
\\
%s
\\
	} \\
\\
	return BLIS_SUCCESS; \\
}

INSERT_GENTFUNCR_BASIC0( %s_%s_opt_var%s )

#endif
"""

OPT_UPPER_TEMPLATE = \
"""/*

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

err_t bli_%s_%s_opt_var%s
     (
       const obj_t*  a,
       const cntx_t* cntx,
             rntm_t* rntm,
             cntl_t* cntl
     )
{
	num_t     dt        = bli_obj_dt( a );

	uplo_t    uploa     = bli_obj_uplo( a );
	diag_t    diaga     = bli_obj_diag( a );
	dim_t     m         = bli_obj_length( a );
	void*     buf_a     = bli_obj_buffer_at_off( a );
	inc_t     rs_a      = bli_obj_row_stride( a );
	inc_t     cs_a      = bli_obj_col_stride( a );

	if ( bli_error_checking_is_enabled() )
		PASTEMAC(%s,_check)( a, cntx );

	// Query a type-specific function pointer, except one that uses
	// void* for function arguments instead of typed pointers.
	%s_opt_vft f = PASTEMAC(%s_%s_opt_var%s,_qfp)( dt );

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
}

#undef  GENTFUNCR
#define GENTFUNCR( ctype, ctype_r, ch, chr, varname ) \\
\\
err_t PASTEMAC(ch,varname) \\
     ( \\
             uplo_t  uploa, \\
             diag_t  diaga, \\
             dim_t   m, \\
             ctype*  a, inc_t rs_a, inc_t cs_a, \\
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     ) \\
{ \\
\\
	for ( dim_t i = 0; i < m; ++i ) \\
	{ \\
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
%s
\\
	} \\
\\
	return BLIS_SUCCESS; \\
}

INSERT_GENTFUNCR_BASIC0( %s_%s_opt_var%s )

#endif
"""
