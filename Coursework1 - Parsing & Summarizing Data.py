###################################################################################################
###################################################################################################
###################################################################################################
################################           Coursework 1             ###############################
################################      Candidate Number: SKGR8       ###############################
###################################################################################################
###################################################################################################
################################              Part A                ###############################
#######################   Creating a CSV File with each Participant's Data    #####################
###################################################################################################
###################################################################################################
###################################################################################################


####  Defining Functions  ####


# Define a function that, given each participant's file, will parse each participant's data to convert the file into a more convenient format
# This format will constitute a list of lists, each list containing one participant's data
# Within each list, each entry from index 3 onward contains multiple items
# Therefore, each entry from index 3 onward will be converted into a sublist to conveniently access each entry's items
# The entries before index 3 only have 1 value, so there is no need to convert them into lists

def parseParticipantData(participantFile):
    openParticipantData = open('results/' + participantFile,'r')
    participantData = openParticipantData.readlines()  # store each participant's data in a list of strings

    # Entries from index 3 onward have one string containing multiple types of information (e.g. the entry at index 3 has one string for name, age and gender)
    # Convert participantData from index 3 onward into a list of strings to access each list's different items conveniently
    for i in range(len(participantData)):
        editedData = participantData[i].strip('\n')  # remove '\n' from each string
        if i < 3:  # entries with index < 3 have only 1 entry, hence they are easily accessible without converting them into a list
            participantData[i] = editedData  # replace the entry containing '\n' with the entry not containing '\n'
        else:
            listedData = editedData.split(',')  # split each string within each entry into a list containing that same data to be more easily accessible
            participantData[i] = listedData  # replace the string in index i of participantData with the new list (listedData)

    return participantData


# Define a function that, given a participant's data, will access the participant's gender and convert it into codes
# participantData will be derived from the above function (parseParticipantData), so the gender will be found in the list in index 3 in its 2nd index
# Code 1 will represent males, and code 2 will represent females

def convertGender(participantData):
    gender = participantData[3][2]

    if gender.lower() == 'male':  # gender.lower() to check gender, irrespective of how the participant wrote it e.g. male, Male, MALE
        genderCode = 1  # males coded as 1
    else:
        genderCode = 2  # females coded as 2

    return genderCode


# Define a function that, given a participant's data, will store the participant's experimental trials in a list
# This list will not include the participant's other information, like name and age, or additional comments found at the end of some participants' file
# This will make the subsequent analysis of their outcomes (hits, near misses, full misses), happiness and willingness to continue more convenient

def isolateParticipantTrials(participantData):
    participantTrials = []  # will contain only the participant's experimental trials
    for trial in participantData[5:]:  # each participant's experimental trials start from index 5 onward
        if 'trial' in trial:  # each trial starts with the word 'trial', so this will access each participant's trials, but not any other entries (like comments) at the end of some participants' file
            participantTrials.append(trial)
    return participantTrials


# Define a function that derives a string containing the trial(s) with the maximum/minimum happiness level (e.g. '9 | 14')
# participantTrials contains a list, which only contains the participant's experimental trials
# The parameter 'maxOrMinHappiness' determines whether the function will derive:
    # The trial(s) with the maximum happiness, if maxOrMinHappiness == 'maximumHappiness'
    # The trial(s) with the minimum happiness, if maxOrMinHappiness == 'minimumHappiness'

