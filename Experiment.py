###################################################################################################
###################################################################################################
###################################################################################################
################################           Coursework 2             ###############################
################################      Candidate Number: SKGR8       ###############################
###################################################################################################
###################################################################################################
###################################################################################################

#### This file contains the code regarding the user interface (the experiment) ####

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Experiment_Interface import *

from random import randint
from Functions import *

# Set up the windowed application
app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_AmbiguityAversionWindow()
ui.setupUi(window)


######## The experiment is written in a stacked widget ########
# Every page of the stacked widget contains one aspect of the experiment:
##    Index 0: Information Sheet
##    Index 1: Consent Form
##    Index 2: Demographics Questionnaire
##    Index 3: Experimental Task
##    Index 4: Choice Outcome
##    Index 5: Debrief


### Experimental task ###
# Participants will be presented with two urns, each containing red and blue marbles
# There are 3 conditions, whereby both urns contain either 2, 10 or 100 marbles each
# Each participant will complete only 1 condition
# In one of the urns, there is an equal number of blue and red marbles (known mix)
# In the other urn, there is a random mix of blue and red marbles (random mix)
# Participants are required to randomly draw a marble from 1 urn, and will enter a lottery draw if the marble is blue


####  Defining Classes and Functions ####


# Create a class of clickable labels
# These labels will contain images (Urn A or Urn B)
# Participants will indicate their choice (Urn A or B) by clicking on the corresponding image
class QClickableImage(QLabel):

    # Creating a custom signal for the class
    clicked = pyqtSignal()

    def mousePressEvent(self, mouseEvent):
        self.clicked.emit()

def checkConsent():
    if ui.checkBoxConsent.isChecked(): return True
    else:
        ui.lblConsentError.show()  # will indicate that participants must consent before continuing
        ui.consentArrow.show()  # a red arrow will appear next to the check box to clarify what participants must do before continuing
        
        window.nudgeItems.append(ui.consentArrow)  # every item in the 'nudgeItems' list will nudge (see functions 'ResetNudgeTimer()' and 'Nudge()' below)
        window.nudgeTimer.start(50)  # the red arrow will nudge to indicate what is required before continuing
        return False

