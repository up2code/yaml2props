import argparse
import os.path
import pyperclip
import re

TAB_SIZE = 2
USE_SPACES = True

parser = argparse.ArgumentParser(
    prog = 'YAML2Properties',
    description = 'Simple script for convert YAML to Properties file format.'
)
parser.add_argument('file', help = 'Path of YAML file')

args = parser.parse_args()

print('YAML File : %s' % args.file)

if not os.path.isfile(args.file):
    raise ValueError(args.file + ' is not file')

formatted = ''

with open(args.file) as f:
    lines = f.readlines()

prop = []
output = ''
array_object = False

for line in lines:
    ignore = re.search(r'^\s*#', line)
    array_line = re.search(r'^\s*-\s', line) is not None

    if not array_line:
        array_index = -1

    if ignore or not line.strip() or not ':' in line and not array_line:
        output += '\n' if len(output) else ''
        continue

    tabs = re.findall(r'(' + (TAB_SIZE * '\s') + ')', line.split(':')[0])

    index = len(tabs) if tabs else 0

    result_prop = re.search(r'.+(?=:\s)', line)
    
    if index is 0:
        prop = []
        prop.append(result_prop.group().strip())
    else:
        if array_line:
            array_index += 1
        else:
            prop_name = result_prop.group(0).strip()

        while array_index < 0 and prop and index < len(prop):
            prop.pop()

        if array_index < 0:
            prop.append(prop_name)

    value = re.search(r'(?<=:).+', line) if array_index < 0 else re.search(r'(?<=-\s).+', line)

    if value and value.group().strip():
        p = '%(key)s%(idx)s%(spc)s=%(spc)s%(value)s\n' % {
            'key': '.'.join(prop),
            'idx': ('[%d]' % array_index) if array_index >= 0 else '',
            'spc': ' ' if USE_SPACES else '',
            'value': value.group().strip()
        }
        output += p

# Prepare write file
file_path = re.sub(r'\..+$', '.properties', args.file)

# For debug output
#print(output) 

print('\nSave to file : ' + file_path)
 
 # Write file
file_props = open(file_path,'w+')
file_props.write(re.sub(r'\n\n\n+', '\n\n', output))
file_props.close()

print('Done!')