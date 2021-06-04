import time
# Interpreter
#file_name = "Esolang1.nvm"
try:
    file_name = str(input("Filename: "))
except FileNotFoundError:
    file_name = str(input("Sorry, I can't find that file. Can you tell me the filename again? "))
file = open(file_name, "r")
c = file.readlines()
i = 0
for l in c:
    c[i] = c[i].replace("\n","")
    i += 1
file.close()

variables = {"answer": "NULL"}
loop_code = []
loop_time = 0
loop_state = False
if_state = False
if_yes_state = False
def commands(command,arguments):
    iterator = 0
    for argument in arguments:
        arguments[iterator] = argument.replace("*44",",")
        iterator+=1
    if command == "make":
        if arguments[1][0] == "$":
            try:
                try:
                    if arguments[2] == "+":
                        if arguments[3][0] == "$" and arguments[1][0] == "$":
                            variables[arguments[0]] = str(int(variables[arguments[1][1:len(arguments[1])]]) + int(variables[arguments[3][1:len(arguments[3])]]))
                        elif arguments[3][0] != "$" and arguments[1][0] == "$":
                            variables[arguments[0]] = str(int(variables[arguments[1][1:len(arguments[1])]]) + int(arguments[3]))
                        elif arguments[3][0] == "$" and arguments[1][0] != "$":
                            variables[arguments[0]] = str(int(arguments[1]) + int(variables[arguments[3][1:len(arguments[3])]]))
                    elif arguments[2] == "++":
                        if arguments[3][0] == "$" and arguments[1][0] == "$":
                            variables[arguments[0]] = variables[arguments[1][1:len(arguments[1])]] + variables[arguments[3][1:len(arguments[3])]]
                        elif arguments[3][0] != "$" and arguments[1][0] == "$":
                            variables[arguments[0]] = variables[arguments[1][1:len(arguments[1])]] + arguments[3]
                        elif arguments[3][0] == "$" and arguments[1][0] != "$":
                            variables[arguments[0]] = arguments[1] + variables[arguments[3][1:len(arguments[3])]]
                except IndexError:
                    variables[arguments[0]] = variables[arguments[1][1:len(arguments[1])]]
            except KeyError:
                print("[Error1] Variable not found")
        else:
            variables[arguments[0]] = arguments[1]
    if command == "print":
        final_print = ""
        for argument in arguments:
            if argument[0] == "$":
                #print(argument)
                try:
                    final_print += variables[argument[1:len(argument)]]
                except KeyError:
                    print("[Error2] Variable not found")
            else:
                final_print += argument
        print(final_print)
    if command == "input":
        answer = str(input(arguments[0]))
        variables["answer"] = answer
# loops over all of the lines in the code
for line in c:
    try:
        command = line.split(",")[0]
        arguments = line.split(",")[1:len(line)]

        if command == "if":
            if_state = True
            if arguments[1] == "==":
                if arguments[0][0] == "$":
                    arguments[0] = variables[arguments[0][1:len(arguments[0])]]
                if arguments[2][0] == "$":
                    arguments[0] = variables[arguments[2][1:len(arguments[2])]]
                try:
                    # int
                    if int(arguments[0]) == int(arguments[2]):
                        continue
                    else:
                        if_yes_state = True
                        continue
                except ValueError:
                    # string
                    if arguments[0] == arguments[2]:
                        continue
                    else:
                        if_yes_state = True
                        continue
        if command == "endif":
            if_state = False
            if_yes_state = False
            continue
        if command == "loop":
            loop_state = True
            loop_time = arguments[0]
            continue
        if command == "endloop":
            loop_state = False
            i = 0
            while i < int(loop_time):
                for loop_line in loop_code:
                    command = loop_line.split(",")[0]
                    arguments = loop_line.split(",")[1:len(loop_line)]
                    commands(command,arguments)
                i+=1
            loop_time = 0
            continue

        if if_yes_state:
            continue

        if loop_state:
            loop_code.append(line)
        else:
            commands(command,arguments)            
    except Exception as e:
        print("Error while interpreting code: " + format(e))

time.sleep(10)