def deriveTrialsForMaxOrMinHappiness(participantTrials,happinessIndex,maxOrMinHappiness,maximumHappiness,minimumHappiness):
    trialsMaximumHappinessList = []  # will contain all the trials with the maximum happiness level
    trialsMinimumHappinessList = []  # will contain all the trials with the minimum happiness level
    trialNumber = 1  # index 0 represents trial 1
    # The trial numbers will be appended as a string rather than an integer, to be able to 'join' them together in a single variable that will be written in the csv file

    for trial in participantTrials:  # each loop accesses one trial for that participant
        # If the value of maxOrMinHappiness is 'maximumHappiness', only the computations for the maximumHappiness will be executed
        if maxOrMinHappiness == 'maximumHappiness':
            if int(trial[happinessIndex]) == maximumHappiness:
                # Append each trial number being rated with the participant's maximum happiness level to the 'maximum' list as a string
                trialsMaximumHappinessList.append(str(trialNumber))

        # If the value of maxOrMinHappiness is 'minimumHappiness', only the computations for the minimumHappiness will be executed
        elif maxOrMinHappiness == 'minimumHappiness':
            if int(trial[happinessIndex]) == minimumHappiness:
                # Append each trial number being rated with the participant's minimum happiness level to the 'minimum' list as a string
                trialsMinimumHappinessList.append(str(trialNumber))

        trialNumber += 1

    # Create 2 variables, each containing a single string with the trials rated with either the maximum or minimum happiness
    if maxOrMinHappiness == 'maximumHappiness':
        trialsMaximumHappiness = ' | '.join(trialsMaximumHappinessList)  # this will join all trials with ' | ' between them (e.g. '9 | 14'), whereas if the list only contains one trial, the variable will simply contain the single trial number (e.g. '9')
        return trialsMaximumHappiness
    elif maxOrMinHappiness == 'minimumHappiness':
        trialsMinimumHappiness = ' | '.join(trialsMinimumHappinessList)
        return trialsMinimumHappiness


# Define a function that will write each participant's analyzed results into the csv file summarizing each participant's results
# participantResults contains a list with each participant's required data

def writeResultsInCSV(participantResults,participantCSV):
    for item in participantResults:  # access each item in each participant's list of results to write it in the csv file
        if participantResults.index(item) == 0:
            # The first item represents a new participant, so the results must be written in a new line of the csv file, hence add '\n'
            participantCSV.write('\n{0}'.format(item))
        else:
            # All the other items in the list belong to the same participant, hence add ',' before each entry
            participantCSV.write(',{0}'.format(item))
    return participantCSV


###################################################################################################
###################################################################################################
###################################################################################################


####  Creating the CSV file  ####


from os import listdir
allParticipantData = listdir('results')  # read the directory containing each participant's data, which is at the same location with the python file

listOfIPAddresses = []  # new IP addresses will be stored, to discard participants who participated multiple times (hence had the same IP address)
participantCSV = open('Participant Results.csv','w')  # create the csv file that will summarize each participant's data (1 row per participant) at the location where the python file is saved

# Create a string that will be written in the first line of the csv file, describing what each column will represent
columnLabels = 'Condition,Name,Age,Gender (1 = male/2 = female),Proportion of Hits,Proportion of Near Misses,Proportion of Full Misses,Mean Happiness for Hits,Mean Happiness for Near Misses,Mean Happiness for Full Misses,Mean Willingness to Continue for Hits,Mean Willingness to Continue for Near Misses,Mean Willingness to Continue for Full Misses,Maximum Happiness Level,Trial(s) with Maximum Happiness Level,Minimum Happiness Level,Trial(s) with Minimum Happiness Level'
participantCSV.write(columnLabels)


