import argparse
import os.path
import pyperclip
import re

parser = argparse.ArgumentParser(
    prog='YAML2Properties',
    description='Simple script for convert YAML to Properties file format.'
)
parser.add_argument('file', help='Path of YAML file')

args = parser.parse_args()

print('YAML File : %s' % args.file)

if not os.path.isfile(args.file):
    raise ValueError(args.file + ' is not file')

formatted = ''

with open(args.file) as f:
    lines = f.readlines()

prop = []

output = ''

for line in lines:
    value = re.search(r'(?<=:).+', line)
    tabs = re.findall(r'(\s\s)', line)
    ignore = re.search(r'^\s?[#-]', line)

    if ignore or not line.strip():
        output += '\n'
        continue

    index = len(tabs) if tabs else 0

    result_prop = re.search(r'.+(?=:\s)', line)
    
    if index is 0:
        prop = []
        prop.append(result_prop.group().strip())
    else:
        prop_name = result_prop.group(0).strip()

        while prop and index < len(prop):
            prop.pop()

        prop.append(prop_name)

    if value and value.group().strip():
        p = '.'.join(prop) + ' = ' + value.group().strip() + '\n'
        output += p

# Prepare write file
splited_name = args.file.split(".")
file_path = ''.join(splited_name[:len(splited_name) - 1]) + '.properties'

# For debug output
#print(output) 

print('\nSave to file : ' + file_path)
 
 # Write file
file_props = open(file_path,'w+')
file_props.write(output)
file_props.close()

print('Done!')