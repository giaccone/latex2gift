# latex2xml
Small script to perform conversion from LaTeX to xml moodle format 

## Instruction

1. Download `latex2xml.py` and `calculated.py` (or the entire repository),
2. write your LaTeX file following the syntax in `example.tex` (it is in the repository)
3. run the code `latex2xml.py` providing also as additional parameter the name of the LaTeX file (e.g. `example.tex`),

Example:
```bash
# python 3+ is required
python latex2xml.py example.tex
```

4. you will find a file named `<your_LaTeX_file>.xml` (e.g. `example.xml`) that che be imported in moodle.

## About the dataset generation

The generation of dataset (i.e. the parameters of the question) are generated within Python. Currently two method are supported:
* uniform distribution
* list (manually defined)

In the second case one must provide all the data for the uniform distribution even if it is unused. This is due to the fact the on the moodle web interface those informations must be always provided.
