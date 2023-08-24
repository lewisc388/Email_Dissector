# ----------------[Define Imports]-----------------
import argparse
import os.path
import json

# ------------[Define Global Variables]------------
unprocessed_data = []
processed_data = {}
sourcefile = ""
outputfile = "output\output.txt"
desc = '''
Dissect Email processes Original Email Messages into a usable dictionary format.
This allows for easy lookups of flags and the ability to integrate with automations and scripts.
'''
parser = argparse.ArgumentParser(description=desc, exit_on_error=True, add_help=True)

# ---------------[Define Parser Flags]---------------
parser.add_argument("-f", "--filename", required=True, 
                    dest="sourcefile",
                    help="Source filename (.txt) containing Original Email Message"
                  )
parser.add_argument("-o", "--output", 
                    dest="outputfile",
                    help=f"Output destination (.txt). Default: {outputfile}"
                  )


# -----------------[Process Flags]-------------------
# process flags
args = parser.parse_args()
sourcefile = args.sourcefile
if args.outputfile != "":
  outputfile = args.outputfile

# Checks if a source file was provided and verifies that it has
# a valid path and can be opened.
if sourcefile != "":
  if os.path.exists(sourcefile):
    try:
      with open(sourcefile, errors='replace') as file:
        unprocessed_data = file.readlines()
        file.close()
        print(f"[*] Sourcefile data successfully read.")
    except IOError as err:
      parser.error(err)
  else:
    parser.error(f"[ERR]: Invalid filename!")
else:
  parser.error(f"[ERR]: Script requires a input filename!")

# Checks if output file exists. If not, try to make the file
if os.path.exists(outputfile):
  print(f"[*] Output filename is valid!")
else:
  try:
    file2 = open(outputfile, 'w+')
    file2.write("")
    file2.close()
    print(f"[*] {outputfile} was made.")
  except:
    parser.error("[ERR]: Output file could not be found nor created!")

#print(unprocessed_data)

#------------------[Dissect Data]------------------
# dissection module
# Rules:
# 1) The first '\n' that is empty indicated the start of the Email Contents.
# 2) Join everything after the first empty '\n' and prepend 'Content: '
# 3) For every entry that starts with a Tab, join to previous entry.
# 4) Seperate the title from flags by the first ':' in the line.
# 5) Seperate the flags by ';'
# 6) Seperate flags and their values by "="

# Sample Structure:
# { 'Delivered-To':
#     'tester.email@gmail.com'
#    [...],
#   'ARC-Seal':
#       {'i': '1',
#        'a': 'rsa-sha256',
#        't': '1690675726',
#        'cv': 'none', 
#         [...]
#       }
# }
# Called via processed_data['ARC-Seal']['a']

# Step 1: Find the Contents section.
for line in unprocessed_data:
  if line == '\n':
    #join everything after it.
    contentstart = unprocessed_data.index(line)
    contentend = len(unprocessed_data)-1
    # copy list
    step1_processed = unprocessed_data
    # add a header for the content
    step1_processed[contentstart] = "Content: \n"
    # Join the content together.
    step1_processed[contentstart : contentend] = [''.join(step1_processed[contentstart : contentend])]
    break

# Step 2: Join all entries that start with a tab or a large whitespace.

step2_processed = []
prev_string = ""

for entry in step1_processed:
  if entry.startswith("   "):
    prev_string = prev_string.rstrip()
    # Provide appropriate spacing between semi-colon
    if prev_string.endswith(";"):
      prev_string += (" " + entry.lstrip())
    else:
      prev_string += entry.lstrip()
  else:
    if prev_string:
      step2_processed.append(prev_string)
    prev_string = entry

#if prev_string:
#  step2_processed.append(prev_string.lstrip().rstrip())

# Step 3: Define the dictionary and seperate all titles from each entry.
# The remaining values are set as either a string or as an internal dictionary.

for entry in step2_processed:
  # Find the index of the first colon
  index = entry.find(":")

  if index != -1:
    key = entry[:index].strip()
    value_str = entry[index + 1:].strip()

    if "; " in value_str and key != "Content":
      sub_dict = {}
      value_list = value_str.split("; ")

      for sub_entry in value_list:
        # Check to see if a sub_dictionary can be made if there is "="
        equ_index = sub_entry.find("=")
        # If "=" can be found, make the value a dictionary
        if equ_index != -1:
          sub_key = sub_entry[:equ_index].strip()
          sub_value = sub_entry[equ_index + 1:].strip()

          sub_dict[sub_key] = sub_value
          processed_data[key] = sub_dict
        # If no "=" can be found, then make the value a list
        else:
          processed_data[key] = value_list
    # If there is no "; " to define a seperation of entries, make the value a string
    else:
      processed_data[key] = value_str


print(processed_data)

# -----------[Process and Display Output]-----------
# Write result to outputfile. Note: any unknown characters will be 
# replaced with '?'
try:
  with open(outputfile, 'w', errors='replace') as file2:
    #file2.write(''.join(str(i) for i in processed_data))
    print(json.dumps(processed_data, indent=2), file=file2)
    file2.close()
    print(f"[*] Result outputted to {outputfile}")
except IOError as err:
  parser.error(err)
