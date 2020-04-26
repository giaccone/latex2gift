import base64
import random

class Calculated:
    
    def __init__(self, name, text, answer, fraction, tolerance, tolerancetype, correctanswerformat, correctanswerlength, dimension, parameters):
        self.name = name
        self.text = text
        self.answer = answer
        self.fraction = fraction
        self.tolerance = tolerance
        self.tolerancetype = tolerancetype
        self.correctanswerformat = correctanswerformat
        self.correctanswerlength = correctanswerlength
        self.dimension = dimension
        self.parameters = parameters
    
    def __str__(self):
        string_format = "name = {}\n".format(self.name)
        string_format += "text = {}\n".format(self.text[:20] + " ...")
        string_format += "answer = {}\n".format(self.answer)
        string_format += "tolerance = {}\n".format(self.tolerance)
        string_format += "fraction = {}\n".format(self.fraction)
        string_format += "tolerancetype = {}\n".format(self.tolerancetype)
        string_format += "correctanswerformat = {}\n".format(self.correctanswerformat)
        string_format += "correctanswerlength = {}\n".format(self.correctanswerlength)
        string_format += "dimension = {}\n".format(self.dimension)
        for k, ele in enumerate(self.parameters):
            string_format += "  * param1 = {}\n".format(ele.name)
            string_format += "     . database = {}\n".format(ele.database)
            string_format += "     . minimum = {}\n".format(ele.minimum)
            string_format += "     . maximum = {}\n".format(ele.maximum)
            string_format += "     . decimals = {}\n".format(ele.decimals)
            string_format += "     . distribution = {}\n".format(ele.distribution)

        return string_format


class DataSet:

    def __init__(self, name, database, minimum, maximum, decimals, distribution):
        self.name = name
        self.database = database
        self.minimum = minimum
        self.maximum = maximum
        self.decimals = decimals
        self.distribution = distribution


def begin_xml(fout, category):
    content = """<?xml version="1.0" encoding="UTF-8"?>\n"""
    content += """<quiz>\n"""
    content += """    <!-- question: 0  -->\n"""
    content += """    <question type="category">\n"""
    content += """        <category>\n"""
    content += """        <text>$course$/{}</text>\n""".format(category)

    content += """        </category>\n"""
    content += """    </question>\n"""

    with open(fout, 'w') as file:
        file.write(content)


def write_question(fout, question):
    # write name
    content = """    <question type="calculated">\n"""
    content += """        <name>\n"""
    content += """        <text>{}</text>\n""".format(question.name)
    content += """        </name>\n"""

    with open(fout, 'a') as file:
        file.write(content)
    
    # write text
    content = """        <questiontext format="html">\n"""
    content += """        <text><![CDATA["""
    for ele in question.text.split('\n'):
        if ele != '':
            if '\includegraphics' in ele:
                img = ele.split("{")[1].replace("}","").strip()
                if not img.lower().endswith('.png'):
                    img += '.png'
                img_enc = base64.b64encode(open(img, "rb").read())
                
                content += """<p><IMG height=162 SRC="data:image/png;base64,"""
                content += img_enc.decode('ascii') + '"> </p>'
            
            else:    
                content += "<p>"
                content += ele
                content += "</p>\n"
        
    content = content[:-1] + "]]></text>\n    </questiontext>\n"

    # write default settings
    content +="""    <generalfeedback format="html">\n"""
    content +="""      <text></text>\n"""
    content +="""    </generalfeedback>\n"""
    content +="""    <defaultgrade>1.0000000</defaultgrade>\n"""
    content +="""    <penalty>0.3333333</penalty>\n"""
    content +="""    <hidden>0</hidden>\n"""
    content +="""    <synchronize>0</synchronize>\n"""
    content +="""    <single>0</single>\n"""
    content +="""    <answernumbering>abc</answernumbering>\n"""
    content +="""    <shuffleanswers>1</shuffleanswers>\n"""
    content +="""    <correctfeedback>\n"""
    content +="""      <text></text>\n"""
    content +="""    </correctfeedback>\n"""
    content +="""    <partiallycorrectfeedback>\n"""
    content +="""    <text></text>\n"""
    content +="""    </partiallycorrectfeedback>\n"""
    content +="""    <incorrectfeedback>\n"""
    content +="""      <text></text>\n"""
    content +="""    </incorrectfeedback>\n"""

    with open(fout, 'a') as file:
        file.write(content)


