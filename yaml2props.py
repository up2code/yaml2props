import argparse
import os.path
import pyperclip
import re
import os

TAB_SIZE = 2
USE_SPACES = True

parser = argparse.ArgumentParser(
    prog = 'YAML2Properties',
    description = 'Simple script for convert YAML to Properties file format.'
)
parser.add_argument('file', help = 'Path of YAML file')
parser.add_argument('--output', help = 'Output path. Default is same path of input file by replace extension to .properties')

args = parser.parse_args()

print('YAML File : %s' % args.file)

output_file_path = args.output

if(not output_file_path):
    output_file_path = os.path.splitext(args.file)[0]+'.properties'

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

print('\nSave to file : ' + output_file_path)
 
 # Write file
file_props = open(output_file_path,'w+')
file_props.write(re.sub(r'\n\n\n+', '\n\n', output))
file_props.close()

print('Done!')