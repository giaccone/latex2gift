# import libraries
import sys

print("\033[93m", end='')
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
    print("\nPlease enter the path of the folder with your images (on Moodle Server):")
    print("\033[0m", end='')
    print("        * leave it empty (i.e. press return) to use the variable \033[93m'http://dummy_path/'\033[0m so that'")
    print("          you can find/replace it later.")
    
    img_path = input()
    if img_path == '':
        img_path = 'http://dummy_path/'

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
    n_multi = 0
    n_true_false = 0
    n_numerical = 0

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

    # start reading LaTeX file
    print("\033[93m", end='')
    print("\n-------------------------------------------")
    print("\033[0m", end='')
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
                    n_multi += 1
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
                    n_true_false += 1
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
                    n_numerical += 1
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
    print("\033[93m", end='')
    print("\n-------------------------------------------")
    print("\033[0m", end='')
    print("\033[1mTotal\033[0m questions written:  {}".format(n, fout))
    print("  * \033[1mmultiple choice\033[0m:  {}".format(n_multi, fout))
    print("  * \033[1mtrue-false\033[0m:       {}".format(n_true_false, fout))
    print("  * \033[1mnumerical\033[0m:        {}".format(n_numerical, fout))
    print("\033[93m", end='')
    print("-------------------------------------------\n\n")
    print("\033[0m", end='')