# Define a function for when the 'next' button ('btnNext') is clicked
# The button will check for specific errors, based on the index of the stacked widget
# For instance, in the consent form, the function will check if the consent box was checked,
# and will not allow participants to continue unless they check the consent box
def NextPage():

    currentIndex = ui.stackedWidget.currentIndex()
    checkOK = True

    if currentIndex == 1: checkOK = checkConsent()
    


    # Information Sheet (index 0 of stacked widget)
    # Participants must simply read the page and click 'next' to continue
    if checkOK: ui.stackedWidget.setCurrentIndex(currentIndex+1)


    # Consent Form (index 1 of stacked widget)
    # The function will check if the participant checked the consent box
    elif currentIndex == 1:
    

    # Demographics Questionnaire (index 2 of stacked widget)
    # Participants are required to indicate their:
    ##   (a) Age: from a spin box
    ##   (b) Gender: from three radio buttons (male, female, other)
    ##   (c) Level of Education: from a combo box (secondary, college, undergraduate, postgraduate)
    elif currentIndex == 2:

        # If participants click 'next' without filling in all fields,
        # an error message will appear, describing which fields they have not yet answered
        # with a red arrow nudging next to those fields indicating the missing information

        errors = []  # will contain error messages for each field that was not answered
        ageError = 'Please indicate your age.'
        youngAgeError = 'You must be over 16 to participate in the experiment.'
        genderError = 'Please indicate your gender.'
        educationError = 'Please indicate your highest level of education.'

        ###  Age  ###
        # For ethical reasons, participants would not be allowed to participate below a certain age
        # Participant ages in the original experiment by Pulford and Colman (2008) ranged between 16-76
        # Therefore, the lowest age allowed to participate in the experiment will be 16
        if ui.spBoxAge.value() == 0: errors.append(ageError)
        elif ui.spBoxAge.value() < 16: errors.append(youngAgeError)

        ###  Gender  ###
        # The radio buttons for participants to indicate their gender are contained in a widget (widgetGender)
        # If one of the three buttons in the widget is checked, the 'noGender' boolean will become False
        noGender = True  # a boolean indicating whether participants reported their gender

        for gender in ui.widgetGender.children():
            if gender.isChecked(): noGender = False

        # Instead, if 'noGender' remains True, this will mark that participants did not indicate their gender
        if noGender: errors.append(genderError)

        ###  Education  ###
        # Index 0 of the education combo box reads 'Please indicate your highest level of education'
        # Therefore, if the current index is 0, this will mark that participants did not answer the field
        if ui.cmbBoxEducation.currentIndex() == 0: errors.append(educationError)

        ###  Error Message  ###
        errorMessage = '\n'.join(errors)  # every error message will appear in a new line

        # If the error message is empty, participants will move on to the experimental task
        # Their responses will also be saved in variables, which will later be written in the csv file
        if errorMessage == '':
            ui.stackedWidget.setCurrentIndex(3)
            ui.btnNext.hide()  # the 'btnNext' will be hidden in the experimental task, ensuring that participants will respond before continuing
            window.animateUrnsTimer.start(50)  # this will animate the urns until they reach their position (see function 'AnimateUrns()')

            window.participantAge = ui.spBoxAge.value()

            for gender in ui.widgetGender.children():
                if gender.isChecked(): window.participantGender = gender.objectName()

            window.participantEducation = ui.cmbBoxEducation.currentText()

        else:  # if the error message is not empty
            ui.lblDemogError.setText(errorMessage)

            # For every error, a red arrow will nudge next to the field with the missing information
            # When participants then provide the missing information but there is other information still missing,
            # the red arrow from the corrected field will be hidden when they click 'next'
            if (ageError in errorMessage) or (youngAgeError in errorMessage):
                ui.ageArrow.show()
                window.nudgeItems.append(ui.ageArrow)
            else: ui.ageArrow.hide()

            if genderError in errorMessage:
                ui.genderArrow.show()
                window.nudgeItems.append(ui.genderArrow)
            else: ui.genderArrow.hide()

            if educationError in errorMessage:
                ui.educationArrow.show()
                window.nudgeItems.append(ui.educationArrow)
            else: ui.educationArrow.hide()

            window.nudgeTimer.start(50)  # this will nudge the red arrows next to the missing information


    # Results Page (index 4 of stacked widget)
    # This page indicates the participant's choice outcome (whether they drew a blue or red marble)
    # Participants drawing a blue marble will have the option to provide their email address to be contacted if they win the draw
    # The participant's email address will be saved in a variable to be written in the csv file
    # The 'next' button will take them to the last page, so the button will be labelled as 'Finish' rather than 'Next'
    elif currentIndex == 4:
        window.participantEmail = ui.lineEditEmail.text()
        ui.stackedWidget.setCurrentIndex(5)
        ui.btnNext.setText('Finish')


    # Debrief Page (index 5 of stacked widget)
    # At this final page, participants' responses will be written in a new line in the csv file
    # This will not register participants' responses who may start but not complete the experiment
    # 'btnNext' is now labelled 'Finish', which will close the programme when clicked
    else:
        resultsCSV.write('\n{0},{1},{2},{3},{4},{5},{6}'.format(window.participantAge,window.participantGender,window.participantEducation,
                                                                participantCondition,window.urnPosition,window.selectedUrn,window.selectedMarble))

        if window.participantEmail != '': resultsCSV.write(',{0}'.format(window.participantEmail))  # this will not write an extra comma if:
                                                                                                    # the participant drew a red marble, hence did not provide their email address,
                                                                                                    # or if the participant drew a blue marble but did not provide their email address

        resultsCSV.close()
        sys.exit()


# Define a function that sets up the variables to nudge the red arrows next to the missing information
# The first time it is called, it will initialize the nudge variables
# Every other time the function is called, the variables will be reset
def ResetNudgeTimer():

    window.nudgeTimer = QTimer()  # set up a timer to animate the red arrows next to the missing information
    window.nudgeLeft = True  # set up a boolean to indicate whether the arrows will move to the left or right
    window.nudgeCounter = 0  # every time the arrow moves, the counter will increase by 1. When it reaches 4, the timer will stop and the arrows will stop nudging
    window.nudgeItems = []  # the list will contain every item that will animate (consent/age/gender/education arrow)
    window.nudgeTimer.timeout.connect(Nudge)


