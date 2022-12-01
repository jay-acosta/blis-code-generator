def convert_to_blis_oapi(name, *params) -> str:
    params = [ x.lower().strip().strip('t') if "FLA" not in x else x.replace("FLA", "BLIS").upper() for x in params ]
    return name + "( " + ", ".join(params) + " );"

def convert_to_blis_tapi(name, *params) -> str:

    parameter_mapping = {
        "a00": "a00, rs_a, cs_a",
        "a01": "a01, rs_a",
        "a02": "a02, rs_a, cs_a",
        "a10": "a10, cs_a",
        "alpha11": "alpha11",
        "a12": "a12, cs_a",
        "a20": "a20, rs_a, cs_a",
        "a21": "a21, rs_a",
        "a22": "a22, rs_a, cs_a",
        "mn_behind": "mn_behind"
    }

    size_mapping = {
        "size_a00": "mn_behind",
        "size_a01": "mn_behind",
        "size_a02": "mn_behind",
        "size_a10": "mn_behind",
        "size_a12": "mn_ahead",
        "size_a20": "mn_ahead",
        "size_a21": "mn_ahead",
        "size_a22": "mn_ahead",
    }

    new_params = []

    for param in params:
        if "FLA" in param:
            new_params += [param.replace("FLA", "BLIS")]
        elif param.startswith("size"):
            param = param.lower().strip().strip('t')
            new_params += [size_mapping[param]]
        elif param not in ["rntm", "cntx"]:
            param = param.lower().strip().strip('t')
            new_params += [parameter_mapping[param]]
        else:
            new_params += [param.lower().strip()]

    return f"PASTEMAC2(ch,{name},BLIS_TAPI_EX_SUF) ( " + ", ".join(new_params) + " );"

def amp(s):
    return f"&{s}"

def size(s):
    return f"size_{s}"

def trmm_mapping(x):
    return convert_to_blis_oapi("bli_trmm_ex", x[0], amp(x[4]), amp(x[5]), amp(x[6]), "cntx", "rntm")

def trsm_mapping(x):
    return convert_to_blis_oapi("bli_trsm_ex", x[0], amp(x[4]), amp(x[5]), amp(x[6]), "cntx", "rntm")

def trmv_mapping(x):
    return convert_to_blis_oapi("bli_trmv_ex", "&FLA_ONE", amp(x[3]), amp(x[4]), "cntx", "rntm")

def trinv_mapping(x):
    return convert_to_blis_oapi("bli_trinv_int", amp(x[2]), "cntx", "rntm", "bli_cntl_sub_node( cntl )" )

def trsv_mapping(x):
    return convert_to_blis_oapi("bli_trsv_ex", "&FLA_ONE", amp(x[3]), amp(x[4]), "cntx", "rntm")

def scalv_mapping(x):
    return convert_to_blis_oapi("bli_scalv_ex", amp(x[0]), amp(x[1]), "cntx", "rntm")

def invscalv_mapping(x):
    return convert_to_blis_oapi("bli_invscalv_ex", amp(x[0]), amp(x[1]), "cntx", "rntm")

def invertsc_mapping(x):
    return convert_to_blis_oapi("bli_invertsc", amp(x[1]), amp(x[1]))

def ger_mapping(x):
    return convert_to_blis_oapi("bli_ger_ex", *[amp(s) for s in x], "cntx", "rntm")

def gemm_mapping(x):
    return convert_to_blis_oapi("bli_gemm_ex", amp(x[2]), amp(x[3]), amp(x[4]), amp(x[5]), amp(x[6]), "cntx", "rntm")

def tapi_trmv_mapping(x):
    return convert_to_blis_tapi("trmv",*x[0:3], size(x[3]), amp("FLA_ONE"), *x[3:], "cntx", "rntm")

def tapi_trsv_mapping(x):
    return convert_to_blis_tapi("trsv", "FLA_NO_CONJUGATE", size(x[1]), x[0], x[1], "cntx", "rntm")

def tapi_scalv_mapping(x):
    return convert_to_blis_tapi("scalv","FLA_NO_CONJUGATE", size(x[1]), amp(x[0]), x[1], "cntx", "rntm")

def tapi_invscalv_mapping(x):
    return convert_to_blis_tapi("invscalv", "FLA_NO_CONJUGATE", size(x[1]), x[0], x[1], "cntx", "rntm")

def tapi_invertsc_mapping(x):
    return f"PASTEMAC(ch,invertsc)( {x[0].replace('FLA', 'BLIS')}, {x[1]}, {x[1]} );"

def tapi_ger_mapping(x):
    return convert_to_blis_tapi("ger", "FLA_NO_CONJUGATE", "FLA_NO_CONJUGATE", size(x[1]), size(x[2]), amp(x[0]), x[1], x[2], x[3], "cntx", "rntm")

