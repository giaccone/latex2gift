import sys
course = sys.argv[1]
fname = sys.argv[2]
fout = sys.argv[3]

gift = ""
tab = "    "
question = ""
answer = ""
Qtype = ""
latex_command = {'\Omega':'\\\\Omega',
                 '\mathrm':'\\\\mathrm',
                 '\bar':'\\\\bar',
                 '\mu':'\\\\mu',
                 '\cos':'\\\\cos',
                 '\varphi':'\\\\varphi'}

def replace_dollars(question_string, flag):
    if "$" not in question_string:
        return question_string
    elif flag == 0:
        question_string = question_string.replace("$","\\\\(", 1)
        return replace_dollars(question_string, flag=1)
    elif flag == 1:
        question_string = question_string.replace("$","\\\\)", 1)
        return replace_dollars(question_string, flag=0)

with open(fname, 'r') as file:
    for line in file:
        if "CAT;" in line:
            gift += "$CATEGORY: $course$/Default per " +  course + "/" + line.split(";")[-1] + "\n"
        elif "NAME;" in line:
            name = (line.split(";")[-1]).replace("\n","")
            name = name.strip()
            print(name)
        elif "TYPE;" in line:
            Qtype = (line.split(";")[-1]).replace("\n","")
            Qtype = Qtype.strip()
        elif "Q;" in line:
            question += "::" + name + "::[html]<p>" + ((line.split(";")[-1]).replace("\n","")).replace("=","\\=") + "<br></p>"
        elif "\includegraphics" in line:
            index = line.index("{")
            fig = line[index+1:-2] + '.png'

            question += '<p><img src\="https://exercise.polito.it/pluginfile.php/333171/mod_folder/content/0/' + fig + '" alt\="" role\="presentation" style\="vertical-align\:text-bottom; margin\: 0 .5em;" class\="img-responsive" width\="667" height\="433"><br></p><p><br></p>'
        elif "DATA;" in line:
            question += "<p>" + ((line.split(";")[-1]).replace("\n","")).replace("=","\\=") + "<br></p>"
        
        if Qtype.lower() == 'multiple':
            if "A+" in line:
                score = (line.split(";")[0]).split('+')[1]
                ans = ((line.split(";")[-1]).replace("\n","")).replace("=","\\=")
                answer += tab + "=<p>" + ans + "<br></p>\n"
            elif "A-" in line:
                score = (line.split(";")[0]).split('-')[1]
                ans = ((line.split(";")[-1]).replace("\n","")).replace("=","\\=")
                answer += tab + "~%-" + score + "%<p>" + ans + "<br></p>\n"
            elif "END;" in line:
                question = replace_dollars(question, flag=0)
                answer = replace_dollars(answer, flag=0)
                question = question.replace("{","\\{")
                question = question.replace("}","\\}")
                answer = answer.replace("{","\\{")
                answer = answer.replace("}","\\}")
                gift += question + "{\n" + answer + "}\n\n\n"
                question = ""
                answer = ""
                Qtype = ""
        elif Qtype.lower() == 'true-false':
            if "A" in line:
                answer = ((line.split(";")[-1]).replace("\n","")).upper()
                answer = answer.strip()
            elif "END;" in line:
                question = replace_dollars(question, flag=0)
                question = question.replace("{","\\{")
                question = question.replace("}","\\}")
                gift += question + "{" + answer + "}\n\n\n"
                question = ""
                answer = ""
                Qtype = ""
        
        if Qtype.lower() == 'numerica':
            if "A+" in line:
                score = (line.split(";")[0]).split('+')[1]
                result = (line.split(";")[1]).replace("\n","")
                answer += tab + "=%" + score + "%" + result + "#\n"
            elif "END;" in line:
                question = replace_dollars(question, flag=0)
                question = question.replace("{","\\{")
                question = question.replace("}","\\}")
                gift += question + "{#\n" + answer + "}\n\n\n"
                question = ""
                answer = ""
                Qtype = ""
                

        else:
            pass



for key in latex_command:
    gift = gift.replace(key, latex_command[key])

            

with open(fout, 'w') as file:
    file.write(gift)