# Define a function to nudge the red arrows contained in the 'nudgeItems' list
def Nudge():

    # After an arrow nudged to the left/right, the nudgeLeft boolean will become false/true,
    # such that the arrow will next nudge to the right/left
    if window.nudgeLeft: window.nudgeLeft = False
    else: window.nudgeLeft = True

    for nudgeItem in window.nudgeItems:
        if window.nudgeLeft == False: nudgeItem.setGeometry(nudgeItem.x() + 10, nudgeItem.y(), nudgeItem.width(), nudgeItem.height())
        else: nudgeItem.setGeometry(nudgeItem.x() - 10, nudgeItem.y(), nudgeItem.width(), nudgeItem.height())

    window.nudgeCounter += 1
    if window.nudgeCounter == 4:
        window.nudgeTimer.stop()
        ResetNudgeTimer()  # reset the nudge variables


# The urns in the experiment page are set up outside the screen
# Define a function to animate the urns in the experiment page until they reach a specific position
def AnimateUrns():

    if leftUrn.x() < 80:
        leftUrn.setGeometry(leftUrn.x() + 10, leftUrn.y(), leftUrn.width(), leftUrn.height())
        rightUrn.setGeometry(rightUrn.x() - 10, rightUrn.y(), rightUrn.width(), rightUrn.height())
    else:
        window.animateUrnsTimer.stop()
        ui.lblUrnA.show()  # displays 'Urn A' below the left urn
        ui.lblUrnARatio.show()  # displays Urn A's red-blue marble ratio below 'Urn A'
        ui.lblUrnB.show()  # displays 'Urn B' below the right urn
        ui.lblUrnBRatio.show()  # displays Urn B's red-blue marble ratio below 'Urn B'

        # Enable urn clickability only after the animation ends, when the urns reach their position
        leftUrn.clicked.connect(OnUrnSelection)
        rightUrn.clicked.connect(OnUrnSelection)


# Define a function for when one urn in the experimental task is selected
# Participants will be allowed to select an urn only once
# When an urn is clicked, this function will start the timer to animate a hand, which will enter and leave the selected urn as if it selected a marble
def OnUrnSelection():

    if not window.selected:
        window.selected = True  # if an urn is clicked again, it will not enter the conditional, such that urns can be clicked only once

        # Identify which urn was selected to determine whether the hand will enter the left or right urn
        urnSignal = window.sender()
        if leftUrn.objectName() == urnSignal.objectName(): window.urnClicked = leftUrn
        else: window.urnClicked = rightUrn

        window.handDown = True  # set up a boolean to indicate whether the hand should animate down or up
        ui.Hand.raise_()  # bring the image of the hand to the front. This cannot be done from the designer, since the urn images are created in the code
        window.animateHandTimer.start(50)  # this will animate the hand (see function 'AnimateHand()' below)


# Define a function to animate the hand
# The hand's geometry will be set based on which urn was clicked (left/right urn will set the hand's geometry above the left/right urn)
# The hand will enter and leave the selected urn as if it selected a marble
def AnimateHand():

    handOffset = 10  # will be added to the hand's x coordinate to be positioned in the middle of the urn

    if window.handDown:  # the hand will animate downward, entering the urn
        ui.Hand.setGeometry(window.urnClicked.x() + handOffset, ui.Hand.y() + 15, ui.Hand.width(), ui.Hand.height())
        # When the hand's y-coordinate is 0, it will be located inside the urn,
        # so the handDown boolean will become True to move up
        if ui.Hand.y() == 0: window.handDown = False
    else:  # the hand will animate upward, leaving the urn
        ui.Hand.setGeometry(window.urnClicked.x() + handOffset, ui.Hand.y() - 15, ui.Hand.width(), ui.Hand.height())
        if ui.Hand.y() == -330:  # it will be located outside the screen
            window.animateHandTimer.stop()
            SelectMarble()  # the marble will be selected once the hand exits the screen
                            # Therefore, if participants keep clicking on the urn,
                            # this will not keep generating urn distributions and changing the outcome


