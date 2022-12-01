def bli_oapi(name, *params) -> str:
    params = [ x.lower().strip().strip('t') if "FLA" not in x else x.replace("FLA", "BLIS").upper() for x in params ]
    return name + "( " + ", ".join(params) + " );"

def bli_tapi(name, *params) -> str:

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