# import libraries
import sys
from calculated import Calculated, DataSet, begin_xml, write_question, write_answer, write_dataset

# decode sys.argv
fname = sys.argv[1]
fout = fname.replace('.tex','.xml')

# max LaTeX commands
latex_command = {r'\Omega':r'\Omega',
                r'\mathrm':r'\mathrm',
                r'\bar':r'\bar',
                r'\mu':r'\mu',
                r'\cos':r'\cos',
                r'\varphi':r'\varphi',
                r'\sqrt':r'\sqrt'}

# math environment LaTeX to html
def replace_dollars(question_string, flag):
    if "$" not in question_string:
        return question_string
    elif flag == 0:
        question_string = question_string.replace("$","\\(", 1)
        return replace_dollars(question_string, flag=1)
    elif flag == 1:
        question_string = question_string.replace("$","\\)", 1)
        return replace_dollars(question_string, flag=0)

# initialization
category = ""
name = ""
text = ""
answer = ""
defaultgrade = ""
fraction = ""
tolerance = ""
tolerancetype = ""
correctanswerformat = ""
correctanswerlength = ""
dimension = ""
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
        if len(line.strip()) > 0:
            if line.strip()[0] == '%':
                pass
            else:
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
                        answer = (element.replace(r"\texttt{","").strip())[:-1]
                        # replace LaTeX notation for curly brackets
                        answer = answer.replace(r"\}",r"}").replace(r"\{",r"{")
                        
                    
                    elif r'\item defaultgrade' in line:
                        defaultgrade = float(element)
                    elif r'\item fraction:' in line:
                        fraction = int(element)
                    elif r'\item tolerance:' in line:
                        tolerance = float(element)
                    elif r'\item tolerancetype:' in line:
                        tolerancetype = (element.split("%"))[0].strip()
                    elif r'\item correctanswerformat:' in line:
                        correctanswerformat = (element.split("%"))[0].strip()
                    elif r'\item correctanswerlength:' in line:
                        correctanswerlength = int(element)
                    elif r'\item dimension:' in line:
                        if 'list' in element.lower():
                            dimension = element.strip()
                        else:
                            dimension = int(element)
                        get_answer = False
                
                # enable/disable get parameters
                elif r'\begin{description}' in line:
                    if get_param_name is False:
                        get_param_name = True
                    else:
                        get_param_prop = True
                
                elif r'\end{description}' in line:
                    if get_param_prop is True:
                        get_param_prop = False
                    else:
                        get_param_name = False

                        # make LaTeX to html conversion for text
                        text = replace_dollars(text, flag=0)
                        text = text.replace(r"\}",r"}").replace(r"\{",r"{")
                        for key in latex_command:
                            text = text.replace(key, latex_command[key])

                        # summarize question
                        Q = Calculated(name,
                                       text,
                                       answer,
                                       defaultgrade,
                                       fraction,
                                       tolerance,
                                       tolerancetype,
                                       correctanswerformat,
                                       correctanswerlength,
                                       dimension,
                                       [DataSet(n,*p) for n, p in zip(param_name, param_prop)])
                        
                        questions.append(Q)
                        
                        # reset variables
                        name = ""
                        text = ""
                        answer = ""
                        defaultgrade = ""
                        fraction = ""
                        tolerance = ""
                        tolerancetype = ""
                        correctanswerformat = ""
                        correctanswerlength = ""
                        dimension = ""
                        get_question_text = False
                        get_answer = False

                        param_name = []
                        param_prop = []
                        param_prop_temp = []
                        get_param_name = False
                        get_param_prop = False


                        

                # get category
                elif r"\section" in line:
                    category = ((line.split(":")[1]).replace("}","")).strip()
                # get question name
                elif r"\subsection" in line:
                    name = ((line.split("{")[1]).replace("}","")).strip()
                    get_question_text = True
                
                # get parameter name
                if get_param_name is True:
                    if r'\item[param:]' in line:
                        param_name.append(line.split("]")[1].strip())
                # get parameter properties
                if get_param_prop is True:
                    if r'\item[database]' in line:
                        param_prop_temp.append(line.split("]")[1].split("%")[0].strip())
                    elif r'\item[minimum]' in line:
                        current_value = float(line.split("]")[1].split("%")[0].strip())
                        if abs(current_value - int(current_value)) == 0:
                            param_prop_temp.append(int(current_value))
                        else:
                            param_prop_temp.append(current_value)
                    elif r'\item[maximum]' in line:
                        current_value = float(line.split("]")[1].split("%")[0].strip())
                        if abs(current_value - int(current_value)) == 0:
                            param_prop_temp.append(int(current_value))
                        else:
                            param_prop_temp.append(current_value)
                    elif r'\item[decimals]' in line:
                        param_prop_temp.append(int(line.split("]")[1].split("%")[0].strip()))
                    elif r'\item[distribution]' in line:
                        current_item = line.split("]")[1].split("%")[0].strip()
                        # unpack list (if any)
                        if "(" in current_item:
                            current_item = current_item.replace("(", '')
                            current_item = current_item.replace(")", '')
                            current_item = [float(str(k)) for k in current_item.split(",")]
                            current_item = [int(k) if abs(k - int(k)) == 0 else k for k in current_item]
                        
                        param_prop_temp.append(current_item)
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