# Define a function that sets up the random distribution for only the urn that was selected
# Based on that distribution, a random marble will be selected
# The marble drawn (blue or red) will be indicated in the next page of the experiment (index 4)
def SelectMarble():

    selectedUrnName = window.urnClicked.objectName()

    if selectedUrnName == 'knownUrn':
        window.selectedUrn = 1  # will be written in the csv file
        blueMarbles = totalMarbles / 2  # half the marbles are red and half the marbles are blue in the known-mix urn

    else:
        window.selectedUrn = 0
        blueMarbles = randint(0, totalMarbles)  # A random number will be selected between 0 and total marbles
                                                # to represent the number of blue marbles in the random-mix urn

    # The number of blueMarbles reflects the urn distribution, such that:
    # The marbles from 0 to 'blueMarbles' will be blue
    # The marbles from 'blueMarbles' to 'totalMarbles' will be red
    # For instance, in the 10-marble condition, if blueMarbles = 2,
    # the distribution will be 1,2 = blue and 3,4,...,10 = red
    # A random marble will be selected ('selectedMarble'), so there is no need to shuffle the distribution

    selectedMarble = randint(1, totalMarbles)  # selecting a random marble from 1 to the total number of marbles in each urn

    # Therefore, any number from 'blueMarbles' and lower will represent a blue marble, and
    # any number from 'blueMarbles' to 'totalMarbles' will represent a red marble
    if selectedMarble <= blueMarbles:
        window.selectedMarble = 'Blue'  # will be written in the csv file
        ui.lblResults.setText('Congratulations! You have drawn a blue marble!\nYou have entered the lottery draw to win £30!\n\nIf you wish, you can provide your email address below, so that we can contact you if you win the draw:')
    else:
        window.selectedMarble = 'Red'
        ui.lblResults.setText('Sorry! You have drawn a red marble...')

    # The next page will be shown, which animates the outcome (blue or red marble)
    ui.stackedWidget.setCurrentIndex(4)
    window.animateMarbleTimer.start(50)  # this will animate the result (see function 'AnimateMarble()' below)


# Define a function to animate the results
# A gray marble will 'fall' from the top to the middle of the screen
# When it reaches the middle of the screen, it will become either blue or red, printing a corresponding message
# If the marble drawn was blue, participants will also have the option to provide their email to be contacted with if they win the lottery draw
# The 'btnNext' will also appear for participants to move to the debrief
def AnimateMarble():

    if ui.grayMarble.y() < 360: ui.grayMarble.setGeometry(ui.grayMarble.x(), ui.grayMarble.y() + 10, ui.grayMarble.width(), ui.grayMarble.height())
    else:
        window.animateMarbleTimer.stop()
        ui.grayMarble.hide()
        ui.lblResults.show()
        ui.btnNext.show()

        if window.selectedMarble == 'Red': ui.redMarble.show()
        else:
            ui.blueMarble.show()
            ui.lineEditEmail.show()



####  Experiment  ####


# Create a csv file at the location where the python file is saved, which will store the participants' data (one participant per row)
resultsCSV = open('Experiment Results.csv','a')

# The contents of the csv file will also be read to determine whether:
##   (a) The participant completing the experiment is the first, whereby labels will be written in the first row of the csv file to indicate what each column will represent
##   (b) The participant's experimental condition (2, 10 or 100 marbles), to determine the next participant's condition
csvContent = open('Experiment Results.csv','r')
results = csvContent.readlines()
resultsLength = len(results)
csvContent.close()

# If nothing is written in the csv file, the length of the 'results' list will be 0
# Therefore, labels for what each column will represent will be written in the first row of the csv file
# The first participant will be assigned to the '2-marble' experimental condition
if resultsLength == 0:

    resultsCSV.write('Age,Gender,Level of Education,Condition (Number of Marbles in each Urn),Position of Urns (0 = Random Urn: B / 1 = Random Urn: A),Selected Urn (0 = Random / 1 = Known),Selected Marble,Email Address')
    participantCondition = 2

# Instead, if the csv file contains data, the 'results' list format will be converted to contain sublists, each containing one participant's data
# In order to ensure that each condition has the same number of participants,
# the last participant's condition will then be accessed (at index [-1][3]) to determine the current participant's condition
else:
    results = convertListFormat(results)
    participantCondition = deriveParticipantCondition(results)


