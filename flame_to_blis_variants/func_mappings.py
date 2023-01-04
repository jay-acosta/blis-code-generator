from constants import amp, size

class Translator(object):
    def __call__(self, statement: str, args):
        return self[statement](args)

    def __getitem__(self, statement: str):
        if hasattr(self, statement):
            return getattr(self, statement)
        else:
            raise KeyError(f"Mapping for statement '{statement}' not found.")

    def translate(self, statement: str, args):
        """
        Functions the same as calling __call__
        """
        return self(statement, args)

class ObjectAPITranslator(Translator):
    # --- Level-0 ---
    def FLA_Absolute_square(self, args):
        return self._map_to_oapi(
            "bli_absqsc",
                amp(args[0]),
                amp(args[0])
        )

    def FLA_Invert(self, args):
        return self._map_to_oapi(
            "bli_invertsc",
                amp(args[1]),
                amp(args[1])
        )

    # --- Level-1 ---
    def FLA_Dots_external(self, args):
        # FLA_Dots_external( FLA_MINUS_ONE, a10t, a01, FLA_ONE, alpha11 );
        return self._map_to_oapi(
            "bli_dotxv_ex",
                amp(args[0]),
                amp(args[1]),
                amp(args[2]),
                amp(args[3]),
                amp(args[4]),
                "cntx",
                "rntm"
        )

    def FLA_Dotcs_external(self, args):
        # FLA_Dotcs_external( FLA_CONJUGATE, FLA_ONE, a21, a21, FLA_ONE, alpha11 );
        # void bli_dotv( obj_t*  x, obj_t*  y, obj_t*  rho );
        original_x = args[2].strip("t")
        conj_x = args[2].strip("t") + "_conj"
        return \
            f"obj_t {conj_x};", \
            f"bli_obj_alias_with_conj( BLIS_CONJUGATE, {amp(original_x)}, {amp(conj_x)} );", \
            self._map_to_oapi(
                "bli_dotxv_ex",
                    amp(args[1]),
                    amp(conj_x),
                    amp(args[3]),
                    amp(args[4]),
                    amp(args[5]),
                    "cntx",
                    "rntm"
            )

    def FLA_Inv_scal_external(self, args):
        return self._map_to_oapi(
            "bli_invscalv_ex",
                amp(args[0]),
                amp(args[1]),
                "cntx",
                "rntm"
        )

    def FLA_Scal_external(self, args):
        return self._map_to_oapi(
            "bli_scalv_ex",
                amp(args[0]),
                amp(args[1]),
                "cntx",
                "rntm"
        )

    # --- Level-2 ---
    def FLA_Gemvc_external(self, args):
        # FLA_Gemvc_external( FLA_NO_TRANSPOSE, FLA_CONJUGATE, FLA_ONE, A02, a12t, FLA_ONE, a01 );
        output = (f"bli_obj_apply_trans( BLIS_TRANSPOSE, {amp(args[3]).lower()} );",) if args[0] == "FLA_NO_TRANSPOSE" else tuple()
        
        original_x = args[4].strip("t")
        conj_x = args[4].strip("t") + "_conj"

        return output + (\
            f"obj_t {conj_x};", \
            f"bli_obj_alias_with_conj( BLIS_CONJUGATE, {amp(original_x)}, {amp(conj_x)} );", \
            self._map_to_oapi(
                "bli_gemv_ex",
                    amp(args[2]),
                    amp(args[3]),
                    amp(args[4]),
                    amp(args[5]),
                    amp(args[6]),
                    "cntx",
                    "rntm"
            )
        )

    def FLA_Ger_external(self, args):
        return self._map_to_oapi(
            "bli_ger_ex",
                *[amp(s) for s in args],
                "cntx",
                "rntm"
        )

    def FLA_Her_internal(self, args):
        return self._map_to_oapi(
            "bli_her_ex",
                amp(args[1]),
                amp(args[2]),
                amp(args[3]),
                "cntx",
                "rntm"
        )

    def FLA_Trmv_external(self, args):
        return self._map_to_oapi(
            "bli_trmv_ex",
                "&FLA_ONE",
                amp(args[3]),
                amp(args[4]),
                "cntx", 
                "rntm"
        )

    def FLA_Trsv_external(self, args):
        return self._map_to_oapi(
            "bli_trsv_ex",
                "&FLA_ONE",
                amp(args[3]),
                amp(args[4]),
                "cntx",
                "rntm"
        )

    # --- Level-3 ---
    def FLA_Gemm_internal(self, args):
        return self._map_to_oapi(
            "bli_gemm_ex",
                amp(args[2]),
                amp(args[3]),
                amp(args[4]),
                amp(args[5]),
                amp(args[6]),
                "cntx",
                "rntm"
        )

    def FLA_Herk_internal(self, args):
        return self._map_to_oapi(
            "bli_herk_ex",
                amp(args[2]),
                amp(args[3]),
                amp(args[4]),
                amp(args[5]),
                "cntx",
                "rntm"
        )

    def FLA_Trmm_internal(self, args):
        return self._map_to_oapi(
            "bli_trmm_ex",
                args[0],
                amp(args[4]),
                amp(args[5]),
                amp(args[6]),
                "cntx",
                "rntm"
        )

    def FLA_Trsm_internal(self, args):
        return self._map_to_oapi(
            "bli_trsm_ex",
                args[0],
                amp(args[4]),
                amp(args[5]),
                amp(args[6]),
                "cntx",
                "rntm"
        )

    # --- Level-4 ---
    def FLA_Trinv_internal(self, args):
        return self._map_to_oapi(
            "bli_trinv_int",
                amp(args[2]),
                "cntx",
                "rntm",
                "bli_cntl_sub_node( cntl )"
        )

    def FLA_Ttmm_internal(self, args):
        return self._map_to_oapi(
            "bli_ttmm_int",
                amp(args[1]),
                "cntx",
                "rntm",
                "bli_cntl_sub_node( cntl )"
        )

    def _map_to_oapi(self, name, *params) -> str:
        params = [ x.lower().strip().strip('t') if "FLA" not in x else x.replace("FLA", "BLIS").upper() for x in params ]
        return name + "( " + ", ".join(params) + " );"

