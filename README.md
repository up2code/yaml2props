# YAML2PROPERTIES

Simple script for convert YAML to Properties file for Spring application configuration.

## Minimum requirement

- Python 2.7+
- pyperclip (pip install pyperclip)

## How to install

```sh
cp yaml2props.py /usr/local/bin/yaml2props.py
cp yaml2props.sh /usr/local/bin/yaml2props
chmod +x /usr/local/bin/yaml2props
```

## How to use

```
$ yaml2props {your_path_file}
```

or you can specific output file path by yourself with option `--output`

```
$ yaml2props {your_path_file} --output {your_destination_file_path}
```

You can try with _sample.yaml_ as example file.