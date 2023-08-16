# ----------------[Define Imports]-----------------
import argparse
import os.path

# ------------[Define Global Variables]------------
unprocessed_data = ""
sourcefile = ""
parser = argparse.ArgumentParser(description="")

# ---------------[Define Parser Flags]---------------
parser.add_argument("-f", "--filename", required=True, 
                    dest="sourcefile",
                    help="Source filename (.txt) containing Original Email Message",
                    metavar="FILE"
                     )
parser.add_argument("-o", "--output")


# -----------------[Process Flags]-------------------
# process flags

args = parser.parse_args()

def is_valid_file(parser, arg):
  if not os.path.exists(arg):
    parser.error(f"[ERR]: The file {arg} cannot be found.")
  else:
    read_txt_file(arg)
  

# get data from file
def read_txt_file(filename):
  with open(filename, 'r') as file:
    unprocessed_data = file.read()
    file.close()

#------------------[Dissect Data]------------------
# dissection module
class Dissect:
  # define the "content" dictionary. This will store the content
  # of the email that we dissect and stores it in a dictionary format.
  content = {}
  def __init__(self, unprocessed_data):
    pass




# -----------[Process and Display Output]-----------
# display output