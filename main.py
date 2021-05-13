"""
Survey Project

"""
import classes
import json




def mainFunction():
    print("Please login in project(enter 'quit' to exit the application")
    data = []
    with open("users.txt", 'r') as jsonReader:
        data = json.load(jsonReader)

    while True:
        username = input("enter username:")
        password = input("enter password:")
        if 'quit' in username or 'quit' in password:
            break
        if not(len(username) and len(password)):
            print("empty input not allowed")
            continue
        elif ' ' in username or ' ' in password:
            print("spaces not allowed in inputs")
            continue
        else:
            notFound = 1
            for p in data['users']:
                if p['username'] == username:
                    notFound = 0
                    if p['password'] == password:
                        print("yes")
                        break
                    #     HERE
                    else:
                        print("Wrong Password")
                        break
            if notFound:
                print("Unregistered username")



def greeting():
    print("*******************  Welcome to Project  *******************\n\n")


def adminMainPage():
    pass

def userMainPage():
    pass

def userWriter():
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



if __name__ == "__main__":

    greeting()
    mainFunction()
