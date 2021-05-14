"""
Survey Project

"""
from classes import *
from configs import *
import json

frontUser = None


def mainFunction():
    print("Please login in project(enter 'quit' to exit the application")
    global frontUser
    with open(FILEHANDLER_FILENAME, 'r') as jsonReader:
        data = json.load(jsonReader)

    while True:
        username = input(INPUT_LOGIN_USERNAME)
        if INPUT_GLOBAL_QUITSTATEMENT in username:
            break
        password = input(INPUT_LOGIN_PASSWORD)
        if INPUT_GLOBAL_QUITSTATEMENT in password:
            break
        if not (len(username) and len(password)):
            print(ERROR_LOGIN_EMPTYINPUT)
            continue
        elif FILEHANDLER_SPACE in username or FILEHANDLER_SPACE in password:
            print(ERROR_LOGIN_SPACEINPUT)
            continue
        else:
            notFound = 1
            for p in data[FILEHANDLER_USER]:
                if p[FILEHANDLER_USERNAME] == username:
                    notFound = 0
                    if p[FILEHANDLER_PASSWORD] == password:
                        if username == ADMINUSERNAME:
                            frontUser = Professor(FILEHANDLER_USERNAME, p[FILEHANDLER_NAME])
                            adminMainPage()
                        else:
                            frontUser = Student(FILEHANDLER_USERNAME, p[FILEHANDLER_NAME])
                            userMainPage()
                        break
                    else:
                        print(ERROR_LOGIN_WRONGPASSWORD)
                        break
            if notFound:
                print(ERROR_LOGIN_USERNAMENOTFOUND)


def greeting():
    print("*******************  Welcome to Project  *******************\n\n")


def adminMainPage():
    CLEARSCREEN()
    switcher = {
        ADMIN_INSTRUCTION_SPEAKERS: admin_speaker,
        ADMIN_INSTRUCTION_SURVEY: admin_surveys,
        ADMIN_INSTRUCTION_LOGOUT: logout
    }
    while True:
        instruction = input("select an operation(enter {} to logout): {} {} {} "
                            "            ".format(ADMIN_INSTRUCTION_LOGOUT,
                                                  ADMIN_INSTRUCTION_SPEAKERS,
                                                  ADMIN_INSTRUCTION_SURVEY,
                                                  ADMIN_INSTRUCTION_LOGOUT))
        func = switcher.get(instruction, invalidInstruction)
        if instruction == ADMIN_INSTRUCTION_LOGOUT:
            break
        func()


def admin_speaker():
    CLEARSCREEN()
    data = openFile()

    if not len(data[FILEHANDLER_SPEAKER]):
        # no speaker to show
        print(ERROR_ADMINPAGE_NOSPEAKER)
    else:
        # have some speakers to print
        counter = 1
        commands = list((ADMIN_INSTRUCTION_SPEAKERS_ADD, ADMIN_INSTRUCTION_SPEAKERS_EDIT,
                         ADMIN_INSTRUCTION_SPEAKERS_REMOVE))
        commandsStringOut = '   '.join(commands)
        print(INPUT_GLOBAL_LINE + ' Speaker ' + INPUT_GLOBAL_LINE)
        print("number \t\t{}\t{}\t\t{}".format(INPUT_ADMINPAGE_SPEAKER_NAME,
                                               INPUT_ADMINPAGE_SPEAKER_TOPIC, INPUT_ADMINPAGE_SPEAKER_DESCRIPTION))
        for p in data[FILEHANDLER_SPEAKER]:
            print("{}.\t\t{}\t{}\t\t{}".format(counter, p[FILEHANDLER_NAME],
                                               p[FILEHANDLER_TOPIC], p[FILEHANDLER_DESCRIPTION]))
        print("\n")
        print(INPUT_GLOBAL_LINE + '   END   ' + INPUT_GLOBAL_LINE)
        while True:
            inputString = "Enter command ({} to exit)   ".format(INPUT_GLOBAL_QUITSTATEMENT) + commandsStringOut + ': '
            inputCommands = input(inputString).strip()
            if INPUT_GLOBAL_QUITSTATEMENT == inputCommands:
                break
            switcher = {
                ADMIN_INSTRUCTION_SPEAKERS_ADD: admin_speaker_add,
                ADMIN_INSTRUCTION_SPEAKERS_EDIT: admin_speaker_edit,
                ADMIN_INSTRUCTION_SPEAKERS_REMOVE: admin_speaker_remove
            }
            func = switcher.get(inputCommands, invalidInstruction)
            func()


def admin_speaker_add():
    print("in add")


def admin_speaker_edit():
    print("in edit")


def admin_speaker_remove():
    print("in remove")


def openFile():
    with open(FILEHANDLER_FILENAME, 'r') as jsonReader:
        data = json.load(jsonReader)
    return data


def admin_surveys():
    pass


def userMainPage():
    pass


def logout():
    print("----------------------- User logged out -----------------------")
    del frontUser


def invalidInstruction():
    print(ERROR_ADMINPAGE_UNKNOWNCOMMAND)


def userWriter():
    """
    data = {'users': []}
    data['users'].append({
        'name': 'Pouya',
        'username': 'pouya',
        'password': 'pouya'
    })
    data['users'].append({
        'name': 'admin',
        'username': 'admin',
        'password': 'admin'
    })
    data['users'].append({
        'name': 'test',
        'username': 'test',
        'password': 'test'
    })

    with open('users.txt', 'w') as outfile:
        json.dump(data, outfile)
"""


if __name__ == "__main__":
    greeting()
    mainFunction()
