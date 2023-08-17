# ----------------[Define Imports]-----------------
import argparse
import os.path

# ------------[Define Global Variables]------------
unprocessed_data = []
sourcefile = ""
outputfile = f"{os.path.dirname(os.getcwd())}\Email_Dissector\output\output.txt"
parser = argparse.ArgumentParser(description="", exit_on_error=True, add_help=True)

# ---------------[Define Parser Flags]---------------
parser.add_argument("-f", "--filename", required=True, 
                    dest="sourcefile",
                    help="Source filename (.txt) containing Original Email Message"
                  )
parser.add_argument("-o", "--output", 
                    dest="outputfile",
                    help=f"Output destination (.txt or .csv). Default: {outputfile}"
                  )


# -----------------[Process Flags]-------------------
# process flags
args = parser.parse_args()
sourcefile = args.sourcefile

def is_valid_file(parser, filename):
  if not os.path.exists(filename):
    parser.error(f"[ERR]: The file {filename} cannot be found.")
  else:
    return True

# get data from file
def read_txt_file(parser, filename):
  try:
    with open(filename, 'r') as file:
      unprocessed_data = file.readlines()
      file.close()
      print(unprocessed_data)
  except IOError as err:
    parser.error(err)

# Checks if a source file was provided and verifies that it has
# a valid path and can be opened.
if sourcefile != "":
  if is_valid_file(parser, sourcefile):
    read_txt_file(parser, sourcefile)
    print(f"[*] Read sourcefile: {sourcefile}.")
  else:
    parser.error(f"[ERR]: Invalid filename.")
else:
  parser.error(f"[ERR]: Script requires a input filename")

if os.path.exists(outputfile):
  print(f"[*] Output filename is valid!")
else:
  try:
    f = open(outputfile, 'w+')
    f.write("")
    f.close()
  except:
    parser.error("[ERR] Output file could not be found nor created.")

print(unprocessed_data)



#------------------[Dissect Data]------------------
# dissection module


# -----------[Process and Display Output]-----------
# display output