"""
Survey Project

"""
from classes import *
from configs import *
import matplotlib.pyplot as plt
import pandas as pd
import json

frontUser = None
usersContainer = None


# Done
def mainFunction():
    global usersContainer
    global frontUser

    usersContainer = openFile()

    while True:
        CLEARSCREEN()
        print("Please login in project(enter '{}' to exit the application".format(INPUT_GLOBAL_QUITSTATEMENT))
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
            for p in usersContainer[FILEHANDLER_USER]:
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
                        WAITFORENTER()
                        break
            if notFound:
                print(ERROR_LOGIN_USERNAMENOTFOUND)
                WAITFORENTER()


# Done
def greeting():
    print("*******************  Welcome to Project  *******************\n\n")


# Done
def adminMainPage():
    switcher = {
        ADMIN_INSTRUCTION_SPEAKERS: admin_speaker,
        ADMIN_INSTRUCTION_SURVEY: admin_surveys,
        ADMIN_INSTRUCTION_LOGOUT: logout,
        ADMIN_INSTRUCTION_VIEWALL: admin_viewAll
    }
    while True:
        CLEARSCREEN()
        instruction = input("select an operation(enter {} to logout): {} {} {} {}"
                            "            ".format(ADMIN_INSTRUCTION_LOGOUT,
                                                  ADMIN_INSTRUCTION_SPEAKERS,
                                                  ADMIN_INSTRUCTION_SURVEY,
                                                  ADMIN_INSTRUCTION_LOGOUT,
                                                  ADMIN_INSTRUCTION_VIEWALL))
        func = switcher.get(instruction, invalidInstruction)
        if instruction == ADMIN_INSTRUCTION_LOGOUT:
            logout()
            break
        func()


# Done
def admin_speaker():
    global usersContainer
    commands = list((ADMIN_INSTRUCTION_SPEAKERS_ADD, ADMIN_INSTRUCTION_SPEAKERS_EDIT,
                     ADMIN_INSTRUCTION_SPEAKERS_REMOVE))
    commandsStringOut = '   '.join(commands)
    switcher = {
        ADMIN_INSTRUCTION_SPEAKERS_ADD: admin_speaker_add,
        ADMIN_INSTRUCTION_SPEAKERS_EDIT: admin_speaker_edit,
        ADMIN_INSTRUCTION_SPEAKERS_REMOVE: admin_speaker_remove
    }
    while True:
        CLEARSCREEN()
        if not len(usersContainer[FILEHANDLER_SPEAKER]):
            # no speaker to show
            print(ERROR_ADMINPAGE_NOSPEAKER)
        # have some speakers to print
        else:
            showSpeakers()
        inputString = "Enter command ({} to exit)   ".format(INPUT_GLOBAL_QUITSTATEMENT) + commandsStringOut + ': '
        inputCommands = input(inputString).strip()
        if INPUT_GLOBAL_QUITSTATEMENT == inputCommands:
            break
        func = switcher.get(inputCommands, invalidInstruction)
        func()


# Done
def admin_speaker_add():
    CLEARSCREEN()
    global usersContainer
    print("Fill-in the information(enter {} to return)".format(INPUT_GLOBAL_QUITSTATEMENT))

    while True:
        newSpeakerName = input("Enter speaker name:")
        if INPUT_GLOBAL_QUITSTATEMENT in newSpeakerName:
            return
        if not len(newSpeakerName.strip()):
            print(ERROR_LOGIN_EMPTYINPUT)
            continue
        break
    while True:
        newSpeakerTopic = input("Enter presentation topic:")
        if INPUT_GLOBAL_QUITSTATEMENT in newSpeakerTopic:
            return
        if not len(newSpeakerTopic.strip()):
            print(ERROR_LOGIN_EMPTYINPUT)
            continue
        break
    newSpeakerDescription = input("Enter presentation Description(optional):")
    newSpeaker = Speaker(newSpeakerName)
    newSpeaker.setTopic(newSpeakerTopic)
    newSpeaker.setPresentationDescription(newSpeakerDescription)
    usersContainer[FILEHANDLER_SURVEY].append(
        {
            FILEHANDLER_SURVEY_OWNER: newSpeakerName,
            FILEHANDLER_SURVEY_SINGLESURVEY: []
        }
    )
    userWriter(FILEHANDLER_SPEAKER, newSpeaker)
    print(OUTPUT_SPEAKER_ADDITION_SUCCEED)
    WAITFORENTER()


