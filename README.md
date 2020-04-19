# latex2gift
Small script to perform conversion from LaTeX to gift (gift = one of the Moodle format file)

## Instruction

1. Download the file `latex2gift.py` (or the entire repository)
2. Write you LaTeX file following the syntax in `example.tex`
3. run the code `latex2gift.py` giving it the following additional parameters
    * name of the classroom
    * name of the LaTeX file
    * name of the output file in the format `whatever_name.txt`


Example:
```bash
python latex2gift.py my_classrom example.tex output.txt
```

You can obtain a short guide by running the code with `--help`:
```bash
python latex2gift.py --help
```