from re import split
from func_mappings import Translator, ObjectAPITranslator, TypedAPITranslator

def translate_flame_updates_to_blis(ftype, file_input):
    # get the middle part of the input where the update statements are
    file_input = split("/\*-+\*/", file_input)
    if len(file_input) != 3:
        return None
    file_input = file_input[1].strip()

    update_statements = condense_func_calls(file_input)

    return translate_update_statements(ftype, update_statements)

def condense_func_calls(file_input):
    update_statements = []
    flame_statements = file_input.split("\n")
    i = 0
    while i < len(flame_statements):
        new_statement = flame_statements[i].strip()

        if "FLA" in new_statement:
            # combine statements until we reach a semicolon
            while (i < len(flame_statements) - 1) and (";" not in flame_statements[i]):
                i += 1
                new_statement = new_statement + " " + flame_statements[i].strip()
                
        update_statements += [new_statement]
        i += 1
    return update_statements

def translate_update_statements(ftype, flame_statements):
    translator = ObjectAPITranslator() if ftype != "opt" else TypedAPITranslator()
    ops = []
    for line in flame_statements:
        if line.startswith("FLA"):
            op = translate_update_statement(translator, line)

            # unpack operation if a function needs multiple lines
            if isinstance(op, tuple):
                ops += [*op]
            else:
                ops += [op]

        elif line.startswith("//") and ftype == "opt":
            ops += [line.replace("//", "/*") + " */"]
        else:
            ops += [line]

    return ops

def translate_update_statement(translator : Translator, update_statement):
    func_name, args = get_func_name_from_update(update_statement), get_func_args_from_update(update_statement)
    try:
        return translator.translate(func_name, args)
    except KeyError:
        print("Unknown operation \"", func_name, "\"")
        print("Try implementing this operation in func_mappings.py. Will mark as a TODO string")
    except Exception as e:
        print(e)
        raise Exception(f"An unknown error occurred while translating \"{update_statement}\".")
    return f"/* TODO: {update_statement} */"


def get_op_func_args(file_input):
    # get arguments from FLAME code
    error_idx = file_input.find("FLA_Error")
    end_paren_idx = file_input.find(")", error_idx+1)
    start_paren_idx = file_input.find("(", error_idx, end_paren_idx)+1

    func_args = file_input[start_paren_idx:end_paren_idx]

    # split at commas then get only the argument name for each argument
    get_arg_name = lambda arg: arg.strip().split()[1].lower()
    func_args = [get_arg_name(arg) for arg in func_args.split(",")]

    # ignore final argument (the FLAME control tree)
    if func_args[-1] == "cntl":
        func_args = func_args[:-1]

    return func_args

def get_op_func_name_from_path(file_path):
    return file_path.name.replace("FLA", "bli").lower()[:-2]

def get_type_from_func_name(func_name):
    if "blk" in func_name:
        return "blk"
    elif "opt" in func_name:
        return "opt"
    else:
        return "unb"

def get_func_name_from_update(update_statement: str):
    return update_statement[:update_statement.find("(")]

def get_func_args_from_update(update_statement: str) -> list:
    return update_statement[update_statement.find("(")+1:update_statement.find(")")] \
            .strip() \
            .split(", ")