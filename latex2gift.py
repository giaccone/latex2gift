# import libraries
import sys

# check sys.argv
if (sys.argv[1]).lower() == '--help':
    print("\n\nYou must call the script in this way\n")
    print("python latex2gipt.py <course> <latex_file.tex> <output_file.txt>\n\n")
    sys.exit()
elif len(sys.argv) < 4:
    print("\n\nToo few arguments\n\n")
    print("You must call the script in this way\n")
    print("python latex2gipt.py <course> <latex_file.tex> <output_file.txt>\n\n")
    sys.exit()
elif len(sys.argv) > 6:
    print("\n\nToo many arguments\n\n")
    print("You must call the script in this way\n")
    print("python latex2gipt.py <course> <latex_file.tex> <output_file.txt>\n\n")
    sys.exit()
else:
    # get path of the image
    print("Please enter the path of the folder with you images (on Moodle Server):\n")
    img_path = input()

    # decode sys.argv
    course = sys.argv[1]
    fname = sys.argv[2]
    fout = sys.argv[3]

    # initilize variables
    gift = ""
    tab = "    "
    question = ""
    answer = ""
    Qtype = ""
    n = 0

    # max LaTeX commands
    latex_command = {'\Omega':'\\\\Omega',
                    '\mathrm':'\\\\mathrm',
                    '\bar':'\\\\bar',
                    '\mu':'\\\\mu',
                    '\cos':'\\\\cos',
                    '\varphi':'\\\\varphi'}

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

    # start reading LaTeX file
    print("\n-------------------------------------------")
    with open(fname, 'r') as file:
        for line in file:
            # get category
            if "CAT;" in line:
                gift += "$CATEGORY: $course$/Default per " +  course + "/" + line.split(";")[-1] + "\n"
            # get question name
            elif "NAME;" in line:
                name = (line.split(";")[-1]).replace("\n","")
                name = name.strip()
            # get question type. (multi, true-false, numerical)
            elif "TYPE;" in line:
                Qtype = (line.split(";")[-1]).replace("\n","")
                Qtype = Qtype.strip()
            # get question text
            elif "Q;" in line:
                question += "::" + name + "::[html]<p>" + ((line.split(";")[-1]).replace("\n","")).replace("=","\\=") + "<br></p>"
            # wrap image (if any)
            elif "\includegraphics" in line:
                index = line.index("{")
                fig = line[index+1:-2] + '.png'
                question += '<p><img src\="' + img_path + fig + '" alt\="" role\="presentation" style\="vertical-align\:text-bottom; margin\: 0 .5em;" class\="img-responsive" width\="667" height\="433"><br></p><p><br></p>'
            # get data for the question (if any)
            elif "DATA;" in line:
                question += "<p>" + ((line.split(";")[-1]).replace("\n","")).replace("=","\\=") + "<br></p>"
            
            # get answers (depending on question type)
            if Qtype.lower() == 'multi':
                # multi
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

                    n += 1
                    print(" * {}) Question: {} - Type {}".format(n, name, Qtype))

                    question = ""
                    answer = ""
                    Qtype = ""

            # true-false
            elif Qtype.lower() == 'true-false':
                if "A" in line:
                    answer = ((line.split(";")[-1]).replace("\n","")).upper()
                    answer = answer.strip()
                elif "END;" in line:
                    question = replace_dollars(question, flag=0)
                    question = question.replace("{","\\{")
                    question = question.replace("}","\\}")
                    gift += question + "{" + answer + "}\n\n\n"

                    n += 1
                    print(" * {}) Question: {} - Type {}".format(n, name, Qtype))

                    question = ""
                    answer = ""
                    Qtype = ""
            
            # numerical
            if Qtype.lower() == 'numerical':
                if "A+" in line:
                    score = (line.split(";")[0]).split('+')[1]
                    result = (line.split(";")[1]).replace("\n","")
                    answer += tab + "=%" + score + "%" + result + "#\n"
                elif "END;" in line:
                    question = replace_dollars(question, flag=0)
                    question = question.replace("{","\\{")
                    question = question.replace("}","\\}")
                    gift += question + "{#\n" + answer + "}\n\n\n"
                    
                    n += 1
                    print(" * {}) Question: {} - Type {}".format(n, name, Qtype))

                    question = ""
                    answer = ""
                    Qtype = ""
                    
            # other question type are not yet supported
            else:
                pass

    # convert LaTeX commands
    for key in latex_command:
        gift = gift.replace(key, latex_command[key])

    # write gift files
    with open(fout, 'w') as file:
        file.write(gift)
    
    # print summary
    print("\n-------------------------------------------")
    print("{} questions written in {}".format(n, fout))
    print("-------------------------------------------\n\n")


