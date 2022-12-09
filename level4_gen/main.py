import os
from pathlib import Path

import argparse as ap

from op_file_writer import write_operation_files
from level_file_writer import build_level_files
from test_file_writer import build_test_files

def main(args):
	print("Starting code generator...")

	# opname, object types, parameter types, dimensions
	params = (args.operation_name, args.object_types, args.parameter_types, args.dimensions, args.num_variants)
	blis_path = Path(args.blis_directory).expanduser()

	print("Creating operation files")
	# write_operation_files(blis_path, *params)
	print()

	print("Adding operation to level 4")
	# build_level_files(blis_path, *params)
	print()

	print("Creating test files")
	build_test_files(blis_path, *params)
	print()
  
	print("""
!---------------------------------------------------------!
Done generating all files for the new operation.

Please make sure to check files for TODO comments and/or 
any syntax errors.

Remember this is not a guaranteed error-free generator, 
but tried its best to do all of the heavy lifting for you.

Also, please consider fixing any whitespace issues. 
Otherwise, Field may not be happy :)
!---------------------------------------------------------!
""")

if __name__ == "__main__":

	example = """
	Example use:
	
	python3 main.py ~/blis/ -n trinv -o m -p ud -d m
	"""

	parser = ap.ArgumentParser(description="An automatic file generator for level 4 operations. This generator will attempt to generate all necessary files BLIS needs to create a new operation. This generator is meant to function as a productivity tool and not a guaranteed, error-free code generator.",
	    epilog=example,
	    formatter_class=ap.RawDescriptionHelpFormatter)

	parser.add_argument(
	    "blis_directory",
	    type=str,
	    help="The location of the current BLIS directory to insert code"
	)

	parser.add_argument(
	    "--operation_name", 
	    "-n",
	    type=str, 
	    required=True,
	    help="The name of the new operation"
	)

	parser.add_argument(
	    "--object_types",
	    "-o",
	    type=str, 
	    required=True,
	    help="The objects that will be passed in as parameters to function calls. Valid characters are 's' for scalar, 'v' for vector, and 'm' for matrix. \n e.g. -o mm (for an operation that deals with two matrices)"
	)

	parser.add_argument(
	    "--parameter_types",
	    "-p",
	    type=str, 
	    required=True,
	    help="The parameters specified for a given operation. Valid characters to specify parameters include 's' for side (solving for right or left hand side), 'u' for uplo (upper/lower triangular storage), 'c' for conj (conjugation), 'h' for trans (all types of transposes), and 'd' for diag (unit/non-unit diagonal) \n e.g. ud (for an operation that must consider uplo and diag)"
	)

	parser.add_argument(
	    "--dimensions",
	    "-d",
	    type=str,
	    required=True,
	    help="Dimensions specified for a given problem statement. The order of these parameters should be 'm', 'n', 'k'. \n e.g. mn (for problems that specify dimensions m and n)"
	)

	parser.add_argument(
	    "--num_variants",
	    "-v",
	    type=int,
	    default=1,
	    help="The number of variants for a given operation. This is parameter should be an integer value. The default value is 1."
	)
	
	args = parser.parse_args()

	main(args)