for eachParticipantFile in allParticipantData:  # create a loop, accessing each participant's file per loop
    # Read each participant's file and parse it to get the file to a convenient format
    participantData = parseParticipantData(eachParticipantFile)

    # Find each participant's IP address and append each unique IP address in listOfIPAddresses
    IPAddress = participantData[2]

    # Participants who completed the experiment more than once have the same IP Address in their file
    # Therefore, if the same IP address is found, only the participant's first participation will be considered
    if IPAddress not in listOfIPAddresses:
        listOfIPAddresses.append(IPAddress)


        # Derive each participant's condition (skill, luck or mixed) and demographic information
        # The demographic information is found in the sublist in index 3
        condition = participantData[0].strip('  ')
        name = participantData[3][0].capitalize()  # make the first letter of the name capital
        age = participantData[3][1]
        genderCode = convertGender(participantData)


        # Creating a new list only containing each participant's trials
        # This list does not include any additional comments found at the end of some participants' files
        # This will make the analysis of the results, happiness and willingness to continue more convenient
        participantTrials = isolateParticipantTrials(participantData)


        # Finding the indices for the result, happiness and willingness to continue
        # The labels in participantData are found in the sublist in index 4
        # The entries in each trial at these indices represent the result/happiness/willingness to continue for each trial
        # Therefore, they will be used to find each participant's result, happiness and willingness to continue in each trial
        resultIndex = participantData[4].index('Result')
        happinessIndex = participantData[4].index('Happinness')
        willingnessIndex = participantData[4].index('WantsMore')


        # Setting up variables to calculate the number of hits, nearMisses and fullMisses
        hits = 0
        nearMisses = 0
        fullMisses = 0

        # Setting up variables to calculate total happiness and willingness to continue for each outcome
        # These totals will later be used to calculate proportions for each outcome
        hitsTotalHappiness = 0
        nearMissesTotalHappiness = 0
        fullMissesTotalHappiness = 0

        hitsTotalWillingness = 0
        nearMissesTotalWillingness = 0
        fullMissesTotalWillingness = 0

        # Setting up a list, which will contain all happiness values
        # This list will later be used to calculate minimum and maximum happiness levels, and subsequently the trial(s) in which they occurred
        allHappinessLevels = []


        for trial in participantTrials:  # access each trial per loop
            happinessValue = int(trial[happinessIndex])  # convert from string to integer to be able to add this value to calculate the total happiness
            allHappinessLevels.append(happinessValue)
            willingnessValue = int(trial[willingnessIndex])  # convert from string to integer to be able to add this value to calculate the total willingness to continue

            if trial[resultIndex] == 'hit':
                hits += 1
                hitsTotalHappiness += happinessValue  # add each happiness value to calculate the total
                hitsTotalWillingness += willingnessValue  # add each willingness to continue value to calculate the total
            elif trial[resultIndex] == 'nearMiss':
                nearMisses += 1
                nearMissesTotalHappiness += happinessValue
                nearMissesTotalWillingness += willingnessValue
            else:
                fullMisses += 1
                fullMissesTotalHappiness += happinessValue
                fullMissesTotalWillingness += willingnessValue


        # Calculating proportions of hits, nearMisses and fullMisses
        participantTotalTrials = len(participantTrials)

        hitsProportion = hits / participantTotalTrials
        nearMissesProportion = nearMisses / participantTotalTrials
        fullMissesProportion = fullMisses / participantTotalTrials


        # Calculating the mean happiness and willingness to continue for each outcome
        hitsMeanHappiness = hitsTotalHappiness / hits
        hitsMeanWillingness = hitsTotalWillingness / hits
        nearMissesMeanHappiness = nearMissesTotalHappiness / nearMisses
        nearMissesMeanWillingness = nearMissesTotalWillingness / nearMisses
        fullMissesMeanHappiness = fullMissesTotalHappiness / fullMisses
        fullMissesMeanWillingness = fullMissesTotalWillingness / fullMisses


        # Calculating minimum and maximum happiness levels, and the trials in which they occurred
        minimumHappiness = min(allHappinessLevels)
        maximumHappiness = max(allHappinessLevels)

        trialsMaximumHappiness = deriveTrialsForMaxOrMinHappiness(participantTrials,happinessIndex,'maximumHappiness',maximumHappiness,minimumHappiness)
        trialsMinimumHappiness = deriveTrialsForMaxOrMinHappiness(participantTrials,happinessIndex,'minimumHappiness',maximumHappiness,minimumHappiness)


        # Summarize each participant's results in a list, which is then used by the function 'writeResultsInCSV' to write each participant's results in a new line in the csv file
        participantResults = [condition,name,age,genderCode,hitsProportion,nearMissesProportion,fullMissesProportion,hitsMeanHappiness,nearMissesMeanHappiness,fullMissesMeanHappiness,hitsMeanWillingness,nearMissesMeanWillingness,fullMissesMeanWillingness,maximumHappiness,trialsMaximumHappiness,minimumHappiness,trialsMinimumHappiness]
        participantCSV = writeResultsInCSV(participantResults,participantCSV)

