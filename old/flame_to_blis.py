from constants import CONVERT_OAPI, CONVERT_TAPI, UNB_LOWER_TEMPLATE, UNB_UPPER_TEMPLATE, BLK_LOWER_TEMPLATE, BLK_UPPER_TEMPLATE, OPT_LOWER_TEMPLATE, OPT_UPPER_TEMPLATE

FILE_INPUT = "operations_unb_opt.in"

def get_flame_args(update_statement: str) -> list:
    return update_statement[update_statement.find("(")+1:update_statement.find(")")] \
            .strip() \
            .split(", ")

def get_func_name(update_statement: str):
    return update_statement[:update_statement.find("(")]

def flame_to_blis_oapi (update_statement):
    func_name, args = get_func_name(update_statement), get_flame_args(update_statement)
    return CONVERT_OAPI[func_name](args)

def flame_to_blis_tapi (update_statement):
    func_name, args = get_func_name(update_statement), get_flame_args(update_statement)
    return CONVERT_TAPI[func_name](args)

def convert_ops(ftype, flame_statements):
    converter_func = flame_to_blis_oapi if ftype != "opt" else flame_to_blis_tapi

    ops = []
    for line in flame_statements:
        if line.startswith("FLA"):
            ops += [converter_func(line)]
        elif line.startswith("//") and ftype == "opt":
            ops += [line.replace("//", "/*") + " */"]
        else:
            ops += [line]

    return ops

def get_ops(file_name):
    update_statements = []
    with open(file_name, "r") as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if line.startswith("~"):
                _, name, param, ftype, num = line.split()
                yield name, param, ftype, num, convert_ops(ftype, update_statements)
                update_statements = []
            else:
                update_statements += [line]

# def write_file(name, param, ftype, num, update_statements):
#     with open(f"bli_{name}_{param}_{ftype}_var{num}.c", "w") as file:

def join_lines(update_statements, suffix):
    return "\t\t" + f"{suffix}\n\t\t".join(update_statements) + suffix

def oapi_formatter(template, name, param, num, update_statements):
    return template % (name, param, num, join_lines(update_statements, ""))

def tapi_formatter(template, name, param, num, update_statements):
    return template % (name, param, num, 
                       name, name, name, 
                       param, num, 
                       join_lines(update_statements, " \\"), 
                       name, param, num)
        
def main():
    # start making unblocked functions
    # func_metadata = get_ops("test_ops.in")
    # print (func_metadata)

    for name, param, ftype, num, update_statements in get_ops(FILE_INPUT):

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

if __name__ == "__main__":
    main()