class TypedAPITranslator(Translator):
    # --- Level-0 ---
    def FLA_Absolute_square(self, args):
        return f"PASTEMAC(ch,absqsc)( {args[0]}, {args[0]} );"
    
    def FLA_Invert(self, args):
        return f"PASTEMAC(ch,invertsc)( {args[0].replace('FLA', 'BLIS')}, {args[1]}, {args[1]} );"

    # --- Level-1 ---
    def FLA_Dotcs_external(self, args):
        return self._map_to_tapi("dotxv",args[0],"FLA_NO_CONJUGATE",size(args[2]),args[1],args[2],args[3],args[4],args[5],"cntx","rntm")

    def FLA_Inv_scal_external(self, args):
        return self._map_to_tapi("invscalv", "FLA_NO_CONJUGATE", size(args[1]), args[0], args[1], "cntx", "rntm")

    def FLA_Scal_external(self, args):
        return self._map_to_tapi("scalv","FLA_NO_CONJUGATE", size(args[1]), args[0], args[1], "cntx", "rntm")

    # --- Level-2 ---
    def FLA_Gemvc_external(self, args):
        return self._map_to_tapi("gemv", *args[0:2], size(args[3]), size(args[4]), *args[2:], "cntx", "rntm")

    def FLA_Ger_external(self, args):
        return self._map_to_tapi("ger", "FLA_NO_CONJUGATE", "FLA_NO_CONJUGATE", size(args[1]), size(args[2]), amp(args[0]), args[1], args[2], args[3], "cntx", "rntm")

    def FLA_Trmv_external(self, args):
        return self._map_to_tapi("trmv",*args[0:3], size(args[3]), amp("FLA_ONE"), *args[3:], "cntx", "rntm")

    def FLA_Trsv_external(self, args):
        return self._map_to_tapi("trsv", "FLA_NO_CONJUGATE", size(args[1]), args[0], args[1], "cntx", "rntm")

    # --- Level-3 ---

    # --- Level-4 ---

    # --- Helper Methods ---

    def _map_to_tapi(self, name, *params) -> str:
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
