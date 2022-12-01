from api_translators import *
from constants import amp, size

"""
To add a new operation, add a custom function mapping for the OAPI and TAPI

After making the function, put it in the map
"""

OAPI_OPS_MAP = {}
TAPI_OPS_MAP = {}

# --- Level-0 --------------------------------------------------------------
# absqsc
def absqsc_oapi(x):
    return bli_oapi("bli_absqsc", amp(x[0]), amp(x[0]))
OAPI_OPS_MAP["FLA_Absolute_square"] = absqsc_oapi

def absqsc_tapi(x):
    return f"PASTEMAC(ch,absqsc)( {x[0]}, {x[0]} );"
TAPI_OPS_MAP["FLA_Absolute_square"] = absqsc_tapi

# invertsc
def invertsc_oapi(x):
    return bli_oapi("bli_invertsc", amp(x[1]), amp(x[1]))
OAPI_OPS_MAP["FLA_Invert"] = invertsc_oapi

def invertsc_tapi(x):
    return f"PASTEMAC(ch,invertsc)( {x[0].replace('FLA', 'BLIS')}, {x[1]}, {x[1]} );"
TAPI_OPS_MAP["FLA_Invert"] = invertsc_tapi

# --- Level-1 -------------------------------------------------------------
# addv
# amaxv
# axpbyv
# axpyv
# copyv
# dotv
def dotcs_oapi(x):
    # FLA_Dotcs_external( FLA_CONJUGATE, FLA_ONE, a21, a21, FLA_ONE, alpha11 );
    # void bli_dotv( obj_t*  x, obj_t*  y, obj_t*  rho );
    original_x = x[2].strip("t")
    conj_x = x[2].strip("t") + "_conj"
    return \
        f"obj_t {conj_x};", \
        f"bli_obj_alias_with_conj( BLIS_CONJUGATE, {amp(original_x)}, {amp(conj_x)} );", \
        bli_oapi("bli_dotxv_ex", amp(x[1]), amp(conj_x), amp(x[3]), amp(x[4]), amp(x[5]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Dotcs_external"] = dotcs_oapi

def dotcs_tapi(x):
    return bli_tapi("dotxv",x[0],"FLA_NO_CONJUGATE",size(x[2]),x[1],x[2],x[3],x[4],x[5],"cntx","rntm")
TAPI_OPS_MAP["FLA_Dotcs_external"] = dotcs_tapi

# dotxv
# normfv
# invscalv
def invscalv_oapi(x):
    return bli_oapi("bli_invscalv_ex", amp(x[0]), amp(x[1]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Inv_scal_external"] = invscalv_oapi

def invscalv_tapi(x):
    return bli_tapi("invscalv", "FLA_NO_CONJUGATE", size(x[1]), x[0], x[1], "cntx", "rntm")
TAPI_OPS_MAP["FLA_Inv_scal_external"] = invscalv_tapi

# scalv
def scalv_oapi(x):
    return bli_oapi("bli_scalv_ex", amp(x[0]), amp(x[1]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Scal_external"] = scalv_oapi

def scalv_tapi(x):
    return bli_tapi("scalv","FLA_NO_CONJUGATE", size(x[1]), x[0], x[1], "cntx", "rntm")
TAPI_OPS_MAP["FLA_Scal_external"] = scalv_tapi

# scal2v
# setv
# subv
# xpbyv

# addm
# axpym
# copym
# normfm
# invscalm
# scalm
# scal2m
# setm
# subm
# xpbym


# --- Level-2 --------------------------------------------------------------
# gemv
def gemvc_oapi(x):
    # FLA_Gemvc_external( FLA_NO_TRANSPOSE, FLA_CONJUGATE, FLA_ONE, A02, a12t, FLA_ONE, a01 );
    output = (f"bli_obj_apply_trans( BLIS_TRANSPOSE, {amp(x[3]).lower()} );",) if x[0] == "FLA_NO_TRANSPOSE" else tuple()
    
    original_x = x[4].strip("t")
    conj_x = x[4].strip("t") + "_conj"

    return output + (\
        f"obj_t {conj_x};", \
        f"bli_obj_alias_with_conj( BLIS_CONJUGATE, {amp(original_x)}, {amp(conj_x)} );", \
        bli_oapi("bli_gemv_ex", amp(x[2]),amp(x[3]),amp(x[4]),amp(x[5]),amp(x[6]), "cntx", "rntm"))
OAPI_OPS_MAP["FLA_Gemvc_external"] = gemvc_oapi

def gemvc_tapi(x):
    return bli_tapi("gemv", *x[0:2], size(x[3]), size(x[4]), *x[2:], "cntx", "rntm")
TAPI_OPS_MAP["FLA_Gemvc_external"] = gemvc_tapi

# ger
def ger_oapi(x):
    return bli_oapi("bli_ger_ex", *[amp(s) for s in x], "cntx", "rntm")
OAPI_OPS_MAP["FLA_Ger_external"] = ger_oapi

def ger_tapi(x):
    return bli_tapi("ger", "FLA_NO_CONJUGATE", "FLA_NO_CONJUGATE", size(x[1]), size(x[2]), amp(x[0]), x[1], x[2], x[3], "cntx", "rntm")
TAPI_OPS_MAP["FLA_Ger_external"] = ger_tapi

# hemv
# her
def her_oapi(x):
    return bli_oapi("bli_her_ex", amp(x[1]), amp(x[2]), amp(x[3]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Her_internal"] = her_oapi

# her2
# symv
# syr
# syr2
# trmv
def trmv_oapi(x):
    return bli_oapi("bli_trmv_ex", "&FLA_ONE", amp(x[3]), amp(x[4]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Trmv_external"] = trmv_oapi

def trmv_tapi(x):
    return bli_tapi("trmv",*x[0:3], size(x[3]), amp("FLA_ONE"), *x[3:], "cntx", "rntm")
TAPI_OPS_MAP["FLA_Trmv_external"] = trmv_tapi

# trsv
def trsv_oapi(x):
    return bli_oapi("bli_trsv_ex", "&FLA_ONE", amp(x[3]), amp(x[4]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Trsv_external"] = trsv_oapi

def trsv_tapi(x):
    return bli_tapi("trsv", "FLA_NO_CONJUGATE", size(x[1]), x[0], x[1], "cntx", "rntm")
TAPI_OPS_MAP["FLA_Trsv_external"] = trsv_tapi

# --- Level-3 --------------------------------------------------------------
# gemm
def gemm_oapi(x):
    return bli_oapi("bli_gemm_ex", amp(x[2]), amp(x[3]), amp(x[4]), amp(x[5]), amp(x[6]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Gemm_internal"] = gemm_oapi

# gemmt
# hemm
# herk
def herk_oapi(x):
    return bli_oapi("bli_herk_ex", amp(x[2]), amp(x[3]), amp(x[4]), amp(x[5]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Herk_internal"] = herk_oapi

# her2k
# symm
# syrk
# syr2k
# trmm
def trmm_oapi(x):
    return bli_oapi("bli_trmm_ex", x[0], amp(x[4]), amp(x[5]), amp(x[6]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Trmm_internal"] = trmm_oapi

# trmm3
# trsm
def trsm_oapi(x):
    return bli_oapi("bli_trsm_ex", x[0], amp(x[4]), amp(x[5]), amp(x[6]), "cntx", "rntm")
OAPI_OPS_MAP["FLA_Trsm_internal"] = trsm_oapi

# --- Level-4 --------------------------------------------------------------
# chol
# trinv
def trinv_oapi(x):
    return bli_oapi("bli_trinv_int", amp(x[2]), "cntx", "rntm", "bli_cntl_sub_node( cntl )" )
OAPI_OPS_MAP["FLA_Trinv_internal"] = trinv_oapi

# ttmm
def ttmm_oapi(x):
    return bli_oapi("bli_ttmm_int", amp(x[1]), "cntx", "rntm", "bli_cntl_sub_node( cntl )" )
OAPI_OPS_MAP["FLA_Ttmm_internal"] = ttmm_oapi

# OAPI_OPS_MAP = {
#     "FLA_Absolute_square": absqsc_oapi,
#     "FLA_Invert": invertsc_oapi,
#     "FLA_Dotcs_external": dotcs_oapi,
#     "FLA_Inv_scal_external": invscalv_oapi,
#     "FLA_Scal_external": scalv_oapi,

#     "FLA_Trmm_internal": trmm_oapi,
#     "FLA_Trsm_internal": trsm_oapi,
#     "FLA_Trmv_external": trmv_oapi,
#     "FLA_Trsv_external": trsv_oapi,
#     "FLA_Trinv_internal": trinv_oapi,
#     "FLA_Ttmm_internal": ttmm_oapi,
#     "FLA_Herk_internal": herk_oapi,
#     "FLA_Her_internal": her_oapi,
#     "FLA_Herc_internal": her_oapi,
#     "FLA_Ger_external": ger_oapi,
#     "FLA_Gemm_internal": gemm_oapi,
    
#     # "FLA_Gemvc_external": gemvc_oapi,
#     "FLA_Her_external": her_oapi
# }

# TAPI_OPS_MAP = {
#     "FLA_Trmv_external": trmv_tapi,
#     "FLA_Trsv_external": trsv_tapi,
#     "FLA_Scal_external": scalv_tapi,
#     "FLA_Inv_scal_external": invscalv_tapi,
#     "FLA_Invert": invertsc_tapi,
#     "FLA_Ger_external": ger_tapi
# }