participantCSV.close()



###################################################################################################
###################################################################################################
###################################################################################################
################################              Part B                ###############################
################################   Creating a Summary Text File     ###############################
###################################################################################################
###################################################################################################
###################################################################################################


####  Defining Functions  ####


# Define a function that, given the participant's file, derives the date that the participant completed the experiment

def deriveDate(participantFile):
    # Create a new list, which will contain each file name's digits and ignore its alphabetic characters
    participantDigits = []

    for character in participantFile:  # access each character in the participant's file per loop
        if character.isdigit():  # access only the digits, which represent the date and time
            participantDigits.append(character)  # these are added in the list participantDigits

    # The first 8 digits will represent the date that the experiment was completed: DDMMYYYY
    # The remaining digits will represent the time that the experiment was completed, which is not required

    participantDay = ''.join(participantDigits[0:2])
    participantMonth = ''.join(participantDigits[2:4])
    participantYear = ''.join(participantDigits[4:8])

    participantDate = '{0}/{1}/{2}'.format(participantDay,participantMonth,participantYear)

    return participantDate


# Define a function that, given a list of all the dates in which the experiment was completed,
# derives a dictionary with each date as its key,
# with the number of participants completing the experiment on that date as the value

def deriveParticipantsPerDateDictionary(listOfDates):
    datesAndParticipantsDictionary = {}  # will contain each date with its corresponding number of participants

    for participantDate in listOfDates:
        # If the date is not already inside the dictionary, it is added and its value is set at 1
        # This is because the first time the date is encountered constitutes the first participant completing the experiment on that date
        if participantDate not in datesAndParticipantsDictionary:
            datesAndParticipantsDictionary[participantDate] = 1

        # Instead, if the date is already inside the dictionary, its value increases by 1
        # This is because another participant is encountered who completed the experiment on that date
        else:
            datesAndParticipantsDictionary[participantDate] += 1

    return datesAndParticipantsDictionary


# Define a function that isolates the files that are in the second list (results2.zip) but not in the first list (results.zip) and are not duplicates (these will be called 'novelFiles'), as well as isolates the duplicate files in the second list
# The parameter 'novelOrDuplicate' determines whether the function will isolate:
    # The novel files, if novelOrDuplicate == 'novelFiles'
    # The duplicate files, if novelOrDuplicate == 'duplicateFiles

def isolateNovelOrDuplicateFiles(results2,allParticipantData,novelOrDuplicate):
    novelFiles = []  # will contain file names in 'results2' not present in the first directory, which are not duplicates
    duplicateFiles = []  # will contain only the duplicate files in 'results2', like 'expABeth04062013211015a.csv' and 'expABeth04062013211015b.csv', but not the original 'expABeth04062013211015.csv'

    # The 5th index starting from the end (i.e. the -5th index) in each file name represents the character preceding '.csv'
    # Therefore, if the -5th index is a digit, the file name is not a duplicate (e.g. 'expABeth04062013211015.csv')
    # Alternatively, if the -5th index is an alphabetic character, the file name is a duplicate (e.g. 'expABeth04062013211015a.csv')
    criticalCharacterIndex = -5

    for eachParticipant in results2:  # access each participant's file for every loop
        if eachParticipant not in allParticipantData:
            # If the value of novelOrDuplicate is 'novelFiles', only the computations for novelFiles will be executed
            if novelOrDuplicate == 'novelFiles':
                if eachParticipant[criticalCharacterIndex].isdigit():
                    novelFiles.append(eachParticipant)

            # If the value of novelOrDuplicate is 'duplicateFiles', only the computations for duplicateFiles will be executed
            elif novelOrDuplicate == 'duplicateFiles':
                if eachParticipant[criticalCharacterIndex].isalpha():
                    duplicateFiles.append(eachParticipant)

    if novelOrDuplicate == 'novelFiles':
        return novelFiles
    elif novelOrDuplicate == 'duplicateFiles':
        return duplicateFiles