# Not Done
def admin_speaker_edit():
    # need to verity the input
    # CLEARSCREEN()
    global usersContainer
    while True:
        speakerName = input("Enter speaker name(enter {} to return):".format(INPUT_GLOBAL_QUITSTATEMENT))
        if INPUT_GLOBAL_QUITSTATEMENT in speakerName:
            return
        for i in usersContainer[FILEHANDLER_SPEAKER]:
            if i[FILEHANDLER_NAME] == speakerName:
                newName = input("Enter new name:(Hit Enter for no change)")
                newTopic = input("Enter new topic:(Hit Enter for no change)")
                newDescription = input("Enter new description:(Hit Enter for no change)")
                newStatus = input("Do you want to toggle the status?"
                                  "(current status = '{}') y/n".format(i[FILEHANDLER_SPEAKER_STATUS]))
                if len(newName):
                    i[FILEHANDLER_NAME] = newName
                if len(newTopic):
                    i[FILEHANDLER_TOPIC] = newTopic
                if len(newDescription):
                    i[FILEHANDLER_DESCRIPTION] = newDescription
                if newStatus == "y":
                    if i[FILEHANDLER_SPEAKER_STATUS] == FILEHANDLER_SPEAKER_STATUS_ACTIVE:
                        i[FILEHANDLER_SPEAKER_STATUS] = FILEHANDLER_SPEAKER_STATUS_PASSIVE
                    else:
                        i[FILEHANDLER_SPEAKER_STATUS] = FILEHANDLER_SPEAKER_STATUS_ACTIVE
                updateFile()
                print(OUTPUT_SPEAKER_EDITION_SUCCEED)
                WAITFORENTER()
                return
        else:
            print(ERROR_LOGIN_USERNAMENOTFOUND)


# Done
def admin_speaker_remove():
    global usersContainer

    while True:
        speakerName = input("Enter speaker name(enter {} to return):".format(INPUT_GLOBAL_QUITSTATEMENT))
        if INPUT_GLOBAL_QUITSTATEMENT in speakerName:
            return
        if not len(speakerName.strip()):
            print(ERROR_LOGIN_EMPTYINPUT)
            continue
        else:
            isDone = userRemover(FILEHANDLER_SPEAKER, speakerName)
            print(OUTPUT_SPEAKER_DELETION_SUCCEED) if isDone else print(ERROR_LOGIN_USERNAMENOTFOUND)
            WAITFORENTER()
            return


# Done
def showSpeakers():
    counter = 1
    CLEARSCREEN()
    print(INPUT_GLOBAL_LINE + ' Speaker ' + INPUT_GLOBAL_LINE)
    print("number \t\t{}\t\t{}\t\t{}\t\t{}".format(INPUT_ADMINPAGE_SPEAKER_NAME,
                                                   INPUT_ADMINPAGE_SPEAKER_TOPIC,
                                                   INPUT_ADMINPAGE_SPEAKER_DESCRIPTION,
                                                   INPUT_ADMINPAGE_SPEAKER_STATUS))
    for p in usersContainer[FILEHANDLER_SPEAKER]:
        print("{}.\t\t{}\t\t{}\t\t{}\t\t{}".format(counter, p[FILEHANDLER_NAME],
                                                   p[FILEHANDLER_TOPIC], p[FILEHANDLER_DESCRIPTION],
                                                   p[FILEHANDLER_SPEAKER_STATUS]))
        counter += 1
    print("")
    print(INPUT_GLOBAL_LINE + '   END   ' + INPUT_GLOBAL_LINE)


def openFile():
    with open(FILEHANDLER_FILENAME, 'r') as jsonReader:
        data = json.load(jsonReader)
    return data


def admin_surveys():
    global usersContainer
    CLEARSCREEN()
    activeSpeakers = getActiveSpeakersCount()
    if len(activeSpeakers) == 0:
        print("No active speaker")
        WAITFORENTER()
        return
    print(INPUT_GLOBAL_LINE)
    print("active speakers:")
    for i, counter in zip(activeSpeakers, range(len(activeSpeakers))):
        print("    {}. {}".format(counter + 1, i))
    print(INPUT_GLOBAL_LINE)
    while True:
        speakerName = input("enter speaker name to view the result(Enter quit to return):  ")
        if INPUT_GLOBAL_QUITSTATEMENT in speakerName:
            return
        if speakerName not in activeSpeakers:
            print("speaker not found")
        else:
            break
    showSurveyResult(speakerName)