#### Consent Form ####
ui.lblConsentError.hide()  # the error message will only appear if 'next' is clicked without consenting
ui.consentArrow.hide()  # the red arrow indicating what is required before continuing will only appear if 'next' is clicked without consenting
ResetNudgeTimer()  # call it once to initialize the nudge variables


#### Demographics Form ####
ui.ageArrow.hide()  # will only appear if the participant clicks 'next' without indicating their age
ui.genderArrow.hide()  # will only appear if the participant clicks 'next' without indicating their gender
ui.educationArrow.hide()  # will only appear if the participant clicks 'next' without indicating their education level


#### Experimental Task ####
# The decision task will be illustrated by two images of urns on either side of the screen, containing marbles
# The urns will be in grayscale, such that participants do not misinterpret colours as being representative of the urn distributions
# The urn with the random mix also has a question mark inside it to illustrate that its distribution is random
# Participants will indicate their choice (Urn A or B) by clicking on the image of the selected urn

# Set up two clickable labels on either screen side
# These are located outside of the screen and will animate to their position once the participant enters the experiment page
# Each will illustrate an image of either the known- or the random-mix urn
# This will be randomly determined by a randomly-generated value (the randomizer; see below)
leftUrn = QClickableImage(ui.Experiment)
leftUrn.setScaledContents(True)
leftUrn.setGeometry(-200, 190, 201, 281)

rightUrn = QClickableImage(ui.Experiment)
rightUrn.setScaledContents(True)
rightUrn.setGeometry(1260, 190, 201, 281)

# The following 4 labels will appear when the urns reach their position
ui.lblUrnA.hide()
ui.lblUrnARatio.hide()
ui.lblUrnB.hide()
ui.lblUrnBRatio.hide()

# Set up a timer to animate the urns to their position
window.animateUrnsTimer = QTimer()
window.animateUrnsTimer.timeout.connect(AnimateUrns)

# Set up two QPixmap objects, one for the known- and one for the random-mix urn images
# These will be assigned to either the leftUrn or the rightUrn, based on the randomizer
knownUrn = QPixmap('KnownUrn.png')
randomUrn = QPixmap('RandomUrn.png')


# To randomize which urn contains the known 50-50 mix or the random mix, a random number (the 'randomizer') will be generated from 0 to 1
# '0' will represent Urn A as the known 50-50 mix and Urn B as the random mix
# '1' will represent Urn A as the random mix and Urn B as the known 50-50 mix
# However, the left urn will remain Urn A, and the right urn will remain Urn B
# Part of the instructions will also change according to the randomizer value and the participant's condition (2, 10 or 100 marbles per urn)

randomizer = randint(0, 1)
window.urnPosition = randomizer  # save the urn positions in a clearly-named variable to be written in the csv file

if randomizer == 0:  # represents Urn A (left) as the known 50-50 mix and Urn B (right) as the random mix

    # Set up the urn images in the corresponding labels
    leftUrn.setPixmap(knownUrn)
    leftUrn.setObjectName('knownUrn')

    rightUrn.setPixmap(randomUrn)
    rightUrn.setObjectName('randomUrn')
    ui.lblUrnBRatio.setText('Unknown mix')

    if participantCondition == 2:
        totalMarbles = 2  # will be used to calculate the urn distribution
        ui.lblUrnARatio.setText('Known 1/1 mix')  # below Urn A, will indicate the red:blue marble ratio
        # The criticalInstructionParagraph is the paragraph in the experimental instructions that changes across conditions
        criticalInstructionParagraph = 'Urn A contains 1 red marble and 1 blue marble. Urn B contains 2 marbles in an unknown color ratio, from 2 red marbles and 0 blue marbles to 0 red marbles and 2 blue marbles. The mixture of red and blue marbles in Urn B has been decided by writing the numbers 0, 1, 2 on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into Urn B, but you do not know the number. Every possible mixture of red and blue marbles in Urn B is equally likely.'

    elif participantCondition == 10:
        totalMarbles = 10
        ui.lblUrnARatio.setText('Known 5/5 mix')
        criticalInstructionParagraph = 'Urn A contains 5 red marbles and 5 blue marbles. Urn B contains 10 marbles in an unknown color ratio, from 10 red marbles and 0 blue marbles to 0 red marbles and 10 blue marbles. The mixture of red and blue marbles in Urn B has been decided by writing the numbers 0, 1, 2, . . ., 10 on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into Urn B, but you do not know the number. Every possible mixture of red and blue marbles in Urn B is equally likely.'

    else:
        totalMarbles = 100
        ui.lblUrnARatio.setText('Known 50/50 mix')
        criticalInstructionParagraph = 'Urn A contains 50 red marbles and 50 blue marbles. Urn B contains 100 marbles in an unknown color ratio, from 100 red marbles and 0 blue marbles to 0 red marbles and 100 blue marbles. The mixture of red and blue marbles in Urn B has been decided by writing the numbers 0, 1, 2, . . ., 100 on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into Urn B, but you do not know the number. Every possible mixture of red and blue marbles in Urn B is equally likely.'