# Define a function that, given a list of file names present in 'results2.zip' but not in 'results.zip' which are not duplicates,
# and a list of duplicate files present in 'results2.zip',
# will create a list containing neither, hence will contain only file names that are neither novel nor duplicate

def deriveNoNovelNoDuplicatesList(results2,novelFiles,duplicateFiles):
    noNovelNoDuplicates = []

    for eachParticipant in results2:
        if (eachParticipant not in novelFiles) and (eachParticipant not in duplicateFiles):
            noNovelNoDuplicates.append(eachParticipant)

    return noNovelNoDuplicates


# Define a function that compares the number of files in the first list ('results' directory) with the second list ('results2' directory), while ignoring the novel and duplicate file names in the second list
# 'noNovelNoDuplicatesList' represents a list of all file names in 'results2.zip', except novel and duplicate files
# Therefore, the number of files in the first list will be compared with the 'noNovelNoDuplicatesList'
# The function will then write whether the number of files in the second list, while ignoring the extra files and duplicates files, is equal to, less than or more than the number of files in the first list

def compareFileNamesPerList(allParticipantData,noNovelNoDuplicatesList):
    numberOfFilesInFirstList = len(allParticipantData)
    numberOfFilesInSecondList = len(noNovelNoDuplicatesList)

    if numberOfFilesInFirstList == numberOfFilesInSecondList:
        summaryFile.write('\nWhen ignoring the extra files and the duplicate files, the number of files in the first list (results.zip) equals the number of files in the second list (results2.zip) i.e. {0} files. Therefore, the discrepancies between the 2 lists are indeed solely due to extra and duplicate files, rather than any additional problem.'.format(numberOfFilesInFirstList))
    elif numberOfFilesInSecondList < numberOfFilesInFirstList:
        summaryFile.write('\nThe number of files in the second list, when ignoring the extra and duplicate files, is less ({0}) than the number of files in the first list ({1}). Therefore, the discrepancies between the 2 lists are not solely due to extra and duplicate files, but there are other problems as well.'.format(numberOfFilesInSecondList,numberOfFilesInFirstList))
    else:
        summaryFile.write('\nThe number of files in the second list, when ignoring the extra and duplicate files, is more ({0}) than the number of files in the first list ({1}). Therefore, the discrepancies between the 2 lists are not solely due to extra and duplicate files, but there are other problems as well.'.format(numberOfFilesInSecondList,numberOfFilesInFirstList))


###################################################################################################
###################################################################################################
###################################################################################################


####  Creating the Summary File  ####

# The summary file will summarize:
    # The percentage of participants in each experiment (expA or expB)
    # The number of participants per date, during which both experiment versions were completed
    # The names of files in the second list (results2) not in the first list (results1), both novel and duplicates
    # Whether the number of files in the second list is the same with that in the first list, while ignoring novel and duplicate files

summaryFile = open('Summary File.txt','w')  # create the summary file at the location where the python file is saved
summaryFile.write('########################################\n'
                  '############  Summary File  ############\n'
                  '########################################\n\n\n')

totalParticipants = len(allParticipantData)  # will then be used to calculate the proportion of participants completing each experiment (expA or expB)

participantsExperimentA = 0  # will count the number of participants completing Experiment A
participantsExperimentB = 0  # will count the number of participants completing Experiment B

listOfDates = []  # will contain all the dates, which will later be sorted to arrange them in chronological order


