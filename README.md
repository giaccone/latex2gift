# latex2xml
Small script to perform conversion from LaTeX to xml moodle format 

## Instruction

1. Download the file `latex2xml.py` (or the entire repository),
2. write you LaTeX file following the syntax in `example.tex`,
3. run the code `latex2xml.py` giving it as additional parameter the name of the LaTeX file (e.g. `example.tex`),

Example:
```bash
python latex2xml.py example.tex
```

4. you will find a file named `<your_LaTeX_file>.xml` (e.g. `example.xml`) that che be imported in moodle.