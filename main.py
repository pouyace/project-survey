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
        password = input(INPUT_LOGIN_PASSWORD)
        if QUITSTATEMENT in username or QUITSTATEMENT in password:
            break
        if not(len(username) and len(password)):
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
    pass

def userMainPage():
    pass

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