def write_answer(fout, question):

    toll_type = {'relative':1,'nominal':2,'geometric':3}
    answ_format = {'decimal':1,'significant figures':2}


    content ="""    <answer fraction="{}">\n""".format(question.fraction)
    content +="""      <text>{}</text>\n""".format(question.answer)
    content +="""      <tolerance>{}</tolerance>\n""".format(question.tolerance)
    content +="""      <tolerancetype>{}</tolerancetype>\n""".format(toll_type[question.tolerancetype])
    content +="""      <correctanswerformat>{}</correctanswerformat>\n""".format(answ_format[question.correctanswerformat])
    content +="""      <correctanswerlength>{}</correctanswerlength>\n""".format(question.correctanswerlength)
    content +="""      <feedback format="html">\n"""
    content +="""      <text></text>\n"""
    content +="""      </feedback>\n"""
    content +="""      </answer>\n"""
    content +="""      <unitgradingtype>0</unitgradingtype>\n"""
    content +="""      <unitpenalty>0.1000000</unitpenalty>\n"""
    content +="""      <showunits>3</showunits>\n"""
    content +="""      <unitsleft>0</unitsleft>\n"""

    with open(fout, 'a') as file:
        file.write(content)


def write_dataset(fout, question):
    content = """    <dataset_definitions>\n"""

    for param in question.parameters:

        content += """    <dataset_definition>\n"""
        content += """    <status><text>{}</text>\n""".format(param.database)
        content += """    </status>\n"""
        content += """    <name><text>{}</text>\n""".format(param.name)
        content += """    </name>\n"""
        content += """    <type>calculated</type>\n"""
        # The following line is no more used because only uniform distrib is supported.
        # When list is selected insted of uniform, the following is still set to
        # uniform because it is unused.

        # content += """    <distribution><text>{}</text>\n""".format(param.distribution)
        content += """    <distribution><text>uniform</text>\n"""

        content += """    </distribution>\n"""
        content += """    <minimum><text>{}</text>\n""".format(param.minimum)
        content += """    </minimum>\n"""
        content += """    <maximum><text>{}</text>\n""".format(param.maximum)
        content += """    </maximum>\n"""
        content += """    <decimals><text>{}</text>\n""".format(param.decimals)
        content += """    </decimals>\n"""

        if isinstance(question.dimension, int):
            content += """    <itemcount>{}</itemcount>\n""".format(question.dimension)
        elif question.dimension.lower() == 'list':
            content += """    <itemcount>{}</itemcount>\n""".format(len(param.distribution))
            
        content += """      <dataset_items>\n"""
        
        if isinstance(question.dimension, int):
            for n in range(question.dimension):
                content += """        <dataset_item>\n"""
                content += """        <number>{}</number>\n""".format(n + 1)
                if param.decimals == 0:
                    value = random.randint(param.minimum, param.maximum)
                else:
                    value = random.uniform(param.minimum, param.maximum)
                    value = round(value, param.decimals)
                content += """          <value>{}</value>\n""".format(value)
                content += """        </dataset_item>\n"""
        elif question.dimension.lower() == 'list':
            for n, value in enumerate(param.distribution):
                content += """        <dataset_item>\n"""
                content += """        <number>{}</number>\n""".format(n + 1)
                content += """          <value>{}</value>\n""".format(value)
                content += """        </dataset_item>\n"""

            
        content += """      </dataset_items>\n"""
        if isinstance(question.dimension, int):
            content += """    <number_of_items>{}</number_of_items>\n""".format(question.dimension)
        elif question.dimension.lower() == 'list':
            content += """    <number_of_items>{}</number_of_items>\n""".format(len(param.distribution))
        
        content += """    </dataset_definition>\n"""
    
    content += """    </dataset_definitions>\n"""
    content += """</question>\n\n"""
    
    with open(fout, 'a') as file:
        file.write(content)