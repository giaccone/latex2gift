# import libraries
import sys
from calculated import Calculated, DataSet, begin_xml, write_question, write_answer, write_dataset

# decode sys.argv
fname = sys.argv[1]
fout = fname.replace('.tex','.xml')

# max LaTeX commands
latex_command = {'\Omega':'\\\\Omega',
                '\mathrm':'\\\\mathrm',
                '\bar':'\\\\bar',
                '\mu':'\\\\mu',
                '\cos':'\\\\cos',
                '\varphi':'\\\\varphi',
                '\sqrt':'\\\\sqrt'}

# math environment LaTeX to html
def replace_dollars(question_string, flag):
    if "$" not in question_string:
        return question_string
    elif flag == 0:
        question_string = question_string.replace("$","\\\\(", 1)
        return replace_dollars(question_string, flag=1)
    elif flag == 1:
        question_string = question_string.replace("$","\\\\)", 1)
        return replace_dollars(question_string, flag=0)

# initialization
category = ""
name = ""
text = ""
answer = ""
fraction = ""
tolerance = ""
tolerancetype = ""
correctanswerformat = ""
correctanswerlength = ""
get_question_text = False
get_answer = False

param_name = []
param_prop = []
param_prop_temp = []
get_param_name = False
get_param_prop = False

questions = []


# read file
with open(fname, 'r') as file:
    for line in file:
        # get question text
        if get_question_text is True:
            if "\\begin{itemize}" in line:
                get_question_text = False
                get_answer = True
            else:
                text += line
        
        # get answer
        elif get_answer is True:
            element = (line.split(":")[1]).strip()
            if '\\item answer:' in line:
                answer = (element.replace("\\texttt{","").strip())[:-1]
                # replace LaTeX notation for curly brackets
                answer = answer.replace("\}","}").replace("\{","{")
                
            
            elif '\\item fraction:' in line:
                fraction = int(element)
            elif '\\item tolerance:' in line:
                tolerance = float(element)
            elif '\\item tolerancetype:' in line:
                tolerancetype = (element.split("%"))[0].strip()
            elif '\\item correctanswerformat:' in line:
                correctanswerformat = (element.split("%"))[0].strip()
            elif '\\item correctanswerlength:' in line:
                correctanswerlength = int(element)
                get_answer = False
        
        # enable/disable get parameters
        elif '\\begin{description}' in line:
            if get_param_name is False:
                get_param_name = True
            else:
                get_param_prop = True
        
        elif '\end{description}' in line:
            if get_param_prop is True:
                get_param_prop = False
            else:
                get_param_name = False

                # make LaTeX to html conversion for text
                text = replace_dollars(text, flag=0)
                text = text.replace("\}","}").replace("\{","{")
                for key in latex_command:
                    text = text.replace(key, latex_command[key])

                # summarize question
                Q = Calculated(name,
                               text,
                               answer,
                               fraction,
                               tolerance,
                               tolerancetype,
                               correctanswerformat,
                               correctanswerlength,
                               [DataSet(n,*p) for n, p in zip(param_name, param_prop)])
                
                questions.append(Q)
                
                # reset variables
                name = ""
                text = ""
                answer = ""
                fraction = ""
                tolerance = ""
                tolerancetype = ""
                correctanswerformat = ""
                correctanswerlength = ""
                get_question_text = False
                get_answer = False

                param_name = []
                param_prop = []
                param_prop_temp = []
                get_param_name = False
                get_param_prop = False


                

        # get category
        elif "\section" in line:
            category = ((line.split(":")[1]).replace("}","")).strip()
        # get question name
        elif "\subsection" in line:
            name = ((line.split("{")[1]).replace("}","")).strip()
            get_question_text = True
        
        # get parameter name
        if get_param_name is True:
            if '\item[param:]' in line:
                param_name.append(line.split("]")[1].strip())
        # get parameter properties
        if get_param_prop is True:
            if '\item[database]' in line:
                param_prop_temp.append(line.split("]")[1].split("%")[0].strip())
            elif '\item[minimum]' in line:
                param_prop_temp.append(int(line.split("]")[1]))
            elif '\item[maximum]' in line:
                param_prop_temp.append(int(line.split("]")[1]))
            elif '\item[decimals]' in line:
                param_prop_temp.append(int(line.split("]")[1]))
            elif '\item[value]' in line:
                param_prop_temp.append(int(line.split("]")[1]))
            elif '\item[distribution]' in line:
                param_prop_temp.append(line.split("]")[1].split("%")[0].strip())
                param_prop.append(param_prop_temp)
                param_prop_temp = []



# write xml
begin_xml(fout, category)

for quest in questions:
    write_question(fout, quest)
    write_answer(fout, quest)
    write_dataset(fout, quest)

with open(fout, 'a') as file:
    file.write("</quiz>\n")


# print summary
print("\n\nQuiz: \033[93m{}\033[0m imported with the following Calculated questions:".format(category))
print("      " + "\033[93m-\033[0m" * len(category))
print("\n")
for k, quest in enumerate(questions):
    if k < 10:
        num = " " + str(k)
    else:
        num = str(k)
    print("    * question {}: \033[93m{}\033[0m ({} parameters)".format(num, quest.name, len(quest.parameters)))
print("\n\n")