# The same loop as Part A is created in Part B to keep the 2 parts separate, instead of mixing them
for participantFile in allParticipantData:  # access each participant's file per loop

    # Count the number of participants completing each experiment (expA or expB)
    # Each file name starts with either 'expA' or 'expB'
    # Therefore, if the file name starts with 'expA', the number of participantsExperimentA increases by 1
    # Alternatively, if the file name starts with 'expB', the number of participantsExperimentB increases by 1

    if participantFile.startswith('expA'):
        participantsExperimentA += 1
    else:
        participantsExperimentB += 1


    # Derive the date that the participant completed the experiment and append every date in listOfDates
    participantDate = deriveDate(participantFile)
    listOfDates.append(participantDate)


# Calculate the proportion of participants in each experiment (expA or expB), which will then be used to calculate percentages
participantProportionExpA = participantsExperimentA / totalParticipants
participantProportionExpB = participantsExperimentB / totalParticipants

# This format will be used to write in the summaryFile, and convert the proportions into percentages
writePercentageInSummaryFile = 'Percentage of Participants in {0}: {1:%}'

summaryFile.write(writePercentageInSummaryFile.format('Experiment A',participantProportionExpA))
summaryFile.write('\n' + writePercentageInSummaryFile.format('Experiment B',participantProportionExpB))


# Derive a dictionary containing each date in which the experiment was completed in chronological order, with the corresponding number of participants completing the experiment on that date
chronologicalListOfDates = sorted(listOfDates)  # sorts the listOfDates in chronological order
datesAndParticipantsDictionary = deriveParticipantsPerDateDictionary(chronologicalListOfDates)

summaryFile.write('\n\n\nDates that the Experiment was Completed and Number of Participants per Date:\n')

for date in datesAndParticipantsDictionary:  # access each date for every loop
    summaryFile.write('\n{0}:'.format(date))  # write the date in the summaryFile
    summaryFile.write(str(datesAndParticipantsDictionary[date]))  # write the number of participants on that date in the summaryFile


# Read the directory 'results2', which is at the same location with the python file
# This will later be compared with the initial directory 'results'
results2 = listdir('results2')


# This directory contains file names that are not present in the first directory (results.zip) i.e. 'novelFiles'
# It also contains duplicates (some files exist multiple times as 'expABeth04062013211015.csv', 'expABeth04062013211015a.csv' and 'expABeth04062013211015b.csv')
# The duplicate files contain the same information as the original (i.e. 'expABeth04062013211015.csv'), hence are redundant

# Isolating the novel and duplicate files
novelFiles = isolateNovelOrDuplicateFiles(results2,allParticipantData,'novelFiles')
duplicateFiles = isolateNovelOrDuplicateFiles(results2,allParticipantData,'duplicateFiles')


# Write in the summary file the names of files in the second list (results2.zip) but not in the first list (results.zip) which are not duplicates
summaryFile.write('\n\n\nNames of the Files in results2.zip, but not in results.zip, which are not Duplicates:\n')

for eachNovelParticipant in novelFiles:
    summaryFile.write('\n{0}'.format(eachNovelParticipant))


# Write in the summary file the names of the files in the second list with extra characters that constitute duplicates
summaryFile.write('\n\n\nNames of the Duplicate Files in results2.zip:\n')

for eachDuplicate in duplicateFiles:
    summaryFile.write('\n{0}'.format(eachDuplicate))


# Directory 'results2' has more files than directory 'results', as it contains novel and duplicate file names
# Therefore, if the discrepancies between the 2 directories are indeed due to the novel and duplicate file names,
# then removing the novel and duplicate file names should lead to the 2 directories having an equal number of files

# Creating a new list that will contain the files in 'results2' that are neither novel nor duplicates
# This list should therefore have the same number of files as the directory 'results'
noNovelNoDuplicatesList = deriveNoNovelNoDuplicatesList(results2,novelFiles,duplicateFiles)

# Lastly, determining whether the number of files in the first list is equal to the number of files in the second list (ignoring novel and duplicate files names) i.e. the noNovelNoDuplicatesList
# This will be calculated and written in the summary file by the function 'compareFileNamesPerList'
summaryFile.write('\n\n\nReport Summary:\n')
compareFileNamesPerList(allParticipantData,noNovelNoDuplicatesList)

summaryFile.close()