def showSurveyResult(speakerName):
    speakerSurvey = next((item for item in usersContainer[FILEHANDLER_SURVEY]
                          if item[FILEHANDLER_SURVEY_OWNER] == speakerName))
    # labels = list(item[FILEHANDLER_SURVEY_SINGLESURVEY_participant] for item in speakerSurvey[FILEHANDLER_SURVEY_SINGLESURVEY])
    labels = "student"
    mainData = [[int(li) for li in item[FILEHANDLER_SURVEY_SINGLESURVEY_RATING]] for item in
                speakerSurvey[FILEHANDLER_SURVEY_SINGLESURVEY]]
    if len(mainData) == 0:
        print("no score yet")
        WAITFORENTER()
        return
    for i, counter in zip(mainData, range(len(labels))):
        i.insert(0, labels)
    print(mainData)
    avgScores = []
    for i in range(5):
        avg = 0
        for j in mainData:
            avg += j[i + 1]
        avgScores.append(avg / len(mainData))
    print("average concentration on topic:", avgScores[0])
    print("average speaking speed:", avgScores[1])
    print("average connection with audience:", avgScores[2])
    print("average punctuality:", avgScores[3])
    print("average knowledge:", avgScores[4])
    print("Comments:")

    for item in speakerSurvey[FILEHANDLER_SURVEY_SINGLESURVEY]:
        print(item[FILEHANDLER_SURVEY_SINGLESURVEY_COMMENT])
    print(mainData)
    df = pd.DataFrame(mainData, columns=['Students', 'concentration on topic', 'speaking speed',
                                         'connection with audience', 'punctuality', 'knowledge'])

    df.plot(x='Students',
            kind='bar',
            stacked=False,
            title='Grouped Bar Graph with dataframe')
    plt.show()
    WAITFORENTER()


def admin_viewAll():
    CLEARSCREEN()
    survey = usersContainer[FILEHANDLER_SURVEY]
    if len(survey) == 0:
        print("no active speaker")
        WAITFORENTER()
        return
    speakersScores = []
    for curSpeaker in survey:
        mainData = [[int(li) for li in item[FILEHANDLER_SURVEY_SINGLESURVEY_RATING]] for item in
                    curSpeaker[FILEHANDLER_SURVEY_SINGLESURVEY]]
        print("----speaker '" + curSpeaker[FILEHANDLER_SURVEY_OWNER] + "':")
        if len(mainData) == 0:
            continue
        avgScores = []
        for i in range(5):
            avg = 0
            for j in mainData:
                avg += j[i]
            avgScores.append(avg / len(mainData))
        speakersScores.append(avgScores)
        speakersScores[-1].insert(0, curSpeaker[FILEHANDLER_SURVEY_OWNER])
        print("average concentration on topic:", avgScores[1])
        print("average speaking speed:", avgScores[2])
        print("average connection with audience:", avgScores[3])
        print("average punctuality:", avgScores[4])
        print("average knowledge:", avgScores[5])
        print("Comments:")
        for item in curSpeaker[FILEHANDLER_SURVEY_SINGLESURVEY]:
            print(item[FILEHANDLER_SURVEY_SINGLESURVEY_COMMENT])

    print("*******************************")
    print(speakersScores)
    if len(speakersScores) == 0:
        print("No data to show")
        WAITFORENTER()
        return
    print("*******************************")

    df = pd.DataFrame(speakersScores, columns=['SPEAKERS', 'concentration on topic', 'speaking speed',
                                               'connection with audience', 'punctuality', 'knowledge'])

    df.plot(x='SPEAKERS',
            kind='bar',
            stacked=False,
            title='Grouped Bar Graph with dataFrame')
    plt.show()


def userMainPage():
    switcher = {
        USER_INSTRUCTION_SURVEY: user_survey,
        USER_INSTRUCTION_LOGOUT: logout
    }
    while True:
        CLEARSCREEN()
        instruction = input("select an operation(enter {} to logout): {} {} "
                            "            ".format(USER_INSTRUCTION_LOGOUT,
                                                  USER_INSTRUCTION_SURVEY,
                                                  USER_INSTRUCTION_LOGOUT))
        func = switcher.get(instruction, invalidInstruction)
        if instruction == USER_INSTRUCTION_LOGOUT:
            logout()
            break
        func()


def user_survey():
    global frontUser
    CLEARSCREEN()
    activeSpeakersCount = getActiveSpeakersCount()
    if not len(activeSpeakersCount):
        print("No survey has been set")
        WAITFORENTER()
    else:
        availableSpeakers = set(getAvailableSpeakers(frontUser.username)).intersection(activeSpeakersCount)
        if not len(availableSpeakers):
            print("no active survey left")
            WAITFORENTER()
        else:
            print(INPUT_GLOBAL_LINE)
            print("there are {} survey(s) left to take-in: ".format(len(availableSpeakers)))
            for i, counter in zip(availableSpeakers, range(len(availableSpeakers))):
                print("    {}. survey for {}".format(counter + 1, i))
            print(INPUT_GLOBAL_LINE)
            while True:
                speakerName = input("Enter the speaker name for starting survey(Enter {} to return)"
                                    .format(INPUT_GLOBAL_QUITSTATEMENT))
                if INPUT_GLOBAL_QUITSTATEMENT in speakerName:
                    return
                elif speakerName not in availableSpeakers:
                    print("speaker not found")
                else:
                    user_survey_add(speakerName, frontUser.username)
                    break


