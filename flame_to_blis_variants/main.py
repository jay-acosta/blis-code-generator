import os
from re import sub
from translation_templates import *
from pathlib import Path
from file_io import *
import argparse

def main(args):
    output_dir = Path(args.output_dir)
    print("Writing output to", output_dir)

    # Quit if output directory is a file
    if output_dir.exists() and not output_dir.is_dir():
        print("Output directory", output_dir, "exists and is not a directory.")
        print("Quitting...")
        return

    # Create the output directory if it does not exist
    if not output_dir.exists():
        print("Creating directory", output_dir)
        os.makedirs(output_dir)
        print(output_dir, "has been created.")

    # start REPL
    while True:
        # read user input, break if no input or if EOF is reached
        try:
            user_file = input("Input a file to translate: ")
        except:
            print("Quitting...")
            break

        if not user_file:
            print("Quitting...")
            break

        print() # spacing 
        
        # find the input FLAME file
        flame_file = Path(user_file).expanduser()
        if not flame_file.exists():
            print("File not found.")
            continue

        # get output name
        name = get_op_func_name_from_path(flame_file)
        new_op_file_path = os.path.join(output_dir, f"{name}.c")

        print(f"Writing to {new_op_file_path}")

        if "opt" in name:
            # translate the unblocked object code to create the optimized variant
            # TODO: add functionality to read variants from the typed FLAME API 

            potential_unb = Path(sub("opt", "unb", str(flame_file)))

            if potential_unb.exists():
                # work on the unblocked instead!
                dump_content_to_file(new_op_file_path, translate_flame_to_blis_tapi_file(potential_unb))
            else:
                print("Can't find a suitable unblocked version for %s to translate. Sorry!" % name)
        else:
            dump_content_to_file(new_op_file_path, translate_flame_to_blis_oapi_file(flame_file))

        print("Done!")
        print()
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--output_dir", "-o", default="output")

    args = parser.parse_args()

    main(args)
