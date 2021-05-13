"""
Speaker:
    1. first name (string)
    2. last name (string)
    3. presentation topic (string)
    4. presentation description (string)

SingleSurvey:
    1. related speaker (Speaker)
    2. rate (SpeakerFeatures)
    3. comment (string)

SpeakerFeatures:
    1. concentration on topic (int)
    2. speed of speaking (int)
    3. Connection with Audience (int)
    4. punctuality (int)
    5. sufficient knowledge (int)

"""
class Student:
    def __init__(self):
        self.username = None
    
class Speaker:
    def __init__(self, name, lastName, firstName):
        self.lastName = lastName
        self.firstName = firstName
        self.topic = ""
        self.presentationDescription = ""

    def setTopic(self, topic):
        self.topic = topic

    def setPresentationDescription(self, presentationDescription):
        self.presentationDescription = presentationDescription

class SingleSurvey:
    def __init__(self, owner):
        self.owner = owner
        self.comment = ""
        self.rating = None

    def setComment(self, comment):
        self.comment = comment

    def setRating(self, rating):
        self.rating = rating


class SpeakerFeatures:
    def __init__(self):
        self.concentrationOnTopic = 0
        self.speedOfSpeaking = 0
        self.ConnectionWithAudience = 0
        self.punctuality = 0
        self.sufficientKnowledge = 0

    def setRating(self, concentrationOnTopic, speedOfSpeaking, ConnectionWithAudience, punctuality,
                  sufficientKnowledge):
        self.concentrationOnTopic = concentrationOnTopic
        self.speedOfSpeaking = speedOfSpeaking
        self.ConnectionWithAudience = ConnectionWithAudience
        self.punctuality = punctuality
        self.sufficientKnowledge = sufficientKnowledge