else:  # represents Urn A (left) as the random mix and Urn B (right) as the known 50-50 mix

    # Set up the urn images in the corresponding labels
    leftUrn.setPixmap(randomUrn)
    leftUrn.setObjectName('randomUrn')
    ui.lblUrnARatio.setText('Unknown mix')

    rightUrn.setPixmap(knownUrn)
    rightUrn.setObjectName('knownUrn')

    if participantCondition == 2:
        totalMarbles = 2
        ui.lblUrnBRatio.setText('Known 1/1 mix')  # below Urn B, will indicate the red:blue marble ratio
        criticalInstructionParagraph = 'Urn A contains 2 marbles in an unknown color ratio, from 2 red marbles and 0 blue marbles to 0 red marbles and 2 blue marbles. Urn B contains 1 red marble and 1 blue marble. The mixture of red and blue marbles in Urn A has been decided by writing the numbers 0, 1, 2 on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into Urn A, but you do not know the number. Every possible mixture of red and blue marbles in Urn A is equally likely.'

    elif participantCondition == 10:
        totalMarbles = 10
        ui.lblUrnBRatio.setText('Known 5/5 mix')
        criticalInstructionParagraph = 'Urn A contains 10 marbles in an unknown color ratio, from 10 red marbles and 0 blue marbles to 0 red marbles and 10 blue marbles. Urn B contains 5 red marbles and 5 blue marbles. The mixture of red and blue marbles in Urn A has been decided by writing the numbers 0, 1, 2, . . ., 10 on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into Urn A, but you do not know the number. Every possible mixture of red and blue marbles in Urn A is equally likely.'

    else:
        totalMarbles = 100
        ui.lblUrnBRatio.setText('Known 50/50 mix')
        criticalInstructionParagraph = 'Urn A contains 100 marbles in an unknown color ratio, from 100 red marbles and 0 blue marbles to 0 red marbles and 100 blue marbles. Urn B contains 50 red marbles and 50 blue marbles. The mixture of red and blue marbles in Urn A has been decided by writing the numbers 0, 1, 2, . . ., 100 on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into Urn A, but you do not know the number. Every possible mixture of red and blue marbles in Urn A is equally likely.'

ui.lblCriticalParagraph.setText(criticalInstructionParagraph)


# Set up a timer to animate the hand
window.animateHandTimer = QTimer()
window.animateHandTimer.timeout.connect(AnimateHand)
window.selected = False  # set up a boolean to indicate whether an urn has been selected, used to disallow participants from being able to select an urn multiple times


#### Results Page ####
# When the grayMarble reaches the middle of the screen,
# the lblResults will appear, indicating whether the participant drew a red or blue marble
# This will be reflected by the appearance of either the redMarble or the blueMarble
# If a blue marble was drawn, the lineEditEmail will also be shown to allow participants to provide their email to be contacted if they win the draw
ui.redMarble.hide()
ui.blueMarble.hide()
ui.lblResults.hide()  # this will appear when the grayMarble reaches the middle
ui.lineEditEmail.hide()  # this will only appear if the participant drew a blue marble

# Set up a timer to animate the marble drawn
window.animateMarbleTimer = QTimer()
window.animateMarbleTimer.timeout.connect(AnimateMarble)

ui.btnNext.clicked.connect(NextPage)

window.show()
sys.exit(app.exec_())