def user_survey_add(owner, username):
    CLEARSCREEN()
    userSurveyForm = SingleSurvey(username)
    userSurveyForm.setRating(getSpeakerFeaturesFromUser())
    userSurveyForm.setComment(input("Enter any comment for this speaker(optional)"))
    status = surveyWriter(owner, userSurveyForm)
    if status:
        print(OUTPUT_ADDING_SURVEY_SUCCEED)
    else:
        print(ERROR_SURVEY_ADDITION_FAILED)
    WAITFORENTER()


def getSpeakerFeaturesFromUser():
    while True:
        speedOfSpeaking = input("score the speed of speaking(1-10): ")
        if not speedOfSpeaking.strip().isdigit():
            print("Enter a valid number from 1 to 10")
        else:
            break
    while True:
        concentrationOnTopic = input("score the concentration of topic(1-10): ")
        if not concentrationOnTopic.strip().isdigit():
            print("Enter a valid number from 1 to 10")
        else:
            break
    while True:
        punctuality = input("score the speaker punctuality(1-10): ")
        if not punctuality.strip().isdigit():
            print("Enter a valid number from 1 to 10")
        else:
            break
    while True:
        sufficientKnowledge = input("score the speaker Knowledge(1-10): ")
        if not sufficientKnowledge.strip().isdigit():
            print("Enter a valid number from 1 to 10")
        else:
            break
    while True:
        connectionWithAudience = input("score the speaker connection with audience(1-10): ")
        if not connectionWithAudience.strip().isdigit():
            print("Enter a valid number from 1 to 10")
        else:
            break

    rating = SpeakerFeatures()
    rating.setRating(concentrationOnTopic, speedOfSpeaking, connectionWithAudience, punctuality, sufficientKnowledge)
    return rating


def getActiveSpeakersCount():
    global usersContainer
    allowedSpeakers = []
    for i in usersContainer[FILEHANDLER_SPEAKER]:
        if i[FILEHANDLER_SPEAKER_STATUS] == FILEHANDLER_SPEAKER_STATUS_ACTIVE:
            allowedSpeakers.append(i[FILEHANDLER_NAME])
    return allowedSpeakers


def getAvailableSpeakers(username):
    availableSpeakersName = []
    for i in usersContainer[FILEHANDLER_SURVEY]:
        participants = getSurveyParticipants(i[FILEHANDLER_SURVEY_OWNER])
        if username not in participants:
            availableSpeakersName.append(i[FILEHANDLER_SURVEY_OWNER])
    return availableSpeakersName


def getSurveyParticipants(owner):
    global usersContainer
    participants = []
    for i in usersContainer[FILEHANDLER_SURVEY]:
        if i[FILEHANDLER_SURVEY_OWNER] == owner:
            for j in i[FILEHANDLER_SURVEY_SINGLESURVEY]:
                participants.append(j[FILEHANDLER_SURVEY_SINGLESURVEY_participant])
    return participants


def logout():
    global frontUser
    print("----------------------- User logged out -----------------------")
    del frontUser


def invalidInstruction():
    print(ERROR_UNKNOWNCOMMAND)


def userWriter(userType, user):
    global usersContainer
    if userType == FILEHANDLER_SPEAKER:
        usersContainer[userType].append({
            FILEHANDLER_NAME: user.name,
            FILEHANDLER_TOPIC: user.topic,
            FILEHANDLER_DESCRIPTION: user.presentationDescription,
            FILEHANDLER_SPEAKER_STATUS: user.status
        })
    updateFile()


def userRemover(userType, username):
    global usersContainer
    if userType == FILEHANDLER_SPEAKER:
        for i in usersContainer[userType]:
            if i[FILEHANDLER_NAME] == username:
                usersContainer[userType].remove(i)
                updateFile()
                return True
        else:
            return False


def surveyWriter(owner, result):
    for i in usersContainer[FILEHANDLER_SURVEY]:
        if i[FILEHANDLER_SURVEY_OWNER] == owner:
            print(i[FILEHANDLER_SURVEY_SINGLESURVEY])
            i[FILEHANDLER_SURVEY_SINGLESURVEY].append(
                {
                    FILEHANDLER_SURVEY_SINGLESURVEY_participant: result.participant,
                    FILEHANDLER_SURVEY_SINGLESURVEY_COMMENT: result.comment,
                    FILEHANDLER_SURVEY_SINGLESURVEY_RATING: result.rating.getRating()
                }
            )
            updateFile()
            return True
    else:
        return False


def updateFile():
    global usersContainer
    try:
        with open(FILEHANDLER_FILENAME, 'w') as jsonWriter:
            jsonWriter.truncate(0)
            jsonWriter.write(json.dumps(usersContainer))
    except FileNotFoundError as exp:
        print(exp)


if __name__ == "__main__":
    greeting()
    mainFunction()
