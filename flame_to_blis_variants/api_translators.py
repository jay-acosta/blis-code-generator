def bli_oapi(name, *params) -> str:
    params = [ x.lower().strip().strip('t') if "FLA" not in x else x.replace("FLA", "BLIS").upper() for x in params ]
    return name + "( " + ", ".join(params) + " );"

def bli_tapi(name, *params) -> str:
    struct_t_mapping = {
        # side
        "FLA_LEFT": "BLIS_LEFT",
        "FLA_RIGHT": "BLIS_RIGHT",
        # uplo
        "FLA_LOWER_TRIANGULAR": "BLIS_LOWER",
        "FLA_UPPER_TRIANGULAR": "BLIS_UPPER",
        # trans
        "FLA_NO_TRANSPOSE": "BLIS_NO_TRANSPOSE",
        "FLA_TRANSPOSE": "BLIS_TRANSPOSE",
        "FLA_CONJ_NO_TRANSPOSE": "BLIS_CONJ_NO_TRANSPOSE",
        "FLA_CONJ_TRANSPOSE": "BLIS_CONJ_TRANSPOSE",
        # conj
        "FLA_NO_CONJUGATE": "BLIS_NO_CONJUGATE",
        "FLA_CONJUGATE": "BLIS_CONJUGATE",
        # diag
        "FLA_NONUNIT_DIAG": "BLIS_NONUNIT_DIAG",
        "FLA_UNIT_DIAG": "BLIS_UNIT_DIAG",
        # "FLA_ZERO_DIAG": "", # no translation for this in BLIS...
    }

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

    constants_mapping = {
        "FLA_ONE": "&one",
        "&FLA_ONE": "&one",
        "FLA_MINUS_ONE": "&minus_one",
        "&FLA_MINUS_ONE": "&minus_one",
    }

    new_params = []

    for param in params:
        if param in struct_t_mapping:
            new_params += ["  " + struct_t_mapping[param] + ","]
        if param in constants_mapping:
            new_params += ["  " + constants_mapping[param] + ","]
        elif "FLA" in param:
            new_params += ["  " + param.replace("FLA", "BLIS") + ","]
        elif param.startswith("size"):
            param = param.lower().strip().strip('t')
            new_params += ["  " + size_mapping[param] + ","]
        elif param not in ["rntm", "cntx"]:
            param = param.lower().strip().strip('t')
            new_params += ["  " + parameter_mapping[param] + ","]
        else:
            new_params += ["  " + param.lower().strip() + ","]

    # return f"PASTEMAC2(ch,{name},BLIS_TAPI_EX_SUF) ( " + ", ".join(new_params) + " );"
    return f"PASTEMAC2(ch,{name},BLIS_TAPI_EX_SUF)", "(", *new_params, ");"