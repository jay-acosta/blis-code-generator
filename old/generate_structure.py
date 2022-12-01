import os
from pathlib import Path

from files import *

def write_to_file (path, output):
    with open(path, 'w') as f:
        f.write(output)
        
def main():
    print ("Generating level 4 operation")
    print ("Please input your...")

    # get paths
    blis_path = Path(input("BLIS directory > ")).expanduser()
    level4_path = Path(os.path.join(blis_path), "frame", "4")        

    # get operation info
    op_name = input("Operation Name > ")
    obj_op_args = input("Object API Operation Arguments > ").strip().split()
    type_op_args = input("Typed API Operation Arguments > ")
    obj_op_params = input("Operation Parameters > ")
    
    print()

    op_dir = Path(os.path.join(level4_path, op_name))
    print (f"Checking to see if {op_dir} exists.")
    if not level4_path.exists():
        print (f"Making directory at {level4_path}")
        os.makedirs(level4_path)

    if not op_dir.exists():
        print (f"Making directory at {op_dir}")
        os.makedirs(op_dir)
    print ("Done.")

    # print (f"Writing to bli_{op_name}.c")
    # write_to_file(os.path.join(op_dir, f"bli_{op_name}.c"), build_op_c(op_name, obj_op_params))
    
    # print (f"Writing to bli_{op_name}.h")
    # write_to_file(os.path.join(op_dir, f"bli_{op_name}.h"), build_op_h(op_name, obj_op_params))

    print ("")

if __name__ == '__main__':
    main()
