import 
from pathlib import Path

def main():
    flame_file = Path("~/oraflame/src/lapack/inv/tri/ln/flamec/FLA_Trinv_ln_unb_var1.c").expanduser()

    # output_content = generate_blis_op(flame_file)

    with open(f"bli_{name}_{param}_{ftype}_var{num}.c", "w") as file:
        if ftype == "blk":
            file_str = BLK_LOWER_TEMPLATE if param[0] == "l" else BLK_UPPER_TEMPLATE
            file.write (oapi_formatter(file_str, name, param, num, update_statements))
        elif ftype == "opt":
            file_str = OPT_LOWER_TEMPLATE if param[0] == "l" else OPT_UPPER_TEMPLATE
            file.write (tapi_formatter(file_str, name, param, num, update_statements))
        else:
            file_str = UNB_LOWER_TEMPLATE if param[0] == "l" else UNB_UPPER_TEMPLATE
            file.write (oapi_formatter(file_str, name, param, num, update_statements))

    # print(output_content)

if __name__ == "__main__":
    main()
