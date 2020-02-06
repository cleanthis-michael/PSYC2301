###################################################################################################
###################################################################################################
###################################################################################################
################################           Coursework 2             ###############################
################################      Candidate Number: SKGR8       ###############################
###################################################################################################
###################################################################################################
###################################################################################################

#### This file contains utility functions used in Experiment.py ####

# Define a function which, when given a list of all the participants' data so far,
# will convert the list of strings into a list of sublists,
# each sublist containing one participant's data
def convertListFormat(listOfData):

    for i in range(len(listOfData)):
        newData = listOfData[i].split(',')  # each string within each entry will be split into a list containing that data
        listOfData[i] = newData  # replace the string at index i with the new list (newData)

    return listOfData


# Participants will be randomly allocated to one of the experimental conditions (2, 10 or 100 marbles per urn)
# However, each participant's condition will depend on the previous participant's condition,
# such that each condition has the same number of participants
##   (a) If the last participant completed the 2-marble condition, the next one will complete the 10-marble condition
##   (b) If the last participant completed the 10-marble condition, the next one will complete the 100-marble condition
##   (c) If the last participant completed the 100-marble condition, the next one will complete the 2-marble condition
# Indices: last participant's (index -1) condition (index 3)
def deriveParticipantCondition(participantResults):

    previousParticipantCondition = int(participantResults[-1][3])
    if previousParticipantCondition == 2: participantCondition = 10
    elif previousParticipantCondition == 10: participantCondition = 100
    else: participantCondition = 2

    return participantCondition