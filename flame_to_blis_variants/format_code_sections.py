from re import findall, split
from constants import BS, TB, NL
from flame_parser import get_op_func_args

def format_calc_b_alg(ftype):
    return "b_alg = bli_chol_determine_blocksize( ij, m, a, cntx, cntl );" if ftype == "blk" else ""

def format_define_b_alg(ftype):
    return "dim_t b_alg;" if ftype == "blk" else ""

def format_func_args(file_input):
    return ",\n".join([f"             obj_t*  {arg}" for arg in get_op_func_args(file_input)])

def format_partition_step(ftype, input_file, update_statements):
    flattend_input_file = input_file.replace("\n", "")
    partitions = findall(r"FLA_Obj(?:\s+\w+.){13};", flattend_input_file)
    partition_strs = []

    for arg in partitions:
        m = [x.lower().strip("t") for x in split("[ ,;]+", arg)]

        width = len(m[9]) + 1

        partition_strs += [
f"""
	obj_t {m[3]}, {m[4]+",":<{width}s} {m[5]};
	obj_t {m[8]}, {m[9]+",":<{width}s} {m[10]};
	obj_t {m[11]}, {m[12]+",":<{width}s} {m[13]};
"""
        ]

    partition = "\n".join(partition_strs)

    return partition

def format_repartition_step(ftype, input_file, update_statements):
    flattend_input_file = input_file.replace("\n", "")
    partitions = findall(r"FLA_Obj(?:\s+\w+.){13};", flattend_input_file)

    repartition_strs = []

    for arg in partitions:
        m = [x.lower().strip("t") for x in split("[ ,;]+", arg)]

        width = len(m[9]) + 1

        repartition_strs += [
f"""
		bli_acquire_mparts_tl2br( ij, {"b_alg" if ftype == "blk" else "1"}, {m[3][0]},
		                          &{m[3] }, &{m[4]+",":<{width}s} &{m[5] },
		                          &{m[8] }, &{m[9]+",":<{width}s} &{m[10]},
		                          &{m[11]}, &{m[12]+",":<{width}s} &{m[13]} );
"""
        ]

    repartition = "\n".join(repartition_strs)

    return repartition

def format_loop_conditional(ftype, file_input):

    while_idx = file_input.find("while")
    end_paren_idx = file_input.find("{", while_idx+1)-1
    start_paren_idx = file_input.find("(", while_idx+1, end_paren_idx)+1

    conditional = file_input[start_paren_idx:end_paren_idx]

    blk_size = "b_alg" if ftype == "blk" else "1"

    # general assumption... probably should be a little smarter here
    if ">" in conditional:
        return f"dim_t ij = m - 1; ij >= 0; ij -= {blk_size}"
    else:
        return f"dim_t ij = 0; ij < m; ij += {blk_size}"

def _format_optimized_loop_body(update_statements):
    output = ""
    for statement in update_statements:
        if statement:
            output += f"{TB}{TB}{statement} \\\n"
        else:
            output += "\\\n"

    return output

def _format_object_loop_body(update_statements):
    return "\n\t\t".join(update_statements)

def format_loop_body(ftype, update_statements):
    return \
        _format_optimized_loop_body(update_statements) \
        if ftype == "opt" else \
        _format_object_loop_body(update_statements)
