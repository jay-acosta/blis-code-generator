def build_op_c(op_name, params):

    params_list = ", ".join(params)
    params_func = ", \n\t\t".join(map(lambda x: "obj_t* " + x, params))

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

err_t bli_{op_name}
	 (
		{params_func}
	 )
{{
	return bli_{op_name}_ex( {params_list}, NULL, NULL );
}}

err_t bli_{op_name}_ex
     (
		{params_func},
		const cntx_t* cntx,
		      rntm_t* rntm
     )
{{
	bli_init_once();

	if ( bli_error_checking_is_enabled() )
		bli_{op_name}_check( {params_list}, cntx );

	// If necessary, obtain a valid context from the gks using the induced
	// method id determined above.
	if ( cntx == NULL ) cntx = bli_gks_query_cntx();

	// Initialize a local runtime with global settings if necessary. Note
	// that in the case that a runtime is passed in, we make a local copy.
	rntm_t rntm_l;
	if ( rntm == NULL ) {{ bli_rntm_init_from_global( &rntm_l ); rntm = &rntm_l; }}
	else                {{ rntm_l = *rntm;                       rntm = &rntm_l; }}

	// Create a control tree
	cntl_t* cntl = bli_{op_name}_cntl_create( rntm );

	// Pass the control tree into the internal back-end.
	err_t r_val = bli_{op_name}_int( {params_list}, cntx, rntm, cntl );

	// Free the control tree.
	bli_{op_name}_cntl_free( rntm, cntl, NULL );

	return r_val;
}}

#endif
"""

def build_op_h(op_name, params):

    params_func = ", \n\t\t".join(map(lambda x: "obj_t* " + x, params))

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

#include "bli_{op_name}_var.h"
#include "bli_{op_name}_int.h"
#include "bli_{op_name}_blksz.h"
#include "bli_{op_name}_cntl.h"

err_t bli_{op_name}
     (
       {params_func}
     );

err_t bli_{op_name}_ex
     (
       {params_func},
       const cntx_t* cntx,
             rntm_t* rntm
     );
"""

def build_op_var_c(op_name, params):

    params_list = ", ".join(params)
    params_func = ", \n\t\t".join(map(lambda x: "obj_t* " + x, params))

    return """/*

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

//
// Prototype object-based interfaces.
//

#undef  GENPROT
#define GENPROT( opname ) \\
\\
err_t PASTEMAC0(opname) \\
     ( \\
       const obj_t*  a, \\
       const cntx_t* cntx, \\
             rntm_t* rntm, \\
             cntl_t* cntl  \\
     );

GENPROT(chol_l_blk_var1)
GENPROT(chol_l_blk_var2)
GENPROT(chol_l_blk_var3)

GENPROT(chol_l_unb_var1)
GENPROT(chol_l_unb_var2)
GENPROT(chol_l_unb_var3)

GENPROT(chol_l_opt_var1)
GENPROT(chol_l_opt_var2)
GENPROT(chol_l_opt_var3)

GENPROT(chol_u_blk_var1)
GENPROT(chol_u_blk_var2)
GENPROT(chol_u_blk_var3)

GENPROT(chol_u_bmt_var1)
GENPROT(chol_u_bmt_var2)
GENPROT(chol_u_bmt_var3)

GENPROT(chol_u_unb_var1)
GENPROT(chol_u_unb_var2)
GENPROT(chol_u_unb_var3)

GENPROT(chol_u_opt_var1)
GENPROT(chol_u_opt_var2)
GENPROT(chol_u_opt_var3)

//
// Prototype BLAS-like interfaces with void pointer operands.
//

#undef  GENTPROT
#define GENTPROT( ctype, ch, varname ) \\
\\
err_t PASTEMAC(ch,varname) \\
     ( \\
             uplo_t  uploa, \\
             dim_t   m, \\
             ctype*  a, inc_t rs_a, inc_t cs_a, \\
       const cntx_t* cntx, \\
             rntm_t* rntm  \\
     );

INSERT_GENTPROT_BASIC0( chol_l_opt_var1 )
INSERT_GENTPROT_BASIC0( chol_l_opt_var2 )
INSERT_GENTPROT_BASIC0( chol_l_opt_var3 )

INSERT_GENTPROT_BASIC0( chol_u_opt_var1 )
INSERT_GENTPROT_BASIC0( chol_u_opt_var2 )
INSERT_GENTPROT_BASIC0( chol_u_opt_var3 )
"""
